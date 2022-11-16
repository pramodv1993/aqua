# -*- coding: utf-8 -*-
from s3path import S3Path
import pandas as pd


dataset = pd.read_csv('datasets/dataset.csv')
metrics = pd.read_csv('datasets/metrics.csv')
composition = pd.read_csv('datasets/global_size.csv')
names = dataset.name.unique()
#metrics
stage_1_metrics = [
 #(graphnum, metric name)   
                    (3, 'total_words_per_doc'),
                    (4, 'avg_word_length'), 
                    (5, 'total_num_sent'),
                    (6, 'avg_sent_length'),
                    (7, 'token_type_ratio'),
                    (8, 'symbol_word_ratio'),
                    (9, 'num_non_alphabet_words')]
stage_2_metrics = [(1, 'num_stop words'),
                    (2, 'num_abbreviations'),
                    (3, 'num_exact_dupl'),
                    (4, 'num_near_dup')]
stage_vs_metrics = {'stage1': stage_1_metrics, 'stage2': stage_2_metrics}

num_graphs = {'stage1': 9, 'stage2':4, 'stage3':2}



def filter_points(selected_datasets=None, ids=None):
    filtered = None
    if selected_datasets:
        filtered = dataset[dataset.name.isin(selected_datasets)]
    if ids:
        if filtered is not None:
            filtered = filtered[filtered.id.isin(ids)]
        else:
            filtered = dataset[dataset.id.isin(ids)]
    return filtered

def get_metrics_for_points(ids):
    return metrics[metrics.id.isin(ids)]

def update_filtered_points(prev_filtered, new_filtered):
    if prev_filtered is not None:
        new_filtered = pd.concat((prev_filtered, new_filtered))
        new_filtered = new_filtered.drop_duplicates(subset=['id'])
    return new_filtered

class S3PathBuilder:
    """
    to build document and metadata s3 path for querying and storage
    eg src path: s3://opengptx/datasources_ogptx/docs/v0.1.1/en/kelm
    """

    def __init__(self, **kwargs):
        self.config = kwargs
        if "bucket" not in kwargs:
            raise ValueError("No Bucket Name specified")
        self.base_path = S3Path(Path("/opengptx/datasources_ogptx/docs"))
        self.base_path /= self.config.get("version", "v0.1.2")

    """build doc s3 path"""

    def get_doc_path(self, src: str, lang: str = "en"):
        return self.base_path / "docs" / self.config["doc_version"] / lang / src

    """build metadata s3 path"""

    def get_metadata_path(self, src: str, lang: str = "en", corpus_level=False):
        return (
            self.base_path
            / "metadata"
            / "corpus_level"
            / self.config["metadata_version"]
            / lang
            / src
            if corpus_level
            else self.base_path
            / "metadata"
            / self.config["metadata_version"]
            / lang
            / src
        )

    """check if file exists in a given path"""

    def has_data(self, path: S3Path):
        return True if len(list(path.iterdir())) else False

    def get_rawdata_path(self, src: str):
        return S3Path(Path("/", self.base_path.parts[1], "raw", src))

    
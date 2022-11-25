# -*- coding: utf-8 -*-
from s3path import S3Path
import pandas as pd
import numpy as np


dataset = pd.read_csv('datasets/dataset.csv')
metrics = pd.read_csv('datasets/metrics.csv')
composition = pd.read_csv('datasets/global_size.csv')
bias = pd.read_csv('datasets/bias.csv')
toxic_words = pd.read_csv('datasets/toxic_words.csv')
names = dataset.name.unique()
final_points = dataset.id
metrics_vs_bounds = {metric: (None, None) for metric in metrics.columns[:-3]}
#metrics
stage_1_metrics = {
                    2: 'composition',
                    3: 'total_words_per_doc',
                    4:'avg_word_length', 
                    5: 'total_num_sent',
                    6: 'avg_sent_length',
                    7: 'token_type_ratio',
                    8: 'symbol_word_ratio',
                    9:'num_non_alphabet_words'}
stage_2_metrics = {1: 'num_stopwords_per_doc',
                    2: 'num_abbreviations_per_doc',
                    3: 'num_exact_duplicates',
                    4: 'num_near_duplicates'}

stage_3_metrics = {1: 'topic_distribution',
                    2: 'classifier_scores'}

stage_4_metrics = {1: 'toxicity',
                    2: 'bias'}
stage_vs_metrics = {1: stage_1_metrics, 2: stage_2_metrics, 3: stage_3_metrics, 4: stage_4_metrics}

def reset_metric_bounds():
    global metrics_vs_bounds
    metrics_vs_bounds = {metric: (None, None) for metric in metrics.columns[:-3]}

def get_bias_info_for_dataset(name):
    return bias[bias.name==name].values[0,2:]

def get_toxic_words_for_points(points):
    if points is None:
        return []
    words = toxic_words.sample(np.random.randint(len(toxic_words)))
    words.sort_values(by='score', ascending=False, inplace=True)
    return words

def apply_metric_filters():
    global metrics_vs_bounds
    final_res = metrics
    for metric, (lb, ub) in metrics_vs_bounds.items():
        if lb:
            final_res = final_res[final_res[metric]>=lb]
        if ub:
             final_res = final_res[final_res[metric]<=ub]
    return final_res.id

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

    
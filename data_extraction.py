from sklearn.base import BaseEstimator, TransformerMixin
from japanese_preprocessing.japanese_char_preprocessing import *
import numpy as np
import MeCab
import pandas as pd


class TextColumSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on text columns in the data
    """
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key]
    
    
class NumberColumSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on numeric columns in the data
    """
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key]


class DenseTransformer(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on numeric columns in the data
    """
    def __init__(self):
        self

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.todense()

    
class TextPreProcessor(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on text columns in the data
    """
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(self.split_line)


    #This method add space mark between word, remove words that useless or non-word characters
    def split_line(self, line):
        stop_words = ["時間", "|", "アルバイト", "パート", "パートナー", "社員", "～",
                  "≫", "≪", "-", "(", ")", "/", "）", "（", "<", " >", ":", "【", "】", "、"]

        #define none-value token types, this information provided by MeCab
        irrelevant_token_type = ['助詞-並立助詞', '助詞-格助詞-一般', '助詞-終助詞', '名詞-固有名詞-地域-一般',
                                 '名詞-接尾-地域', '名詞-数','記号-一般', '記号-括弧開', '助詞-連体化', '名詞-非自立-一般']

        mecab = MeCab.Tagger ("-Ochasen")
        line_token = []
        if(str(line)=="nan"):
            return ""
        for text in mecab.parse(line).split("\n"):
            if 'EOS' not in text and len(text.split())>0:
                tokens = text.split()
                #tokens[-1] is the word's type, tokens[0] is the word
                if tokens[-1] in irrelevant_token_type:
                    continue
                for stop_word in stop_words:
                    tokens[0] = tokens[0].replace(stop_word,"")
                if(len(tokens[0])==0):
                    continue
                else:
                    if tokens[0] == "の":
                        continue
                    line_token.append(tokens[0])
        return " ".join(line_token)
    

class KanjiFilter(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(lambda x: "".join(extract_unicode_block(kanji,x)))

    
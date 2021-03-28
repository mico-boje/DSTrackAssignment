from bs4 import BeautifulSoup
import requests
import nltk # Note that nltk.download() might need to be called to download the required packages
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import pandas as pd

class ArticleReader(object):
    def __init__(self):
        self.table = {}
        self.total_word_frequency = {}
        self.lemmatizer = WordNetLemmatizer()

    def data_reader(self, url: str):
        html = self._get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.find_all('doc'):
            docid = i.docid.string
            text = i.find_all('text')[0].get_text()
            lemmatized_words = self._get_lemmatized_words(text)
            self._set_table(lemmatized_words, int(docid))

    def get_table(self):
        return self.table

    def get_total_freq(self):
        return self.total_word_frequency

    def clear_table(self):
        self.table.clear()

    def _set_table(self, words: list, docid: int):
        count_dict = Counter(words)
        for key in count_dict.keys():
            if key in self.table:
                self.table[key].append([docid, count_dict[key]])
                self.total_word_frequency[key] += count_dict[key]
            else:
                self.table[key] = [[docid, count_dict[key]]]
                self.total_word_frequency[key] = count_dict[key]

    @staticmethod
    def _get_html(url: str) -> bytes:
        html = requests.get(url)
        return html.content

    def _get_lemmatized_words(self, text: str) -> list:
        tokens = word_tokenize(text)
        words = [word for word in tokens if word.isalpha()]
        lemmatized_words = [self.lemmatizer.lemmatize(word.lower()) for word in words]
        return lemmatized_words


a = ArticleReader()
a.data_reader(url='https://www.uva.nl/binaries/content/assets/programmas/information-studies/txt-for-assignment-data-science.txt')
hash_table = a.get_table()
print(hash_table)

# Plotting frequency distributions
freq_list = list(a.get_total_freq().values())
df = pd.DataFrame(freq_list, columns=['Frequency'])
import plotly.express as px
fig = px.histogram(df, x='Frequency', histnorm='percent')
fig.show()
print('Median: ', df.median())
print('Mean: ', df.mean())
print('Mode: ', df.mode())

#calculate skewness
from scipy.stats import skew, skewtest, kurtosis
print('Skewness: ', skew(df.Frequency))
print('Kurtosis: ', kurtosis(df.Frequency))


from bs4 import BeautifulSoup
import requests
import nltk # Note that nltk.download() might need to be called to download the required packages
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

class ArticleReader(object):
    def __init__(self):
        self.table = {}
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

    def _set_table(self, words: list, docid: int):
        count_dict = Counter(words)
        for key in count_dict.keys():
            if key in self.table:
                self.table[key].append([docid, count_dict[key]])
            else:
                self.table[key] = [[docid, count_dict[key]]]

    #This method could be integrated into data_reader, but for the sake of limiting a method to one function i've split it into two
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
#print(list(soup.children))
print(a.get_table())

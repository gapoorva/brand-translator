from nltk import download
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from collections import Counter
import math
import re
import statistics

regex = re.compile('[^a-zA-Z]')

def clean_word(w):
    return regex.sub('', w).lower()

class ContentProcessor():
    def __init__(self):
        self.documents = []
        self.documentnames = []
        self.stop_words = set(stopwords.words('english'))

    def add_document(self, filename, content):
        soup = BeautifulSoup(content, features="html.parser")

        paragraphtexts = Counter()
        for p in soup.find_all('p'):
            text = word_tokenize(p.get_text())
            paragraphtexts.update([ clean_word(w) for w in text if (not w in self.stop_words) and (len(clean_word(w)) > 2 ) ])

        self.documentnames.append(filename)
        self.documents.append(paragraphtexts)

    def tfidf_scoring(self):
        BENCHMARK_IDF = 4.3
        BENCHMARK_TF = 0.0035

        # for testing
        idf_scores = []

        # create inverted index matrix
        num_docs = len(self.documentnames)
        inverted_idx = {}
        print('start building inverted index...')

        for i in range(len(self.documents)):
            doc = self.documents[i]
            words_in_doc = len(doc)
            for w in doc:
                if w not in inverted_idx:
                    inverted_idx[w] = {
                        'tfscores': [0] * num_docs,
                        'idfscore': 0,
                    }

                inverted_idx[w]['tfscores'][i] += (doc[w] / words_in_doc)

        print('calculate term frequencies', len(inverted_idx))

        for w in inverted_idx:
            mentioned_docs = 0
            for tf in inverted_idx[w]['tfscores']:
                if tf > 0:
                    mentioned_docs += 1
            inverted_idx[w]['idfscore'] = math.log(num_docs / mentioned_docs)
            idf_scores.append(inverted_idx[w]['idfscore'])

            inverted_idx[w]['deleted'] = inverted_idx[w]['idfscore'] < BENCHMARK_IDF

        print('mean of idf scores', statistics.mean(idf_scores))
        print('median of idf scores', statistics.median(idf_scores))
        print('stddev of idf scores', statistics.stdev(idf_scores))

        print('remove corpus-specific stop words')

        sig_words = { w: stats['tfscores'] for w, stats in inverted_idx.items() if not stats['deleted'] }

        doc_sig_words = []
        for i in range(num_docs):
            doc_sig_words.append(set())

        print('find document-specific keywords', len(sig_words))

        for w, tfscores in sig_words.items():
            for i in range(len(tfscores)):
                if tfscores[i] > BENCHMARK_TF:
                    doc_sig_words[i].add(w)

        final_docs = {}

        words_written = []

        for i in range(len(self.documentnames)):
            name = self.documentnames[i]
            final_docs[name] = ' '.join(doc_sig_words[i])
            words_written.append(len(doc_sig_words[i]))

        print('mean of words written', statistics.mean(words_written))
        print('median of words written', statistics.median(words_written))
        print('stddev of words written', statistics.stdev(words_written))

        return final_docs



    def old_tfidf_scoring(self):
        vectorizer = TfidfVectorizer(min_df=0.2, token_pattern='[a-zA-Z]{2,}')
        X = vectorizer.fit_transform(self.documents)
        words = np.array(vectorizer.get_feature_names())

        docs = {}

        for i in range(X.shape[0]):
            row = X.getrow(i)
            rel_words = [ words[j] for j in row.indices ]
            docs[self.documentnames[i]] = ' '.join(rel_words)

        return docs
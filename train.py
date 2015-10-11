import argparse
import cPickle as pickle
import nltk.tokenize
import numpy as np
import random
from bs4 import BeautifulSoup
from glob import glob
from nltk.corpus import cmudict


print 'Loading CMU dictionary...'
cmudict.ensure_loaded()
cmudict_loaded = cmudict.dict()

FILTERED_CHARS = {'.', ',', '!', ':', ';', '?'}


def fetch_corpus():
    try:
        sonnets = pickle.load(open('sonnets.pickle', 'rb'))
        print 'Loaded sonnets.pickle'
    except IOError:
        sonnets = []

        for f in glob('corpus/*.html'):
            print 'Reading file', f
            parser = BeautifulSoup(open(f).read(), 'lxml')
            sonnet = parser.find(id='sonnet').find('p').text.lower()

            tokens = nltk.tokenize.wordpunct_tokenize(sonnet)
            filtered = [''.join([w for w in sentence if w not in FILTERED_CHARS]) for sentence in tokens]
            filtered = filter(lambda w: w, filtered)
            sonnets.append(filtered)

        print 'Read %d sonnets' % len(sonnets)
        pickle.dump(sonnets, open('sonnets.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
    return sonnets


def ngrams(corpus, n=2):
    for i in xrange(0, len(corpus) - n):
        yield tuple(map(lambda s: s.lower(), corpus[i:i + n]))


# TODO: only rhymes on the last two "sounds" (not sure of the jargon)
# TODO: only checks the first pronunciation
def check_rhyme(a, b):
    try:
        return tuple(w[0] for w in cmudict_loaded[a][0])[-2:] == tuple(w[0] for w in cmudict_loaded[b][0])[-2:]
    except KeyError:
        # implies one of the words is invalid, like punctuation or a typo
        return False


def generate(cfd, word, num=50):
    sonnet = []
    sentence = []
    for i in xrange(num):
        sentence.append(word)

        words, frequencies = zip(*cfd[word].items())
        frequencies = np.array(frequencies)

        attempts = 0
        while attempts < 1000:
            word = np.random.choice(words, p=frequencies / float(frequencies.sum()))
            attempts += 1
            if len(sonnet) == 0 or (i + 1) % 6 != 0:
                # no need to enforce rhyming on first sentence or non-final words
                break
            if check_rhyme(sonnet[-1][-1], word):
                break
        else:
            print 'Warning: word "%s" on line %d won\'t rhyme' % (word, len(sonnet))

        if (i + 1) % 6 == 0:
            sentence = ' '.join(sentence)
            sentence = sentence[0].upper() + sentence[1:]
            sonnet.append(sentence)
            sentence = []
    return sonnet


def train(start_word=None):
    sonnets = fetch_corpus()
    tokens = sum(sonnets, [])
    cfd = nltk.ConditionalFreqDist(ngrams(tokens))

    sonnet = generate(cfd, word=start_word if start_word else random.choice(tokens))

    div = '-' * max(len(line) for line in sonnet)
    print '\n\n' + div
    print ',\n'.join(sonnet)
    print div + '\n\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a sonnet.')
    parser.add_argument('--start', help='A starting token to init the algorithm', default=None)
    args = parser.parse_args()
    train(args.start)

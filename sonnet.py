import argparse
import cPickle as pickle
import nltk.tokenize
import numpy as np
import random
import string
from bs4 import BeautifulSoup
from glob import glob
from nltk.corpus import cmudict


FILTERED_CHARS = {'.', ',', '!', ':', ';', '?'}
RHYMABLE_SET = set(string.ascii_letters + "'")
MAX_ATTEMPTS = 1000
CORPUS_CACHE_PATH = 'sonnets.v2.pickle'

# Corresponds to index pairs with matching rhyming for
# abab-cdcd-efef-gg
# 0101-2323-4545-66
RHYMING_SCHEME = [
    (0, 2),
    (1, 3),
    (4, 6),
    (5, 7),
    (8, 10),
    (9, 11),
    (12, 13),
]

print 'Loading CMU dictionary...'
cmudict.ensure_loaded()
cmudict_loaded = cmudict.dict()


def fetch_corpus():
    try:
        sonnets = pickle.load(open(CORPUS_CACHE_PATH, 'rb'))
        print 'Loaded', CORPUS_CACHE_PATH
    except IOError:
        sonnets = []

        valid = set(RHYMABLE_SET)
        valid.add('\n')
        valid.add(' ')

        for f in glob('corpus/*.html'):
            print 'Reading file', f
            parser = BeautifulSoup(open(f).read())
            text = parser.find(id='sonnet').find('p').text.lower()

            tokens = filter(lambda c: c in valid, text).split()
            sonnets.append(tokens)

        print 'Read %d sonnets' % len(sonnets)
        pickle.dump(sonnets, open(CORPUS_CACHE_PATH, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
    return sonnets


def ngrams(corpus, n=2):
    for i in xrange(0, len(corpus) - n):
        yield tuple(map(lambda s: s.lower(), corpus[i:i + n]))


def clean_token(s):
    return filter(lambda c: c in RHYMABLE_SET, s.lower())


# TODO: only checks the first pronunciation
def check_rhyme(a, b):
    a = clean_token(a)
    b = clean_token(b)

    try:
        return tuple(w[0] for w in cmudict_loaded[a][0])[-2:] == tuple(w[0] for w in cmudict_loaded[b][0])[-2:]
    except KeyError:
        # implies one of the words is invalid, like punctuation or a typo
        return False


def sonnet_rhyming_score(lines):
    assert len(lines) == 14
    # for a, b in RHYMING_SCHEME:
    #     print a, b, lines[a][-1], lines[b][-1], check_rhyme(lines[a][-1], lines[b][-1])
    return sum(check_rhyme(lines[a][-1], lines[b][-1]) for a, b in RHYMING_SCHEME) / float(len(RHYMING_SCHEME))


def to_properly_cased_string(words):
    sentence = ' '.join(words)
    sentence = sentence[0].upper() + sentence[1:]
    return sentence


def to_properly_cased_sonnet(sentences):
    return map(to_properly_cased_string, sentences)


def sample_word_from_cfd(cfd, word):
    words, frequencies = zip(*cfd[word].items())
    frequencies = np.array(frequencies)
    return np.random.choice(words, p=frequencies / float(frequencies.sum()))


# TODO
def num_syllables(sentence):
    return 0


def generate(cfd, word, lines=14):
    best = None
    best_score = -1

    for attempt in xrange(1, MAX_ATTEMPTS + 1):
        sonnet = []
        sentence = []
        while lines > len(sonnet):
            sentence.append(word)

            word = sample_word_from_cfd(cfd, word)

            if len(sentence) % 6 == 0:
                sonnet.append(sentence)
                sentence = []

        score = sonnet_rhyming_score(sonnet)
        if best_score < score:
            best_score = score
            best = sonnet
        if best_score == 1.0:
            break

    print 'Generated a sonnet with score %.2f in %d attempts' % (best_score, attempt)
    return best


def train(start_word=None):
    sonnets = fetch_corpus()
    tokens = sum(sonnets, [])
    cfd = nltk.ConditionalFreqDist(ngrams(tokens))

    sonnet = generate(cfd, word=start_word if start_word else random.choice(tokens))
    sonnet = to_properly_cased_sonnet(sonnet)

    div = '-' * max(len(line) for line in sonnet)
    print '\n\n' + div
    print ',\n'.join(sonnet)
    print div + '\n\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a sonnet.')
    parser.add_argument('--start', help='A starting token to init the algorithm', default=None)
    args = parser.parse_args()
    train(args.start)

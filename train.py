import nltk.tokenize
import random
import cPickle as pickle
from glob import glob
from bs4 import BeautifulSoup
from nltk.corpus import cmudict

FILTERED_CHARS = {'.', ',', '!', ':', ';', '?'}

try:
    sonnets = pickle.load(open('sonnets.pickle'))
    print 'Loaded sonnets.pickle'
except:
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


def ngrams(corpus, n=2):
    for i in xrange(0, len(corpus) - n):
        yield tuple(map(lambda s: s.lower(), corpus[i:i + n]))


def generate(cfd, word='the', num=50):
    sonnet = []
    sentence = []
    for i in xrange(num):
        arr = []  # make an array with the words shown by proper count
        for j in cfd[word]:
            for k in xrange(cfd[word][j]):
                arr.append(j)

        sentence.append(word)
        word = arr[int((len(arr)) * random.random())]

        if (i + 1) % 6 == 0:
            sentence = ' '.join(sentence)
            # sentence = ''.join([sonnet[-1][0].upper()] + sonnet[-1][1:])
            sonnet.append(sentence)
            sentence = []
    return sonnet

tokens = sum(sonnets, [])
cfd = nltk.ConditionalFreqDist(ngrams(tokens))
print '\n\n'
sonnet = generate(cfd, word=random.choice(tokens))
print ',\n'.join(sonnet)
print '\n\n'

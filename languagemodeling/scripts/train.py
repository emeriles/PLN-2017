"""Train an n-gram model.

Usage:
  train.py -n <n> [-m <model>] -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from sys import exit

from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer

from languagemodeling.ngram import NGram, AddOneNGram



def _get_sents(filename):

    pattern = r'''(?ix)    # set flag to allow verbose regexps
          (?:sr\.|sra\.)
        | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
        | \w+(?:-\w+)*        # words with optional internal hyphens
        | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
        | \.\.\.            # ellipsis
        | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
    '''

    tokenizer = RegexpTokenizer(pattern)

    corpus = PlaintextCorpusReader('.', filename, word_tokenizer=tokenizer)
    return corpus.sents()

if __name__ == '__main__':
    opts = docopt(__doc__)

    #get parameters and check them
    model_n = int(opts['-n'])
    filename = opts['-o']
    try:
        model_t = opts['-m']
    except:
        model_t = 'ngram'
    if (model_t not in {'ngram', 'addone'}):
        print ('Wrong -m parameter. Expected \'ngram\' or \' addone\'')
        exit()

    # train the model in the chosen mode
    sents = _get_sents(filename)        #  TO DO: alert when file not found
    if (model_t == 'ngram'):
        ngram = NGram(model_n, sents)
    else:
        ngram = AddOneNGram(model_n, sents)

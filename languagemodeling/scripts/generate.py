"""Generate natural language sentences using a language model.

Usage:
  generate.py -i <file> -n <n>
  generate.py -h | --help

Options:
  -i <file>     Language model file.
  -n <n>        Number of sentences to generate.
  -h --help     Show this screen.
"""
from docopt import docopt

from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer

from languagemodeling.ngram import NGram, NGramGenerator
N = 3     # N stands for the N-gram model to be used


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


def main():
    opts = docopt(__doc__)

    # get parameters
    nsents = int(opts['-n'])
    filename = opts['-i']

    # get sentences                     TO DO: alert when file not found
    corpus = _get_sents(filename)
    # train the model with n-grams
    ngram = NGram(N, corpus)
    generator = NGramGenerator(ngram)

    # generate and print sentences
    for i in range(nsents):
        _pretty_print(generator.generate_sent())


def _pretty_print(list_str):
    """Prints a list of tokens as a string"""
    out_str = ''
    for word in list_str:
        out_str += ' ' + word
    print(out_str)


if __name__ == '__main__':
    main()

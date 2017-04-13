# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from random import random, choice
from math import log


class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)
        self.probs = {}
        self.sorted_probs = {}
        self.beginning_words = []       # used to generate random sentences

        # Avoid underflow by adding beginning and ending characters in sents
        for sent in sents:
            self.beginning_words.insert(0, sent[0])
            for x in range(n-1):
                sent.insert(0, "<s>")
            sent.insert(len(sent), "</s>")

        # Make the ngrams (and n-1-grams) aparitions
        for sent in sents:
            for i in range(len(sent) - n + 1):
                    ngram = tuple(sent[i: i + n])
                    counts[ngram] += 1
                    counts[ngram[:-1]] += 1

        # begin self.probs construction
        # it's a dictionary with tuples as keys, and dictionaries as values.
        # those last dictionaries have strings as keys and floats as values

        # Algorithm: take every n-length segment of sentence seen, calculate
        # the conditional probability and try to append it to the dictionary
        # of the (n-1)-gram that worked as key. if it doesn't exist
        # the dictionary is initialized as equals to {}

        # get all n-length tuples that were actually counted
        nlen_tuples = {k for k in counts.keys() if len(k) == n}
        for tok_tuple in nlen_tuples:
            tup_beg = tok_tuple[:-1]   # take the beginning of the tuple
            tup_end = tok_tuple[-1:]   # take the last element of tuple
            # Simple convertion to string, so as to use as a dict key.
            tup_end_str = ''.join(tup_end)
            # convert tup_end to string, to use as a dictionary key
            # calculate conditional probability
            cond_p = self.cond_prob(tup_end_str, prev_tokens=list(tup_beg))
            assert(cond_p > 0)  # as all tok_tuple were seen once at least
            # try to insert {tup_end_str: cond_p} to the correct dictionary
            try:
                self.probs[tup_beg][tup_end_str] = cond_p
            except Exception:
                self.probs[tup_beg] = {}
                self.probs[tup_beg][tup_end_str] = cond_p
        # end self.probs construction

        # begin self.sorted_probs construction

        # same as self.probs, only that the values of the tuples-keys is now
        # a list.
        for toks_tuple, dic in self.probs.items():
            # convert the dictionary to list
            list_dic = [(k, v) for k, v in dic.items()]
            list_dic.sort()
            self.sorted_probs[toks_tuple] = list_dic

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]

        denom_count = self.counts[tuple(prev_tokens)]
        # avoid division by zero
        if (denom_count == 0):
            ret = 0
        else:
            ret = float(self.counts[tuple(tokens)]) / denom_count
        return ret

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self.counts[tuple(tokens)]

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        prob = 1.0
        n = self.n
        # insert end an beginning of sentence-markers
        for x in range(n-1):
            sent.insert(0, "<s>")
        sent.insert(len(sent), "</s>")
        # the probabiliy wanted is the multiplication of conditional probs
        for i in range(n-1, len(sent)):
            prob *= self.cond_prob(sent[i], sent[i+1-n: i])
        return prob

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        prob = 0.0
        n = self.n

        # just a simple alias to call base 2 logarithm
        def log2(x): return log(x, 2)

        # insert end an beginning of sentence-markers
        for x in range(n-1):
            sent.insert(0, "<s>")
        sent.insert(len(sent), "</s>")
        # the probaility wanted is the sum of log(conditional probabilities)
        for i in range(n-1, len(sent)):
            prob_cond = self.cond_prob(sent[i], sent[i+1-n: i])
            if (prob_cond != 0):
                prob += log2(prob_cond)
            else:
                return float('-inf')
        return prob


class NGramGenerator:

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.model = model
        self.probs = model.probs
        self.sorted_probs = model.sorted_probs

    def generate_sent(self):
        """Randomly generate a sentence."""
        n = self.model.n
        beginning_tokens = self.model.beginning_words
        first_token = choice(beginning_tokens)
        sent = [''.join(first_token)]
        while True:
            if (n != 1):
                new_token = self.generate_token(tuple(sent[-n+1:]))
            else:
                new_token = self.generate_token(tuple([]))
            sent.insert(len(sent), new_token)
            if (new_token == '</s>'):
                break
        return (sent[:-1])  # take of the '</s>'

    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.

        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.model.n
        rand = random()
        acum = 0
        # add necessary beginning of sentence marks, so that it can be found
        # on sorted_probs
        while (len(prev_tokens) <= n-2):
            prev_tokens = ('<s>',) + prev_tokens
        # simple inverse transformed sampling in ordered discrete probabilities
        for string, prob in self.sorted_probs[prev_tokens]:
            if (rand < prob + acum):
                return string
            acum += prob

# https://docs.python.org/3/library/collections.html
from collections import defaultdict
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

        for sent in sents:
            for x in range(n-1):
                sent.insert(0, "<s>")
            sent.insert(len(sent), "</s>")

        for sent in sents:
            for i in range(len(sent) - n + 1):
                    ngram = tuple(sent[i: i + n])
                    counts[ngram] += 1
                    counts[ngram[:-1]] += 1

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
        for x in range(n-1):
            sent.insert(0, "<s>")
        sent.insert(len(sent), "</s>")
        for i in range(n-1, len(sent)):
            prob *= self.cond_prob(sent[i], sent[i+1-n: i])
        return prob

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        prob = 0.0
        n = self.n

        def log2(x): return log(x, 2)

        for x in range(n-1):
            sent.insert(0, "<s>")
        sent.insert(len(sent), "</s>")
        for i in range(n-1, len(sent)):
            prob_cond = self.cond_prob(sent[i], sent[i+1-n: i])
            if (prob_cond != 0):
                prob += log2(prob_cond)
            else:
                return float('-inf')
        return prob

import os 
from itertools import product
import re
import random
import numpy as np
import math
from collections import Counter, defaultdict
from typing import List, Tuple
import pickle

# Helper functions to save/load class ass Model
def save_model(model, filepath: str) -> None:
    with open(filepath, "wb") as f:
        pickle.dump(model, f)

def load_model(filepath: str):
    with open(filepath, "rb") as f:
        model = pickle.load(f)
    return model

"""
# Save Model
model = ngram(n=2, korpus=raw_text)
save_model(model, "bigram_model.pkl")

# Load Model
model_loaded = load_model("bigram_model.pkl")
print(model_loaded.generate("das wetter", 10))
"""


class ngram:
    def __init__(self, n: int, korpus: str, smoothing: bool = False):
        """
        Input:
            n         : int (order of n-gram)
            korpus    : str (training text)
            smoothing : bool (add-one smoothing flag)
        """
        self.n = n
        self.smoothing = smoothing
        self.toks = self.init_toks(korpus)
        self.vocab, self.vocab_count = self.init_vocab()
        self.counts = self.count()

    def init_toks(self, korpus: str) -> List[List[str]]:
        """
        Tokenize text into sentences (list of token lists).
        """
        text_no_p = re.sub(r"[^\w\s;.?!]", "", korpus)
        text_no_p = re.sub(r"([;.?!])", r" \1", text_no_p)
        text_no_p_ends = re.sub(r"([?!;.])", r"\1 </s>|||<s> ", text_no_p)
        text_no_p_ends = "<s> " + text_no_p_ends + " </s>"
        text_no_p_ends = text_no_p_ends.lower()
        tokens = re.findall(r'</s>|<s>|\w+|[;.!?]', text_no_p_ends)

        toks: List[List[str]] = []
        group: List[str] = []
        for tok in tokens:
            group.append(tok)
            if tok == "</s>":
                toks.append(group)
                group = []
        return toks

    def random_unk(self) -> None:
        """
        Replace some tokens with frequency == 1 by "<UNK>".
        """
        for i, cnt in enumerate(self.vocab_count):
            if cnt == 1:
                start_idx = i
                break
        idx_range = range(start_idx, len(self.vocab_count))
        choices = [random.choice(idx_range) for _ in range(10)]
        for i in choices:
            rare = self.vocab[i]
            for sent in self.toks:
                for j, w in enumerate(sent):
                    if w == rare:
                        sent[j] = "<UNK>"
            self.vocab[i] = "<UNK>"

    def init_vocab(self) -> Tuple[List[str], List[int]]:
        """
        Build vocab (tokens sorted by count) and their counts.
        """
        counter = Counter(tok for sent in self.toks for tok in sent)
        items = counter.most_common()
        vocab, vocab_count = zip(*items)
        return list(vocab), list(vocab_count)

    def count(self) -> defaultdict:
        """
        Build n-gram counts (context → Counter of next tokens).
        """
        counts = defaultdict(Counter)
        for sent in self.toks:
            for i in range(len(sent) - self.n + 1):
                ctx = tuple(sent[i : i + (self.n - 1)])
                nxt = sent[i + self.n - 1]
                counts[ctx][nxt] += 1

        if self.smoothing:
            for ctx in counts:
                for w in self.vocab:
                    counts[ctx][w] += 1
        return counts

    def next_word(self, seed: str) -> str:
        """
        Return one next token given seed.
        """
        toks = seed.lower().split()
        while len(toks) < self.n - 1:
            toks.insert(0, "<s>")
        ctx = tuple(toks[-(self.n - 1) :])
        counter = self.counts.get(ctx)
        if not counter:
            return random.choice(self.vocab)
        words, weights = zip(*counter.items())
        return random.choices(words, weights=weights, k=1)[0]

    def generate(self, seed: str, length: int) -> str:
        """
        Generate sequence of up to `length` tokens from seed.
        """
        toks = seed.lower().split()
        while self.n > 1 and len(toks) < self.n - 1:
            toks.insert(0, "<s>")
        for _ in range(length):
            ctx = " ".join(toks[-(self.n - 1) :])
            nxt = self.next_word(ctx)
            toks.append(nxt)
            if nxt == "</s>":
                break
        return " ".join(toks)

    def len_grams(self) -> int:
        """
        Return total number of unique (context → next token) entries.
        """
        if self.n == 1:
            return len(self.counts.get((), {}))
        return sum(len(counter) for counter in self.counts.values())

    def ppx(self, test_set: str) -> float:
        """
        Compute perplexity on a test string.
        """
        test_sents = self.init_toks(test_set)
        N = sum(max(0, len(sent) - self.n + 1) for sent in test_sents)
        V = len(self.vocab)
        log_sum = 0.0
        for sent in test_sents:
            for i in range(len(sent) - self.n + 1):
                ctx = tuple(sent[i : i + (self.n - 1)])
                nxt = sent[i + self.n - 1]
                count_ctx_w = self.counts.get(ctx, Counter()).get(nxt, 0)
                count_ctx = sum(self.counts.get(ctx, Counter()).values())
                num = count_ctx_w + 1
                denom = count_ctx + V
                prob = num / denom
                log_sum += -math.log(prob)
        return math.exp(log_sum / N)

def save_model(model, filepath: str) -> None:
    """
    Speichert das gegebene ngram-Modell in eine Datei.

    Input:
        model    : ngram-Instanz
        filepath : str (Pfad zur Datei, z.B. "model.pkl")
    Output:
        None (schreibt binär in filepath)
    """
    with open(filepath, "wb") as f:
        pickle.dump(model, f)


def load_model(filepath: str):
    """
    Lädt ein ngram-Modell aus einer Datei und gibt die Instanz zurück.

    Input:
        filepath : str (Pfad zur Datei, z.B. "model.pkl")
    Output:
        ngram-Instanz (vom gespeicherten Modell)
    """
    with open(filepath, "rb") as f:
        model = pickle.load(f)
    return model







import re
from collections import defaultdict
import os
import random
import numpy as np

class ngram:
    def __init__(self, n : int, korpus : str, smoothing = False):
        self.korpus = korpus
        self.n = n

        # [["<s>", "bla", "blub", </s>], [...], [...], [...]]
        self.text_normalized_noInterP_withSeg_asList = []
        self.num_vocab = [[int, str]]
        self.prepare()

        self.table = np.zeros([len(self.num_vocab)] * n, dtype=int)
        
    def prepare(self):
        # Alle Interpunktionszeichen außer \w \s ; . ? ! entfernen
        text_no_p = re.sub(r"[^\w\s;.?!]", "", self.korpus)
        # Leerzeichen vor jedem übrigen Punktionszeichen setzen
        text_no_p = re.sub(r"([;.?!])", r" \1", text_no_p)

        # Satzgrenzen
        text_no_p_ends = re.sub(r"([?!;.])", r"\1 </s>|||<s> ", text_no_p)
        text_no_p_ends = "<s> " + text_no_p_ends + " </s>"

        text_no_p_ends = text_no_p_ends.lower()

        self.text_normalized_noInterP_withSeg_asList = [s.split(" ") for s in text_no_p_ends.split("|||")]

        for sentence in self.text_normalized_noInterP_withSeg_asList:
            for s in sentence.split(" "):
                self.num_vocab[s] += 1

        self.num_vocab = list([val, key] for key, val in self.num_vocab.items())

        for i, (num, word) in enumerate(self.num_vocab):
            if num == 1:
                begin = i
                break

        start_end_indexes = list(range(begin, len(self.num_vocab)))

        choosen = []

        for _ in range(10):
            rand_idx = random.choice(start_end_indexes)
            choosen.append(rand_idx)
            start_end_indexes.remove(rand_idx)

        for i in choosen:
            self.num_vocab[i][1] = "<UNK>"


    def train(self):
        

if __name__ == "__main__":
    raw_text = ""

    for txt in os.listdir("korpus"):
        with open(f"korpus/{txt}", "r", encoding="utf-8") as f:
            content = f.read()
    
        raw_text += content + " "

    
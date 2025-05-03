class ngram:
    def __init__(self, n : int, korpus : str, smoothing = False):
        self.korpus = korpus
        self.n = n

        # [["<s>", "bla", "blub", </s>], [...], [...], [...]]
        self.toks = self._init_toks()
        print("Korpus Verarbeitet")

        # [["bla", 100], ["blub",50], ["blib", 20], [...], [...]]
        self.num_vocab = self._init_num_vocab()
        print("Vokabular erstellt")

        # Index Dict for Table
        self.vocab_index = {key : idx for idx, (key, val) in enumerate(self.num_vocab)}

        self.counts = self._count()

        self.probs = self._normalize(smoothing)
        



    def _init_toks(self):
        # Alle Interpunktionszeichen außer \w \s ; . ? ! entfernen
        text_no_p = re.sub(r"[^\w\s;.?!]", "", self.korpus)
        # Leerzeichen vor jedem übrigen Punktionszeichen setzen
        text_no_p = re.sub(r"([;.?!])", r" \1", text_no_p)

        # Satzgrenzen
        text_no_p_ends = re.sub(r"([?!;.])", r"\1 </s>|||<s> ", text_no_p)
        text_no_p_ends = "<s> " + text_no_p_ends + " </s>"

        text_no_p_ends = text_no_p_ends.lower()

        text_no_p_ends_list = re.findall(r'\w+|<s>|</s>|[;.!?]', text_no_p_ends)

        # Each sentence gets a whole list
        toks = []
        group = []

        for tok in text_no_p_ends_list:
            group.append(tok)

            if tok == "</s>":
                toks.append(group)
                group = []

        return toks

    def _init_num_vocab(self):
        num_vocab = defaultdict(int)
        for sentence in self.toks:
            for w in sentence:
                num_vocab[w] += 1

        num_vocab = list([key, val] for key, val in num_vocab.items())
        num_vocab = list(sorted(num_vocab, key=lambda x : x[1], reverse=True))

        return num_vocab


    def _count(self):
        table = np.zeros([len(self.num_vocab)] * self.n, dtype=int)

        for sentence in self.toks:
            for idx in range(len(sentence)):
                if idx + self.n > len(sentence):   # genug Tokens vorhanden?
                    break

                indices = [
                    self.vocab_index[sentence[idx + j]]
                    for j in range(self.n)
                ]

                # for i in indices:
                #     print(f"{self.num_vocab[i][0]} ", end="")
                
                # print("+++")
                
                table[tuple(indices)] += 1           # N-gram hochzählen
        
        return table
    
    def _normalize(self, smoothing):
        counts = self.counts.astype(float)

        if smoothing:
            counts += 1
            print("Smoothing angewendet")
        
        denoms = counts.sum(axis=-1, keepdims=True)

        probs = counts / denoms
        return probs


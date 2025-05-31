###############################################
######## Beispiel nutzung               #######
######## Siehe readme für Beispiele     #######
###############################################
from my_ngram import ngram
import os

raw_text = ""
for datei in os.listdir("korpus"):
    if datei.endswith(".txt"):
        with open(f"korpus/{datei}", "r", encoding="utf-8") as f:
            raw_text += f.read() + " "



lm3 = ngram(n=3, korpus=raw_text, smoothing=False)

out = a1.generate("<s> es war", 10)

print(out)

###############################################
######## Beispiel nutzung               #######
######## Siehe readme für Beispiele     #######
###############################################


"""
# Save Model
model = ngram(n=2, korpus=raw_text)
save_model(model, "bigram_model.pkl")

# Load Model
model_loaded = load_model("bigram_model.pkl")
print(model_loaded.generate("das wetter", 10))
"""


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


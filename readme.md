### Installation
just `pip install -r requirements.txt` inside cloned repo

### Hier eine kurzgefasste Anleitung, wie du die `ngram`-Klasse einsetzen kannst:

1. **Korpus vorbereiten**
   Lies alle Textdateien deines Korpus (z. B. im Ordner `korpus/`) ein und füge sie zu einem großen String zusammen:

   ```python
   import os

   raw_text = ""
   for datei in os.listdir("korpus"):
       if datei.endswith(".txt"):
           with open(f"korpus/{datei}", "r", encoding="utf-8") as f:
               raw_text += f.read() + " "
   ```

2. **Modell erstellen**
   Importiere die Klasse und initialisiere sie mit der gewünschten Ordnung `n`.

   * `n=1` → Unigramm,
   * `n=2` → Bigramm,
   * `n=3` → Trigramm, usw.
     Standardmäßig ist kein Smoothing aktiv.

   ```python
   from ngram_model import ngram

   # Beispiel: Bigramm ohne Glättung
   model = ngram(n=2, korpus=raw_text, smoothing=False)
   ```

3. **Text generieren**
   Mit `generate(seed, length)` kannst du vom „Seed“-String aus neue Wörter vorhersagen.

   * `seed`: Anfangswort oder -satz (wird intern in Kleinbuchstaben umgewandelt).
   * `length`: maximale Anzahl zusätzlicher Tokens, die generiert werden.

   ```python
   start = "das wetter"
   generated = model.generate(seed=start, length=10)
   print(generated)  
   # Mögliche Ausgabe: "das wetter ist heute sehr schön . </s>"
   ```

   Sobald das Token `</s>` (Satzende) erzeugt wird, bricht die Generierung ab.

4. **Perplexität berechnen**
   Um zu messen, wie gut dein Modell auf einem Testtext ist, rufst du
   `ppx(test_text)` auf:

   ```python
   test_text = "Das ist ein kurzer Test ."
   ppx_wert = model.ppx(test_text)
   print("Perplexität:", ppx_wert)
   ```

   Ein niedrigerer Wert bedeutet, dass das Modell den Text besser vorhersagen kann.

5. **Größe der gelernten n-Gramme abfragen**
   Mit `len_grams()` bekommst du die Anzahl aller unterschiedlichen (Kontext → Folgewort)-Paare:

   ```python
   anzahl = model.len_grams()
   print("Anzahl unique n-Gramme:", anzahl)
   ```

6. **Seltene Wörter durch `<UNK>` ersetzen (optional)**
   Falls du dein Vokabular verkleinern möchtest, kannst du mit `random_unk()` zufällig seltene Wörter (Häufigkeit = 1) durch `"<UNK>"` ersetzen:

   ```python
   model.random_unk()
   # Danach verändert sich das Vokabular: seltene Wörter werden zu "<UNK>"
   ```

   Nachdem du `random_unk()` aufgerufen hast, solltest du – falls nötig – das Modell neu instanziieren, damit die neuen `<UNK>`-Token korrekt eingearbeitet werden.

---

### Zusammenfassung der wichtigsten Methoden

* **Konstruktor:**

  ```python
  ngram(n: int, korpus: str, smoothing: bool=False)
  ```

  * `n` = Ordnung des n-Gramm-Modells
  * `korpus` = großer Text-String (alle Sätze)
  * `smoothing=True` aktiviert Add-One-Smoothing (Laplace-Glättung)

* **Texterzeugung:**

  ```python
  generate(seed: str, length: int) → str
  ```

  Gibt vom Anfangs-„seed“ aus bis zu `length` neue Tokens (bzw. bis `</s>`) zurück.

* **Nächstes Wort vorhersagen:**

  ```python
  next_word(seed: str) → str
  ```

  Liefert genau ein Wort basierend auf dem letzten Kontext.

* **Perplexität:**

  ```python
  ppx(test_set: str) → float
  ```

  Berechnet die Perplexität des Modells auf dem übergebenen Testtext.

* **Anzahl gelernter n-Gramme:**

  ```python
  len_grams() → int
  ```

  Zeigt die Anzahl aller (Kontext→Folgewort)-Kombinationen.

* **Seltene Wörter ersetzen:**

  ```python
  random_unk()
  ```

  Wandelt zufällig einige seltene Wörter in `"<UNK>"` um.

---

Mit diesen wenigen Schritten kannst du dein n-Gramm-Modell aufbauen, neue Texte generieren und die Modellqualität über Perplexität bewerten. Ende.



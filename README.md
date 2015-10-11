# sonnet-155
Generate sonnets trained on Shakespeare et al., where a sonnet has the constraints:
* 14 lines
* **todo** 10 syllables per line
* **todo** Rhyming scheme (e.g. _abab-cdcd-efef-gg_)

## Prepping corpus
```bash
cd corpus
./download.sh
```

## Install requirements
```bash
pip install -r requirements.txt
# download cmudict
python -c 'import nltk; nltk.download()'
# verify
python -c 'from nltk.corpus import cmudict; cmudict.ensure_loaded()'
```

## Verify unit tests pass
```bash
py.test
```

## Run
```bash
python train.py
```
```
Still shine bright in his blood,
Make the marigold at the sun,
Staineth let him advantage on thy,
Abundance am now crown themselves be,
Broken while shadows doth put on,
All oblivious enmity shall live no,
Time to be crossed prison my,
Nobler part nor dare not the
```

Well said indeed.


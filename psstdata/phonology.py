import json

from psstdata import assets

PAD = "<pad>"
UNK = "<unk>"
SIL = "<sil>"
SPN = "<spn>"

VOCAB_ARPABET_JSON = assets.path("vocab_arpabet.json")  # redundancy alert

with open(VOCAB_ARPABET_JSON) as f:
    VOCAB_ARPABET = json.load(f)

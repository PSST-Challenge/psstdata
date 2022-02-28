from psstdata import assets

PAD = "<pad>"
UNK = "<unk>"
SIL = "<sil>"
SPN = "<spn>"

VOCAB_ARPABET_JSON = assets.path("vocab_arpabet.json")  # redundancy alert
VOCAB_ARPABET = {
    "<pad>": 0,
    "AA": 1,
    "AE": 2,
    "AH": 3,
    "AO": 4,
    "AW": 5,
    "AY": 6,
    "B": 7,
    "CH": 8,
    "D": 9,
    "DH": 10,
    "DX": 11,
    "EH": 12,
    "ER": 13,
    "EY": 14,
    "F": 15,
    "G": 16,
    "HH": 17,
    "IH": 18,
    "IY": 19,
    "JH": 20,
    "K": 21,
    "L": 22,
    "M": 23,
    "N": 24,
    "NG": 25,
    "OW": 26,
    "OY": 27,
    "P": 28,
    "R": 29,
    "S": 30,
    "SH": 31,
    "T": 32,
    "TH": 33,
    "UH": 34,
    "UW": 35,
    "V": 36,
    "W": 37,
    "Y": 38,
    "Z": 39,
    "ZH": 40,
    "<sil>": 41,
    "<spn>": 42,
    "<unk>": 43
}
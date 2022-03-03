import psstdata.assets
from psstdata._system import read_json

PAD = "<pad>"
UNK = "<unk>"
SIL = "<sil>"
SPN = "<spn>"

VOCAB_ARPABET_JSON = psstdata.assets.path("vocab_arpabet.json")
VOCAB_ARPABET = read_json(VOCAB_ARPABET_JSON, dict)

ACCEPTED_PRONUNCIATIONS = read_json(psstdata.assets.path("correctness.json"), dict)

PROMPTS_BNT = (
    'house',
    'comb',
    'toothbrush',
    'octopus',
    'bench',
    'volcano',
    'canoe',
    'beaver',
    'cactus',
    'hammock',
    'stethoscope',
    'unicorn',
    'tripod',
    'sphinx',
    'palette'
)

PROMPTS_VNT = (
    'cut',
    'bark',
    'put',
    'send',
    'drive',
    'wash',
    'read',
    'laugh',
    'watch',
    'give',
    'swim',
    'stir',
    'pinch',
    'crawl',
    'deliver',
    'pour',
    'howl',
    'throw',
    'bite',
    'shove',
    'tickle',
    'shave',
)
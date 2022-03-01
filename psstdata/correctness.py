import psstdata.assets
from psstdata._system import read_json

CORRECT_PRONUNCIATIONS_BNT = read_json(psstdata.assets.path("correctness_bnt.json"), dict)
CORRECT_PRONUNCIATIONS_VNT = read_json(psstdata.assets.path("correctness_vnt.json"), dict)

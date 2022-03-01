# psstdata

This package downloads the data for the [PSST challenge](https://psst.study).

## If you run into issues

First, note that this package was developed for and tested using Python 3.8, so switching to this version may serve as a workaround for some problems. If you still have problems, we'll be keeping an eye on [the project's issue tracker](https://github.com/PSST-Challenge/psstdata/issues).

## Access to the data

The data is hosted on TalkBank, and protected by password. To get the password and participate in the challenge, please complete [this form](https://docs.google.com/forms/d/e/1FAIpQLScwAC3j7NQ2giyFSjrNen6NhmSbnHqdxS915ftZDBRi2SHQtQ/viewform).

The `psstdata` tools will prompt for these credentials upon the first download. Credentials are thereafter stored in `~/.config/psstdata/settings.json`, and the data files are kept in `~/psst-data`. (Tip: you can change where data is stored in the `settings.json`)

### Just the data, please!

If you're not using Python, or you'd like write your data-loading code, you can download the data set directly 
from TalkBank. Once you have the password, head over to our resource page at [TalkBank](https://media.talkbank.org/aphasia/RaPID/). 

## Installation
With a minimum of Python 3.? installed, `psstdata` can be installed using `pip`:
```bash
pip install psstdata
```

- TSVs are similar in structure, different in length.
- relative paths start at ..

## Contents

In addition to corpus downloading, this package contains a few additional resources that could get you set up more quickly. These are referenced in the [baseline systems](https://github.com/PSST-Challenge/psstbaseline), which you are certainly welcome to use as an example or a jumping off point!

(Key: `python reference` — [json file]())

- **ARPAbet symbols** (and integer mappings)
  - `psstdata.VOCAB_ARPABET` — [psstdata/assets/vocab_arpabet.json](psstdata/assets/vocab_arpabet.json)  
  - `psstdata.VOCAB_ARPABET_JSON` (the filename for above)
- **"Correct" pronunciations for the BNT/VNT tasks:**
  - `psstdata.CORRECT_PRONUNCIATIONS_BNT` — [psstdata/assets/correctness_bnt.json](psstdata/assets/correctness_bnt.json) 
  - `psstdata.CORRECT_PRONUNCIATIONS_VNT` — [psstdata/assets/correctness_vnt.json](psstdata/assets/correctness_vnt.json)

## Basic usage

```python
>>> import psstdata

>>> data_asr = psstdata.load_asr()

psstdata INFO: Downloading a new data version: 2022-03-01
psstdata INFO: Loaded data `asr` version 2022-03-01 from /Users/bobby/psst-data

>>> data_correctness = psstdata.load_correctness()

psstdata INFO: Loaded data `correctness` version 2022-03-01 from /Users/bobby/psst-data
```

This will download data to the default directory (`~/psst-data/`) and return an object of type `PSSTData`, containing the `train`, `valid`, and `test` splits:

```python
>>> len(data_asr.train)

2173

>>> len(data_asr.valid)

325

>>> len(data_asr.test)

624
```

And each of those sets is a `PSSTUtteranceCollection`, which is a collection of `PSSTUtterance`:

```python
>>> data_asr.train[0]

PSSTUtterance(id='ACWT02a-BNT01-house', session='ACWT02a', prompt='house', transcript_ipa="haʊ's", transcript_arpabet='HH AW S', filename='train/audio/bnt/ACWT02a/ACWT02a-BNT01-house.wav', duration_frames=12752, code='C', aq_index=74.6, is_correct=True)

>>> data_asr.train['ACWT02a-BNT01-house']

PSSTUtterance(id='ACWT02a-BNT01-house', session='ACWT02a', prompt='house', transcript_ipa="haʊ's", transcript_arpabet='HH AW S', filename='train/audio/bnt/ACWT02a/ACWT02a-BNT01-house.wav', duration_frames=12752, code='C', aq_index=74.6, is_correct=True)
```


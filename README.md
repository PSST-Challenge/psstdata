# psstdata

This package downloads the data for the [PSST challenge](https://psst.study).

## Just the data, please!

If you're not using Python, or you'd like write your own code to parse the files, you can download the data set directly 
from TalkBank. See [the challenge guidelines](https://psst.study/join/) for more details.

## Installation
With a minimum of Python 3.X installed, `psstdata` can be installed using `pip`:
```bash
pip install psstdata
```

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


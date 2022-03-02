# psstdata

This package downloads the data for the [PSST challenge](https://psst.study).

## If you run into issues

First, note that this package was developed for and tested using Python 3.8 (MacOS and Linux), so switching to this version may serve as a workaround for some problems. If you still have problems, we'll be keeping an eye on [the project's issue tracker](https://github.com/PSST-Challenge/psstdata/issues).

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

>>> data = psstdata.load()

psstdata INFO: Downloading a new data version: 2022-03-02
psstdata INFO: Loaded data version 2022-03-02 from /Users/bobby/psst-data

```

This will download data to the default directory (`~/psst-data/`) and return an object of type `PSSTData`, containing the `train`, `valid`, and `test` splits:

```python
>>> len(data.train)

2298

>>> len(data.valid)

341

>>> len(data.test)

652
```

And each of those sets is a `PSSTUtteranceCollection`, which is a collection of `PSSTUtterance`:

```python
>>> data.train[0]

PSSTUtterance(utterance_id='ACWT02a-BNT01-house', session='ACWT02a', test='BNT', prompt='house', transcript='HH AW S', aq_index=74.6, correctness=True, filename='audio/bnt/ACWT02a/ACWT02a-BNT01-house.wav', duration_frames=12752)

>>> data.train['ACWT02a-BNT01-house']

PSSTUtterance(utterance_id='ACWT02a-BNT01-house', session='ACWT02a', test='BNT', prompt='house', transcript='HH AW S', aq_index=74.6, correctness=True, filename='audio/bnt/ACWT02a/ACWT02a-BNT01-house.wav', duration_frames=12752)
```

## Uninstalling

Removing the package can be accomplished using pip:
`pip uninstall psstdata`

You may also want to delete the data and configs (Copy/paste `rm -rf` commands cautiously, of course!!)
- Data: `rm -rf ~/psst-data`
- Configs: `rm -rf ~/.config/psstdata`

# psstdata

This package downloads the data for the [PSST challenge](https://psst.study).

[![DOI](https://zenodo.org/badge/464440318.svg)](https://zenodo.org/badge/latestdoi/464440318)

<style>
  .bibliography { padding: 2em; text-indent: -2em; }
</style>

## Citing This Work

<p class="bibliography">
Robert C. Gale, Mikala Fleegle, Gerasimos Fergadiotis, and Steven Bedrick. 2022. 
<a href="https://aclanthology.org/2022.rapid-1.6">The Post-Stroke Speech Transcription (PSST) Challenge</a>.
In Proceedings of the RaPID Workshop - Resources and ProcessIng of linguistic, para-linguistic and extra-linguistic Data 
from people with various forms of cognitive/psychiatric/developmental impairments - within the 13th Language Resources 
and Evaluation Conference, pages 41–55, Marseille, France. European Language Resources Association.
</p>

<p class="bibliography">
Robert Gale, Mikala Fleegle, Steven Bedrick, and Gerasimos Fergadiotis. 2022. 
<a href="https://zenodo.org/record/6326002#.ZF2wicHMKvA">Dataset and tools for the PSST Challenge on Post-Stroke Speech Transcription.</a>
March. Project funded by the National Institute on Deafness and Other Communication Disorders 
grant number R01DC015999-04S1.
<a href="https://zenodo.org/badge/latestdoi/464440318"><img src="https://zenodo.org/badge/464440318.svg" alt="DOI: 10.5281/zenodo.6326002"></a>
</p>

<p class="bibliography">
Brian MacWhinney, Davida Fromm, Margaret Forbes, and Audrey Holland. 2011.
<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3424615/">AphasiaBank: Methods for Studying Discourse.</a> 
Aphasiology, 25(11):1286–1307.
Supported by NIH-NIDCD R01-DC008524 (2022-2027).
</p>

## Access to the data

The data is hosted on TalkBank, and protected by password. To get the password and participate in the challenge, please complete [this form](https://docs.google.com/forms/d/e/1FAIpQLScwAC3j7NQ2giyFSjrNen6NhmSbnHqdxS915ftZDBRi2SHQtQ/viewform).

The `psstdata` tools will prompt for these credentials upon the first download. Credentials are thereafter stored in `~/.config/psstdata/settings.json`, and the data files are kept in `~/psst-data`. (Tip: you can change where data is stored in the `settings.json`)

### Just the data, please!

If you're not using Python, or you'd like write your data-loading code, you can download the data set directly 
from TalkBank. Once you have the password, head over to our resource page at [TalkBank](https://media.talkbank.org/aphasia/RaPID/). 

### Usage Notes

Conditions for using the PSST Dataset are described on the [task website](https://psst.study).

## Setup

First, please note that this package was developed for and tested using Python 3.8 (MacOS and Linux), so switching to 
this version may serve as a workaround for some problems.

With a minimum of Python 3.? installed, `psstdata` can be installed using `pip`:

```bash
pip install psstdata  # Install python helpers
python -m psstdata    # Download `./psst-data` into your user directory (437MB on disk)
```

The python helpers include data loader tools. For more information, see [Basic Usage](#basic-usage).

## Contents

### Data Packs
The data retrieved by this tool is described in detail in each data pack's README file. A copy of those files is available in this repository for each of the [train](readme/train/README.md), [valid](readme/valid/README.md), and [test](readme/test/README.md) data packs. (These three files have only trivial differences.)

### Additional Resources
This tool also provides some additional resources to get you set up more quickly. These are referenced in the [baseline systems](https://github.com/PSST-Challenge/psstbaseline), which you are certainly welcome to use as an example or a jumping off point!

(Key: `python reference` — [json file]())

- **ARPAbet symbols** (and integer mappings)
  - `psstdata.VOCAB_ARPABET` — [psstdata/assets/vocab_arpabet.json](psstdata/assets/vocab_arpabet.json)  
  - `psstdata.VOCAB_ARPABET_JSON` (the filename for above)
- **"Correct" pronunciations for the BNT/VNT tasks:**
  - `psstdata.ACCEPTED_PRONUNCIATIONS` — [psstdata/assets/correctness.json](psstdata/assets/correctness.json) 

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

However, you'll basically only need four fields:

```python
# Print the first four records in the train data

for utterance in data.train[:4]:

    # The key ingredients
    utterance_id = utterance.utterance_id
    transcript = utterance.transcript
    correctness = "Y" if utterance.correctness else "N"
    filename_absolute = utterance.filename_absolute

    print(f"{utterance_id:26s} {transcript:26s} {correctness:11s} {filename_absolute}")

    
""" utterance_id           transcript                 correctness filename_absolute

ACWT02a-BNT01-house        HH AW S                    Y           /Users/bobby/audio/bnt/ACWT02a/ACWT02a-BNT01-house.wav
ACWT02a-BNT02-comb         K OW M                     Y           /Users/bobby/audio/bnt/ACWT02a/ACWT02a-BNT02-comb.wav
ACWT02a-BNT03-toothbrush   T UW TH B R AH SH          Y           /Users/bobby/audio/bnt/ACWT02a/ACWT02a-BNT03-toothbrush.wav
ACWT02a-BNT04-octopus      AA S AH P R OW G P UH S    N           /Users/bobby/audio/bnt/ACWT02a/ACWT02a-BNT04-octopus.wav
"""
```


## Uninstalling

Removing the package can be accomplished using pip:
`pip uninstall psstdata`

You may also want to delete the data and configs (Copy/paste `rm -rf` commands cautiously, of course!!)
- Data: `rm -rf ~/psst-data`
- Configs: `rm -rf ~/.config/psstdata`

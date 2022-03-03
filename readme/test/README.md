# PSST Data Pack README

This data pack contains audio files and labels for the PSST Challenge: https://psst.study

This is the **test** partition of the PSST Challenge dataset, and should contain data and labels for 652 productions.

The contents of this data pack are organized as follows:

### The `./audio` directory

The "audio" directory contains sub-directories for the BNT and VNT naming tasks (see task description for more details)

- Within each task directory, there is a subdirectory for each session (e.g. "elman11a")
- Within each session directory, there is a .wav file for each test item (e.g. "elman11a-BNT01-house.wav")
- The naming scheme is consistent across instances, but not all items are present for all speakers
- The audio files are mono audio recordings in standard PCM format, at a sampling rate of 16 kHz and a bitrate of 256 kb/s

### The `./utterances.tsv` file

The labels are in the file "utterances.tsv", which is a UTF-8 encoded, tab-separated file with the following fields:

  - `utterance_id` is a unique identifier for each production, of the form {session}-{test}{item}-{prompt} (e.g. "ACWT02a-BNT01-house")
  - `session` is the name of the AphasiaBank session from which the production was taken
  - `test` indicates which test each utterance comes from, either `BNT` (Boston Naming Test) or `VNT` (Verb Naming Test)
  - `prompt` is an orthographic rendering of the target word
  - `transcript` is the phonemic transcription of the production, in ARPAbet.
      - Silence is marked using `<sil>`
      - Spoken noise is marked using `<spn>`
  - `correctness` is marked as `TRUE` if the production is "correct" according to the clinical scoring rules of the BNT/VNT, `FALSE` otherwise
      - For task 2 (correctness), this is the outcome label
  - `aq_index` is the participant's Aphasia Quotient (AQ).  AQ is the Western Aphasia Battery - Revised Aphasia Quotient (Kertesz, 2007) and it is a standardized total score that reflects overall aphasia severity. Values can fall between between 0.0 and 100.0. A lower number indicates higher severity.
  - `duration_frames` is the number of audio frames in each recording, or the duration in seconds times 16000
  - `filename` contains the relative path within the data pack to the file containing the audio recording for this production

For any questions about the contents of this data pack, please contact Robert Gale (galer@ohsu.edu) and Steven Bedrick (bedricks@ohsu.edu)
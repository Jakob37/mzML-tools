Collection for basic interaction with the strange world that is proteomic file formats.

Cross-checking with OpenMS tools is done, but there is no guarantee that everything is in order after
processing.

Currently working tool is 'SubsetMzML', a basic utility for extracting a subset of the spectras from
an existing mzML tool. Coming from the sequencing field, subsetting FASTA and FASTQ files was a trivial
task which was a central part for me while testing out software. In proteomics this is not so straight-forward,
and I have yet to find another tool similar to seqtk that does this (hats of to OpenMS though, who has some
great tools).

# Instructions

To perform a basic check of number of spectras in the file:

```
python3 SubsetMzML --input <target.mzML> --check_only
```

Perform subsetting based on the number of MS1 spectra you want to retain:

```
python3 SubsetMzML --input <target.mzML> --output <out.mzML> --ms1_count 100
```

If your mzML file is indexed, you need to use an additional flag:

```
python3 SubsetMzML --input <target.mzML> --output <out.mzML> --ms1_count 100 --is_indexed
```

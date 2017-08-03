Collection for basic interaction with the strange world that is proteomic file formats.

Cross-checking with OpenMS tools is done, but there is no guarantee that everything is in order after
processing.

Currently working tool is 'SubsetMzML', a basic utility for extracting a subset of the spectras from
an existing mzML tool. Coming from the sequencing field, subsetting FASTA and FASTQ files was a trivial
task which was a central part for me while testing out software. In proteomics this is not so straight-forward,
and I have yet to find another tool similar to seqtk that does this (hats of to OpenMS though, who has some
great tools).

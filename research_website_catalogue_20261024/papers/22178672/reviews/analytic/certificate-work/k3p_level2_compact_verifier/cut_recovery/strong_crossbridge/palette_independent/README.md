# Self-contained noncut witness evidence

This directory removes the generic noncut argument's dependence on the
companion JC pointwise cut theorem.

`enumerate_balanced_word_reduction.py` exhausts all 808,642 balanced binary
word distributions with four through eight active ports.  It proves that
each has a three-run path obstruction or reduces to the finite short palette,
with singleton doubling when needed.  `verify_reduced_palette_cleanroom.py`
independently builds the five directed primitive cores, validates the rooted
and fixed-mixed presentations, enumerates 379,742 valid direct or
singleton-doubled palette presentations, and finds no split displayed by
every switching.  The two programs share no project graph or switching code.

`verify_cut_combinatorics.py` reruns both computations and requires their
outputs to agree byte-for-byte with the committed certificates.
`verify_displayed_tree_minor.py` independently checks the exact quartet-tree
Fourier determinant used in the handwritten boundary-specialization proof.

The historical 808,642 count in the frozen JC manuscript is therefore an
active reproducibility checksum here, not a premise imported on trust.

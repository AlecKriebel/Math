# Manuscript build

From the research-program root, the full exact reproduction command is:

```bash
make paper1
```

This runs the unit tests, the independent verifier, rebuilds the manuscript,
and installs the PDF under `output/pdf/`.

To compile only the manuscript from this directory, run:

```bash
tectonic main.tex
```

The manuscript is self-contained.  Its short related-work section was added
only after the theorem and verifier completed independent hostile review, in
accordance with the discovery embargo.

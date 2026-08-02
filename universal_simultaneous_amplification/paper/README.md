# Manuscript build

From the research-program root, the full exact reproduction command is:

```bash
make paper1
```

This runs the undirected and directed obstruction checks, the triangle and
symmetric-`K_4` exact certificates, the asymptotic lumping checks, and the
independent full-state cross-checks.  It then rebuilds the manuscript and
installs the PDF under `output/pdf/`.

To compile only the manuscript from this directory, run:

```bash
tectonic main.tex
```

The manuscript is self-contained.  Its short related-work section was added
only after the theorem and verifier completed independent hostile review, in
accordance with the discovery embargo.

The released environment used Python 3.14.6, SymPy 1.14.0, and Tectonic
0.16.9.  SymPy is pinned in `requirements.txt`; any compatible Tectonic
installation can build the document.

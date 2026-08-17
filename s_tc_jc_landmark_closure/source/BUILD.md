# Deterministic manuscript build

Requirements: Tectonic 0.15 or later with its standard cached bundle.

From the monorepository root:

```bash
cd s_tc_jc_landmark_closure/source/paper
tectonic main.tex
```

For the supplement:

```bash
cd ../supplement
tectonic supplement.tex
```

From the root of the extracted bioRxiv source ZIP, use the archive-local
paths:

```bash
cd paper
tectonic main.tex
cd ../supplement
tectonic supplement.tex
```

The main source includes every figure as repository-native TikZ and uses
`references.bib`; there are no generated raster figures or absolute paths.

# Deterministic manuscript build

Exact-byte replay was tested with Tectonic 0.16.9, default bundle v33,
and `SOURCE_DATE_EPOCH=1786924800`.  `requirements.txt` at project root is
the Python dependency lock; Tectonic and its bundle are separate build
requirements.

From the project root:

```bash
export SOURCE_DATE_EPOCH=1786924800
cd source/paper
tectonic main.tex
```

For the supplement:

```bash
export SOURCE_DATE_EPOCH=1786924800
cd ../supplement
tectonic supplement.tex
```

From the root of the extracted bioRxiv source ZIP, use the archive-local
paths:

```bash
export SOURCE_DATE_EPOCH=1786924800
cd paper
tectonic main.tex
cd ../supplement
tectonic supplement.tex
```

The main source includes every figure as repository-native TikZ and uses
`references.bib`; there are no generated raster figures or absolute paths.

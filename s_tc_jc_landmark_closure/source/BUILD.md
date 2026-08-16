# Deterministic manuscript build

Requirements: Tectonic 0.15 or later with its standard cached bundle.

From `source/paper/`:

```bash
tectonic main.tex
```

From `source/supplement/`:

```bash
tectonic supplement.tex
```

The main source includes every figure as repository-native TikZ and uses
`references.bib`; there are no generated raster figures or absolute paths.

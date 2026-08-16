# Reproducibility

## Full flagship replay

From the project root:

```bash
bash release/one_command_replay.sh
```

The replay verifies the four frozen source archives, runs independent all-dimensional symbolic checks and mutation tests, regenerates exact instances and coefficient tables, recomputes the numerical illustrations, rebuilds the figures and PDFs, assembles submission and specialist-audit packages, runs a clean portable repository replay, performs PDF/font checks, and writes the release SHA-256 manifest.

## Portable public replay

```bash
cd public/repository
bash replay.sh
```

This command has no dependency on the private source projects. The all-dimensional proof certificates are listed in `public/repository/CERTIFICATES.md`; finite `m` calculations are regressions only.

## Software environment

Python dependencies are listed in `requirements.txt`. The build also requires a TeX distribution with `pdflatex`, `biber`, TikZ, `biblatex`, and the standard AMS packages, plus `poppler-utils` for PDF audit commands.

## Numerical scope

Cosine-Galerkin integrations are deterministic illustrations. They are not used in any theorem, sign proof, or certificate.

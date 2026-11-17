# Nonattainment in the Harrell–Stubbe Dirichlet gap inequality

Alec Kriebel · ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X) · Version 1.0.1 · 2026-09-23 (UTC)

For every nonempty bounded open Ω in Rⁿ and every finite J≥1, the Dirichlet eigenvalues satisfy

\[
\left(\frac{n+2}{nJ}\sum_{j=1}^J E_j\right)^2
-\frac{n+4}{nJ}\sum_{j=1}^J E_j^2
>\frac{(E_{J+1}-E_J)^2}{4}.
\]

Thus the **corrected saturation question** [OWR-3389-016](https://www.unsolvedmath.com/problems/OWR-3389-016) has a negative answer. The theorem includes disconnected domains, rough boundaries, eigenvalue multiplicities, and n=1. The original 2009 report prints a missing square; the paper explicitly explains the correction. Neighboring growth-bound questions are outside this result.

## Read and verify

1. Read [the paper](output/pdf/paper.pdf), whose complete analytic proof is self-contained after standard Dirichlet spectral theory. [LaTeX source](manuscript/paper.tex).
2. Read the concise [verification report](audit/VERIFICATION_REPORT.md) and [priority audit](audit/priority-audit-independent.md). The scoped search found no earlier explicit nonattainment proof; this is not a guarantee of originality.
3. Run `python3 verification/verify.py` from this folder. Python 3.10+ and the standard library suffice. The deterministic output must agree with [results.json](verification/results.json). There are 7,016 exact checks across 1,312 certified box/index cases, including 600 zero gaps, 12 repeated-ground cases, and three detected negative controls.

The script audits algebra and explicit model spectra. It does **not** machine-prove the functional analysis or the theorem for arbitrary domains. The proof and audits carry that burden.

## Additional preprint review

Version 1.0.1 adds a direct supporting-package link and PDF metadata; the mathematical text is unchanged from version 1.0.0. The [review record](audit/PREPRINT_REVIEW.md) tracks fresh adversarial reviews and the disposition of every finding. Earlier audits and deployment checkpoints remain historical records of the versions they reviewed.

## Publication artifacts

- [Source and verification ZIP](output/source-and-verification.zip): proof source, PDF, exact scripts/results, audits, metadata, and build instructions.
- [Zenodo upload kit](output/zenodo-upload-kit.zip): unpack, upload the files in `files/`, and copy the fields from [zenodo/UPLOAD.md](zenodo/UPLOAD.md).
- [GitHub Pages](https://aleckriebel.github.io/Math/papers/strict-dirichlet-gap/).
- No DOI has been minted by this package. No GitHub release is needed for manual deposition.

Build the PDF with `tectonic manuscript/paper.tex --outdir output/pdf`. Build deterministic archives with `python3 build_package.py`; add `--deploy-copy` only in the original repository to copy the site into `docs/papers/strict-dirichlet-gap/`. The PDF's bytes may vary with TeX/runtime metadata; the packaged PDF is hashed. Archive construction itself is deterministic for identical input files.

## Provenance and licensing

The user supplied an AI-generated candidate proof. Independent AI reviews checked its original zero-extension argument and a shorter self-adjointness argument used in the paper. The classical trace identity and non-strict inequality are attributed to prior work. This package is an AI-assisted research preprint, not an external peer-review certificate.

Text/PDF: CC BY 4.0. Code: MIT. See [LICENSES.md](LICENSES.md). Third-party source downloads and source-page renderings are excluded from the public package. See [research log](RESEARCH_LOG.md) for the recorded audit decisions.

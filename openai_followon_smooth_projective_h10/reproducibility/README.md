# Reproduction and scope

This package currently establishes conditional implications. None of the finite checks certifies H10(Q) or the pointwise 2-converse.

From the repository root, with Python 3.10 or later:

```sh
python3 openai_followon_smooth_projective_h10/reproducibility/arithmetic_checks.py
python3 openai_followon_smooth_projective_h10/agent_notes/parity_matrix_check.py
```

The first output must match `arithmetic_checks.expected.json` as a JSON object. It checks exact quadratic-field identities and all 26 primes below 5000 satisfying the prescribed congruences. The second checks 1960 reciprocity-consistent matrix instances with seed 4003. These are finite interface checks; their scope is recorded in the accompanying source audits.

The four-page conditional note is a standalone LaTeX document. It was compiled with the native Codex LaTeX compiler and exported using Tectonic 0.16.9. A clean build is:

```sh
mkdir -p /tmp/smooth-projective-build
cp openai_followon_smooth_projective_h10/manuscript/main.tex /tmp/smooth-projective-build/main.tex
tectonic --outdir /tmp/smooth-projective-build /tmp/smooth-projective-build/main.tex
```

The build needs standard LaTeX packages fetched or cached by Tectonic. No project file or bibliography outside `main.tex` is needed. PDF bytes can differ across toolchains; validate text, page count, equations, references and metadata. The checked local export is `manuscript/main.pdf`; hashes are in the checkpoint receipt.

Source provenance is in `sources/PINNED_INPUT.json` and `sources/PINNED_COMPANIONS.json`. The upstream clone is read-only. The derived family004 build compatibility source omits only three unsupported pdfTeX PDF metadata primitives; its build receipt is `receipts/source_build.json`. A successful build is layout verification, not mathematical verification.

`checkpoint.py` is an operational aid for safely publishing explicitly named owned files on shared main. It uses an isolated index and a fast-forward push of a commit hash, without changing the checkout, index, branch or HEAD. It is not needed to reproduce any mathematical result.

There is no Zenodo payload manifest yet: an unconditional publication candidate has not passed the arithmetic gate.

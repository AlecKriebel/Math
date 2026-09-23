# Radial orthogonality does not imply dual 1-conformal flatness

Alec Kriebel · [ORCID](https://orcid.org/0009-0001-9320-500X) · Version 1.0.0 · 22 September 2026

This four-page note gives a negative answer to Takashi Kurose's Question 3(e) in Furuhata–Matsuzoe–Urakawa (1998), p.126, indexed as AMR-059-0011 / 6000011.

**Counterexample:** the unit round cylinder `S² × R` with product metric and Levi–Civita connection. Every radial orthogonal distribution is tangent to level sets of endpoint energy. A hypothetical 1-conformal flattening would force both `A(e₁)=e₁` and `A(e₁)=0`. The dual equals the original connection. The note also verifies a deformation with nowhere zero cubic tensor and the extension to every dimension at least three.

- [Paper](output/pdf/paper.pdf) and [editable LaTeX source](manuscript/paper.tex).
- [GitHub Pages article](https://aleckriebel.github.io/Math/papers/radial-statistical-counterexample/).
- [Verification report](research/VERIFICATION_REPORT.md), [original-source audit](research/SOURCE_AUDIT.md), and [priority audit](reviews/priority_audit.md).
- [Deeper priority follow-up, 23 September 2026](reviews/priority_followup.md), including the successful [live database recheck](research/DATABASE_RECHECK.md). The paper and version 1.0.0 archives retain the initial audit snapshot; these later notes update the historical assessment.
- [Independent proof review](reviews/proof_audit.md) and [coordinate-computation review](reviews/computation_review.md).
- [Zenodo upload instructions and copyable metadata](zenodo/UPLOAD.md).

## Verify in under a minute

From this directory, using Python 3.9 or later:

```sh
python3 verification/verify_exact.py
```

The standard-library checker solves all components of the necessary pointwise curvature identity using rational row reduction. It checks dimensions 3, 4 and 5, compatible constant-curvature controls, the dimension-two boundary, and the projective Weyl obstruction. The proof covers all dimensions at least three; the finite computation does not prove that quantifier.

For the independent calculation from the coordinate metric, install SymPy in a virtual environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r verification/requirements.txt
.venv/bin/python verification/verify_symbolic.py
```

This computes the connection, curvature, general conformal change, cubic tensor, and dual connection without assuming the claimed identities. Both checkers retain their checks under Python's `-O` option. Expected outputs are included. The human-readable proof supplies the first-variation theorem and coverage of all centers and neighborhoods; this is not complete proof-assistant verification.

## Rebuild and package

```sh
tectonic manuscript/paper.tex --outdir output/pdf
python3 build_package.py
```

Alternatively compile the source twice with a conventional LaTeX distribution. `build_package.py` creates deterministic ZIP archives, payload checksums, and the self-contained web page's download files. It does not publish, upload, or contact anyone. Tectonic needs its usual TeX package cache or network access on the first build; the delivered PDF is ready to read.

## Attribution and status

The argument resolves the printed implication, not a classification problem. Independent AI reviews and exact checks found no substantive mathematical gap. A focused literature search found no earlier explicit answer; it cannot certify priority or the question's current status in every source. The Gauss-lemma mechanism, Kurose's criterion, and the projective/conformal deformation machinery are prior work. A browser retry on 23 September 2026 successfully read the public database's annotations: its partial-status label refers to machine-generated research progress, and its report identifies no verified proof or counterexample. See the dated follow-up for deeper citation checks and remaining access gaps.

This is an unrefereed, AI-assisted preprint, prepared with OpenAI Codex and separate adversarial AI reviewers from the supplied AI-generated candidate. No external human peer review, Zenodo deposit, or DOI is claimed. The two supplied gradient-path filenames belong to a different problem and are not used here.

Text and manuscript: CC BY 4.0. Original verification and packaging code: MIT. See [LICENSES.md](LICENSES.md). Third-party source PDFs are linked, not redistributed.

# Radial orthogonality does not imply dual 1-conformal flatness

Alec Kriebel · [ORCID](https://orcid.org/0009-0001-9320-500X) · Version 1.0.1 · 26 September 2026

This four-page note gives a negative answer to Takashi Kurose's Question 3(e) in Furuhata–Matsuzoe–Urakawa (1998), p.126, indexed as AMR-059-0011 / 6000011.

**Counterexample:** the unit round cylinder `S² × R` with product metric and Levi–Civita connection. Every radial orthogonal distribution is tangent to level sets of endpoint energy. A hypothetical 1-conformal flattening would force both `A(e₁)=e₁` and `A(e₁)=0`. The dual equals the original connection. The note also verifies a deformation with nowhere zero cubic tensor and the extension to every dimension at least three.

- [Paper](output/pdf/paper.pdf) and [editable LaTeX source](manuscript/paper.tex).
- [GitHub Pages article](https://aleckriebel.github.io/Math/papers/radial-statistical-counterexample/).
- [Verification report](research/VERIFICATION_REPORT.md), [original-source audit](research/SOURCE_AUDIT.md), and [priority audit](reviews/priority_audit.md).
- [Deeper priority follow-up, 23 September 2026](reviews/priority_followup.md), including the successful [live database recheck](research/DATABASE_RECHECK.md). Version 1.0.1 incorporates these follow-ups into the manuscript and download packages; the dated audit reports preserve the search history.
- [Review of three supplied full texts, 24 September UTC](reviews/priority_supplied_papers.md): Matsuzoe 1999, Matsuzoe 2010, and Kurose 2023/2024. These source gaps are closed; no earlier explicit answer was found in them. The exact deformation is already printed in Matsuzoe 1999.
- [Current priority statement](research/PRIORITY_STATUS.md) and [preprint review record](research/PREPRINT_READINESS.md).
- [Initial independent proof review](reviews/proof_audit.md) and [coordinate-computation review](reviews/computation_review.md).
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

The argument proves that the printed implication is false. **Historical priority remains unresolved. No first-resolution claim is made, and the paper does not assert that the question remained open at publication.** No earlier explicit answer was found in the bounded search, but Kurose's 1999 affine-realization paper, Binder–Simon's 2000 problem list, the full content of Kurose's 2016 talk, and narrower citation leads remain uninspected. An earlier answer or implicit resolution in them cannot be excluded. See the [current priority statement](research/PRIORITY_STATUS.md).

The Gauss-lemma mechanism, Kurose's curvature criterion, and the deformation machinery are prior work. The exact deformation is credited directly to Matsuzoe (1999), p.178, equation (2.1). The database annotations were successfully read on 23 September; their machine-generated report identifies no verified answer, which is not evidence establishing priority. Version 1.0.1 corrects the original access statement and incorporates the fuller attribution throughout.

This is an unrefereed, AI-assisted preprint, prepared with OpenAI Codex and separate adversarial AI reviewers from the supplied AI-generated candidate. No external human peer review, Zenodo deposit, or DOI is claimed. The two supplied gradient-path filenames belong to a different problem and are not used here.

Text and manuscript: CC BY 4.0. Original verification and packaging code: MIT. See [LICENSES.md](LICENSES.md). Third-party source PDFs are linked, not redistributed.

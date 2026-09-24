# A Lipschitz-nonincreasing deformation of small unitary-valued maps

Alec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X) · Version 1.1 · 2026-09-23 UTC

**Result:** the candidate proof passes independent algebraic and geometric audits. For a unit-round sphere and either the unnormalized Hilbert–Schmidt or operator-norm length metric on U(N), the maps with Lipschitz constant at most 1/2 strongly deformation retract onto the constant maps. The deformation multiplies the Lipschitz constant by at most `(1-t²)/(1+t²)`. It also preserves the strict sublevel.

This answers the literal assertion in [Gromov's 2017 question [?24](i), p. 36](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf), catalogued as [AMR-066-0025](https://www.unsolvedmath.com/problems/AMR-066-0025). It is an unrefereed, AI-assisted preprint, not an externally peer-reviewed or formally machine-checked result.

**Priority:** the documented search located no earlier explicit resolution or exact quantitative map-space retraction. This is a qualified no-conflict result, not proof of first discovery. Cayley/Möbius transforms are classical; ordinary contraction without preserving the Lipschitz sublevel already follows from a standard logarithm chart. The note explicitly acknowledges this.

Version 1.1 incorporates three editorial improvements from a [fresh adversarial preprint review](audit/preprint_round1.md): an explicit derivative variable, a companion-material link, and embedded PDF metadata. See the [revision response](audit/preprint_revision_response.md). The theorem and proof are unchanged.
A [second fresh adversarial review](audit/preprint_round2.md) found no actionable issues. The [preprint-readiness record](audit/preprint_readiness.md) identifies the exact audited source and PDF.

## Read and verify

1. Read [the four-page paper](paper/main.pdf), with [editable LaTeX source](paper/main.tex). The main proof is entirely analytic.
2. Inspect [the proof checklist](audit/verification_summary.md), [algebra review](audit/algebra_review.md), [independent geometric route](audit/geometry_review.md), and [final manuscript review](audit/final_manuscript_review.md).
3. Read [the priority audit](audit/priority_review.md), including the query log, comparisons to earlier work, and limitations.
4. Optionally run the finite diagnostics described in [verification/README.md](verification/README.md):

   ```sh
   python3 verification/verify_exact.py
   # Optional, requires NumPy:
   python3 verification/verify_numeric.py
   ```

The recorded checks pass: 10 exact algebra checks and 7,679 floating-point checks. They do not prove the all-dimensions theorem, the curve-length argument, or parameter continuity. No numerical calculation is needed to verify the written proof.

## Build and deposit

- Rebuild the paper with `tectonic paper/main.tex` (tested with Tectonic 0.16.9).
- Rebuild the download archives and GitHub Pages assets with `python3 build_release.py`.
- See [Zenodo upload instructions](zenodo/UPLOAD.md), [copy-and-paste fields](zenodo/COPY_PASTE.txt), and [metadata JSON](zenodo/metadata.json).
- [Project website](https://aleckriebel.github.io/Math/papers/gromov-unitary-lipschitz/).

The research source lives in this dedicated top-level repository directory. Only the published site copy is placed under `docs/papers/gromov-unitary-lipschitz/`, as required by this repository's existing GitHub Pages configuration. Other project files are not part of this package. The author has deposited version 1.1 on [Zenodo](https://zenodo.org/records/22929857), which assigns DOI `10.5281/zenodo.22929857`. The deposited PDF and reproducibility archive match the reviewed release byte for byte. At the deposit audit, the direct record worked but doi.org had not resolved the identifier; see [the audit receipt](research/zenodo_22929857_audit.json). The frozen download archives preserve their pre-deposit preparation snapshot. No GitHub release was created.

## Scope

The constant at the endpoint is the input map's value at a fixed point p; the constant-map copy of U(N) is not itself contracted to a preassigned point. The theorem concerns the two explicitly defined metrics, not every invariant metric with one normalization. It answers the printed threshold 1/2, not a claim of Lipschitz-bound preservation below 1 in the surrounding discussion. The optional S⁰ extension uses angular distance π.

[Research log](research/LOG.md) · [Source record](research/source_record.md) · [Licensing](LICENSE.md)

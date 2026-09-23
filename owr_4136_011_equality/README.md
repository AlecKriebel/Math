# Equality in the Fradelizi–Paouris–Schütt second-moment inequality

**Version 1.0.0 · 23 September 2026 · Alec Kriebel · Unrefereed preprint**

The general-convex-body equality conjecture in FPS Theorem 1.1 is proved: if
all extreme points of a convex body K in R^n have norm at least r>0, then

    C₂(K) ≥ [r² + (n+1)‖g_K‖²]/(n+2),

with equality exactly for nondegenerate simplices with all vertices of norm r.
The proof covers n≥1 and the full scope of [OWR-4136-011](https://www.unsolvedmath.com/problems/OWR-4136-011).
The inequality, simplex moment formula, and polytope equality case are prior
results of Fradelizi, Paouris, and Schütt. No earlier general equality proof
was found in the bounded priority audit; global novelty is not certified.

## Read and verify

1. Read the [four-page paper](output/pdf/paper.pdf), especially Lemma 2 and
   the exact deficit identity (4). The proof is analytic and self-contained
   apart from standard finite-dimensional convexity and integration facts.
2. For a second argument, read [the finite-approximation proof](audit/independent-proof.md).
3. Run `python3 verification/verify.py`. The standard-library-only script
   reports 298 exact checks across 18 finite cases. It does **not** prove the
   universal theorem or determine priority.
4. Consult [the verification report](audit/VERIFICATION_REPORT.md),
   [exact source match](audit/source-match.md), and
   [bounded priority audit](audit/priority-independent.md).

## Publication files

- [Manuscript source](manuscript/paper.tex)
- [Source and verification archive](output/source-and-verification.zip)
- [Zenodo upload kit](zenodo/zenodo-upload-kit.zip)
- [Copy-and-paste Zenodo fields](zenodo/UPLOAD.md) and [metadata JSON](zenodo/metadata.json)
- [Public paper page](https://aleckriebel.github.io/Math/papers/fps-equality/)

Extract the Zenodo kit and upload the three files inside `upload/`. The kit
has not been deposited and contains no assigned or invented DOI. Creating
this package does not create a GitHub release.

## Rebuild

With Tectonic installed, run from this folder:

```sh
python3 build_package.py --compile
```

To also refresh the repository's GitHub Pages mirror, add `--publish-site`.
Without `--compile`, the script packages the existing checked PDF. Python
3.9+ is sufficient for the verifier and packaging. No credentials are needed.
The checked verifier result is `output/verification.json`; original source
hashes are in `SOURCE_SHA256SUMS`. Zip files use fixed timestamps for repeatable
packaging of unchanged inputs. TeX/PDF bytes may vary with the compiler version.

The candidate came from prior AI-assisted work supplied by the author.
OpenAI Codex prepared the publication with separate AI verification agents;
these audits are not external human peer review. Text: CC BY 4.0. Code: MIT.
ORCID: https://orcid.org/0009-0001-9320-500X.

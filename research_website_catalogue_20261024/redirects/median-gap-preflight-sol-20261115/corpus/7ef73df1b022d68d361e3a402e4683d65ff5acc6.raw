# Manual Zenodo upload: version 1.0.0

The package is ready for a **new preprint record**. No deposit has been made
and no DOI has been assigned. No GitHub release was created.

1. Extract `zenodo-upload-kit.zip`.
2. Open [Zenodo's new upload page](https://zenodo.org/uploads/new).
3. Upload the three files in `upload/`: `paper.pdf`,
   `source-and-verification.zip`, and `SHA256SUMS`.
4. Fill the fields below. The JSON is a reusable metadata object; uploading
   it as a file does not fill the form. `deposition.json` additionally provides
   the documented REST API wrapper, without an upload or publish command.
5. Preview the files and record, obtain the DOI through Zenodo, and publish
   when ready. If you reserve a DOI to print in the paper first, update the
   manuscript and rebuild the files before publishing.

Upload the contents of `upload/`, rather than the outer convenience kit, so
readers can view the PDF directly.

## Copy-and-paste fields

**Resource type:** Publication → Preprint

**Title:**

Equality in the Fradelizi–Paouris–Schütt second-moment inequality

**Creator:** Kriebel, Alec

**ORCID:** 0009-0001-9320-500X

**Affiliation:** Independent researcher

**Publication date:** 2026-09-23

**Version:** 1.0.0

**Language:** English

**Access:** Open access

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0).
Code in the companion archive is separately MIT licensed.

**Description:**

Fradelizi, Paouris, and Schütt proved a sharp lower bound for the normalized
second moment of a convex body whose extreme points have Euclidean norm at
least r, and characterized equality for polytopes. This note proves their
conjectured characterization for arbitrary convex bodies: equality in
C₂(K) ≥ [r²+(n+1)‖g_K‖²]/(n+2) holds exactly for nondegenerate simplices with
all vertices of norm r. The proof covers every dimension n≥1 and resolves
the mathematical question catalogued as OWR-4136-011.

The four-page proof uses an almost-everywhere extreme-point simplex partition
and an exact nonnegative deficit identity. A retained-pair estimate supplies
a second finite-approximation route. The deposit includes LaTeX source, an
exact standard-library Python verifier, independent AI proof audits, a source
comparison, and a bounded priority search. All 298 finite checks across 18
cases pass; they do not replace the analytic proof. No earlier resolution was
found in the searched literature, without certifying global priority. This is
an unrefereed, AI-assisted preprint. Text is CC BY 4.0; code is MIT.

**Keywords:**

convex geometry; second moment; equality cases; extreme points; simplex;
Fradelizi–Paouris–Schütt inequality; OWR-4136-011

**Related identifiers:**

- References (DOI): 10.4153/CMB-2011-142-1
- References (DOI): 10.4171/OWR/2009/53
- Is supplemented by (URL): https://github.com/AlecKriebel/Math/tree/main/owr_4136_011_equality
- Is documented by (URL): https://aleckriebel.github.io/Math/papers/fps-equality/

**Additional notes:**

Prepared with OpenAI Codex from a candidate supplied by the author from prior
AI-assisted work, with separate AI verification agents. The inequality,
simplex moment identity, and polytope equality case are due to Fradelizi,
Paouris, and Schütt; the contribution is the general-convex-body equality
classification. The audits are not external human peer review.

## Verify the files

From the extracted `upload/` folder on macOS or Linux:

```sh
shasum -a 256 -c SHA256SUMS
```

Extract the source archive, enter its project folder, and run
`python3 verification/verify.py`. No credentials or network are needed.

Fields were checked against [Zenodo's official metadata documentation](https://developers.zenodo.org/#deposit-metadata)
and [upload guidance](https://help.zenodo.org/docs/deposit/create-new-upload/)
on 2026-09-23. Keep the original preprint date unless preparing a later
version. Only Zenodo can supply the deposit's DOI.

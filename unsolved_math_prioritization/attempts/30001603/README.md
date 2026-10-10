# Accepted prior negative resolution: toric jet spanning

**Rank 698 · ID 30001603 / OWR-4527-007 · already_solved · 1/5 substantive author turns.**

## Read the corrected proof and final acceptance

The accepted proof is [the corrected PROOF.md](toric_jets_30001603_corrected_release/packet/PROOF.md). The final independent verdict is [DELTA_AUDIT.md](toric_jets_30001603_delta_audit/DELTA_AUDIT.md), with [exact-byte acceptance](toric_jets_30001603_delta_audit/EXACT_ACCEPTANCE.json). The original full [mathematical audit](toric_jets_30001603_independent_audit/AUDIT.md) remains part of the evidence; its source-description correction requirement is resolved by the later delta acceptance.

This verifies the published Di Rocco–Jabbusch–Smith example from *Toric vector bundles and parliaments of polytopes* ([2018 journal article](https://doi.org/10.1090/tran/7201), Examples 4.2 and 5.3). Their rank-three ample, hence nef, bundle on the complex projective plane has invariant-curve splitting types (4,3,1), (5,2,1), (6,1,1), so tau = 1. Value ranks are (3,3,2), and first-jet ranks are (9,9,7). It therefore refutes the original [OWR45/2010](https://doi.org/10.4171/owr/2010/45) implication at k = 1. This is an attributed prior result, not a new counterexample or a resolution under an additional global-generation hypothesis. The credited Hering–Mustata–Payne positivity criterion is [here](https://doi.org/10.5802/aif.2534).

## Important supersession and source correction

**Both inspected DJS PDFs print (-1,-2). The (-1,2) sign-flip test is synthetic only. There is no current claim of a DJS printing error.**

The directory `toric_jets_30001603/` is the **superseded original freeze**, preserved unchanged only for provenance and complete old/new delta replay. Its erroneous source allegation must not be used as the current account. The [complete correction diff](toric_jets_30001603_corrected_release/controls/CORRECTION.diff) includes removed historical text; removed lines are not current claims. The [original audit](toric_jets_30001603_independent_audit/README.md) found the allegation and required its correction. The [later delta audit](toric_jets_30001603_delta_audit/README.md) accepted the corrected descriptions and independently replayed all mathematics.

The unchanged preparation records inside the corrected release still say that review was pending when those bytes were frozen. The separate exact-bound delta acceptance completes that review. The source narrative and descriptive labels changed; bundle inputs, arithmetic, and mathematical results did not.

## Reproduce

Use Python 3 and SymPy 1.14.0. The corrected author verifier itself uses only the standard library. From this directory:

```sh
python3 -B verify_publication.py
```

The wrapper verifies the exact publication membership, original and corrected manifest anchors, acceptance anchor, and all member hashes. It then runs the corrected packet (79 checks and three temporary-copy integrity controls), the independent complete delta replay (115 checks and the independently derived 60-check mathematics with eight corruption controls), and the original full audit as a historical replay. It preserves every input file. No network is used. To anchor the outer publication manifest against the digest recorded with this draft, supply it as the optional sole argument to the wrapper.

The geometric proof, especially nefness, comes from the full arguments and credited sources. Finite checks alone are not a proof of nefness or a check of printed source text. Independent AI review is not conventional human peer review or proof-assistant certification.

## Scope and contents

- `toric_jets_30001603_corrected_release/`: accepted corrected proof, exact arithmetic, source metadata, complete correction diff, and binding controls
- `toric_jets_30001603_delta_audit/`: final exact-bound acceptance and independent correction/mathematical replay
- `toric_jets_30001603_independent_audit/`: original full audit and independent verifier, retained unchanged
- `toric_jets_30001603/`: superseded original freeze, retained unchanged for reproducibility only
- `RESEARCH_LOG.md`, `verify_publication.py`, `PUBLICATION_MANIFEST.json`: release context, portable checks, and public file hashes

The live problem page returned HTTP 403; that page and the old selected full corpus/AI record were not inspected. No unavailable statement-byte hash match is claimed. Identification rests on the inspected descriptor and authoritative primary contribution. All source PDF hashes, sizes, and inspection details are in the bound source metadata. No PDF, extract, image, raw dataset record, or private coordination file is redistributed.

This delivery is one draft PR. Only the target queue row's Status, Turns, and previously blank Findings are changed. Chat, DOI, every other row, and the existing embedded queue header are preserved byte for byte. No queue regeneration, merge, release, DOI, or outreach is part of this publication.

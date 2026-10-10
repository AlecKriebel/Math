# Generic wreath-product actions: affirmative candidate

**Problem 30006166 / OWR-14299082-012, rank 830: claimed_solved, 3/5 substantive approaches.**

The candidate establishes hyperfiniteness of the entire orbit equivalence relation on Cantor space for a comeager set of continuous actions of the restricted wreath product W = Z wr Z. Both independent adversarial AI audits accept the complete affirmative candidate and require no proof correction. This remains AI-assisted, unrefereed work; no human-peer-review, formal-verification, novelty or priority certification is claimed.

## Proof and exact scope

Read the immutable [author proof](author/PROOF.md), [first independent audit](audit_bundle/audit/REPORT.md), and [second independent audit](independent_review_2/AUDIT.md) together.

1. Relative finite-factor lifting yields a coherent continuous profinite-height factor for a dense G_delta set in the full Cantor-action space.
2. Each finite-width slab graph has finite Borel asymptotic dimension, including nonfree actions. Increasing factorial-width slabs meet the exact compatible-metric-union hypotheses of Conley–Jackson–Marks–Seward–Tucker-Drob Theorem 7.3. No dimension bound uniform in the slab width is required.
3. The entire exceptional preimage of the embedded integers is handled separately using increasing finite-height bands and hyperfiniteness of the countable abelian lamp subgroup. It is not discarded as negligible. The two invariant pieces give hyperfiniteness on the whole Cantor space.

The Borel argument applies to actions admitting a Borel equivariant profinite-height factor. No assertion is made about all Borel W-actions. Freeness, minimality, and measure preservation are not assumptions. Genericity is in action space, not a restriction to a comeager subset of the phase space. The argument does not invoke an unrestricted increasing-union theorem for hyperfinite relations.

## Credited published inputs

The deep input is Conley, Jackson, Marks, Seward, and Tucker-Drob, [Borel asymptotic dimension and hyperfinite equivalence relations](https://doi.org/10.1215/00127094-2022-0100), Duke Mathematical Journal 172 (2023), 3175–3226: Corollary 5.5 for nonfree finite-rank abelian actions, Theorem 7.3 for compatible metric unions, and Corollary 7.5 for the countable abelian lamp subgroup. The inspected [author manuscript](https://math.berkeley.edu/~marks/papers/polycyclic_v13.pdf) is pinned in both reviews. The exact target is Question 3 in Iyer's contribution, joint with Shinko, to [Oberwolfach Report 2/2025](https://doi.org/10.4171/owr/2025/2), printed p. 115. [Iyer–Shinko](https://arxiv.org/abs/2409.03078) supplies credited background; its locally finite-asymptotic-dimension hypothesis does not cover W.

Source titles, public URLs, PDF hashes and sizes, retrieval and inspection history, and public manuscript status are retained in the frozen metadata. Bounded searches are not a certification of worldwide openness or historical priority. No source PDFs, extracts, images, dataset contents or private coordination material are included.

## Preserved evidence

All three original ZIP archives and all 51 extracted members are unchanged, including the author's duplicate copy inside the first audit. Original pending-review and no-publication labels are historical freeze-stage statements; the current acceptance is recorded by the two later audits and this wrapper. The proof itself is unchanged.

Finite diagnostics and software-integrity checks test reproducibility and selected constructions. They do not prove Baire category, Borel measurability on arbitrary spaces, the published inputs, or the infinite theorem. Hashes are integrity bindings, not signatures.

## Reproduction

Python 3.10+ with its standard library is sufficient. Retain a trusted SHA-256 digest of PUBLICATION_MANIFEST.json separately, inspect verify_publication.py, and verify the manifest bytes against that trusted digest before running:

    python -I -B verify_publication.py TRUSTED_MANIFEST_SHA256 --full
    python -I -O -B verify_publication.py TRUSTED_MANIFEST_SHA256 --full

The wrapper rejects any unexpected file, directory, symlink or other nonregular entry, binds every byte to the externally pinned publication manifest, verifies all ZIP/member equivalences and inner-manifest pins, and replays each frozen checker and integrity suite. Relocate the complete publication directory and repeat. The second audit also checks its binding to the external author proof, archive and manifest. Coordinated replacement of all content and the externally trusted digest is outside the integrity threat model.

Draft publication changes only this problem's queue Status, Turns and Findings cells. No merge, release, DOI or external outreach is part of this publication.

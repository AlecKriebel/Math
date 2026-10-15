# Partial results for the actual Erdős–Selfridge minimum

Problem 2485 / Erdős Problem 1095. Dated 12 October 2026. Status: unsolved by this work.

This AI-assisted, unrefereed mathematical packet preserves complete authored partial proofs and the complete substantive independent audit and post-authoring review. It makes no claim of a full resolution, novelty, priority, an exhaustive current literature search, external human peer review, journal acceptance or formal proof-assistant certification.

## Accepted scope

Let g(k) be the least n>k+1 such that every prime factor of C(n,k) is greater than k, and let L_k=lcm(1,...,k).

- An exact finite construction in the classical family t L_k P_y-1 retains all leading-digit filters and proves a sufficient union-bound criterion. Fixed-epsilon use of the prime number theorem gives limsup (log g(k)-log L_k)/(k/log k)<=1. The main scale remains exp((1+o(1))k).
- An exact first-survivor characterization at prime q>=3 proves g(q)>=g(q-1)+1. It does not give an unbounded multiplicative jump.
- Printed Lemma 3.8 of Lukes–Scheidler–Williams (1997) fails under its own candidate hypotheses: q=3,n=5 refutes the g(q) branch, q=3,k=2,n=4 refutes the other branch, and n=k+L_k is a uniform family. A full-density calculation repairs the relevant model comparison while retaining leading-digit filters.
- Historical independent exact-minimality verification covers k=1,...,46 and 2,562,964 exclusion intervals. The mathematical method is supplied in full; raw certificates, minimum tables and programs are separately retained and not distributed here.

The source's implementation expressly retained the disputed leading-digit filters. No table invalidity or paper-wide failure follows from the printed-lemma defect. No source-author program was executed.

## Prior results and unresolved questions

The construction is credited to Ecklund–Erdős–Selfridge (1974), who used the same family with a larger cutoff constant and already noted that it could be reduced. The coefficient-1 refinement is not claimed to be new. The prior source screen already reconstructed the exact Lucas/CRT density and the reciprocal-density model's prime-step ratio proof; PRIOR_DENSITY_CONTEXT.md retains that entire earlier section with attribution to Sorenson–Sorenson–Webster (2020 and the 2021 addendum). These model statements are not theorems about the actual first admissible integer.

The asymptotic scale near exp(Theta(k/log k)), the eventual inequality g(k)<L_k, and both successive-ratio conjectures remain unresolved by this work. Finite evidence does not prove any asymptotic claim. The inspected September 2026 Eastwood repository reports a table through 400. Earlier checks established admissibility of its 400 witnesses; this continuation independently establishes minimality only through 46. It does not extend that reported frontier.

## Contents and verification boundary

ACTUAL_MINIMUM_PARTIALS.md and SOURCE_CORRECTION.md are byte-identical to the accepted authored versions. COMPUTATIONAL_CERTIFICATE.md retains the complete search, termination, periodicity and coverage arguments, with distribution references corrected. MATHEMATICAL_AUDIT.md and POST_AUTHORING_AUDIT.md retain every substantive audit argument and qualification. EDITION_MAP.json identifies every editorial change by original byte ranges and exact hashes. ORIGINAL_INPUT_PINS.json binds the reviewed originals; ACCEPTANCE.md binds the public mathematical edition.

SOURCE_METADATA.json records public scholarly titles, URLs and dated retrieval/inspection identities. VERIFICATION.json supplies aggregate historical checks: three byte-identical minimality modes, four resealed semantic negative controls plus one stale-checksum control, independent analytic regressions, and the exact source-table match scope. This public prose edition is not a standalone executable replay package.

Programs, raw certificates, per-minimum generated records, public-source dataset contents, copied third-party PDFs, text, page images or quotations, and private coordination material are excluded. Recorded source history and computations are not new retrievals or reruns by edition preparation. MANIFEST.json is a closed inventory of this directory, listing itself without a recursive self-hash; its identity is independently sealed outside the directory.

The separate queue proposal changes only rank 1745's Status, Turns and Findings. It retains unsolved status, records at least one substantive continuation with lifetime total unknown, and does not assert that the five-exchange allowance was exhausted. Editorial preparation adds no proof attempt. All unrelated queue bytes and existing links are preserved. This packet and proposal do not themselves publish, merge, create a release or DOI, or contact anyone.

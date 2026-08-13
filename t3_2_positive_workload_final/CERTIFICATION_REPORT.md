# T3-2 certification report

Date: 2026-08-12

## Decision

**Strict pass at the stated theorem scope.** The package contains a complete
proof that every finite weakly reversible binary stochastic mass-action
network with at most three species and at most two linkage classes is
nonexplosive and positive recurrent on each closed irreducible population
class, for every positive rate vector.

“Strict pass” means that independent adversarial readers replayed the exact
frozen bytes, checked the load-bearing stochastic interfaces, rebuilt the
documents, and found no remaining mathematical or publication blocker. It
does not mean computer-formal proof or external peer review.

## What was certified

### Fixed-class reduction

The global theorem deletes dormant reactions before projection, absorbs
classwise constants into rates, merges projected linkages that share a
complex, and identifies each closed irreducible physical class with its
reduced image. The resulting system has zero, one, or two active projected
linkages. The conjugacy preserves explosion times, communication, and return
times.

The frozen theorem is
`research_notes/proof_first_t3_2_global_theorem.md`, SHA-256
`781d2520cbb3ad30e1749814f620d49d4c503c5c341ccd1add39a5fec31e2b7f`.
Its canonical exact-byte audit is
`research_notes/proof_first_t3_2_global_theorem_exact_byte_audit.md`, SHA-256
`bbc47342d8d7b3cacf4b34d2ce2b5bd122798f41838787e8edafa4c70c859560`.
An independent second audit is frozen at
`109a7226a6b0bbf6aa2b314a3b2e1a4e6c247663312cfe59061c6bb076d2065a`.

### Exact two-linkage universe

After reduction, the ordered support universe has exactly 46,872 members.
The final certificate proves the pairwise-disjoint identity

\[
46{,}872=27{,}462+432+146+336+18{,}496.
\]

The five terms are, respectively, the completed mixed orbit, the exclusive
active-invariant orbit gap, the strictly positive invariant branch, the
level-set residual, and the outside-mixed remainder. Every term is charged to
a standalone fixed-pair analytic theorem for arbitrary strong labelled
orientations and arbitrary positive rates.

The final theorem is
`research_notes/proof_first_two_linkage_46872_final_theorem.md`, SHA-256
`dae2a58f170836427ffc053ff931c1909d64ac591d77b971591b0d5814526cde`.
Its canonical audit SHA-256 is
`a4f50dcbc2235766524ddb7000a264ec88bf04f8841b3ce9b8d4689c800ba619`;
two additional independent audits are frozen at
`8a2a7a82696a3230c31e198bfc03227618baa0245f49599dd0b56be1f99e2e5a`
and
`615785300db808a228988a9558545e2bfade414ebedd3ca405de70fbf8370e3c`.

### Formerly open interfaces

The final proof does not use the invalid shortcuts identified during the
repair:

- tightness is never replaced by one fixed inactive environment;
- embedded reaction count is never used as physical duration;
- chart exits are not treated as negative drift without a charge;
- local potentials from different fixed support branches are not glued along
  one trajectory;
- dormant Flat0 phases are handled by a cap-free killed resolvent with actual
  endpoint control;
- level-set boundary faces use physical-time workload/service macros.

These repairs are preserved in the technical supplement together with the
counterexamples that ruled out earlier interfaces.

## Executable evidence and its boundary

`verify_read_only.py` passes 418 tests under isolated Python and confirms that
its declared files are not mutated. The final union source/test hashes are

```text
5b249ded4b54801f7eb5ab9ced943ed566216e1228c0e07f3e205b1eef319288
dd51ce074aa43bb4722d176ef4c85face956c924150681d5cae32f3b615c5e76
```

The finite layer certifies support membership, exact counts, fingerprints,
tier and affine identities, and regression examples. It does not enumerate
rate vectors, orientations, populations, or stochastic paths and does not by
itself prove recurrence. All stochastic quantifiers are discharged in the
analytic theorem notes.

## Publication verification

`publication/build_publication.sh` authenticates 40 proof-note inputs and
builds:

- `output/pdf/main.pdf` — 7 letter-size pages;
- `output/pdf/technical-supplement.pdf` — 189 letter-size pages.

Both build logs are free of TeX warnings and errors. Every supplement page
was reviewed in contact sheets, with high-resolution checks of the title,
branch transitions, long hash blocks, theorem composition, and final pages.
The main article was inspected page by page.

## Claim boundary

The result applies exactly to finite weakly reversible stochastic
mass-action networks with complex molecularity at most two, at most three
species, and at most two linkage classes, classwise after the stated exact
projection. It makes no claim for larger molecularity, four or more dynamic
species, three or more active linkage classes, non-weakly-reversible systems,
or non-mass-action kinetics.

The research package deliberately contains no author, license, journal, or
submission metadata. Those are not mathematical certification questions and
remain for the human researcher.

# Bounded density result for Erdős Problem 1110

For coprime integer bases p > q ≥ 2, the elementary antichain bound in PROOF.md proves that representable positive integers have natural density zero, failures have natural density one, and infinitely many failures can be chosen pairwise coprime and individually coprime to pq, in each of these three ranges:

- q ≥ 4
- q = 3 and p ≥ 7
- q = 2 and p ≥ 11

The imported density direction must therefore be corrected: it is the representable integers that have density zero in these ranges.

## Exact boundary

The density argument does not cover (4,3), (5,3), (5,2), (7,2) or (9,2). The pair (3,2) is separately fully representable, with the classical induction included in the proof. These five pairs describe the limits of this argument, not the unresolved cases of the entire literature.

The Erdős Problem 1110 tracker also credits coprime-failure results for (4,3) and (7,2); those extensions are not proved here. Yu–Chen's 2022 publication metadata and abstract were seen through search indexing. The full theorem and PDF were not obtained or inspected. No full resolution, novelty or exhaustive present-day literature assessment is claimed.

## Contents

- PROOF.md: complete corrected mathematical argument, byte-identical to the accepted proof (9,717 bytes; SHA-256 9ffee49c0f6746c495a1db6c10ca2198e946c67d64e03b5b08c86c7427412118).
- ACCEPTANCE.md: mathematical and source audit with the acceptance boundary and source-access limitations.
- CORRECTION.md: public editorial copy of the separately pinned scope correction. Its mathematical content is unchanged; original and public-copy identities are distinguished.
- SOURCE_PINS.json: public bibliographic metadata, available PDF hash and size, retrieval and inspection history, and original proof/correction provenance.
- MANIFEST.json: exact paths, SHA-256 hashes and byte counts for the other five public artifacts. It intentionally excludes itself to avoid circular hashing.

## Review disclosure

This proof reconstruction, audit and editorial preparation were AI-assisted. No external human review or formal proof-assistant certification has been obtained. The acceptance report records a bounded mathematical audit, not peer review or certification. Finite checks support the argument but do not prove an asymptotic result by enumeration. No source-author code was executed.

Source documents, copied source text, source images, datasets, raw enumerations and executable scripts are not included.

## Public references

- P. Erdős and Mordechai Lewin, d-Complete Sequences of Integers, Mathematics of Computation 65(214) (1996), 837–840: https://www.brand.site.co.il/riddles/201507a_files/2153618.pdf
- Wang-Xing Yu and Yong-Gao Chen, On a conjecture of Erdős and Lewin, Journal of Number Theory 238 (2022), 763–778: https://doi.org/10.1016/j.jnt.2021.09.018
- T. F. Bloom, Erdős Problem 1110: https://www.erdosproblems.com/1110

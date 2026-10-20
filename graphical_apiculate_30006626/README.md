# Graphical apiculate algebras: partial results

**Unsolved after five substantive attempts.** Neither full structural characterization in Problem 14 of Oberwolfach Report 8/2026 is resolved. No novelty claim is made.

Source: https://doi.org/10.4171/owr/2026/8 , printed pages 533–534.

## Audited results

- For finite connected geodetic graphs, the apex algebra is graphical exactly when the graph is a block graph. Complete proof: GEODETIC_AUDIT.md.
- GENERAL_ATTEMPT.md proves an exact edge-rank criterion for realization of each closed subalgebra, including infinite graphs. It does not derive the criterion from a structural forbidden-subalgebra condition.
- All connected graph-atlas entries through order seven were checked: 393 apiculate, 320 graphical, 73 nongraphical. These are finite data, not an unrestricted theorem.
- The house is graphical but not weakly median. Twenty-nine graphical atlas entries violate the proposed conjunction A9+A11; explicit six-vertex witnesses are included.
- House products with K2 and P3 passed exhaustive closed-subset checks. No general product-closure theorem follows.

The three exceptional four-element algebras and the C5 obstruction are already in Bandelt–Chepoi, *The algebra of metric betweenness II*, Lemma 4, DOI https://doi.org/10.1016/j.ejc.2007.03.003 . They are verified prior work, not discoveries here. The generalized-median identity is from Part I, DOI https://doi.org/10.1016/j.ejc.2006.07.003 .

## Reproduce

Use Python 3 and the version in requirements.txt. From computation run, in order:

1. python atlas_apex.py
2. python apex_identities.py
3. python apex_A9_A11.py
4. python classify_obstructions.py
5. python generalized_median_check.py
6. python product_tests.py
7. python independent_audit.py

Generated result files are reproduced by the scripts rather than all being stored. The independent audit uses different distance, apex, and realization algorithms, but the same NetworkX atlas catalog. Its scope and qualifications are in FINAL_PARTIAL_AUDIT.md.

The exploratory literal TQ! transcription test is excluded from this package and is not used as evidence. The definitive non-weakly-median house certificate uses the triangle condition and the checked A8 identity.

Only authored proofs, audits, code and generated certificates are included. No third-party source files are included.

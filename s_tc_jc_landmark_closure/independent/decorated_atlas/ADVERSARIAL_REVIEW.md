**Verdict: `ACCEPT_PRIMITIVE_GATE`**

No P0 or P1 findings for the bounded p7 primitive-atlas gate. I did not assess the global identifiability theorem.

**P2 Findings**
- Rooting census `root_edge_indices` are not tied to the stored `canonical_edges` order. The census enumerates `graph.edges` in `rootings.py`, then stores only indices, while role records separately store `canonical_edges`. Independent recomputation matched all `S_TC` counts/booleans but saw edge-index-set ambiguity in 195/198 roles if interpreted against canonical edge order. See [rootings.py](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/rootings.py:96), [rootings.py](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/rootings.py:184), [primitive.py](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/primitive.py:516).
- p7 records store tensor probes, not complete tensor hashes. This is nonblocking because p7 has zero displayed-signature collisions, but the p7 certificate itself is not a full tensor commitment. See [build_atlas.py](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/build_atlas.py:77) and [fourier.py](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/fourier.py:241).
- Mutation harness is hard-coded to p4 fixtures, so it does not directly exercise `certificates_p7_trial`. See [mutation_tests.py](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/mutation_tests.py:64).
- Future equality-collision certificates should make the verifier check that the stored switching map is induced by a reticulation permutation/flips, not only by mask agreement. The producer constructs such a witness, but the verifier ignores the normalizer metadata. See [fourier.py](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/fourier.py:278) and [fourier.py](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/fourier.py:290).

**Tests Performed**
- Read the required lock/review files first.
- Independently recomputed p7 raw primitive census: matched 42 cycle, 2,265 theta, 2,307 accepted orientations, 2,268 directed-cycle rejections, and 1,767 rooted-tree-child rejections.
- Parsed all p7 JSONL records with only Python stdlib: manifest/file hashes, record hashes, Merkle roots, uniqueness, references, port bijections, match-edge counts, and transport index checks all passed.
- Independently checked p7 role census counts: all 198 roles remain `S_TC`, with zero non-tree-child admissible rootings.
- Independently recomputed switchings and JC tensor probe for one p7 primitive; matched stored probe hash.
- Checked p7 displayed-parameter signatures: 138,060 records, 138,060 signature groups, zero collisions.

The implementation correctly avoids claiming the displayed-parameter signature is a complete observational separator: see [README.md](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/README.md:44) and [README.md](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/README.md:48).
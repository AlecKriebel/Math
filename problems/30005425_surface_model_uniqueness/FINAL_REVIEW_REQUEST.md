# Independent review request

Audit all five frozen proofs against FINAL_AUTHOR_MANIFEST.json. Preserve original bytes; corrections should be additive unless explicitly versioned. Proposed disposition is original unsolved 5/5, with scoped mathematical results only.

Highest-risk checks:
- Read Baur's entire OWR pp.441–444, and visually inspect printed443.png. It fixes string A and varies finite covers; the source's rotation phrase is not a formal homeomorphism equivalence. Check the expanded Baur–Coelho Simões paper for any actual definition that this packet missed.
- Compare Xin–Zhang2026 Definition1.13/1.14 and Remark2.2. Its saturated labelled/dissected homeomorphism relation is different unless independently identified. Credit its local classification; do not imply a new classification.
- Verify the four-vertex witness is finite, gentle, saturated, and a cover of the same A; confirm both ribbon cycles and the separate PPP lozenge gluing including blossom choices.
- Check the four-seam local surgery and the cyclic two-vertex finite-locus obstruction. Do not promote either to the undefined original quotient.
- Check the acyclic genus formula, boundary nonemptiness, isolated-vertex convention, multiquiver/parallel-arrow minimality proof and all versus saturated covers.
- Check the all-k connected construction, central thread, dimension and boundary connected sum; the proof must go beyond finite tests.
- Check the simultaneous-surgery proof for loops, shared lozenge corners, distinct side use, nonsaturated covers and finite endpoints. The broad move and label-reconstruction caveat must remain explicit. Verify its linear-size certificate claim under stated preprocessing.

Sources (local-only, hashes in SOURCE_HASHES.json and SOURCE_ADDITION_TURN_1.json): sources/owr2023-7.pdf and sources/printed443.png; sources/baur-simoes2024.pdf; sources/xin-zhang2026.pdf; sources/ppp2019.pdf; sources/ops2018.pdf. Do not publish source PDFs/images or raw imported source_record.json.

Run python turn1/verify_witness.py, turn2/verify_switches.py, turn3/verify_minimality.py, turn4/verify_family.py and turn5/verify_surgery.py. Their stdout should byte-match each turn's verification.json. Replay turn1/ribbon_certificate.py separately. Expected assertion totals:55,972,480,2674,63847 (68,028 total). The seeded search is a supplementary discovery record, not an exhaustive proof. Frozen manifests bind historical files; no prior proof or log was rewritten.

A full scoped PASS or precise required corrections is requested. No public publication or final status promotion is authorized by this request alone.

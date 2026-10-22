# Designed-tree congestion: proof and verification supplement

Associated paper: A designed tree model with a sharp congestion–fragmentation transition, Alec Kriebel, version1.0,21October2026. The standalone PDF accompanies this ZIP. Editable source is paper/main.tex; ordinary LaTeX with the listed standard packages compiles it. The source was built with Tectonic0.17.0 and every final page was visually inspected; PDF_VISUAL_QA.json binds the inspected PDF.

The complete theorem concerns the explicit fixed-design binary tree, dense cross-root traffic, independent fixed-law exponential slopes, actual offered-slope marginal normalization, and the two outer phases. The width is a sufficient upper bound. No critical profile, universal congestion law, canonical right-model claim or global priority certification is made.

## Contents

- candidate/ preserves all24 original files byte-for-byte, including the historical wrapper, frozen proofs, checks and historical review. SOURCE_SNAPSHOT.json records original repository provenance; its historical local original/ prefix corresponds to candidate/ here. candidate-binding.json supplies the exact portable binding.
- paper/main.tex is the complete analytic proof. Finite controls are supplementary, not a substitute for this proof.
- replay.py and REPLAY_README.md implement and document the narrow portability repair. The historical wrapper remains unchanged and is not claimed to pass bitwise under unpinned libraries.
- probability_controls.py is the independently authored standard-library probability checker; its retained expected output records2796678 assertions and695520 cut-size pairs.
- reviews/ contains the three distinct flow, probability and source/priority audit families, their sealed reports, code and retained evidence. Earlier individual verdicts retain then-pending package findings; the later REPAIR_RECEIPT.json documents the replay repair. No individual family report alone is release clearance.
- ROOT_MATHEMATICAL_AUDIT.md and ROOT_PRIORITY_ASSESSMENT.md state the strongest accepted result, exact scope and bounded-source limitations.
- publication-metadata.json is a provenance copy of the intended deposit manifest; its upload paths refer to the separate publication directory, not a second upload instruction from inside this ZIP.
- MANIFEST.json binds every payload by length and SHA256 and excludes only itself. The associated public ZIP checksum binds that manifest.

## Replay

Supply Python3.9.6, NumPy2.0.2 and SciPy1.13.1 for the tested full replay; requirements-tested.txt pins the numerical packages. The wrapper installs nothing. From an extracted archive:

    python3 -B replay.py

It verifies all24 original identities and runs each unchanged component once in its own disposable copy. Active turn2 output must remain byte-identical. Only the enumerated40 older floating diagnostics and the specified runtime/public-input projection differences are permitted; every other field, type, boolean and exact control remains exact. Failed-run receipts/logs are retained; no automatic retry or tolerance broadening occurs. Other library/platform combinations are not guaranteed.

Optional standard-library guard controls:

    python3 -B negative_controls.py --candidate candidate --output replay-output/guard-tests

The retained171 controls include127 required rejections. To rerun either independent mathematical checker without changing evidence, copy probability_controls.py or reviews/flow_adversary_01/independent_flow_controls.py to a new working directory and execute that copy. Each writes its output beside its script. The flow checker uses exact rational primal/dual witnesses. The priority comparison checker can likewise be copied; it tests calculations, not absence of old literature.

Historical receipts contain their original dates, paths, versions and pending-review wording. They are preserved evidence, not claims that those paths exist in this extracted layout or that all old floating bytes reproduce everywhere. No private source body, account record, secret, or third-party PDF is included.

AI tools were extensively involved in research, proof/model development, computation, writing and auditing. This is an unrefereed preprint; internal AI reviews are not formal independent human peer review. The manuscript has not undergone such human peer review.

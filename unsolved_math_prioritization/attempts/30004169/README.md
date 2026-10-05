# BLRS descent: audited partial results for problem 30004169

**Status: unsolved, 5/5 approaches. The independent audit passes only within this expressly unresolved scope.**

This packet concerns the Bloch–Levine–Rost–Schmid (BLRS) splice over a perfect field of characteristic different from 2, for smooth separated finite-type schemes, integral Milnor–Witt coefficients, and weights q >= 0. Intrinsic determinant twists remain part of the complex. It is not a claim about the ordinary flasque Rost–Schmid resolution alone.

## Verified scope and the remaining gap

- The weight-zero case is already known and has an explicit contraction here.
- An explicit lower BLRS term is not flasque. This is not a counterexample to descent: the example lies on the affine line, where the published positive comparison applies.
- A quadratic-residue obstruction blocks naive coefficientwise closure. Correcting boundary-supported components remain possible.
- Finite Čech descent reduces to acyclicity of a lower-part augmented defect. The reduction does not prove its vanishing.
- Square-twist identities do not supply the missing global support-moving argument.

For general positive weight, the required defect acyclicity or a genuine nonzero defect class remains unproved. No full solution, general counterexample, or novelty claim is made. Exact bounded code controls supplement the written arguments; they do not compute arbitrary Milnor–Witt groups or constitute formal verification.

## Source hypotheses

The published Bachmann–Yakerson affine comparison assumes trivial canonical bundle and, for general coefficients M, a homotopy-module structure on M_{-q}. Its perfect-field formulation includes finite fields by transfer. Milnor–Witt coefficients meet the coefficient hypothesis.

The separate topology-comparison statement in Chapter 3, Corollary 3.2.13 of *Milnor-Witt Motives* assumes an **infinite perfect field** (with the characteristic restriction in the source). That monograph statement compares derived computations; it does not identify naive BLRS global sections with their localization. This additional hypothesis must not be imposed on the different published affine comparison theorem.

The May 2026 Gysin paper is recorded as a public preprint. Ordinary Rost–Schmid representability does not by itself identify the BLRS splice. The bounded literature search located no full resolution and provides no literature-wide openness certificate.

## Preserved checkpoints

The author folder and ZIP, and the independent-audit folder and ZIP, are byte-identical to their reviewed freezes. Earlier pending-audit and no-remote-write wording records the state when those freezes were made. The later audit is included unchanged and lists no mandatory corrections. This wrapper adds the audit's optional monograph-hypothesis clarification without changing either freeze.

## Replay

Use Python 3 with assertions enabled. Run:

    python3 verify_publication.py --expected-manifest <MANIFEST-SHA256>

The externally recorded digest is in the draft PR description. In a repository checkout, optionally append:

    --queue ../../QUEUE.md

The verifier binds the exact inventory, both manifests and both original ZIPs; checks all ZIP members against their frozen folders; and replays the author and independent offline controls from an unrelated working directory. Optimization flags are rejected. Optional source, dataset, and catalog byte checks in the audit require external inputs; offline replay does not claim to retrieve or recheck those inputs.

Only the target queue row's Status and Turns cells change. Findings, Chat, DOI, all other rows and the stale embedded queue header are preserved byte-for-byte. Contents are authored proof, review and code, plus public bibliographic/verification metadata. No scholarly PDFs or extracts, raw datasets, or private coordination files are included.

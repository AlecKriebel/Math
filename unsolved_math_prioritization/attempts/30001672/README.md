# Existing negative resolution: Boolean coalition influence

Problem **30001672 / OWR-4791-032**, *High Influence Small Sets in Boolean Functions*.

**Status: already_solved. One substantive route (1/5). No new discovery claimed.**

[Kahn–Kalai (2013), Theorem 1.1](https://arxiv.org/abs/1308.2794), also published in [Bourgain–Kahn–Kalai (2024), Theorem 1.1](https://toc.cs.uchicago.edu/articles/v020a004/), provides exactly balanced functions with a fixed inverse-polynomial deficit in output-1 reachability for every coalition of size at most n/3. The probability that a fiber remains undetermined is bounded by that reachability. A polynomial deficit eventually exceeds any prescribed exponential deficit c^n, so the proposed universal guarantee is false.

Exact balance is obtained by constructing at a higher limiting mean and deleting enough 1-inputs. This preserves the upper bound for one-sided reachability J^+; it does **not** require the undetermined-fiber probability U to decrease under support deletion. Neither a novel construction nor an optimal exponent is claimed.

## Evidence and review

- [Frozen author proof](author/PROOF.md), sources, log and exact controls are retained byte-for-byte.
- [Full independent adversarial AI audit](audit-independent/AUDIT.md) independently checks the source, theorem application, quantifiers and construction parameters. It also gives a specialized construction check and tests the unsafe support-deletion inference explicitly.
- The historical author files correctly show that review was still pending at their freeze. This release note and [STATUS.json](STATUS.json) record the subsequent independent PASS; the frozen history has not been rewritten.

The outcome is a prior-literature correction. No new peer-reviewed result is represented by this packet, and AI review is not a substitute for human mathematical review.

## Reproduce

Run `python3 -B verify_packet.py` from this directory. Python 3.10+ and its standard library suffice. The verifier checks exact inventory and hashes, both frozen manifests, the original 1,050,698-pair controls, the independent 1,050,698-pair controls, 52,833 support-inclusion checks and 112 exact clause-probability checks. It also requires deliberate corrupted copies to fail integrity checks.

`SHA256SUMS` covers every other file in the packet, including `MANIFEST.json`. The manifest separately lists the safe payload. All controls are finite; asymptotic existence and the limiting comparison require the written mathematics. Only newly authored reports, proofs, code, results and manifests are distributed. No source PDFs or full-text extracts are included.

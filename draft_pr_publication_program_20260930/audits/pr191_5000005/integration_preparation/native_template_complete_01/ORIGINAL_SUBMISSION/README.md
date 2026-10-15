# 5000005 — signed types of parallel short trajectories

**Current status: full candidate passed separate adversarial AI review; claimed solved, awaiting human review.**

This attempt concerns Fuchs's Conjecture 2.6, the signed rule
\(A_k\mapsto A_{\varepsilon k-\ell}\) at angle \(\ell\pi/n+\varepsilon\alpha\), with even \(\ell\) for even \(n\). It does not duplicate the labelled length-ratio target 5000006 / PR152.

- [Independent review](review/REVIEW.md): PASS_COMPLETE_SIGNED_TYPE_RULE, no mandatory mathematical correction; 441,920 independently authored exact controls passed
- [Candidate proof](CANDIDATE.md): common cyclic germ labels, endpoint reflection in model directions, affine common-shift transport, and exact angular alignment
- [Exact checker](verify.py) and [receipt](verification.json): 3,276,822 integer/rational assertions passed
- [Source audit](SOURCE_AUDIT.md) and [manifest](source_manifest.json): primary conventions, dependencies, provenance, limitations
- [Continuity](continuity.json): one interrupted earlier turn plus this reconstruction, **2/5 consumed turns**, one approach family
- [Research log](RESEARCH_LOG.md): checkpoints and completion estimates

Run the controls with `python3 verify.py` from this folder. They do not replace the proof, imported classical results, or separate review.

The prior local-only candidate is missing. This reconstruction has its own hash and is not represented as a recovery of identical bytes. It preserves the earlier route and credits the already-reviewed cone/type work in [PR152](https://github.com/AlecKriebel/Math/pull/152). The PR152 review does not itself verify the new endpoint-matching argument.

The candidate and frozen author metadata retain their original pre-review status labels for hash integrity. The later review above supplies the current result. The mathematical proof was not changed by review.

This is AI-generated research, not human peer review. Historical priority is unconfirmed. It relies on credited classical Veech theorems read in complete later primary papers; the original Veech full text was not retrieved. A draft PR is the intended publication checkpoint; no merge, release, DOI, or researcher outreach is part of this work.

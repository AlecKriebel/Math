# Research log: 2302073 / AMR-022-2073

All times UTC, 4 October 2026. One substantive investigation turn was used. Tool calls, source reads and sections of the proof are not separate attempt turns.

## Turn 1: source-first recovery and verification of a prior resolution

### 07:39–07:40 — exact target recovered

The live catalogue page failed to load. The public matching dataset record and Hayman–Lingham's primary Problem 2.73 were recovered. The actual question asks whether a normal family with two entire parameters can fail to factor through one entire parameter. The source's 2018 no-progress update and the queue's queued/0/5 row do not establish current openness. Exact-ID PR and code searches did not locate earlier work.

Completion estimate toward the target's mathematical disposition: 10%. No new theorem established at this checkpoint.

### 07:40–07:41 — current primary resolution located

A preliminary rigidity idea was considered: normality might force rank-one parameter dependence and then global factorization. It was not promoted to a lemma. The gap was that boundedness of other evaluations on fibers of one evaluation does not justify a global Liouville argument on those fibers. No general theorem establishing the claimed rank bound was found or used.

Current primary-source searches located He–Tang–Zhang, arXiv:2603.20883v1 (21 March 2026), whose Theorem 1.2 gives an affirmative answer to the exact question. Their construction has a nowhere-zero parameter Jacobian, so it rules out the preliminary rank-one route. Source verification replaced further new-solution search.

Completion estimate: 35%, pending inspection of the full proof and its basin theorem.

### 07:41–07:45 — full construction and dependencies checked

The entire He–Tang–Zhang proof was read: the inverse polynomial map, local weighted contraction, backward-invariant containing sets, the coordinate changes into the parabolic tube, both normality cases, and the differential contradiction to factorization.

The Rosay–Rudin theorem and its relevant complete proofs were retrieved and read. A direct specialization was derived using the normalized iterates M^(−n)f^n. The geometric ratio is 27/32<1. The reconstruction proves the biholomorphism globally, including injectivity and surjectivity, rather than merely citing its existence. The determinant can be normalized to 1, yielding defect 1/625 after the fixed coordinate changes. This is a classical normalization, with no novelty claim.

Completion estimate: 90% for an attributed complete reconstruction; independent audit outstanding.

### 07:45–07:50 — prior-report gate and reproducible algebra

The pinned public research-results corpus was read selectively in memory; the exact dictionary-key report contains no proof, only an obsolete open-triage assessment based on the 2018 edition. Root listings, the actual attempts directory, a recursive problems tree, related-target groups, branch/commit searches and broad Rubel PR results were checked. No actual earlier target attempt was found. Recursive attempt-tree reads failed with transport errors; the successful actual directory listing is the evidence retained.

The complete proof was written in PROOF.md. The verifier checks 35 exact algebraic and rational assertions, including inverse compositions, contraction and summation constants, threshold inequalities, both Jacobian computations and the factorization obstruction. It uses no numerical approximation or orbit sampling. Its deterministic output was reproduced. Analytic convergence and global normality remain proof obligations discharged in the written proof, not in finite tests.

Completion estimate: 100% for author reconstruction of the known answer, conditional on independent review; 0% claim of a new discovery.

## Turn accounting and stopping condition

Turn 1 establishes a complete prior affirmative resolution and an explicit verification packet. The early-stop condition for a known full resolution therefore applies. No additional proof-search turns are claimed, and no five-turn exhaustion is asserted.

Requested disposition: already_solved, 1/5. Independent review is pending at the author freeze. No remote changes, merge, release, publication deposit or outside communication were performed during this turn.

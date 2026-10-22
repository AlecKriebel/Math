# Independent cover-reduction adversarial review log

Scope: adversarial mathematical review of the proposed tripartite-cover reduction from uniform triangle-freeness testing to vertex-distribution-free testing of the fixed property P. Work is confined to this review folder. No other review reports are consulted. No external communication, Git mutation, or PR action is authorized or performed.

## 2026-10-17 19:31 UTC — initial checkpoint

Best-guess completion: **30%** of this independent review.

- Read the pinned `../../inputs/PROOF.md`, focusing independently on the definition of P, its distance normalization, and Lemma 3.
- Established the elementary cover-distance proof at the proposed factor 1/9, including why arbitrary repairs can be replaced with deletions.
- Independently reconstructed Lemma 3's lower bound: a K4-free repaired graph forces the undeleted apex neighborhood to be triangle-free; isolating vertices with deleted apex edges costs no more than their normalized apex-edge deletion budget.
- Identified the required n≥1 guard. The empty graph is a trivial yes-input and can be accepted without invoking the weighted construction.
- Next: write a fully quantified oracle simulation and run exact finite cover-distance controls on every labeled graph with n≤4.

The strongest verified result so far is the elementary finite-graph distance implication. No primary-source classical lower bound is being promoted at this checkpoint.

## 2026-10-17 19:32 UTC — exact finite control checkpoint

Best-guess completion: **80%** of this independent review.

- Completed a dependency-free exact triangle-hitting-set computation on all 76 labeled graphs with 0≤n≤4. All cover-distance inequalities and triangle equivalences passed; 24 cases contain triangles.
- Checked the K4 boundary explicitly: τ(H)=2, τ(L)=12, and the cover has 24 triangles.
- Completed the unrestricted adaptive simulation argument. No permutation is needed, even if the cover structure, distribution, apex, names, and size are revealed.
- Added two oracle guards: the apex self-query is 0, and different-part copies of the same original vertex have adjacency 0 without issuing an original loop query.
- Drafted the full report. Next: independently reread formulas and quantifiers, validate the saved artifacts, and record hashes.

Strongest verified result: the complete algorithmic reduction at factor 36, including arbitrary additions, all n≥1, and direct acceptance of n=0. The external classical lower-bound import remains outside this review's verified claim.

## 2026-10-17 19:34 UTC — final review checkpoint

Best-guess completion: **100%** of the assigned reduction review.

- Reread the cover-distance proof, the independent heavy-apex argument, all constants, and the oracle simulation.
- Rechecked that the saved result file matches the authored script hash, includes exactly 76 cases and 24 triangle-containing cases, and satisfies all proposed distance inequalities.
- Final verdict: **PASS with explicit n=0 and self-query guards; no substantive counterexample or gap found.**
- Final scope boundary: the exact source theorem needed for an imported classical asymptotic lower bound has not been independently checked here. The completed report promotes only the elementary reduction and its exact complexity comparison.
- Recorded hashes of the report, script, result file, this log, local ignore file, and the pinned source proof in `HASHES.sha256`.

No external communication, other-review reading, Git mutation/fetch/index operation, or PR action occurred.

# Source gate: orientation-compatible integer vertex multicover

Checked 2026-10-21. Queue row 1872, ID 3000062, AMR-029-0062. This is the exact successor of row 1871 (3000040). The recovered question matches the Egres problem page; no generated replacement theorem was substituted.

## Exact mathematical scope (authored normalization)

Input: a finite digraph D=(V,A), with each arc a assigned a nonnegative even integer W_a. Output: nonnegative INTEGERS x_v such that x_u+x_v >= W_uv for every arc uv, and every vertex v with x_v>0 has at least one INCOMING arc uv satisfying x_u+x_v=W_uv. The question is whether an output can always be constructed in polynomial time in the binary-encoded input length.

There is no objective to minimize sum(x), no binary restriction on x, no requirement that every arc be tight, and no permission to reverse the incoming witness. Even weights do not require even coordinates. The manuscript defines the cover in integer vectors; the shorter wiki wording leaves that implicit.

## Sources and established results

- [Egres problem page](https://oldlemon.cs.elte.hu/egres/open/Orientation-compatible_w-vertex_cover): retrieved successfully with HTTP 200 after the web reader could not access it. Revision 1600, last modification 2013-12-16 19:00. The page remains in its open-problem category, but this stale classification is not proof of current unresolved status.
- Tamás Király and Júlia Pap, [PPAD-completeness of polyhedral versions of Sperner's Lemma, EGRES TR-2012-04](https://egres.elte.hu/tr/egres-12-04.pdf), §3, Theorem 3.4, Question, Proposition 3.5.
- Same authors, [2013 author-submitted manuscript](https://real.mtak.hu/20824/1/dm_submission.pdf), Theorem 9 and Proposition 10. [Repository record](https://real.mtak.hu/20824/) explicitly identifies this PDF as a submitted version. [Publisher record](https://doi.org/10.1016/j.disc.2013.04.006) verifies publication in Discrete Mathematics 313(15), 1594–1599 (2013); the publisher typeset full text was not independently inspected.

Existence is already established. An indegree-one polynomial construction is already established. The manuscript explicitly leaves the general polynomial-time construction open. Its PPAD-completeness results concern broader polyhedral search problems; their title is NOT a hardness classification of this special graph problem. A fresh existence proof or indegree-one construction is not a solution of the remaining question.

## Source/proof traps

1. Integral polyhedron does not imply that an arbitrary LP optimum obeys the required incoming tightness condition. Cover feasibility alone is insufficient.
2. The quoted manuscript's cycle-algorithm prose says to take the minimum of zero and a residual, inconsistent with nonnegativity and its following discussion. The intended recurrence is max(0, W_previous - x_previous). Its displayed alternating-weight description also appears to omit the factor 2 under its w rather than W convention. Any implementation must derive the recurrence from the constraints, rather than copy that prose.
3. Evenness belongs to the INPUT. Dividing the weights by two without tracking output integrality can silently weaken the task.
4. A pseudo-polynomial bound in maximum weight is not a binary-input polynomial bound.
5. Finite testing, a fixed-dimensional algorithm, or solving only uniform weights does not settle the unrestricted problem.

## Duplicate and current-status checks

The 15,458-record corpus has one exact title match and no second record matching the orientation/even-weight vertex-cover filter. Its associated research record is OPEN-TRIAGE with no cited resolution, and omits the primary-source existence and indegree-one results. This is not authoritative evidence of openness.

Fresh public searches on the exact title, orientation-compatible cover variants, the 2w-cover formulation, and Király/Pap plus vertex-cover/orientation terms retrieved the source paper and Egres pages but no verified later solution or hardness theorem for this exact problem. The 2022 stable-hypergraph/multicommodity-flow complexity paper surfaced as related work; its exposed results concern different problems, so it cannot be counted as a resolution here. Negative search results are not an exhaustive literature proof.

Disposition: source scope VERIFIED; general algorithmic question NOT RESOLVED by this gate. Continue substantive work only on the exact integer search problem; retain an open/not-solved classification unless a full algorithm or exact literature resolution is independently verified.

## Publication boundary

Only this authored gate and source_metadata.json are intended as public audit material. Source PDFs, HTML, copied corpus records, and extracted text are private research inputs and must not be included in any publication package. No queue cells or remote repository state were changed by this source-gate task.

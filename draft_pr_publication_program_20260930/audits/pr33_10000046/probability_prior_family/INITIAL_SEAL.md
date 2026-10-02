# Independent initial seal — probability / prior family

UTC seal: 2026-10-02T02:16:47Z. Audit completion estimate: 15%; new proof-attempt responses: 0. Scope is the frozen PR33 original stage, head `de5877c38bf3604f0a8e074af7a9c55fca334522` (actual metadata base `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`). No other review, code, result, sibling report, or root research content has been read. Applicable root and nested AGENTS instructions were read. No shared mutation, paper edits, Git operations, or outside communication is authorized for this subtask.

## Evidence read before this seal

1. Literal archived author URL: https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf . Browser fetch failed; the exact URL was recovered with a direct download and its text read.
2. Benjamini, *Coarse Geometry and Randomness*, dated October 30, 2013: standing graph definitions / SRW convention on printed p. 5, and full section 12.7 endpoint around Open Problem 12.33 on printed p. 104.
3. Frozen `source_snapshot/PARTIAL.md`, read in full only after the literal source.

## Literal target and formal assumptions

Open Problem 12.33 asks whether two simple random walks on Z^3 or Z^4, starting distance 10 apart, can be coupled so their paths have positive probability of not intersecting. Standing distance is shortest-path graph distance, hence l1 on the nearest-neighbour lattice. Each marginal must be the entire discrete-time SRW path law: independent uniform increments from the 2d coordinate directions, starting at the specified vertex. The joint coupling is arbitrary; no causal, co-adapted, Markovian, or independence restriction appears. Full trace disjointness means X_i != Y_j for **all** i,j >= 0, including both initial vertices. Same-time avoidance and matching one-time distributions are insufficient.

The literal question does not explicitly quantify over every orientation of the distance-10 displacement. The package fixes arbitrary x,y with l1 distance 10. I will audit that stronger natural formulation explicitly, separately for d=3 and d=4; a theorem allowing every nonzero displacement certainly covers it. A d=4 attribution cannot become a solution or new result for the bundled d=3/d=4 target.

Success criteria: (i) the probability assertions follow from complete marginal laws, with all-time/time-0 boundary cases; (ii) cited prior theorems genuinely cover full traces, arbitrary starts at distance 10, and arbitrary couplings; (iii) any full-proof verification or unverified repair boundary is stated accurately; (iv) original code/results replay without altering original artifacts; (v) current primary-source status is checked without claiming the bounded search proves openness.

## Sealed independent mechanisms and falsifiers

**T — synchronous translation.** Put Y_n=X_n+v, l1(v)=10. Within a single N-step trace, displacement between times has l1 norm at most N; therefore trace collision is impossible for N<10, regardless of orientation. For infinite time, choose a fixed 10-increment geodesic word summing to v. Disjoint increment blocks are iid and have positive probability (2d)^(-10) of that word. Almost surely infinitely many blocks occur; each forces X_(10k+10)=Y_(10k). This is a probability-one full-range collision, although X_n !=Y_n always. Falsifiers: a non-SRW increment marginal, dependent blocks, time-0 excluded, or treating same-time noncollision as full-range noncollision.

**H — fixed initial vertex obstruction.** Every coupling loses full disjointness whenever X visits y, because Y_0=y. Thus alpha(x,y)<=1-P_x(T_y<infinity)<1, with the strict inequality obtained from any geodesic word of positive probability. If a_i=|v_i| and sum a_i=10, the probability of first hitting y by time 10 is exactly 10!/(product a_i!)*(2d)^(-10): no earlier hit is possible and every successful 10-step path is a geodesic permutation. Falsifiers: wrong graph versus Euclidean distance, double-counting signs or repeated directions, allowing earlier hits, or omitting initial vertices.

**G — additional graph / geometric controls.** At translation horizon N=10, a collision can only involve times 0 and 10. Collision probability is exactly twice the geodesic count divided by (2d)^10, accounting for displacement +v and -v. Exact orientation controls should compare axial (10,0,...) and spread displacement, and enforce lattice parity. The distance-10 claim must fail to extend to a shorter graph-distance displacement at horizons reaching that distance; the all-time obstruction is orientation-independent. These are proof-driven adversarial controls, not extrapolations from small finite counts.

**P — existing 4D prior.** Read primary Benjamini–Kozma theorem, definitions, Hall-matching construction, annular estimates, and final induction plus source TeX; identify dependencies and determine the bounded repair needed for the two reported typographical inconsistencies. Falsifiers: tails replacing full traces; initial vertices omitted; start-distance restrictions; failure to preserve full path marginals; nonsummable induction error; a repair transferring the central estimate to an unsupported statement. Acknowledging intended attribution is distinct from certifying the complete paper.

**S — current 3D source status.** Read the new Shi et al. paper's full relevant statements and assumptions. Independent-walk exponents alone do not evaluate unrestricted coupling probability. Falsifiers: an actual arbitrary-coupling theorem, explicit coupling result, or a theorem whose quantified law differs from the inference attributed to it. Check all arXiv versions/status directly; record receipts.

## Initial verdict

The package correctly distinguishes the unresolved bundled target from its 4D attribution and labels its transport reduction standard. Its iid-block and initial-hit mechanisms appear formally sound under the sealed SRW model. I have not yet verified the original computation or the prior paper's proof. The principal prior-audit issue is whether attribution is adequately qualified where a complete mathematical repair has not been independently checked. No new 3D route will be pursued in this audit.

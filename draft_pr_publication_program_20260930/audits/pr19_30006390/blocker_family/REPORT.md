# PR 19 blocker-family adversarial audit

**Verdict: PASS_UNRESOLVED_PARTIAL_ANALYSIS for this mathematical family.** No blocker-geometry error or required mathematical repair was found at exact head `f1053196b6405623d5f5d8611289939765918d72`. The strongest verified lower bound is the classical Bruen bound, with its event exceptions and exact integer rounding. Neither the divergent-ratio conjecture nor its logarithmic strengthening is proved, and no novelty is established.

## Verified claims and assumptions

The baseline proof uses only finite projective-plane axioms. It applies to every existing plane of integer order q>=2, without assuming field coordinates or that all possible plane orders are prime powers. For every ordinary blocker B that contains no line,

|B| >= q+ceil(sqrt(q))+1.

The incidence parameters also have a direct axiomatic check. For any point x, choose a line not through x; lines through x correspond bijectively to its q+1 points by unique intersection and unique join. Thus the degree is q+1. The q+1 lines through x partition all other points into q-point pieces, giving n=q(q+1)+1. Counting all point-line incidences then gives exactly n lines. Nondegeneracy supplies a quadrangle and excludes the degenerate order-1 triangle. The exact finite constructions explicitly check a quadrangle, point degrees, line lengths, unique joins, and unique meets.

The proof's two indispensable conditions were checked separately: ordinary blocking supplies r_L>=1; absence of a whole line supplies x in L outside B and r_L<=|B|-q. The exact summed inequality is

|B|(|B|-1) <= (|B|-q) (|B|(q+1)-(q^2+q+1)),

whose difference of sides, with a=|B|-q-1, is q(a^2-q). The argument does not assume minimality or an equality-case classification. The universal derivation is preserved in the sealed `INDEPENDENT_ANALYSIS.md`.

For the random half of the **point** set, the no-empty-section and no-full-line exceptions each have probability at most (q^2+q+1)2^(-(q+1)). Outside their union, every admissible transversal is a nontrivial ordinary blocker, so the lower bound holds with high probability. R=empty, R contained in a line, and R equal to a whole line prevent a false deterministic extension. In particular, tau(empty)=0 and tau(R)=|R| when R lies in a line. The PG(2,2) good event is empty; this is consistent with the asymptotic statement and shows why small-order probability controls must not be overinterpreted.

On the no-empty-section event, tau(R)<=k if and only if R contains an inclusion-minimal ordinary blocker of size at most k. Minimality is equivalent to a tangent-line witness at each selected point. A minimal blocker containing a whole line must equal that line. These facts justify use of **all** minimal blockers, without an unsupported structural classification.

For the deterministic family M_q(k) of such blockers,

P(tau(R)<=k) <= (q^2+q+1)2^(-(q+1)) + sum_{B in M_q(k)} 2^(-|B|).

This is a sufficient first-moment route, not a necessary criterion. The line members are negligible asymptotically, but no usable weighted count of the nontrivial members at every threshold Cq is established. That count, or a different mechanism excluding small blockers from R, remains the central gap. The derivation transfers the difficulty rather than solving it; the ratio of the established Bruen lower bound to q tends to 1.

## Independence and fresh controls

The independent proof and first computation were sealed at 2026-10-01 17:31:28 UTC before the candidate programs, previous results/reviews, root findings, or sibling findings were read. The sealed hashes and exact input boundary are in `independence_seal.json`.

The pre-seal program constructed the two small planes by affine completion and directly optimized transversal size over every pair B subset R using covered-line sets. Ordinary-blocker and minimal-blocker subset transforms were then compared with that independent optimum. It checked 8,320 R-subsets, examined 1,596,510 (R,B) candidates, and passed 104,600 counted assertions. The certificates retain every tau(R), all lines, and every minimal ordinary blocker. This is evidence at orders 2 and 3 only.

After the seal, a supplementary mechanism constructed cyclic planes from perfect difference sets {0,1,3} in Z_7 and {0,1,3,9} in Z_13. Explicit join/meet closure produced complete incidence isomorphisms to the sealed affine planes, without invoking small-order uniqueness classifications. An incremental minimal-hitting-set antichain construction independently reproduced all minimal blockers. Dual inclusion-exclusion over all 8,320 **line** subsets independently reproduced every coefficient of the blocker-cardinality polynomials. These controls are preserved in `dual_count_controls.py` and `dual_count_results.json` and are explicitly distinguished from the pre-seal evidence.

The exact small-order census is:

| Plane | Retained subsets | Ordinary blockers | Nontrivial blockers | Minimal blockers |
|---|---:|---:|---:|---|
| PG(2,2) | 128 | 64 | 0 | 7 lines, each size 3 |
| PG(2,3) | 8,192 | 4,330 | 468 | 13 lines of size 4; 234 nontrivial sets of size 6 |

The order-3 triangle-side boundary with vertices removed gives a 6-point nontrivial minimal blocker attaining the rounded lower bound. The corresponding order-2 construction is a whole line, a negative control against unqualified transfers.

## Exact replay and integrity

The candidate author and reviewer programs were run from byte-identical standalone copies in ignored `tmp/` directories. Their generated JSON files match the stored source outputs byte for byte. Each covers all 8,320 point subsets. Actual reviewer `verify()` calls were observed and independently counted from its call sites and independently determined census values: 467 checks at order 2 and 27,605 at order 3, totaling the claimed 28,072. Following the unmodified author replay, a separate in-memory assertion-entry observer counted 5,344 author assertions; observing entries avoids overcounting generator-related source-line events. The standalone copies remain byte-identical to the snapshot.

An explicit affine-to-homogeneous point permutation was checked on every line, establishing that the author's homogeneous construction agrees with the sealed affine construction. All 13 exact-head source-snapshot file hashes were unchanged before and after replay. Baseline SHA-256 remains `9e0a930e61d849799c4395024c85d4f9c75b63ae2172321ef78ebf643f283c82`. Detailed measurements and all input hashes are in `reproduction_results.json`.

The shared-point failure dependence was checked analytically and on every line pair in both small planes: the joint empty-section probability is twice the product of marginals. Conditioning on a fixed ordinary blocker being contained in R already forces all sections to be hit by that blocker. An independent-incidence model cannot substitute for the target model.

## Scope and remaining gap

This family certifies the universal blocker proof, event-qualified reduction, exact integer bound, minimality equivalence, geometric/model boundary cases, and finite reproducibility. Container hypotheses, source normalization, and the upper-bound probability calculations belong to the other audit families. No promotion to a solved result is warranted by this report. Classical attribution, unresolved status, and finite-evidence limitations should remain explicit.

No Git changes, environment installation, external communication, publication action, DOI operation, canonical paper edit, tracker change, or new central attempt were made by this audit agent. The original unsolved 2/5 attempt state is untouched.

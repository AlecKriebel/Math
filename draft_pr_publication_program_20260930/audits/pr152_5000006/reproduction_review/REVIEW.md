# PR152 independent computational adversarial review

## Verdict and scope

The frozen numerical claims reproduce: the author verifier reports **14,630** checks and the frozen independent checker reports **60,055** checks. Neither count establishes Conjecture 2.7. A separate physical billiard search found no labelled sine-ratio counterexample in the tested range.

Two actionable findings were established. First, the original `ck` uses removable Python `assert`; an explicitly false check still produces `PASS` under `-O`. Second, the candidate identifies physical source-label reversal with intrinsic saddle-connection reversal without the necessary initial-chart qualification. An exact pentagon path demonstrates the difference. The proposed repaired proof makes this distinction, and its revised verifier passes **19,458** controls both normally and under `-O`; both modes reject the false-control mutation.

This is a bounded computational review, not an all-n proof approval. The repaired chart statement is compatible with the exact source-angle algebra and all physical controls performed here. Universal affine/cusp arguments require the separate proof and source audits.

## Frozen inputs and independence

Frozen candidate SHA-256: `100454abdfcbeb6647e0e0596a86b86b3a39d330de2605fe485ae242d9e91c9a`.

Frozen author verifier SHA-256: `8e7b57f47567c0cb61f1090af50d1f13da09859f8b63a15444da3f60d1ceb5cd`.

The candidate and complete author verifier source were inspected before execution. The independently devised mechanism was then formed and tested before reading the old independent checker: enumerate reflected polygon copies, propose rays to their vertices, and trace those rays in the physical original polygon using first side intersections and specular reflections. Terminal physical angles and unfolded corner labels are measured, not generated from the candidate's index equation. No old review verdict was read. The old independent checker was inspected and replayed only after the physical mechanism and its first results existed.

All executed programs import only inspected standard-library dependencies. Replays use `/opt/homebrew/opt/python@3.14/bin/python3.14 -E -S -B -P` and owned copies. No frozen file, Git state, publication tracker, or remote was changed, and no external communication occurred.

The primary convention check is Fuchs, [Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra](https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf), §§1.1, 2.2–2.3 and Conjecture 2.7, printed pp.494, 502–506, 512. The sign in the endpoint-angle condition is selected by segment parity. No neighboring conjecture is assumed.

## What the advertised controls establish

The author's endpoint disjoint-set calculation meaningfully checks the proposed edge pairing. Direct-chord labels and rational source-branch comparisons check finite algebraic consistency. The corner-index loop generates beta from the proposed cone difference, then checks consequences of that same equation; it does not discover or trace an admissible trajectory. The fixed-point count is supplied as `n + n%2`, rather than obtained by solving a fixed-point problem. The four rational matrix controls test linear identities; the matrices are not shown to be affine automorphisms of the surface.

The old independent checker improves coverage by traversing corner cycles, testing all source-angle grid points rather than five start angles, and considering the full twelve triangular-lattice symmetries. Its nonlinear angular map is an explicitly constructed antipodal lift, rather than a measured lift of every affine automorphism. Its lattice search assumes the source's marked-point set. These are useful exact controls, but neither script tests the imported Veech/cusp theorem application or universal chart normalization.

Both original checkers use removable assertions. `optimization_audit.py` replaces the author's first vertex-class condition with literal `False` in isolated copies. The normal run exits 1; the optimized run exits 0, reports `PASS`, and still counts 14,630 checks. Repair: raise an explicit exception on a false condition, or refuse optimized mode. The repaired verifier uses explicit `RuntimeError`.

## New physical and exact evidence

`physical_controls.py` examines n=3,…,16, with reflected-copy depths 5 for n≤6, 4 for 7≤n≤10, and 3 thereafter. It independently verifies **925 physical first-vertex trajectories**, with source labels and cone indices measured from the traced path. **684 comparisons** within the complete Fuchs direction orbit preserve L/sin((k+1)pi/n). The largest relative discrepancy is `4.618527782440651e-14`.

The search includes source parallelism under theta -> ±theta + 2*pi*j/n modulo pi, rather than only identical unfolded slopes. Physical polygon reflection, physical reversal, source angle bounds, copy-to-double-polygon translation matching, and a deterministic tighter-tolerance repeat are checked. Additionally, **401 primitive lattice paths each** for n=3,4,6 are physically traced and their measured source types agree with the elementary lattice rules. The maximum segment counts in these three controls are 96, 48, and 35. Exact triangular-lattice visibility and all twelve symmetry transforms are also checked over primitive integer directions in [-30,30]^2.

The final physical result records **61,794 control calls**, with **156 intentional failures**, all in `candidate_unqualified_physical_reversal`. Every repaired parity-sensitive physical reversal control, every weight control, and every other category passes. The maximum endpoint discrepancy is `1.7453816170132086e-12`, copy-match discrepancy `1.5739134377203758e-13`, and distance of the measured cone index from an integer `2.6645352591003757e-15`.

## Exact source-label reversal witness

Let c=cos(pi/5)=(1+sqrt(5))/4, u=cos(2*pi/5)=(sqrt(5)-1)/4, s=sin(pi/5), and v=sin(2*pi/5)=2cs. A side-one clockwise regular pentagon has

O=(0,0), P1=(-u,v), P2=(1/2,v+s), P3=(1+u,v), P4=(1,0).

The vertical ray from O reaches A=(0,2s) strictly inside side P1P2. Its reflected direction is (v,-u), normal to side P3P4; it reaches B=(5/4,2c²s) strictly inside that side. The normal reflection retraces BA, and the reflection at A returns vertically to O. Thus **O-A-B-A-O** is a short physical billiard path with side word [1,3,1] in zero-based indexing. Convexity and the strict side-interior certificates exclude intermediate vertices. It has N=4 and alpha=beta=pi/2, so the source difference condition gives k=-1 mod3=2. Its physical reverse is the identical path, still A2; the unqualified prediction -k mod3 is A1.

`exact_reversal_counterexample.py` supplies 15 non-removable exact controls in Q(sqrt(5)) for this construction. This refutes the unqualified physical source-label reversal statement, **not** the sine-ratio theorem: w5(1)=w5(2).

Generally physical reversal gives alpha'=pi-beta, beta'=pi-alpha. For odd N the sum index changes s -> n-s, so k'=-k modulo n-2. For even N the difference index is unchanged, so k'=k. Hence **k'=(-1)^N k**. Reflection across the initial vertex bisector instead gives alpha'=delta-alpha, beta'=pi+2pi/n-beta, and k'=-k for both parities.

The necessary repair distinguishes the intrinsic cone index K from the physical source label. K=k for an orientation-preserving initial P chart and K=-k for a reflected Q chart. The oriented saddle connection itself reverses K -> -K. The reversed physical lift starts in P for odd N and Q for even N, explaining precisely the parity difference. Since w(-k)=w(k), the invariant quantity needed by the ratio proof survives both chart orientations.

## Repaired artifact reproduction

Reviewed repaired candidate SHA-256: `e6d40a40032b5af335777abf692e6b0bb45b1582f85d7a02bed192b4984217b9`.

Reviewed repaired verifier SHA-256: `144f07e343c494548935b9214d15cfa75a6be7b035b1b1b71deca550bcb922f8`.

The repaired Section 3 explicitly defines K, explains the orientation-reversing Q fold, and derives the parity-sensitive physical reversal law. Its model-direction argument uses intrinsic weights. `repair_reproduction.py` independently copies these inspected files into owned directories and runs all four normal/optimized and unmutated/false-control combinations. Both unmutated modes pass **19,458** controls; both false-control modes exit 1. The receipt and complete diagnostic output are retained in `repair_reproduction_results.json` and the four owned replay folders.

## Remaining limits

The physical search uses double precision and finite copy/direction deduplication. Its hit, angle, and grouping tolerances are explicit in the source. Repeating selected paths with a 100-fold tighter hit tolerance reproduces their reflection sequences and endpoints, but does not make this validated interval arithmetic. The search is incomplete beyond its finite n/depth/radius limits. The 100-segment cap exceeds all tested small-lattice paths but remains a general search restriction.

No finite output here proves the all-n ratio theorem, historical novelty, cusp classification, affine map existence, hyperelliptic uniqueness, or universal affine cone-germ action. No sine-ratio counterexample was found. The strongest independently checkable negative result is the exact physical-reversal label witness; the strongest positive result is bounded agreement of measured physical labels, cone indices and source-parallel weighted lengths, plus reproduction of the repaired explicit controls.

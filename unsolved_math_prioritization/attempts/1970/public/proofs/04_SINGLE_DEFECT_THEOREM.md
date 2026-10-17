# All-scale single-defect theorem

This is a newly authored reconstruction with an exhaustive finite certificate. It does not identify the unrestricted optimum with the one-defect optimum.

## 1. Statement and dependencies

Use the notation and definitions of [the structural supplement](02_EXACT_ONE_STRUCTURE.md): the vertices are

P_X = {(a,b) in Z_{≥0}^2 : 2^a 3^b ≤ X},

and the contained corners are {(a,b),(a+1,b),(a,b+1)}. For a hitting set H, D(H) is the sum of its corner hit counts minus one. Write q1(X) for the minimum size with D≤1 and C_r(X) for the color-r count, color a+2b modulo three, after omitting isolated vertices. For X≥3 the only possible isolated vertex is the largest pure power of two; for X<3 every vertex is isolated.

Define ε_r(X)=1 exactly when

24·2^m ≤ X < 27·2^m,  m≥0 an integer,  r≡m+2 (mod 3),

and define it to be zero otherwise. The intervals are disjoint.

**Theorem.** For every real X≥1,

q1(X) = min_{r=0,1,2} (C_r(X) - ε_r(X)).

This proof uses the freshly reconstructed height-three rigidity, all-scale q0 theorem, four-profile exact-one terminal correction table, and explicit exceptional patch in the structural reconstruction. It does not assume any earlier acceptance statement. The exceptional patch proves the upper bound. We prove the lower bound below. Unrestricted τ=q1 is not claimed, and the original irrationality problem remains open.

The executable certificate `checks/check_single_defect.py` uses only integer arithmetic and the Python standard library. It rebuilds all local enumerations and exactly solves every smooth cutoff X<3^18. Its generated output is `fixtures/check_single_defect.json`.

## 2. Binary recurrence and local stencil notation

Set A_b=max{a:2^a3^b≤X} for each nonempty row. The indicators of a D=1 cover satisfy

x(a,b+1) = 1 - x(a,b) - x(a+1,b) + 1_{(a,b)=(s,t)},       (1)

where (s,t) is its unique double-hit corner. There cannot be a triple-hit corner when D=1. The bottom row and the defect anchor determine all remaining entries uniquely. A propagated value outside {0,1} rejects that bottom row.

Let T_H denote the triangular stencil with vertices (i,j)≥0, i+j≤H and anchors i+j≤H-1. Its row widths are H,H-1,...,0. Translating it by (a,0) is valid whenever 2^a3^H≤X: every vertex in that stencil has weight at most 2^a3^H because 2≤3. A T_H configuration is exhaustively checked by trying all 2^(H+1) bottom words and applying (1).

Every exact T_3 stencil has bottom word 0010,0100, or 1001. Thus a consecutive run of exact bottom stencils forces one color phase throughout their bottom intervals. A stencil beginning at (j,0) contains defect (s,t) only when t≤2 and

s-(2-t) ≤ j ≤ s.                                    (2)

The unconstrained exact stencils form the left and right phase intervals used below.

We may always omit isolated vertices from a minimizing cover: doing so changes neither coverage nor D and cannot increase its size.

## 3. High-row defects have nonnegative cost

If t≥3, every bottom T_3 stencil is exact. It forces a core phase r through a=A_3+3. The remaining at most two bottom bits contribute a nonnegative correction relative to the adjusted phase, by the exact-one four-profile table. Their perturbation vanishes by row three: its row-b support can only start at a=A_3+4-b, beyond the domain at b=3.

The defect subsequently creates difference +1 relative to the phase at (s,t+1), followed by the homogeneous recurrence d(a,b+1)=-d(a,b)-d(a+1,b). The initial changed phase value must be zero. If both potential next vertices (s,t+2) and (s-1,t+2) are present, their differences are -1 and both phase values would have to be one, impossible for horizontally adjacent vertices of different colors.

If s=0, the support stays on that vertical axis. If s>0, the only possible surviving next vertex is (s-1,t+2), because existence of (s,t+2) implies existence of its left neighbor. The missing right successor remains missing at later stages: the corresponding weight is multiplied by 3/2 at each northwest step. Hence subsequent support is a single northwest chain, until it ends. Its signs alternate +1,-1,+1,... . The phase residue changes by two on a vertical chain or by one on a northwest chain. A fourth changed vertex would have the same residue as the first, but would require phase value one rather than zero. Thus the chain has length at most three and total cost 1,0, or 1. The nonnegative bottom correction and this nonnegative chain prove |H|≥C_r(X).

This is also Section 5 of the structural reconstruction, with the boundary propagation spelled out here. Hence only t=0,1,2 can give an improvement.

## 4. Small scales and the exact finite recurrence

For 1≤X<3^18, the possible domains occur at exactly 280 smooth cutoffs, generated as all 2^a3^b<3^18. Between successive cutoffs the domain is constant. The exceptional indicator changes only at smooth cutoffs 24·2^m and 27·2^m, so the candidate value is also constant on these intervals. The certificate verifies the formula at all 280 cutoffs.

Here is a complete independent description of that exhaustive solver. In column a let h_a be the number of vertices, and represent its chosen bits by a mask m. Adjacent column heights are h and k∈{h,h-1}. Each corner at row b<h-1 has hit count

m_b + m_(b+1) + n_b,

where n is the next-column mask. If the first two bits sum to zero, n_b is forced to one. If they sum to one, n_b can be zero, or can be one at the cost of one excess unit. If they sum to two, n_b must be zero and already costs one excess unit; choosing one would exceed the entire budget. When k=h, its extra top bit is free. These are all choices. Store the minimum total selected cardinality for each state (current mask, cumulative excess 0 or 1), adding the popcount of each next mask. A current column having two adjacent 11 pairs can be omitted immediately because its corners would already have excess at least two. Appending an empty column terminates the recurrence.

This partitions all D≤1 covers by their column masks and never discards a potentially optimal state. The certificate records each exact minimum, a full selected-number witness, and the state counts. It independently validates the witness by direct corner incidence. It then compares the minimum with min(C_r-ε_r). Thus this finite part does not rely on the all-scale formula it is checking.

For the rest of the proof assume X≥3^18. The finite cutoff is chosen for this reduction; no sharper threshold is claimed.

## 5. Low defects near the left axis

First suppose s<3 and t<3. The domain contains T_6. The certificate checks all 128 bottom words for each of these nine defect positions. Exactly the following six configurations survive. Changes are relative to the phase r that appears on bottom coordinates 3,4,5,6; all unlisted changes are zero.

| Defect (s,t) | Phase r | Changes (a,b,Δ) | Total change |
|---|---:|---|---:|
| (0,0) | 1 | (0,0,+1) | +1 |
| (0,0) | 2 | (0,0,+1) | +1 |
| (0,1) | 0 | (0,0,-1),(0,1,+1) | 0 |
| (0,2) | 2 | (0,0,+1),(0,1,-1),(0,2,+1) | +1 |
| (1,0) | 0 | (0,0,-1),(1,0,+1) | 0 |
| (2,0) | 1 | (0,0,+1),(1,0,-1),(2,0,+1) | +1 |

The remaining positions (1,1),(1,2),(2,1),(2,2) admit no T_6 configuration. Every surviving change is supported on a≤2,b≤2. T_6 contains every corner that can meet that support, so the listed finite change itself has exactly the indicated defect and no other changed corner sums in the full first quadrant.

All T_3 stencils beginning at j≥3 are exact. They force the same right phase from bottom coordinate 3 through A_3+3, since their initial four bits overlap the right phase found in T_6. Subtract the listed local change from H. The result is binary and exact-one: on the local support it becomes the phase, and outside that support it remains H. Its remaining bottom changes lie strictly beyond A_3+3. These are separated from the left support and vanish by row three as in Section 3. Equivalently, uniqueness of recurrence (1) splices the listed left change, the unaltered phase, and the usual terminal correction.

The all-scale q0 phasewise argument therefore gives |H|≥C_r, because the left change has nonnegative size and the terminal correction is nonnegative. No low left-axis defect improves its core phase.

## 6. An impossible interior stencil

Now suppose s≥3 and t<3. If 2^(s-3)3^7≤X, then P_X contains T_7 translated by (s-3,0). Within it the defect has relative coordinates (3,t). For each t=0,1,2 the certificate propagates all 256 bottom words, and **none** stays binary throughout T_7.

Consequently every low defect with s≥3 must satisfy

2^(s-3)3^7 > X.                                        (3)

This eliminates the deep interior directly. No unproved localization or informal bubble-removal claim is used.

## 7. Complete residual suffix reduction

Put

k = A_7 = floor(log_2(X/3^7)),   Y=X/2^k.

Thus 2187=3^7≤Y<2·3^7=4374. Since X≥3^18, k≥17. Condition (3) gives s≥k+4.

Exact bottom stencils with j≤min(A_3,s-3+t) force a single phase r through

a = min(A_3+3,s+t).

Both quantities on the right are at least k+4: s+t≥k+4, and A_3-k is six or seven since Y/27∈[81,162). Therefore the bottom prefix through k+4 is fixed to phase r.

Restrict the configuration to a≥k and translate a'=a-k. This is exactly the domain P_Y. Its phase is r'=r-k modulo three, its bottom coordinates 0,...,4 are fixed to that phase, its defect is (s-k,t) with s-k≥4 and t≤2, and its optional isolated pure-two vertex is omitted. There are exactly eight shapes because the complete smooth-cutoff list in [2187,4374) is

2187, 2304, 2592, 2916, 3072, 3456, 3888, 4096.

For each of the eight shapes and each of the three phases, the certificate tries every contained defect with s'≥4,t≤2 and every remaining bottom word, then applies (1). This is exhaustive. It also checks a crucial boundary invariant: **every surviving configuration agrees with its raw phase on its whole column a'=0**. The column has rows 0,...,7. It follows by row-by-row recurrence that the original configuration agrees with the phase at every a<k as well: its bottom does, its defect lies to the right, and the only required interface values on column k agree. This includes any vertices above row seven to the left of that interface. Thus the global cardinality difference from C_r is exactly the computed suffix cardinality difference. The possible isolated vertex is the same rightmost pure-two vertex globally and in P_Y; no isolated left-edge artifact is subtracted.

The complete summary table is below. Entries are (number of feasible configurations, minimum difference from the adjusted indicated phase). The detailed certificate lists every surviving bottom word, defect anchor, changed vertex, and difference.

| Y interval | Phase 0 | Phase 1 | Phase 2 |
|---|---:|---:|---:|
| [2187,2304) | (8,0) | (5,0) | (10,0) |
| [2304,2592) | (7,0) | (5,0) | (9,+1) |
| [2592,2916) | (6,0) | (5,0) | (4,+1) |
| [2916,3072) | (6,0) | (5,0) | (4,+1) |
| [3072,3456) | (10,-1) | (10,0) | (10,0) |
| [3456,3888) | (10,0) | (8,0) | (5,0) |
| [3888,4096) | (10,0) | (8,0) | (5,0) |
| [4096,4374) | (10,0) | (8,0) | (5,0) |

There is exactly one negative-difference configuration in this normalized enumeration. It has Y∈[3072,3456)=[24·2^7,27·2^7), r'=0, and defect (7,1). Its changes are

remove (9,0),(10,1),(8,2); add (10,0),(8,1).

Returning to the global coordinates gives m=k+7 and r=r'+k≡m+2 modulo three, exactly the stated exceptional patch. The suffix lower bound is therefore |H|≥C_r-ε_r.

## 8. Completion

A minimizing D≤1 cover has D=0 or D=1. The D=0 case is bounded below by min C_r, hence by min(C_r-ε_r). A D=1 cover is covered exhaustively by: the 280 finite small scales; a high-row defect; a low left-axis defect; an impossible deep-interior defect; or one of the 24 normalized suffix phase cases. Each gives |H|≥min(C_r-ε_r). Together with the explicit exceptional patch and ordinary phase covers, this proves the theorem.

This theorem about q1 is not an assertion about unrestricted τ. Proving unrestricted τ=q1 or deciding the original irrationality question would require additional work.

## 9. Reproduction

Run `python3 -I -B checks/check_structure.py` and `python3 -I -B checks/check_single_defect.py` from the public package directory. The second command checks three impossible T_7 stencils, nine complete T_6 left classifications, twenty-four full suffix phase cases, and all 280 small smooth cutoffs. Its complete output is in `fixtures/check_single_defect.json`; appending `--check fixtures/check_single_defect.json` freshly recomputes and rejects any difference. Neither invocation changes a file.

Four deliberate corruptions are also tested and rejected: fabricated interior feasibility, removal of the suffix interface invariant, an extra suffix saving, and an incorrect finite minimum. Every substantive check uses an explicit runtime condition rather than Python's optimization-removable assert statement. The package wrapper repeats verification under normal, -O, and -OO Python.

The separate `checks/check_local_independently.py` evaluates the affine recurrence by a closed-form binomial convolution at each vertex, without importing this checker. It checks all 173 surviving suffix configurations, all six left configurations, and the three interior impossibilities against this certificate. The proof above supplies the all-scale reductions; numerical agreement alone is not an all-scale proof.

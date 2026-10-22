# Audit clarifications accompanying the frozen five-turn packet

These are transparent release clarifications from the independent audit,
not a sixth proof attempt. The original 18 author files and their manifests
remain byte-for-byte unchanged. The full audit and its independent controls
are preserved in [independent_review](independent_review/AUDIT.md).

**Disposition remains: original Problem 3.17 unresolved, 5/5 attempts.**
No realized-knot counterexample, global Kricker–Lescop calibration, novelty
claim or impossibility theorem is asserted.

## A. Polynomial residues versus rational-coefficient residues

Write

Q_Delta(x,y,z)=Delta(x)Delta(y)Delta(z), with xyz=1,

and use the normalized root-grid average A_n from Turn 2. The polynomial
H of Turn 3 satisfies A_n(H)=0 for every n. This does **not** imply that
A_n(H/Q_Delta)=0 for a fixed nontrivial Alexander polynomial.

The independent audit gives an exact negative control:

Delta(t)=t+t^-1-1,
A_5(H)=0,
A_5(H/Q_Delta)=12.

On fifth roots, the identity

(t+t^-1-1)^-1=t^2+t^-2-1

holds because the product is 1 modulo t^5-1. Multiplying H by these three
inverse polynomials and applying the exact coefficient-selection rule
produces 12. The audit's checker verifies this without floating-point
evaluation. Thus H must not be described as an arbitrary fixed-denominator
**numerator** perturbation invisible to the rational residues.

The correct unrestricted fixed-denominator statement uses

delta F = Q_Delta H

or, when a prescribed finite logarithmic jet is also to vanish,

delta F = Q_Delta H^[J].

Then delta F/Q_Delta is exactly H or H^[J]. Its reduced specialization,
all admissible rational residues and the indicated finite jet vanish.
The numerator perturbation is nonzero and theta-symmetric. It is integral
when Delta and the chosen kernel polynomial are integral; otherwise one
may clear rational denominators. Multiplication by Q_Delta preserves a
vanishing jet since it is regular at (1,1) and has constant term 1.

This remains a statement in an unrestricted ambient target ring. Degrees
grow with J and with Q_Delta; there is no fixed-genus counterexample, no
claim of actual knot realization, and no contradiction with Turn 5's
bounded-degree reconstruction.

## B. Zero-framed PBW/wheeling bridge for the theta degree bound

The original source discusses a wheeling algebra identification, whereas
the 2007 numerator used for the genus theorem is expressed using inverse
PBW. The independent audit supplies the following low-loop bridge.

For the zero-framed strut-free expansion, nonempty connected input
components have first Betti number at least 1. A nonidentity wheeling or
unwheeling term glues even wheels, each with at least two legs, to input
components. In an affected connected output, let r be the number of input
components, m the number of inserted wheels, and k their total glued legs.
Before gluing there are r+m components; gluing k pairs of legs contributes
the corresponding edges to the connectivity graph. The resulting first
Betti number is

sum_i beta_1(input_i)+m+k-(r+m)+1
  = sum_i beta_1(input_i)+k-r+1
  >= k+1 >= 3.

Therefore nontrivial corrections do not change the connected theta sector,
whose first Betti number is 2. Disjoint unaffected factors do not change
this conclusion when passing to the connected logarithm.

Consequently the zero-framed theta component is unchanged between these
conventions. A 12-fold sum versus an average only rescales the same
numerator and leaves its support bound unchanged. This supplies the bridge
used to apply Ohtsuki's twice-genus degree bound in Turn 5.

The strut-free zero-framing hypothesis is essential to this counting
argument; it must not be silently extended to a framed expansion containing
struts. Nor does the argument calibrate Lescop's scalar invariant against
the exact P_K^theta normalization. The class-dependent constants in Turn 4
and that separate scalar/hair comparison remain outside the proved result.

## C. Evidence and interpretation

The independent audit passes the packet only as scoped partial results.
Its 1,513 exact controls supplement the author's 2,499 controls. The all-n,
all-J and all-degree statements rely on the written proofs; none of these
finite checks proves knot realization or the missing topological input.

The exact unsolvedmath page's recorded 403 limitation remains visible in
SOURCE_GATE.md. “Unsolved” records this campaign's lack of a complete
solution and the absence of a certified resolution in the sources checked;
it is not a guarantee of an exhaustive literature search.

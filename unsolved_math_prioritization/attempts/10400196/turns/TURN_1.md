# Turn 1: an exact obstruction at the quadratic-data level

**Original target remains unresolved.** This turn establishes a scoped algebraic obstruction and a domain calibration, rather than imposing additional axioms on Deloup's abbreviated question. No novelty is asserted.

## 1. Normalization and an automatic but uninformative lift

For a finite abelian group G and a quadratic function q:G→Q/Z with nonsingular associated pairing b, set

    gamma(q)=sum_(x in G) exp(2 pi i q(x)),
    phi(q)=arg(gamma(q))/(2 pi) in Q/Z,
    B(q)=8 phi(q) in Q/8Z.

The phase is defined: writing x=y+h in |gamma|² and using character orthogonality gives

    |gamma(q)|²=sum_h exp(2 pi i q(h)) sum_y exp(2 pi i b(y,h))=|G|.

The first nonzero contribution is h=0, and all others vanish by nonsingularity. Orthogonal sums multiply gamma and therefore add B. The rationality of this phase is the standard quadratic Gauss-sum fact used by the source; none of the obstruction below needs a new general rationality proof.

The reduction Q/16Z→Q/8Z is a surjection with kernel {0,8}. An arbitrary set-theoretic section, composed with a Y^c_1-invariant B, is a Y^c_1-invariant lift and hence has degree at most zero. Thus a purely pointwise choice of argument cannot supply genuinely new degree-one information. This observation is a warning about the literal abbreviated wording, not a claimed solution of the intended problem.

For a concrete nonintegral value, use G=Z/3 and q(j)=(j²-j)/6 modulo1. This is well-defined because changing j by3 alters the expression by j+1. Its pairing is jk/3, hence nonsingular. The values are0,0,1/3, giving

    gamma=2+exp(2 pi i/3)=sqrt(3) exp(pi i/6),
    phi=1/12, B=2/3 modulo8.

Thus a general lift cannot be forced into Z/16Z with the usual reduction to Z/8Z. The rational mod-16 normalization retains the source's Q/Z phase.

## 2. No orthogonal-sum additive lift depending only on the quadratic function

Let q_+ and q_- be the functions on Z/2 defined by

    q_+(1)=1/4,      q_-(1)=-1/4.

Their nonsingular pairings are the same, namely b(1,1)=1/2. Their Gauss sums are1+i and1-i, respectively, so B(q_+)=1 and B(q_-)=-1 modulo8.

**Theorem 1.** There is no isometry-invariant function L from all finite nonsingular quadratic functions to Q/16Z that is additive under orthogonal sum and reduces to B modulo8. This remains false when the domain is restricted to homogeneous quadratic functions.

**Proof.** On F2^4 let A=I+J, with J the all-ones matrix. Since J²=4J=0 in characteristic2, A²=I; it is invertible. For a binary vector x of weight w, Ax=x if w is even, and Ax is its coordinatewise complement if w is odd. Consequently

    q_+^⊕4(Ax) = q_-^⊕4(x) modulo1.

Indeed, in the even case their difference is w/2, an integer; in the odd case the first side is (4-w)/4, which agrees with -w/4 modulo1. Thus A is an explicit isometry between the two fourfold sums. It also preserves the pairing, either by polarization or directly from AᵀA=I over F2.

Any lift must satisfy

    L(q_+)=1+8e,      L(q_-)=-1+8f  modulo16,

with e,f in {0,1}. Additivity gives L(q_+^⊕4)=4 and L(q_-^⊕4)=12 modulo16, irrespective of e,f. These unequal values contradict isometry invariance. Both input functions are homogeneous, so this proves the final assertion as well. ∎

This obstruction does not assume that L factors only through the numerical phase; it excludes dependence on the entire isometry class of q under the stated additivity requirement. Conversely it does not exclude a topological lift that uses information beyond q, and degree-one invariants are allowed to do that.

## 3. Topological consequence under explicitly stated additivity

**Corollary 2.** A connected-sum additive rational mod-16 lift of B on oriented rational homology Spin^c three-spheres cannot have degree zero in the Spin^c Goussarov–Habiro theory.

**Proof.** Deloup–Massuyeau Example3.1 provides the two Spin^c structures on oriented RP³ with quadratic functions q_+ and q_- (their Gauss phases are opposite eighth roots). The quadratic function for a connected sum is the orthogonal sum: this follows directly from the block-diagonal surgery/discriminant construction, or from the splitting of the linking pairing and Spin^c structure.

Take four copies with the plus structure and four copies with the minus structure. Their first homology groups are both (Z/2)^4, and the explicit isometry above identifies their quadratic functions. Deloup–Massuyeau Corollary2 therefore makes these two Spin^c rational homology spheres Y^c_1-equivalent. Every degree-zero invariant takes the same value on them. Additivity and reduction modulo8 force values4 and12, the same contradiction as Theorem1. ∎

This does not disprove the sought degree-one invariant. It rigorously explains why an additive answer, if intended, must involve information beyond the degree-zero quadratic invariant. The known T³ obstruction to descending the full spin Rochlin invariant is a separate, credited statement and is not used as a substitute for this corollary.

## 4. Why the finite Gauss phase cannot be naively used for all Chern classes

The published canonical function for a general Spin^c three-manifold is defined on H2(M;Q/Z). Its finite quotient is obtained through the Bockstein map only when the function vanishes on the divisible radical. The following exact discriminant example isolates the issue.

Take H=Z², the bilinear lattice f=diag(0,2), and characteristic covector c=(2,0). The characteristic condition holds because both diagonal entries are even. Its discriminant group and quadratic function are

    G_f=(Q/Z) ⊕ (Z/2),
    q(r,j)=j²/4-r modulo1.

Here j is represented by0 or1, corresponding to j/2 in the dual lattice's second coordinate. Changing representatives changes the expression by an integer. The associated pairing is jj'/2; its radical is Q/Z in the first coordinate. The restriction of q to this radical is -r, so q does not descend to the finite quotient.

There are two group-homomorphic sections of the quotient onto Z/2,

    s_0(j)=(0,j),        s_1(j)=(j/2,j).

Their pulled-back quadratic functions are q_+ and q_- respectively. Their Gauss sums have phases1/8 and-1/8. Thus choosing an arbitrary section does not produce a section-independent Gauss phase, even for this single fixed discriminant quadratic function. The standard surgery construction realizes the lattice by the split0-framed and2-framed unknots, giving S¹×S² connected sum RP³ with a non-torsion Spin^c Chern component. A global sign convention for the boundary pairing interchanges the two phases but does not remove their inequality.

This is not a proof that no appropriately defined general invariant exists. It rules out only the naive finite-section prescription and keeps the original problem's domain ambiguity visible. The finite-phase target is unambiguous on torsion-Chern structures, in particular rational homology spheres.

## 5. Remaining target and next route

No construction or impossibility proof for the genuinely new degree-one lift has been obtained. The obstruction in Theorem1 assumes additivity and dependence only on quadratic data; the desired order-one theory can evade the latter. The section example concerns non-torsion Chern classes and does not invalidate the canonical finite phase on the torsion-Chern domain. The known Rochlin non-descent example imposes exact recovery of the spin invariant, which is stronger than merely lifting its mod8 value.

The next substantive route is to formulate the lift problem on the degree-one Spin^c surgery quotient, with an explicit target normalization, and identify whether its extension obstruction can be evaluated without silently adding spin compatibility or discarding non-torsion structures. A second route is a surgery-presentation formula with a proved mod16 change law. Both still require actual topology; the elementary phase branch choice is blocked as a meaningful solution.

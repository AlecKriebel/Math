# Degree multisets are recoverable from any fixed nonempty permutation wreath

Checkpoint24October2026. New candidate general mechanism, under fresh adversarial review. This excludes a family of potential counterexample constructions for21.135; it is not a complete solution or an originality claim. The construction agent first proved the cyclic-prime case by a Dirichlet-polynomial argument. The coordinator developed the support-orbit proof below for transitive actions; coordinator and construction agent independently extended it to the stated nontransitive case.

## Statement

Let P be a fixed finite group acting on a fixed nonempty finite set Omega. The action need not be faithful or transitive. For any finite group X, form the permutation wreath product

    W_P(X)=X^Omega semidirect P.

If finite groups X,Y have identical multisets of irreducible complex character degrees after applying W_P, then X,Y already have identical degree multisets. This conclusion is equality of multisets, not isomorphism of the base groups. It includes the trivial base, a trivial top action, singleton orbits, and a one-point coordinate set. Nonemptiness is essential: for Omega empty, W_P(X)=P is independent of X.

## Ordinary irreducible characters of the wreath product

Write B=X^Omega. Its irreducibles are indexed by tuples R=(rho_i)_(i in Omega) of irreducibles of X. Choose once a representation space for each rho. P permutes the tuple positions. Let P_R be the stabilizer of the tuple, t=[P:P_R], and d_i=rho_i(1).

The tensor representation rho_R of B extends to B semidirect P_R: every stabilizing permutation moves only between factors carrying the same chosen representation space, so canonical permutation of the tensor factors gives an actual linear representation satisfying the group law. There is no projective obstruction here. By Clifford theory (or its direct isotypic-component proof), the irreducibles over the orbit of R are exactly the inductions of these extensions tensored with eta in Irr(P_R). Their degrees are

    t * product_i d_i * eta(1).                    (1)

To see completeness, an irreducible wreath representation restricts to a sum of one P-orbit of B-types. Its isotypic summand for R is the tensor of rho_R with a representation of P_R; the actual extension makes that multiplicity-space representation ordinary. Irreducibility of the whole representation is equivalent to irreducibility of that multiplicity representation. Induction recovers the representation, and distinct orbits or distinct eta give distinct irreducibles. Thus (1) is a bijective parametrization, retaining all multiplicities.

Let c be the number of P-orbits on Omega, m0 their minimum size, and ell_X the number of linear characters of X. Formula(1) gives

    ell_(W_P(X)) = ell_X^c * ell_P.               (2)

Indeed a degree-one constituent requires t=1, all d_i=1, and eta linear; the invariant tuples are precisely constant choices of one linear label on each coordinate orbit. Since c>=1, equality of output multisets determines ell_X from (2).

## A lower bound that controls every omitted label

Suppose a tuple contains a base character of degree e>=2 at a coordinate in orbit Omega_j. Let S be the positions in that orbit whose base degrees are at least e, and put a=|S|>=1. Every element of P_R preserves S, because it preserves the labels, so the t distinct tuple translates determine at most t support translates. Their union is all of Omega_j by transitivity on that orbit. Consequently

    t*a >= |Omega_j| >= m0.

The product in (1) is at least e^a. For every integer e>=2 and a>=1, e^a>=ae: for a=1 this is equality; the elementary bound 2^(a-1)>=a for a>=1 proves the general case. Formula(1) therefore yields

    output degree >= t*e^a >= t*a*e >= m0*e.      (3)

Neither transitivity of the whole P-action nor faithfulness is used. It follows that output characters of degree at most m0*d use only base-character labels of degrees at most d. Label counts above d cannot affect that truncated output multiset.

## Reconstruction by the first different degree

Suppose D(X) differs from D(Y). If their numbers of linear characters differ, equation(2) already distinguishes their wreath multisets. Otherwise let d>=2 be the least degree with different multiplicities. Interchange X,Y if necessary so that X has fewer degree-d characters.

Identify the labels of degrees below d in the two bases, choosing their trivial characters to correspond, and inject the degree-d labels of X into those of Y. These identifications give a P-equivariant injection between tuples using labels of degrees at most d. It preserves equality patterns, stabilizers, tuple products, orbit lengths, and every inertia representation eta. Thus all output irreducibles from the smaller label collection persist in the larger one, with their degrees unchanged. The statement uses only the label dimensions and equality pattern in (1), not equivalence of representations of X with representations of Y.

At least one additional output irreducible has degree exactly m0*d: choose a new degree-d label at just one coordinate of an orbit of size m0 and use the trivial base character at all other coordinates. Its tuple orbit has size m0. Its stabilizer's trivial character has eta(1)=1, giving degree m0*d by (1). This tuple orbit cannot come from the smaller label collection. Therefore the multiplicity of degree m0*d strictly increases when passing from the truncated labels of X to those of Y.

By (3), base labels of degrees greater than d cannot contribute at or below m0*d, so later differences cannot cancel this increase. The full wreath multisets differ, proving the contrapositive. QED.

## Exact scope for construction research

Thus applying the same fixed nonempty finite permutation-wreath functor to two base groups cannot conceal a pre-existing discrepancy in their degree multisets. It cannot manufacture a first counterexample to21.135 from bases whose degrees differ. It does not prove that all groups with a wreath-product degree multiset themselves have a wreath decomposition, does not compare different top groups or actions, and does not reconstruct the group X from D(X).

For a faithful permutation action and nontrivial radical-free X, radical-freeness of X is also preserved: a solvable normal subgroup of W intersects the perfect-product socle or base radical trivially; more directly its intersection with B is contained in R(B)=1, hence it centralizes B, whose centralizer in W is trivial when X is centerless and the action is faithful. Conversely R(X)^Omega is solvable normal if R(X) is nontrivial. The trivial-base and nonfaithful-action cases require separate radical statements and are deliberately not included in that preservation assertion. Injectivity of degree multisets above needs neither of those additional hypotheses.

No complete counterexample or general radical-recognition proof follows. The relevant character theory is standard; any novelty of the elementary recovery argument remains unestablished. No preprint, DOI, tracker row, human peer-review claim, or formal-verification claim is attached.

# Postseal adversarial cross-check
PR788 / problem30001522 / original head3412d5a074c3f3a03f75735a9ccf1755e172204a.

Result: zero blocking mathematical issues in the full theorem or source interpretation. The sealed compact-group packet was kept byte-for-byte unchanged. This is a separate adversarial checkpoint after early independence was frozen and the packet sealed. The peer REPORT.md was read only at this checkpoint; its acceptance label was not treated as evidence.

Completion estimate for this adversarial validation checkpoint: 100%. The supplied program budget remains 2/5, with zero additional substantive proof-search turns. No priority claim or current-open-status conclusion is made.

## 1. Actual W and a finite complex
SU(3)/SO(3) is a closed smooth manifold for the real-matrix closed subgroup, with dimension 8-3=5. A finite smooth triangulation gives a homeomorphism from a finite polyhedron to its actual underlying space. Actions transport along that homeomorphism. Nothing requires them to be simplicial or to preserve one chosen finite triangulation; the primary source imposes no such restriction. There is no replacement by a merely homotopy-equivalent complex.

The bundle sequence gives pi1(W)=0 and pi2(W)=Z/2. Both fundamental-group conditions are consequently automatic. The integral homology groups are Z in degrees0,5 and Z/2 in degree2; H3 HOMOLOGY is zero but H3 COHOMOLOGY is Z/2. The peer keeps this distinction correct. Rational Hurewicz and rational Whitehead apply to the simply connected finite-type spaces involved; a nonzero rational degree-five sphere map is a rational homology equivalence, establishing rational type S5 and finite total rational homotopy. No unknown pi3 inclusion map is needed for the weaker finiteness conclusion.

## 2. A torsion pi2 class really detects tangent w2
A torsion homotopy element can be detected by a characteristic class with F2 coefficients. Specifically, the integral Hurewicz map pi2(W) -> H2(W;Z) is an isomorphism Z/2 -> Z/2; reduction H2(W;Z) -> H2(W;F2) is an isomorphism because H1(W;Z)=0. A generator sphere thus remains nonzero in mod-two homology.

The tangent bundle is associated to the isotropy representation on Sym_0(R3), not merely to the standard three-dimensional SO(3) representation. It splits on a coordinate rotation circle into one fixed line and real rotation planes of weights1 and2. Its pi1(SO3) -> pi1(SO5) map has parity1+2=1. The boundary pi2(W) -> pi1(SO3) is an isomorphism. The pullback tangent bundle on that sphere therefore has the nontrivial SO5 clutching loop and nonzero w2. This identifies w2(W) as the unique nonzero degree-two class independently of the principal-bundle characteristic class. There is no rationalization of this torsion argument and no substitution of w(P) for w(TW).

## 3. Bockstein and the exact characteristic number
For the coefficient sequence 0 -> Z/2 -> Z/4 -> Z/2 -> 0, universal coefficients identify H2(W;Z/4) with Hom(Z/2,Z/4). Every homomorphism sends the torsion generator to0 or2. Mod-two reduction sends both values to0, so H2(W;Z/4) -> H2(W;F2) is zero. Exactness forces its connecting map to be nonzero on the generator x. This connecting map is Sq1, hence Sq1(x)=y is the nonzero degree-three class.

Orientation gives w1=0, and the identity Sq1(w2)=w1w2+w3 gives w3=y. Poincare duality over F2 pairs H2 and H3 nondegenerately. Each has dimension1, so xy is the nonzero top class and <w2w3,[W]>=1. This proof uses tangent w2 throughout. The independently bound primary Debray-Yu body agrees and explicitly distinguishes tangent and principal-bundle classes.

## 4. Arbitrary continuous free even-order actions
For a continuous free C2 action, the group maps are homeomorphisms. A chart U can be chosen disjoint from its translate, giving an evenly covered quotient chart. The quotient is a closed Hausdorff topological five-manifold; smoothness, local linearity, and triangulability of the quotient are unnecessary.

A covering is a local homeomorphism. Pulling back diagonal neighborhoods identifies its topological tangent microbundle with that of W. The mod-two Thom definition of Stiefel-Whitney classes is natural for this pullback. Thus w_i(W)=q*w_i(N) even when no smooth quotient structure is present. The fundamental-class pushforward in F2 homology is q_*[W]=2[N]=0; no orientation assumption on N is needed. All tangent characteristic numbers would vanish, contradicting the nonzero number above.

This excludes free C2, hence every free action whose group contains C2. In particular it excludes positive-rank tori and elementary abelian2-groups. More generally a finite even-order group contains C2 by Cauchy's theorem, so any free action of it is also excluded; that stronger observation is not needed for the stated ranks. The argument never invokes a manifold-quotient theorem for a circle action.

## 5. All primes, all isotropy, and the fixed-space quantifier
For the one fixed embedding D(z)=diag(z,z,z^-2), a fixed coset forces a conjugate into SO3, whose elements have eigenvalue1. Thus any stabilizing z lies in {1,-1}. Every odd finite subgroup intersects this set trivially. At z=-1 there is actually a fixed identity coset, so the circle is only almost free. At primitive cubic roots D(z) is scalar but has no eigenvalue1, which prevents any central-kernel exception.

The same W and embedding precede the prime. This proves a free action for every odd prime, an infinite set, by a congruence argument rather than extrapolation from samples. The exceptional prime2 is the integral obstruction to the torus. The primary Hanke definitions use actual free actions on X; they do not optimize over rational or homotopy replacements or admit finite stabilizers as free toral actions. Its asymptotic homotopy-Euler bound allows the observed gap0<1.

## 6. Arbitrary-action Borel bound, nilpotents, and extensions
For odd p, W has Fp cohomology only in degrees0 and5. An elementary abelian p-group acts trivially on those lines because Fp* has orderp-1. The first-quadrant Serre spectral sequence therefore has just two rows and only d6 can connect them.

For E=(Z/p)^2, put R=Fp[t1,t2] tensor Lambda(s1,s2). R-linearity makes the bottom-row image precisely the principal ideal generated by the degree-six transgression f. The bottom E_infinity row is R/(f). This does not assume f is nonzero, a non-zero-divisor, polynomial, or without exterior terms. Killing the exterior generators gives a surjection
R/(f) -> Fp[t1,t2]/(f_bar).
If f_bar=0, this is the full polynomial ring. Otherwise f_bar is a nonzero homogeneous binary cubic; multiplication by it injects degree m-3 into degree m, leaving dimension3 for each m>=3. Thus both possibilities retain classes in arbitrarily high degrees. The possible nilpotent/exterior components of f cannot reverse this quotient argument.

No differential after d6 can alter the bottom row because no fiber row exists above5. The first-quadrant, two-row spectral sequence has finite filtration in each total degree, so the nonzero associated-graded classes represent nonzero total cohomology. Additive or multiplicative extensions cannot erase a nonzero graded piece.

A free finite action makes the quotient a compact topological5-manifold by covering charts. The Borel construction is homotopy equivalent to it via the associated contractible-fiber bundle, so cohomology vanishes above5. This contradicts the surviving bottom row. Every rank>=2 action restricts to a rank-two subgroup, proving the exact upper bound1 for arbitrary continuous actions, without assuming they are homogeneous.

## 7. Peer-specific wording and precise disposition
Every requested mathematical edge case passes. No repair of the theorem is required. The peer's supplemental Gysin route remains conditional and unnecessary; its local-section/ANR hypotheses are not smuggled into the finite-cover proof.

One nonblocking bibliographic wording distinction is worth preserving: the report body is Report32/2010, while publisher metadata records online publication in2011. Therefore a catalog's parenthetical2011 need not by itself be a mathematical-source mismatch. The peer labels this a bibliographic-year mismatch; that label does not affect definitions, hypotheses, or this verdict. No priority investigation was performed here.

INPUT_BINDINGS.json pins the exact peer report, original author proof, primary bodies, and sealed compact-group packet. CHECK.py validates these bytes and reruns the previously sealed checker after verifying its input binding. The new checkpoint contains no third-party full body and changes no sealed packet or source input.

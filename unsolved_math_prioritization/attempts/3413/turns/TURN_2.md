# Turn 2: the free ambient action case and a linking obstruction

**Unreviewed scoped partial. The original full hyperbolic-link realization question remains unresolved, 2/5.**

The distinction throughout is between a cyclic group acting freely on all of S3 and a generator that merely has no fixed points. All nonidentity elements must have no fixed points for the former condition. We do not assume the original source group acts freely. No novelty is claimed for these consequences of covering spaces and the classical torsion linking pairing.

## 1. Linking of two invariant circles under a free cyclic action

**Lemma 2.1.** Suppose a cyclic group H of order k>1 acts smoothly, freely and orientation preservingly on S3. If two disjoint embedded circles K and J are each preserved setwise by all of H, then their ordinary integral linking number satisfies

    gcd(lk(K,J),k)=1.                                           (2.1)

In particular it cannot be zero. The circles need not be unknotted.

Proof. Let p:S3->M=S3/H be the oriented k-sheeted covering. Its quotient is a closed oriented three-manifold with pi_1(M)=H=C_k, because S3 is the universal cover. Consequently H_1(M;Z)=C_k and M is a rational homology sphere (Poincare duality gives its rational H_2=0).

The action on each circle preserves its orientation: an orientation-reversing self-homeomorphism of a circle has a fixed point, impossible for a nonidentity element of a free action. The quotient circles barK and barJ are embedded. Each has connected full preimage. Covering-space monodromy therefore maps its fundamental group onto H. Since pi_1(M) is already abelian cyclic, their homology classes are generators of H_1(M), say a z and b z, with a,b units modulo k.

The torsion linking pairing lambda_M on H_1(M) is nonsingular. This classical fact is given with its Bockstein/Poincare-duality proof in Massuyeau, Section5.2, Lemma5.7; no lens-space classification or linearization theorem is needed. Bilinearity writes lambda_M(z,z)=c/k modulo Z. Nonsingularity forces gcd(c,k)=1: the homomorphism lambda_M(z,-) must have order k. Thus lambda_M([barK],[barJ])=abc/k modulo Z, with abc a unit modulo k.

We check the covering normalization explicitly. Choose an integral singular two-chain C in M with boundary k barK, in general position relative to barJ. Let transfer(C) be the sum of all its simplex lifts. Since transfer(barK)=K with the compatible orientation, its boundary is k K. Each transverse intersection of C with barJ has exactly k lifts on J, of the same sign, so

    transfer(C) . J = k (C . barJ).

In S3 this also equals k lk(K,J). It follows that lk(K,J)=C . barJ and therefore

    lk(K,J)/k = lambda_M([barK],[barJ]) modulo Z.

Hence lk(K,J)=abc modulo k, proving (2.1). Reversing either orientation changes signs but not the coprimality. QED.

This is a linking-number obstruction, not an assertion that pairwise vanishing linking numbers characterize an unlink.

## 2. Classification at the intermediate ambient-unlink level

**Theorem 2.2.** Let m>1. Suppose C_m acts freely and orientation preservingly on S3 and preserves an n-component unlink U. The induced signed component permutation consists of:

- any number a>=0 of positive cycles of length m; and
- at most one positive cycle of length1.

Thus n=am+epsilon with epsilon in{0,1}. Conversely, every such signed cycle multiset occurs for some smooth free orientation-preserving C_m action preserving an unlink.

This is a complete classification only for this intermediate problem. It does not classify the original hyperbolic links or their full symmetry groups.

Proof of necessity. For a component orbit of length d dividing m, its stabilizer is H=<g^d> of order m/d. A negative cycle would mean g^d reverses the component, hence has a fixed point on it, contradicting freeness. Thus every cycle sign is positive.

If 1<d<m, H is nontrivial and itself acts freely on S3. Because the full group is abelian, H preserves every component of that orbit. Choose two of them. Lemma2.1 forces their linking number to be nonzero, whereas two components of an unlink have linking number zero. This excludes every intermediate d. If there are two distinct singleton orbits, apply the same lemma with H=C_m to these two components, again obtaining a contradiction. The only remaining lengths are m and at most one1. QED.

Proof of converse. Write S3 as the unit sphere in C². The scalar action

    g(z,w)=(zeta z,zeta w),  zeta=exp(2 pi i/m),

is orientation preserving and free: for 0<j<m, zeta^j is not1 and no nonzero vector is fixed. The circle K={w=0} is invariant, unknotted, and positively rotated. Include it if epsilon=1.

To add a full orbit of unlink components, choose a small ball B whose m translates are disjoint, and put a small round circle with a spanning disk inside B. Include its m images. Each lies in its own ball and bounds the corresponding image disk. This gives a positive length-m cycle because g^m is the identity. Choose as many distinct free ball orbits as the prescribed finite number a requires.

When K is included, first choose an embedded spanning disk D for K. First choose a points in distinct group orbits outside the finite union of all translates of D. This finite union of surfaces has empty interior, so finitely many previously chosen points and their translates cannot exhaust its complement. The total collection of orbit points is finite and disjoint from D and K. Then choose balls small enough that all their translates are mutually disjoint and avoid D and K. The disks inside these balls, together with D, are then mutually disjoint spanning disks for all components. This proves the unlink property, not just pairwise linking zero. The component cycle data are exactly the requested multiset. QED.

Boundary cases: the empty unlink is allowed in this intermediate statement; a=0,epsilon=1 has a trivial signed representation despite a nontrivial free ambient action. Thus ambient faithfulness is not signed-action faithfulness. For m=1 the condition would be different: every component can be fixed, with no restriction to one. That case is explicitly excluded here.

## 3. A computable conditional filter for the source representations

For any proposed source representation rho:C_m->B_n and any subgroup C_k known independently to act freely on S3, restrict rho to that subgroup. Theorem2.2 applies: its signed cycle multiset must have only positive k-cycles and at most one positive singleton.

This restriction can be calculated without choosing coordinates. Put q=m/k. A signed g-cycle of length d and sign epsilon breaks under g^q into h=gcd(d,q) cycles. Each has length d/h and sign epsilon^(q/h). This follows by traversing d/h steps: the original cycle is traversed q/h full times. This formula also handles negative original cycles whose signs become positive on a subgroup.

The condition is conditional on the actual ambient subgroup being free. The signed permutation by itself does not prove that hypothesis. In particular:

- If the whole source action is free, C6 with a positive2-cycle is excluded even though it is an abstract homomorphism. C6 with a positive2-cycle and a positive3-cycle is faithful but also excluded from the free-action case.
- Two positive singleton components under any C_m,m>1 cannot belong to the free-action case. They may still belong to a nonfree ambient action.
- A source action with a negative cycle is automatically outside the free-action case by Turn1's reversal lemma. This is consistent with the Borromean and Whitehead examples; they are not counterexamples to Theorem2.2.

## 4. Explicit controls against overextending the hypothesis

**A fixed-point-free generator does not suffice.** On S3 in C², let

    g(z,w)=(i z,-w).

Its order is4 and it has no fixed point. But g²(z,w)=(-z,w) fixes the circle z=0. Thus the C4 action is not free. Applying the free-action linking lemma merely because g has no fixed point would be invalid. The exact matrix control records these fixed-space dimensions.

**Several positive singletons are possible for a nonfree action.** Rotate R³ by angle2pi/m about its vertical axis and extend over the point at infinity to S3. The horizontal round circles of radius1 in planes z=0 and z=3 are both invariant, with positive orientations. Their planar spanning disks are disjoint, so they form an unlink. The ambient action has the vertical axis plus infinity as its fixed circle. This realizes two positive singleton cycles at the ambient-unlink level and shows exactly why Theorem2.2 is not an unconditional restriction on the original source representations.

Neither control constructs a hyperbolic source link or asserts that the exhibited cyclic group is the full source group.

## 5. Classical inputs, failed transfer and exact remaining gap

The only new external theorem used in this turn is the classical nonsingularity of the torsion linking pairing, checked in Gwenael Massuyeau, *An introduction to the abelian Reidemeister torsion of three-dimensional manifolds*, arXiv1003.2517v1, Section5.2, equation(5.3) and Lemma5.7, printed29–30:
https://webhomes.maths.ed.ac.uk/~v1ranick/papers/massu.pdf
The normalization and consequences above are proved here. These are credited consequences of classical topology, not a historical novelty claim.

A separate lead was checked in Luisa Paoluzzi, *Three Covers Determine Hyperbolic Knots*, JKTR14(2005),641–655, Claim2.1, printed643:
https://www.i2m.univ-amu.fr/perso/luisa.paoluzzi/jktr05.pdf
It concerns periodic symmetries of an invariant unknot, their common axis and a Hopf-link conclusion. Its word “periodic” explicitly requires a nonempty fixed set disjoint from that knot. It cannot be used to replace the free-action analysis or to declare every cyclic action free. No additional conclusion from that lead is asserted in this turn.

The source action may have fixed-point subgroups, and this turn does not classify all their possible invariant unlink patterns. More importantly, the constructive converse in Theorem2.2 supplies an ambient action and an unlink only. It does not add a distinguished component L0 so that the complement is hyperbolic, does not prove the precise prescribed full orientation-preserving/oriented-L0 symmetry group, and does not eliminate accidental additional symmetries. Declaring generic asymmetric decorations would leave all three tasks unproved and might destroy either the unlink condition or the desired cyclic action. This transfer is not accepted as a solution.

Next research must address the nonfree cyclic strata and actual hyperbolic exact-symmetry constructions. Original unresolved2/5; estimated completion25%. The finite controls validate the modular-linking algebra, cycle restrictions and calibration matrices; the covering and construction arguments above are the proofs.

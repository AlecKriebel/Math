# Turn 5: complete ambient classification and the unclosed hyperbolic gap

**Unreviewed partial. Five substantive author turns are exhausted. The original problem is unsolved5/5.**

The principal partial result in this final turn is a characterization of signed representations realized by a faithful smooth orientation-preserving cyclic action on S3 preserving an unlink. It is necessary for the source problem and has explicit ambient constructions. It still does not characterize which of those models admit a single distinguished hyperbolic completion with precisely the prescribed full source group. No novelty is claimed; the geometric inputs are classical and are credited below.

## 1. An equivariant disk forces equality of the orbit and axis orders

We use the fixed-boundary equivariant Dehn lemma of Meeks–Yau, also proved topologically by Edmonds1986, Theorem on printed606. In the form needed here: a simple closed curve Gamma in the boundary of a three-manifold, null-homotopic in the manifold, whose translates are equal or disjoint and which is transverse to the exceptional set of a finite group action, bounds an embedded disk D whose translates are equal or disjoint. There is no irreducibility hypothesis. For a smooth action one can use the smooth version with an invariant mean-convex metric, or pass to a compatible equivariant triangulation and use Edmonds's PL version. A finite smooth action admits such a triangulation, also used in Paoluzzi–Porti's equivariant construction. No hyperbolization theorem is part of this input.

**Theorem5.1.** Suppose G=C_m acts faithfully and orientation preservingly on S3 and preserves an unlink. Let a positive component orbit have length 1<d<m. Then its stabilizer H=<g^d> is the full pointwise stabilizer P_A of one of the fixed axes A. Equivalently,

    d = order(g on A) = m/|P_A|.                                (5.1)

Proof. Turn3 Corollary3.2 already shows that H fixes an axis A pointwise. Let K be a component of the orbit. The periodic group H acts faithfully and positively on K, with axis A disjoint from K, and K union A is a Hopf link. The equivariant disk fibration of the unknot exterior used in Paoluzzi's Claim2.1 provides an H-invariant preferred longitude Gamma on an H-invariant small boundary torus T_K. Indeed the generator of H fixes each disk fiber, so fixes its boundary circle setwise. Choose its tubular neighborhood small enough to miss A and all other unlink components, and propagate this choice around the component orbit to make it G-invariant. This gives one longitude on each of its distinct boundary tori; translates of Gamma are equal exactly for H and otherwise disjoint.

Let E be the full unlink exterior with all tubular neighborhoods removed. Because the whole link is an unlink, the preferred longitude Gamma is null-homotopic in E, not merely in the exterior of K alone. It is disjoint from the exceptional set of G. To verify this last condition, any element fixing a point of T_K must preserve T_K and K, hence belong to H. Every nonidentity element of H has fixed set A, which misses T_K. Thus the fixed-boundary equivariant Dehn lemma applies in E.

Obtain an embedded equivariant disk D bounded by Gamma. Its setwise stabilizer is precisely H: membership in H preserves its boundary and therefore, by equivariance, preserves D; equality of another translate would force equality of their boundary tori and hence membership in H. The generator of H acts on this disk, so Brouwer's fixed point theorem gives a point p in D fixed by it. Such a point lies on A.

Write e=order(g on A). Since g^d fixes A, e divides d. The element g^e fixes p, so D and g^e D intersect. Equivariance forces equality; consequently g^e belongs to H and d divides e. Thus d=e and |H|=|P_A|. QED.

The boundary-curve hypothesis is indispensable. We did not assume every invariant unknot has an invariant spanning disk under an arbitrary free action. Here the preferred longitude was explicitly made invariant under the purely periodic stabilizer, using the classical equivariant fibration. Without that step a free action can permute parallel longitude curves on the same boundary torus, and the argument would not apply.

## 2. Exact ambient classification: statement

Start with a multiset of signed cycles(d,epsilon) for a homomorphism rho:C_m->B_n. Retain the actual domain order m. The abstract homomorphism condition is d|m for positive cycles and2d|m for negative ones. Let c1 be the number of positive singleton cycles, and D the set of distinct positive lengths strictly between1 and m. Multiplicities at allowed lengths are arbitrary unless stated otherwise.

**Theorem5.2 (ambient-unlink characterization).** Subject to the abstract homomorphism condition, rho is induced by some faithful smooth orientation-preserving C_m action on S3 preserving an n-component unlink if and only if the following rules hold.

### A. No negative cycles

For m=1, the representation is the identity on every component, with arbitrary n.

For m>1:

- If c1>=2, D is empty.
- If c1=1, D contains at most one length.
- If c1=0, D contains at most two lengths. When there are two distinct lengths d1,d2, their stabilizer orders are coprime:

       gcd(m/d1,m/d2)=1.                                      (5.2)

Positive cycles of length m are unrestricted in all cases.

### B. At least one negative cycle

The order m must be even. Every negative cycle has length d=m/2.

For m=2, arbitrary numbers of negative singletons, positive singletons and positive2-cycles are allowed.

For m>2:

- c1 is either0 or1.
- If c1=1, the only other positive lengths are d and m.
- If c1=0, in addition to d and m there is at most one distinct positive length e. If present, it must satisfy

       m/e is an odd divisor of m greater than1.                (5.3)

In particular distinct odd stabilizer orders cannot coexist in this signed/no-singleton case.

This theorem classifies ambient cyclic actions on unlinks. It is not a claim that every listed representation is already realized as the full source group of a hyperbolic KGL.

## 3. Necessity of the classification

Turn3 showed that there are at most two distinct fixed axes for G, with coprime orders of their full pointwise stabilizers. Theorem5.1 assigns every positive nonsingleton proper orbit to exactly one such axis, with its length determining that axis's full stabilizer order.

In the unsigned case with c1=0, this immediately gives at most two proper lengths and the coprimality condition(5.2). With c1>=2, Turn3 Lemma3.1 makes all of G fix one axis pointwise. There is no second axis, and Theorem5.1 would give length1 for any orbit assigned to it, so no proper nonsingleton orbit can occur.

Suppose c1=1 and two different proper lengths occurred. They supply two axes A and B. Let U be the positive singleton. If U is neither axis, the elements fixing A and B are periodic symmetries of U with two distinct axes, contradicting Paoluzzi's common-axis theorem. If U=A, a component from the orbit assigned to A is periodically invariant about U and forms a Hopf link with it, contradicting the unlink condition. The case U=B is the same. Hence at most one proper length occurs.

For the signed case, Turn1 gives all negative lengths m/2. Turn3 identifies the negative involution axis A with |P_A|=2. For m>2 it permits at most one positive singleton, and its Theorem3.4 already gives the c1=1 case. If c1=0, Theorem5.1 allows positive proper orbits on A only at length m/2. There is at most one other axis B, with |P_B| odd by coprimality; all its positive proper orbits have the single length e=m/|P_B|. This proves(5.3) and the uniqueness of e. The m=2 case has no further cycle lengths allowed even algebraically.

For example, C18 with a negative9-cycle, a positive6-cycle and a positive2-cycle is excluded: the two odd stabilizer orders3 and9 cannot both be the full pointwise stabilizer of the other axis. This passes the weaker Turn3 parity test. In the unsigned case, C12 with positive3- and6-cycles is excluded because the stabilizer orders4 and2 are not coprime. C6 with positive2-,3- and1-cycles is excluded because the positive singleton cannot coexist with both proper lengths.

## 4. Explicit smooth constructions for all admitted patterns

The following construction proves sufficiency and the unlink property, not just vanishing pairwise linking numbers. Write zeta=exp(2pi i/m). For coprime divisors k,l of m, the diagonal action

    g(z,w)=(zeta^l z,zeta^k w) on S3 subset C²                 (5.4)

has order m. The coordinate circles A={z=0}, B={w=0} have pointwise stabilizers of orders k,l respectively, where an order1 stabilizer means no nontrivial fixed-axis subgroup. Their point orbits have lengths m/k,m/l. Points off both axes have trivial stabilizer.

Choose finitely many distinct point orbits on either axis and disjoint small metric-ball orbits around them. In the normal two-plane to an axis, a small circle bounds a disk and is preserved positively by the axis stabilizer. Its ball orbit therefore gives a positive cycle of the corresponding length. If the stabilizer order is2, a circle in a plane spanned by one tangent-axis direction and one normal direction is instead reversed by that involution; its translates give a negative m/2-cycle. This is the local model from Turn3. Any desired positive m-cycles are obtained in disjoint ball orbits about free points. Every component so obtained bounds a disk in its own ball.

One may also include one of the coordinate circles as a positive singleton. Its spanning disk must then be kept disjoint from every ball and every component disk. Balls centered on that same axis cannot be used: a positive local meridian would link the included circle, and a negative local circle would intersect it. Balls on the other axis are possible. A spanning disk of one Hopf coordinate circle meets the other axis in one point; avoid the finite orbit of these intersection points and choose all balls small enough. Free ball centers avoid the finite union of disk translates. The chosen disks and the coordinate-circle disk are then mutually disjoint. Both coordinate circles cannot be included because they are a Hopf link.

Apply this template as follows.

### Unsigned patterns

- With c1=0 and two proper lengths, take k=m/d1,l=m/d2. Condition(5.2) makes(5.4) faithful. Use normal circles in the two kinds of ball orbits and arbitrary free ball orbits. With one proper length use its k and l=1. With none use k=l=1.
- With c1=1 and one proper length d, take k=m/d,l=1, include B and use normal circles about A, plus free ball orbits. With no proper length use the free scalar action k=l=1 and include either coordinate circle.
- With c1>=2 and no proper length, take k=m,l=1, so G fixes A pointwise. Use exactly c1 normal circles in disjoint balls about distinct points of A, and the requested free ball orbits. No coordinate circle need be added.
- For m=1 take any ordinary unlink and the trivial action.

### Signed patterns

- If m>2 and c1=0, choose k=2. If an extra proper positive length e occurs, set l=m/e, an odd divisor by(5.3); otherwise set l=1. Around A use the requested negative and positive m/2-cycles, around B use the positive e-cycles, and elsewhere the positive m-cycles. Do not include a coordinate circle.
- If m>2 and c1=1, use k=2,l=1 and include B. This is exactly the construction of Turn3 Theorem3.5.
- If m=2, use k=2,l=1. Balls about distinct points of A give arbitrary negative or positive singleton circles, and free ball orbits give positive2-cycles.

All actions and circles are smooth. Exact orders, signs and component counts follow from the displayed stabilizers. Mutually disjoint spanning disks prove the constructed links are unlinks. This establishes the intermediate characterization.

## 5. What the hyperbolic construction attempt does and does not prove

The free-quotient connected completion in Turn4 is proved. For the remaining nonfree cases, let E_reg be the unlink exterior with the nontrivial fixed sets removed. It is connected, and E_reg->E_reg/G is a connected regular cover. Consequently a loop with generator monodromy exists in the regular quotient and can be represented by an embedded knot. Its full lift is a connected invariant circle. This handles connectedness and orientation, but says nothing about hyperbolicity.

One can insert backtracking detours to make such a loop cross proposed regular fundamental-domain faces repeatedly, retaining its generator monodromy. Local homotopies of the resulting arc tangles relative to their endpoints keep the circle connected and preserve the fixed unlink. Myers's theorem can make an individual tangle exterior excellent when its own boundary hypotheses hold. The unresolved step is the global decomposition near fixed strata and the incompressibility of every gluing subsurface and its complementary boundary subsurface. Counting punctures gives Euler characteristic information, not that missing incompressibility assertion. Faces of an equivariant triangulation also meet along edges; they cannot simply be treated as an already disjoint family of proper gluing surfaces. Those issues prevent the attempted general equivariant one-component construction from closing.

For precision, the following conditional certificate is valid directly by Myers's gluing lemma. Suppose an actual connected invariant regular circle J has been supplied, and its exterior X=E\N(J) has a decomposition along a finite, pairwise disjoint, two-sided proper surface system F such that:

1. every component of the cut-open X is excellent;
2. the two copies of F and the closure of their complementary boundary are incompressible in every cut-open component;
3. every component of F has negative Euler characteristic.

Then Myers Lemma2.1 makes X excellent. Its torus-boundary hyperbolization gives a hyperbolic completion with the original unlink unchanged. If the signed representation satisfies Turn4's exact-group test with no admissible index q>1, the full source group is then exactly the prescribed C_m. In particular this last conclusion holds with one negative cycle.

This is a sufficient, checkable gluing certificate, not a proof that such a certificate exists for every ambient model. Neither the source nor the present work supplies those data in general. No assertion that arbitrary local decorations suppress extra symmetries or imply the gluing hypotheses is made.

## 6. Final disposition and source provenance

The five-turn partial package establishes necessary source restrictions, the complete intermediate ambient-unlink characterization above, a classical free-action connected hyperbolic completion with subgroup inclusion, and a finite exact-group rigidity criterion when negative cycles occur. It does not close the original classification: the nonfree one-component hyperbolic completion is unproved, and extra source symmetries can remain in the unsigned free-completion theorem or in signed cases passing the extension test. The status is **unsolved5/5**, not claimed_solved. Estimated completion50%, purely heuristic.

The fixed-boundary Dehn lemma and its surrounding hypotheses were checked in the author-uploaded full-text rendering of Allan Edmonds, *A topological proof of the equivariant Dehn lemma*, Trans.AMS297(1986),605–615, theorem on606, DOI10.1090/S0002-9947-1986-0854087-X. Its hypothesis that the boundary curve be transverse to the exceptional set was explicitly checked above by disjointness. The original Meeks–Yau PDF and the publisher PDF download were not available through the attempted readers; no full-PDF inspection is claimed for those files. The primary author's public full text was available here:
https://www.researchgate.net/publication/265109397_A_topological_proof_of_the_equivariant_Dehn_lemma
The PL/smooth distinction and equivariant-triangulation alternative are stated explicitly in Section1. The other classical inputs and their full cached primary PDFs are recorded in Turns1–4 and source_manifest.json.

All mathematical research stops after this fifth substantive turn. Independent review may validate or require corrections to these scoped claims; it must not be counted as fresh author search for the unresolved original target. The final review request must especially attack the preferred-longitude construction, all Dehn-lemma hypotheses, the distinction between subgroup and full-group realization, and every case of the ambient classification.

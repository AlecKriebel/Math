# Independent classification theorem for the candidate key

This deduction was developed before consulting the candidate's historical review. It is conditional only on the separate claims that the input's canonical APS surface/dual dissection has been correctly constructed and that the displayed winding numbers are correct. No conclusion about those algorithmic claims is asserted here.

## Scope and accepted existing inputs

Fix a field k. Let A=kQ/I be a nonzero, finite-dimensional gentle algebra, with I specified by quadratic monomial generators. Ordinary, ungraded gentle algebras are intended. No finite-global-dimension or algebraically closed field hypothesis is imposed: APS §2 works over a base field k, and APS4.3/6.1 explicitly treats the finite-dimensional class characterized by Pwhite=empty. Characteristic two does not affect the topological Z2 quadratic form.

Use APS4.3 for the canonical marked oriented surface and APS6.1/7.2 for the equivalence between derived equivalence and an orientation-preserving marked-surface homeomorphism carrying the line field up to homotopy. These are existing classification inputs. For the numerical orbit criterion use **LP Theorem1.2.4 in its full all-boundary form**, rather than the printed puncture-truncated ranges in APS7.3/7.4. LP's topology theorem concerns arbitrary line fields, so the different dissection used to construct the LP algebraic line field (APS Remark3.17) is irrelevant to this application. We do not invoke LP's algebraic Fukaya/graded smoothness criterion.

The exact primary PDFs used are recorded in sources/acquisition_manifest.json and evidence/render_primary_01. APS is the publisher's final 36-page Selecta29:30 PDF, SHA256 42a3956f82fa7098dd37941c2d1bc5a767ad2a46afd6b3bb2b069c10db0c56f1. Original OWR printed161–164, APS full §§3,6,7, and LP full §§1.1–1.2 including proof have been read. APS pp.6,12,13,19,23,24,25,26,27 and OWR163 were also visually inspected.

## Exact key

For one connected component let g be genus, b>=1 the number of original boundary circles, p the number of black punctures, and d=b+p. A finite-dimensional nonzero component cannot have b=0: APS3.7 requires both puncture colors to be nonempty if the boundary is empty, contradicting Pwhite=empty.

For each end c let n(c) be its number of white boundary marks if original, and zero if a puncture. Original boundary circles have n(c)>=1, by alternation and nonemptiness. Orient each c with the remaining surface on the right; its corresponding removed disk, boundary, or puncture lies on the left. Set

    R = multiset of paired records (n(c),w(c)), over all d ends.

Let G=(a1,b1,...,ag,bg) be a geometric handle system; its images in the closed surface obtained by filling all ends form a symplectic integral homology basis. Define H by

    g=0: empty;
    g=1: gcd(w(a1),w(b1), {w(c)+2:c peripheral}), chosen >=0;
    g>=2: ODD if some winding on G union B is odd;
          EVEN_RADICAL_NONZERO if all are even and some peripheral w(c)=0 mod4;
          EVEN_ARF(A) otherwise, A=sum_i (w(ai)/2+1)(w(bi)/2+1) mod2.

The connected key is K=(g,b,p,R,H), with total marks optionally retained as the redundant quantity 2 sum_c n(c). For disconnected inputs take the multiset of connected keys. Curve encodings and raw basis winding values are certificates and are excluded from K.

## Peripheral data and marked permutations

If K(A)=K(A'), a multiset equality yields one bijection of end components matching both n and w. It cannot send an original boundary to a puncture because the former has n>=1 and the latter n=0. Thus it separately matches the b original boundaries and p punctures, including arbitrary allowed puncture permutations. Given matched circles and equal positive white counts, alternating white/black cyclic mark configurations are related by an orientation-preserving boundary diffeomorphism. Such boundary diffeomorphisms extend to collars; the classification of oriented surfaces gives an orientation-preserving marked-surface diffeomorphism between the components with the prescribed end matching. The matching uses **paired** records, not separate sorted lists of counts and windings.

Necessity is immediate from APS6.1: its homeomorphism preserves genus, end type, marked counts, and winding of each oriented peripheral simple curve. In particular every puncture winding is necessary. Consequently extra puncture records cannot distinguish derived-equivalent inputs. Redundant b,p,total-mark data also cannot introduce spurious distinctions.

## Compact-core reduction and sufficiency without the false printed range

Remove pairwise disjoint sufficiently small puncture disks and take collars of the original boundary. The resulting compact core S0 has genus g and exactly d boundary circles. Its interior is homotopy equivalent to the original punctured open surface, with corresponding tangent bundles identified on the core. A puncture end is a cylinder; restriction and extension along collars give a bijection on homotopy classes of line-field sections. Thus one may apply LP's theorem to S0.

First choose the marked diffeomorphism Phi between the two surfaces implementing R's paired end matching. Compare eta on S0 with Phi^*(eta') on that same core. All d peripheral windings coincide. LP Theorem1.2.4 then says that equality of H is exactly the additional condition for these line fields to lie in the orbit of the mapping class group fixing **every core boundary pointwise**. Such a representative extends by the identity down each puncture cylinder and on original collars. It preserves all original marks and all puncture labels after the initial allowed permutation. Composing it with Phi gives the homeomorphism required by APS6.1/7.2. Therefore K equality is sufficient for derived equivalence.

This proof also establishes the necessity and basis independence of H, because the numerical quantities in LP's theorem are intrinsic mapping-class invariants. It proves the candidate key independently of the erroneous truncated statements, rather than silently changing their printed quantifiers.

## Sign conversion between APS and LP

For the same oriented immersed curve and same line field, APS Definition3.2 computes the projective-fiber degree of the line field relative to the tangent, while LP Definition1.1.3 computes tangent degree relative to the line field. Hence w_LP(gamma)=-w_APS(gamma). This can be checked directly with a constant line field on the plane: a counterclockwise circle has tangent degree2, LP winding2, and APS winding-2.

LP uses the ordinary boundary orientation (surface on the left); APS peripheral curves here use the surface on the right. Their peripheral curve orientations are opposite, so the two sign changes cancel:

    w_LP(boundary in LP orientation)=w_APS(c in APS orientation).

Handle values negate, which does not affect gcd or oddness. For even handle values, (-w/2+1)=(w/2+1) mod2, so the Arf formula also agrees. All peripheral w+2 corrections are unchanged. APS Remark3.3(3), Proposition3.20(1),(5), and LP1.1.3/1.3 confirm these conventions. The candidate's orientation agrees with APS. Reversing peripheral curves without changing the convention would instead replace w+2 by -w+2 and is not harmless; for example d=1,g=1 requires w(c)=-2, making the correct correction zero.

## Genus-one gcd and geometric basis independence

LP equation(1.6) and the following characterization identify

    D = gcd{w(gamma): gamma a nonseparating simple closed curve}.

This intrinsic ideal generator is the same for every handle system and is preserved by all marked orientation-preserving homeomorphisms. It includes all d correction terms, including punctures. APS p.26 also credits this characterization to Kawazumi.

The correction can be seen locally: if alpha and a peripheral c are band-summed to a nonseparating alpha', the intervening pair of pants has oriented boundary alpha,c,-alpha'. APS3.20(5) gives w(alpha)+w(c)-w(alpha')=-2, so

    w(alpha')=w(alpha)+w(c)+2.

Unimodular handle moves give the usual shears and sign/interchange operations on the rank-two winding pair; peripheral detours add integer multiples of w(c)+2. The ideal generated by the handle values together with all corrections is unchanged under these invertible moves. Do not treat winding as a homology-linear integer functional: the +2 is exactly the obstruction. The source's intrinsic characterization supplies the full independence theorem without assuming every raw handle change is linear.

For d=1, APS3.20(5) forces w(c)=-2 when g=1, so its correction is zero. Gcd of all zero entries is legitimately zero, as LP states its range Z>=0. For d>=2, omitting corrections fails even at the elementary level: values (6,12), corrections(4,-4) give D=2, while handle-only gcd=6; adding the first peripheral to a gives a'=10 and handle-only gcd=2.

## Parity, spin condition, radical, and Arf independence

APS3.4(4) makes winding modulo2 a linear functional on H1(S0;F2). G together with peripheral classes spans this group (rank2g+d-1), so an odd value occurs among G union B exactly when the functional is nonzero. By APS3.4(3), its vanishing is exactly the condition for the line field to lift to a nonvanishing vector field. This establishes the global meaning and basis independence of the ODD branch.

In the even case APS7.5 gives the quadratic refinement

    q([gamma]) = w(gamma)/2 + 1 mod2,
    q(x+y)=q(x)+q(y)+(x,y).

The radical of the intersection form on H1(S0;F2) is generated by the d peripheral classes, with their single sum relation; filling all ends quotients by this radical. On a peripheral class,

    q(c)=0 iff w(c)=2 mod4.

Since all w are even, the only alternatives are2 mod4 and0 mod4. Therefore the EVEN_RADICAL_NONZERO branch is exactly the case where q does not descend to the closed surface. In this case a handle-only Arf sum need not be independent of the lift: replacing a handle class a by a+r for radical r gives q(a+r)=q(a)+q(r); if q(r)=1 and q(b)=1, the term q(a)q(b) flips. The candidate correctly omits Arf here. LP1.2.4(iii) says no additional invariant is needed after peripheral values and parity are fixed in this branch.

If every peripheral w=2 mod4, q vanishes on the radical and descends to the nondegenerate symplectic space of the closed surface. The formula sum q(ai)q(bi) is then the Arf invariant and is independent of symplectic basis, including handle lifts changed by peripheral classes. One checkable proof uses the number N0 of zeros of q:

    N0 = 2^(2g-1) + (-1)^Arf(q) 2^(g-1).

The formula follows by multiplying the two-dimensional character sums for the g hyperbolic pairs; the sum over one pair is2*(-1)^(q(a)q(b)). N0 is basis independent, so the Arf bit is basis independent. The basis curve orientation is irrelevant: for even w, (-w/2+1)=(w/2+1) mod2. LP1.2.5 explains this branch as extension of the induced spin structure across every capped end.

No additional characteristic assumption enters: this quadratic refinement is over F2 regardless of the algebra's base field. There is no unrestricted integer-linear substitute for it.

## Disconnected-factor necessity and sufficiency

A bound-quiver component determines a block: for a connected quiver, a central idempotent maps in A/rad(A) to a choice of0 or1 at each vertex. Commuting with every arrow forces adjacent vertex choices equal; connectedness makes them all equal. An idempotent in the nilpotent radical is zero, so no further block exists.

At the category level, D^b(A1 x ... x Ar) is the product of the D^b(Ai), and each connected factor is intrinsically indecomposable as a triangulated category. To see this, in an orthogonal product decomposition each indecomposable vertex projective must lie in one factor. Nonzero maps between adjacent vertex projectives force them into the same factor; connectedness puts all vertex projectives there. Any object of another factor has Hom(P_v,X[n])=0 for all vertices and n, hence has zero cohomology and is zero. This argument works even when the algebra has infinite global dimension, because projectives detect cohomology without needing to generate D^b by finite cones.

Consequently an equivalence permutes connected derived factors; the multiset of connected K's is necessary and sufficient. This is a precise replacement for the candidate's brief phrase about primitive central idempotents of the category.

## Isolated and empty cases

For A=k, the canonical model is a disk with two white and two black boundary marks, one white dissection arc, no punctures, and g=0. APS3.12 gives |Delta|=2+0+1-2=1. APS3.20(5) gives w(boundary)=2, and its AG pair is(2,0). Thus K=(0,1,0,{(2,2)},empty) is consistent with the field block. Products of such blocks are covered by the factor proof.

The candidate explicitly permits rejection of the empty quiver as outside its nonzero source class. If its opening claim is read as all finite gentle bound quivers including the zero algebra, that needs one scope clarification or the trivial empty-multiset output. It is not a classification obstruction. The source problem does not insist on the zero algebra case.

## Strongest conclusion and exact limitation

**Verified conditional theorem:** The candidate's connected key with all paired peripheral records and its listed genus branches is a complete derived-equivalence invariant for nonzero finite-dimensional gentle algebras over the fixed source field. The component multiset extends it correctly to nonzero disconnected inputs. It is independent of the geometric handle basis and cannot acquire spurious distinctions from puncture winding records.

**Mandatory proof/source correction:** TURN_1.md's statement that equality implies the displayed sufficient conditions of the final printed APS7.4 must not be the sufficiency argument, because the printed iff with only j<=b is false (see the exact A(3,5)/A(4,4) witness). Add the all-end compact-core LP1.2.4 + APS6.1/7.2 derivation above, or explicitly state and prove the all-b+p corrected consequence from those sources. The numerical output itself needs no correction. This is existing classification mathematics and cannot be promoted as candidate novelty.

**Optional clarity:** Make the nonzero scope explicit at the first claim (or output empty multiset); say workshop per-boundary total marks are2n(c), while final APS uses white marks; replace the categorical-central-idempotent shorthand by the factor argument.

**Not verified by this audit:** Correct PPP-to-APS construction, correctness/termination of rational PL search, winding computation for every enumerated certificate, translation of curves to quiver walks, practical implementation, or historical novelty. Those are separate approach families. This classification deduction does not transfer their difficulty to a new unsupported lemma.

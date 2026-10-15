# The weak-to-strong bridge for automorphisms of order four

**Status:** accepted restricted theorem after independent AI mathematical audit. This does not settle higher orders or odd characteristic. Written 2026-10-10 UTC.

## Theorem

Let k be algebraically closed of characteristic 2. Let σ∈Aut_k(k[[t]]) have exact order 4. Suppose σ(t) belongs to a degree-2 Artin–Schreier extension of k(t) contained in k((t)), as required by the original weak almost-rational definition. Then

L=k(t,σ(t),σ²(t),σ³(t))=k(t,σ(t)),

and [L:k(t)]=2. Consequently the known strong classification applies: σ belongs to the already-known order-four conjugacy class over algebraically closed k. The known conjugacy class and formula are not new results here; the restricted assertion is the removal of the common-orbit-field hypothesis in the order-four case. Historical novelty is not certified.

Dependencies are the fully stated proofs in ORBIT_TOWER_PARTIAL.md and ORDER4_R3_EXCLUSION.md. Neither companion's proof uses the conclusion of this note. The separately written ramification partial is not needed.

## 1. Reduction to orbit degree four

Put t_i=σ^i(t), with indices modulo 4. The orbit-tower theorem gives [L:k(t_i)]=2^r, with 1≤r≤3, and these extensions are Galois. It gives the corresponding degree and Galois statements for all consecutive coordinate intervals. The separate elementary group-theoretic proposition ORDER4_R3_EXCLUSION.md excludes r=3.

It remains to exclude r=2. Assume this case throughout the rest of the proof. Let X be the smooth projective curve with function field L, and let x be the place supplied by L⊂k((t)). Then σ fixes x, t is a local parameter at x, and σ acts faithfully on X with exact order 4.

Define

H_i=Gal(L/k(t_i)),
A_i=H_i∩H_(i+1)=Gal(L/k(t_i,t_(i+1))),

and write a_i for the nonidentity element of A_i. We have |H_i|=4, |A_i|=2, and every intersection of three consecutive H_i is trivial.

Neighboring A_i and A_(i+1) are distinct and lie in H_(i+1). They therefore generate H_(i+1)≅C₂×C₂ and commute. Opposite A_i are distinct too. Indeed, A₀=A₂ would, after conjugating by σ, imply A₁=A₃; then H₀=⟨A₃,A₀⟩ would equal H₁=⟨A₀,A₁⟩, contrary to [k(t₀,t₁):k(t₀)]=2. Thus all four involutions are distinct, and

H_i=⟨a_(i−1),a_i⟩≅C₂×C₂.                 (1)

Let E_i=L^{A_i}=k(t_i,t_(i+1)). All E_i have the same genus e because σ permutes them, and e≤1 by the bidegree-(2,2) genus bound. The whole-curve bound in the orbit-tower note gives

g_X≤5.                                                    (2)

## 2. Elementary elliptic facts and the low-genus cases

We use the following facts over an algebraically closed field of characteristic 2:

(a) An elliptic curve admitting an origin-fixing automorphism of order 4 is supersingular.
(b) On a supersingular elliptic curve there is no subgroup C₂×C₂ of the full automorphism group, even if the subgroup is not assumed to fix the origin.
(c) An involution of an elliptic curve with rational quotient has fixed points and is a translate of the negation involution. The product of two such involutions is a translation.

Here are explicit justifications, to avoid importing any HKG hypothesis. An ordinary elliptic curve has a model

y²+xy=x³+c x²+d,  d≠0.

Every origin-preserving automorphism has the form x↦u²x+r, y↦u³y+v x+w. Comparing the xy and y coefficients in this equation forces u=1 and r=0; comparing x and x² then gives w=0 and v²+v=0. Thus its origin-preserving automorphism group has only the identity and negation, proving (a).

A supersingular elliptic curve has a model y²+y=x³. The same substitution gives u³=1, v=u²r², r⁴=r, and w²+w=r³. If the automorphism is an involution, then u=1; its square acts by y↦y+r³, so r=0 and v=0. The unique nonidentity origin-preserving involution is therefore y↦y+1, namely negation. Also, this negation has no affine fixed point, so the group of k-rational 2-torsion points is trivial. Every elliptic automorphism is a translation followed by an origin-preserving automorphism. An involution cannot have trivial linear part, since there is no nonzero rational 2-torsion translation; hence every nonidentity involution is T_Q∘[−1]. The product of two distinct ones is a nonzero translation, which cannot have order 2. Distinct commuting involutions would have a product of order 2, proving (b).

For (c), an involution with rational quotient cannot act freely: an unramified degree-2 cover from genus 1 to genus 0 contradicts Riemann–Hurwitz. Choose a fixed point as origin. The ordinary and supersingular calculations just given show that the involution becomes negation. Returning to another origin makes it T_Q∘[−1], and the product formula proves the last assertion.

Now g_X=0 is impossible because PGL₂(k) has no element of order 4. If g_X=1, choose the σ-fixed point x as origin. By (a), X is supersingular, whereas (1) embeds C₂×C₂ in Aut(X), contradicting (b). Hence

2≤g_X≤5.                                                   (3)

In particular Aut(X) is finite. If e=0, the two fields E₀ and E₁ are rational and generate L (three consecutive coordinates already generate L when r=2). Both have index 2 in L. Castelnuovo–Severi gives g_X≤1, contrary to (3). We conclude

e=1.                                                       (4)

## 3. Two commuting dihedral subgroups

Put

B=⟨a₀,a₂⟩,  C=⟨a₁,a₃⟩,  P=BC,
r_B=a₀a₂,  r_C=a₁a₃.

Every generator of B commutes with every generator of C, by the neighboring commutations proved above. Thus B and C commute elementwise, P is a subgroup, and any inner automorphism by an element of P restricts on B to an inner automorphism by an element of B.

The two generators in each of B,C are distinct involutions. Since Aut(X) is finite, their products have finite order d≥2, the same d for both groups because σ exchanges B and C. Each group is the dihedral group of order 2d: its elements have the usual alternating normal forms in its two generating involutions. Conjugation by σ satisfies

σ(r_B)=r_C,   σ(r_C)=r_B^{-1}.                            (5)

Here σ denotes conjugation on these group elements. It normalizes P. Also P contains H₀=⟨a₃,a₀⟩, so L^P is a nonconstant subfield of k(t₀); by Lüroth it is rational.

### Even d is impossible

When d is even, the generating reflections a₀,a₂ of the dihedral group B belong to different conjugacy classes. For example, the abelianization B/[B,B] is C₂×C₂ and their classes are distinct. Thus no inner automorphism of B interchanges a₀ and a₂.

But σ² does interchange them. If σ²∈P, its conjugation on B would be an inner automorphism of B, since C commutes with B. Contradiction. Hence ⟨σ⟩∩P=1: every nontrivial subgroup of the cyclic order-4 group contains σ². Artin's fixed-field theorem gives Aut(L/L^P)=P, so σ induces exact order 4 on the rational field L^P. This is impossible in characteristic 2. Therefore d is odd.

## 4. Odd d forces S₃×S₃ on a genus-four curve

For odd d the center of a dihedral group of order 2d is trivial. Since B and C commute, their intersection lies in both centers; hence B∩C=1 and

P=B×C.                                                     (6)

Consider E₀=L^{A₀}, a genus-one function field. The group C commutes with A₀, so descends to its curve. The descent is faithful: its kernel is C∩Aut(L/E₀)=C∩A₀, which is trivial by (6).

The involutions a₁,a₃ on E₀ have rational quotients. Their respective fixed fields are

L^{⟨A₀,A₁⟩}=L^{H₁}=k(t₁),
L^{⟨A₀,A₃⟩}=L^{H₀}=k(t₀).

By elliptic fact (c), their product r_C acts on E₀ as a translation. It is nontrivial and has exact order d, by faithfulness. Thus every nonidentity element of R_C=⟨r_C⟩ acts without fixed points on E₀, and consequently also without fixed points on X. Riemann–Hurwitz for the free action on X gives

g_X−1=d(g_(X/R_C)−1).

Together with (3), odd d≥3 implies

d=3,  g_X=4.

Consequently B≅C≅S₃, and R=⟨r_B,r_C⟩≅C₃×C₃ is characteristic in P and normalized by σ.

## 5. The quotient by C₃×C₃ is rational

Let Y=X/R and h=g_Y. The order of R is prime to the characteristic. A nontrivial inertia group is cyclic and lies in C₃×C₃, so it has order 3. If s is the number of branch points on Y, the tame Hurwitz formula is

6=2g_X−2=9(2h−2)+6s.

Therefore s=4−3h. The only possibilities are (h,s)=(0,4) and (1,1).

The second possibility is impossible for this abelian cover. To see this algebraically, suppose there were exactly one branch point Q. Its inertia subgroup has order 3. Choose a homomorphism χ:R→C₃ nontrivial on that inertia subgroup. The degree-3 cyclic intermediate cover corresponding to ker χ is branched at Q and nowhere else. Since k contains the cube roots of unity, this cover is Kummer: its function field is k(Y)(w) with w³=f for some f∈k(Y)×. For a tame cubic Kummer extension, a place is ramified exactly when its valuation on f is not divisible by 3. Thus v_Q(f) is not divisible by 3, while every other valuation of f is divisible by 3. This contradicts the degree-zero principal divisor identity Σ_T v_T(f)=0, since all places have residue degree 1 over algebraically closed k.

Hence h=0 and Y is rational.

## 6. Final quotient-action contradiction

Equation (5) shows that conjugation by σ² acts on R by inversion: it sends r_B to r_B^{-1} and r_C to r_C^{-1}. Since these elements have order 3, this action is nontrivial. As R is abelian, σ² cannot belong to R. Therefore ⟨σ⟩∩R=1.

The group σ normalizes R, so acts on k(Y)=L^R. By Artin's fixed-field theorem the kernel of restriction from ⟨σ⟩ is exactly ⟨σ⟩∩R. Its action on the rational field L^R therefore has exact order 4, again impossible in PGL₂(k).

This eliminates r=2. With r=3 already excluded, r=1 is forced, proving the theorem.

## Scope, credit, and remaining problem

The deduction of the familiar conjugacy class is an application of Bleher–Chinburg–Poonen–Symonds, Theorem 1.2 and Remark 1.4, once this restricted bridge has been established. The accepted restricted assertion here is the order-four bridge itself. Independent mathematical audit found no mandatory correction; priority and historical novelty are not certified.

The original target still asks for all orders p^n>p and all primes. This theorem leaves every order 2^n with n≥3 and all odd-characteristic possibilities unresolved. It does not claim that the order-four result settles the original weak classification.

Primary contextual source: F. M. Bleher, T. Chinburg, B. Poonen, P. Symonds, *Automorphisms of Harbater–Katz–Gabber curves*, DOI https://doi.org/10.1007/s00208-016-1490-2; author manuscript https://math.mit.edu/~poonen/papers/AutK.pdf. Its Example 7.4 records the supersingular elliptic automorphism structure in its own HKG setting; the explicit elliptic calculations in Section 2 above supply the facts needed here without assuming that setting. All other ingredients used above are the stated companion field/group arguments, Castelnuovo–Severi, Artin's fixed-field theorem, Lüroth, and tame Kummer/Riemann–Hurwitz theory.

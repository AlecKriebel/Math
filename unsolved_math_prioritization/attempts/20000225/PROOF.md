# A tangency obstruction to a proposed irreducible Harbourne construction

## Result and exact scope

The existence of a reduced irreducible complex plane curve with proper-point Harbourne constant

\[
h(C)=\frac{d^2-\sum_{p\in\operatorname{Sing}(C)}m_p^2}{\#\operatorname{Sing}(C)}<-2
\]

is **not resolved here**. The strict inequality is the target; equality is a separate, weaker threshold. Infinitely near singular points are not included in this definition.

We prove a rigorous obstruction to the proposed extension in §1.3 of Orevkov's *On curves of degree 10 with 12 triple points*, arXiv:2601.07809v3. Its required pair of smooth curves of bidegrees (1,n) and (n,1), having n distinct contacts of intersection multiplicity n, cannot exist over C when n≥5. The obstruction covers asymmetric pairs as well as symmetric pairs. This is precisely the range in which the proposed degree n²+1, (n²+n)-point family would cross the Harbourne threshold.

The argument uses the classical critical-orbit constraint for parabolic rational maps, in the precise form provided by Epstein's Theorem 1. The dynamical result is credited, not claimed as new. Every step of its application to the algebraic curves is given below. Global novelty of this application is unverified.

## 1. The dynamical input, with its normalization

For a rational map T:P¹(C)→P¹(C) of degree D>1, write δ(T) for the number of distinct infinite forward critical-orbit tails. Two forward orbits define the same tail if they meet after discarding finitely many terms.

**Standard parabolic critical-orbit bound.** Suppose p₁,…,pᵣ are distinct fixed points of T, and in a local coordinate w at pᵢ,

\[
T(w)=w+c_iw^{k_i}+O(w^{k_i+1}),\qquad c_i\ne0,\quad k_i\ge2.
\]

Then

\[
\sum_{i=1}^r(k_i-1)\le\delta(T)\le\#\operatorname{CV}(T),                 \tag{1}
\]

where CV(T) denotes the set of distinct critical values on the whole Riemann sphere, including infinity when applicable.

**Precise source and deduction.** Epstein, *Infinitesimal Thurston Rigidity and the Fatou–Shishikura Inequality*, arXiv:math/9902158v1, p.1, Theorem 1, proves γ(T)≤δ(T). The weight assigned there to a parabolic cycle is at least ν when the multiplier has order q and the first nonidentity term has degree qν+1. Our fixed points have multiplier 1, so q=1 and ν=kᵢ−1. All other cycle weights are nonnegative. This proves the first inequality of (1). Each critical orbit has the same eventual tail as the orbit of its first critical value; hence the number of infinite tails is at most the number of distinct critical values. This proves the second inequality. Epstein p.2 also credits the parabolic-petal critical-point statement to Fatou and Julia. The general irrationally indifferent part of the refined theorem is not needed for this application.

This paragraph states the complete imported theorem fragment. It does not claim a new proof of Fatou's theorem or an independent reconstruction of Epstein's full proof.

## 2. Critical values of a composition

Let f:P¹_y→P¹_x and g:P¹_x→P¹_y be rational maps of positive degrees a and b, with ab>1, and put T=g∘f. Local degrees multiply:

\[
e_y(T)=e_y(f)e_{f(y)}(g).
\]

Consequently

\[
\operatorname{Crit}(T)\subseteq
\operatorname{Crit}(f)\cup f^{-1}(\operatorname{Crit}(g)),
\]

and, after applying T,

\[
\operatorname{CV}(T)\subseteq
 g(\operatorname{CV}(f))\cup\operatorname{CV}(g).                    \tag{2}
\]

Riemann–Hurwitz on P¹ gives total ramification 2a−2 and 2b−2. Therefore the numbers of distinct critical points, and thus distinct critical values, are at most these numbers. Equation (2) yields

\[
\#\operatorname{CV}(T)\le 2a+2b-4.                                \tag{3}
\]

This is the essential improvement over applying the degree-ab bound 2ab−2 directly. Several critical points of T can have the same critical value and hence the same forward tail. Neither those preimages nor the tails are counted repeatedly.

Degree-one factors are allowed: their ramification contribution is zero. The hypothesis ab>1 is indispensable.

## 3. The graph tangency theorem

Use bihomogeneous bidegrees: a curve of bidegree (u,v) has degree u in the first coordinate x and degree v in the second coordinate y. Let

\[
\Gamma_f=\{(x,y):x=f(y)\},\qquad
\Gamma_g=\{(x,y):y=g(x)\}
\]

in P¹_x×P¹_y. Their bidegrees are (1,a) and (b,1). Each graph is smooth and irreducible.

Conversely, any reduced irreducible curve of bidegree (1,a) is such a graph. Indeed its projection to P¹_y has degree one. Equivalently its equation is x₀P(y)−x₁Q(y)=0 with coprime homogeneous P,Q of degree a: a common factor would be a fiber component. The pair (P,Q) defines a degree-a morphism P¹_y→P¹_x. This also proves smoothness directly. The analogous assertion holds for bidegree (b,1).

**Theorem 1 (total tangency excess).** For positive a,b with ab>1, let Γ_f and Γ_g be as above. Then they have no common component and

\[
\boxed{\quad
\sum_{p\in\Gamma_f\cap\Gamma_g}\bigl(I_p(\Gamma_f,\Gamma_g)-1\bigr)
\le 2a+2b-4.
\quad}                                                           \tag{4}
\]

In particular their number N of distinct intersections satisfies

\[
\boxed{\quad N\ge ab-2a-2b+5=(a-2)(b-2)+1.\quad}                    \tag{5}
\]

A negative right side in (5) is merely a vacuous lower bound.

**Proof.** A common graph component would force g∘f=id. This is impossible since deg(g∘f)=ab>1. Every intersection p=(x₀,y₀) has x₀=f(y₀) and T(y₀)=y₀, and y₀ determines p uniquely. Thus distinct intersections correspond bijectively to distinct fixed points of T.

Take local coordinates u at x₀ and v at y₀, with both coordinates zero at the indicated points. The two graph equations in the completed local ring are

\[
u-f(v)=0,\qquad v-g(u)=0.
\]

Here f and g denote their holomorphic local expressions in these charts. Eliminating u gives

\[
I_p(\Gamma_f,\Gamma_g)
 =\dim_{\mathbf C}\mathbf C[[v]]/(v-g(f(v)))
 =\operatorname{ord}_{v=0}(T(v)-v).                               \tag{6}
\]

This is finite because T is not the identity. The argument is valid at infinity by using local reciprocal coordinates; no affine-chart exclusion is being made.

If the order in (6) is one, the contribution to (4) is zero. If it is k≥2, T has multiplier one at y₀ and parabolic degeneracy k−1. Applying (1) to all such fixed points, followed by (3), proves (4).

Finally, the intersection number of bidegrees (1,a) and (b,1) is ab+1. Summing their finite local intersection multiplicities therefore gives

\[
ab+1=N+\sum_p(I_p-1)\le N+2a+2b-4,
\]

which proves (5). □

**Corollary 2 (high-contact count).** The number t of distinct intersections with I_p≥q≥2 is at most

\[
t\le\left\lfloor\frac{2a+2b-4}{q-1}\right\rfloor.                 \tag{7}
\]

This follows because each of those points contributes at least q−1 to (4).

## 4. Application to Orevkov's proposed extension

Orevkov §1.3 proposes producing an irreducible rational plane curve of degree n²+1 with n²+n ordinary n-fold points from a pair of curves of bidegrees (1,n) and (n,1) with n distinct contacts of order n. The terminology agrees with local intersection multiplicity n: his n=3 construction has three cubic contacts, which are reproduced exactly in §5 below.

**Corollary 3.** Such an irreducible graph pair is impossible for every n≥5, with no symmetry assumption.

**Proof.** Set a=b=q=n in (7). There can be at most

\[
\left\lfloor\frac{4n-4}{n-1}\right\rfloor=4
\]

contacts of local intersection multiplicity at least n. Equivalently, the n specified contacts would require

\[
n(n-1)\le4n-4,
\]

which for n>1 is n≤4. □

For comparison, if the proposed plane curve existed with the stated singularities, its numerical Harbourne constant would be

\[
h_n=\frac{(n^2+1)^2-(n^2+n)n^2}{n^2+n}
    =\frac{-n^3+2n^2+1}{n^2+n}.                                   \tag{8}
\]

The genus budget is exactly saturated:

\[
(n^2+n)\binom n2
 =\frac{n^2(n^2-1)}2
 =\frac{(n^2+1-1)(n^2+1-2)}2.
\]

Thus these are numerically rational patterns, but arithmetic consistency is not realizability.

For n=2,3,4 the values in (8) are respectively 1/6, −2/3, and −31/20, all greater than −2. For n≥5,

\[
h_n+2=\frac{-n^3+4n^2+2n+1}{n^2+n}<0.                            \tag{9}
\]

To check the strict sign uniformly, put n=5+t with t≥0. The negative of the numerator in (9) is

\[
n^3-4n^2-2n-1=t^3+11t^2+33t+14>0.
\]

The first attractive numerical target would therefore be degree 26 with 30 ordinary quintuple points, h=−37/15. Its required five quintic graph contacts demand 20 parabolic units while only 16 critical values are available. It cannot be obtained by the specified graph-pair construction.

This does **not** prove that every degree-26 plane curve with that singularity pattern is impossible: no converse saying that every such curve comes from the graph-pair construction has been proved or assumed. Nor does it settle arbitrary h<−2 curves, degree 21, or the n=4 graph-pair problem. The n=4 case passes the non-strict dynamical bound and would in any event have h>−2.

## 5. Exact positive control and boundary tests

Orevkov's established n=3 construction uses

\[
p(z)=z^3-3z^2+1,\quad q(z)=z^3-z^2+z,\quad f(z)=-q(z)/p(z),\quad g=f.
\]

These polynomials are coprime, so f has degree three. Exact symbolic calculation gives

\[
f(z)-z=-\frac{z(z-2)(z-1)(z+1)}{p(z)},
\]

and

\[
f(f(z))-z=
\frac{-3z^3(z-2)(z-1)^3(z+1)^3}
{3z^9-9z^8+6z^7-13z^6+39z^5-30z^4-8z^3+12z^2-1}.
\]

The latter numerator and denominator are coprime. Infinity is not fixed: f(∞)=−1 and f(−1)=−1. Hence the two graphs have exactly the three order-three contacts z=−1,0,1 and one transverse intersection z=2. The tangency excess is 6≤8. This checks both the contact convention and that the obstruction does not discard the known example. The curve's h=−2/3 remains credited to the established construction and does not meet the assigned threshold.

As a hypothesis control, take degree-one maps f=id and g(z)=z+1. Their graphs have a single intersection at infinity of multiplicity two. The excess is 1 while 2a+2b−4=0. Thus dropping ab>1 really would make Theorem 1 false. The historical exact checker tested this exception and rejected attempts to invoke the bound for it.

Projective coordinates are essential when checking fixed-point multiplicities: T(z)=z+1/z is degree two and has at infinity a parabolic fixed point of multiplicity three. In coordinate w=1/z, its local expression is w/(1+w²), so T(w)−w=−w³/(1+w²). Its two critical values supply exactly the required two units. The historical checker included this projective-coordinate test.

## 6. Relationship to earlier necessary conditions

Earlier work established the proper-point genus/defect identity, the nonnegative slack identity, and a degree-21 necessary-pattern classification. These are background comparisons, not findings newly proved here or dependencies of the present graph theorem. In particular, a degree-21 strict example must be rational, have no positive infinitely-near delta defect above its proper singularities, and satisfy the earlier necessary multiplicity patterns. Those conditions did not establish realizability.

The result proved here is the graph tangency obstruction above. It is a construction-route obstruction and leaves all the existing degree-21 realizability questions open. The main complex proper-point existence question remains unresolved in the primary sources and bounded current-status searches inspected here.

## Edition and verification limits

The complete mathematical argument and substantive independent audit are included in this AI-assisted, unrefereed edition. The exact one-sentence projective-coordinate clarification described in [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md) has been applied. No theorem or formula was changed. Acceptance is not external human peer review, journal acceptance or proof-assistant certification. Historical exact checks supplement the written proof; the result does not depend on omitted programs or generated certificates. Copied source documents, source extracts or images, datasets, programs, raw outputs, generated certificates and private coordination material are excluded. Edition preparation rechecked frozen bytes and publication integrity without new scholarly-source retrieval, source-text inspection, literature search or mathematical-program reruns.

## References

1. AIM, *Degenerations in Algebraic Geometry: Problem Session*, September 7, 2016, Problem 5.3. https://aimath.org/pastworkshops/degenalggeomproblems.pdf
2. A. Dimca, B. Harbourne and G. Sticlaru, *On the Bounded Negativity Conjecture and singular plane curves*, Moscow Mathematical Journal 22 (2022), 427–450. https://arxiv.org/abs/2101.07187 ; https://doi.org/10.17323/1609-4514-2022-22-3-427-450
3. S. Yu. Orevkov, *On curves of degree 10 with 12 triple points*, arXiv:2601.07809v3, especially Proposition 1 and §1.3. https://arxiv.org/abs/2601.07809 ; https://doi.org/10.17323/1609-4514-2026-26-1-87-96
4. A. L. Epstein, *Infinitesimal Thurston Rigidity and the Fatou–Shishikura Inequality*, Stony Brook IMS Preprint 1999/1, arXiv:math/9902158v1, pp.1–2, Theorem 1 and the preceding weight convention. https://arxiv.org/abs/math/9902158

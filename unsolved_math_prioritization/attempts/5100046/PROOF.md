# The focal-inversion area ratio for periods congruent to two modulo four

**5100046 / AMR-050-0046 / original arXiv k805. First-turn complete candidate, pending separate review.**

This is the opposite-parity corollary of the cyclic-sum argument already established for campaign5100044, [PR207](https://github.com/AlecKriebel/Math/pull/207). Its generic proportionality proof is repeated below with the odd half-period condition checked explicitly. The prior argument, its numerical ratio controls, Stachel's parametrization and the published N=6 formula are credited; no separate discovery or historical-priority claim is made.

## 1. Exact target and domain

Let E have axes a>b>0, center0 and original foci f_±=(±c,0), where c²=a²−b². Let the fixed strictly nested confocal elliptic caustic have axes α>β>0, with α²−β²=c². Suppose its billiard family has **least period N≡2 mod4**. Necessarily N≥6 in this nondegenerate ellipse-pair setting.

For trajectory-ordered vertices P_i, let A be their signed shoelace area. Invert each original vertex in a unit circle about f_j and join successive inverse vertices by **straight** segments; call that signed area A_j^dagger. Then

\[
 A/A_j^\dagger\quad\hbox{is independent of the orbit phase.}             \tag{1}
\]

Both areas are nonzero throughout the family, including primitive stars. Both focus choices give the same inverse area. The ratio is therefore a defined positive quantity, after choosing counterclockwise orientation, and orientation reversal does not change it.

This is arXiv2004.12497v11 Table9 k805, not the later paper's differently numbered k805,a product. The published *Fifty New Invariants* omits the row; Garcia–Reznik's *Exploring self-intersected N-periodics* calls it k806. The original source's surrounding model uses two confocal ellipses. Hyperbolic/degenerate caustics and artificial parity changes by repeating a shorter odd orbit are not included. Repeating a supported even primitive orbit merely multiplies both signed areas equally.

## 2. Positivity before division

The origin and both foci lie strictly inside the caustic. Orient every billiard segment so that this caustic lies to its left. For any point f strictly inside the caustic,

\[
 \det(P_i-f,P_{i+1}-f)>0.                                     \tag{2}
\]

Indeed the edge's supporting line is tangent to the caustic and the strict interior lies in its left half-plane. The determinant in (2) is exactly the corresponding oriented edge/point test. Taking f=0 proves A>0.

The inverse vertices, after translating the inversion center to0, are

\[
 I_i=(P_i-f)/|P_i-f|^2.
\]

Their edge determinants equal (2) divided by two positive squared distances. Hence A_j^dagger>0. Each inversion is finite because the focus is strictly inside E. This argument uses trajectory order and works for stars; it does not assume the star bounds an unsigned region. In particular a proportionality constant below cannot vanish.

## 3. Canonical coordinates and the orbit area

Use Stachel's published Theorem4.3 and equation4.9. Let k=c/α∈(0,1), k'=β/α, and let K,K' be the complete elliptic integrals for k and k'. Jacobi functions in the formulas below use modulus k, not parameter k². For the primitive turning number τ,

\[
 P(w)=(-a\operatorname{sn}w,b\operatorname{cn}w),\quad
 a=\alpha\frac{\operatorname{dn}v}{\operatorname{cn}v},\quad
 b=\frac\beta{\operatorname{cn}v},\quad
 \delta=2v=\frac{4K\tau}{N},
\]
\[
 \gcd(\tau,N)=1,\qquad 0<\tau<N/2.
                                                               \tag{3}
\]

Put m=N/2, which is odd, and ℓ=2K/m. The integer τ is odd. Since mδ=2Kτ, opposite orbit vertices are antipodal. Define

\[
 S(w)=\sum_{j=0}^{m-1}\operatorname{dn}(w+j\delta),\qquad
 C_A=ab\frac{\operatorname{sn}v\operatorname{cn}v}{\operatorname{dn}v}>0.
\]

A direct addition-formula calculation gives

\[
 A(w)=2C_A S(w).                                              \tag{4}
\]

In detail, the determinant of P(u−v),P(u+v) is

\[
 \frac{2ab\operatorname{sn}v\operatorname{cn}v\operatorname{dn}u}
 {1-k^2\operatorname{sn}^2v\operatorname{sn}^2u}.
\]

Its half equals (C_A/2)[dn(u−v)+dn(u+v)]. Summing over all N edges gives C_A times the N-term dn sum, which is2S because dn has real period2K. No convexity assumption enters this signed-area identity.

The set of real shifts jδ modulo2K is exactly {jℓ:0≤j<m}, since gcd(τ,m)=1. Thus S has periods ℓ and4iK' and anti-period2iK'. On

\[
 X=\mathbb C/(\ell\mathbb Z+4iK'\mathbb Z),
\]

it has exactly two simple poles, at p=iK' and p+2iK', with nonzero residues. At any representative of a pole, exactly one cyclic summand has that pole modulo2K; there is no cancellation. This pole statement holds for odd m as well as even m. S is strictly positive on the real axis.

## 4. The focal-inverse edge identity, with its actual distances

Take f=f_+. The ordinary distance from P(w) to f is

\[
 d_f(w)=a+c\operatorname{sn}w>0.                              \tag{5}
\]

Squaring verifies the identity, and a−c>0 fixes its sign. Translation of the inverse polygon by−f preserves area, so use I(w)=(P(w)−f)/d_f(w)².

For compactness set h=sn v, t=h², q=cn²v=1−t and

\[
 U=1-2k^2t+k^2t^2,\quad V=1-2t+k^2t^2,\quad W=1-k^2t^2,
\]
\[
 C=\frac{b h\operatorname{dn}v\,q^2}{\alpha^3}>0,
 \qquad D(u)=1-k^2t\operatorname{sn}^2u.
\]

The addition formulas yield

\[
 \operatorname{cn}\delta=V/W,\quad \operatorname{dn}\delta=U/W,
 \quad U+V=2q\operatorname{dn}^2v,
 \quad U-V=2t(k')^2,
\]
\[
 U^2-k^2V^2=(k')^2W^2>0.                                    \tag{6}
\]

In particular U>0 and U>|kV|. For s=sn u, the product of the two **ordinary** focal distances and the translated cross product are

\[
 d_f(u-v)d_f(u+v)=
 \frac{\alpha^2(1+ks)(U+kVs)}{qD(u)},                        \tag{7}
\]
\[
 \det(P(u-v)-f,P(u+v)-f)=
 \frac{2\alpha b h\operatorname{dn}v\operatorname{dn}u(1+ks)}{D(u)}.
                                                               \tag{8}
\]

For (7), expand the product of a+c sn(u±v), using
sn(u−v)+sn(u+v)=2s cn(v)dn(v)/D(u) and
sn(u−v)sn(u+v)=(s²−t)/D(u); the numerator factors as (1+ks)(U+kVs). Equation (8) follows from the same additions and the determinant expansion. Dividing half of (8) by the square of (7) gives the inverse half-edge area

\[
 E_+(u)=\frac12\det(I(u-v),I(u+v))
       =\frac{C\operatorname{dn}u\,D(u)}{(1+ks)(U+kVs)^2}.      \tag{9}
\]

All its real factors have the required nonzero signs. These algebraic formulas define meromorphic continuations without any complex conjugation of w.

## 5. Antipodal pairing and the shared two-pole lemma

Pair opposite edges and define

\[
 A_+^\dagger(w)=R(w+v),\qquad
 R(u)=\sum_{j=0}^{m-1}B(u+j\delta),
\]
\[
 B(u)=E_+(u)+E_+(u+2K)
 =\frac{2CD(u)[U^2+k^2V(V+2U)\operatorname{sn}^2u]}
 {\operatorname{dn}u\,[U^2-k^2V^2\operatorname{sn}^2u]^2}.
                                                               \tag{10}
\]

We prove the same generic proportionality used in PR207:

\[
 \boxed{R(u)=C_R S(u+K)\quad\text{for a constant }C_R>0.}       \tag{11}
\]

The proof does **not** require m even. The only exceptional case of that earlier argument was V=0, equivalent to cnδ=0 and hence δ=K. That would imply τ/m=1/2, impossible for the odd integer m here. Thus only the following generic argument is needed.

Let r=K+iK'. On the base torus with periods2K and4iK', possible poles of B are

\[
 r,\ r+2iK',\quad r\pm\delta,\ r\pm\delta+2iK'.              \tag{12}
\]

At r and its imaginary translate, dn has a simple zero. The remaining denominator equals U²−V²=(U−V)(U+V)>0, so the pole order is at most1. The second denominator factor in (10) is W² times

\[
 \operatorname{dn}^2\delta-k^2\operatorname{cn}^2\delta\operatorname{sn}^2u.
\]

On the sn² torus (periods2K,2iK') it has one double pole and zeros at r±δ, by the standard identity

\[
 \operatorname{sn}(z+K+iK')=\operatorname{dn}z/(k\operatorname{cn}z).
\]

These two zeros are distinct: equality modulo the sn² lattice would force δ=K in0<δ<2K. Neither is p=iK' nor r. They exhaust the zero divisor and are simple, so their squares give possible double poles of B. At a common pole p of sn,cn,dn, the numerator of B has pole order at most4 and its denominator order5. Thus B is removable there. This accounts for every pole.

Reflection about r gives sn(2r−u)=sn u and dn(2r−u)=−dn u. Consequently

\[
 B(2r-u)=-B(u).                                               \tag{13}
\]

The Laurent coefficients of order−2 at r+δ and r−δ are therefore opposite; those of order−1 have the same sign. In the cyclic sum R, these locations belong to the same δ-orbit. At each possible reduced pole exactly one translate of each double-pole location contributes, and their order−2 terms cancel. The r-locations contribute at most simple poles. This remains true for the smallest odd m=3, where the three types all occur at the same reduced pole but are distinct translates on the base torus.

Thus on X, R has at most simple poles at r and r+2iK'. It has real periodℓ and imaginary anti-period2iK', as does S(u+K). The latter has a nonzero residue at r. Choose C_R to cancel that residue; the anti-period cancels the other. The difference is holomorphic on the compact torus X, hence constant, and its anti-period makes the constant zero. This proves (11). On the real axis R>0 by Section2 or (9), while S>0, so C_R is real and strictly positive.

## 6. The opposite-parity corollary

Since m and τ are both odd,

\[
 \frac{K+v}{\ell}=\frac{m+\tau}{2}\in\mathbb Z.
\]

Therefore (11) gives

\[
 A_+^\dagger(w)=C_R S(w+v+K)=C_R S(w).
\]

Combining with (4) proves

\[
 \boxed{\frac{A(w)}{A_+^\dagger(w)}=\frac{2C_A}{C_R}>0,}
\]

uniformly in phase. A finite positive expression for the constant, if desired, is

\[
 \frac{2C_A S(0)}{\sum_{j=0}^{m-1}B(v+j\delta)}.
\]

The half-orbit shift sends P_i to−P_i. Central reflection interchanges the two original foci and intertwines their unit inversions, preserving signed areas. Thus A_-^dagger=A_+^dagger and the proof holds for either focus.

The contrast with the earlier product theorem is exactly the parity of this final shift: m even and τ odd give a half-integer shift and the product invariant, whereas the present m odd gives an integer shift and the ratio invariant. We do not claim that the parity corollary is independent of the previously reviewed campaign mechanism.

## 7. Published special case, credit, and validation limits

Garcia–Reznik's later accepted manuscript, Proposition4.16, already gives for simple N=6 and unit radius

\[
 A/A_j^\dagger=\frac{4a^3b^4}{(2a-b)(a+b)^2}.
\]

For a general inversion radiusρ the ratio gains the factorρ^−4. This published case is credited, not presented as new. The all-N theorem here uses the earlier campaign generic pole lemma with its odd-m scope checked, rather than extrapolating from that special case.

The exact algebra and residue-location checks accompany this proof. Direct high-precision Euclidean inversion tests include both foci, primitive stars, positive edge determinants, the N=6 value and excluded-parity controls. They are diagnostics; the written compact-torus argument is the universal proof.

The exact source table pages and surrounding definitions were independently checked before this first substantive turn. The original target had no previous exact campaign PR; the related proof and its already existing numerical ratio controls were explicitly identified in the readiness gate. No source PDF or full text is uploaded. A separate adversarial review must decide correctness and the appropriate credited status before publication.

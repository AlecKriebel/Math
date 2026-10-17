# Proof 31  Every surviving odd four circuit of mass at least seven fails

Included supporting and related chapters: [Circuit obstructions and positive uncentered blocks](01_circuit_obstructions.md); [Every odd collinear triple with frequency at least seven fails](30_all_odd_triples.md); [A fixed noncollinear four point counterexample throughout the interval](32_uniform_noncollinear_k7.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## Theorem

Fix p with 4<p<6 and an odd integer K≥7. Every primitive affine four-circuit with relation pattern

$$
(K-2,2,-(K-2),-2)
$$

fails the constant-one **real** majorant inequality at exponent p.

The coefficients in this proof may depend on p and K. A separate exact certificate in [A fixed noncollinear four point counterexample throughout the interval](32_uniform_noncollinear_k7.md) gives one fixed full-support coefficient vector that works for every 4<p<6 when K=7.

The unresolved member of this particular surviving family is K=5. No positive or negative all-amplitude classification is claimed for it here.

## 1. Representative and real sign choice

Put L=K−2, so L≥5 is odd. Use the genuine two-dimensional configuration

$$
\Gamma_L=\{(0,0),(2,0),(0,1),(L,1)\}.
$$

Its primitive affine relation, in that order, is (L,−L,−2,2), of mass L+2=K. Each triple is affinely independent, with absolute triangle determinants 2,2,L,L. For 0<y<1 and t>0 define

$$
P_s(z,w)=1+s\,t z^2+w(y+t z^L),\qquad s\in\{1,-1\}.
$$

The positive magnitudes are (1,t,y,t), and P_− differs from their positive majorant only by the real sign of the coefficient at (2,0). Both torus variables are integrated independently throughout.

Write q=p/2∈(2,3), H(w)=1+yw, and V_s(z,w)=s z²+wz^L. If

$$
0<t<(1-y)/2,
$$

then |tV_s/H|≤2t/(1−y)<1. Hence the two binomial expansions in

$$
|P_s|^{2q}=|H|^{2q}
\left(1+\frac{tV_s}{H}\right)^q
\left(1+\frac{t\overline{V_s}}{\overline H}\right)^q
$$

converge absolutely and uniformly over the two-torus on every smaller closed t-disk. Termwise integration and a Taylor remainder of the form O(t^{K+1}) are therefore valid with y,p,K fixed.

## 2. The first sign-sensitive order

In a term from these expansions, let α₁,α₂ be the counts of z² and wz^L from V_s, and β₁,β₂ the corresponding counts from its conjugate. Integration in z imposes

$$
2(\alpha_1-\beta_1)+L(\alpha_2-\beta_2)=0.
$$

Since L is odd, the integer solutions have

$$
(\alpha_1-\beta_1,\alpha_2-\beta_2)=r(L,-2),\quad r\in\mathbb Z.
$$

If r=0, the exponent α₁+β₁ of s is even, so the term is sign independent. If r≠0, its total t-degree is at least |r|(L+2). In particular no degree below K=L+2 is sign sensitive.

At degree exactly K the only possible sign-sensitive count pairs are

$$
(\alpha_1,\alpha_2;\beta_1,\beta_2)=(L,0;0,2)
$$

and its reversal. They are complex conjugates, and L is odd. Consequently, for

$$
D_{p,L,y}(t)=\int|P_+|^p-\int|P_-|^p,
$$

we obtain

$$
D_{p,L,y}(t)=4\binom qL\binom q2 I_{L,q}(y)t^K+O(t^{K+1}),
$$

where the real quantity I is

$$
I_{L,q}(y)=\int_{\mathbb T}
H(w)^{q-L}\overline{H(w)}^{q-2}w^{-2}\,dw.
$$

The powers can be taken in their binomial branches because |yw|<1. Equivalently they are principal powers, since Re H>0. The formula also follows by simplifying |H|^{2q}H^{−L}\overline H^{−2} without a branch choice.

## 3. Exact evaluation of the remaining coefficient

Expanding in w gives

$$
I_{L,q}(y)
=y^2\sum_{n\ge0}\binom{q-L}{n+2}\binom{q-2}{n}y^{2n}
=y^2\binom{q-L}{2}
\,{}_2F_1(K-q,2-q;3;y^2).
$$

For completeness the coefficient identity is

$$
\frac{\binom{q-L}{n+2}\binom{q-2}{n}}
{\binom{q-L}{2}}
=\frac{(L+2-q)_n(2-q)_n}{(3)_n n!},
$$

where (a)_n is the rising factorial and L+2=K.

The leading norm-difference coefficient is therefore

$$
C_{p,L}(y)=
4\binom qL\binom q2\binom{q-L}{2}y^2
F_{K,q}(y^2),
\qquad
F_{K,q}(x)={}_2F_1(K-q,2-q;3;x).
$$

All factors outside F are strictly positive: binom(q,L)>0 because L≥5 is odd and 2<q<3; binom(q,2)>0; and binom(q−L,2)>0 because q−L<0.

## 4. The hypergeometric factor tends to minus infinity

Write A=K−q>0 and B=2−q∈(−1,0). Its series is

$$
F_{K,q}(x)=1+\sum_{n\ge1}c_n x^n,
\qquad c_n=\frac{(A)_n(B)_n}{(3)_n n!}<0.
$$

The sign follows directly: (A)_n>0, (B)_n<0 for every n≥1, and the denominator is positive. The gamma-ratio asymptotic gives

$$
c_n\sim
\frac{\Gamma(3)}{\Gamma(K-q)\Gamma(2-q)}
n^{K-p-2}.
$$

Its constant is negative because Γ(2−q)<0. As K≥7 and p<6,

$$
K-p-2>-1.
$$

Thus the series ∑_{n≥1}|c_n| diverges. Since all c_n are negative, monotone convergence of ∑|c_n|x^n as x↑1 gives

$$
F_{K,q}(x)\longrightarrow-\infty\qquad(x\uparrow1).
$$

Choose y∈(0,1) sufficiently close to 1 that F_{K,q}(y²)<0. Then C_{p,L}(y)<0. The analytic expansion in Section 2 now implies D_{p,L,y}(t)<0 for every sufficiently small positive t; choose t also below (1−y)/2. This is an actual majorant violation with four nonzero real coefficient magnitudes, completing the representative case.

The choices can, if desired, both be rational: the negative inequality for F persists in an open interval of y, and the negative norm difference persists in an interval 0<t<ε.

## 5. Transfer to the entire relation class

For any primitive affine four-circuit with this relation pattern, order its frequencies so that its relation is (L,−L,−2,2). After adjoining an independent common unit phase, the joint distribution of its four characters is Haar measure on the subgroup of the four-torus with annihilator

$$
\mathbb Z\,(L,-L,-2,2).
$$

The representative Γ_L has that same annihilator. Their joint measures therefore agree by equality of every Fourier coefficient. The extra common phase does not alter the absolute value of the polynomial. Hence their coefficient-dependent norm functions agree, and the real coefficient witness transfers unchanged in the matched ordering. This is the affine relation-lattice transfer in [Proof 01](01_circuit_obstructions.md).

## 6. What fails at K=5

At K=5 the same small-t leading coefficient does not furnish a counterexample. Indeed A=5−q and B=2−q, so at x=1 the convergent hypergeometric sum is

$$
F_{5,q}(1)
=\frac{\Gamma(3)\Gamma(2q-4)}
{\Gamma(q-2)\Gamma(q+1)}>0.
$$

All its nonconstant coefficients are negative, so F_{5,q}(x)≥F_{5,q}(1)>0 for 0≤x≤1. Thus this entire near-two-vertex perturbative route favors the positive majorant in the K=5 case. This is a precise obstruction to this method, **not** a proof of the full majorant property at K=5.

## Proven scope

- Every odd K≥7 in the surviving four-circuit family fails MP_p for every prescribed 4<p<6.
- Each witness here can depend on the chosen p and K.
- The separately certified K=7 coefficient vector (4,4,5,2) works simultaneously throughout 4<p<6.
- K=5 remains unresolved by these results, as does the complete fixed-exponent classification.
- No degeneration to a collinear frequency set, unexplained transfer of majorant properties under projection, or inference from a later Taylor term is used.

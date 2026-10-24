# Independent adversarial audit of the homology deductions

Checkpoint: **2026-10-17 21:39 UTC**. Completion estimate: **100% of this two-claim audit; 5% toward a resolution of 21.139**. The two elementary deductions are valid. The proposed implication from vanishing second L²-Betti number to zero second Alexander rank is false, including for hyperbolic compact-special groups. No claim here resolves 21.139.

## 1. Stabilization after a maximal second Betti number

Let
\[
C=\sup_{[G:K]<\infty}b_2(K;\mathbb Q)<\infty.
\]
All these Betti numbers are nonnegative integers, so some finite-index subgroup \(G_0\leq G\) attains \(C\). For any finite-index \(H\leq G_0\), rational restriction is injective: transfer composed with restriction is multiplication by \([G_0:H]\). Thus
\[
C=b_2(G_0)\leq b_2(H)\leq C,
\]
and restriction \(H^2(G_0;\mathbb Q)\to H^2(H;\mathbb Q)\) is an isomorphism. Equality of rational homology and cohomology dimensions is justified by field coefficients.

If \(H\triangleleft G_0\), the image of restriction lies in the invariants under \(G_0/H\). Surjectivity therefore makes the entire deck action on \(H^2(H;\mathbb Q)\) trivial. This conclusion is equally valid for the dual action on \(H_2(H;\mathbb Q)\). Residual finiteness is unnecessary for these statements; type F is more than the required finiteness of the Betti numbers.

### Finite-image coefficients: a stronger exact conclusion

For every finite-dimensional rational representation \(V\) of \(G_0\) with finite image, the natural map is an isomorphism:
\[
H^2(G_0;\mathbb Q)\otimes V^{G_0}
\ \xrightarrow{\ \cong\ } H^2(G_0;V).
\]
Indeed take the finite-index normal subgroup \(H=\ker(G_0\to\mathrm{GL}(V))\) and set \(Q=G_0/H\). Finite-group cohomology over \(\mathbb Q\) vanishes in positive degrees, so Hochschild–Serre gives
\[
H^2(G_0;V)\cong
\big(H^2(H;\mathbb Q)\otimes V\big)^Q.
\]
The first tensor factor has trivial \(Q\)-action by the preceding argument; restriction identifies it with \(H^2(G_0;\mathbb Q)\). In particular invariant-free finite-image systems have zero second cohomology, and
\[
\dim H^2(G_0;V)=C\dim V^{G_0}.
\]
Shapiro gives the equivalent check: \(H^2(G_0;\mathbb Q[Q])\cong H^2(H;\mathbb Q)\) has dimension \(C\), so the augmentation summand of the regular representation contributes zero. Maschke's theorem then gives the same vanishing for every representation with no trivial summand. The same conclusions hold with any finite-index subgroup of \(G_0\) as base.

Conversely, this invariant-free finite-image vanishing condition for a base group implies constant second Betti number on its finite-index subgroups: apply Shapiro to regular representations for normal subgroups, and then compare any subgroup with its normal core. Thus this is a useful equivalent formulation of the stabilized condition, not an independent solution mechanism.

## 2. Cyclic-cover formula and its precise strength

Let \(X\) be a finite \(K(G,1)\), \(\chi:G\twoheadrightarrow\mathbb Z\), \(\Lambda=\mathbb Q[t,t^{-1}]\), and \(A_i=H_i(X_\infty;\mathbb Q)=H_i(\ker\chi;\mathbb Q)\). The cellular complex \(C_*(X_\infty;\mathbb Q)\) consists of finitely generated free \(\Lambda\)-modules. Since \(\Lambda\) is Noetherian, every \(A_i\) is finitely generated. Write \(A_i\cong\Lambda^{r_i}\oplus T_i\). Every finitely generated torsion \(\Lambda\)-module is finite-dimensional over \(\mathbb Q\); the qualification about the torsion part of \(A_1\) is therefore automatic here.

For \(f_n=t^n-1\), multiplication by \(f_n\) on the cellular complex gives the exact homology sequence
\[
0\longrightarrow A_2/f_nA_2
\longrightarrow H_2(X_n;\mathbb Q)
\longrightarrow\ker(f_n:A_1\to A_1)
\longrightarrow0.
\]
Consequently, with \(G_n=\chi^{-1}(n\mathbb Z)\),
\[
b_2(G_n)=nr_2+
\dim_{\mathbb Q}(T_2/f_nT_2)+
\dim_{\mathbb Q}\ker(f_n:A_1\to A_1).
\]
The free part of \(A_1\) has zero kernel. The final two terms lie between zero and \(\dim T_2+\dim T_1\). Thus
\[
\sup_{n\geq1}b_2(G_n)<\infty
\quad\Longleftrightarrow\quad r_2=0,
\qquad
\lim_{n\to\infty}\frac{b_2(G_n)}n=r_2.
\]
There is no hidden cancellation: all terms are nonnegative. The short exact sequence need not split naturally, but no splitting is needed for the dimension formula.

More explicitly, if \(T_i\cong\bigoplus_j\Lambda/(p_{ij})\), each torsion contribution is \(\sum_j\deg\gcd(p_{ij},t^n-1)\). The bounded remainder is periodic in \(n\): only cyclotomic factors contribute. After maximal-Betti stabilization in part 1, neither \(T_1\) nor \(T_2\) can contain a cyclotomic factor \(\Phi_m\) with \(m>1\). Powers of \(t-1\) and noncyclotomic torsion are not excluded by cyclic Betti numbers alone. This last observation states a limitation of the test.

## 3. Falsified implication: vanishing L²-homology does not control every character

Take a closed orientable surface \(S_g\) of genus \(g\geq2\) and
\[
G=\pi_1(S_g)*\langle u\rangle,
\qquad \chi(\pi_1(S_g))=0,\quad\chi(u)=1.
\]
The finite aspherical complex \(S_g\vee S^1\) is a \(K(G,1)\). Its infinite cyclic cover is a line with one surface attached at each integer. Translation gives
\[
A_2\cong\Lambda,\qquad A_1\cong\Lambda^{2g}.
\]
Its \(n\)-fold cyclic cover is a circle with \(n\) attached surfaces, so \(b_2(G_n)=n\). In particular \(r_2=1\).

There is a direct check that \(b_2^{(2)}(G)=0\). Use the presentation with one relator
\[
R=[a_1,b_1]\cdots[a_g,b_g].
\]
One coordinate of the top cellular boundary is the Fox derivative
\[
\frac{\partial R}{\partial a_1}=1-a_1b_1a_1^{-1}.
\]
The corresponding operator on \(\ell^2(G)\) is injective: a vector fixed by translation by the infinite-order element \(a_1b_1a_1^{-1}\) is constant on each infinite orbit, and square summability forces it to be zero. Therefore the top boundary has zero kernel, and the 2-dimensional complex has zero second L²-Betti number. This proof does not depend on an L² free-product formula or an approximation theorem.

The example is within the ambient class of 21.139. Closed orientable surface groups admit compact special cubulations; wedging such a cube complex with a circle preserves nonpositive curvature and specialness, and gives the free product. The free product of the hyperbolic surface group with \(\mathbb Z\) is hyperbolic. For a primary confirmation of the compact-special surface assertion, see Fioravanti, *Divisible cube complexes and finite-order automorphisms of RAAGs*, arXiv:2311.12680v2, Theorem A and Corollary B(a), and its explicit surface examples: <https://arxiv.org/html/2311.12680>. The construction of the wedge preservation is immediate from disjoint vertex links and the absence of new squares or hyperplane identifications.

This is **not** a counterexample to 21.139: it violates its boundedness hypothesis. It is a counterexample to the unsupported intermediate implication \(b_2^{(2)}(G)=0\Rightarrow r_2(\chi)=0\) for arbitrary \(\chi\), even with hyperbolicity and compact specialness retained. That implication must be marked blocked rather than used as a reduction.

## Exact audit outcome

- Stabilization, restriction isomorphisms, and trivial deck action: **proved**.
- Finite-image coefficient formula: **proved**, and equivalent to stabilized boundedness.
- Cyclic-cover formula and boundedness iff zero Alexander rank: **proved**; the stated torsion finiteness proviso is redundant under finite K(G,1).
- Vanishing second L²-Betti number forcing zero second Alexander rank for every character: **refuted** by the explicit hyperbolic compact-special example above.
- Novelty and full resolution of 21.139: **not claimed**. The surviving gap is to exploit uniform control over all finite-index subgroups, rather than L²-vanishing alone or one selected cyclic tower.

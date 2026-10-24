# A failed top-degree spectral filter, with a checkable product calculation

**Status:** partial negative filter, not a solution of Kourovka 21.129 and not a novelty claim for the general product formula. It eliminates an explicitly defined top-degree spectral strategy for all four residual pairs. It does not eliminate lower-degree spectral information of the centerless quotients.

## 1. Objects and established input

For each irreducible spherical type T of rank n in

`F4, H4, D6, E6, D7, E7, D8, E8`,

let P_T be the pure Artin group and Q_T=P_T/Z(P_T). The reviewed reduction supplies P_T≅Q_T×Z. The reflection-arrangement model is a K(P_T,1). Deconing one reflecting hyperplane gives an affine arrangement complement X_T of complex dimension d=n−1 and a product M_T≅X_T×C*. Its circle factor is Z(P_T), so X_T is a K(Q_T,1). One may replace X_T by a finite d-dimensional CW model. The arrangement is essential of rank d.

The primary inputs inspected here are:

- [Davis–Januszkiewicz–Leary, Theorem A / Theorem 6.2](https://people.math.osu.edu/davis.12/djl2.pdf), *Groups Geom. Dyn.* 1 (2007), 301–309: reduced L2 Betti numbers of an affine arrangement complement vanish outside its rank; the remaining value is the beta invariant.
- [Davis, Theorem 3.13](https://people.math.osu.edu/davis.12/papers/DavisHyper.pdf), 25 February 2015 manuscript, p.11: a repaired poset-of-spaces proof of the same result. Its introduction explains the missing hypothesis in the older spectral-sequence argument. The repair is included in the source dependency, rather than silently repeating the original proof.

In particular,

\[
b_j^{(2)}(Q_T)=0\quad(j\ne d),\qquad b_d^{(2)}(Q_T)=c_T>0.
\tag{1}
\]

The strict positivity also follows from [Brieskorn, Theorem 6(ii)](https://www.numdam.org/item/SB_1971-1972__14__21_0.pdf), scanned p.401-09 / printed p.29, giving the Coxeter-arrangement Poincare factorization with exponents 1=e_1<e_2≤⋯≤e_n:

\[
P_{X_T}(u)=\prod_{i=2}^{n}(1+e_i u),\qquad
c_T=(-1)^d\chi(X_T)=\prod_{i=2}^{n}(e_i-1)>0.
\tag{2}
\]

The numerical table and exact matrix certificates are separately reproducible in `PROFILE_TABLE.md`, `compute_profiles.py`, and `profiles.json`; the spectral argument below needs only (1), not the numerical sizes of c_T.

**First failed filter:** the nonvanishing degrees of reduced L2 cohomology agree within each residual pair. Its numerical von Neumann dimension is not asserted to be a quasi-isometry invariant. Finite-index changes rescale these numbers; for example nonabelian free groups are quasi-isometric and have distinct first L2 Betti numbers.

## 2. General product lemma

Let X be a finite CW complex, let G=π1(X), and let Δ_j^X be the full cellular Laplacian on the Hilbert G-module of square-summable j-cochains of its universal cover. Give the circle one vertex and one edge, use the product cochain inner product on X×S1, and set

\[
\Theta_j^X(t)=\operatorname{tr}_{\mathcal N G}(e^{-t\Delta_j^X}),\quad
b_j=\operatorname{tr}_{\mathcal N G}(1_{\{0\}}(\Delta_j^X)).
\]

Zero cochain modules in degrees outside the dimension range contribute zero. Then for every integer k and t>0,

\[
\boxed{\quad
\Theta_k^{X\times S^1}(t)
 =q(t)\bigl(\Theta_k^X(t)+\Theta_{k-1}^X(t)\bigr),\qquad
q(t)=\frac1{2\pi}\int_{-\pi}^{\pi}e^{-2t(1-\cos\theta)}d\theta.
\quad}
\tag{3}
\]

Consequently,

\[
\boxed{\quad
\lim_{t\to\infty}\sqrt{4\pi t}\,\Theta_k^{X\times S^1}(t)=b_k+b_{k-1}.
\quad}
\tag{4}
\]

No positive lower bound on the nonzero spectrum of any Δ_j^X is required.

### Proof

The total cellular differential on the product complex is the graded tensor sum. The cross terms cancel when computing its full Laplacian. Hence the k-cochain module splits orthogonally as the sum of

\[
C^k_{(2)}(\widetilde X)\otimes C^0_{(2)}(\mathbb R)
\quad\text{and}\quad
C^{k-1}_{(2)}(\widetilde X)\otimes C^1_{(2)}(\mathbb R),
\]

and the Laplacian on each summand is Δ_j^X⊗1+1⊗Δ_q^line. With the standard cell structure of the line, both line Laplacians are 2−z−z^−1. Fourier transform identifies this with multiplication by 2(1−cosθ). The exponential of a tensor sum factors, its von Neumann trace factors, and the trace is additive on the two summands. This proves (3).

For completeness the scalar asymptotic is elementary. In the integral for q(t), outside any fixed neighborhood of 0 the contribution is exponentially small. Inside that neighborhood put θ=v/√t. Since 2t(1−cos(v/√t))→v², with a Gaussian dominating function after fixing a sufficiently small neighborhood, dominated convergence gives

\[
q(t)\sim(4\pi t)^{-1/2}.
\]

For the finite trace measure μ_j of Δ_j^X, dominated convergence also gives

\[
\Theta_j^X(t)=\int e^{-t\lambda}d\mu_j(\lambda)\longrightarrow\mu_j(\{0\})=b_j.
\]

Substitution into (3) proves (4). The same identity, since each Θ_j^X is bounded, shows all reduced L2 Betti numbers of X×S1 vanish. ∎

## 3. Application and conventions

For X_T and d=n−1, (1) and (4) yield

\[
\Theta_d^{P_T}(t)\sim\Theta_{d+1}^{P_T}(t)
\sim\frac{c_T}{\sqrt{4\pi t}},
\qquad
\sqrt t\,\Theta_k^{P_T}(t)\longrightarrow0
\quad(k\notin\{d,d+1\}).
\tag{5}
\]

Thus the explicitly normalized full-Laplacian heat exponent

\[
\eta_k=-2\lim_{t\to\infty}\frac{\log\Theta_k(t)}{\log t}
\]

exists and equals 1 in the two degrees k=d,d+1. In other degrees the limit need not exist; (5) does **not** prove that any exponent is strictly greater than 1. A logarithmic correction could retain exponent 1.

The convention matters. Some sources define the full-Laplacian Novikov–Shubin exponent without the factor 2; its value in (5) is then 1/2. Conventional boundary-map invariants also have a degree shift. Equation (5) proves a value 1 for the top boundary-map invariant in the normalization which gives Z the value 1. It does **not** prove that the preceding boundary-map invariant has value 1: the preceding full Laplacian also contains the top boundary contribution. Keeping (3)–(5) as the precise claim prevents an indexing error.

The leading amplitudes c_T depend on the chosen group trace normalization and therefore do not rescue the failed filter. Passing to finite-index subgroups changes them. The equal exponents alone cannot distinguish the rank-matched pairs.

## 4. Exact remaining gap

The useful object for a future analytic route is the centerless Q_T. Its lower-degree nonzero spectral tails are not computed by DJL's dimension-vanishing theorem: zero reduced cohomology does not imply closed image, a spectral gap, or a particular Novikov–Shubin exponent. Numerical Euler characteristics cannot replace those estimates.

[Sauer, Theorem 1.6](https://arxiv.org/pdf/math/0312129v2), pp.4 and 28, proves quasi-isometry invariance of the indicated extended Novikov–Shubin invariants for an amenable class. Every Q_T here surjects onto F2 and is nonamenable, so this theorem does not establish invariance for the proposed invariants on these groups. Theorem 6.11 treats common cocompact lattices, another hypothesis not supplied here.

An analytic separation therefore requires **both** a valid invariance mechanism under arbitrary group quasi-isometries in this nonamenable setting and an actual spectral estimate that differs within a residual pair. The top product exponents (5) cannot provide the second item. Merely postulating the first item or inferring spectral gaps from reduced L2 vanishing marks a blocked route, not progress toward a proof.

Strongest verified result in this note: the exact identity (3), asymptotic (4), and its failed-filter consequence (5), conditional only on the explicitly cited arrangement theorem and reviewed arrangement/central-splitting model. No residual quasi-isometry implication is settled.

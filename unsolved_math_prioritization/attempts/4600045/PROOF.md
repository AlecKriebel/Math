# A controlled affine-fibre obstruction to sparse jointly periodic growth

Problem 4600045 / AMR-045-0045, research attempt 1. Authored derivation, 2026-10-10.

**Status.** This note proves a complete exclusion theorem for a family of surjective cellular automata. It does **not** construct a cellular automaton with growth strictly below its alphabet size and does **not** settle Boyle–Lee Conjecture 1.4 / Boyle Conjecture 25.5. No claim of publication priority is made for the exclusion theorem.

## 1. Exact target and notation

Let `A` be a finite alphabet of size `N>1`, let `X=A^Z`, and use the shift convention `(sigma x)_i=x_{i+1}`. A cellular automaton is a finite-range, translation-invariant map `f:X→X`. Write

\[
P_k=\operatorname{Fix}(\sigma^k),\qquad
J_k(f)=|P_k\cap\operatorname{Per}(f)|,\qquad
\nu(f)=\limsup_{k\to\infty}J_k(f)^{1/k}.
\]

The original target is to find a **surjective** such `f` with `nu(f)<N`. The limsup is over every positive integer `k`, and `P_k` includes points whose least spatial period divides `k`. These conventions are verified in Boyle–Lee, pp. 2–3 [BL], and Boyle, p. 26 [B].

A strict bound requires, equivalently, some `rho<N` and `k_0` such that `J_k(f)≤rho^k` for every `k≥k_0`. A small count along one subsequence does not suffice.

## 2. The excluded family

Let `B` be any nonempty finite control alphabet of size `s`. Let `K=F_q` be a finite field of characteristic `p`. Let `c,d:B^Z→K` be arbitrary finite-range coordinate functions: each depends on only finitely many coordinates of its argument. No linearity, algebraic structure on `B`, or single-site dependence is assumed. Define `F` on the full shift `(B×K)^Z` by

\[
F(a,b)_i=
\left(a_{i+1},\ b_i+c(\sigma^i a)b_{i+1}+d(\sigma^i a)\right).
\tag{2.1}
\]

Its alphabet size is `N=sq`. The dependence of `c` or `d` on the control track can make the full map nonlinear.

**Theorem.** The map `F` is a surjective one-dimensional cellular automaton. For every `k≥1` and every control word `a∈B^k`, extend `a` periodically and set

\[
c_i=c(\sigma^i a),\qquad
Q_a(t)=\prod_{i=0}^{k-1}(t-c_i)-1,\qquad
r(a)=\operatorname{ord}_{t=0}Q_a(t).
\]

Here `r(a)=0` when `Q_a(0)≠0`. Then

\[
J_k(F)=\sum_{a\in B^k} q^{\,k-r(a)}.
\tag{2.2}
\]

In particular, the count does not depend on the affine term `d`. If `p^v` is the largest power of `p` dividing `k`, then

\[
r(a)\le(q-1)p^v.
\tag{2.3}
\]

Consequently, for every `k` not divisible by `p`,

\[
J_k(F)\ge s^kq^{\,k-(q-1)},
\tag{2.4}
\]

and therefore

\[
\boxed{\nu(F)=sq=N.}
\tag{2.5}
\]

The possibly negative exponent in the harmless lower bound (2.4) for small `k` need not be used; the exact formula remains valid.

## 3. Surjectivity on the bi-infinite full shift

The formula is finite-range and translation-invariant. Given any desired output `(u,v)`, its control preimage is uniquely determined by `a_i=u_{i-1}`. We must solve

\[
b_i+c_i b_{i+1}=y_i,
\qquad y_i=v_i-d(\sigma^i a),\quad i\in\mathbb Z.
\tag{3.1}
\]

Every finite collection of these equations has a solution. Enclose its indices in `[L,R]`, choose `b_{R+1}` arbitrarily, and recursively set

\[
b_i=y_i-c_i b_{i+1}\quad(i=R,R-1,\ldots,L).
\]

Extend the other coordinates arbitrarily. Each individual equation defines a closed subset of the compact product space `K^Z`. The finite-intersection property therefore supplies a simultaneous solution of every equation. This proves surjectivity, including when some coefficients vanish. Surjectivity on the full shift does **not** assert surjectivity on each finite periodic ring.

## 4. A shift adjustment fixes the control track

Let `S` denote the simultaneous spatial shift on both tracks and put `H=S^{-1}F`. Since `F` is a cellular automaton, `F` and `S` commute. Both preserve `P_k`, and `S^k` is the identity there. Thus, on `P_k`,

\[
\operatorname{Per}(F)=\operatorname{Per}(H).
\tag{4.1}
\]

Indeed, if `F^t x=x`, then `H^{tk}x=S^{-tk}F^{tk}x=x`; the reverse implication follows from `F=SH` in the same way.

The adjusted map is

\[
H(a,b)_i=(a_i,\ b_{i-1}+c_{i-1}b_i+d(\sigma^{i-1}a)).
\tag{4.2}
\]

For each fixed `a∈B^k`, its action on the fibre `K^k` is the affine map `b↦T_a b+e_a`, where

\[
(T_a b)_i=b_{i-1}+c_{i-1}b_i,
\]

and all indices are reduced modulo `k`.

## 5. Counting periodic points of an affine finite-dimensional map

**Lemma.** Let `T:K^k→K^k` be linear, and let `e∈K^k`. If the characteristic polynomial of `T` has a root of multiplicity `r` at zero, the affine map `A(x)=Tx+e` has exactly `q^{k-r}` periodic points.

**Proof.** Choose `m` sufficiently large that the images and kernels of powers have stabilized. The Fitting decomposition is

\[
K^k=V_0\oplus V_1,
\qquad V_0=\ker T^m,\quad V_1=\operatorname{im}T^m.
\]

For completeness, rank-nullity gives the required dimensions; the intersection is zero because, after stabilization, `ker T^{2m}=ker T^m`. The restriction `T_0` to `V_0` is nilpotent, while the restriction `T_1` to `V_1` is invertible. Their characteristic polynomials show `dim V_0=r`.

Decompose `e=e_0+e_1`. On `V_0`, the affine map has a unique fixed point because `I−T_0` is invertible. Translation by that point conjugates this component to `T_0`, whose only periodic point is zero. On `V_1`, the affine map is a permutation of the finite set `V_1`, so all `q^{k-r}` points are periodic. Their product proves the assertion. ∎

The characteristic polynomial of `T_a` is

\[
\det(tI-T_a)=\prod_{i=0}^{k-1}(t-c_i)-1=Q_a(t).
\tag{5.1}
\]

For `k≥2`, the determinant expansion has just the diagonal permutation and the complete cyclic permutation. The latter contributes `−1`, including `k=2`. For `k=1`, the operator is multiplication by `1+c_0`, and (5.1) follows directly. This handles the small-ring overlap explicitly.

Apply the affine lemma in each of the `s^k` distinct control fibres, then use (4.1). This proves (2.2). There is no division by `k`: words with a distinguished origin are exactly the points of `P_k`, not shift orbits.

## 6. The bounded-root-multiplicity argument

We prove (2.3). If any `c_i=0`, then `Q_a(0)=−1≠0`, so `r(a)=0`. The same conclusion holds whenever `Q_a(0)≠0`. Assume all `c_i≠0` and `Q_a(0)=0`.

Let `U⊂K^×` be the set of distinct coefficients and write `n_u>0` for the number of occurrences of `u`. Set

\[
e=\min_{u\in U}v_p(n_u),\quad n_u=p^e m_u,
\quad R(t)=\prod_{u\in U}(t-u)^{m_u}.
\]

At least one `m_u` is not divisible by `p`, and `p^e` divides `sum n_u=k`. In characteristic `p`,

\[
Q_a(t)=R(t)^{p^e}-1=(R(t)-1)^{p^e}.
\tag{6.1}
\]

As `Q_a(0)=0`, necessarily `R(0)=1`. Put `h=ord_0(R−1)`, so `r(a)=p^e h`.

The logarithmic derivative is

\[
\frac{R'(t)}{R(t)}
=\sum_{u\in U}\frac{m_u}{t-u}
=\frac{A(t)}{D(t)},\qquad
D(t)=\prod_{u\in U}(t-u).
\tag{6.2}
\]

The numerator `A` is not the zero polynomial. To see this, choose `u` with `m_u≠0` in `K`; the corresponding rational function has nonzero residue at its distinct pole `u`. Also `deg A≤|U|−1`. Since `R(0)=1` and `D(0)≠0`,

\[
\operatorname{ord}_0 R'
=\operatorname{ord}_0 A\le |U|-1.
\]

Differentiation of a polynomial with a zero of order `h` at zero gives a derivative with order at least `h−1`. In positive characteristic the order can increase; this only strengthens the needed inequality. The derivative is nonzero by (6.2). Therefore

\[
h-1\le\operatorname{ord}_0R'\le |U|-1,
\quad h\le|U|\le q-1.
\]

It follows that

\[
r(a)=p^e h\le(q-1)p^e\le(q-1)p^{v_p(k)}.
\]

For `p∤k`, summing `q^{k-r(a)}≥q^{k-(q-1)}` proves (2.4). Since there are arbitrarily large `k` not divisible by `p`, this supplies a subsequence on which `J_k(F)^{1/k}→sq`. The general upper bound `J_k(F)≤(sq)^k` proves (2.5). Using a subsequence here is legitimate because it establishes a **lower** bound for the full limsup, rather than trying to establish a strict upper bound.

## 7. Two sharper special cases

### 7.1 Nonconstant one-site coefficients

Suppose `c(a)=c_0(a_0)` with `c_0:B→K` nonconstant. Let

\[
M=\max_{z\in K}|c_0^{-1}(z)|<s.
\]

A fibre has an invertible linear part exactly when

\[
(-1)^k\prod_{i=0}^{k-1}c_0(a_i)\ne1.
\tag{7.1}
\]

After fixing the first `k−1` symbols, a zero partial product makes every final choice good. A nonzero partial product excludes at most `M` final symbols. Thus at least `(s−M)s^{k−1}` control words have wholly periodic fibres. Consequently

\[
J_k(F)\ge(1-M/s)(sq)^k\quad\text{for every }k≥1,
\]

and the ordinary limit `lim_k J_k(F)^{1/k}=sq` exists. The affine function `d` may still depend on a larger control block.

### 7.2 Constant coefficients and the liminf trap

If `c≡0`, every fibre is invertible and `J_k(F)=(sq)^k`. Suppose `c≡c_*≠0`, and let `D` be the multiplicative order of `−c_*` in `K^×`. Write `k=p^v m` with `p∤m`. Then

\[
(t-c_*)^k-1=((t-c_*)^m-1)^{p^v}.
\]

The inner polynomial has nonzero derivative at zero. Its value at zero vanishes exactly when `D` divides `m`. Hence

\[
r(a)=
\begin{cases}
p^v,&D\mid m,\\
0,&D\nmid m,
\end{cases}
\qquad
J_k(F)=s^kq^{k-r(a)}.
\tag{7.2}
\]

In particular,

\[
\liminf_k J_k(F)^{1/k}=s q^{1-1/D},
\qquad
\limsup_k J_k(F)^{1/k}=sq.
\tag{7.3}
\]

For the lower limit, when loss occurs one has `m≥D`, so `r/k=1/m≤1/D`; equality occurs along `k=Dp^v`. For the upper limit use arbitrarily large `k` coprime to `p`, as already proved.

A transparent example is the binary additive automaton `f(b)_i=b_i+b_{i+1}` (`s=1`, `q=2`, `c_*=1`, `d=0`). Here

\[
J_k(f)=2^{k-2^{v_2(k)}}.
\]

For every power-of-two period there is only one jointly periodic point, but along odd periods `J_k=2^{k-1}`. Thus its lower exponential limit is `1` while the required upper exponential limit is `2`. It is **not** a solution to the sparse-growth target.

## 8. Attribution and exact remaining gap

Boyle–Lee [BL, Proposition 3.4] define linearity using coordinatewise addition modulo the alphabet size and prove full limsup growth in that setting. In particular, our one-track prime-field specialization with constant coefficient and zero affine term is already covered. The broader finite-field and controlled-alphabet cases are justified here by the self-contained proof, rather than attributed literally to that proposition. Their discussion of equicontinuity points provides another known full-growth class. The present derivation deals directly with a shift control track and arbitrary local scalar coefficients; it is offered as an authored, checkable exclusion calculation, not as a claim that no version appears elsewhere.

The preceding proof does not extend to an arbitrary nonlinear surjective automaton. Its crucial reduction is that, after multiplication by the inverse spatial shift, the control track is fixed and each fibre becomes a single affine linear map with characteristic polynomial (5.1). A general reversible control evolution, nonlinear dependence on the fibre, or a more general banded fibre operator lacks this reduction. No uniform sub-full exponential upper bound has been obtained for any such candidate. Replacing the logarithmic-derivative estimate by an unsupported claim about these general maps would transfer rather than solve the central problem.

No identified Boyle–Fiebig theorem or construction is used as evidence of a resolution.

### References

[B] Mike Boyle, *Open Problems in Symbolic Dynamics*, Conjecture 25.5, p. 26, author manuscript dated November 2007: https://www.math.umd.edu/~mboyle/papers/openfinalsub3nov2007.pdf.

[BL] Mike Boyle and Bryant Lee, *Jointly Periodic Points in Cellular Automata: Computer Explorations and Conjectures*, author manuscript dated November 2006, definitions pp. 2–3, Conjecture 1.4 p. 3, Theorem 3.2 and Proposition 3.4 p. 7: https://math.umd.edu/~mboyle/papers/18nov2006.pdf. Published in *Experimental Mathematics* 16 (2007), 293–302, https://doi.org/10.1080/10586458.2007.10129005.

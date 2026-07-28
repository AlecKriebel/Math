# The homogeneous four-party rank-two purity inequality

## Research log and outcome

- **2026-07-28 14:41 PDT.** Recast the homogeneous inequality as a
  quadratic form of the four local reduction maps and as the second
  derivative at \(-1\) of the local antisymmetry generating polynomial.
- **2026-07-28 15:03 PDT.** Reduced the theorem exactly to a single global
  cross-overlap inequality for two orthogonal pure states.  This
  formulation isolates the use of the two-dimensional reference.
- **2026-07-28 15:17 PDT.** Refuted the corresponding pair-by-pair
  Cauchy estimate by an exact Bell-factor example.  The global estimate
  is saturated because other physical pairs compensate.
- **2026-07-28 15:31 PDT.** Derived the sharp formula for a Schmidt flag.
  It proves the theorem on a large family for a qubit reference and gives
  exact counterexamples in every reference dimension at least three.
- **2026-07-28 15:44 PDT.** Audited the conditional and grouped
  three-party inequalities.  They give two independent necessary bounds
  on the swap layers, but no nonnegative linear combination gives the
  four-party target.
- **2026-07-28 15:15 PDT (variational continuation).** Derived the exact
  local-filter Euler and Hessian conditions at a putative negative
  minimum, reduced the all-qubit case to one Pauli-weight inequality, and
  found a qutrit equality family which refutes every strictly positive
  lower bound proportional to the sum of the four one-site
  determinants.

The homogeneous theorem is **not proved or refuted here**.  No
qubit-reference counterexample was found.  The main exact result is the
equivalence in Proposition 3.1: the whole question is a global
Cauchy-type inequality (24) for the marginal overlaps of two orthogonal
vectors.  The note proves several large subclasses, exhibits sharp
equality cases, and rules out three tempting shortcuts.

All arguments are from the definitions in the project.  No external
results are used.

## 1. The homogeneous functional

Let
\[
|\Psi\rangle\in
K\otimes A_1\otimes A_2\otimes A_3\otimes A_4,
\qquad \dim K\leq2,
\tag{1}
\]
be a normalized pure vector.  Put
\[
H=\operatorname{Tr}_K|\Psi\rangle\langle\Psi|.
\tag{2}
\]
Thus \(H\succeq0\), \(\operatorname{Tr}H=1\), and
\(\operatorname{rank}H\leq2\).  Write \(H_T=\operatorname{Tr}_{\bar T}H\)
and
\[
P_T=\operatorname{Tr}H_T^2.
\tag{3}
\]
Purity equality for complementary reductions of (1) gives
\[
\operatorname{Tr}\rho_K^2=\operatorname{Tr}H^2,
\qquad
\operatorname{Tr}\rho_{Ki}^2
=\operatorname{Tr}(\operatorname{Tr}_iH)^2.
\tag{4}
\]
The proposed quantity is therefore
\[
\boxed{\quad
\mathcal F(H)
=6\operatorname{Tr}H^2
+\sum_{i<j}\operatorname{Tr}H_{ij}^2
-3\sum_i\operatorname{Tr}(\operatorname{Tr}_iH)^2.
\quad}
\tag{5}
\]
The theorem under investigation is
\[
H\succeq0,\quad \operatorname{rank}H\leq2
\quad\Longrightarrow\quad
\mathcal F(H)\geq0.
\tag{6}
\]
The normalization \(\operatorname{Tr}H=1\) is immaterial because
\(\mathcal F\) is homogeneous of degree two.

### Lemma 1.1 (double-reduction form)

For a physical party define
\[
\mathcal R_i(Z)=\operatorname{Tr}_i(Z)\otimes I_i-Z.
\tag{7}
\]
Then, in arbitrary finite local dimensions,
\[
\boxed{\qquad
\mathcal F(H)
=\sum_{i<j}\langle H,\mathcal R_i\mathcal R_j(H)\rangle.
\qquad}
\tag{8}
\]

#### Proof

Partial-trace adjointness gives
\[
\begin{aligned}
\langle H,\mathcal R_i\mathcal R_j(H)\rangle
={}&\|H\|_2^2
-\|\operatorname{Tr}_iH\|_2^2
-\|\operatorname{Tr}_jH\|_2^2
+\|\operatorname{Tr}_{ij}H\|_2^2.
\end{aligned}
\tag{9}
\]
Summing over the six pairs counts each one-site trace three times.
Moreover, complementation permutes the six two-element subsets, so
\[
\sum_{i<j}\|\operatorname{Tr}_{ij}H\|_2^2
=\sum_{i<j}\|H_{ij}\|_2^2.
\]
This is (5). \(\square\)

Individual summands in (8) can be negative.  The proposed result is
genuinely a statement about their six-term sum.

## 2. Swap sectors and the generating polynomial

On two physical replicas let \(F_i\) swap the two copies of \(A_i\), and
put
\[
S_i=\frac{I+F_i}{2},\qquad
A_i=\frac{I-F_i}{2},\qquad
\Pi_R=\prod_{i\in R}A_i\prod_{i\notin R}S_i.
\tag{10}
\]
Define
\[
p_R=\operatorname{Tr}[(H\otimes H)\Pi_R]\geq0,\qquad
e_r=\sum_{|R|=r}p_R.
\tag{11}
\]

### Lemma 2.1 (sector formula)

\[
\boxed{\qquad
\mathcal F(H)=4e_2-12e_3+24e_4.
\qquad}
\tag{12}
\]

#### Proof

The swap trick turns (9) into
\[
\langle H,\mathcal R_i\mathcal R_j(H)\rangle
=\operatorname{Tr}\!\left[
(H\otimes H)F_{\overline{\{i,j\}}}
(I-F_i)(I-F_j)\right].
\tag{13}
\]
On \(\Pi_R\), (13) vanishes unless \(\{i,j\}\subseteq R\).  When it
does not vanish, its eigenvalue is
\[
4(-1)^{|R|-2}.
\]
There are \(\binom{|R|}{2}\) eligible pairs.  The coefficients at
levels \(2,3,4\) are therefore \(4,-12,24\), respectively. \(\square\)

Introduce the probability-generating polynomial
\[
g_H(z)=
\operatorname{Tr}\!\left[
(H\otimes H)\prod_{i=1}^4(S_i+zA_i)\right]
=\sum_{r=0}^4e_rz^r.
\tag{14}
\]
Then
\[
\boxed{\qquad \mathcal F(H)=2g_H''(-1).\qquad}
\tag{15}
\]
Also
\[
g_H(1)=1,\qquad
g_H(-1)=\operatorname{Tr}H^2=\operatorname{Tr}\rho_K^2.
\tag{16}
\]
For a qubit reference, \(g_H(-1)\geq1/2\).

These scalar facts do not prove (15) is nonnegative.  For example, the
formal nonnegative coefficient vector
\[
e_0=\frac34,\qquad e_3=\frac14,\qquad
e_1=e_2=e_4=0
\tag{17}
\]
satisfies \(g(1)=1\) and \(g(-1)=1/2\), but
\[
2g''(-1)=-3.
\]
Thus the missing input is not merely the reference purity.  It is the
fact that all the sector weights come from one common rank-two positive
operator.

## 3. Exact reduction to a global overlap inequality

Take a spectral decomposition
\[
H=\lambda|u\rangle\langle u|
+\mu|v\rangle\langle v|,
\qquad
\lambda,\mu\geq0,\qquad
\langle u,v\rangle=0,
\tag{18}
\]
where \(u,v\) are unit vectors.  For a subset \(T\), write
\[
u_T=\operatorname{Tr}_{\bar T}|u\rangle\langle u|,
\qquad
v_T=\operatorname{Tr}_{\bar T}|v\rangle\langle v|.
\tag{19}
\]
Define the two pure-state slacks
\[
\begin{aligned}
\alpha(u)
&=6+\sum_{i<j}\operatorname{Tr}u_{ij}^2
-3\sum_i\operatorname{Tr}u_{\bar i}^2,\\
\gamma(v)
&=6+\sum_{i<j}\operatorname{Tr}v_{ij}^2
-3\sum_i\operatorname{Tr}v_{\bar i}^2,
\end{aligned}
\tag{20}
\]
and the cross overlap
\[
\delta(u,v)
=\sum_{i<j}\operatorname{Tr}(u_{ij}v_{ij})
-3\sum_i\operatorname{Tr}(u_{\bar i}v_{\bar i}).
\tag{21}
\]
There is no cross term from \(6\operatorname{Tr}H^2\), because
\(\langle u,v\rangle=0\).  Direct expansion gives
\[
\boxed{\qquad
\mathcal F(H)
=\lambda^2\alpha(u)+2\lambda\mu\delta(u,v)
+\mu^2\gamma(v).
\qquad}
\tag{22}
\]

The diagonal quantities are always nonnegative.  Indeed, purity
complementarity for the pure vector \(u\) gives
\[
\begin{aligned}
\alpha(u)
&=\sum_{i<j}
\left(1-\operatorname{Tr}u_i^2-\operatorname{Tr}u_j^2
+\operatorname{Tr}u_{ij}^2\right)\\
&=\sum_{i<j}
\langle u|^{\otimes2}(I-F_i)(I-F_j)|u\rangle^{\otimes2}
\geq0,
\end{aligned}
\tag{23}
\]
and similarly for \(v\).

### Proposition 3.1 (the exact remaining lemma)

The homogeneous theorem (6) is equivalent to the following statement:

> For every pair of orthogonal unit vectors \(u,v\) on four finite
> parties,
> \[
> \boxed{\qquad
> \delta(u,v)\geq-\sqrt{\alpha(u)\gamma(v)}.
> \qquad}
> \tag{24}
> \]

#### Proof

By (23), \(\alpha,\gamma\geq0\).  The quadratic form
\[
\lambda^2\alpha+2\lambda\mu\delta+\mu^2\gamma
\]
is nonnegative for all \(\lambda,\mu\geq0\) exactly when
\(\delta\geq-\sqrt{\alpha\gamma}\).  If \(\delta\geq0\), this is
immediate.  If \(\delta<0\), minimize after setting
\(t=\lambda/\mu\geq0\):
\[
\alpha t^2+2\delta t+\gamma
\]
has minimum \(\gamma-\delta^2/\alpha\) when \(\alpha>0\).
The cases \(\alpha=0\) or \(\gamma=0\) follow by taking a one-sided
limit and require \(\delta\geq0\).  This proves both directions.
\(\square\)

There is a useful transition-operator form.  For pure \(u,v\),
index contraction gives
\[
\operatorname{Tr}(u_Tv_T)
=\left\|\operatorname{Tr}_T|u\rangle\langle v|\right\|_2^2.
\tag{25}
\]
Thus (24) is a norm inequality for the different partial contractions
of the one rank-one transition operator \(|u\rangle\langle v|\).

For the equal-spectrum state \(H=(|u\rangle\langle u|+
|v\rangle\langle v|)/2\), nonnegativity yields only
\[
\delta\geq-\frac{\alpha+\gamma}{2}.
\tag{26}
\]
Since \((\alpha+\gamma)/2\geq\sqrt{\alpha\gamma}\), (26) is strictly
weaker in general.  Hence the homogeneous theorem is not a formal
consequence of the equal-spectrum statement; the global estimate (24)
is additional content.

## 4. Why pairwise Cauchy does not prove Proposition 3.1

Put
\[
Q_{ij}=(I-F_i)(I-F_j).
\tag{27}
\]
For orthogonal \(u,v\), define
\[
\begin{aligned}
\alpha_{ij}&=\langle u|^{\otimes2}Q_{ij}|u\rangle^{\otimes2},\\
\gamma_{ij}&=\langle v|^{\otimes2}Q_{ij}|v\rangle^{\otimes2},\\
\delta_{ij}&=\langle u\otimes v|Q_{ij}|v\otimes u\rangle.
\end{aligned}
\tag{28}
\]
The last number is real.  The global physical swap turns (13) into
(28), and therefore
\[
\alpha=\sum_{i<j}\alpha_{ij},\qquad
\gamma=\sum_{i<j}\gamma_{ij},\qquad
\delta=\sum_{i<j}\delta_{ij}.
\tag{29}
\]
If
\[
\delta_{ij}\stackrel{?}{\geq}
-\sqrt{\alpha_{ij}\gamma_{ij}}
\tag{30}
\]
held for each pair, summing it and applying Cauchy--Schwarz would prove
(24).  Inequality (30) is false.

Let \(A,B,C,D\) be four parties, let
\(\phi\in A\otimes C\) be an entangled unit vector, and take
\[
u=\phi_{AC}\otimes|0\rangle_B\otimes|0\rangle_D,
\qquad
v=\phi_{AC}\otimes|1\rangle_B\otimes|0\rangle_D.
\tag{31}
\]
Write
\[
s=\operatorname{Tr}
\left(\operatorname{Tr}_C|\phi\rangle\langle\phi|\right)^2<1.
\tag{32}
\]
For the pair \(A,B\), the \(B\) factor is pure in each of \(u,v\), so
\[
\alpha_{AB}=\gamma_{AB}=0.
\tag{33}
\]
On the other hand, expanding \(Q_{AB}\), or directly swapping the
\(A\)- and \(B\)-replicas, gives
\[
\delta_{AB}=s-1<0.
\tag{34}
\]
Thus (30) fails maximally.

The global inequality is nevertheless saturated on (31).  A direct
purity count gives
\[
\alpha=\gamma=2(1-s),\qquad
\delta=-2(1-s),
\tag{35}
\]
so
\[
\delta=-\sqrt{\alpha\gamma}.
\]
The negative contribution (34) is repaired by other physical pairs.
Cross-pair compensation is therefore essential.

## 5. The quadratic has no uniform radial curvature

Fix a two-dimensional code \(U:\mathbb C^2\to A_1A_2A_3A_4\), and
restrict \(\mathcal F\) to Hermitian operators \(UhU^\dagger\).
This is a quadratic polynomial on the logical Bloch ball.  One might
hope to prove the theorem from the already nonnegative pure-state
boundary by showing that every radial restriction is concave, or from
the equal-spectrum center by showing that it is convex.  Both signs
occur exactly.

First take
\[
u=|0000\rangle,\qquad v=|1100\rangle,\qquad
Z=|u\rangle\langle u|-|v\rangle\langle v|.
\tag{36}
\]
A direct reduction count gives
\[
\boxed{\mathcal F(Z)=-2.}
\tag{37}
\]
For the opposite sign, let
\[
u=|0\rangle_{A_4}\otimes|\phi\rangle_{A_1A_2A_3},
\qquad
v=|1\rangle_{A_4}\otimes|\phi\rangle_{A_1A_2A_3},
\tag{38}
\]
and put
\[
T=\sum_{i=1}^3\operatorname{Tr}\phi_i^2.
\]
For the same traceless \(Z\),
\[
\boxed{\mathcal F(Z)=12-4T\geq0.}
\tag{39}
\]
For a two-level GHZ vector, \(T=3/2\), and (39) equals \(6\).
Thus there is neither uniform convexity nor uniform concavity on code
Bloch balls.

## 6. What the three-party theorem gives

The sharp three-party rank-two inequality can be proved in a form
needed here without assuming local dimensions.

### Lemma 6.1 (three-party sign-frame inequality)

Let \(G\succeq0\) have rank at most two on three finite parties.  Then
\[
\boxed{\quad
3\|G\|_2^2+\sum_i\|G_i\|_2^2
-2\sum_i\|\operatorname{Tr}_iG\|_2^2\geq0.
\quad}
\tag{40}
\]

#### Proof

By homogeneity take \(\operatorname{Tr}G=1\), purify \(G\) with a
qubit \(K\), and expand
\[
|\Phi\rangle\langle\Phi|
=\frac12\sum_{a=0}^3\sigma_a\otimes X_a.
\tag{41}
\]
Write \(r_a=\operatorname{Tr}X_a\) for \(a=1,2,3\), and
\(X_{a,i}=\operatorname{Tr}_{\bar i}X_a\).  Pauli orthogonality and
purity complementarity turn the left side of (40) into
\[
\frac32(1+|r|^2)
-\sum_{i=1}^3\sum_{a=1}^3\|X_{a,i}\|_2^2.
\tag{42}
\]

Fix a permutation \(\pi\) of the three Pauli axes and put
\[
Y_i=\operatorname{sgn}(X_{\pi(i),i}),\qquad
O_i=\sigma_{\pi(i)}\otimes Y_i.
\]
The \(O_i\)'s are pairwise anticommuting Hermitian contractions.
If \(x_i=\langle O_i\rangle\), then
\((\sum_ix_iO_i)^2\leq(\sum_ix_i^2)I\); taking its expectation proves
\[
\sum_i\|X_{\pi(i),i}\|_1^2\leq1.
\tag{43}
\]
For any Hermitian \(X\),
\[
2\|X\|_2^2\leq\|X\|_1^2+(\operatorname{Tr}X)^2.
\tag{44}
\]
Indeed, if the positive and negative eigenvalue magnitudes sum to
\(p,q\), then
\(\|X\|_2^2\leq p^2+q^2
=\bigl((p+q)^2+(p-q)^2\bigr)/2\).
Equations (43)--(44) give
\[
2\sum_i\|X_{\pi(i),i}\|_2^2\leq1+|r|^2.
\]
Sum over all six permutations.  Every \((i,a)\) occurs twice, proving
that the last term in (42) is at most
\(\frac32(1+|r|^2)\). \(\square\)

In three-party swap-sector notation, (40) is exactly
\[
E_2\geq3E_3.
\tag{45}
\]
There are two natural ways to apply it to four parties.

First, condition the fourth party against a rank-one bra and average
over that bra.  Its second moment is a positive multiple of the
symmetric two-replica projector at the conditioned site.  For every
physical triple \(T\), this gives
\[
\sum_{\substack{R\subset T\\|R|=2}}p_R\geq3p_T.
\tag{46}
\]
Summing over the four triples counts each pair twice:
\[
\boxed{\qquad 2e_2\geq3e_3.\qquad}
\tag{47}
\]

Second, group a physical pair \(\{i,j\}\) as one party and leave the
other two sites \(k,l\) separate.  Equation (45) becomes
\[
\begin{aligned}
p_{kl}+p_{1234}
+p_{ik}+p_{jk}+p_{il}+p_{jl}
\geq3(p_{ikl}+p_{jkl}).
\end{aligned}
\tag{48}
\]
Sum (48) over all six grouped pairs.  Every two-site sector occurs
five times, the four-site sector six times, and every triple sector
three times on a right side already carrying coefficient three:
\[
\boxed{\qquad
5e_2+6e_4\geq9e_3.
\qquad}
\tag{49}
\]

Neither bound proves
\[
e_2+6e_4\geq3e_3.
\tag{50}
\]
Indeed, the formal aggregate values
\[
e_2=\frac95,\qquad e_3=1,\qquad e_4=0
\tag{51}
\]
satisfy (47) and saturate (49), but violate (50).  This is not a
physical counterexample; it proves only that a nonnegative linear
combination of these two trace-level consequences cannot close the
argument.

## 7. Schmidt flags and why the qubit dimension is sharp

Let \(\phi\) be an arbitrary pure state on \(A_1A_2A_3\), and put
\[
T=\sum_{i=1}^3\operatorname{Tr}\phi_i^2.
\tag{52}
\]
Since every reduced state has purity at most one,
\[
T\leq3.
\tag{53}
\]

### Proposition 7.1 (qubit Schmidt flag)

For
\[
|\Psi\rangle
=\sqrt{\lambda}\,|0\rangle_K|0\rangle_{A_4}|\phi\rangle
+\sqrt{\mu}\,|1\rangle_K|1\rangle_{A_4}|\phi\rangle,
\qquad
\lambda+\mu=1,
\tag{54}
\]
put \(s=\lambda^2+\mu^2=\operatorname{Tr}\rho_K^2\).  Then
\[
\boxed{\qquad
\mathcal F(H)=(2s-1)(3-T)\geq0.
\qquad}
\tag{55}
\]

#### Proof

The six physical-pair purities sum to
\[
(1+s)T:
\]
the three pairs inside \(A_1A_2A_3\) contribute \(T\), by purity
complementarity of \(\phi\), and the three pairs containing \(A_4\)
contribute \(sT\).  The four \(K\)-physical purities sum to
\[
1+sT:
\]
the state on \(KA_4\) is pure, while tracing \(A_4\) makes
\(\rho_K\) independent of each \(\phi_i\).  Therefore
\[
\begin{aligned}
\mathcal F(H)
&=6s+(1+s)T-3(1+sT)\\
&=(2s-1)(3-T).
\end{aligned}
\]
A qubit density matrix has \(s\geq1/2\), and (53) finishes the proof.
\(\square\)

Equality in (55) holds if the two Schmidt coefficients are equal, or
if \(T=3\).  For pure \(\phi\), the latter means that every one-party
reduction is pure, hence \(\phi\) is a product vector.

The same calculation exposes the exact higher-reference obstruction.
Let
\[
|\Psi_r\rangle
=|\Omega_r\rangle_{KA_4}\otimes|\phi\rangle_{A_1A_2A_3},
\qquad
|\Omega_r\rangle=\frac1{\sqrt r}\sum_{a=0}^{r-1}|a,a\rangle.
\tag{56}
\]
Then
\[
\boxed{\qquad
\mathcal F(H_r)
=\frac6r-3+\left(1-\frac2r\right)T.
\qquad}
\tag{57}
\]
For the \(r\)-level GHZ vector
\[
|\phi_r\rangle=\frac1{\sqrt r}\sum_{a=0}^{r-1}|a,a,a\rangle,
\qquad T=\frac3r,
\tag{58}
\]
equation (57) becomes
\[
\boxed{\qquad
\mathcal F(H_r)
=-\frac{3(r-1)(r-2)}{r^2}.
\qquad}
\tag{59}
\]
It vanishes at \(r=2\) and is strictly negative for every \(r\geq3\).
At \(r=3\) it is exactly \(-2/3\).

## 8. Orthogonal product eigenvectors

There is another exact nontrivial subclass.  Let \(u,v\) be orthogonal
product vectors which are identical at \(4-h\) sites and orthogonal at
the remaining \(h\) sites.  For
\[
H=\lambda|u\rangle\langle u|+\mu|v\rangle\langle v|,
\qquad \lambda,\mu\geq0,
\tag{60}
\]
put
\[
q=\lambda^2+\mu^2,\qquad t=(\lambda+\mu)^2.
\]
A reduction has squared norm \(q\) if it retains at least one
distinguishing site and \(t\) if all distinguishing sites were traced
out.  Counting the six pair reductions and four one-site traces in
(5) gives
\[
\boxed{
\mathcal F(H)=
\begin{cases}
0,&h=1,\\
2\lambda\mu,&h=2,\\
0,&h=3,4.
\end{cases}}
\tag{61}
\]
Thus all such rank-two positive operators satisfy the theorem.  The
large equality set at Hamming distances \(1,3,4\) is exact and includes
unequal Schmidt coefficients.

For comparison, the traceless choice \((\lambda,\mu)=(1,-1)\) at
distance \(h=2\) gives (37).  Positivity of the two spectral
coefficients is essential.

## 9. Conclusions and the remaining proof target

The homogeneous theorem contains the equal-spectrum four-copy endpoint
as a special case, but it has a particularly clean qubit formulation.

1. It is the reduction-map quadratic form (8), or equivalently the
   swap-polynomial curvature condition \(g_H''(-1)\geq0\).
2. Proposition 3.1 reduces it exactly to the global overlap inequality
   \[
   \sum_{i<j}\operatorname{Tr}(u_{ij}v_{ij})
   -3\sum_i\operatorname{Tr}(u_{\bar i}v_{\bar i})
   \geq-\sqrt{\alpha(u)\gamma(v)}.
   \]
3. The pairwise version is false by (31)--(35).  A successful
   epsilon/Fierz or Gram proof must mix different physical pairs.
4. The quadratic form has both curvature signs on two-dimensional code
   spaces, so neither a pure-boundary concavity argument nor an
   equal-center convexity argument works.
5. Conditional and grouped uses of the sharp three-party theorem yield
   (47) and (49), but their aggregate cone still allows (51).
6. The qubit Schmidt-flag formula (55) is nonnegative and sharp.
   Formula (59) gives exact counterexamples as soon as the reference
   dimension is at least three.

The most focused unresolved lemma is therefore (24).  It is global,
sharp, homogeneous, and expressed only through two orthogonal pure
vectors.  It is a suitable target for a direct qubit epsilon identity:
the local failures (33)--(34) show in advance that the required
sum-of-squares must contain cross-pair terms.

## 10. Minimal exact arithmetic audit

```python
from fractions import Fraction as F

# Formal swap polynomial obstruction (17).
e2, e3, e4 = F(0), F(1, 4), F(0)
assert 4*e2 - 12*e3 + 24*e4 == -3

# Higher-reference Schmidt flag with r=3 and a qutrit GHZ state.
r = F(3)
T = F(1)
assert 6/r - 3 + (1 - 2/r)*T == F(-2, 3)

# Formula (59), independently.
assert -3*(r - 1)*(r - 2)/(r*r) == F(-2, 3)

# Aggregate conditional/grouped obstruction (51).
e2, e3, e4 = F(9, 5), F(1), F(0)
assert 2*e2 >= 3*e3
assert 5*e2 + 6*e4 == 9*e3
assert e2 + 6*e4 < 3*e3
```

The audit checks only the displayed rational evaluations.  The
structural identities and inequalities are proved above.

## 11. Exact local-filter equations at a putative negative minimum

This section records the boundary argument in a form which does not make
an unproved genericity assumption.  Return to a normalized purification
\[
 |\Psi\rangle\in K\otimes A_1\otimes\cdots\otimes A_4,
 \qquad \dim K\leq2,
\tag{62}
\]
and denote its reductions by \(\rho_S\).  On two replicas put
\[
 M=6F_K+\sum_{i<j}F_iF_j-3\sum_iF_KF_i.
\tag{63}
\]
Then
\[
 c:=\langle\Psi|^{\otimes2}M|\Psi\rangle^{\otimes2}
 =6P_K+\sum_{i<j}P_{ij}-3\sum_iP_{Ki}
 =\mathcal F(H).
\tag{64}
\]

### Proposition 11.1 (full Euler equation)

At a stationary point of \(c\) on the unit sphere,
\[
\boxed{\quad
\left[
 6(\rho_K\otimes I_{\bar K})
 +\sum_{i<j}(\rho_{ij}\otimes I_{\overline{ij}})
 -3\sum_i(\rho_{Ki}\otimes I_{\overline{Ki}})
\right]|\Psi\rangle
=c|\Psi\rangle .
\quad}
\tag{65}
\]

#### Proof

For any subsystem \(S\), direct differentiation of
\(\operatorname{Tr}\rho_S^2\) gives
\[
 \delta\operatorname{Tr}\rho_S^2
 =4\operatorname{Re}
 \langle\delta\Psi|
 (\rho_S\otimes I_{\bar S})|\Psi\rangle .
\tag{66}
\]
The Lagrange multiplier equation for (64) therefore has the operator
on the left of (65).  Taking its expectation in \(\Psi\) shows that the
multiplier is \(c\). \(\square\)

Fix a physical site \(\ell\).  For a positive semidefinite local effect
\(A=L^\dagger L\), define
\[
\begin{aligned}
 N_\ell(A)
 &=
 \langle\Psi|^{\otimes2}
 (A\otimes A)_\ell M
 |\Psi\rangle^{\otimes2},\\
 d_\ell(A)&=\operatorname{Tr}(A\rho_\ell).
\end{aligned}
\tag{67}
\]
The normalized state obtained by applying \(L\) has value
\[
 \frac{N_\ell(A)}{d_\ell(A)^2}.
\tag{68}
\]
Let \(B_{N_\ell}\) denote the symmetric real polarization of the
quadratic form \(N_\ell\).

### Proposition 11.2 (local-filter Hessian certificate)

If \(\Psi\) is a global minimizer in the fixed local dimensions, then
\[
\boxed{\quad
 Q_{\ell,c}(A):=
 N_\ell(A)-c\bigl(\operatorname{Tr}A\rho_\ell\bigr)^2
 \geq0
 \quad\text{for every Hermitian }A.
\quad}
\tag{69}
\]
Moreover,
\[
\boxed{\quad
 B_{N_\ell}(I,X)=c\operatorname{Tr}(\rho_\ell X)
 \quad\text{for every Hermitian }X.
\quad}
\tag{70}
\]

#### Proof

Global minimality and (68) first give (69) for \(A\succeq0\), and
\(Q_{\ell,c}(I)=0\).  The identity is an interior point of the
positive-semidefinite cone.  Hence, for every Hermitian \(X\), the
quadratic polynomial
\[
 t\longmapsto Q_{\ell,c}(I+tX)
\tag{71}
\]
is nonnegative for all sufficiently small positive and negative \(t\)
and vanishes at \(t=0\).  Its linear coefficient is zero and its
quadratic coefficient is nonnegative.  These statements are,
respectively, (70) and \(Q_{\ell,c}(X)\geq0\). \(\square\)

There is a useful trace consequence.  Let
\(\{E_a\}_{a=1}^{d_\ell^2}\) be any Hilbert--Schmidt orthonormal
Hermitian basis on \(A_\ell\).  The completeness identity
\[
 \sum_aE_a\otimes E_a=F_\ell
\tag{72}
\]
and (69) imply
\[
\boxed{\quad T_\ell-cP_\ell\geq0,\quad}
\tag{73}
\]
where
\[
\begin{aligned}
T_\ell
&:=\langle\Psi|^{\otimes2}F_\ell M|\Psi\rangle^{\otimes2}\\
&=6P_{K\ell}
  +\sum_{j\ne\ell}P_j
  +\sum_{m\ne\ell}P_{Km}
  -3P_K
  -3\sum_{\{j,m\}\subseteq[4]\setminus\{\ell\}}P_{jm}.
\end{aligned}
\tag{74}
\]
Indeed, summing (69) over the basis gives
\[
 \sum_aQ_{\ell,c}(E_a)
 =T_\ell-c\operatorname{Tr}\rho_\ell^2.
\]
Formula (74) follows by multiplying (63) by \(F_\ell\), cancelling
\(F_\ell^2=I\), and using purity equality for complementary reductions
of the pure five-party state.

For qutrit \(A_\ell\), (74) has a direct rank-reduction consequence.
Let \(P_x=I-|x\rangle\langle x|\), where \(x\) is Haar-uniform on the
qutrit unit sphere.  The elementary second moment
\[
 \mathbb E_x\bigl[|x\rangle\langle x|^{\otimes2}\bigr]
 =\frac{I+F_\ell}{12}
\]
gives
\[
\mathbb E_x[P_x^{\otimes2}]
=\frac{5I+F_\ell}{12}.
\]
Consequently
\[
\boxed{\quad
\mathbb E_xN_\ell(P_x)=\frac{5c+T_\ell}{12}.
\quad}
\tag{74a}
\]
Thus, whenever \(5c+T_\ell<0\), at least one rank-two orthogonal
projection on site \(\ell\) preserves strict negativity.  Conversely,
a negative state for which no rank-two projection filter at site
\(\ell\) is negative must satisfy
\[
T_\ell\geq-5c.
\tag{74b}
\]

This condition can also be read directly in the local-swap sectors of
the purification.  Let \(q_{ij}\) be the mass in the sector with
physical sites \(i,j\) antisymmetric and \(K\) symmetric, let \(r_\ell\)
be the mass with \(K\) and the three physical sites other than
\(\ell\) antisymmetric, and let \(s\) be the mass with all four
physical sites antisymmetric and \(K\) symmetric.  Put
\[
e_2=\sum_{i<j}q_{ij},\qquad e_3=\sum_\ell r_\ell,\qquad
Q_\ell=\sum_{j\ne\ell}q_{\ell j}.
\]
Since the two-copy purification is invariant under the total swap,
these are precisely the sectors on which (63) is nonzero, and
\[
\begin{aligned}
\frac c4&=e_2-3e_3+6s,\\
\frac{T_\ell}{4}
&=e_2-2Q_\ell+3e_3-6r_\ell-6s.
\end{aligned}
\tag{74c}
\]
In particular, failure of all four one-site rank-reduction tests
\(5c+T_\ell<0\) forces
\[
\boxed{\quad
10e_2-27e_3+48s\geq0.
\quad}
\tag{74d}
\]
This is an additional exact necessary condition on an
interior-only negative state, but it is compatible with
\(e_2-3e_3+6s<0\); hence it is not yet a contradiction.  For an exact
formal illustration, take
\[
e_0=\frac1{20},\qquad e_2=\frac7{10},\qquad
e_3=\frac14,\qquad e_1=s=0.
\tag{74e}
\]
These masses sum to one, have reference purity
\(e_0+e_2-e_3=1/2\), and satisfy
\[
2e_2\geq3e_3,\qquad
5e_2+6s\geq9e_3,\qquad
10e_2-27e_3+48s=\frac14>0,
\]
but \(e_2-3e_3+6s=-1/20\).  Thus even the new averaged
rank-reduction condition, combined with both three-party consequences,
does not close the scalar sector cone.

Equations (65), (69), (70), and (73) are necessary conditions for a
negative interior minimizer.  They do not by themselves give a
full-rank contradiction: a homogeneous quadratic form can be
nonnegative on every rank-deficient positive effect and negative at a
positive-definite effect.  For example,
\[
 x^2+y^2+z^2-\frac{11}{10}(xy+yz+zx)
\tag{75}
\]
is nonnegative when one of \(x,y,z\) is zero and the other two are
nonnegative, but is negative at \((1,1,1)\).  Thus a boundary proof
must use more of the common-state structure than positivity of each
one-site filter polynomial.

## 12. Exact Pauli reduction for four physical qubits

Suppose now that \(K,A_1,\ldots,A_4\) are all qubits.  For a physical
subset \(R\subseteq[4]\), define
\[
\begin{aligned}
A_R&=\sum_{\substack{Q:\ \operatorname{supp}_{[4]}Q=R\\Q_K=I}}
       \langle Q\rangle_\Psi^2,\\
B_R&=\sum_{\substack{Q:\ \operatorname{supp}_{[4]}Q=R\\Q_K\ne I}}
       \langle Q\rangle_\Psi^2,
\end{aligned}
\tag{76}
\]
where the sum is over tensor products of \(I,X,Y,Z\), and put
\[
A_r=\sum_{|R|=r}A_R,\qquad B_r=\sum_{|R|=r}B_R.
\tag{77}
\]
In particular \(A_0=1\) and \(B_0\) is the squared Bloch-vector length
of \(\rho_K\).

For a physical subset \(S\), Pauli orthogonality gives
\[
\begin{aligned}
P_S&=2^{-|S|}\sum_{R\subseteq S}A_R,\\
P_{KS}&=2^{-(|S|+1)}
 \sum_{R\subseteq S}(A_R+B_R).
\end{aligned}
\tag{78}
\]
Substitution in (64) immediately yields
\[
\boxed{\quad 4\mathcal F=6+A_2-3B_1.\quad}
\tag{79}
\]
On the other hand, summing \(P_{ij}=P_{K\overline{\{i,j\}}}\) over the
six physical pairs gives
\[
\boxed{\quad
6+3A_1+A_2-6B_0-3B_1-B_2=0.
\quad}
\tag{80}
\]
Eliminating \(A_2-3B_1\) between (79) and (80) proves the second exact
form
\[
\boxed{\quad
4\mathcal F=6B_0-3A_1+B_2.
\quad}
\tag{81}
\]
Consequently, the entire all-qubit local-support case is equivalent to
the single sharp inequality
\[
\boxed{\qquad B_2+6B_0\geq3A_1.\qquad}
\tag{82}
\]

The constants in (82) are all sharp.  Three equality examples are:

* a fully product five-qubit state, for which
  \((B_0,A_1,B_2)=(1,4,6)\);
* an EPR pair between \(K\) and one physical qubit, tensored with three
  pure physical qubits, for which \((B_0,A_1,B_2)=(0,3,9)\);
* the five-qubit repetition vector
  \((|00000\rangle+|11111\rangle)/\sqrt2\), for which all three
  quantities in (82) vanish.

The endpoint \(B_0=1\) is completely proved.  In that case \(\rho_K\)
is pure, so the global pure state factors as
\(|\kappa\rangle_K\otimes|x\rangle_{[4]}\).  After rotating
\(\kappa\), exactly one nonidentity Pauli on \(K\) has expectation one,
and hence \(B_R=A_R\) for every \(R\).  Inequality (82) becomes
\[
 6+A_2-3A_1\geq0,
\tag{83}
\]
which is precisely four times the pure-state sum of squares (23).
Likewise, if any physical qubit marginal is pure, Section 8 proves the
claim by factoring that site.  Thus a counterexample, if one exists,
must have \(B_0<1\) and every physical marginal mixed.

Equation (82) has not been proved or refuted.  It is a smaller,
dimension-specific version of the global Plücker inequality (24).

## 13. Why linear Pauli-shadow constraints do not prove (82)

The obvious first-principles linear constraints on (76) are:
\[
\begin{aligned}
2^{-|S|}\sum_{R\subseteq S}A_R
&=
2^{-(1+|\bar S|)}
\sum_{R\subseteq\bar S}(A_R+B_R),\\
\sum_{R\subseteq S}(-1)^{|R|}A_R&\geq0,\\
\sum_{R\subseteq S}(-1)^{|R|}(A_R-B_R)&\geq0
\qquad(S\subseteq[4]).
\end{aligned}
\tag{84}
\]
The equality is complementary purity.  To prove the inequalities,
write, for any \(m\)-qubit reduction \(\sigma\),
\[
\widetilde\sigma=Y^{\otimes m}\sigma^TY^{\otimes m}.
\tag{85}
\]
Then \(\widetilde\sigma\succeq0\) and Pauli orthogonality gives
\[
2^m\operatorname{Tr}(\sigma\widetilde\sigma)
=\sum_{\operatorname{supp}Q\subseteq S}
(-1)^{|\operatorname{supp}Q|}\langle Q\rangle^2\geq0.
\tag{86}
\]
This proves (84), with and without \(K\).

Even the subset-resolved system (84), together with
\(A_R,B_R\geq0\) and \(A_\varnothing=1\), does not imply (82).  Here is
an exact formal countermodel.  Distinguish physical site \(1\) and put
\(U=\{2,3,4\}\).  The nonzero entries are
\[
\begin{array}{c|c}
R&A_R\\ \hline
\varnothing&1\\
\{1\}&1\\
\{i\},\ i\in U&2/3\\
\{1,i\},\ i\in U&1\\
\{i,j\}\subset U&2\\
U&3
\end{array}
\qquad
\begin{array}{c|c}
R&B_R\\ \hline
\varnothing&1\\
\{1\}&3\\
\{i\},\ i\in U&1\\
[4]&9 .
\end{array}
\tag{87}
\]
All omitted entries are zero.  Direct substitution in all sixteen
instances of (84) verifies them exactly, while
\[
A_1=3,\quad A_2=9,\quad B_0=1,\quad B_1=6,\quad B_2=0
\tag{88}
\]
and hence
\[
6+A_2-3B_1=-3.
\tag{89}
\]
This is not a physical Pauli distribution.  For example \(B_0=1\)
would make \(K\) pure and force factorization, a nonlinear consequence
not present in (84).  Thus any proof of (82) must use a nonlinear
pure-state or common-Plücker constraint.

## 14. An exact obstruction to a determinant-sum lower bound

A natural attempt suggested by boundary numerics is a bound
\[
\mathcal F(H)\stackrel{?}{\geq}
C\sum_{i=1}^4\det\rho_i,\qquad C>0,
\tag{90}
\]
for qutrit physical sites.  This is false, even on the zero set.

Let
\[
|\phi\rangle_{123}
=\frac{|000\rangle+|111\rangle+|222\rangle}{\sqrt3}
\tag{91}
\]
and
\[
|\Psi\rangle
=|\phi\rangle_{123}\otimes
\frac{|0\rangle_K|0\rangle_4+|1\rangle_K|1\rangle_4}{\sqrt2}.
\tag{92}
\]
Then
\[
H=|\phi\rangle\langle\phi|_{123}
\otimes\frac{|0\rangle\langle0|+|1\rangle\langle1|}{2}
\tag{93}
\]
has rank two.  Its needed purities are
\[
\begin{aligned}
\operatorname{Tr}H^2&=\frac12,\\
\sum_{i<j}\operatorname{Tr}H_{ij}^2
&=3\cdot\frac13+3\cdot\frac16=\frac32,\\
\sum_i\operatorname{Tr}(\operatorname{Tr}_iH)^2
&=3\cdot\frac16+1=\frac32.
\end{aligned}
\tag{94}
\]
Therefore
\[
\boxed{\quad\mathcal F(H)=0.\quad}
\tag{95}
\]
But
\[
\rho_1=\rho_2=\rho_3=I_3/3,\qquad
\rho_4=\operatorname{diag}(1/2,1/2,0),
\tag{96}
\]
so
\[
\sum_i\det\rho_i=\frac19>0.
\tag{97}
\]
Thus (90) fails for every \(C>0\).  In particular, equality does not
force all four one-site qutrit marginals to be rank deficient.  The
weaker statement that every *negative* state can be filtered to one
having a rank-deficient local marginal remains open; (69)--(74) are
the exact necessary conditions currently available for attacking it.

## 15. Status of the variational/boundary attack

The all-qubit reduction (82), the local-filter Hessian certificate
(69), and the determinant counterexample (92) are exact.  They do not
close the four-party rank-two theorem.  The remaining obstruction is
nonlinear: neither marginal-purity identities, spin-flip shadows, nor
one-site filter Hessians currently control the common decomposable
bivector strongly enough.  A proof of (82) would supply the desired
all-qubit base case, but an iteration from qutrits would still require
a separate sign-preserving rank-reduction lemma.  Formula (75) explains
why such a lemma cannot follow from boundary nonnegativity of an
arbitrary local quadratic alone.

## 16. Minimal exact audit for the continuation

The following verifier uses only rational arithmetic.  It checks every
subset instance of (84), the negative formal objective (89), and the
purity/determinant arithmetic in (94)--(97).

```python
from fractions import Fraction as F

wt = lambda x: bin(x).count("1")
full = 15
A = {r: F(0) for r in range(16)}
B = {r: F(0) for r in range(16)}

A[0] = A[1] = F(1)
for i in (2, 4, 8):
    A[i] = F(2, 3)
    A[1 | i] = F(1)
for i, j in ((2, 4), (2, 8), (4, 8)):
    A[i | j] = F(2)
A[14] = F(3)

B[0], B[1], B[15] = F(1), F(3), F(9)
for i in (2, 4, 8):
    B[i] = F(1)

for S in range(16):
    C = full ^ S
    lhs = sum(A[R] for R in range(16)
              if not (R & ~S)) / F(2**wt(S))
    rhs = sum(A[R] + B[R] for R in range(16)
              if not (R & ~C)) / F(2**(1 + wt(C)))
    assert lhs == rhs

    sh_phys = sum((-1)**wt(R) * A[R] for R in range(16)
                  if not (R & ~S))
    sh_K = sum((-1)**wt(R) * (A[R] - B[R])
               for R in range(16) if not (R & ~S))
    assert sh_phys >= 0 and sh_K >= 0

A1 = sum(A[R] for R in range(16) if wt(R) == 1)
A2 = sum(A[R] for R in range(16) if wt(R) == 2)
B1 = sum(B[R] for R in range(16) if wt(R) == 1)
assert (A1, A2, B[0], B1) == (F(3), F(9), F(1), F(6))
assert 6 + A2 - 3*B1 == -3

e0, e2, e3, e4 = F(1, 20), F(7, 10), F(1, 4), F(0)
assert e0 + e2 + e3 + e4 == 1
assert e0 + e2 - e3 + e4 == F(1, 2)
assert 2*e2 >= 3*e3
assert 5*e2 + 6*e4 >= 9*e3
assert 10*e2 - 27*e3 + 48*e4 == F(1, 4)
assert e2 - 3*e3 + 6*e4 == -F(1, 20)

rank2_purity = F(1, 2)
pair_sum = 3*F(1, 3) + 3*F(1, 6)
trace_one_sum = 3*F(1, 6) + 1
assert 6*rank2_purity + pair_sum - 3*trace_one_sum == 0
assert 3*F(1, 27) == F(1, 9)
```

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
- **2026-07-28 15:33 PDT.** Repeated the filter analysis for the weaker
  actual four-copy target \(e_2-3e_3+10e_4\).  The rank-one and rank-two
  Haar averages differ by exactly one third of the target.  The resulting
  aggregate filter slack \(R\) and conditioned slack \(C\) obey
  \(8\mathcal Q=R-C\); an exact rational sector distribution shows that
  separate positivity of all available linear slacks does not prove the
  needed comparison.
- **2026-07-28 16:24 PDT.** Corrected the preceding filter
  interpretation.  The polynomial \(e_2-3e_3+10e_4\) uses the
  equal-spectrum projection identities and cannot be continued through
  a nonunitary filter.  For the genuine endpoint form, derived the exact
  effect polynomial and the identity
  \(\mathfrak q_4(H)=3\mathbb E_x[
  \mathfrak q_4(H_{P_x})-\mathfrak q_4(H_{Q_x})]\).  The rank-one term is
  pointwise nonnegative, but the identity gives only an ordering, not a
  sign-preserving rank reduction.
- **2026-07-28 18:24 PDT.** Proved that a minimal negative projection
  would force a five-dimensional local effect Hessian to be positive
  definite.  Derived basis-free trace and determinant formulas for that
  restricted Hessian, and found exact sparse codes refuting both proposed
  scalar sign shortcuts.  If the local compression has rank at most
  three, proved that it admits an entire orthonormal basis of balanced
  qutrit lines.  If it has rank four, complexified its five-dimensional
  kernel and proved that it contains a rank-one matrix.  This reduces the
  surviving obstruction to a correlated sign question on rank-one
  points of one common kernel.

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

There is a second reduction involving only the physical Pauli weights.
Purity of the full physical system equals purity of \(K\), so (78)
with \(S=[4]\) gives
\[
B_0=\frac{-7+A_1+A_2+A_3+A_4}{8}.
\tag{82a}
\]
Summing \(P_{Ki}=P_{\bar i}\) over \(i\) gives
\[
B_1=\frac{3+A_2-A_4}{2}.
\tag{82b}
\]
Substituting (82a)--(82b) in (80) yields
\[
B_2=\frac{27+9A_1-5A_2-3A_3+3A_4}{4}.
\tag{82c}
\]
Therefore
\[
\boxed{\quad
B_2+6B_0-3A_1=\frac{3-A_2+3A_4}{2}.
\quad}
\tag{82d}
\]
In particular, the all-qubit theorem is equivalently the physical
weight-enumerator inequality
\[
\boxed{\qquad A_2\leq3(1+A_4).\qquad}
\tag{82e}
\]

For completeness, (82b) follows directly from
\[
\frac{4(1+B_0)+A_1+B_1}{4}
=\sum_iP_{Ki}
=\sum_iP_{\bar i}
=\frac{4+3A_1+2A_2+A_3}{8},
\]
followed by (82a).  This also proves (82c)--(82e) without an
independence assumption on the Pauli blocks.

The rank-one physical case of (82e) has a short complete proof.  If
\(H=|u\rangle\langle u|\), complementary purity and total Pauli
Parseval give
\[
A_2=2A_1+A_4-3.
\tag{82f}
\]
Full four-qubit spin flip gives the nonnegative square
\[
\left|\langle u|Y^{\otimes4}|\bar u\rangle\right|^2
=\frac{1-A_1+A_2-A_3+A_4}{16}
=\frac{A_1+A_4-5}{4}\geq0.
\tag{82g}
\]
Also \(A_1\leq4\), because each of the four one-qubit Bloch vectors
has squared length at most one.  Hence
\[
\begin{aligned}
3(1+A_4)-A_2
&=2(3+A_4-A_1)\\
&\geq2(8-2A_1)\geq0.
\end{aligned}
\tag{82h}
\]
Equality forces \(A_1=4\), hence every one-qubit marginal is pure and
\(u\) is fully product.  Thus the unresolved part of (82e) is genuinely
the rank-two mixing term.

A sharp spectral statement would finish not only rank two but every
positive four-qubit operator:
\[
\boxed{\quad
X=X^\dagger,\ X\text{ has exact Pauli weight }2
\quad\Longrightarrow\quad
\|X_+\|_2^2\leq\frac34\|X\|_2^2.
\quad}
\tag{82i}
\]
Here \(X_+\) is the positive part.  To see the implication, replace
\(H\) by its full-spin-flip average
\[
\sigma=\frac12\left(H+Y^{\otimes4}H^TY^{\otimes4}\right).
\]
This preserves \(A_2,A_4\), removes the odd Pauli weights, and remains
a density operator.  Put \(X=\Pi_2(\sigma)\), its exact-weight-two
orthogonal projection.  Then
\[
\|X\|_2^2=\frac{A_2}{16},\qquad
\|\sigma\|_2^2=\frac{1+A_2+A_4}{16},\qquad
\langle\sigma,X\rangle=\|X\|_2^2.
\]
Since \(\sigma\succeq0\),
\[
\|X\|_2^2
\leq\langle\sigma,X_+\rangle
\leq\|\sigma\|_2\|X_+\|_2
\leq\frac{\sqrt3}{2}\|\sigma\|_2\|X\|_2.
\]
Thus (82i) implies
\[
A_2\leq\frac34(1+A_2+A_4),
\]
which rearranges to (82e).  The constant in (82i) would be sharp:
\[
X=X_1X_2-Y_1Y_2+Z_1Z_2
\]
has eigenvalue \(3\) with multiplicity \(4\) and eigenvalue \(-1\)
with multiplicity \(12\), while \(\sum_{i<j}Z_iZ_j\) has eigenvalues
\(6,0,-2\) with multiplicities \(2,8,6\), respectively; both have
\(\|X_+\|_2^2/\|X\|_2^2=3/4\).

No proof of (82i) is currently available.  It is now the most compact
all-qubit subproblem: a purely spectral inequality for zero-field
two-local four-qubit Hamiltonians.

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
from math import comb

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

# Sharp spectra in the candidate two-local spectral lemma (82i).
assert F(4*3**2, 4*3**2 + 12*1**2) == F(3, 4)
assert F(2*6**2, 2*6**2 + 6*2**2) == F(3, 4)

rank2_purity = F(1, 2)
pair_sum = 3*F(1, 3) + 3*F(1, 6)
trace_one_sum = 3*F(1, 6) + 1
assert 6*rank2_purity + pair_sum - 3*trace_one_sum == 0
assert 3*F(1, 27) == F(1, 9)

# Actual-target obstruction (106)--(110).
e0, e1, e2, e3, e4 = (
    F(79, 160), F(1, 8), F(39, 160), F(1, 8), F(1, 80))
Q = e2 - 3*e3 + 10*e4
C = 2*e2 - 3*e3
G = 5*e2 - 9*e3 + 6*e4
R = 10*e2 - 27*e3 + 80*e4
assert e0 + e1 + e2 + e3 + e4 == 1
assert (Q, C, G, R) == (
    -F(1, 160), F(9, 80), F(27, 160), F(1, 16))
assert R - C == 8*Q
assert e0 - e1 + e2 - e3 + e4 == F(1, 2)  # P_K
assert 1 - e1/2 - e2 - F(3, 2)*e3 - 2*e4 == F(77, 160)

x = F(2, 3)
weights = {2: F(1), 3: F(-3), 4: F(10)}
layers = {2: e2, 3: e3, 4: e4}
phis = []
for k in range(5):
    value = F(0)
    for r in (2, 3, 4):
        moment = sum(
            F(comb(k, j)*comb(4-k, r-j), comb(4, r))*x**j
            for j in range(k + 1)
            if j <= r and r-j <= 4-k)
        value += weights[r]*layers[r]*moment
    phis.append(value)
assert phis == [
    -F(1, 160), F(1, 192), F(41, 2880),
    F(17, 864), F(71, 3240)]

sector = {S: F(0) for S in range(16)}
sector[0] = e0
for S in range(16):
    if wt(S) == 1:
        sector[S] = F(1, 32)
    elif wt(S) == 2:
        sector[S] = F(13, 320)
    elif wt(S) == 3:
        sector[S] = F(1, 32)
sector[15] = e4

mixed = {}
for z in range(5):
    for t in range(5-z):
        ratios = [F(0)]*z + [F(2, 3)]*t + [F(1)]*(4-z-t)
        value = F(0)
        for S, mass in sector.items():
            term = weights.get(wt(S), F(0))*mass
            for i in range(4):
                if (S >> i) & 1:
                    term *= ratios[i]
            value += term
        mixed[z, t] = value
assert mixed == {
    (0, 0): -F(1, 160), (0, 1): F(1, 192),
    (0, 2): F(41, 2880), (0, 3): F(17, 864),
    (0, 4): F(71, 3240),
    (1, 0): F(9, 320), (1, 1): F(31, 960),
    (1, 2): F(11, 360), (1, 3): F(19, 720),
    (2, 0): F(13, 320), (2, 1): F(13, 480),
    (2, 2): F(13, 720),
    (3, 0): F(0), (3, 1): F(0), (4, 0): F(0)}
```

## 17. The weaker actual four-copy target

The homogeneous functional studied above asks for
\(e_2-3e_3+6e_4\geq0\).  The actual four-copy endpoint target arising
elsewhere in the project is weaker:
\[
\boxed{\quad
\mathcal Q:=e_2-3e_3+10e_4\geq0.
\quad}
\tag{98}
\]
It is important to check whether the additional \(4e_4\) makes the
filter argument close.  The answer is that the present *linear*
filter/three-party inequalities still do not suffice.

For common local-qubit support, however, (98) is completely proved.
On a qubit,
\[
\langle\epsilon|C\otimes D|\epsilon\rangle
=\frac12\operatorname{Tr}(CYD^TY),
\qquad
|\epsilon\rangle=\frac{|01\rangle-|10\rangle}{\sqrt2}.
\]
Applying this identity at all four physical sites gives
\[
e_4=\frac1{16}\operatorname{Tr}(H\widetilde H)
=\frac{1-A_1+A_2-A_3+A_4}{256},
\qquad
\widetilde H=Y^{\otimes4}H^TY^{\otimes4}.
\tag{98a}
\]
The strong sector expression is
\[
e_2-3e_3+6e_4
=\frac{3-A_2+3A_4}{32}
\]
by (12) and (82d).  Therefore (82a) and (98a) simplify the actual
target to
\[
\boxed{\quad
\mathcal Q
=\frac{7-A_1-A_2-A_3+7A_4}{64}
=\frac{A_4-B_0}{8}.
\quad}
\tag{98b}
\]
In the projection-reduced problem \(\rho_K=I/2\), so \(B_0=0\), and
\[
\boxed{\qquad \mathcal Q=\frac{A_4}{8}\geq0.\qquad}
\tag{98c}
\]
Thus the actual four-copy target is rigorously settled whenever every
physical local support is at most two-dimensional.  The remaining
rank-reduction problem is specifically to pass from qutrit supports to
this qubit boundary without losing the sign.

**Important filter caveat.**  Formula (98) was obtained only after
using the equal-spectrum identities for a rank-two projection (or,
equivalently, \(\rho_K=I/2\)).  A nonunitary physical filter changes
the two nonzero eigenvalues and therefore destroys those identities.
Consequently, the calculations (99)--(110) below concern the *formal
continuation of the projection-eliminated polynomial* \(\mathcal Q\);
they are not values of the actual endpoint quadratic form on the
filtered operator.  They remain a valid obstruction to a purely
linear argument in the eliminated sector variables, but they do not
give a physical rank-reduction step.  Section 18 derives the correct
filter polynomial.

Use the purification sectors from (74c).  Write
\[
u_\ell=\sum_{j\ne\ell}q_{\ell j},
\]
and let \(\Theta_\ell\) denote insertion of the local swap \(F_\ell\)
in the two-copy expression for \(\mathcal Q\).  Sector signs give
\[
\boxed{\quad
\Theta_\ell
=e_2-2u_\ell+3e_3-6r_\ell-10e_4.
\quad}
\tag{99}
\]
For a Haar-uniform qutrit unit vector \(x\), put
\[
Q_x=|x\rangle\langle x|,\qquad P_x=I-Q_x.
\]
The two Haar moments used in Section 11 give the exact identities
\[
\begin{aligned}
\mathbb E_x N_\ell(Q_x)
&=\frac{\mathcal Q+\Theta_\ell}{12},\\
\mathbb E_x N_\ell(P_x)
&=\frac{5\mathcal Q+\Theta_\ell}{12}.
\end{aligned}
\tag{100}
\]
Define the individual conditioned three-party slack
\[
C_\ell=e_2-u_\ell-3r_\ell.
\tag{101}
\]
Then (99) gives
\[
\boxed{\quad
\mathbb E_x N_\ell(Q_x)=\frac{C_\ell}{6},\qquad
\mathbb E_x N_\ell(P_x)=\frac{\mathcal Q}{3}
                              +\frac{C_\ell}{6}.
\quad}
\tag{102}
\]
The first identity is exactly the conditioned three-party inequality
\(C_\ell\geq0\).  The second shows precisely why separate
nonnegativity of the rank-one and rank-two filtered states does not
compare them strongly enough.

If none of the four averaged rank-two filters is negative, summing the
second numerator in (100) gives
\[
\boxed{\quad
R:=10e_2-27e_3+80e_4\geq0.
\quad}
\tag{103}
\]
The summed conditioned inequality and the grouped inequality are
\[
C:=2e_2-3e_3\geq0,\qquad
G:=5e_2-9e_3+6e_4\geq0.
\tag{104}
\]
There is no nonnegative Farkas combination of \(C,G,R\) equal to
\(\mathcal Q\).  In fact the exact relation is
\[
\boxed{\qquad 8\mathcal Q=R-C.\qquad}
\tag{105}
\]
Thus it would be enough to prove the *comparison* \(R\geq C\), but
the currently proved facts only say \(R,C\geq0\).  Solving
\(\mathcal Q=aC+bG+cR\) gives uniquely
\[
(a,b,c)=(-1/8,0,1/8),
\]
so a nonnegative linear certificate from these three inequalities is
impossible.

Here is an exact symmetric scalar obstruction which also passes all
multi-site Haar rank-two averages.  Put
\[
e_0=\frac{79}{160},\qquad
e_1=\frac18,\qquad
e_2=\frac{39}{160},\qquad
e_3=\frac18,\qquad
e_4=\frac1{80},
\tag{106}
\]
distribute \(e_1\) equally over the four reference-plus-single sectors,
\(e_2\) equally over the six physical pairs, and \(e_3\) equally over
the four reference-plus-triple sectors.  Then
\[
\begin{aligned}
\mathcal Q&=-\frac1{160},&
C&=\frac9{80},&
G&=\frac{27}{160},&
R&=\frac1{16}.
\end{aligned}
\tag{107}
\]
The masses sum to one, give \(P_K=1/2\), and give every physical
one-site purity \(77/160\).  Thus the formal point obeys the
projection-reduced condition \(B_0=0\), as well as the elementary
qutrit one-site purity lower bound.

More strongly, formally insert independent Haar-averaged rank-two
replica effects at any nonempty set \(L\) of physical sites in the
projection-eliminated polynomial.  On a sector whose physical
antisymmetry set is \(S\), each inserted symmetric site contributes
\(6/12\), while each inserted antisymmetric site contributes \(4/12\).
Hence, for \(k=|L|\), the resulting formal value is
\[
2^{-k}\Phi_k,\qquad
\Phi_k=
\sum_{r=2}^4 w_re_r
\sum_j
\frac{\binom{k}{j}\binom{4-k}{r-j}}{\binom4r}
\left(\frac23\right)^j,
\quad (w_2,w_3,w_4)=(1,-3,10).
\tag{108}
\]
For (106), exact arithmetic gives
\[
\begin{array}{c|ccccc}
k&0&1&2&3&4\\ \hline
\Phi_k&
-1/160&1/192&41/2880&17/864&71/3240 .
\end{array}
\tag{109}
\]
Thus every nonempty formally averaged boundary insertion is strictly
positive even though the unfiltered eliminated target is negative.

The same formal obstruction survives arbitrary mixtures of independent
rank-one and rank-two Haar replica effects.  After removing the positive
overall factors \(1/6\) for a rank-one filter and \(1/2\) for a
rank-two filter, a rank-one filtered site has antisymmetric/symmetric
ratio \(0\), a rank-two filtered site has ratio \(2/3\), and an
unfiltered site has ratio \(1\).  If \(z\) sites receive rank-one
filters and \(t\) disjoint sites receive rank-two filters, the exact
sector polynomial for (106) is:
\[
\begin{array}{c|ccccc}
z\backslash t&0&1&2&3&4\\ \hline
0&-1/160&1/192&41/2880&17/864&71/3240\\
1&9/320&31/960&11/360&19/720&\\
2&13/320&13/480&13/720&&\\
3&0&0&&&\\
4&0&&&&
\end{array}
\tag{110}
\]
Every allowed entry except the unfiltered \((z,t)=(0,0)\) entry is
nonnegative.

The distribution (106) is a formal swap-sector distribution, not a
state construction and therefore not a counterexample to (98).
It proves a narrower but rigorous obstruction: conditioned/grouped
three-party inequalities plus every independent mixed rank-one/rank-two
formal replica insertion cannot establish the projection-eliminated
four-copy target by linear sector arithmetic.  It makes no assertion
about the correctly filtered endpoint form of Section 18.

## 18. Correct qutrit filter polynomial for the endpoint form

Checkpoint: 2026-07-28 16:24 PDT.

Let
\[
\mathcal L(Z)=Z-\frac12\operatorname{Tr}(Z)I_3
\]
and, for an arbitrary (possibly unnormalized) Hermitian operator \(H\)
on four qutrits, define the genuine endpoint quadratic form
\[
\mathfrak q_4(H)
=\langle H,\mathcal L^{\otimes4}(H)\rangle.
\tag{111}
\]
On two replicas put
\[
K_4=\prod_{i=1}^4\left(F_i-\frac12I\right).
\]
Then
\[
\mathfrak q_4(H)
=\operatorname{Tr}[(H\otimes H)K_4]
=\frac1{16}\sum_{R\subseteq[4]}(-3)^{|R|}p_R(H),
\tag{112}
\]
where \(p_R(H)=\operatorname{Tr}[(H\otimes H)\Pi_R]\).
Unlike (98), formula (112) is valid before and after filtering.

Fix a physical site \(\ell\).  If \(E\succeq0\) is an effect on that
qutrit, write
\[
H_E=(E^{1/2}_\ell\otimes I)H(E^{1/2}_\ell\otimes I).
\]
Because \(E\otimes E\) commutes with the local swap,
\[
\boxed{\quad
\mathfrak q_4(H_E)
=\operatorname{Tr}[(H\otimes H)(E\otimes E)_\ell K_4].
\quad}
\tag{113}
\]
Thus the filtered value is a quadratic polynomial in the *effect*
\(E\), not in an equal-spectrum projection-eliminated expression.

For a unit qutrit vector \(x\), set
\[
Q_x=|x\rangle\langle x|,\qquad P_x=I-Q_x,
\]
and abbreviate
\[
q_x=\mathfrak q_4(H_{Q_x}),\qquad
p_x=\mathfrak q_4(H_{P_x}).
\tag{114}
\]
Define the real polarized cross term
\[
c_x=\frac12\operatorname{Tr}\!\left[
(H\otimes H)
\bigl(P_x\otimes Q_x+Q_x\otimes P_x\bigr)_\ell K_4
\right].
\tag{115}
\]
For \(E_t=P_x+tQ_x\), direct expansion of (113) gives the exact
pointwise filter polynomial
\[
\boxed{\qquad
\mathfrak q_4(H_{E_t})=p_x+2t\,c_x+t^2q_x,
\qquad
\mathfrak q_4(H)=p_x+2c_x+q_x.
\qquad}
\tag{116}
\]

The Haar averages have an especially simple form.  On two qutrit
replicas,
\[
\mathbb E_x Q_x^{\otimes2}=\frac{I+F_\ell}{12}
=\frac16S_\ell,
\]
whereas
\[
\mathbb E_x P_x^{\otimes2}
=\frac{5I+F_\ell}{12}
=\frac12S_\ell+\frac13A_\ell.
\tag{117}
\]
Subtracting gives the scalar operator identity
\[
\mathbb E_x(P_x^{\otimes2}-Q_x^{\otimes2})
=\frac13I.
\tag{118}
\]
Inserting (118) into (113) proves the exact rank-reduction identity
\[
\boxed{\qquad
\mathfrak q_4(H)
=3\,\mathbb E_x\!\left[p_x-q_x\right].
\qquad}
\tag{119}
\]
This identity holds for every Hermitian \(H\); no rank, positivity, or
equal-spectrum assumption is used.

For a more resolved version, define the signed contribution from
sectors symmetric at \(\ell\) by
\[
a_\ell(H)
=\frac1{16}\sum_{\ell\notin R}(-3)^{|R|}p_R(H).
\tag{120}
\]
Equations (117) and (112) give
\[
\boxed{\quad
\mathbb E_x q_x=\frac16a_\ell(H),\qquad
\mathbb E_x p_x
=\frac16a_\ell(H)+\frac13\mathfrak q_4(H).
\quad}
\tag{121}
\]
For the normalized projection state \(H=P/2\), the first quantity in
(120) is explicitly
\[
16a_\ell
=p_\varnothing
-3\sum_{i\ne\ell}p_{\{i\}}
+9\!\!\sum_{\substack{i<j\\i,j\ne\ell}}\!\!p_{\{i,j\}}
-27p_{[4]\setminus\{\ell\}}.
\tag{122}
\]
The weight-zero and weight-one terms in (122) are precisely the terms
lost by incorrectly applying (98) after a filter.

There is useful pointwise positivity on the rank-one branch.  Put
\[
h_x=(\langle x|_\ell\otimes I)H(|x\rangle_\ell\otimes I).
\]
The filtered operator factors as \(H_{Q_x}=Q_x\otimes h_x\), and hence
\[
\boxed{\qquad
q_x=\frac12\mathfrak q_3(h_x).
\qquad}
\tag{123}
\]
If \(H\succeq0\) has rank at most two, so does \(h_x\), and the proved
strong three-party theorem gives
\[
\mathfrak q_3(h_x)
\geq\frac18\left(
2\operatorname{Tr}h_x^2-(\operatorname{Tr}h_x)^2
\right)\geq0.
\tag{124}
\]
Thus \(q_x\geq0\) for every \(x\).

Identity (119) now has an exact but limited consequence.  If
\(\mathfrak q_4(H)<0\), then some \(x\) obeys \(p_x<q_x\).  It does
*not* follow that \(p_x<0\): the nonnegative rank-one value can be
larger than the rank-two value while both remain nonnegative.  Also,
even when \(H=P/2\) starts with equal nonzero eigenvalues,
\(H_{P_x}\) generally has unequal nonzero eigenvalues.  Therefore
(119) is a correct comparison identity, but not by itself a
projection-preserving rank-reduction theorem.

The averaged rank-two branch is sign-reducing exactly under the
additional condition
\[
\boxed{\qquad
\mathbb E_xp_x<0
\quad\Longleftrightarrow\quad
a_\ell(H)+2\mathfrak q_4(H)<0.
\qquad}
\tag{124a}
\]
Negativity of the parent alone does not imply (124a), even in linear
sector arithmetic.  For the symmetric formal distribution (106),
\[
\mathfrak q_4(H)=\frac12\mathcal Q=-\frac1{320},
\qquad
a_\ell(H)=\frac{149}{5120}
\]
at every site.  Consequently the *correct* filter averages are
\[
\boxed{\qquad
\mathbb E_xq_x=\frac{149}{30720},\qquad
\mathbb E_xp_x=\frac{39}{10240}.
\qquad}
\tag{124b}
\]
Both are positive, while their difference is
\(-1/960=\mathfrak q_4(H)/3\), exactly as (119) requires.  The
distribution is still only formal, but it proves that the corrected
Haar identity plus linear sector constraints cannot force a negative
rank-two boundary average.

The same calculation tensorizes.  If \(J\) is any set of physical
qutrit sites and independent Haar vectors are chosen there, then
\[
\boxed{\quad
\mathfrak q_4(H)
=3^{|J|}
\sum_{S\subseteq J}(-1)^{|J|-|S|}
\mathbb E\,
\mathfrak q_4\!\left(
H_{\prod_{i\in S}P_{x_i}\prod_{j\in J\setminus S}Q_{x_j}}
\right).
\quad}
\tag{125}
\]
For \(J=[4]\), every leaf has common local support of dimension at most
two and its endpoint value is a literal squared norm.  Formula (125)
is nevertheless an alternating finite difference of those
nonnegative leaves, so leafwise positivity alone does not determine
the sign of the parent.

## 19. A nonlinear projection-preserving qutrit compression

Checkpoint: 2026-07-28 17:02 PDT.

The unequal-spectrum defect in Section 18 can be avoided at one
qutrit site.  The key is to choose the discarded line
state-dependently.

### Lemma 19.1 (three traceless qutrit observables have a common zero)

Let \(A_1,A_2,A_3\) be traceless Hermitian operators on
\(\mathbb C^3\).  There is a unit vector \(x\in\mathbb C^3\) such that
\[
\boxed{\qquad
\langle x,A_jx\rangle=0,\qquad j=1,2,3.
\qquad}
\tag{126}
\]

#### Proof

We first record the only topological fact used below.

> If \(G:\mathbb {CP}^2\to S^2\) is continuous, then the restriction
> of \(G\) to every projective line
> \(\mathbb {CP}^1\subset\mathbb {CP}^2\) has degree zero.

Here is a proof.  Let \(u\) generate
\(H^2(S^2;\mathbb Z)\), and let \(h\) generate
\(H^2(\mathbb {CP}^2;\mathbb Z)\).  The elementary cell decomposition
\[
\mathbb {CP}^2=e^0\cup e^2\cup e^4
\]
has one cell in each displayed dimension; its degree-two class \(h\)
satisfies that \(h^2\) generates \(H^4(\mathbb {CP}^2;\mathbb Z)\).
Equivalently, the projective line meets a generic projective line once,
with positive orientation.  Write \(G^*u=kh\).  Since
\(u^2=0\) on the two-sphere,
\[
0=G^*(u^2)=k^2h^2,
\]
and hence \(k=0\).  Restriction of \(h\) to a projective line is the
generator of its second cohomology, so \(k\) is exactly the degree of
the restriction.  This proves the stated fact.

Now consider the compact convex set
\[
\mathcal D=\left\{
\rho\succeq0:\ \operatorname{Tr}\rho=1,\
\operatorname{Tr}(\rho A_j)=0\ (j=1,2,3)
\right\}.
\tag{127}
\]
It is nonempty because \(I_3/3\in\mathcal D\).  Choose an extreme
point \(\rho\).  If \(r=\operatorname{rank}\rho\geq3\), the real vector
space of Hermitian perturbations supported on
\(\operatorname{ran}\rho\) has dimension \(r^2\geq9\).  The four real
homogeneous conditions
\[
\operatorname{Tr}D=0,\qquad
\operatorname{Tr}(DA_j)=0\quad(j=1,2,3)
\]
therefore have a nonzero solution \(D\) on that support.  For
sufficiently small \(\epsilon>0\), both
\(\rho+\epsilon D\) and \(\rho-\epsilon D\) are positive and belong to
\(\mathcal D\), contradicting extremality.  Thus
\(\operatorname{rank}\rho\leq2\).

If \(\rho\) has rank one, its spanning vector proves (126).  Suppose
it has rank two, and let \(W:\mathbb C^2\to\mathbb C^3\) be an
isometry onto its support.  Write all density matrices on this support
in Bloch form
\[
\rho(r)=\frac12W(I+r\cdot\sigma)W^\dagger,
\qquad |r|\leq1.
\tag{128}
\]
The three expectations define an affine map
\[
F(r)=c+Mr\in\mathbb R^3.
\tag{129}
\]
Our rank-two \(\rho\) corresponds to an \(r_0\) with
\(|r_0|<1\) and \(F(r_0)=0\).

If \(M\) is singular, choose \(0\ne v\in\ker M\).  The line
\(r_0+\mathbb Rv\) meets the unit sphere, and every point on that line
has the same image under \(F\).  A point of intersection therefore
gives a pure state with all three expectations zero.

It remains to exclude invertible \(M\).  Assume, for contradiction,
that no pure qutrit state has all three expectations zero.  Then
\[
G([z])
=\frac{(\langle z,A_1z\rangle,
          \langle z,A_2z\rangle,
          \langle z,A_3z\rangle)}
       {\sqrt{\sum_j\langle z,A_jz\rangle^2}}
\tag{130}
\]
is a continuous map from \(\mathbb {CP}^2\) to \(S^2\).
On the projective line \(\mathbb P(\operatorname{ran}W)\), identified
with the Bloch sphere \(|r|=1\), it is
\[
r\longmapsto
\frac{M(r-r_0)}{|M(r-r_0)|}.
\tag{131}
\]
Because \(|r_0|<1\), replacing \(r_0\) continuously by zero never
makes the denominator vanish on \(|r|=1\).  The resulting normalized
invertible linear map has degree
\(\operatorname{sgn}\det M\), hence degree \(+1\) or \(-1\).
This contradicts the topological fact proved above.  Therefore the
assumed global absence of a zero is impossible, and (126) follows.
\(\square\)

### Corollary 19.2 (balanced local line)

Let
\[
U:\mathbb C^2\longrightarrow\mathbb C^3\otimes\mathcal R
\]
be an isometry.  There are a unit qutrit vector \(x\) and a scalar
\(0\leq r\leq1\) such that
\[
\boxed{\qquad
U^\dagger(|x\rangle\langle x|\otimes I_{\mathcal R})U
=rI_2.
\qquad}
\tag{132}
\]

#### Proof

For a unit \(x\), put
\[
M(x)=U^\dagger(|x\rangle\langle x|\otimes I)U.
\]
For \(a=1,2,3\), the logical Pauli coefficient
\[
m_a(x)=\frac12\operatorname{Tr}[\sigma_aM(x)]
\]
is a real Hermitian quadratic form in \(x\), say
\(m_a(x)=\langle x,A_ax\rangle\).  If
\((e_1,e_2,e_3)\) is any orthonormal qutrit basis, then
\[
\operatorname{Tr}A_a
=\sum_i m_a(e_i)
=\frac12\operatorname{Tr}\!\left[
\sigma_aU^\dagger(I\otimes I)U\right]
=\frac12\operatorname{Tr}\sigma_a=0.
\]
Lemma 19.1 gives an \(x\) for which all three nonidentity Pauli
coefficients vanish.  Hence \(M(x)=rI_2\).  Positivity of \(M(x)\) and
\(M(x)\leq I_2\) give \(0\leq r\leq1\). \(\square\)

If \(0<r<1\), put \(Q=|x\rangle\langle x|\), \(P_x=I-Q\), and
\[
U_Q=\frac{(Q\otimes I)U}{\sqrt r},\qquad
U_P=\frac{(P_x\otimes I)U}{\sqrt{1-r}}.
\tag{133}
\]
Both maps are isometries.  Thus the line branch and its orthogonal
two-plane branch are genuine equal-spectrum rank-two codes.  The cases
\(r=1\) and \(r=0\) say respectively that the original code already
has local support one or at most two.

### Proposition 19.3 (exact balanced critical-point interpolation)

Let \(P_C=UU^\dagger\) be a rank-two code projection on four qutrits,
and let
\[
F(P_C)=\langle P_C,\mathcal L^{\otimes4}(P_C)\rangle.
\tag{134}
\]
Choose a balanced line as in (132), write \(a=1-r\), and assume
\(0<r<1\).  Let
\[
P_0=U_PU_P^\dagger,\qquad P_\infty=U_QU_Q^\dagger,
\]
so \(P_0\) has local support at most two and \(P_\infty\) has local
support one.  For \(t\geq0\), set
\[
E_t=P_x+tQ,\qquad
g(t)=a+rt,
\]
\[
P(t)=\frac{E_t^{1/2}P_CE_t^{1/2}}{g(t)}.
\tag{135}
\]
Then every \(P(t)\) is a rank-two projection, with
\(P(1)=P_C\), \(P(0)=P_0\), and
\(\lim_{t\to\infty}P(t)=P_\infty\).  There is a real number \(\zeta\)
such that
\[
\boxed{\quad
F(P(t))
=\frac{a^2F(P_0)+2t\zeta+r^2t^2F(P_\infty)}
       {(a+rt)^2}.
\quad}
\tag{136}
\]
If \(P_C\) is a critical point of \(F\) on the rank-two
Grassmannian, then
\[
\boxed{\quad
a^2F(P_0)-r^2F(P_\infty)=(a-r)F(P_C),
\quad}
\tag{137}
\]
and, more sharply,
\[
\boxed{\quad
F(P(t))
=F(P_C)
+\frac{\kappa(t-1)^2}{(a+rt)^2},
\qquad
\kappa
=r^2\!\left(F(P_\infty)-F(P_C)\right)
=a^2\!\left(F(P_0)-F(P_C)\right).
\quad}
\tag{138}
\]

#### Proof

Equation (132) gives
\[
U^\dagger(E_t\otimes I)U=(a+rt)I_2.
\]
Hence the numerator in (135) is \(g(t)\) times an orthogonal
rank-two projection, proving the first assertions.

The endpoint form is quadratic in the filtered effect, by (113).
At \(t=0\), the unnormalized filtered operator is \(aP_0\); its
quadratic value is \(a^2F(P_0)\).  The coefficient of \(t^2\) is
similarly \(r^2F(P_\infty)\).  Polarization supplies the real cross
coefficient \(2\zeta\), proving (136).

At a Grassmann critical point, the derivative of \(F(P(t))\) at
\(t=1\) vanishes.  Since \(g(1)=1\) and the numerator of (136) equals
\(F(P_C)\) at \(t=1\), differentiation gives
\[
\zeta+r^2F(P_\infty)=rF(P_C).
\tag{139}
\]
Combining (139) with the value at \(t=1\) gives (137).
Finally, subtract \(F(P_C)g(t)^2\) from the numerator in (136).
The resulting quadratic has a double zero at \(t=1\), so it is
\(\kappa(t-1)^2\).  Comparing its leading and constant coefficients
gives both expressions for \(\kappa\) in (138). \(\square\)

The rank-one branch satisfies
\[
F(P_\infty)=\frac12
\left\langle P_{\rm rem},
\mathcal L^{\otimes3}(P_{\rm rem})\right\rangle\geq0
\tag{140}
\]
by the exact three-copy projection theorem.  (Here \(P_{\rm rem}\) is
the rank-two projection after deleting the pure local line.)  Thus a
negative critical point has \(\kappa>0\): it is a strict minimum along
every nontrivial balanced interpolation.  This does not yet exclude
such a critical point, because the two-plane endpoint \(F(P_0)\) may
be nonnegative while the rational curve dips below zero in its
interior.  What (138) supplies is a finite exact reduction of the
critical-point problem: every full-qutrit local support admits two
honest lower-support code endpoints, and their values must obey the
rigid secant identity (137).

### Corollary 19.4 (finite projection-preserving compression chain)

For every isometry
\[
U:\mathbb C^2\longrightarrow
\bigotimes_{i=1}^4\mathbb C^3
\]
there are local orthogonal projectors \(E_i\) of rank at most two and
a scalar \(\lambda>0\) such that
\[
\boxed{\qquad
U^\dagger(E_1\otimes E_2\otimes E_3\otimes E_4)U
=\lambda I_2.
\qquad}
\tag{141}
\]
Consequently
\[
\widetilde U
=\lambda^{-1/2}
(E_1\otimes E_2\otimes E_3\otimes E_4)U
\tag{142}
\]
is an isometry whose physical support is a tensor product of local
spaces of dimension at most two.

#### Proof

Start with \(U^{(0)}=U\).  Apply Corollary 19.2 at the first site.
If its scalar is \(0\), retain the rank-two complementary projector;
if it is \(1\), retain any rank-two projector containing the balanced
line; and if it lies strictly between \(0\) and \(1\), retain either
the line or its rank-two complement.  In every case one obtains a
local projector \(E_1\) of rank at most two and a number \(c_1>0\)
such that
\[
(U^{(0)})^\dagger E_1U^{(0)}=c_1I_2.
\]
Set \(U^{(1)}=E_1U^{(0)}/\sqrt{c_1}\).  This is an isometry.

Repeat at sites \(2,3,4\).  Later projectors commute with all earlier
ones and do not enlarge their supports.  After four steps,
\[
U^{(k)}
=\left(\prod_{i=1}^kc_i\right)^{-1/2}
\left(\prod_{i=1}^kE_i\right)U
\]
is an isometry.  Taking \(k=4\) proves (141)--(142), with
\(\lambda=\prod_ic_i>0\). \(\square\)

Corollary 19.4 removes a geometric obstruction completely: a
projection-preserving route from every qutrit code to the common
local-qubit boundary always exists in four finite steps.  What is
still missing is a sign monotonicity theorem along such a chain.
Proposition 19.3 shows that even at a negative critical point the
first balanced step may rise to a nonnegative endpoint, so
projection preservation alone does not supply that monotonicity.

### Proposition 19.5 (no balanced orthonormal basis)

Lemma 19.1 cannot be strengthened from one balanced line to an
orthonormal balanced basis.  In fact, there are three traceless
Hermitian qutrit operators for which no two common-zero vectors are
orthogonal.

Take
\[
A_1=
\begin{pmatrix}0&1&0\\1&0&0\\0&0&0\end{pmatrix},\qquad
A_2=
\begin{pmatrix}0&-i&0\\i&0&0\\0&0&0\end{pmatrix},\qquad
A_3=\operatorname{diag}(2,-1,-1).
\tag{143}
\]
For a unit vector \(x=(x_1,x_2,x_3)\), the first two zero conditions
are equivalent to
\[
\overline{x_1}x_2=0.
\]
The third, together with normalization, is
\[
2|x_1|^2-|x_2|^2-|x_3|^2=0
\quad\Longleftrightarrow\quad
|x_1|^2=\frac13.
\]
Thus every common zero has the form
\[
x=\frac{e^{i\alpha}}{\sqrt3}e_1
+\sqrt{\frac23}\,e^{i\beta}e_3.
\tag{144}
\]
For any two such vectors \(x,y\), the two terms in their inner product
have magnitudes \(1/3\) and \(2/3\).  The reverse triangle inequality
therefore gives
\[
\boxed{\qquad |\langle x,y\rangle|\geq\frac13.\qquad}
\tag{145}
\]
There is no orthogonal common-zero pair.

This example also pinpoints why a tempting strengthening of the
extreme-point argument in Lemma 19.1 fails.  The density matrix
\[
\rho=\operatorname{diag}\left(\frac13,\frac23,0\right)
\tag{146}
\]
obeys \(\operatorname{Tr}(\rho A_j)=0\) for all three \(j\), and is an
extreme point of the feasible set (127).  Indeed, any Hermitian
perturbation \(D\) for which both \(\rho+\epsilon D\) and
\(\rho-\epsilon D\) remain positive must be supported on
\(\operatorname{span}\{e_1,e_2\}\).  On that support the restrictions
of \(I,A_1,A_2,A_3\) span all Hermitian \(2\times2\) matrices, so the
four homogeneous feasible-perturbation equations force \(D=0\).
None of the pure zeros (144) lies in the support of \(\rho\).
Consequently the feasible set can have genuine rank-two extreme
points and need not be the convex hull of its pure common zeros.

Nor is (143) an artifact of allowing arbitrary triples which cannot
come from a code.  Put
\[
J=\frac13I_3\otimes I_2
+\frac1{24}\sum_{a=1}^3A_a^T\otimes\sigma_a.
\tag{147}
\]
Since
\[
\left\|\sum_aA_a^T\otimes\sigma_a\right\|
\leq\sum_a\|A_a\|=4,
\]
one has \(J\succeq I/6\).  Also
\(\operatorname{Tr}_{\mathbb C^3}J=I_2\).  Factor \(J=T^\dagger T\)
and define
\[
V_i z=T(e_i\otimes z),\qquad
U z=\sum_i e_i\otimes V_i z.
\]
Then \(\sum_iV_i^\dagger V_i=I_2\), so \(U\) is an isometry.  Direct
block contraction gives
\[
U^\dagger(|x\rangle\langle x|\otimes I)U
=\frac13I_2
+\frac1{24}\sum_a\langle x,A_ax\rangle\sigma_a.
\tag{148}
\]
Hence this genuine code has precisely the balanced lines (144), every
one with \(r=1/3\), and no two of them are orthogonal.  The environment
used in the factorization has dimension at most six and therefore
embeds in the other three qutrits of the four-copy problem.

## 20. Finite algebraic separator for a minimal negative projection

Checkpoint: 2026-07-28 17:41 PDT.

The balanced-line theorem gives a precise nonlinear necessary
condition for any negative counterexample of minimal local-support
complexity.

For \(0\leq k\leq4\), let \(\mathcal C_k\) be the set of rank-two
projections for which at least \(4-k\) physical one-site supports have
dimension at most two.  These are compact sets: a one-site support has
dimension at most two exactly when all its \(3\times3\) maximal minors
vanish, and \(\mathcal C_k\) is a finite union of intersections of
such closed conditions.  The common-local-qubit theorem gives
\[
\min_{P\in\mathcal C_0}F(P)\geq0.
\tag{149}
\]

Suppose a negative projection exists.  Choose the least \(k\geq1\)
for which
\[
m_k:=\min_{P\in\mathcal C_k}F(P)<0,
\tag{150}
\]
and let \(P_C=UU^\dagger\) attain this minimum.  It has exactly \(k\)
full qutrit supports.  Fix one of them, say \(\ell\).

For a unit vector \(x\) at \(\ell\), define the logical compression
\[
M_\ell(x)
=U^\dagger(|x\rangle\langle x|_\ell\otimes I)U.
\tag{151}
\]
Its balanced zero variety is
\[
\mathcal Z_\ell
=\{[x]\in\mathbb {CP}^2:M_\ell(x)=r_\ell(x)I_2\}.
\tag{152}
\]
Corollary 19.2 says that \(\mathcal Z_\ell\ne\varnothing\).  In
coordinates, if
\[
\frac12\operatorname{Tr}[\sigma_aM_\ell(x)]
=\langle x,A_{\ell,a}x\rangle,
\]
then
\[
\mathcal Z_\ell
=\{[x]:\langle x,A_{\ell,a}x\rangle=0,\ a=1,2,3\}.
\tag{153}
\]
It is therefore a finite system of three explicit Hermitian quadratic
equations.  Since the local support is full,
\[
0<r_\ell(x)<1\qquad(x\in\mathcal Z_\ell).
\tag{154}
\]

Put \(Q_x=|x\rangle\langle x|\), \(P_x=I-Q_x\), and define the two
unnormalized endpoint polynomials
\[
\begin{aligned}
D_\ell(x)
&=F\bigl((Q_x\otimes I)P_C(Q_x\otimes I)\bigr),\\
C_\ell(x)
&=F\bigl((P_x\otimes I)P_C(P_x\otimes I)\bigr).
\end{aligned}
\tag{155}
\]
On the unit sphere both are polynomials of bidegree at most
\((2,2)\) in \(x,\overline x\); they may be homogenized by replacing
\(I\) in \(P_x\) with \(\|x\|^2I\).
On \(\mathcal Z_\ell\), they are
\[
D_\ell(x)=r_\ell(x)^2F(P_\infty(x)),\qquad
C_\ell(x)=(1-r_\ell(x))^2F(P_0(x)).
\tag{156}
\]
The two endpoint projections belong to \(\mathcal C_{k-1}\), so
minimality of \(k\) gives
\[
C_\ell(x)\geq0,\qquad D_\ell(x)\geq0.
\tag{157}
\]

For \(t\) near \(1\), the balanced path (135) remains in
\(\mathcal C_k\).  Since \(P_C\) minimizes \(F\) there, its derivative
at \(t=1\) vanishes.  Proposition 19.3 therefore gives the pointwise
identity
\[
\boxed{\qquad
C_\ell(x)-D_\ell(x)
=\bigl(1-2r_\ell(x)\bigr)m_k,
\qquad x\in\mathcal Z_\ell.
\qquad}
\tag{158}
\]

Write \(s=-m_k>0\).  Equations (157)--(158) imply the exact nonlinear
separator
\[
\boxed{\quad
D_\ell(x)
\geq s\bigl(1-2r_\ell(x)\bigr)
\quad\text{for every }x\in\mathcal Z_\ell
\text{ with }r_\ell(x)<\frac12.
\quad}
\tag{159}
\]
Conversely, if a balanced \(x\) violates (159), then
\[
C_\ell(x)
=D_\ell(x)-s(1-2r_\ell(x))<0,
\]
and the normalized plane branch \(P_0(x)\) is an explicit negative
rank-two projection in \(\mathcal C_{k-1}\), contradicting the choice
of \(k\).

There is a simple universal upper bound on the left side.  The line
branch factors off one pure physical site, so
\[
D_\ell(x)
=\frac{r_\ell(x)^2}{2}F_3(P_{\rm rem}(x)).
\]
The Hilbert--Schmidt operator norm of
\(\mathcal L^{\otimes3}\) is one and
\(\|P_{\rm rem}\|_2^2=2\).  Together with the three-copy theorem this
gives
\[
0\leq D_\ell(x)\leq r_\ell(x)^2.
\tag{160}
\]
Hence every minimal negative projection must also satisfy
\[
\boxed{\quad
s\leq
\frac{r_\ell(x)^2}{1-2r_\ell(x)}
\quad
\left(x\in\mathcal Z_\ell,
0<r_\ell(x)<\frac12\right).
\quad}
\tag{161}
\]

Define the finite-dimensional algebraic threshold
\[
\eta_\ell(P_C)
=\inf_{\substack{x\in\mathcal Z_\ell\\r_\ell(x)<1/2}}
\frac{D_\ell(x)}{1-2r_\ell(x)},
\tag{162}
\]
with the infimum \(+\infty\) if the displayed set is empty.  A
minimal-support negative minimizer must obey
\[
\boxed{\qquad -F(P_C)\leq\eta_\ell(P_C)\qquad}
\tag{163}
\]
at every full qutrit site.  All data in (162) are explicit quadratic
or biquadratic polynomials in one qutrit vector.  Thus the remaining
sign-descent question at \(n=4\) has been reduced to polynomial
nonnegativity on four real algebraic curves (one per full site), not
to aggregate sector arithmetic.

Equations (159)--(163) do not yet exclude a negative minimizer.  The
counterexample (147)--(148) shows why a universal averaging shortcut
is unavailable: a code-induced balanced variety can contain no
orthogonal pair and can have constant \(r\).  A completion now needs a
relation between the endpoint quartic \(D_\ell\) and the common
four-site origin of the four balanced varieties.

### Proposition 20.1 (five-dimensional balanced-kernel Hessian)

The whole linear space behind the balanced variety gives a stronger
finite criterion.  At a full qutrit site \(\ell\), define
\[
\mathcal K_\ell
=\left\{
A=A^\dagger\in M_3:
U^\dagger(A_\ell\otimes I)U=0
\right\}.
\tag{164}
\]
The map from \(9\)-dimensional Hermitian qutrit matrices to
\(4\)-dimensional Hermitian logical matrices has kernel dimension at
least five, so
\[
\dim_{\mathbb R}\mathcal K_\ell\geq5.
\tag{165}
\]
Define on this kernel the exact quadratic form
\[
\mathcal N_\ell(A)
=\operatorname{Tr}\!\left[
(P_C\otimes P_C)(A\otimes A)_\ell K_4
\right].
\tag{166}
\]
For the minimal negative projection in (150), with \(s=-m_k>0\),
\[
\boxed{\qquad
\mathcal N_\ell(A)\geq s\|A\|_{\rm op}^2
\qquad(A\in\mathcal K_\ell).
\qquad}
\tag{167}
\]
In particular,
\[
\boxed{\qquad
\mathcal N_\ell(A)\geq\frac{s}{3}\|A\|_2^2,
\qquad
\mathcal N_\ell|_{\mathcal K_\ell}
\succeq\frac{s}{3}I_{\mathcal K_\ell}.
\qquad}
\tag{168}
\]

#### Proof

For \(A\in\mathcal K_\ell\), set \(E_t=I+tA\).  Whenever
\(E_t\succeq0\),
\[
U^\dagger(E_t\otimes I)U=I_2.
\]
Hence
\[
U_t=E_t^{1/2}U
\]
is already an isometry, without any logical whitening.  The endpoint
form is exactly quadratic in the effect:
\[
F(U_tU_t^\dagger)
=m_k+2t\,b_\ell(A)+t^2\mathcal N_\ell(A).
\tag{169}
\]
For sufficiently small positive and negative \(t\), this path remains
in \(\mathcal C_k\).  Minimality at \(t=0\) gives
\(b_\ell(A)=0\).

If \(A\ne0\), it is indefinite.  Indeed, the full local support makes
\(\operatorname{Tr}_{\bar\ell}P_C\) positive definite, while
\[
\operatorname{Tr}\!\left[
A\,\operatorname{Tr}_{\bar\ell}P_C\right]
=\operatorname{Tr}[U^\dagger(A_\ell\otimes I)U]=0;
\]
a nonzero semidefinite \(A\) could not have zero pairing with that
positive definite matrix.  Choose the sign of \(t_*\) so that
\[
|t_*|=\|A\|_{\rm op}^{-1},
\qquad E_{t_*}\succeq0,\qquad
\operatorname{rank}E_{t_*}\leq2.
\]
Then \(U_{t_*}U_{t_*}^\dagger\in\mathcal C_{k-1}\), and hence its
endpoint value is nonnegative.  Equation (169) gives
\[
0\leq-s+t_*^2\mathcal N_\ell(A),
\]
which is (167).  Finally,
\(\|A\|_{\rm op}^2\geq\|A\|_2^2/3\), proving (168).
\(\square\)

For a balanced rank-one projector \(Q_x\), the centered observable
\[
A_x=Q_x-r_\ell(x)I
\tag{170}
\]
belongs to \(\mathcal K_\ell\).  Its operator norm is
\(\max\{r_\ell(x),1-r_\ell(x)\}\), and direct expansion at the critical
point gives
\[
\mathcal N_\ell(A_x)
=D_\ell(x)+s\,r_\ell(x)^2.
\tag{171}
\]
When \(r_\ell(x)<1/2\), substituting (170)--(171) into (167) recovers
exactly (159).  Thus the algebraic-curve separator is the rank-one
boundary of the stronger five-dimensional Hessian condition.

Equivalently, if \(\lambda_{\min}^{(\ell)}\) denotes the least
Hilbert--Schmidt eigenvalue of the real symmetric quadratic form
\(\mathcal N_\ell\) restricted to \(\mathcal K_\ell\), then every
minimal negative projection must satisfy
\[
\boxed{\qquad
\lambda_{\min}^{(\ell)}>0,\qquad
-F(P_C)\leq3\lambda_{\min}^{(\ell)}
\qquad}
\tag{172}
\]
at each full qutrit site.  The matrices defining
\(\mathcal K_\ell\) and \(\mathcal N_\ell\) are finite contractions of
the two code tensors.  Therefore (172) is an exact finite
critical-point test: finding one nonpositive kernel eigenvalue at a
putative negative minimizer produces a sign-descending singular
filter and rules it out.

### Proposition 20.2 (basis-free restricted trace and determinant)

Polarize (166) to the real symmetric bilinear form
\[
\mathcal N_\ell(A,B)
=\operatorname{Tr}\!\left[
(P_C\otimes P_C)(A\otimes B)_\ell K_4
\right].
\tag{173}
\]
The expression is symmetric on Hermitian \(A,B\), by conjugating with
the global replica swap.  Choose Hilbert--Schmidt orthonormal Hermitian
bases \((\tau_\mu)_{\mu=1}^9\) of \(M_3\) and
\((\gamma_a)_{a=1}^4\) of \(M_2\), and put
\[
\begin{aligned}
H_{\mu\nu}&=\mathcal N_\ell(\tau_\mu,\tau_\nu),\\
C_{a\mu}
&=\operatorname{Tr}\!\left[
\gamma_aU^\dagger(\tau_\mu{}_\ell\otimes I)U
\right],\\
G&=CC^{\mathsf T},\qquad M=CHC^{\mathsf T}.
\end{aligned}
\tag{174}
\]
Then the orthogonal projector onto \(\mathcal K_\ell\) is
\[
\Pi_{\mathcal K}
=I_9-C^{\mathsf T}G^+C,
\tag{175}
\]
where \(G^+\) is the Moore--Penrose inverse.  Consequently
\[
\boxed{\quad
\operatorname{tr}(H|_{\mathcal K_\ell})
=\frac34h_\ell-\frac12F(P_C)
-\operatorname{tr}(G^+M),
\quad}
\tag{176}
\]
where
\[
h_\ell
=\operatorname{Tr}\!\left[
(P_C\otimes P_C)K_{\bar\ell}\right],
\qquad
K_{\bar\ell}
=\prod_{i\ne\ell}\left(F_i-\frac12I\right).
\tag{177}
\]
If \(C\) has full row rank four and \(Q\) is any
Hilbert--Schmidt orthonormal basis matrix for \(\ker C\), then
\[
\boxed{\quad
\det(Q^{\mathsf T}HQ)
=
\frac{
\det\begin{pmatrix}H&C^{\mathsf T}\\ C&0\end{pmatrix}}
{\det(CC^{\mathsf T})}.
\quad}
\tag{178}
\]

#### Proof

The row space of \(C\) is the orthogonal complement of its kernel.
The standard range projector is
\(C^{\mathsf T}(CC^{\mathsf T})^+C\), proving (175).  Therefore
\[
\operatorname{tr}(H|_{\mathcal K_\ell})
=\operatorname{tr}(H\Pi_{\mathcal K})
=\operatorname{tr}H-\operatorname{tr}(G^+M).
\tag{179}
\]
Completeness of a Hermitian Hilbert--Schmidt basis gives
\[
\sum_{\mu=1}^9\tau_\mu\otimes\tau_\mu=F_\ell.
\]
Writing
\[
j_\ell
=\operatorname{Tr}[(P_C\otimes P_C)F_\ell K_{\bar\ell}],
\]
one obtains
\[
\begin{aligned}
\operatorname{tr}H
&=\operatorname{Tr}\!\left[
(P_C\otimes P_C)
F_\ell\left(F_\ell-\frac12I\right)K_{\bar\ell}
\right]\\
&=h_\ell-\frac12j_\ell.
\end{aligned}
\]
Since \(F(P_C)=j_\ell-h_\ell/2\), this is
\(\operatorname{tr}H=3h_\ell/4-F(P_C)/2\), proving (176).

For (178), complete \(Q\) to an orthogonal matrix \((Q,R)\).
Then \(C(Q,R)=(0,D)\), where \(D\) is invertible and
\(\det(D)^2=\det(CC^{\mathsf T})\).  In these coordinates the bordered
matrix in (178) is
\[
\begin{pmatrix}
Q^{\mathsf T}HQ&Q^{\mathsf T}HR&0\\
R^{\mathsf T}HQ&R^{\mathsf T}HR&D^{\mathsf T}\\
0&D&0
\end{pmatrix}.
\]
Taking the Schur complement of the upper-left block, first when it is
invertible and then by polynomial continuity, gives
\(\det(Q^{\mathsf T}HQ)\det(D)^2\).  This is (178).
\(\square\)

Neither the trace nor the determinant in Proposition 20.2 has a
universal sign.  Here are exact sparse obstructions, included to prevent
those scalar routes from being retried.

At site one, take
\[
\begin{aligned}
u&=\frac{|1001\rangle+|1022\rangle+2|2202\rangle}{\sqrt6},\\
v&=\frac{2|0022\rangle+|0220\rangle}{\sqrt5},
\qquad P=|u\rangle\langle u|+|v\rangle\langle v|.
\end{aligned}
\tag{180}
\]
The local support is three-dimensional and \(C\) has rank four.  Direct
exact contraction gives
\[
F(P)=\frac{121}{450},
\qquad
\operatorname{spec}(H|_{\mathcal K_1})
=\left\{
-\frac1{18},-\frac1{36},-\frac1{36},
\frac1{12},\frac1{12}
\right\}.
\tag{181}
\]
Thus
\[
\operatorname{tr}(H|_{\mathcal K_1})
=\frac1{18}
>\frac18F(P).
\tag{182}
\]
In the local Hermitian basis consisting of the three diagonal matrix
units followed by normalized \(X_{ij},Y_{ij}\), an orthonormal kernel
basis is
\[
\frac{\operatorname{diag}(0,-2,1)}{\sqrt5},
\quad X_{02},Y_{02},X_{12},Y_{12}.
\]
In this basis the restriction is already diagonal with the entries in
(181), so (181) is independently checkable without an eigensolver.

Even the sign of the restricted determinant fails.  Take
\[
\begin{aligned}
u&=\frac{-i|1212\rangle+|0010\rangle}{\sqrt2},\\
v&=\frac{
i|2212\rangle+(-1+i)|0111\rangle+(1-i)|1111\rangle}{\sqrt5}.
\end{aligned}
\tag{183}
\]
Again the first-site support is full and \(\operatorname{rank}C=4\), but
\[
F(P)=\frac{163}{400},
\quad
\operatorname{spec}(H|_{\mathcal K_1})
=\left\{
-\frac7{160},-\frac{59}{2400},
\frac1{400},\frac1{400},\frac3{160}
\right\}.
\tag{184}
\]
An orthonormal kernel basis in the same convention as above is
\[
\frac{\operatorname{diag}(1,-1,0)}{\sqrt2},\quad
\frac{2\sqrt2\,\operatorname{diag}(0,0,1)+X_{01}}3,\quad
Y_{01},\quad X_{02},\quad Y_{02}.
\]
The restriction is diagonal in this basis, in the order
\[
-\frac7{160},\quad-\frac{59}{2400},\quad
\frac3{160},\quad\frac1{400},\quad\frac1{400}.
\]
The determinant in (184) is positive although the restriction is
indefinite.  The robust statement suggested by every exact and numerical
audit is therefore the genuinely spectral assertion
\[
\lambda_{\min}(H|_{\mathcal K_\ell})\leq0,
\tag{185}
\]
not a trace or determinant inequality.  Equation (185) remains
unproved.  The standard-library script
`verification/verify_effect_kernel_obstructions.py` independently
reconstructs both sparse projections with rational Gaussian arithmetic
and checks (181)--(184) entry by entry.

### Lemma 20.3 (rank-deficient compression has a balanced basis)

Let
\[
T_\ell:\operatorname{Herm}(3)\longrightarrow\operatorname{Herm}(2),
\qquad
T_\ell(A)=U^\dagger(A_\ell\otimes I)U.
\tag{186}
\]
If \(\operatorname{rank}_{\mathbb R}T_\ell\leq3\), there is an
orthonormal qutrit basis \(x_1,x_2,x_3\) and numbers \(r_i\geq0\) such
that
\[
\boxed{\qquad
T_\ell(|x_i\rangle\langle x_i|)=r_iI_2,
\qquad
r_1+r_2+r_3=1.
\qquad}
\tag{187}
\]
If the local support of \(P_C\) is full, then every \(r_i>0\).

#### Proof

Because \(T_\ell(I_3)=I_2\), the traceless part of its range has real
dimension at most two.  Thus there are at most two linearly independent
traceless Hermitian qutrit matrices \(A_1,A_2\) whose quadratic
expectations are the nonidentity logical coefficients of
\(T_\ell(|x\rangle\langle x|)\).

Lemma 19.1 gives a unit vector \(x_1\) with
\(\langle x_1,A_ax_1\rangle=0\) for both \(a\).  Compress the \(A_a\)'s
to \(x_1^\perp\).  The two resulting \(2\times2\) matrices are traceless:
their traces are
\(\operatorname{Tr}A_a-\langle x_1,A_ax_1\rangle=0\).
Represent them by two Bloch vectors.  A unit Bloch vector perpendicular
to both gives a unit \(x_2\in x_1^\perp\) with both expectations zero.
Its orthogonal companion \(x_3\) has the opposite Bloch vector, hence
also has both expectations zero.  All three logical compressions are
therefore scalar.

Summing their rank-one projectors gives \(I_3\), so summing the three
compressions gives \(I_2\), proving \(\sum_i r_i=1\).  If the local
support is full, its reduced matrix is positive definite; hence no
nonzero local line has zero code weight, and every \(r_i>0\).
\(\square\)

Thus the failed balanced-orthonormal-basis shortcut of Proposition 19.5
becomes valid precisely throughout the rank-deficient-compression
stratum.  For a minimal negative projection, all diagonal effects in
this basis have scalar logical compression.  Their endpoint values form
a \(3\times3\) real quadratic form which is nonnegative on every
coordinate face and has the negative value \(m_k\) at \((1,1,1)\).
Abstract quadratic forms with these properties exist, so this
face-copositivity statement alone is not yet a contradiction.

### Proposition 20.4 (rank-one point in the complex kernel)

Complexify (164):
\[
\mathcal K_\ell^{\mathbb C}
=\left\{
Z\in M_3(\mathbb C):
U^\dagger(Z_\ell\otimes I)U=0
\right\}.
\tag{188}
\]
Then \(\dim_{\mathbb C}\mathcal K_\ell^{\mathbb C}\geq5\), and there
are nonzero qutrit vectors \(x,y\) such that
\[
Z=|x\rangle\langle y|\in\mathcal K_\ell^{\mathbb C}.
\tag{189}
\]
Write
\[
A=\frac{Z+Z^\dagger}{2},
\qquad
B=\frac{Z-Z^\dagger}{2i}.
\tag{190}
\]
Then \(A,B\in\mathcal K_\ell\).  With
\[
V_x=(\langle x|_\ell\otimes I)U,\qquad
V_y=(\langle y|_\ell\otimes I)U,
\tag{191}
\]
one has
\[
V_x^\dagger V_y=0.
\tag{192}
\]
Let
\[
H_x=V_xV_x^\dagger,\quad H_y=V_yV_y^\dagger,\quad
B_{xy}=V_yV_x^\dagger,
\qquad \Phi_3=\mathcal L^{\otimes3}.
\tag{193}
\]
The exact paired Hessian value is
\[
\boxed{\quad
\mathcal N_\ell(A)+\mathcal N_\ell(B)
=\operatorname{Tr}[H_x\Phi_3(H_y)]
-\frac12\operatorname{Tr}
\!\left[B_{xy}\Phi_3(B_{xy}^\dagger)\right].
\quad}
\tag{194}
\]
Moreover \(H_xH_y=0\) and \(B_{xy}^2=0\).

#### Proof

The complex kernel has codimension at most four in the
nine-dimensional complex matrix space.  The projectivized rank-one
matrices form
\[
\{[xy^{\mathsf T}]:[x],[y]\in\mathbb {CP}^2\}
\subset\mathbb {CP}^8,
\]
of complex dimension four, while
\(\mathbb P(\mathcal K_\ell^{\mathbb C})\) has dimension at least four.
These two projective sets intersect.  For completeness, the elementary
dimension fact used here follows by passing to their affine cones:
the product of cones has dimension at least \(5+5=10\), and the nine
linear equations equating their two ambient \(M_3\) coordinates leave
dimension at least one.  The origin is zero-dimensional, so the
intersection contains a nonzero point.  This proves (189).

The kernel is closed under adjoint.  Hence (190) gives Hermitian
members of the real kernel.  Equation (192) is simply
\[
U^\dagger(|x\rangle\langle y|_\ell\otimes I)U
=V_x^\dagger V_y=0.
\]

Extend the real polarization (173) complex bilinearly.  Since
\(Z=A+iB\) and \(Z^\dagger=A-iB\),
\[
\mathcal N_\ell(Z,Z^\dagger)
=\mathcal N_\ell(A)+\mathcal N_\ell(B).
\tag{195}
\]
On the two local replicas,
\[
(Z\otimes Z^\dagger)F_\ell
=|x\rangle\langle x|\otimes|y\rangle\langle y|.
\tag{196}
\]
The swapped part of \(K_4\) therefore contracts to
\(\operatorname{Tr}[H_x\Phi_3(H_y)]\).  For the identity part,
\[
\operatorname{Tr}_\ell(P_CZ)=V_yV_x^\dagger=B_{xy},
\qquad
\operatorname{Tr}_\ell(P_CZ^\dagger)=B_{xy}^\dagger.
\]
This proves (194).  Finally, (192) gives
\[
H_xH_y=V_x(V_x^\dagger V_y)V_y^\dagger=0,
\qquad
B_{xy}^2=V_y(V_x^\dagger V_y)V_x^\dagger=0.
\]
\(\square\)

For a full-rank compression, the projective intersection in the proof
is generically finite; its points all come from the same four logical
compression equations.  If one could prove that at least one such
point obeys
\[
\mathcal N_\ell(A)+\mathcal N_\ell(B)\leq0,
\tag{197}
\]
then (168) would immediately exclude a negative minimal projection.
Individual rank-one kernel points can have a positive value in (194),
so (197) must use the collection of common solutions, not one isolated
rank-one factor.  This is the remaining nonlinear realizability target
exposed by the kernel-Hessian method.

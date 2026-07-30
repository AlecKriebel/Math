# Final research dossier: closure of the two-setting qubit POVM–PVM dichotomy

## 0. Final outcome

**Outcome E1 is proved.** For every bipartite Bell scenario with two inputs per party and arbitrary finite output sets,

\[
\boxed{
\mathcal Q^{\mathrm{POVM}}_2(2,2)
=
\mathcal Q^{\mathrm{PVM}}_2(2,2).
}
\]

Both sides include arbitrary shared classical randomness. On the PVM side, zero projectors, deterministic relabelings, and stochastic postprocessing are allowed, but the local Hilbert spaces remain of dimension at most two.

Combined with the frozen exact \(3\times2\) separation, this gives the minimum-setting classification:

\[
\boxed{
\text{fixed-qubit POVM–PVM separation requires and is achieved by }3\times2
\text{ inputs, up to exchanging the parties.}
}
\]

The proof closes the only inherited residual architecture, namely one binary PVM and one genuine extremal ternary rank-one POVM on each party, with a pure entangled two-qubit state.

The closure mechanism has three parts.

1. A Lorentz-coordinate incidence model converts the residual pure-strategy set into five null equations in a \(4\times4\) probability block and a four-parameter local metric.
2. At every strict Bell maximizer, local duality produces five strictly positive determinant multipliers. If the metric-projection differential has rank at least two, its second fundamental form necessarily has an uphill direction.
3. The two exceptional ranks are exact and harmless: rank one cannot carry a strictly positive multiplier, while rank zero has an explicit deterministic local, hence PVM, decomposition.

No numerical observation is used in the theorem.

---

## 1. Frozen dependencies used

The proof uses the following results from the preceding frozen phases.

### D1. Exact \(3\times2\) separation

There is an explicit rational Bell functional with three inputs on one side and two on the other for which an exact qubit-POVM strategy exceeds a global analytic upper bound for all fixed-qubit PVM strategies.

### D2. One-binary-party theorem

With two inputs per party, if either party has binary outcomes on both inputs, every qubit-POVM behavior is in the convex hull of fixed-qubit PVM behaviors.

### D3. Residual architecture theorem

If a two-setting separator exists, a strictly maximizing component can be chosen with:

- a pure entangled two-qubit state;
- one nondegenerate binary PVM and one genuine extremal ternary rank-one POVM on Alice;
- one nondegenerate binary PVM and one genuine extremal ternary rank-one POVM on Bob;
- no four-outcome POVM.

The two local real operator spans intersect only in \(\mathbb RI\).

The present dossier proves that this residual architecture cannot strictly maximize any Bell functional above the fixed-qubit PVM value.

---

## 2. Finite-dimensional convex completion criterion

Let \(V\) be the finite-dimensional real affine space of behaviors for a fixed declared output architecture. Let \(\mathcal P\subset V\) be the convex hull of fixed-qubit PVM behaviors, and let \(\mathcal R\subset V\) be the closure of the residual pure-strategy behaviors.

These sets are compact. For fixed output counts, density matrices and POVM tuples form closed bounded subsets of finite-dimensional matrix spaces, hence compact sets; the Born map is continuous. The same is true for PVM tuples and finite stochastic postprocessings. Finally, the convex hull of a compact set in a real affine space of dimension \(m\) is compact: every convex combination of more than \(m+1\) points has affinely dependent support, so one can vary its coefficients along a nonzero affine dependence until one coefficient vanishes, and iterate. Thus every point of the convex hull is represented by at most \(m+1\) support points, making the convex hull the continuous image of a compact product of the original compact set and the closed probability simplex.

### Lemma 2.1. Elementary strict separation from a nearest point

If \(q\notin\mathcal P\), choose \(p_0\in\mathcal P\) minimizing \(\|q-p\|^2\). Then

\[
c=q-p_0
\]

satisfies

\[
c\cdot q>\sup_{p\in\mathcal P}c\cdot p.
\]

#### Proof

For any \(p\in\mathcal P\), the segment \(p_0+t(p-p_0)\) remains in \(\mathcal P\) for \(0\le t\le1\). The derivative at \(t=0\) of

\[
\|q-p_0-t(p-p_0)\|^2
\]

must be nonnegative. Therefore

\[
(q-p_0)\cdot(p-p_0)\le0.
\]

Thus \(c\cdot p\le c\cdot p_0<c\cdot q\). ∎

### Corollary 2.2. A strict full-POVM separator has a residual global maximizer

Let \(\mathcal Q\) be the compact convex set of all fixed-qubit POVM behaviors for the declared finite outputs. If \(\mathcal Q\not\subseteq\mathcal P\), Lemma 2.1 gives a linear functional \(c\) such that

\[
\max_{q\in\mathcal Q}c\cdot q>\max_{p\in\mathcal P}c\cdot p.
\]

The maximum over \(\mathcal Q\) is attained. Linearity removes shared randomness: at least one underlying strategy component attains the same value. Frozen dependency D3 then replaces a maximizing component, without lowering the value, by a strategy in the genuine residual architecture. Thus a failure of equality produces a **global** POVM maximizer in \(\mathcal R\) whose value is strictly above the PVM support value. In particular, each one-party measurement in that strategy is itself globally optimal when the state and the remaining measurements are fixed.

For the residual convex hull alone, the same nearest-point argument proves

\[
\operatorname{conv}(\mathcal R)\not\subseteq\mathcal P
\Longrightarrow
\max_{r\in\mathcal R}c\cdot r>\max_{p\in\mathcal P}c\cdot p
\]

for some \(c\). The full-POVM maximization and D3 are what additionally justify the local POVM dual conditions used below.

Consequently, it is enough to prove:

> No non-PVM residual strategy can be a global Bell maximizer strictly above the PVM support value.

The remaining proof establishes exactly this statement on every smooth and singular residual stratum.

---

## 3. Lorentz coordinates for qubit effects

Write every Hermitian \(2\times2\) matrix uniquely as

\[
X=x_0I+x_1\sigma_x+x_2\sigma_y+x_3\sigma_z.
\]

Associate the real vector

\[
x=(x_0,x_1,x_2,x_3)^T
\]

and the Lorentz matrix

\[
\eta=\operatorname{diag}(1,-1,-1,-1).
\]

Then

\[
\det X=x^T\eta x.
\]

Moreover, \(X\ge0\) precisely when \(x_0\ge0\) and \(x^T\eta x\ge0\). A nonzero positive rank-one operator corresponds to a future null vector:

\[
x_0>0,
\qquad
x^T\eta x=0.
\]

Two distinct future null rays have strictly positive Lorentz product. Indeed, write

\[
x=s(1,\mathbf n),
\qquad
y=t(1,\mathbf m),
\]

with \(s,t>0\) and unit vectors \(\mathbf n,\mathbf m\). Then

\[
x^T\eta y=st(1-\mathbf n\cdot\mathbf m)>0
\]

unless the rays coincide.

---

## 4. The five outcome rays and the local metric

For one party, label the two binary effects by \(E_1,E_2\), and the three ternary effects by \(E_3,E_4,E_5\). They satisfy

\[
E_1+E_2=E_3+E_4+E_5=I.
\]

Set

\[
r_1=e_1,
\quad r_2=e_2,
\quad r_3=e_3,
\quad r_4=e_4,
\quad r_5=v=(1,1,-1,-1)^T,
\]

where \(e_i\) are the standard coordinate vectors in \(\mathbb R^4\). Also set

\[
u=(1,1,0,0)^T.
\]

The relation is

\[
r_1+r_2=r_3+r_4+r_5=u.
\]

Because the binary span has dimension two, the ternary span has dimension three, and their intersection is exactly \(\mathbb RI\), the four effects \(E_1,E_2,E_3,E_4\) form a real basis of \(\operatorname{Herm}(2)\).

Let \(\mathsf E\) be the \(4\times4\) matrix whose columns are their Lorentz coordinate vectors. Define

\[
g=\mathsf E^T\eta\mathsf E.
\]

Then

\[
r_i^Tgr_i=0
\quad(i=1,\ldots,5),
\qquad
u^Tgu=1.
\]

Writing

\[
a=g_{13},\quad b=g_{14},\quad c=g_{23},\quad d=g_{24},
\]

these equations force

\[
\boxed{
g(a,b,c,d)=
\begin{pmatrix}
0&\tfrac12&a&b\\
\tfrac12&0&c&d\\
a&c&0&a+b+c+d-\tfrac12\\
b&d&a+b+c+d-\tfrac12&0
\end{pmatrix}.}
\]

Thus the local measurement pair is encoded, modulo local Lorentz/unitary gauge, by four real metric parameters.

Because all five effect rays are distinct on the genuine residual stratum, all ten off-diagonal products between distinct rays are strictly positive. In particular,

\[
\begin{aligned}
&a,b,c,d>0,\\
&e:=a+b+c+d-\tfrac12>0,\\
&a+b<\tfrac12,
\quad c+d<\tfrac12,
\quad a+c<\tfrac12,
\quad b+d<\tfrac12.
\end{aligned}
\]

These strict inequalities are used only in the exceptional-fiber analysis.

---

## 5. The \(4\times4\) probability block

Choose the first four effects on each party as bases. Let \(P\in M_4(\mathbb R)\) be the corresponding probability block. The full \(5\times5\) table is reconstructed by

\[
p_{ij}=r_i^TPr_j,
\qquad i,j=1,\ldots,5.
\]

All nonsignaling identities follow from

\[
r_1+r_2=r_3+r_4+r_5=u.
\]

Normalization is the one affine equation

\[
\boxed{u^TPu=1.}
\]

### Pure-state Lorentz relation

Write the pure state as

\[
|\psi_C\rangle=\sum_{m,n=0}^1C_{mn}|mn\rangle,
\qquad \det C\ne0.
\]

Define

\[
\Theta_C(N)=CN^TC^\dagger.
\]

Then

\[
\langle\psi_C|E\otimes N|\psi_C\rangle
=
\operatorname{Tr}(E\Theta_C(N)).
\]

Let \(L_C\) be the real \(4\times4\) matrix representing \(\Theta_C\) in Lorentz coordinates. Since

\[
\det(CN^TC^\dagger)=|\det C|^2\det N,
\]

polarization of the quadratic identity gives

\[
L_C^T\eta L_C=|\det C|^2\eta.
\]

If \(h\) is Bob's local metric, direct substitution yields

\[
\boxed{
P^Tg^{-1}P=4|\det C|^2h.
}
\]

In particular, \(P\) is invertible on the dense entangled residual stratum.

---

## 6. Incidence description of the residual strategy set

Set

\[
Q=g^{-1},
\qquad
x_j=Pr_j.
\]

The preceding Lorentz relation implies the five equations

\[
\boxed{
F_j(P,g):=x_j^TQx_j=0,
\qquad j=1,\ldots,5.
}
\]

Together with \(u^TPu=1\), these equations provide a local exact model of the residual behavior set.

### Lemma 6.1. Local physical completeness of the incidence equations

Near every genuine residual point, every nearby pair \((P,g)\) satisfying the five null equations, normalization, and strict time orientation is realized by a genuine two-qubit residual strategy. Positivity of the reconstructed probability table is a consequence, not an additional hypothesis.

#### Proof

First reconstruct Alice's effects from \(g\). The restriction of \(g\) to \(u^{\perp_g}\) is negative definite because \(g\) has signature \((1,3)\) and \(u^Tgu=1\). Choose a \(g\)-orthonormal basis \((u,w_1,w_2,w_3)\) and map it to the standard Minkowski basis. This gives a linear isometry \(\mathsf E\) with

\[
\mathsf E^T\eta\mathsf E=g,
\qquad \mathsf E u=(1,0,0,0)^T.
\]

The construction can be made smoothly near the original point by ordinary Gram–Schmidt on the negative-definite complement. Each \(r_i\) is \(g\)-null. Moreover \(g(u,r_i)>0\), because it is a sum of strictly positive products with the other rays in either measurement decomposition. Hence \(\mathsf E r_i\) is future null. These five vectors therefore represent positive rank-one effects and sum to the identity in both measurement partitions.

Let \(\mathsf E\) be the resulting effect-coordinate matrix. For each Bob outcome define the Hermitian coordinate vector

\[
s_j=\frac12\mathsf E^{-T}x_j.
\]

Then

\[
4s_j^T\eta s_j=x_j^Tg^{-1}x_j=0.
\]

Also,

\[
2(s_j)_0=u^Tx_j,
\]

which is the corresponding Bob outcome marginal. It is strictly positive at a genuine residual point and remains positive nearby. Thus each \(s_j\) is future null and represents a positive rank-one operator \(S_j\). The coefficient identity for the \(r_j\) gives

\[
S_1+S_2=S_3+S_4+S_5=:\rho_A.
\]

Normalization gives \(\operatorname{Tr}\rho_A=1\), and nearby full Schmidt rank gives \(\rho_A>0\). Choose \(C=\rho_A^{1/2}\), and define

\[
N_j^T=C^{-1}S_jC^{-\dagger}.
\]

These are positive rank-one effects. They sum to \(I\) on each measurement. The state \(|\psi_C\rangle\) is normalized. Moreover, for every pair of outcome rays,

\[
\operatorname{Tr}(E_iS_j)
=2(\mathsf E r_i)^Ts_j
=r_i^Tx_j
=r_i^TPr_j.
\]

Thus the Born probabilities are precisely the entries reconstructed from \(P\), and they are automatically nonnegative because \(E_i,S_j\ge0\). No separate probability-positivity assumption is required. ∎

Thus an increasing curve in the incidence manifold is a genuine physical increasing curve, not merely an algebraic relaxation.

### Lemma 6.2. Smoothness of the normalized incidence manifold

The five differentials \(dF_j\) are linearly independent with respect to the \(P\)-variables.

Indeed,

\[
\nabla_PF_j=2QPr_jr_j^T.
\]

If

\[
\sum_j\mu_j\nabla_PF_j=0,
\]

then, since \(QP\) is invertible,

\[
\Lambda_\mu:=\sum_j\mu_jr_jr_j^T=0.
\]

But

\[
\Lambda_\mu=
\operatorname{diag}(\mu_1,\mu_2,\mu_3,\mu_4)+\mu_5vv^T,
\]

whose off-diagonal entries force \(\mu_5=0\), and then whose diagonal entries force \(\mu_1=\cdots=\mu_4=0\).

The normalization differential is independent of the five null differentials because the radial variation \(\delta P=P\) annihilates all \(dF_j\) but changes \(u^TPu\). Therefore the normalized incidence set is a smooth real manifold of dimension

\[
16+4-5-1=14.
\]

This proves the previously observed dimension exactly, without numerical rank testing.

At a Bell stationary point, the objective differential annihilates the common kernel of the six independent constraint differentials. Elementary linear algebra therefore puts it in their row span. With a sign convention chosen for later dual positivity, there are unique real numbers \(\alpha,\lambda_1,\ldots,\lambda_5\) such that

\[
\boxed{
c-\alpha uu^T=-2QP\Lambda,
\qquad
\Lambda=\sum_j\lambda_jr_jr_j^T,
}
\]

and stationarity in the metric variables gives

\[
\boxed{\lambda\in\ker\mathcal D^T.}
\]

The next section proves that the chosen multipliers are strictly positive at any putative separator.

---

## 7. Strict Bell maxima have positive determinant multipliers

Fix all variables except one of Bob's measurements. Let \(K_j\) be the Hermitian score operator for outcome \(j\). The optimization is

\[
\max_{N_j\ge0,\ \sum_jN_j=I}
\sum_j\operatorname{Tr}(K_jN_j).
\]

### Lemma 7.1. Elementary dual certificate for a finite POVM optimization

At an optimum there is a Hermitian \(\Gamma\) such that

\[
\Gamma\ge K_j
\quad\text{for every }j,
\]

and

\[
(\Gamma-K_j)N_j=0.
\]

#### Proof

Weak duality is immediate:

\[
\sum_j\operatorname{Tr}(K_jN_j)
\le
\sum_j\operatorname{Tr}(\Gamma N_j)
=
\operatorname{Tr}\Gamma.
\]

Let \(V\) be the primal optimum. For \(\varepsilon>0\), consider the convex cone

\[
\mathcal C=
\left\{
\left(\sum_jX_j,
\sum_j\operatorname{Tr}(K_jX_j)-t\right):
X_j\ge0,
\ t\ge0
\right\}
\subset\operatorname{Herm}(2)\times\mathbb R.
\]

This cone is closed. Indeed, if its first components converge, then every \(X_j\) is bounded because \(0\le X_j\le\sum_kX_k\); a subsequence of every \(X_j\) converges, and the scalar equation then gives a nonnegative limiting \(t\).

The point \((I,V+\varepsilon)\) is not in \(\mathcal C\). By the nearest-point separation argument of Lemma 2.1, applied to the closed cone and this point, there is a nonzero real linear functional

\[
\ell(A,s)=\operatorname{Tr}(\Gamma A)+\gamma s
\]

with \(\ell\ge0\) on \(\mathcal C\) and \(\ell(I,V+\varepsilon)<0\). Since \((0,-t)\in\mathcal C\) for all \(t\ge0\), one has \(\gamma\le0\). If \(\gamma=0\), positivity on all \((X,\operatorname{Tr}(K_jX))\), \(X\ge0\), would give \(\Gamma\ge0\), contradicting \(\ell(I,V+\varepsilon)=\operatorname{Tr}\Gamma<0\). Thus \(\gamma<0\); normalize it to \(-1\).

Taking only one nonzero \(X_j=X\ge0\) gives

\[
\operatorname{Tr}((\Gamma-K_j)X)\ge0
\quad\text{for every }X\ge0,
\]

so \(\Gamma\ge K_j\). The strict separation inequality gives

\[
\operatorname{Tr}\Gamma<V+\varepsilon.
\]

Weak duality gives the reverse lower bound \(\operatorname{Tr}\Gamma\ge V\). The matrices \(\Gamma_\varepsilon\) are bounded: \(\Gamma_\varepsilon\ge K_1\) gives a fixed lower spectral bound, while their traces are bounded above. A convergent subsequence as \(\varepsilon\downarrow0\) yields a dual feasible \(\Gamma\) with \(\operatorname{Tr}\Gamma=V\).

Finally,

\[
0=
\operatorname{Tr}\Gamma-
\sum_j\operatorname{Tr}(K_jN_j)
=
\sum_j\operatorname{Tr}((\Gamma-K_j)N_j).
\]

Every summand is nonnegative, so each vanishes. If \(A,B\ge0\) and \(\operatorname{Tr}(AB)=0\), then \(A^{1/2}BA^{1/2}\ge0\) has zero trace and is zero, hence \(AB=0\). Therefore \((\Gamma-K_j)N_j=0\). ∎

For a nonzero rank-one qubit effect \(N_j\), the slack therefore has the form

\[
\Gamma-K_j=s_j\operatorname{adj}(N_j),
\qquad s_j\ge0.
\]

The steered determinant constraint satisfies

\[
F_j=4|\det C|^2\det N_j.
\]

Pull the full incidence Lagrange equation back to variations of Bob's effects. Since

\[
F_j=4|\det C|^2\det N_j,
\]

it has the form

\[
K_j-\Gamma_y+4|\det C|^2\lambda_j\operatorname{adj}(N_j)=0.
\]

The normalization multiplier \(\Gamma_y\) in this equation is the same as the dual operator above. To see uniqueness, suppose \(\Gamma_y'\) is another operator satisfying complementary slackness. Then \(\Gamma_y-\Gamma_y'\) annihilates the range of every effect in that measurement. Those ranges span \(\mathbb C^2\) because the effects sum to the identity, so the difference is zero. Therefore

\[
4|\det C|^2\lambda_j\operatorname{adj}(N_j)
=\Gamma_y-K_j
=s_j\operatorname{adj}(N_j),
\]

and hence \(\lambda_j\ge0\). Metric stationarity of the same full Lagrange equation gives \(\lambda\in\ker\mathcal D^T\).

### Lemma 7.2. A zero slack gives a PVM tie

If \(s_j=0\), then \(K_j=\Gamma\). Replacing that entire measurement by the deterministic PVM

\[
N_j'=I,
\qquad
N_k'=0\quad(k\ne j)
\]

preserves its optimal score:

\[
\operatorname{Tr}K_j=
\operatorname{Tr}\Gamma.
\]

After this replacement Bob has only one nontrivial input. Every nonsignaling behavior with only one nontrivial input on one party is local: if the nontrivial Bob input has output \(b\), sample \(b\) with its marginal probability and independently sample potential Alice outputs for both of her inputs from their conditional distributions given \(b\). The deterministic Bob input is then fixed. This reproduces all observed pairs.

Every deterministic local response is implemented by qubit PVMs consisting of one identity projector and zero projectors. Thus a zero slack produces a fixed-qubit PVM strategy with the same Bell value.

Therefore, at a residual Bell maximizer whose value is strictly above the PVM support value,

\[
\boxed{\lambda_j>0\quad(j=1,\ldots,5).}
\]

Define

\[
\boxed{
\Lambda=
\sum_{j=1}^5\lambda_jr_jr_j^T
=
\operatorname{diag}(\lambda_1,\ldots,\lambda_4)+\lambda_5vv^T.
}
\]

This matrix is positive definite because \(r_1,\ldots,r_4\) already form a basis and all \(\lambda_j\) are positive.

---

## 8. Metric differential and the null-ray map

A tangent variation of the local metric has the form

\[
H(A,B,C,D)=
\begin{pmatrix}
0&0&A&B\\
0&0&C&D\\
A&C&0&A+B+C+D\\
B&D&A+B+C+D&0
\end{pmatrix}.
\]

For \(y=(y_0,y_1,y_2,y_3)^T\),

\[
\frac12y^THy=
A\phi_1(y)+B\phi_2(y)+C\phi_3(y)+D\phi_4(y),
\]

where

\[
\boxed{
\Phi(y)=
\begin{pmatrix}
y_2(y_0+y_3)\\
y_3(y_0+y_2)\\
y_2(y_1+y_3)\\
y_3(y_1+y_2)
\end{pmatrix}.}
\]

Set

\[
y_j=QPr_j.
\]

Then

\[
y_j^Tgy_j=(Pr_j)^TQ(Pr_j)=F_j=0.
\]

Under the physical reconstruction, \(\mathsf E y_j\) is twice the spatial Lorentz reflection of the future-null steered operator \(S_j\); hence every \(y_j\) is itself a future null ray in the \(g\)-geometry. The metric differential map is

\[
\mathcal D:H\longmapsto
(y_1^THy_1,\ldots,y_5^THy_5).
\]

Hence

\[
\operatorname{rank}\mathcal D
=
\dim\operatorname{span}\{\Phi(y_1),\ldots,\Phi(y_5)\}.
\]

Let

\[
K=\ker\mathcal D^T,
\qquad
k=\dim K=5-\operatorname{rank}\mathcal D.
\]

Metric stationarity of the Bell Lagrangian says

\[
\lambda=(\lambda_1,\ldots,\lambda_5)^T\in K.
\]

---

## 9. Exact constrained second variation

Let \((\delta P,H)\) be a tangent vector. Define

\[
S=P^TQP.
\]

Since \(Q\) has signature \((1,3)\) and \(P\) is invertible, \(S\) also has signature \((1,3)\).

Write

\[
\delta P=PW+HQ P.
\]

Equivalently,

\[
PW=\delta P-HQP.
\]

For a straight first-order variation, direct differentiation gives

\[
\frac{d^2}{dt^2}
\bigg|_{t=0}
(Pr_j)^Tg^{-1}(Pr_j)
=
2(PWr_j)^TQ(PWr_j).
\]

Weighting by \(\lambda_j\) yields the exact square-completion identity

\[
\boxed{
\sum_j\lambda_jD^2F_j[(\delta P,H)]
=
2q(W),
\qquad
q(W)=\operatorname{Tr}(SW\Lambda W^T).
}
\]

### Tangent solvability in \(W\)-coordinates

The first-order equations are

\[
2r_j^TSWr_j+y_j^THy_j=0.
\]

A solution \(H\) exists precisely when

\[
\boxed{
\operatorname{Tr}(SW\Lambda_\mu)=0
\quad\text{for every }\mu\in K,
}
\]

where

\[
\Lambda_\mu=\sum_j\mu_jr_jr_j^T.
\]

Define

\[
\mathcal H_K=
\left\{W\in M_4(\mathbb R):
\operatorname{Tr}(SW\Lambda_\mu)=0
\text{ for all }\mu\in K
\right\}.
\]

The functionals indexed by \(K\) are independent, so

\[
\dim\mathcal H_K=16-k.
\]

Every \(W\in\mathcal H_K\) lifts to an incidence tangent vector.

### Inertia of the ambient second form

Because \(S\) has signature \((1,3)\) and \(\Lambda>0\), invertible congruences transform \(q\) into

\[
q_0(Z)=
\sum_{j=1}^4 Z_{1j}^2-
\sum_{i=2}^4\sum_{j=1}^4Z_{ij}^2.
\]

Thus

\[
\boxed{
\operatorname{inertia}(q)=(4,12).
}
\]

Any subspace on which \(q\le0\) has dimension at most twelve. To see this directly, project such a subspace onto the twelve negative coordinates. The projection is injective, because a nonzero vector with all negative coordinates zero has strictly positive \(q\).

### Normalization does not remove an uphill direction

The identity matrix belongs to \(\mathcal H_K\), because

\[
\operatorname{Tr}(S\Lambda_\mu)
=
\sum_j\mu_jr_j^TSr_j=0.
\]

Moreover, for every \(W\in\mathcal H_K\),

\[
q(W+tI)=q(W).
\]

Indeed, \(q(I)=0\) and the polar cross term is

\[
\operatorname{Tr}(SW\Lambda)=0
\]

because \(\lambda\in K\).

Adding \(tI\) to \(W\) adds the radial variation \(tP\) to \(\delta P\), while leaving the tangent compatibility equations unchanged. It changes the normalization derivative by exactly \(t\). Therefore every positive-\(q\) tangent can be shifted to a normalized positive-\(q\) tangent.

### Sign at a Bell maximum

The stationarity equation has the sign

\[
c-\alpha uu^T=-2QP\Lambda.
\]

Along a normalized feasible curve, differentiating the constraints twice gives

\[
\frac{d^2}{dt^2}L_c(P(t))\bigg|_{t=0}=2q(W).
\]

Thus local maximality requires

\[
q(W)\le0
\]

for every normalized tangent direction.

---

## 10. Rank at least two is impossible at a strict maximum

Suppose

\[
\operatorname{rank}\mathcal D\ge2.
\]

Then

\[
k\le3
\]

and therefore

\[
\dim\mathcal H_K=16-k\ge13.
\]

But a nonpositive subspace for a quadratic form of inertia \((4,12)\) has dimension at most twelve. Hence there exists

\[
W\in\mathcal H_K
\]

with

\[
q(W)>0.
\]

After the radial normalization adjustment, this gives a normalized physical residual curve with strictly positive second derivative of the Bell value. Therefore the point is not a local maximum.

This proves:

\[
\boxed{
\operatorname{rank}\mathcal D\ge2
\quad\Longrightarrow\quad
\text{no strict residual Bell maximum.}
}
\]

This replaces the earlier, overly strong numerical conjecture that every generic Hessian has signature \((7,7)\). The exact ambient statement is the inertia \((4,12)\); the projected signature can vary, but rank at least two always leaves an uphill direction.

---

## 11. Projective injectivity of the null-ray map

The rank-one case requires an exact classification of the fibers of \(\Phi\) on the strict null quadric

\[
\mathcal N_g=
\{[x]\in\mathbb{RP}^3:x^Tgx=0\}.
\]

### Lemma 11.1. Base locus

On \(\mathcal N_g\),

\[
\Phi(x)=0
\]

holds exactly on the five rays

\[
[r_1],\ldots,[r_5].
\]

#### Proof

If \(x_2=x_3=0\), nullness gives \(x_0x_1=0\), yielding \(r_1,r_2\). If \(x_2=0\) and \(x_3\ne0\), the second and fourth components force \(x_0=x_1=0\), yielding \(r_4\). The case \(x_3=0\) gives \(r_3\). If \(x_2x_3\ne0\), all four equations give

\[
x_0=x_1=-x_2=-x_3,
\]

which is the ray \(r_5=v\). ∎

### Lemma 11.2. Rational inverse on the generic set

Write

\[
\Phi(x)=(A,B,C,D).
\]

Then

\[
\begin{aligned}
A-B&=x_0(x_2-x_3),\\
C-D&=x_1(x_2-x_3),\\
A-C&=x_2(x_0-x_1),\\
B-D&=x_3(x_0-x_1),\\
AD-BC&=x_2x_3(x_0-x_1)(x_2-x_3).
\end{aligned}
\]

Consequently,

\[
\begin{pmatrix}
(A-B)(A-C)(B-D)\\
(C-D)(A-C)(B-D)\\
(AD-BC)(A-C)\\
(AD-BC)(B-D)
\end{pmatrix}
=
\omega(x)x
\]

with

\[
\omega(x)=x_2x_3(x_2-x_3)(x_0-x_1)^2.
\]

Whenever \(\omega(x)\ne0\), the projective ray \([x]\) is recovered uniquely from \([\Phi(x)]\).

### Lemma 11.3. Exceptional fibers remain injective off the base locus

For every nonzero projective value \([w]\), the fiber

\[
\{[x]\in\mathcal N_g\setminus\{[r_1],\ldots,[r_5]\}:
[\Phi(x)]=[w]\}
\]

contains at most one point.

#### Proof

Only four exceptional source divisors remain after Lemma 11.2.

#### Case 1: \(x_2=0\)

The target has the form \([0:B:0:D]\). Any other preimage \(z\) either has \(z_2=0\), in which case after setting \(z_3=1\) and \((z_0,z_1)=t(B,D)\), nullness is

\[
t^2BD+2t(bB+dD)=0.
\]

The root \(t=0\) is the base ray \(r_4\), and there is at most one nonzero root.

Or \(z_2\ne0\), in which case the first and third target coordinates force \(z_0=z_1=-z_3\). A nonzero target then requires \(B=D\). Setting \(z_3=1\) and \(z_2=t\), one obtains

\[
z^Tgz=(1-2(b+d))(1-t).
\]

Strictness gives \(b+d<1/2\), hence \(t=1\), which is the base ray \(-v\).

#### Case 2: \(x_3=0\)

The symmetric calculation gives the equation

\[
t^2AC+2t(aA+cC)=0
\]

on the direct branch, and

\[
(1-2(a+c))(1-t)=0
\]

on the cross branch. Again there is at most one nonbase preimage.

#### Case 3: \(x_0=x_1\)

A nonbase point can be scaled to \(x_0=x_1=1\). Put \(p=x_2,q=x_3\). A target has the form \([A:B:A:B]\). The null and target-ratio equations are

\[
N=1+2(a+c)p+2(b+d)q+2epq=0,
\]

\[
R=Bp(1+q)-Aq(1+p)=0.
\]

Eliminating \(p\) gives the exact resultant

\[
\operatorname{Res}_p(N,R)
=-(q+1)
\left[
B+q\bigl(A(2a+2c-1)+2B(b+d)\bigr)
\right].
\]

At \(q=-1\), the null equation becomes

\[
(1-2(b+d))(1+p)=0,
\]

so strictness gives \(p=-1\), the base ray \(v\). The second factor is not identically zero: if \(B\ne0\), its constant term is nonzero; if \(B=0\), then \(A\ne0\) and strictness gives \(2(a+c)-1\ne0\). Hence there is at most one further \(q\), and the null equation then determines at most one \(p\). The only apparent failure of linear determination would require

\[
2(a+c)(b+d)=a+b+c+d-\tfrac12,
\]

which is equivalent to

\[
(2(a+c)-1)(2(b+d)-1)=0
\]

and is excluded by strictness.

#### Case 4: \(x_2=x_3\)

The target has the form \([A:A:C:C]\). For any preimage \(z\), the equalities of the first two and last two target coordinates give

\[
z_0(z_2-z_3)=z_1(z_2-z_3)=0.
\]

If \(z_2\ne z_3\), then \(z_0=z_1=0\), and strict \(e>0\) plus nullness forces \(z_2z_3=0\), a base ray. Thus a nonbase preimage has \(z_2=z_3\). Scale it to \(x_2=x_3=1\), and put \(p=x_0,q=x_1\). The equations are

\[
N=pq+2(a+b)p+2(c+d)q+2e=0,
\]

\[
R=C(p+1)-A(q+1)=0.
\]

The exact resultant is

\[
\operatorname{Res}_p(N,R)
=-(q+1)
\left[
Aq+2A(a+b)+2C(c+d)-C
\right].
\]

At \(q=-1\), the null equation becomes

\[
(2(a+b)-1)(p+1)=0,
\]

so strictness gives the base ray \(v\). Strictness also excludes an identically vanishing second factor or an undetermined null equation.

These four cases exhaust the zero set of \(\omega(x)\). ∎

---

## 12. Rank one cannot support a strict KKT multiplier

Suppose

\[
\operatorname{rank}\mathcal D=1.
\]

All nonzero row vectors \(\Phi(y_j)\) have the same projective image. The vectors \(y_j=QPr_j\) are five distinct future null rays because \(QP\) is invertible. By Lemma 11.3, at most one of them can lie outside the base locus of \(\Phi\). The base-locus rows are zero by Lemma 11.1.

Therefore exactly one row of \(\mathcal D\) is nonzero. If that row is indexed by \(j_0\), then

\[
K=\ker\mathcal D^T
=
\{\mu:\mu_{j_0}=0\}.
\]

No vector in \(K\) is strictly positive. This contradicts the strict KKT multiplier

\[
\lambda_j>0
\quad(j=1,\ldots,5).
\]

Hence

\[
\boxed{
\operatorname{rank}\mathcal D=1
\quad\Longrightarrow\quad
\text{no strict residual Bell maximum.}
}
\]

---

## 13. Rank zero has an explicit deterministic PVM decomposition

Suppose

\[
\operatorname{rank}\mathcal D=0.
\]

Then every \(y_j=QPr_j\) lies in the base locus of \(\Phi\), so

\[
y_j=t_jr_{\pi(j)}
\]

for a permutation \(\pi\) and positive scalars \(t_j\). Positivity of the scalars follows because the physical vector corresponding to \(y_j\) is the spatial Lorentz reflection of a future null steered operator and hence remains future null.

The five rays have the unique linear relation

\[
r_1+r_2-r_3-r_4-r_5=0.
\]

Write its coefficient vector as \(\epsilon=(1,1,-1,-1,-1)\). Applying \(QP\) gives

\[
\sum_j \epsilon_j t_j r_{\pi(j)}=0.
\]

Uniqueness of the circuit means that, for some nonzero scalar \(\tau\),

\[
\epsilon_jt_j=\tau\epsilon_{\pi(j)}
\quad(j=1,\ldots,5).
\]

All \(t_j\) are positive. If \(\tau<0\), the permutation would have to exchange the two positive-sign rays with the three negative-sign rays, which is impossible because the two sign classes have different cardinalities. Hence \(\tau>0\), \(\pi\) preserves the binary and ternary partitions, and every \(t_j=\tau=: \kappa\).

After relabeling within the two partitions, \(QP r_j=\kappa r_j\) for all five rays. Since \(r_1,\ldots,r_4\) are a basis, \(QP=\kappa I\), hence \(P=\kappa g\). The normalizations \(u^TPu=1\) and \(u^Tgu=1\) give \(\kappa=1\). Therefore

\[
\boxed{
p_{ij}=r_i^Tgr_j.}
\]

It remains to exhibit a deterministic local decomposition.

Let the ternary outcomes be indexed by \(i,j\in\{1,2,3\}\). Define

\[
c_{ij}=g_{ij}\quad(i\ne j),
\qquad c_{ii}=0,
\]

where these indices refer to the ternary rays. Also set

\[
a_i=g_{1,i},
\qquad
b_i=g_{2,i}.
\]

The Gram relations imply

\[
\sum_{j\ne i}c_{ij}=a_i+b_i,
\]

and

\[
\sum_i a_i=
\sum_i b_i=\frac12.
\]

We need a matrix \(Q=(q_{ij})\) satisfying

\[
0\le q_{ij}\le c_{ij},
\qquad q_{ii}=0,
\]

\[
\sum_jq_{ij}=b_i,
\qquad
\sum_iq_{ij}=a_j.
\]

### Lemma 13.1. The bounded transportation matrix exists

Write

\[
q_{ij}=\frac{c_{ij}}2+f_{ij},
\qquad f_{ij}=-f_{ji}.
\]

Set

\[
d_i=\frac{b_i-a_i}{2},
\qquad d_1+d_2+d_3=0.
\]

Choose

\[
f_{12}=t,
\qquad
f_{13}=d_1-t,
\qquad
f_{23}=d_2+t.
\]

The divergence equations are then automatic. The bounds \(|f_{ij}|\le c_{ij}/2\) require \(t\) to lie in the three intervals

\[
\begin{aligned}
I_{12}&=[-c_{12}/2,c_{12}/2],\\
I_{13}&=[d_1-c_{13}/2,d_1+c_{13}/2],\\
I_{23}&=[-d_2-c_{23}/2,-d_2+c_{23}/2].
\end{aligned}
\]

They intersect pairwise because

\[
|d_i|
\le
\frac{a_i+b_i}{2}
=
\frac{c_{ij}+c_{ik}}2.
\]

Three closed intervals on the real line with pairwise intersections have a common point: the interval with the largest left endpoint intersects the interval with the smallest right endpoint. Thus an admissible \(t\) exists. ∎

Now split each ternary pair probability \(c_{ij}\) into two deterministic components:

- weight \(q_{ij}\): Alice outputs binary outcome \(1\), Bob outputs binary outcome \(2\), while the ternary outputs are \((i,j)\);
- weight \(c_{ij}-q_{ij}\): Alice outputs binary outcome \(2\), Bob outputs binary outcome \(1\), while the ternary outputs are \((i,j)\).

The row and column sums reproduce both cross-setting blocks. The binary block is perfectly anticorrelated with weights \(1/2,1/2\), and the ternary block is exactly \(c_{ij}\).

This is a convex combination of deterministic local behaviors. Each deterministic behavior is a qubit-PVM behavior using one identity projector and zero projectors. Therefore

\[
\boxed{
\operatorname{rank}\mathcal D=0
\quad\Longrightarrow\quad
p\in\mathcal Q^{\mathrm{PVM}}_2(2,2).
}
\]

---

## 14. Closure of the residual architecture

Let a Bell functional have a residual maximum strictly above its PVM maximum. By Lemma 7.2, its determinant multiplier satisfies \(\lambda_j>0\) for all five outcomes.

There are only three cases.

### Case 1: \(\operatorname{rank}\mathcal D\ge2\)

Section 10 constructs a normalized physical tangent with positive Bell second derivative, contradicting local maximality.

### Case 2: \(\operatorname{rank}\mathcal D=1\)

Section 12 proves that \(\ker\mathcal D^T\) contains no strictly positive vector, contradicting \(\lambda>0\).

### Case 3: \(\operatorname{rank}\mathcal D=0\)

Section 13 gives an explicit PVM convex decomposition, contradicting a value strictly above the PVM support value.

Therefore no strict residual separator exists.

By the finite-dimensional convex criterion and the inherited residual architecture theorem,

\[
\boxed{
\mathcal Q^{\mathrm{POVM}}_2(2,2)
=
\mathcal Q^{\mathrm{PVM}}_2(2,2)
}
\]

for every finite output architecture.

---

## 15. Minimum-setting classification

A Bell experiment with one input on either party is local, hence cannot separate POVMs from PVMs. The theorem above excludes two inputs on both parties. The frozen rational \(3\times2\) example supplies a strict separation.

Thus, up to exchanging Alice and Bob,

\[
\boxed{
(3,2)
}
\]

is the minimum setting architecture for fixed-qubit POVM–PVM Bell separation.

The inherited one-binary-party theorem additionally shows that in a hypothetical two-setting separator both parties would have needed genuine nonbinary measurements; the present theorem proves that even this two-sided nonprojectivity is insufficient.

---

## 16. Exact versus exploratory statements

### Proved exactly

1. Universal two-setting equality for arbitrary finite output sets.
2. Exact Lorentz incidence model of the residual architecture.
3. Exact residual dimension \(14\).
4. Exact ambient second-form inertia \((4,12)\).
5. Rank-at-least-two uphill-direction theorem.
6. Projective injectivity of the quadratic null-ray map away from five base rays.
7. Rank-one incompatibility with strictly positive KKT multipliers.
8. Explicit deterministic/PVM decomposition of every rank-zero behavior.
9. Minimum setting architecture \(3\times2\), using the frozen separation.

### Corrected exploratory conjecture

The earlier numerical conjecture that the intrinsic Hessian always has signature \((7,7)\) is false. Different smooth residual points can have different projected signatures. The invariant fact needed for closure is instead that the ambient second form has inertia \((4,12)\), and every rank-at-least-two tangent space is too large to be nonpositive.

### No longer unresolved

There are no residual ternary or four-outcome architectures left. No exact two-setting Bell separator exists.

---

## 17. Verification boundary

The accompanying exact verifier checks:

- the four-parameter metric identities;
- the metric-derivative/null-ray map;
- the exact rational inverse of the quadratic map;
- all exceptional-fiber resultant factorizations;
- the pure-state conformal Lorentz relation on an exact algebraic test strategy;
- the weighted Hessian square-completion identity;
- independence of the five rank-one constraint matrices;
- the rank-zero transportation/decomposition identities.

The following parts are human-readable finite-dimensional arguments rather than finite enumerations:

- the nearest-point convex separation lemma;
- the positive-slack argument;
- the dimension bound for nonpositive subspaces;
- the interval-intersection existence proof;
- the inherited architecture reduction.

No numerical optimizer, SDP value, random sample, or interval approximation enters the theorem.

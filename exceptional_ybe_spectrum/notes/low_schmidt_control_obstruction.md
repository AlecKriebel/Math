# Low operator-Schmidt rank forces divisibility by four

**Date:** 2026-07-29

**Status:** PROVED

**Scope:** arbitrary exceptional solutions of operator-Schmidt rank at most
three.  No Pauli, sparsity, irreducibility, or a priori leg-commutant
assumption is made.  The result does not exclude a \(d\equiv2\pmod4\)
solution of operator-Schmidt rank at least four.

## 1. Result

For \(H\in\operatorname{End}(V\otimes V)\), let
\(\operatorname{OSR}(H)\) denote its operator-Schmidt rank.  Put
\[
 H_1=H\otimes I,\qquad H_2=I\otimes H.
\]

The structural statement proved below is slightly more general than the
exceptional application.

> **Theorem 1 (twisted control becomes a true rank-one symmetry).**
> Let \(H\) be a Hermitian unitary which is locally equivalent to a
> controlled bipartite unitary.  Suppose
> \[
> H_1H_2H_1-H_2H_1H_2=c(H_1-H_2)
> \tag{1}
> \]
> for a scalar \(c\) with \(\lvert c\rvert\ne1\).  Then one of the true
> one-leg commutants of \(H\) contains a rank-one projection.

Here “locally equivalent” has its standard quantum-information meaning:
four independent local pre- and post-unitaries are allowed.  It is
strictly broader than sitewise conjugacy and does **not** preserve (1).
The proof below does not make that invalid inference.  Hermiticity converts
the four-unitary normal form into a twisted controlled form by one valid
sitewise conjugacy; (1) is used only after that conversion.

Cohen--Yu prove that every bipartite unitary of operator-Schmidt rank two is
locally equivalent to a controlled unitary
([arXiv:1211.5201](https://arxiv.org/abs/1211.5201), Theorem 6).
Chen--Yu prove the same statement in operator-Schmidt rank three
([arXiv:1407.5464](https://arxiv.org/abs/1407.5464), Theorem 11).
Rank one is immediate.  Theorem 1 therefore gives:

> **Corollary 2 (complete low-Schmidt spectrum).**
> An exceptional solution of operator-Schmidt rank at most three exists in
> local dimension \(d\) if and only if
> \[
> \boxed{4\mid d.}
> \tag{2}
> \]
> In particular, every hypothetical exceptional solution in dimension
> \(d\equiv2\pmod4\), including \(d=6\), has
> \[
> \boxed{\operatorname{OSR}(H)\ge4.}
> \tag{3}
> \]

Necessity combines Theorem 1 with automatic standardness and the exact
rank-one leg-commutant arithmetic recalled in Section 5.  Sufficiency uses
the published rank-three \(d=4\) witness and identity stabilization, which
preserves operator-Schmidt rank three.

## 2. From four local unitaries to a valid twisted-control form

Assume first that the controlling side is the first tensor factor.  Local
equivalence to a controlled unitary means that there are unitaries
\(Q,R,S,T\in U(V)\), an orthonormal basis with rank-one projections
\[
E_i=|i\rangle\langle i|,
\]
and unitaries \(U_i\in U(V)\) such that
\[
H=(Q\otimes S)
   \left(\sum_i E_i\otimes U_i\right)
   (R\otimes T).
\tag{4}
\]
The four factors in (4) may all be different.  We do **not** apply (1) to
the controlled operator in parentheses.

Instead make the sitewise conjugacy
\[
\widetilde H=(Q^*\otimes Q^*)H(Q\otimes Q).
\tag{5}
\]
Unlike general local equivalence, (5) preserves Hermiticity, unitarity,
operator-Schmidt rank, both leg-commutant projection ranks, and the
three-site equation (1).  Absorbing the second-leg factors gives the exact
identity
\[
\boxed{
\widetilde H=\sum_i E_iK\otimes V_i,
\qquad
K=RQ,\quad
V_i=Q^*SU_iTQ.
}
\tag{6}
\]
Both \(K\) and every \(V_i\) are unitary.  This is the only conversion from
the Chen--Yu normal form used in the proof.

If the controlled side supplied by the cited theorem is the second tensor
factor, replace \(H\) by \(H^{\mathrm{op}}=FHF\), where \(F\) is the tensor
flip.  Reversal of the three tensor sites interchanges the two adjacent
copies and reverses both sides of (1), so \(H^{\mathrm{op}}\) again satisfies
(1) with the same \(c\).  At the end, tensor flip simply exchanges the two
leg commutants.

## 3. The Hermitian support graph

In the control basis, the \(ij\) block of (6) is
\[
\widetilde H_{ij}=K_{ij}V_i.
\tag{7}
\]
Hermiticity is therefore exactly
\[
\boxed{
K_{ij}V_i=\overline{K_{ji}}\,V_j^*.
}
\tag{8}
\]
In particular,
\[
K_{ij}\ne0\quad\Longleftrightarrow\quad K_{ji}\ne0,
\tag{9}
\]
and along every such edge \(V_j\) is a phase multiple of \(V_i^*\).

Let \(G\) be the undirected support graph of \(K\), loops included.  Its
connected-component projections
\[
Z_C=\sum_{i\in C}E_i
\tag{10}
\]
reduce \(K\).  Hence
\[
[Z_C\otimes I,\widetilde H]=0,
\tag{11}
\]
so \(\widetilde H\) is a direct sum over the graph components on its first
leg.

### 3.1 A nonbipartite component gives a rank-one projection

Along a path, (8) alternates projective classes
\[
[W],\ [W^*],\ [W],\ [W^*],\ldots.
\]
If a connected component \(C\) is nonbipartite, an odd cycle makes
\([W]=[W^*]\).  Thus every target unitary in that component is a phase
multiple of one fixed unitary:
\[
V_i=\alpha_iW\qquad(i\in C),\qquad |\alpha_i|=1.
\tag{12}
\]
The corresponding block factors:
\[
\widetilde H_C=A_C\otimes W,\qquad
A_C=\sum_{i\in C}\alpha_iE_iK\big|_{Z_CV}.
\tag{13}
\]
Because \(\widetilde H_C\) and \(W\) are unitary, \(A_C\) is unitary.  Let
\(e\) be the rank-one projection onto any eigenvector of the normal
operator \(A_C\).  Then
\[
[e\otimes I,\widetilde H_C]=0.
\]
For every other graph component \(D\), one has \(eZ_D=Z_De=0\), so the same
rank-one \(e\), extended by zero, commutes with the **full**
\(\widetilde H\):
\[
\boxed{[e\otimes I,\widetilde H]=0.}
\tag{14}
\]
Notice that no commutation between \(W\) and the target unitaries belonging
to other components is needed.  The graph decomposition is on the first,
controlling leg.

It remains to show that the alternative—all components bipartite—is
incompatible with (1).

## 4. The all-bipartite branch contradicts the cubic

Let \(C=L\sqcup R\) be a bipartite support component.  In this decomposition
\[
K_C=
\begin{pmatrix}
0&K_{LR}\\
K_{RL}&0
\end{pmatrix}.
\tag{15}
\]
Since \(K_C\) is unitary, \(K_{LR}\) and \(K_{RL}\) are square unitaries;
in particular \(\dim L=\dim R\).  Equation (8) gives a unitary \(W_C\) and
phases such that the \(V_i\)'s are phase multiples of \(W_C\) on one
bipartition class and of \(W_C^*\) on the other.  Absorbing the phases into
the off-diagonal blocks, the component of \(\widetilde H\) has the form
\[
\widetilde H_C=C_C\otimes W_C+C_C^*\otimes W_C^*,
\tag{16}
\]
where \(C_C:R\to L\) is unitary and is zero on the orthogonal complement.
Hermiticity gives the displayed adjoint pairing exactly.

Choose an orthonormal basis \(r_{C,u}\) of \(R\) and put
\(\ell_{C,u}=C_Cr_{C,u}\).  Then
\[
C_C=\sum_u|\ell_{C,u}\rangle\langle r_{C,u}|.
\tag{17}
\]
Doing this independently in every component produces an orthonormal basis
of \(V\), a fixed-point-free involution \(x\mapsto\bar x\), and unitaries
\(U_x\) with \(U_{\bar x}=U_x^*\) such that
\[
\boxed{
\widetilde H=\sum_x S_x\otimes U_x,
\qquad
S_x=|\bar x\rangle\langle x|.
}
\tag{18}
\]
This is only an orthonormal-basis expansion of the same \(\widetilde H\);
no independent first-leg transformation is applied to the Yang--Baxter
equation.

Fix \(x\), and apply the first-leg matrix functional
\[
\varphi_x(A)=\langle\bar x|A|x\rangle
\tag{19}
\]
to (1).  Since
\[
S_aS_b
=\delta_{a,\bar b}\,|\bar a\rangle\langle\bar a|
\tag{20}
\]
is always diagonal when nonzero, the first cubic word gives
\[
(\varphi_x\otimes\operatorname{id}\otimes\operatorname{id})
(\widetilde H_1\widetilde H_2\widetilde H_1)=0.
\tag{21}
\]
In the other word, the middle copy of \(\widetilde H_1\) supplies the
unique first-leg coefficient \(S_x\), so
\[
(\varphi_x\otimes\operatorname{id}\otimes\operatorname{id})
(\widetilde H_2\widetilde H_1\widetilde H_2)
=
\widetilde H(U_x\otimes I)\widetilde H.
\tag{22}
\]
The two linear terms give
\[
(\varphi_x\otimes\operatorname{id}\otimes\operatorname{id})
(\widetilde H_1)=U_x\otimes I,
\qquad
(\varphi_x\otimes\operatorname{id}\otimes\operatorname{id})
(\widetilde H_2)=0.
\tag{23}
\]
Consequently (1) would force
\[
\boxed{
-\widetilde H(U_x\otimes I)\widetilde H
=c(U_x\otimes I).
}
\tag{24}
\]
The left side of (24) is unitary, while the right side has operator norm
\(\lvert c\rvert\).  This contradicts \(\lvert c\rvert\ne1\).

Thus at least one support component is nonbipartite, and (14) proves
Theorem 1.  Conjugating \(e\) back through (5), and undoing a tensor flip if
one was used, gives a rank-one projection in a true one-leg commutant of
the original \(H\).

## 5. Exceptional arithmetic

For the exceptional class, \(c=1/3\).  Write \(P=(I-H)/2\).
Automatic standardness gives
\[
\operatorname{Tr}_1P=\operatorname{Tr}_2P=\frac d2I.
\tag{25}
\]
Let \(e\) be the rank-one projection from Theorem 1.  It commutes with
\(P\) on one leg.  Restricting \(P_{12},P_{23}\) to the corresponding
three-site spectator sector gives two projections on a space of dimension
\[
D=d^2
\]
with ranks \(D/2\), overlap trace \(D/4\), and the same shifted
two-projection relation.  The common-one and common-zero multiplicities are
both
\[
\frac D8=\frac{d^2}{8}.
\tag{26}
\]
They are integers, so \(8\mid d^2\), equivalently \(4\mid d\).  This is the
rank-one case of the invariant leg-commutant theorem C17.

Conversely, the published \(d=4\) reflection has operator-Schmidt rank
three.  If \(d=4m\), identity stabilization gives
\[
H^{(4m)}
=\sum_{\nu=1}^3
(A_\nu\otimes I_m)\otimes(B_\nu\otimes I_m),
\tag{27}
\]
and both coefficient triples remain linearly independent.  Hence
\(\operatorname{OSR}(H^{(4m)})=3\).  This completes Corollary 2.

## 6. Exact calibrations and type distinction

For the published five-Pauli witness, an exact three-term form is
\[
H=\sum_{\nu=X,Y,Z}A_\nu\otimes B_\nu,
\tag{28}
\]
with
\[
\begin{aligned}
A_X&=X\otimes I,&
B_X&=-\frac1{\sqrt3}X\otimes X,\\
A_Y&=Y\otimes I,&
B_Y&=\frac1{\sqrt6}(Z\otimes Y-Y\otimes Z),\\
A_Z&=Z\otimes I,&
B_Z&=\frac1{\sqrt6}(Y\otimes Y-Z\otimes Z).
\end{aligned}
\tag{29}
\]
The left coefficient commutant is
\[
I_2\otimes M_2,
\tag{30}
\]
whose minimal projections have ordinary rank two.  In contrast, the three
right coefficients in (29) commute and generate a four-dimensional MASA
\(\mathbb C^4\); its joint eigenspaces are rank one.  This distinction is
important: a dimension-four commutant need not be a MASA, but Theorem 1
needs a rank-one projection on only one side.

The \(s=1,t=0\) representative of the C15 color/face circle also has an
exact Clifford/tetrahedral three-term form.  Its right coefficients are
\[
-\frac1{\sqrt3}X\otimes Z,\qquad
-\frac1{\sqrt3}I\otimes Z,\qquad
\frac1{\sqrt3}X\otimes I,
\tag{31}
\]
which again generate a MASA.

The independent verifier reconstructs both matrices from their original
formulas and checks exactly:

- Hermiticity, involutivity, trace zero, and both scalar partial traces;
- the full \(64\times64\) shifted cubic;
- operator-Schmidt rank three with three equal singular values
  \(4/\sqrt3\);
- the right-leg rank-one commuting projections;
- the tensor-flipped, opposite-control orientation.

It also constructs a balanced, fully standard, rank-three \(d=6\)
fixed-point-free twisted-control involution.  It deliberately fails the
exceptional cubic with exact squared residual norm
\[
512.
\tag{32}
\]
For all six off-diagonal control coefficients, the verifier separately
replays (21)--(24).  Thus involutivity, balance, standardness, and low
Schmidt rank alone are not the obstruction; the shifted cubic is used at
the decisive step.

Replay:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_low_schmidt_control_obstruction.py
```

## 7. Limitations

This theorem completely closes only the branch
\(\operatorname{OSR}(H)\le3\).  It does not prove that an arbitrary
exceptional solution is locally equivalent to a controlled gate, and the
cited unitary-structure theorems do not extend to arbitrary operator-
Schmidt rank.  A dimension-six witness, if one exists, must therefore use
at least four genuinely independent operator-Schmidt directions and have
no rank-one projection in either true leg commutant.

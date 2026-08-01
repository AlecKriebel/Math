# Direct physical DTH track from the complete-PPT pseudomoment

## Status

An unrestricted complex search on the physical DTH variety found no value
above (1/8).  Several independent starts converged to (1/8), including
the best seed in the deterministic 27-atom ensemble selected by overlap with
the exact complete-tripartition-PPT pseudomoment.  The equality attractors
share a rigid local compatibility relation, proved below to be sufficient
for DTH and to give an exact positive-semidefinite deficit identity.

This is a rigorous explanation of the observed equality face.  It is not a
proof of DTH away from that face, and absence of a numerical violation is
not used as evidence for the global theorem.

## 1. Lossless physical optimization

Write an orthonormal frame of the physical two-plane as

\[
 U=(u_0,u_1),
 \qquad
 W={u_0u_1^{\mathsf T}-u_1u_0^{\mathsf T}\over\sqrt2}.
\]

For fixed (U), set

\[
 g_j=\operatorname{Tr}(D_{e_j}W)
     =\sqrt2,u_1^{\mathsf T}D_{e_j}u_0
\]

and

\[
 G_{jk}={1\over2}\sum_{a=0}^1
 \langle D_{e_j}u_a,D_{e_k}u_a\rangle.
\]

Then

\[
 \|D_zW\|_2^2=z^\dagger Gz,
\]

while the two physical DTH equations are exactly

\[
 U^\dagger z=0,
 \qquad g^{\mathsf T}z=0.
\]

Thus, for fixed (U), the best (z) is the top eigenvector of (G)
compressed to

\[
 \ker[U^\dagger;g^{\mathsf T}].
\]

This eliminates (z) without a penalty or relaxation.  The discovery code
`discovery/agent_dth_physical_pseudomoment_seed.py` differentiates this
compressed eigenvalue, including the multipliers of both eliminated
constraints, and optimizes over the full complex Grassmannian
\(\operatorname{Gr}(2,27)\).  A central finite-difference check agrees with
the analytic horizontal derivative to about (10^{-11}) in representative
runs.

Eight unrestricted complex random starts and the pseudomoment-selected
physical seed gave no value above (1/8).  Three runs reached (1/8) to
double precision; the remaining runs ended between (8.2\times10^{-8})
and (2.7\times10^{-6}) below it.  These figures are discovery data only.

The finite seed is not claimed to be the global best rank-one approximation
to the mixed pseudomoment.  It is the best of the exact deterministic
27-atom product-DTH ensemble in the invariant-coordinate scan; its overlap
with the normalized candidate was

\[
 2.272120185942265\times10^{-6}.
\]

## 2. The active equality compatibility

Every converged equality point inspected has, after a permutation of the
three sites, the following properties.  There is a unit vector
\(a\in\mathbb C^3\) and a two-qutrit vector \(\xi\) such that

\[
 z=a\otimes\xi,
 \qquad \operatorname{SchmidtRank}(\xi)\le2,
\tag{1}
\]

and the code plane obeys

\[
 \operatorname{ran}U\subset a^\perp\otimes
     (\mathbb C^3\otimes\mathbb C^3).
\tag{2}
\]

Numerically, this is detected intrinsically by

\[
 \rho_z^{(i)}=|a\rangle\langle a|,
 \qquad
 \operatorname{Tr}(\rho_U^{(i)}\rho_z^{(i)})=0.
\tag{3}
\]

At equality one further has

\[
 D_z^\dagger D_z U={1\over8}U.
\tag{4}
\]

For two unrelated random equality runs the active sites were different,
the cofactor norms were approximately (0.1566) and (0.3699), and all
non-active one-site code marginals were full rank.  Hence this was not an
artifact of a zero-cofactor or completely product ansatz.

## 3. Exact one-site-factor deficit theorem

### Theorem

Let (z,U,W) be normalized as above.  Suppose (1) and (2) hold at one
physical site.  Then

\[
 \boxed{\|D_zW\|_2^2\le {1\over8}.}
\tag{5}
\]

Moreover, if (T=D_\xi^\dagger D_\xi), then the deficit has the exact
positive-semidefinite representation

\[
 \boxed{
 {1\over8}-\|D_zW\|_2^2
 ={1\over4}\sum_{r=0}^1
 \left\langle u_r,
 I_{a^\perp}\otimes\left({1\over4}I-T\right)u_r
 \right\rangle .}
\tag{6}
\]

Equality holds precisely when

\[
 \operatorname{ran}U
 \subset a^\perp\otimes E_{1/4}(T),
\tag{7}
\]

equivalently (D_z^\dagger D_zU=U/8).  The support and Omega equations,
when imposed, only cut out subplanes of this equality eigenspace; they are
not needed for inequality (5).

### Proof

Local Hodge covariance permits choosing (a=e_0) and Schmidt bases in
which

\[
 \xi=s|00\rangle+t|11\rangle,
 \qquad s,t\ge0,quad s^2+t^2=1.
\]

Write (A_p=2^{-1/2}(\varepsilon_{pai})_{a,i}).  Then

\[
 A_0^\dagger A_0={1\over2}P_{e_0^\perp},
 \qquad
 D_z=A_0\otimes D_\xi.
\tag{8}

The singular values of

\[
 D_\xi=sA_0\otimes A_0+tA_1\otimes A_1
\]

are

\[
 {1\over2},{1\over2},
 {s\over2},{s\over2},
 {t\over2},{t\over2},0,0,0.
\tag{9}

For completeness, the six off-diagonal matrix units give the two copies of
\(s/2\), the two copies of (t/2), and two zero values.  On the diagonal
matrix units the unscaled matrix is

\[
 {1\over2}
 \begin{pmatrix}
 0&0&t\\
 0&0&s\\
 t&s&0
 \end{pmatrix},
\]

whose singular values are (1/2,1/2,0).  This proves

\[
 0\preceq T\preceq {1\over4}I.
\tag{10}

Because both (u_r) lie in the local support (e_0^\perp), (8) gives

\[
 \|D_zu_r\|^2={1\over2}\langle u_r,(I\otimes T)u_r\rangle.
\]

Orthogonality of (u_0,u_1) removes the cross terms in the normalized skew
matrix (W), so

\[
 \|D_zW\|_2^2={1\over2}\sum_{r=0}^1\|D_zu_r\|^2
 ={1\over4}\sum_{r=0}^1\langle u_r,(I\otimes T)u_r\rangle.
\]

Subtracting this expression from (1/8), using
\(\|u_0\|^2+\|u_1\|^2=2\), proves (6).  Equation (10) proves its
nonnegativity, and its kernel gives (7).  This also proves (4).  \(\square\)

## 4. Exact equality point

Take

\[
 \xi={3|00\rangle+4|11\rangle\over5},
 \qquad
 q={4|00\rangle+3|11\rangle\over5},
\]

\[
 z=e_0\otimes\xi,
 \qquad
 u_0=e_1\otimes q,
 \qquad
 u_1=e_2\otimes q.
\]

Then (U^\dagger z=0),
\(\operatorname{Tr}(D_zW)=0\), and

\[
 \|D_zW\|_2^2={1\over8},
 \qquad
 (D_zW)^2=0.
\]

The two nonzero singular values of (D_zW) are both (1/4).  The
dependency-free verifier

```text
python3 verification/verify_dth_one_site_factor_equality.py
```

checks all of these statements over the rationals after clearing the fixed
Hodge square roots.

## 5. Interpretation and remaining gap

The nonlinear compatibility (3), followed by the spectral saturation (4),
is exactly what the mixed first-level pseudomoment does not encode.  It
explains why optimization seeded from the pseudomoment is driven to a
known local-support boundary instead of following its small negative
direction into the physical variety.

This does not show that every physical critical point satisfies (1)--(4).
The unresolved direct route is to prove that an interior stationary point
with full one-site support has strict deficit, or to find an exact interior
counterexample.  The exact complete-PPT pseudomoment remains only a
certificate-degree obstruction.

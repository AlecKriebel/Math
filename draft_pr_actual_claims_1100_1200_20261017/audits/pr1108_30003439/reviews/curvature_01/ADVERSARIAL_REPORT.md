# Independent adversarial curvature audit of PR1108 / 30003439

- Frozen proof revision: `148130ab93ab46a3459d7bc98a11a1ca79052d65`.
- Frozen proof path: `unsolved_math_prioritization/attempts/30003439/PROOF.md`.
- Problem identifier: 30003439 / OWR-15219-008.
- Assigned mechanism: exact universal negative-third-derivative certificate.
- Final mathematical checkpoint: 2026-10-17 17:12:50 UTC.
- Persistence and execution checkpoint: 2026-10-17 17:15:04 UTC.
- Final artifact checkpoint: 2026-10-17 17:16:43 UTC.
- Assigned-scope completion estimate: **100%**.
- Verdict: **the claimed curvature inequality is independently verified; no mathematical gap or counterexample found within this scope**.

## Exact claim and scope

Let
\[
K=\{(x,y,z):x,y,z\ge0,\ xy^2-z^3\ge0\},\qquad
f=-\log(xy^2-z^3)-\log z,\qquad F=25f.
\]
The audited statement is
\[
D^3F(a)[h,u,u]\le0
\quad(a\in\operatorname{int}K,\ h\in K,\ u\in\mathbb R^3).
\]
Base points are strictly interior; directions may be on any part of the closed cone, including the origin and coordinate-axis endpoints.

The original proof was retrieved at its pinned revision. The old MATHEMATICAL_AUDIT.md was not read. The derivative mechanism was reconstructed before comparing the claimed NC1 entries. This report does not determine self-concordance, nonhyperbolicity, source matching, novelty or priority. The scope-completion estimate measures this assigned verification, not the overall research program.

## Independent derivative mechanism

For \(p=xy^2-z^3\), let \(v=\nabla p\), \(H=\nabla^2p\). Differentiating \(-\log p-\log z\) gives
\[
-p^3D^3f[h]
=2p_hvv^\top
-p\{(Hh)v^\top+v(Hh)^\top+p_hH\}
+p^2D_hH+\frac{2p^3h_z}{z^3}E_{33}.
\]
Here \(D^3f[h]\) is the symmetric matrix with entries \(D^3f[h,e_i,e_j]\), in coordinate order \(x,y,z\). Thus a positive semidefinite matrix on the right establishes the required *negative* third derivative.

At \(a=(r,1,1)\), put \(s=r-1>0\), \(h(t)=(t^3,1,t)\). Direct derivatives of the cubic, without using NC1, are
\[
v=(1,2r,-3)^\top,\quad
H=\begin{pmatrix}0&2&0\\2&2r&0\\0&0&-6\end{pmatrix},
\]
\[
p_h=t^3+2r-3t,\quad Hh=(2,2t^3+2r,-6t)^\top,\quad
D_hH=\begin{pmatrix}0&2&0\\2&2t^3&0\\0&0&-6t\end{pmatrix}.
\]
Substitution reconstructs \(M=-s^3D^3f(r,1,1)[h(t)]\). Every claimed entry is recovered:
\[
\begin{aligned}
M_{11}&=2(t-1)^2(t+2),\\
M_{12}&=2(t-1)(2t^2+2t-1-3r),\\
M_{13}&=6(t-1)(r-t^2-t+1),\\
M_{22}&=4r^3+12r^2-18r^2t+6rt^3-6rt+2t^3,\\
M_{23}&=12r^2t-18r^2-6rt^3+24rt-6r-6t^3,\\
M_{33}&=6(r+2)t^3+2(r^3-6r^2-18r-4)t+12r(r+2).
\end{aligned}
\]
The checker expands these as exact polynomials in \(s,t\); all nine matrix-entry residuals vanish.

## Minors, square identities and universal positivity

Independent exact determinant expansion verifies
\[
\det M_{\{1,2\},\{1,2\}}=4s(t-1)^2P,\qquad
\det M=8s^4(t-1)^2R,
\]
where
\[
P=2(t+2)s^2-3(t-1)(3t+5)s+3(t-1)^2(t+2)^2,
\]
\[
R=(t+2)\{2ts^2-3(t-1)(3t+1)s+3(t-1)^2(t^2+4t+1)\}.
\]
It also verifies
\[
8(t+2)P=\{4(t+2)s-3(t-1)(3t+5)\}^2
+3(t-1)^2(8t^3+21t^2+6t-11),
\]
\[
\frac{8tR}{t+2}=\{4ts-3(t-1)(3t+1)\}^2
+3(t-1)^3(8t^2+13t+3).
\]
For the latter computation the positive \(t+2\) denominator is cleared; the analytic use of the identity is only for \(t\ge1\), so no division by zero or change of sign is hidden.

For \(0\le t<1\), the displayed terms of \(P,R\) are nonnegative and their constant terms are strictly positive. At \(t=1\), both equal \(6s^2>0\). For \(t>1\), both square remainders are strictly positive:
\[
8t^3+21t^2+6t-11
=8(t-1)^3+45(t-1)^2+72(t-1)+24>0,
\]
and \(8t^2+13t+3>0\). All scaling factors have positive sign. Consequently \(P,R>0\) for every \(s>0,t\ge0\); no additional possible positive root or unproved range remains.

When \(t\ne1\), \(M_{11}>0\), the leading two-by-two minor is positive and the full determinant is positive. Sylvester's criterion gives \(M\succ0\).

### Exceptional direction \(t=1\)

Exact substitution gives
\[
M(r,1)=2s^2
\begin{pmatrix}0&0&0\\0&2r+1&-3\\0&-3&r+2\end{pmatrix}.
\]
Both lower diagonal entries are positive, and the lower determinant is
\[
(2r+1)(r+2)-9=(r-1)(2r+7)>0.
\]
Thus this is positive semidefinite of rank two, with kernel \(\mathbb R e_x\). The exceptional direction is not inferred using the invalid strict Sylvester conditions at a zero leading entry.

### Endpoint \(e_x\)

Linearity in \(h\) identifies the coefficient of \(t^3\) in \(M(r,t)\) with
\[
-s^3D^3f(r,1,1)[e_x]
=2aa^\top+6sbb^\top,\quad
a=(1,2,-3)^\top,\quad b=(0,1,-1)^\top.
\]
This identity is independently checked coefficientwise. Both terms are positive semidefinite. Since \(a,b\) are independent and \(s>0\), its rank is two and its kernel is \(\mathbb R(1,1,1)\).

The alternative limit proof also works: \(h(t)/t^3\to e_x\), multiplication by \(t^{-3}\) preserves positive semidefiniteness for \(t>0\), the third derivative is linear in \(h\), and the positive semidefinite cone is closed. No uniform-in-base-point limit is needed.

## Automorphisms and completeness of direction reduction

For a *fixed* positive diagonal map \(D=\operatorname{diag}(a,b,c)\) with \(ab^2=c^3\),
\[
p(Dq)=c^3p(q),\qquad f(Dq)=f(q)-4\log c.
\]
Both \(D\) and \(D^{-1}\) preserve \(K\). For an arbitrary interior base point \((x,y,z)\), the choice
\[
D=\operatorname{diag}(y^2/z^3,1/y,1/z)
\]
takes it to \((xy^2/z^3,1,1)\), with the first coordinate greater than one.

When differentiating, this \(D\) is fixed at the selected base point. Therefore
\[
D^3f(Da)[Dh,Du,Du]=D^3f(a)[h,u,u].
\]
In matrix form the original-coordinate negative-third-derivative matrix is the congruence \(D^\top[-D^3f(Da)[Dh]]D\). This verifies the coordinate convention and sign.

If \(h_y>0\), define \(t=h_z/h_y\ge0\). Then
\[
h=h_y(t^3,1,t)+
\left(h_x-\frac{h_z^3}{h_y^2}\right)e_x.
\]
Both coefficients are nonnegative by membership in \(K\). If \(h_y=0\), the cone inequality and nonnegative coordinates force \(h_z=0\), so \(h=h_xe_x\) with \(h_x\ge0\). This includes \(h=0\). The \(t=0\) direction includes the \(e_y\) boundary.

Consequently every transformed cone direction is a nonnegative combination of directions already proved. Linearity gives the universal inequality for \(f\). Multiplication by 25 preserves its sign and establishes the claimed inequality for \(F\).

The excluded limit \(s=0\) is a boundary base point, outside the statement. Possible degeneration as \(s\downarrow0\) therefore creates no missing case.

## Computational reproduction and adversarial controls

The saved checker uses only Python standard-library exact fractions and a sparse polynomial ring over \(\mathbb Q\). It does not use SymPy, floating-point eigenvalues, numerical thresholds or external programs.

It checks:
1. All nine NC1 entries, NC2, NC3, NC4 and NC5 as polynomial identities.
2. The exceptional \(t=1\) matrix, endpoint Gram identity and endpoint kernel.
3. Forty-five rational parameter pairs, with
   \(s\in\{1/100,1/3,1,3,100\}\) and
   \(t\in\{0,1/100,1/2,99/100,1,101/100,2,10,100\}\).
4. An independent derivative mechanism at those pairs: expand
   \(f(q+\epsilon h+\eta u)\) through total degree three using the exact logarithm series. Its \(\epsilon\eta^2\) coefficient equals \(D^3f[h,u,u]/2\). Seven directions per pair give **315 exact contractions**, including all basis and pairwise-sum directions and \((2,-3,5)\).

These finite tests support the analytic universal proof above; they are not its replacement.

Three falsification controls pass:
- Reverse the whole curvature sign: the leading entry becomes \(-4\) at \(r=2,t=0\).
- Extend the formula to the forbidden direction \(t=-1\): at \(q=(2,1,1)\), \(h=(-1,1,-1)\), its determinant is \(-1216\), and \(u=(5,1,2)\) gives
  \(-D^3f(q)[h,u,u]=-2\), hence \(D^3f(q)[h,u,u]=2>0\).
- Omit \(-\log z\): the resulting matrix is \(M_0=M-2s^3tE_{33}\). Its determinant is \(-24576\) at \(s=4,t=2\). Thus this additional logarithm is essential for negative curvature, not only for boundary blowup.

The checker has a mandatory explicit startup rejection when Python's optimization disables assertions. Two normal runs returned exit code zero, empty stderr and byte-identical single final JSON documents. Each final document is emitted only after all 315 logarithm-series checks and all controls pass. A run with `python3 -O` returned exit code one, empty stdout and the expected startup RuntimeError before any mathematical work.

## Artifacts and exact remaining gap

- `curvature_reproduction.py`: complete tested exact checker.
- `results.json`: the single final JSON output after every mathematical check.
- `execution.json`: normal rerun determinism and optimized-rejection execution record.
- `optimized_rejection.txt`: complete optimized-mode rejection output.
- `RESEARCH_LOG.md`: authoritative checkpoints and scope-completion estimates.
- `SHA256SUMS`: SHA-256 hashes of these files and this report.

**Strongest verified result:** the universal negative-third-derivative inequality for the specified pair \((K,F)\), including all cone-direction endpoints.

**Exact remaining gap in assigned scope:** none found. No route is blocked or deferred inside this curvature proof. Overall full-solution acceptance requires the separate assigned audits of the other theorem components and target interpretation.

No other files, PRs, branches, commits, remote content or external communications were changed by this audit.

# Hostile audit: remaining finite companions in the outer-infinity chart

**Verdict: PASS.**

The stated theorem is correct in its stated chart:
\[
p=x^2,\quad q=yz,\qquad
H_4=((p-aq)^2,q^2,0)^T,\qquad
(H_3)_3=x(p-cq).
\]
For every \((a,c)\ne(0,0)\), the homogeneous Jacobian equations force
\(\det L=0\).  I found no omitted projective endpoint, illegal division,
unaccounted gauge direction, or exceptional lower-degree branch.

This verdict is conditional only in the scope already stated by the note.
It does not reprove the separate \((a,c)=(0,0)\) theorem and it does not
address the companion-at-infinity form \(xq\), the two-finite-critical-point
chart, or the rank-one-restriction pencil.  I checked that the separately
audited `line22_marked_critical_infinity` result has exactly the one-point
scope required by the final frontier statement.

No global document was edited and no commit was made.

## 1. Stabilizer and orbit taxonomy

Let a source linear map preserving \(\langle x^2,yz\rangle\) send \(x\) to
\(X\).  Since \(X^2\) is a rank-one member of the pencil and \(x^2\) is its
unique rank-one member, \(X=\alpha x\).  Factoring the image of \(yz\) on
the plane \(x=0\), and then comparing the \(xy,xz\) coefficients, shows
that the full source stabilizer is
\[
(x,y,z)\mapsto(\alpha x,\beta y,\gamma z)
\]
up to interchange of \(y,z\).  Consequently
\[
u=\frac{x^2}{yz}\mapsto
\frac{\alpha^2}{\beta\gamma}u.
\]
After diagonal target rescalings restore the displayed coefficients of
\(H_4\) and \(x(p-cq)\), this induces
\[
(a,c)\mapsto(\lambda a,\lambda c),\qquad \lambda\in\mathbb C^\times.
\]
Every nonzero \(\lambda\) occurs.  The interchange of \(y,z\) acts
trivially on \(p,q\) and on the parameters.

Thus the nonzero orbits are exactly \([a:c]\in\mathbb P^1\), while the
origin is a separate fixed orbit.  The following five disjoint strata
exhaust that projective line:
\[
\begin{array}{c|c}
\text{stratum}&\text{representative}\\ \hline
a\ne0,\ c(3a-c)(3a-2c)\ne0&
  (1,t),\quad t(3-t)(3-2t)\ne0\\
c=3a\ne0&(1,3)\\
2c=3a\ne0&(2,3)\\
c=0,\ a\ne0&(1,0)\\
a=0,\ c\ne0&(0,1).
\end{array}
\]
In particular, both projective endpoints are present.  Normalizing
\((1,t)\), \((1,3)\), \((2,3)\), \((1,0)\), or \((0,1)\) divides only by
the coordinate explicitly assumed nonzero on that stratum.

## 2. Target-shear legality

The shears
\[
F_1\mapsto F_1+\lambda F_3,\qquad
F_2\mapsto F_2+\mu F_3
\]
have determinant one.  They leave \(H_4\) unchanged and, because the
\(x^3\) coefficient of \(x(p-cq)\) is one, remove exactly the \(x^3\)
coefficients of \(U=(H_3)_1\) and \(V=(H_3)_2\).  Simultaneously they make
the row operations
\[
\operatorname{row}_1(L)\mapsto\operatorname{row}_1(L)+
\lambda\operatorname{row}_3(L),\qquad
\operatorname{row}_2(L)\mapsto\operatorname{row}_2(L)+
\mu\operatorname{row}_3(L)
\]
and relabel the unrestricted first two quadratic components.  Hence they
preserve both the Keller property and \(\det L\).  No source translation
is used in this package.

## 3. Raw \(E_7\): ranks, minors, and complete kernels

I independently formed the \(36\times26\) coefficient matrix of \(E_7\)
from completely general cubics \(U,V\) and a completely general quadratic
\(W\).  The exact results are:
\[
\begin{array}{c|c|c}
(a,c)&\operatorname{rank}E_7&\operatorname{nullity}E_7\\ \hline
(1,t)\text{ over }\mathbb Q(t)&18&8\\
(1,3)&14&12\\
(2,3)&14&12\\
(1,0)&16&10\\
(0,1)&18&8.
\end{array}
\]
Using the row and column indices recorded in the supplied verifier, direct
determinant evaluation reproduced
\[
-782757789696\,t^4(t-3)^4(2t-3)^6
\]
and the four specialized maximal minors
\[
\begin{aligned}
-101559956668416,\qquad
-6499837226778624,\qquad
25999348907114496,\qquad
-50096498540544.
\end{aligned}
\]
The generic symbolic rank gives the upper bound \(18\); its displayed
minor gives the matching lower bound away from exactly
\(t=0,3,3/2\).  The four specialized exact ranks and nonzero maximal
minors give both bounds at every exceptional point, including the
projective endpoint \(a=0\).

I also checked kernel completeness rather than merely substituting the
listed families.  After the two independent shear directions are removed,
the parameter-direction ranks of the displayed kernels are respectively
\[
6,\quad10,\quad10,\quad8,\quad6.
\]
Adding back the two \(x^3\) shear directions gives
\[
8,\quad12,\quad12,\quad10,\quad8,
\]
exactly the raw nullities above.  Each direction is annihilated by the raw
matrix.  Independence is immediate as well from the unique appearances
of the \(W\)-coefficients, followed by \(A,B,r_1,r_2\).  Therefore all five
gauge-fixed kernels in the note are complete.

## 4. Generic lower converse

On \(a=1,c=t\), the only denominators in the kernel and lower solution are
powers of \(t\), and this stratum assumes \(t\ne0\).  The raw-kernel
completeness separately assumes \(t\ne3,3/2\); there is no hidden
specialization of a generic formula at either resonance.

The complete \(E_6\) coefficient table in the verifier has lower-unknown
matrix rank \(10\).  Its proposed ten substitutions are its unique
solution.  The deductions use only
\[
t\ne0,\qquad 2t-3\ne0;
\]
the separate condition \(t\ne3\) entered already at \(E_7\).

After that solution, the \(E_5\) matrix in
\(\ell_{12},\ell_{13},\ell_{22},\ell_{23}\) has rank \(4\).
For example, an exact maximal minor is
\[
144(2t-3)^2\ne0.
\]
Thus the four displayed \(E_5\) formulas are necessary and sufficient,
not an ansatz.  They give
\[
\operatorname{col}_2(L)=w_1v,\qquad
\operatorname{col}_3(L)=w_2v
\]
as polynomial identities.  This includes \(w_1=0\), \(w_2=0\), and
\(w_1=w_2=0\), without division by either parameter.

## 5. First resonance \(c=3a\)

The enlarged gauge-fixed kernel has dimension \(10\), as required.
The first \(E_6\) squares are exactly
\[
[y^5z]E_6=-\frac{16}{3}w_3^2,\qquad
[yz^5]E_6=\frac{16}{3}w_5^2.
\]
After \(w_3=w_5=0\), the triangular coefficients are
\[
\begin{array}{c|c}
x^5y&3(Br_1-2\beta_1)\\
x^5z&-3(Br_2-2\beta_2)\\
x^4y^2&3(r_1^2-4\beta_3)\\
x^4z^2&-3(r_2^2-4\beta_5)\\
y^4z^2&-12(\alpha_3-\beta_3)\\
y^2z^4&12(\alpha_5-\beta_5).
\end{array}
\]
Substitution leaves the two exact squares
\[
-\frac23(3r_1+2w_1)^2,\qquad
\frac23(3r_2+2w_2)^2.
\]
Over \(\mathbb C\) these force \(r_i=-2w_i/3\).  The remaining linear
\(E_6\) system has rank \(8\) in the ten displayed lower unknowns; its
two free variables are exactly \(\ell_{32},\ell_{33}\), and row reduction
reproduces (17).  This proves the full \(E_6\) converse.

After introducing \(s_1,s_2\), the \(E_5\) matrix in the four remaining
linear entries has constant rank \(4\), with exact maximal minor \(1296\).
Its unique solve is (19), and its complete residual is
\[
\frac29x^2yz(s_1y-s_2z)K_1.
\]
Thus \(K_1s_1=K_1s_2=0\), with no cancellation.  On \(K_1\ne0\) both
\(s_i\) vanish.  On \(K_1=0\), the independent \(E_4\) coefficients are
\[
-\frac8{27}s_1^2,\qquad \frac8{27}s_2^2,
\]
so they again vanish.  The resulting columns are \(w_1v,w_2v\), including
all zero specializations.

## 6. Second resonance \(2c=3a\)

Here the exact first squares are
\[
[x^2y^4]E_6=\frac{16}{3}w_3^2,\qquad
[x^2z^4]E_6=-\frac{16}{3}w_5^2.
\]
After they vanish, the stated \(x^4y^2,x^4z^2\) squares force
\(r_i=-2w_i/3\).  The remaining \(E_6\) matrix again has rank \(8\) in
ten lower unknowns with precisely \(\ell_{32},\ell_{33}\) free, and its
row reduction is exactly (25).

The \(E_5\) matrix for the other four linear entries has constant rank
\(4\), witnessed by a maximal minor \(5184\).  Its unique solve is (27),
and the complete residual is
\[
-\frac29x^4(s_1y-s_2z)K_2.
\]
The \(K_2\ne0\) branch gives \(s_1=s_2=0\).  On \(K_2=0\), the exact
\(E_4\) coefficients
\[
\frac8{27}s_1^2,\qquad-\frac8{27}s_2^2
\]
give the same conclusion.  The two final columns are exactly \(w_1v,w_2v\).

## 7. The two projective endpoints

At \(c=0,a\ne0\), the two \(E_6\) squares force \(w_1=w_2=0\).  The
remaining lower-unknown matrix has rank \(10\), so (33) is its unique
solution.  The \(E_5\) matrix has constant rank \(4\), with a maximal
minor \(1296\), and its unique solution is (34).  Consequently
\[
\operatorname{col}_2(L)=r_1v,\qquad
\operatorname{col}_3(L)=r_2v,
\]
also when one or both \(r_i\) vanish.

At \(a=0,c\ne0\), the \(E_6\) lower-unknown matrix has rank \(10\), so
(36) is its unique solution.  The \(E_5\) matrix has constant rank \(4\),
with a maximal minor \(576\), and its unique solution is (37).  Hence the
columns are \(w_1v,w_2v\), again including every zero specialization.

These endpoint calculations also show why neither point may be inferred by
substituting into the generic formulas: \(t=0\) is singular there, while
\(a=0\) is the missing point of the \(a=1\) affine chart.  Both were
instead computed directly.

## 8. Determinant exits and theorem scope

Every leaf ends in a polynomial proportional-column identity, never in a
division by a column factor:
\[
\begin{array}{c|c}
\text{leaf}&(\operatorname{col}_2,\operatorname{col}_3)\\ \hline
\text{generic, both resonances, }a=0&(w_1v,w_2v)\\
c=0&(r_1v,r_2v).
\end{array}
\]
Therefore \(\det L=0\) on every specialization.  This contradicts the
degree-zero Keller equation \(\det L\ne0\).

Combining this result with the separately audited fixed point
\((a,c)=(0,0)\) removes every finite companion in this outer chart.
The only companion type not removed **within this chart** is therefore
\((H_3)_3=xq\), with residual outer parameter orbits \(a=0\) and
\(a\ne0\).  The note correctly refrains from claiming either of those
orbits is solved.

## 9. Executable and fail-closed checks

All supplied commands passed:

```text
line-(2,2) remaining finite-companion outer-infinity SymPy checks passed
line-(2,2) remaining finite-companion outer-infinity PARI/GP checks passed
line-(2,2) remaining outer-infinity fail-closed tests passed
```

The SymPy run took about 17 seconds and peaked below 70 MB RSS on this
machine.  The Python verifier rejects optimized mode before any
optimization-sensitive check.  Its substantive checks use explicit
exceptions, not `assert`.

The strict GP wrapper propagates a nonzero status, rejects `***`, and
requires exact whole-output equality with the success sentinel.  In
addition to the supplied fault test, I injected:

- a GP diagnostic followed by the genuine sentinel;
- the genuine sentinel followed by extra output.

Both were rejected.  No fail-open path was found.

## 10. Package-local correction and certificate-coverage observation

The original raw-rank table described its \((1,t)\) row by
\(c(3a-c)(3a-2c)\ne0\).  That condition also holds at \(a=0,c\ne0\),
so it overlapped the separately listed marked-mixed endpoint, even though
that endpoint cannot be normalized to \((1,t)\).  I corrected the row to
say “generic with \(a\ne0\)” explicitly.  This is an orbit-ledger
correction only; the dedicated \(a=0\) calculation was already present
and correct.

The supplied SymPy verifier proves every proposed substitution and records
the decisive squares, but it does not itself explicitly assert all of the
lower coefficient-matrix ranks quoted above.  That is a certificate
coverage limitation, not a theorem defect: the direct rank computations
in this audit establish the missing converses, and the note's triangular
identities are correct.  No source patch is required for the mathematical
claim.

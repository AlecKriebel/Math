# Permutation and reshuffling contraction audit

**Date:** 2026-07-29
**Scope:** arbitrary exceptional reflection/projection unless a subsection is
explicitly labeled as a limitation model
**Status:** exact identities and an exact negative audit; no
four-divisibility obstruction

## 1. Conclusion

Closing the three-site cubic relation against the six tensor-permutation
operators does not produce a new scalar invariant.

More precisely:

1. the identity closure is automatic from \(H^2=I\);
2. the \(F_{13}\) closure and both three-cycle closures cancel identically
   for every two-site operator \(H\), even before imposing the cubic;
3. the \(F_{12}\) and \(F_{23}\) closures are only single
   Hilbert--Schmidt functionals of the already-known outer partial-trace
   identities.

The one genuinely unrecorded ordinary partial contraction is the middle
one.  In projection form it says

\[
\boxed{
\operatorname{Tr}_2(P_{12}P_{23}P_{12})
=
\operatorname{Tr}_2(P_{23}P_{12}P_{23}).
}
\tag{1}
\]

Its common value \(M\) is positive, has scalar marginals, and obeys

\[
\boxed{
\frac d6 I_{d^2}\leq M\leq\frac d2I_{d^2},\qquad
\operatorname{Tr}_1M=\operatorname{Tr}_3M=\frac{d^2}{4}I_d,\qquad
\operatorname{Tr}M=\frac{d^3}{4}.
}
\tag{2}
\]

These constraints do not contain a parity obstruction: at \(d=6\), the
scalar matrix \(M=\frac32I_{36}\) satisfies all of them.

The negative result remains true after a substantial enlargement of the
scalar closures.  Let \(U_\pi\) be the six permutation operators on
\(V^{\otimes3}\), and partially transpose any subset of their three sites.
There are \(6\cdot2^3=48\) resulting scalar tests.  An exact \(d=6\)
standard Hermitian involution satisfies every one of these 48 contracted
cubic equations while failing the cubic equation itself.  Thus no argument
using only these permutation/Brauer scalar shadows can prove \(4\mid d\).

The obstruction, if one exists, must retain genuinely operator-valued
overlap information.  In this audit the already-known outer channel
identities detect the \(d=6\) limitation model, while every scalar
permutation/partial-transpose closure and even the middle operator
contraction miss it.

## 2. All six tensor-permutation closures

Put

\[
A=H_{12},\qquad B=H_{23},
\]

and, for a scalar \(c\), define the residual

\[
\Delta_c(H)=ABA-BAB-c(A-B).
\tag{3}
\]

For the exceptional relation, \(c=1/3\).  Let \(F_{ij}\) denote the
transposition of tensor sites \(i,j\), and let \(C,C^{-1}\) denote the two
three-cycles.

### Proposition 2.1

For every \(H\in\operatorname{End}(V\otimes V)\),

\[
\operatorname{Tr}(F_{13}\Delta_c(H))
=\operatorname{Tr}(C\Delta_c(H))
=\operatorname{Tr}(C^{-1}\Delta_c(H))=0.
\tag{4}
\]

If \(H^2=I\), then also

\[
\operatorname{Tr}\Delta_c(H)=0.
\tag{5}
\]

The remaining two closures are

\[
\operatorname{Tr}(F_{12}\Delta_c(H))
=\operatorname{Tr}\!\left(
F\,\operatorname{Tr}_3\Delta_c(H)\right),
\tag{6}
\]

\[
\operatorname{Tr}(F_{23}\Delta_c(H))
=\operatorname{Tr}\!\left(
F\,\operatorname{Tr}_1\Delta_c(H)\right).
\tag{7}
\]

Here \(F\) is the flip on the two untraced tensor sites.  Consequently the
six full closures consist of four tautologies and one scalar shadow of each
of the two outer partial-trace equations.

### Proof

Choose any finite tensor expansion

\[
H=\sum_r A_r\otimes B_r.
\]

Then

\[
ABA
=\sum_{r,s,t}
A_rA_t\otimes B_rA_sB_t\otimes B_s,
\tag{8}
\]

\[
BAB
=\sum_{r,s,t}
A_s\otimes A_rB_sA_t\otimes B_rB_t.
\tag{9}
\]

For simple tensors,

\[
\begin{aligned}
\operatorname{Tr}(F_{13}(X\otimes Y\otimes Z))
 &=\operatorname{Tr}(XZ)\operatorname{Tr}Y,\\
\operatorname{Tr}(C(X\otimes Y\otimes Z))
 &=\operatorname{Tr}(XYZ),\\
\operatorname{Tr}(C^{-1}(X\otimes Y\otimes Z))
 &=\operatorname{Tr}(XZY).
\end{aligned}
\tag{10}
\]

Substitution of (8)--(9) proves the three cubic cancellations by cyclicity
of trace and dummy-index relabeling.  For \(F_{13}\), interchange \(r,t\)
in the first sum and cyclically rotate both trace factors.  For \(C\), use
the relabeling

\[
(r,s,t)\longmapsto(s,t,r).
\]

For \(C^{-1}\), use

\[
(r,s,t)\longmapsto(t,r,s)
\]

and one cyclic rotation of the resulting six-factor trace.  The linear
terms cancel by (10) as well:

\[
\operatorname{Tr}(F_{13}A)=\operatorname{Tr}(F_{13}B),
\qquad
\operatorname{Tr}(CA)=\operatorname{Tr}(CB),
\qquad
\operatorname{Tr}(C^{-1}A)=\operatorname{Tr}(C^{-1}B).
\]

For the identity closure, cyclicity and \(A^2=B^2=I\) give

\[
\operatorname{Tr}(ABA)=\operatorname{Tr}B,\qquad
\operatorname{Tr}(BAB)=\operatorname{Tr}A.
\]

The two traces are both \(d\operatorname{Tr}H\), and the linear term has
zero trace.  This proves (5).  Equations (6)--(7) are the defining flip
trace identity after first tracing the spectator tensor factor.  \(\square\)

### Consequence

No scalar obtained by closing the cubic residual with an element of the
group algebra \(\mathbb C[S_3]\) can give more information than the outer
partial-trace identities.  In particular, this route cannot produce a new
determinant, signature, or rank whose integrality might distinguish
\(d=4m\) from \(d=4m+2\).

## 3. The middle partial contraction

Let

\[
p=P_{12},\qquad q=P_{23}
\]

for an arbitrary exceptional projection.  Automatic standardness gives

\[
\operatorname{Tr}_1P=\operatorname{Tr}_2P=\frac d2I_d.
\tag{11}
\]

Taking the middle partial trace of

\[
pqp-qpq=\frac13(p-q)
\]

and using (11) proves (1).

There is a useful positive description of the common value.  The
common-one projection of \(p,q\) is

\[
e=\frac32pqp-\frac12p.
\tag{12}
\]

Put

\[
K=\operatorname{Tr}_2e.
\]

Since \(0\leq e\leq p\),

\[
0\leq K\leq\operatorname{Tr}_2p=\frac d2I_{d^2}.
\tag{13}
\]

Equation (12) gives

\[
\boxed{
M=\frac23K+\frac d6I_{d^2}.
}
\tag{14}
\]

This proves the operator bounds in (2).

For completeness, the outer marginal of \(e\) follows directly:

\[
\operatorname{Tr}_3e
=\frac32p\,\operatorname{Tr}_3(q)\,p
-\frac12\operatorname{Tr}_3p
=\frac d4p.
\tag{15}
\]

The other outer marginal is its right-hand analogue.  Tracing once more
and using (11) gives

\[
\operatorname{Tr}_1K=\operatorname{Tr}_3K=\frac{d^2}{8}I_d,
\qquad
\operatorname{Tr}K=\frac{d^3}{8}.
\tag{16}
\]

Equations (14)--(16) prove the remaining statements in (2).

### Reflection form

Put \(H=I-2P\), and define

\[
S=\operatorname{Tr}_2(pq).
\]

Expansion gives

\[
\operatorname{Tr}_2(H_{12}H_{23}H_{12})
=4(S+S^*)-8M.
\tag{17}
\]

The same expression is obtained from
\(\operatorname{Tr}_2(H_{23}H_{12}H_{23})\), precisely because of (1).
The common operator in (17) is Hermitian and has zero partial trace on
either remaining site.  It need not be assumed to vanish.  It does vanish
for the published sparse witness, but the proof above does not promote
that feature to a universal identity.

## 4. Why positivity and inertia do not force four-divisibility

At \(d=6\), set

\[
M=\frac32I_{36},\qquad K=\frac34I_{36}.
\tag{18}
\]

Then (14) holds, and

\[
\frac d6I\leq M\leq\frac d2I,\qquad
0\leq K\leq\frac d2I.
\]

Moreover,

\[
\operatorname{Tr}M=54=\frac{d^3}{4},\qquad
\operatorname{Tr}_1M=\operatorname{Tr}_3M=9I_6
=\frac{d^2}{4}I_6,
\]

\[
\operatorname{Tr}K=27=\frac{d^3}{8},\qquad
\operatorname{Tr}_1K=\operatorname{Tr}_3K=\frac92I_6
=\frac{d^2}{8}I_6.
\]

This is a limitation model for the consequences derived in Section 3.  It
is not claimed to arise as \(\operatorname{Tr}_2(pqp)\) for a projection
\(P\).  It proves that positivity, determinant bounds, inertia, total
trace, and scalar marginals of the middle contraction alone cannot exclude
\(d=6\).

## 5. Forty-eight permutation/partial-transpose shadows

Fix a conjugation on \(V\).  For \(\pi\in S_3\), let \(U_\pi\) be the
corresponding tensor-permutation operator.  For a subset
\(S\subseteq\{1,2,3\}\), let \(\Gamma_S\) denote partial transpose on the
sites in \(S\).  The 48 scalar Brauer-type shadows of the cubic are

\[
\operatorname{Tr}\!\left(
\bigl((U_\pi)^{\Gamma_S}\bigr)^*
\Delta_{1/3}(H)\right)=0.
\tag{19}
\]

Partial transpose of a flip replaces a through-string by the usual
maximally-entangled cup-cap, so (19) includes the elementary scalar
closures suggested by partial transpose and reshuffling.

### Proposition 5.1: exact \(d=6\) limitation involution

Let

\[
V=\mathbb C^2\otimes\mathbb C^3,\qquad
Z_6=Z\otimes I_3,\qquad X_6=X\otimes I_3,
\]

and put

\[
H=Z_6\otimes X_6\in\operatorname{End}(V\otimes V).
\tag{20}
\]

Then

\[
H=H^*,\qquad H^2=I,\qquad
\operatorname{Tr}_1H=\operatorname{Tr}_2H=0,
\tag{21}
\]

and \(H\) has eighteen eigenvalues of each sign.  Thus
\((I-H)/2\) is a rank-18 standard projection.

Nevertheless,

\[
\Delta_{1/3}(H)=\frac23(H_{12}-H_{23})\ne0,
\qquad
\|\Delta_{1/3}(H)\|_2^2=192.
\tag{22}
\]

It satisfies all 48 scalar equations (19), and also

\[
\operatorname{Tr}_2\Delta_{1/3}(H)=0.
\tag{23}
\]

### Proof

The matrices \(Z_6,X_6\) are traceless anticommuting Hermitian
involutions.  Hence

\[
H_{12}H_{23}H_{12}=-H_{23},\qquad
H_{23}H_{12}H_{23}=-H_{12},
\]

which proves the first formula in (22).  The two summands
\(H_{12},H_{23}\) are Hilbert--Schmidt orthogonal and each has squared norm
\(d^3=216\), proving the norm formula.

For (19), regroup the three copies of
\(\mathbb C^2\otimes\mathbb C^3\) into their qubit and qutrit tensor
factors.  Tensor permutations and their sitewise partial transposes factor
across this regrouping.  Every resulting qubit closure of

\[
Z\otimes X\otimes I-I\otimes Z\otimes X
\]

contains either a one-Pauli loop or an \(X,Z\) two-Pauli loop.  It vanishes
by

\[
\operatorname{Tr}X=\operatorname{Tr}Z
=\operatorname{Tr}(XZ)=0.
\]

Equivalently, this is a finite check of eight cup-cap choices for each of
the six permutations.  The exact verifier enumerates all 48 rather than
relying on diagram inspection.  Finally, (23) follows immediately by
tracing the middle Pauli in each summand.  \(\square\)

The outer contractions do detect this fake:

\[
\operatorname{Tr}_3\Delta_{1/3}(H)=4H,\qquad
\operatorname{Tr}_1\Delta_{1/3}(H)=-4H.
\tag{24}
\]

This precisely locates the information loss.  Scalar permutation and
partial-transpose closures cannot replace the operator-valued channel
relations already obtained from the outer partial traces.

## 6. Verification

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_permutation_contraction_audit.py
```

The verifier:

1. reconstructs the published \(d=4\) witness over
   \(\mathbb Q(\sqrt2,\sqrt3)\);
2. checks its cubic and middle-contraction identities exactly;
3. constructs (20) with integer matrices;
4. checks standardness, signature, the nonzero residual and its exact norm;
5. enumerates all \(48\) partially-transposed permutation pairings exactly;
6. checks the \(d=6\) scalar middle-marginal model using rational
   arithmetic.

Recorded output:

```text
results/permutation_contraction_audit_exact.txt
```

SHA-256 at creation:

```text
64023a78384e5017a259913d6c5243c02752b893e42a145b04aafa82428e60f3  verifiers/verify_permutation_contraction_audit.py
9200cc77cf7d417857ff79f262c7acd30997212de75b1561516d1692206e79d5  results/permutation_contraction_audit_exact.txt
```

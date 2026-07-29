# Exact audit of the diagonal-regular group ansatz

**Date:** 2026-07-28

**Status:** PROVED within the stated ansatz; exact \(d=4\) calibration
independently reproduced
**Scope:** the no-go applies to the complete diagonal-regular ansatz for
groups of order \(d\equiv2\pmod4\), including \(C_6\) and \(S_3\).  It is
not a no-go for arbitrary exceptional matrices.

## 1. Result

Let \(G\) be a finite group of even order \(d\), let \(L_x\) denote its
left-regular representation on \(V=\mathbb C[G]\), and let
\[
 h=h^*=h^{-1}\in M_d(\mathbb C),\qquad \operatorname{Tr}h=0.
\]
In the original tensor coordinates, the diagonal-regular ansatz searched
by `scripts/d6_group_relative_search.py` is
\[
 \boxed{
 H=\sum_{x\in G}|x\rangle\langle x|\otimes h_x,
 \qquad h_x=L_xhL_x^*.
 }
 \tag{1}
\]
Equivalently, after the relative-coordinate permutation
\[
 |x,g\rangle\longmapsto |x,xg\rangle,
\]
it is \(I_d\otimes h\).

### Theorem

If (1) satisfies
\[
 H_{12}H_{23}H_{12}-H_{23}H_{12}H_{23}
 =\frac13(H_{12}-H_{23}),
 \tag{2}
\]
then
\[
 \boxed{4\mid d.}
 \tag{3}
\]
Consequently, neither \(G=C_6\) nor \(G=S_3\) can yield a
six-dimensional exceptional solution through this ansatz.

This is an exact theorem, not an inference from the retained numerical
failures.  In fact, the group covariance is unnecessary once (1) is seen
to be rank-one controlled: the proof applies to every reflection of the
form
\[
 H=\sum_{x=1}^d |x\rangle\langle x|\otimes A_x.
 \tag{4}
\]

## 2. Why the rank-one controlled theorem applies

Put
\[
 P=\frac{I-H}{2}.
\]
For every \(x\), the rank-one projection
\[
 z_x=|x\rangle\langle x|
\]
satisfies
\[
 [z_x\otimes I,P]=0.
\tag{5}
\]
The controlled-leg divisibility theorem in
`notes/controlled_leg_divisibility.md` states that if a rank-\(r\)
projection \(z\) belongs to this one-leg commutant, then
\[
 8\mid r d^2.
\tag{6}
\]
Taking \(r=1\) gives \(8\mid d^2\).  In \(2\)-adic valuations,
\[
 2v_2(d)\ge3,
\]
so \(v_2(d)\ge2\) and hence \(4\mid d\).

For completeness, the integer obstruction behind (6) is short.  Restrict
\[
 p=P_{12},\qquad q=P_{23}
\]
to
\[
 zV\otimes V\otimes V,
\]
which has dimension
\[
 N=r d^2.
\]
Automatic standardness gives
\[
 \operatorname{rank}p=\operatorname{rank}q=\frac N2,
 \qquad
 \operatorname{Tr}(pq)=\frac N4.
\tag{7}
\]
The two-projection relation
\[
 pqp-qpq=\frac13(p-q)
\tag{8}
\]
has only common-zero blocks, common-one blocks, and generic
two-dimensional blocks with squared principal cosine \(1/3\).
If \(a\) is the common-one multiplicity and \(g\) is the number of generic
blocks, then
\[
 a+g=\frac N2,\qquad a+\frac g3=\frac N4.
\]
Therefore
\[
 a=\frac N8.
\tag{9}
\]
Since \(a\) is an integer, \(8\mid N=r d^2\).

Notice that the proof uses neither the Fourier theory of \(G\) nor
irreducibility of its regular representation.  It therefore excludes the
full \(h\)-Grassmannian searched for both \(C_6\) and \(S_3\).

## 3. Exact reduced cubic equations

Although the divisibility theorem is sufficient, it is useful to record
the complete reduction of (2).  With
\(\Pi_y=|y\rangle\langle y|\), direct multiplication gives, on the block
with first coordinate \(x\),
\[
\begin{aligned}
 &\sum_y h_x\Pi_yh_x\otimes h_y
 -\sum_{y,z}\Pi_yh_x\Pi_z\otimes h_yh_z\\
 &\qquad =
 \frac13\left(h_x\otimes I-\sum_y\Pi_y\otimes h_y\right).
\end{aligned}
\tag{10}
\]
Taking the \((y,z)\) matrix entry on the first displayed tensor factor
yields the equivalent operator identities
\[
\boxed{
 \sum_a (h_x)_{ya}(h_x)_{az}h_a
 -(h_x)_{yz}h_yh_z
 =\frac13\bigl((h_x)_{yz}I-\delta_{yz}h_y\bigr).
}
\tag{11}
\]
These are only \(d^4\) equations in \(M_d\), rather than one dense equation
in \(M_{d^3}\).

Automatic standardness and the canonical-channel contraction imply that
all diagonal entries of all \(h_x\) vanish.  The diagonal case \(y=z\) of
(11) then becomes
\[
\boxed{
 \sum_a |(h_x)_{ya}|^2h_a=-\frac13h_y.
}
\tag{12}
\]
Thus every unistochastic matrix
\[
 W^{(x)}_{ya}=|(h_x)_{ya}|^2
\]
acts by the eigenvalue \(-1/3\) on the matrix-valued orbit
\((h_a)_{a\in G}\).  Equation (12) is a useful exact filter for any future
controlled search.

Here is the channel step explicitly.  Put \(p_x=(I-h_x)/2\).  The canonical
right channel of \(P\) is the Schur multiplier
\[
 \mathcal E_R(X)_{ab}
 =\frac2d\operatorname{Tr}(p_ap_b)X_{ab}
 =\frac{1+c_{a,b}}2X_{ab},
 \qquad
 c_{a,b}=\frac1d\operatorname{Tr}(h_ah_b).
\tag{13}
\]
The universal contraction is
\[
 \mathcal E_R(h_x)=\frac13h_x.
\tag{14}
\]
Since the diagonal Schur symbol in (13) equals \(1\), (14) forces
\((h_x)_{aa}=0\).  If \((h_x)_{ab}\ne0\), it also forces
\[
 c_{a,b}=-\frac13.
\tag{15}
\]

## 4. An independent cyclic \(C_6\) Fourier obstruction

There is a second, group-specific proof for \(C_6\).  It is redundant with
Section 2 but audits the leg orientation and the reduced equations by a
different mechanism.

Use additive notation for \(C_6\), and let \(K=F^*hF\), where \(F\) is the
unitary Fourier matrix.  Define the symmetric probability measures
\[
 w_t=\frac16\sum_u|h_{u,u+t}|^2,
 \qquad
 q_r=\frac16\sum_p|K_{p,p-r}|^2.
\tag{16}
\]
Hermiticity gives
\[
 w_{-t}=w_t,\qquad q_{-r}=q_r,
\]
and involutivity gives
\[
 \sum_t w_t=\sum_rq_r=1.
\]
The canonical channel identity forces \(h_{uu}=0\), while automatic
standardness \(\sum_xL_xhL_x^*=0\) forces \(K_{pp}=0\).  Hence
\[
 w_0=q_0=0.
\tag{17}
\]

Let
\[
 S=\operatorname{supp}w,\qquad F=\operatorname{supp}q.
\]
Equation (12), read in a nonzero Fourier matrix entry of \(h_x\), gives
\[
 \widehat w(r)=-\frac13\qquad(r\in F).
\tag{18}
\]
The Schur form of the canonical channel gives the reciprocal condition
\[
 \widehat q(t)=-\frac13\qquad(t\in S).
\tag{19}
\]

Write a symmetric probability measure on \(C_6\setminus\{0\}\) as
\[
 \mu_{\pm1}=a,\qquad
 \mu_{\pm2}=b,\qquad
 \mu_3=c,\qquad
 2a+2b+c=1.
\tag{20}
\]
Its three nontrivial Fourier types are
\[
\widehat\mu(1)=a-b-c,\qquad
\widehat\mu(2)=-a-b+c,\qquad
\widehat\mu(3)=-2a+2b-c.
\tag{21}
\]
There are only seven nonempty inverse-closed supports, indexed by the
nonempty subsets of
\[
\{\{\pm1\},\{\pm2\},\{3\}\}.
\]
Solving (20)--(21) over \(\mathbb Q\) shows:

- no singleton support can serve as the measure support in a feasible
  ordered pair;
- if the constrained Fourier support is a pair, then the measure support
  must be all three types;
- the reciprocal ordered pair would then require a pair support constrained
  on all three types, and no such measure exists.

Therefore no pair \((w,q)\) satisfies both (18) and (19).  This separately
excludes the cyclic \(C_6\) ansatz.  The exact seven-by-seven support replay
is included in `verifiers/verify_group_relative_exact.py`.

## 5. Exact \(V_4\) calibration

The numerical \(d=4\) calibration converged, for three retained seeds, to
phase/sign variants of a skew-conference matrix.  One exact representative
is
\[
 C=
 \begin{pmatrix}
 0&1&1&1\\
 -1&0&-1&1\\
 -1&1&0&-1\\
 -1&-1&1&0
 \end{pmatrix},
 \qquad
 C^T=-C,\qquad C^2=-3I_4.
\tag{22}
\]
Put
\[
 h=\frac{i}{\sqrt3}C.
\tag{23}
\]
Then \(h=h^*\), \(h^2=I_4\), and \(\operatorname{Tr}h=0\).  For
\(G=V_4\), define \(h_x=L_xhL_x^*\) and use (1).  Exact symbolic
calculation gives
\[
 \sum_xh_x=0,
\tag{24}
\]
\[
 \frac14\operatorname{Tr}(h_xh_y)
 =
 \begin{cases}
 1,&x=y,\\
 -1/3,&x\ne y,
 \end{cases}
\tag{25}
\]
and the full \(64\times64\) identity (2).

Thus the \(d=4\) calibration is a regular tetrahedron of four reflections
in Hilbert--Schmidt space.  Restricting \(P_{12},P_{23}\) to one fixed
first control coordinate gives a \(16\)-dimensional two-projection
representation with
\[
 (m_{11},m_{00},g)=(2,2,6),
\tag{26}
\]
exactly saturating the integer formula \(m_{11}=d^2/8=2\).

This exact reconstruction is proof-independent of the floating-point
optimizer.  No uniqueness or local-equivalence claim is made.

## 6. Provenance and replay

The discovery generator is
`scripts/d6_group_relative_search.py`.  Its predeclared seeds and raw
JSONL output are retained in

- `results/d6_group_relative_seed_manifest.json`;
- `results/d6_group_relative_runs.jsonl`;
- `results/d6_group_relative_candidates/`.

The three successful \(V_4\) calibrations were seeds
\[
26073311,\quad26073312,\quad26073313.
\]
They reached full cubic residuals between approximately
\(6.5\times10^{-11}\) and \(1.0\times10^{-10}\), after which (22)--(23)
were recognized and verified exactly.  The \(d=6\) numerical runs are now
logically superseded by the theorem in Section 2; their failure is not used
as evidence.

Run the exact verifier with

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_group_relative_exact.py
```

It checks:

1. the integer conference identities;
2. Hermiticity, involutivity, trace and both partial traces;
3. the full \(64\times64\) cubic relation;
4. the restricted two-projection multiplicities;
5. the exact \(C_6\) dual-Fourier support exhaustion;
6. the \(r=1,d=6\) divisibility arithmetic.

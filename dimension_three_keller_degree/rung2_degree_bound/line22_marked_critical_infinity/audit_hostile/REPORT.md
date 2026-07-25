# Hostile audit: marked-critical infinity orbit

**Verdict:** **PASS, with exposition and certificate-coverage corrections.**

The provisional theorem is correct for the single orbit
\[
p=x^2,\quad q=yz,\qquad
H_4=(p^2,q^2,0)^T,\qquad (H_3)_3=x^3.
\]
I found no omitted zero specialization, illegal division, or lower-degree
solution that can retain \(\det L_0\ne0\).

This package closes only the point \((a,c)=(0,0)\) in the
outer-critical-at-infinity chart
\[
H_4=((p-aq)^2,q^2,0),\qquad R_3=x(p-cq).
\]
It does not address the rest of that chart, its two mixed resonances, its
noncritical triple endpoint, or its companion-at-infinity orbits.

No theorem or global document was modified.

## 1. Complete \(E_7\) quotient — PASS

For completely general cubics \(U,V\) and quadratic \(W\), direct
expansion gives
\[
E_7=-2x^2q\,\delta(3U-4xW),\qquad
\delta=z\partial_z-y\partial_y.
\]
The action of \(\delta\) on cubics has rank \(8\), with kernel
\[
\langle x^3,xq\rangle.
\]
Hence the raw \(36\times26\) coefficient matrix has rank \(8\) and
nullity \(18\), and
\[
U=\frac43xW+a x^3+A xq,
\]
while \(V,W\) are otherwise arbitrary.

The gauge-fixed family has fourteen parameters:

- six coefficients of \(W\);
- seven retained coefficients of \(V\);
- \(A\).

The four removed directions are independent:

- \(a x^3\) in \(U\), removed by a first-component target shear;
- the \(x^3\) coefficient of \(V\), removed by a second-component target
  shear;
- \(\partial_y(q^2)=2yz^2\);
- \(\partial_z(q^2)=2y^2z\).

An independent \(26\times18\) direction matrix has rank \(18\) and is
annihilated by the raw \(E_7\) matrix.  Thus the displayed quotient is
complete, not merely a family of solutions.

Affine translation changes lower homogeneous pieces, but this loses no
condition.  The new linear term is \(JF(d)X\), and the Keller hypothesis
gives
\[
\det JF(d)=\text{the same nonzero constant}.
\]
The changed quadratic and linear coefficients remain completely general at
the stage where the translations are used.

## 2. Target-shear ledger — PASS, but it should be stated

For a first-component target shear \(F_1\mapsto F_1+\lambda F_3\),
\[
\begin{aligned}
U&\mapsto U+\lambda x^3,\\
(H_2)_1&\mapsto(H_2)_1+\lambda W,\\
\operatorname{row}_1(L_0)&\mapsto
\operatorname{row}_1(L_0)+\lambda\operatorname{row}_3(L_0).
\end{aligned}
\tag{S1}
\]
The analogous second-component shear changes \(V,(H_2)_2\), and row 2.
Both target matrices have determinant one, so
\[
\det L_0\quad\text{is unchanged.}
\]

After \(w_1=w_2=w_3=w_5=0\), removing the tied term
\((4/3)w_0x^3\) uses \(\lambda=-4w_0/3\).  In first-component lower
coordinates,
\[
\begin{aligned}
u_0'&=u_0-\frac43w_0^2,\\
u_4'&=u_4-\frac43w_0w_4,\\
\ell_{1j}'&=\ell_{1j}-\frac43w_0\ell_{3j}.
\end{aligned}
\tag{S2}
\]
All case formulas written with \(H_{3,1}=Cxq\) use these post-shear
coordinates, relabelled without primes.

This is mathematically safe, and the independent audit verifies it
exactly.  The provisional note should state (S1)--(S2), especially before
defining \(K\).  In the \(A=0,C\ne0\) case, \(w_4=3C/4\), so the displayed
\[
K=2Cw_0+3u_4
\]
uses post-shear \(u_4\).  In pre-shear coordinates the same expression is
\[
K=3u_4-Cw_0.
\]

## 3. Complete \(E_6\) radical and converse — PASS

The lower-unknown coefficient matrix in raw \(E_6\) has constant rank
\(4\).  A constant four-by-four minor solves exactly for
\[
u_1,u_2,u_3,u_5.
\]
The square coefficients
\[
-\frac{16}{3}w_3^2,\qquad \frac{16}{3}w_5^2
\]
force
\[
w_3=w_5=0.
\]
After setting
\[
C=A+\frac43w_4
\]
and substituting
\[
\begin{aligned}
u_1&=\frac43\ell_{32}+\frac49w_0w_1,&
u_2&=\frac43\ell_{33}+\frac49w_0w_2,\\
u_3&=\frac29w_1^2,&
u_5&=\frac29w_2^2,
\end{aligned}
\]
every remaining \(E_6\) coefficient is one of exactly eight products:
\[
\begin{array}{c|c}
\text{monomial}&\text{coefficient}\\ \hline
x^5y&-3Av_1\\
x^5z&3Av_2\\
x^4y^2&-6Av_3\\
x^4z^2&6Av_5\\
x^3y^3&-9Av_6\\
x^3z^3&9Av_9\\
xy^3z^2&-2Cw_1\\
xy^2z^3&2Cw_2
\end{array}
\]
and all other coefficients vanish.

This proves both necessity and converse and yields exactly the four
specialization-safe leaves
\[
(A,C)\in
(\mathbb C^\times,\mathbb C^\times),\
(\mathbb C^\times,0),\
(0,\mathbb C^\times),\
(0,0).
\]

## 4. The four lower leaves

### 4.1 \(A\ne0,C\ne0\) — PASS

\(E_6\) gives \(w_1=w_2=0\) and \(V=v_4xq\).  In post-shear
coordinates,
\[
H_3=(Cxq,v_4xq,x^3).
\]
The two \(E_5\) coefficients
\[
-2C\ell_{32},\qquad2C\ell_{33}
\]
kill \(\ell_{32},\ell_{33}\).  Two further coefficients are then
\[
6\ell_{12},\qquad-6\ell_{13}.
\]
Thus rows 1 and 3 of \(L_0\) are both supported in column 1 and
\(\det L_0=0\).  The values of \(B=v_4,w_0,w_4,u_0,u_4\) and every
unused lower coefficient may be zero without changing the exit.

### 4.2 \(A\ne0,C=0\) — PASS

The raw \(E_5\) cubes are
\[
\frac89w_1^3,\qquad-\frac89w_2^3,
\]
so \(w_1=w_2=0\).  The complete remaining \(E_5\) system is
\[
\begin{aligned}
-3Ah_1&=0,&3Ah_2&=0,&-6Ah_3&=0,&6Ah_5&=0,\\
\frac23(9\ell_{12}-4w_0\ell_{32})&=0,&
-\frac23(9\ell_{13}-4w_0\ell_{33})&=0.
\end{aligned}
\]
Because \(A\ne0\), this gives the four stated \(h\)-values and
\[
\ell_{12}=\frac49w_0\ell_{32},\qquad
\ell_{13}=\frac49w_0\ell_{33}.
\]
The \(E_4\) squares
\[
-\frac83\ell_{32}^2,\qquad
\frac83\ell_{33}^2
\]
finish the branch.  This remains valid for
\(B=0,w_0=0,u_4=0\).

### 4.3 \(A=0,C\ne0\) — PASS

The first \(E_5\) coefficients kill
\[
v_3,v_5,v_6,v_9,\ell_{32},\ell_{33}.
\]
The exact remainder is
\[
\begin{aligned}
-Kv_1&=0,&Kv_2&=0,\\
\frac34(C^2v_1+8\ell_{12})&=0,&
-\frac34(C^2v_2+8\ell_{13})&=0,
\end{aligned}
\qquad
K=2Cw_0+3u_4.
\]

If \(K\ne0\), this immediately makes the relevant row entries zero and
\(\det L_0=0\).

If \(K=0\), \(E_4\) forces
\[
h_1=\frac23v_1w_0,\qquad
h_2=\frac23v_2w_0,\qquad
h_3=h_5=0.
\]
There are also two omitted, harmless \(E_4\) products
\[
v_1Q=0,\qquad v_2Q=0,
\tag{E4-extra}
\]
where
\[
Q=9Cv_4+24\ell_{31}-36u_0-32w_0^2.
\]
They only further restrict the solution set and are not needed for the
exit.

After the complete \(E_5/E_4\) substitutions, the necessary \(E_2\)
coefficient is
\[
[x^2]E_2=-\frac38C^2
(v_1\ell_{23}-v_2\ell_{22}),
\]
and direct polynomial expansion gives
\[
\boxed{\det L_0=\frac{\ell_{31}}3[x^2]E_2.}
\]
This identity remains valid when any of
\[
v_1,\ v_2,\ w_0,\ u_4,\ \ell_{31}
\]
is zero.  It never divides by one of them.

### 4.4 \(A=C=0\) — PASS

Before the target shear, the same two cubes kill \(w_1,w_2\).  The shear
\(\lambda=-4w_0/3\) then removes \((4/3)w_0x^3\) with the lower effects
recorded in (S2).

In the canonical post-shear coordinates, the full \(E_5\) table includes
\[
\begin{aligned}
\frac23(9\ell_{12}+8w_0\ell_{32})&=0,\\
-\frac23(9\ell_{13}+8w_0\ell_{33})&=0,
\end{aligned}
\]
plus products of \(u_4\) with the noninvariant coefficients of \(V\).
Those products are deliberately not divided: when \(u_4=0\), \(V\) may
remain arbitrary.

Regardless of that specialization, \(E_4\) contains
\[
-\frac83\ell_{32}^2,\qquad
\frac83\ell_{33}^2.
\]
Hence \(\ell_{32}=\ell_{33}=\ell_{12}=\ell_{13}=0\), and
\(\det L_0=0\).  The cases \(w_0=0\), \(u_4=0\), or both are safe.

## 5. Division and specialization audit — PASS

No illegal division occurs.

- Squares and cubes are used only over \(\mathbb C\).
- \(A,C,K\) are divided conceptually only inside branches where they are
  explicitly nonzero.
- \(K=0\) has its own exact lower calculation.
- The resonant determinant identity does not divide by
  \(v_1,v_2,\ell_{31}\), or \(C\).
- \(w_0=0\) and \(u_4=0\) remain present in all relevant formulas.
- In \(A=C=0\), no division by \(u_4\) is used to reduce \(V\).
- Target shears have determinant one for every shear parameter, including
  zero.
- Source translations preserve the nonzero constant Jacobian at the new
  origin.

The four \(A,C\) leaves and the two \(K\) leaves exhaust every zero
specialization used in the proof.

## 6. Executable guards and fault injection — PASS

### SymPy

The supplied verifier explicitly rejects optimized mode before doing any
work:

```python
if not __debug__:
    raise RuntimeError(...)
```

Running it with `python -O` returns nonzero with the intended diagnostic.
Its substantive checks use explicit `require_zero` calls rather than
optimization-sensitive assertions.

### PARI/GP

The supplied strict runner:

- propagates a nonzero GP exit status;
- rejects any output containing `***`;
- requires the entire captured output to equal the one exact success
  sentinel.

The audit fake `gp` confirmed all of these behaviors.  It tested exact
success, a forged sentinel following a diagnostic, extra trailing output,
a wrong sentinel, and exit status \(7\).  Only exact success was accepted.

## 7. Corrections

These corrections do not change the theorem.

1. **Typesetting:** equation (4) is missing a `+` between
   \(v_5xz^2\) and \(v_6y^3\).
2. **Coordinate ledger:** state the lower effects (S1)--(S2) of every
   target shear and say explicitly that all later \(u_i,\ell_{ij}\) are
   post-shear variables.  In particular, clarify the coordinate used in
   the definition of \(K\).
3. **Affine-gauge ledger:** state that the \(y,z\) translations change
   lower terms but preserve invertibility of the new linear coefficient
   because it is \(JF(d)\).
4. **Complete \(K=0\) record:** either add the harmless products
   \(v_1Q=v_2Q=0\) from (E4-extra), or say that (18) lists only the four
   \(E_4\) equations needed later.
5. **Verifier-description accuracy:** the supplied scripts reconstruct the
   decisive identities, but several lower solves are checked only after
   substituting the proposed answer.  They do not explicitly assert the
   exact factors giving (13), (16)--(18), and (21), nor do they literally
   back-substitute the general \(E_6\) solution into every coefficient as
   claimed in the prose.  Add those exact assertions or narrow the
   verification description.  The independent audit script supplies all
   of these missing converses.

No correction is required to the theorem scope, \(E_7\) equation, raw
\(E_6\) radical, four-way split, degree-five cubes, degree-four squares,
resonant \(E_2\) identity, or either executable guard.

## 8. Reproducible audit artifacts

- `audit_exact_reconstruct.py` independently checks the raw \(E_7\)
  rank/kernel, target-shear ledger, complete \(E_6\) converse, all four
  lower branches, extra \(E_4\) products, and the resonant determinant
  factor.  It rejects optimized mode.
- `test_python_guard.sh` fault-injects `python -O`.
- `test_runner_faults.sh` and `fakebin/gp` exercise every strict-runner
  outcome described above.

# Independent PARI repair of the binary fixed-conic \(E_7\to E_6\) bridge

## Verdict

\[
\boxed{\textbf{PASS: legacy equations (7)--(9) are universally forced}}
\]

The retained calculation repairs the exact gap identified by the post-freeze
audit. It starts with the complete degree-eight cubic kernel, all 12
coefficients of \(V\), all 18 coefficients of \(H_2\), and all 9 entries of
the linear part \(L\). It parametrizes the full degree-seven affine fibre
using a constant nonzero minor, then substitutes that whole fibre into degree
six. The resulting \(r^2\) coefficients are exactly the legacy factors (7)
and (8), independent of every free coefficient of \(V,H_2,L\). The tangent
list (9), including all zero and intersection specializations, is exhaustive.

This is a pass for the disputed binary \(E_7\to E_6\) bridge only. The later
branch-specific endgames in the working note were not re-audited here from
their claimed complete lower-degree fibres. Therefore this package alone does
**not** promote the entire binary theorem or the global frozen row; that
larger promotion remains fail-closed pending a separate retained audit of
those endgames.

## 1. Exact setup and degree-eight completeness

Put
\[
D(s)=\det\!\left(L+sJH_2+s^2JH_3+s^3JH_4\right),\qquad E_k=[s^k]D(s).
\]
All computations are over \(\mathbb Q\) in PARI/GP 2.17.4.

For each of \(h=pq,p^2\), the linear \(E_8\) map from a completely general
ternary cubic vector (30 coefficients) has
\[
\operatorname{rank}E_8=12,\qquad \dim\ker E_8=18.
\]
The displayed normal
\[
H_3=V(p,q)+r\{(ap+bq)A_p+(cp+dq)A_q\}
       +\frac{r^2}{2}(eA_p+fA_q)
\]
has 18 independent parameters (12 in \(V\), six tangent parameters), lies in
that kernel, and hence is the complete \(E_8\) normal in both cases.

Write
\[
\begin{aligned}
V_1&=v_1p^3+v_2p^2q+v_3pq^2+v_4q^3,\\
V_2&=v_5p^3+v_6p^2q+v_7pq^2+v_8q^3,\\
V_3&=v_9p^3+v_{10}p^2q+v_{11}pq^2+v_{12}q^3.
\end{aligned}
\]
This report uses the checker's one-based indices.

## 2. Full degree-seven compatibility and affine fibre

In each case the \(E_7\) coefficient matrix in the 18 entries of \(H_2\) is
a constant rational matrix of rank \(7\). The same seven pivot coefficients
are
\[
w_4,w_5,w_6,w_{10},w_{12},w_{16},w_{18},
\]
and the constant pivot determinant is
\[
-524288=-2^{19}.
\]
Thus no parameter-dependent division or generic-rank assumption occurs.
The fibre has the 11 free entries
\[
w_1,w_2,w_3,w_7,w_8,w_9,w_{11},w_{13},w_{14},w_{15},w_{17}.
\]
Here the six monomials in each component of \(H_2\) are ordered as
\((p^2,pq,q^2,pr,qr,r^2)\).

### 2.1 Split roots \(h=pq\)

The raw left-null calculation returns 15 nonzero compatibility generators
(printed in full by the checker). Their set-theoretic radical is
\[
\sqrt{I_{7,pq}}=
\left\langle
e,f,b,c,\ (a-3d)v_4,\ (3a-d)v_9
\right\rangle.
\]
In particular it independently recovers \(e=f=b=c=0\), and also retains the
two \(V\)-compatibilities omitted from the abbreviated legacy equation (6).

On this compatibility locus the complete affine fibre is
\[
\begin{aligned}
w_4={}&\frac{5a+d}{4}v_2-\frac{a+5d}{2}v_7
       +\frac{-3a+9d}{4}v_{12}+2w_{11},\\
w_5={}&\frac{a+5d}{4}v_3+\frac{3a-9d}{2}v_8,\\
w_6={}&0,\\
w_{10}={}&\frac{-9a+3d}{8}v_1+\frac{5a+d}{4}v_6
       +\frac{-a-5d}{8}v_{11}+\frac12w_{17},\\
w_{12}={}&-\frac12(a-d)^2,\\
w_{16}={}&\frac{-9a+3d}{2}v_5+\frac{5a+d}{4}v_{10},\\
w_{18}={}&0.
\end{aligned}
\]
Substitution into all 36 monomial coefficients of \(E_7\) leaves exactly
\[
3(a-3d)v_4,\qquad -3(3a-d)v_9,
\]
so the parametrization is both sufficient and necessary.

### 2.2 Double root \(h=p^2\)

The raw left-null calculation returns 13 nonzero generators. Their
set-theoretic radical is
\[
\sqrt{I_{7,p^2}}=
\left\langle
e,f,b,\ (a-2d)v_4,
(a-4d)v_3-6cv_4-6(a-2d)v_8
\right\rangle.
\]
Thus \(e=f=b=0\), while \(c\) remains arbitrary as required.

The complete affine fibre is
\[
\begin{aligned}
w_4={}&\frac32av_1+cv_2-(a+2d)v_6-4cv_7
       +\left(-\frac a2+2d\right)v_{11}+3cv_{12}+2w_{11},\\
w_5={}&\left(\frac a2+d\right)v_2+2cv_3+(a-4d)v_7
       -6cv_8+\left(-\frac{3a}{2}+3d\right)v_{12},\\
w_6={}&(a-d)^2,\\
w_{10}={}&\frac32av_5+cv_6-\left(\frac a4+\frac d2\right)v_{10}
       -cv_{11}+\frac12w_{17},\\
w_{12}={}&c(a-d),\\
w_{16}={}&\frac32av_9+cv_{10},\\
w_{18}={}&c^2.
\end{aligned}
\]
The only residual \(E_7\) coefficients are exactly
\[
6(a-2d)v_4,\qquad
2\{(a-4d)v_3-6cv_4-6(a-2d)v_8\}.
\]

## 3. Universal degree-six compatibility

The checker forms \(E_6\) with a symbolic \(3\times3\) matrix \(L\), then
substitutes all seven solved \(H_2\) entries while leaving the 11 fibre
parameters, all 12 \(v_i\), and all 9 entries of \(L\) symbolic.
Direct polynomial equality gives
\[
[r^2]E_{6,pq}
=12p^2q^2(a-d)^2(a+d)
\]
and
\[
[r^2]E_{6,p^2}
=24dp^2\bigl(cp+(d-a)q\bigr)^2.
\]
Neither remainder contains a free \(H_2\), \(V\), or \(L\) coefficient.
These are therefore necessary compatibility conditions on the complete
degree-seven fibre, not evaluations on a particular solution.

The associated set-theoretic branch ideals are
\[
\sqrt{I_{6,pq}}=\langle a-d\rangle\cap\langle a+d\rangle
\]
and
\[
\sqrt{I_{6,p^2}}
=\langle d\rangle\cap\langle c,d-a\rangle.
\]
Scheme-theoretically, the three binary coefficients in the second case
generate \(d\langle c,d-a\rangle^2\), up to a nonzero constant.

## 4. Exhaustive tangent branches

The factors and residual \(E_7\) equations give the following complete list.

| case | parameter locus | tangent orbit | retained \(V\)-conditions |
|---|---|---|---|
| \(pq\) | \(a=d\ne0\) | \(2A\) | \(v_4=v_9=0\) |
| \(pq\) | \(a=-d\ne0\) | \(pA_p-qA_q\) | \(v_4=v_9=0\) |
| \(pq\) | \(a=d=0\) | \(0\) | none |
| \(p^2\) | \(c=0,\ d=a\ne0\) | \(2A\) | \(v_4=0,\ v_3=2v_8\) |
| \(p^2\) | \(d=0,\ a\ne0\), any \(c\) | \(pA_p\) | \(v_4=0,\ v_3=6v_8\) |
| \(p^2\) | \(d=a=0,\ c\ne0\) | \(pA_q\) | \(v_4=0\) |
| \(p^2\) | \(a=c=d=0\) | \(0\) | none |

On the double-root component \(d=0,a\ne0\), a lower-triangular change
preserving \(p^2\) removes \(c\); when \(a=0,c\ne0\) the field is the
nonzero nilpotent orbit. The scalar component is \(c=0,d=a\). Their only
intersection is the zero field. Hence there is no omitted rank-jump or zero
specialization and no counterexample to legacy (7), (8), or (9).

## 5. Reproduction and scope guard

Run:

```sh
taxonomy_freeze/fixed_conic_binary_repair_pari/verify_strict.sh
```

The wrapper rejects recovered GP parse/type/user errors even when GP exits
zero, requires exact rank, determinant, dimension, factor, and final pass
markers, and prints

```text
PASS strict fixed-conic binary PARI replay
```

No ledger, registry, branch, commit, or remote state was changed.

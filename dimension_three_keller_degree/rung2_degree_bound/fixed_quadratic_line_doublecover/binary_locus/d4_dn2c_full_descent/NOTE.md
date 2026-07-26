# Exclusion of the frozen family D4-DN-2C

> **Status and disclosure (2026-07-26 UTC).** This is an AI-assisted,
> exact-computation research note. It is **not peer reviewed**. Exact symbolic
> checks are evidence about the encoded algebra, not peer review. The theorem
> below concerns one frozen normalized quartic family only; it is not a
> quartic-wide degree bound.

Work over \(\mathbb C\).  After subtracting harmless constants, the
normalized family consists of all maps
\[
F=L(p,q,r)^t+H_2+H_3+H_4,
\]
where \(L\) is an arbitrary constant \(3\times3\) matrix,
\[
H_4=(P,Q,0),\qquad H_3=(U,V,R),\qquad H_2=(A,B,T),
\]
\(U,V\) are arbitrary ternary cubics, and \(A,B,T\) are arbitrary ternary
quadratics, subject only to the Keller identities.  Fix the binary top data
\[
h=(p+q)^2,\qquad P=hp^2,\qquad Q=hq^2,\qquad
R=h(p-2q).
\]
For a Keller map, \(\det L\) is its nonzero constant Jacobian.

## Theorem

No quartic Keller counterexample has this frozen `D4-DN-2C` binary top
data. Equivalently, every Keller map in this normalized family is a
polynomial automorphism.

The proof starts from the complete \(E_7/E_6\) contact atlas in the sibling
directory `d4_dn2c_full_rebuild`.  Its exact verifier derives the complete
\(E_7\) kernel, retains all 18 lower variables occurring in \(E_6\), and
proves that the geometric contact locus has exactly four charts:

1. two conjugate rank-seven plane interiors;
2. their rank-six punctured intersection line; and
3. the rank-five origin.

The present certificate retains every free coefficient after each displayed
pivot and closes all four charts.

## 1. Transverse plane interiors

Write \(\eta^2=-2\).  On the plus plane use parameters \(k,s\); its
intersection with the other plane is \(2k+3s=0\).  Thus the transverse
interior has \(2k+3s\ne0\).

After the specialization-safe \(E_6\) solve, whose pivot is
\[
93312(\eta-1)(2k+3s)^2,
\]
two lower-variable-free \(E_5\) coefficients are
\[
[p^3r^2]E_5=\frac{(2k+3s)Q_1(k,s)}{162},\qquad
[p^2qr^2]E_5=\frac{(2k+3s)Q_2(k,s)}{243},
\]
where
\[
\begin{aligned}
Q_1={}&(-16+40\eta)k^2+(-120-24\eta)ks+(18-45\eta)s^2,\\
Q_2={}&(116+88\eta)k^2+(-30-6\eta)ks+(180+36\eta)s^2.
\end{aligned}
\]
If \(k\ne0\), put \(t=s/k\).  The exact Bézout identity
\[
A(t)Q_1(1,t)+B(t)Q_2(1,t)=1
\]
holds with
\[
\begin{aligned}
A(t)&=\left(\frac16-\frac{5\eta}{36}\right)t
       +\frac{13}{108}+\frac{11\eta}{72},\\
B(t)&=\left(\frac5{72}+\frac{\eta}{24}\right)t
       +\frac5{108}-\frac{\eta}{18}.
\end{aligned}
\]
If \(k=0\), then
\[
Q_1(0,s)=(18-45\eta)s^2,
\]
whose coefficient has nonzero norm \(4374\); the transverse condition gives
\(s\ne0\).  Therefore \(Q_1,Q_2\) never vanish simultaneously on the
interior.  The minus plane is the \(\eta\mapsto-\eta\) conjugate and is
excluded identically.

## 2. Punctured plane intersection

The common line is
\[
(a,b,x,y)=\left(k,k,-\frac23k,-\frac23k\right),\qquad k\ne0.
\]
It is recomputed from the rank-six \(E_6\) chart; no vanished plane pivot is
specialized.

### 2.1 Complete \(E_5\) ideal

The four \(r^1\)-equations of \(E_5\) have rank two.  A safe pivot
\(-64k^3/9\) gives
\[
\begin{aligned}
b_{qr}&=\frac{k}{3}(v_1-v_2),\\
t_0&=\frac14(4t_1-4t_2+3u_1-6u_2+9u_3
                    -3v_1+6v_2-9v_3).
\end{aligned}
\]
The six binary equations next solve three more coefficients on pivot
\(-32k^3\).  The exact residual ideal over \(\mathbb C(k)\) is
\[
\langle \mathcal Q,\ \mathcal A\mathcal B\rangle,                 \tag{1}
\]
where
\[
\begin{aligned}
\mathcal A={}&8t_1-8t_2-6u_2+9u_3+12v_2-18v_3,\\
\mathcal B={}&-6\ell_8+2kt_1-4kt_2-3kv_1+6kv_2-9kv_3,
\end{aligned}
\]
and
\[
\begin{aligned}
\mathcal Q={}&u_1^2-4u_1u_2+6u_1u_3-6u_1v_0+4u_1v_1-2u_1v_2\\
&+4u_2^2-12u_2u_3+12u_2v_0-8u_2v_1+4u_2v_2\\
&+9u_3^2-18u_3v_0+12u_3v_1-6u_3v_2\\
&+18v_0^2-30v_0v_1+24v_0v_2-18v_0v_3\\
&+13v_1^2-22v_1v_2+18v_1v_3\\
&+10v_2^2-18v_2v_3+9v_3^2 .
\end{aligned}
\]
The verifier compares reduced Gröbner bases, so (1) is equality, not merely
one containment.

### 2.2 The common \(E_4\) conditions

Two \(r^2\)-coefficients equal
\[
-\frac23 k^3\mathcal S,\qquad
\mathcal S=v_0-v_1+v_2-v_3.
\]
Thus \(\mathcal S=0\).  On this hyperplane,
\[
\mathcal Q=\mathcal D^2,\qquad
\mathcal D=u_1-2u_2+3u_3-v_1+2v_2-3v_3,
\]
so \(\mathcal D=0\).  It remains to split the product in (1).

### 2.3 Branch \(\mathcal B=0\)

The \(E_4,r^1\) system solves on pivot \(-2k^2/3\).  Its binary part then
solves on pivot \(4k^2\), leaving exactly
\[
\mathcal A\mathcal F_B=0,
\]
where
\[
\begin{aligned}
\mathcal F_B={}&4\ell_6-4\ell_7-2t_1v_1+4t_1v_2-6t_1v_3\\
&+4t_2v_1-8t_2v_2+12t_2v_3\\
&+3v_1^2-12v_1v_2+18v_1v_3\\
&+12v_2^2-36v_2v_3+27v_3^2.
\end{aligned}
\]
The exact reduced determinant has \(\mathcal F_B\) as a factor.  Hence, if
\(\mathcal A\ne0\), then \(\det L=0\), contradicting the Keller condition.
The boundary \(\mathcal A=0\) is the next branch.

### 2.4 Branch \(\mathcal A=0\)

The \(E_4,r^1\) equations again use pivot \(-2k^2/3\), but their residual
ideal is the square of
\[
\mathcal C=
24\ell_8+8kt_2-6ku_2+9ku_3+12kv_1-12kv_2+18kv_3.
\]
Thus \(\mathcal C=0\).  The binary \(E_4\) equations then solve on pivot
\(4k^2\) with no residual.  The determinant factors as
\[
\det L=\frac{\mathcal F_A\mathcal H_A}{1152},
\]
where the second factor is computed exactly in the verifier and
\[
\begin{aligned}
\mathcal F_A={}&16\ell_6-16\ell_7\\
&+8t_2v_1-16t_2v_2+24t_2v_3\\
&-6u_2v_1+12u_2v_2-18u_2v_3\\
&+9u_3v_1-18u_3v_2+27u_3v_3\\
&+12v_1^2-36v_1v_2+54v_1v_3\\
&+24v_2^2-72v_2v_3+54v_3^2 .
\end{aligned}
\]
If \(\mathcal F_A=0\), then \(\det L=0\).  On the complementary
localization, the first two \(E_3\) equations solve \(a_{q^2},b_{q^2}\) on
the pivot
\[
\frac{k^2\mathcal F_A^2}{144}.
\]
Each remaining \(E_3\) equation is exactly
\[
\frac{k\mathcal F_A^2}{288},
\]
which is nonzero on this localization.  This closes branch
\(\mathcal A=0\), including the overlap \(\mathcal A=\mathcal B=0\).
Every pivot boundary has therefore been handled.

## 3. Origin and the plane exit

At \(a=b=x=y=0\), the fresh \(E_6\) pivot is the nonzero constant \(31104\).
It gives
\[
\begin{aligned}
a_{pr}&=\frac{3b_{qr}+4\ell_8}{3},&
a_{qr}&=\frac{2(3b_{qr}+2\ell_8)}{3},&
a_{r^2}&=b_{pr}=b_{r^2}=0.
\end{aligned}
\]
Two \(E_4,r^1\) coefficients are
\[
[p^3r]E_4=-3b_{qr}^2,\qquad
[q^3r]E_4=\frac23(3b_{qr}+2\ell_8)^2.
\]
Thus \(b_{qr}=\ell_8=0\), and literally all six \(r\)-dependent quadratic
coefficients
\[
a_{pr},a_{qr},a_{r^2},b_{pr},b_{qr},b_{r^2}
\]
vanish.

All nonlinear terms now depend only on \(p,q\).  Since the full Jacobian is
a nonzero constant, the constant \(r\)-column is nonzero.  An invertible
linear target change sends it to the third coordinate vector.  The first two
coordinates then define a plane Keller map of degree at most four, while the
third coordinate is triangular in \(r\).  Moh's unconditional theorem for
plane Keller maps of degree strictly less than \(100\) makes the plane map a
polynomial automorphism; the triangular extension is therefore an
automorphism.

Reference: R. Biggers, T. T. Moh, and M. Fried, “On the Jacobian conjecture
and the configurations of roots,” *J. Reine Angew. Math.* **340** (1983),
140–213.

## Verification

Run:

```sh
./verify_strict.sh
```

The strict wrapper:

- runs the frozen \(E_7/E_6\) rebuild and the complete descent;
- invokes an independent direct PARI/GP reconstruction from the raw top
  forms through the complete all-18-variable contact atlas and every lower
  chart, including its adjugate check of the origin plane normalization;
- rejects optimized Python, where assertions are disabled;
- requires all chart markers;
- corrupts an interior \(E_5\) coefficient and requires failure; and
- corrupts the origin square and independently requires failure.

The terminal marker is:

```text
D4_DN2C_FULL_DESCENT_STRICT_PASS
```

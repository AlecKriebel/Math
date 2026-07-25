# Certified adjacent merging on the minimal metric face

This note proves the quartic-energy inequality on one exact face of the
five-point `C5` angle metric polytope.  It does **not** yet prove the inequality
off that face.

## 1. The minimal face is a simplex

Put \(L=\pi/3\) and

\[
F(x)=h(\cos Lx),\qquad
P(x)=F(x)+F(1-x)-\frac34,
\quad h(t)=t^2(t^2-\tfrac14).
\]

Write the five cycle angular distances as \(\pi-LA_i\) and the five chord
distances as \(L(1+C_i)\).  Thus \(0\le A_i,C_i\le1\).  The relevant spherical
triangle and perimeter inequalities include

\[
C_i\le A_i+A_{i+1}-1,\qquad
1-A_i\le C_{i+1}+C_{i+3}.
\]

On summing these two families,

\[
\sum_i C_i\le2\sum_i A_i-5,\qquad
2\sum_iC_i\ge5-\sum_iA_i.
\]

Consequently \(\sum_iA_i\ge3\).  On the minimal face
\(\sum_iA_i=3\), every displayed inequality is an equality after summing, so

\[
\sum_iC_i=1,\qquad C_i=A_i+A_{i+1}-1.
\]

Put \(x_i=1-A_i\).  Then

\[
x_i\ge0,\qquad x_i+x_{i+1}\le1,\qquad \sum_i x_i=2.
\]

This four-dimensional polytope is a simplex.  Its barycentric coordinates
\(\lambda_i\ge0\), \(\sum_i\lambda_i=1\), are characterized by

\[
x_i=\lambda_i+\lambda_{i-2}.
\]

Equivalently,

\[
A_i=1-\lambda_i-\lambda_{i-2},\qquad C_i=\lambda_{i+2}.
\]

For example, starting from \(x\), one may take
\(\lambda_i=C_{i-2}=1-x_{i-2}-x_{i-1}\); the identity for \(x_i\) follows from
\(\sum_i x_i=2\).  Conversely, the formulas from any point of the standard
simplex satisfy all the face constraints.

The exact trigonometric identity

\[
F(c)+F(1-c)+h(\cos L(1+c))=\frac34
\]

therefore gives the total ten-pair energy on the face as

\[
\mathcal E(\lambda)
=\sum_iF(1-\lambda_i-\lambda_{i-2})-\sum_iP(\lambda_i).
\tag{1}
\]

## 2. The adjacent-mass lemma

Take two adjacent barycentric coordinates and write

\[
(\lambda_0,\lambda_1,\lambda_2,\lambda_3,\lambda_4)
=(x,y,a,b,c),\quad s=x+y,\quad r=a+c.
\]

Only the following part of (1) changes when mass is moved between \(x\) and
\(y\):

\[
\Phi(X)=
F(X+r)+F(s-X+r)+F(1-X-a)+F(1-s+X-c)
-P(X)-P(s-X).
\]

The secant gap is

\[
D=(1-t)\Phi(0)+t\Phi(s)-\Phi(st),\qquad t=x/s.
\tag{2}
\]

At \(s=0\) use the continuous extension.

**Certified adjacent-mass lemma.**  For
\(x,y,a,b,c\ge0\) with \(x+y+a+b+c=1\),

\[
D\ge 2xy(a+c).
\tag{3}
\]

In particular,

\[
\mathcal E(x,y,a,b,c)
\le \frac{y}{s}\mathcal E(0,s,a,b,c)
   +\frac{x}{s}\mathcal E(s,0,a,b,c).
\tag{4}
\]

The proof of (3) is computer-assisted but uses only exact integer arithmetic.
The rest of this section records the complete certificate and its analytic
error bound.

## 3. Rational polynomial certificate

Let

\[
k=\frac{2\pi}{3},\qquad k_0=\frac{1309}{625}=2.0944.
\]

Define the rational degree-18 polynomial

\[
f(z)=\frac34+
\sum_{j=1}^{9}
\frac{(-1)^j(3+2^{2j})k_0^{2j}}{8(2j)!}\,z^{2j}.
\tag{5}
\]

It is the degree-18 Maclaurin truncation of

\[
F(z)=\frac14+\frac38\cos(kz)+\frac18\cos(2kz),
\]

with \(k\) replaced by \(k_0\).  Put
\(p(z)=f(z)+f(1-z)-3/4\), and form \(\Phi_f,D_f\) from (2) by replacing
\(F,P\) by \(f,p\).

Set \(x=st\), \(y=s(1-t)\), \(a=ru\), and \(c=r(1-u)\).  Exact polynomial
division verifies that

\[
Q_f(s,t,r,u)=\frac{D_f}{s^2t(1-t)r}
\]

is a polynomial.  The remaining simplex inequality is parametrized by
\(r=(1-s)v\), where \(0\le s,t,u,v\le1\).  The polynomial

\[
B(s,t,v,u)=Q_f(s,t,(1-s)v,u)-2
\]

has tensor multidegree \((15,15,15,16)\).

The verifier converts \(B\) exactly from the power basis to the tensor
Bernstein basis on \([0,1]^4\).  All \(69\,632\) Bernstein coefficients are
strictly greater than \(7/50\).  Since the Bernstein basis is nonnegative and
partitions unity,

\[
Q_f\ge 2+\frac7{50}.
\tag{6}
\]

The complete integer tensor, enumerated lexicographically, has SHA-256 digest

```text
5153dc70e2db1f215f2c8e60c39f55e1a5a41960f849bfb315edd2fb6a47b21b
```

The smallest coefficient margin occurs at Bernstein index \((15,0,0,0)\).
The checker regenerates the tensor from (5); the digest is only a pin against
accidental certificate drift.

## 4. Rigorous analytic remainder

Machin's identity

\[
\frac\pi4=4\arctan\frac15-\arctan\frac1{239}
\]

and alternating arctangent series give, using rational arithmetic,

\[
3.14159<\pi<3.14160.
\]

For completeness, the tangent identity is exact:

\[
\tan(2\arctan\tfrac15)=\frac5{12},\qquad
\tan(4\arctan\tfrac15)=\frac{120}{119},
\]

and subtracting \(\arctan(1/239)\) gives tangent \(1\) in the interval
\((0,\pi/2)\).  The verifier checks rational alternating-series enclosures.
It follows that

\[
0<k_0-k<\frac1{150000},\qquad k,k_0<\frac{21}{10}.
\]

Differentiating three times,

\[
F'''(z)=k^3\left(\frac38\sin(kz)+\sin(2kz)\right).
\]

The next omitted term in the sine series obtained from (5) has degree \(17\).
The exact bound used by the verifier is

\[
\begin{split}
\|F'''-f'''\|_\infty
\le{}&
\frac1{150000}
\left[
\frac38(3K^2+K^3)+(3K^2+2K^3)
\right]\\
&+
\frac{k_0^3}{17!}
\left[\frac38k_0^{17}+(2k_0)^{17}\right]
<\frac1{800},
\qquad K=\frac{21}{10}.
\end{split}
\tag{7}
\]

It remains to explain why a \(C^3\) bound controls the normalized secant gap
uniformly even on its equality boundaries.  Let \(e=F-f\), let \(D_e\) be the
linear error in (2), and put \(a=ru,c=r(1-u)\).  At \(r=0\) the corresponding
\(\Phi_e\) vanishes identically.  Two differentiations in \(X\), followed by
the fundamental theorem of calculus in \(r\), express
\(\Phi_e''/r\) as an average of four values of \(e'''\), with absolute
coefficients

\[
1,\quad1,\quad u,\quad1-u.
\]

Their sum is \(3\).  The Green-kernel formula for the secant gap is

\[
D_e=(1-t)\int_0^{st}w\,\Phi_e''(w)\,dw
   +t\int_{st}^{s}(s-w)\,\Phi_e''(w)\,dw.
\]

After division by \(s^2t(1-t)r\), the total kernel mass is \(1/2\).
Consequently

\[
\left|\frac{D_e}{s^2t(1-t)r}\right|
\le\frac32\|e'''\|_\infty
<\frac3{1600}.
\tag{8}
\]

Combining (6) and (8),

\[
\frac{D}{xy(a+c)}
>2+\frac7{50}-\frac3{1600}>2.
\]

This proves (3) in the interior.  All boundary cases follow by continuity;
both sides vanish when \(x=0\), \(y=0\), or \(a+c=0\).

## 5. Energy bound on the whole face

If two adjacent positive \(\lambda\)-coordinates exist, (4) shows that merging
their total mass to one endpoint does not decrease the larger endpoint
energy.  Each merge reduces the support size.  Repeating ends at an
independent subset of the five-cycle, hence at support size at most two.

For a nonadjacent two-point support of masses \(q,1-q\), direct substitution
in (1) gives

\[
\mathcal E=\frac32-P(q).
\]

If

\[
Y=\cos\!\left(\frac{2\pi}{3}(q-\tfrac12)\right),
\]

then \(1/2\le Y\le1\) and

\[
P(q)=\frac{(1-Y)(2Y-1)}8\ge0.
\]

Thus

\[
\boxed{\mathcal E\le\frac32}
\]

on the entire face \(\sum_iA_i=3\).

There is genuine equality continuum: every simplex edge supported on two
adjacent \(\lambda\)-coordinates has energy \(3/2\).  There are additional
boundary equality segments (for example \(a=c=0\), \(x+y=1/2\),
\(b=1/2\)); no uniqueness assertion is used.

## 6. Reproduction

Run

```bash
python3 verify_adjacent_merge.py
python3 test_verify_adjacent_merge.py
```

No third-party package or floating-point arithmetic is used by the verifier.
The separate `search_merge_bernstein.py` file is discovery code and is not
trusted by the proof.

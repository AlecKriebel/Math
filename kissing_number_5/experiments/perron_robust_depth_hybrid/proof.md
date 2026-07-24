# Exact Perron/depth identities and endpoint barriers

## 1. Scope

Let \(x_1,\ldots,x_{41}\in S^4\), let \(X\) have the \(x_i\) as
columns, and put
\[
G=X^{\mathsf T}X,\qquad A=2G-J,\qquad W=I-A.
\]
For a hypothetical 41-point kissing code the already certified cap and
contact results imply
\[
\operatorname{inertia}A=(5,1,35),\qquad W\geq0,
\]
and \(W\) is irreducible.  Write its Perron root as
\(\rho=t+1\), normalize the Perron vector \(p>0\) by
\({\bf1}^{\mathsf T}p=1\), and set
\[
v=Xp,\qquad r=\|v\|,\qquad \Delta=41-t=42-\rho.
\]
The known spectral argument gives \(17<t\leq41\).

This note derives exact consequences of the new robust cap theorem and
then proves that their scalar and frame shadows do **not** separate
\(\rho\) from 42.  It does not construct a 41-point kissing code.

## 2. Exact Perron-axis identities

The equation \(Wp=(t+1)p\) is equivalent to
\[
tp_i=1-2\langle x_i,v\rangle.                         \tag{1}
\]
Taking its scalar product with \(p\) gives
\[
1=t\|p\|^2+2r^2.                                      \tag{2}
\]

Suppose first that \(r>0\), put \(u=v/r\), and write
\[
a_i=\langle x_i,u\rangle,\qquad
E=\sum_i a_i^2=u^{\mathsf T}(XX^{\mathsf T})u.
\]
Summing (1), and then multiplying (1) by \(a_i\) and summing, gives
\[
\boxed{\quad
\sum_i a_i=\frac{\Delta}{2r},\qquad
E=\frac{\Delta}{4r^2}-\frac t2.
\quad}                                                 \tag{3}
\]
Equivalently, if \(\bar a=41^{-1}\sum_i a_i\) and
\[
V_a=\sum_i(a_i-\bar a)^2,
\]
then direct substitution into (3) yields the useful exact identity
\[
\boxed{\quad
\Delta-82r^2=\frac{164r^2}{t}V_a.
\quad}                                                 \tag{4}
\]
It is the same identity as
\[
\sum_i\left(p_i-\frac1{41}\right)^2
   =\frac{4r^2}{t^2}V_a
   =\frac{\Delta-82r^2}{41t}.                          \tag{5}
\]

Let
\[
\delta=\frac1{300}.
\]
The exact enlarged-cap theorem, applied to \(u\) and \(-u\), supplies
at least seven indices with \(a_i<-\delta\) and at least seven with
\(a_i>\delta\).  Equation (1) therefore gives the strict order statistics
\[
\begin{aligned}
\#\left\{i:p_i>\frac{1+2\delta r}{t}\right\}&\geq7,\\
\#\left\{i:p_i<\frac{1-2\delta r}{t}\right\}&\geq7.
\end{aligned}                                          \tag{6}
\]

Here is the strongest variance conclusion obtainable from just these
two cardinality statements.

**Two-tail variance lemma.**  If 41 real numbers include seven values
strictly below \(-\delta\) and seven strictly above \(\delta\), then
\[
V_a>14\delta^2=\frac7{45000}.                          \tag{7}
\]

**Proof.**  Choose disjoint seven-element sets \(L,H\) of such values,
and let their means be \(\ell<-\delta\) and \(h>\delta\).  Replacing the
values within \(L\), within \(H\), and within the 27 remaining positions
by their respective group means can only decrease the variance.  For
fixed \(\ell,h\), minimizing over the third group mean puts it at
\((\ell+h)/2\).  The resulting variance is
\[
\frac72(h-\ell)^2>\frac72(2\delta)^2=14\delta^2.
\]
This argument is just the orthogonal projection onto the three group-
constant subspace, so it includes arbitrary values and all degeneracies
outside the two strict tails. \(\square\)

Combining (4) and (7) gives
\[
\boxed{\quad
\Delta>82r^2+\frac{287}{11250t}r^2.
\quad}                                                 \tag{8}
\]
The exact frame floor
\[
XX^{\mathsf T}\succ\ell_0 I,\qquad
\ell_0=\frac{15059}{40000},
\]
gives the stronger small-\(r\) estimate
\[
\Delta=2r^2(t+2E)>2r^2(t+2\ell_0),                    \tag{9}
\]
or, after using \(t=41-\Delta\),
\[
\boxed{\quad
\Delta>
\frac{835059\,r^2}{10000(1+2r^2)}.
\quad}                                                 \tag{10}
\]
Neither (8) nor (10) gives a positive lower bound for \(\Delta\), because
the identities provide no positive lower bound for \(r\).

If \(r=0\), (1)--(2) instead force
\[
p=\frac1{41}{\bf1},\qquad t=41,\qquad \rho=42,
\qquad X{\bf1}=0.                                     \tag{11}
\]
Thus the endpoint is precisely the centered case; it cannot be removed
by dividing by \(r\).

## 3. An exact family defeating a Perron/frame gap

The failure as \(r\to0\) is real, rather than an artifact of a loose
estimate.  For any rational
\[
0<r\leq\frac1{100},
\]
define
\[
\begin{aligned}
\Delta&=\frac{574}{5}r^2,&
t&=41-\Delta,&
\rho&=42-\Delta,\\
m&=\frac75r,&
c^2&=\frac{41}{70}-\frac{41}{25}r^2.
\end{aligned}                                         \tag{12}
\]
Take a list of 41 axial coordinates consisting of
\[
\underbrace{m-c,\ldots,m-c}_{7},\quad
\underbrace{m,\ldots,m}_{27},\quad
\underbrace{m+c,\ldots,m+c}_{7}.                       \tag{13}
\]
For this range of \(r\), \(c>3/4\), \(0<m\leq7/500\), and \(c<4/5\).
Consequently all values in (13) lie in \((-1,1)\), seven are strictly
below \(-1/300\), and seven are strictly above \(1/300\).

Their first two moments are
\[
\sum_i a_i=41m=\frac{\Delta}{2r},\qquad
\sum_i a_i^2
=41m^2+14c^2
=\frac{41}{5}+\frac{\Delta}{2}
=\frac{\Delta}{4r^2}-\frac t2.                        \tag{14}
\]
Define
\[
p_i=\frac{1-2ra_i}{t}.
\]
Then the middle 27 weights equal \(1/41\), while the two tails are
\[
\frac1{41}+\frac{2rc}{t}
\quad\hbox{and}\quad
\frac1{41}-\frac{2rc}{t}.                             \tag{15}
\]
They are positive, sum to one, and satisfy (1)--(6) exactly.

These data also have a common unit-vector realization, although it is
not claimed to be a kissing code.  For \(n=7,27\), use the zero-sum
unit-norm tight frame in \(\mathbb R^4\)
\[
y_{n,j}=\frac1{\sqrt2}
\left(
\cos\frac{2\pi j}{n},\sin\frac{2\pi j}{n},
\cos\frac{4\pi j}{n},\sin\frac{4\pi j}{n}
\right).
\]
For each of the three layers in (13), take
\[
x_i=(a_i,\sqrt{1-a_i^2}\,y_{n,j}),
\]
using one 7-frame for each outer layer and the 27-frame for the middle
layer.  Roots-of-unity summation shows that every layer has zero
transverse centroid and transverse frame operator \(nI_4/4\).
Therefore the 41 vectors have
\[
s:=\sum_i x_i=(41m,0,0,0,0)
\]
and frame spectrum
\[
\boxed{\quad
\lambda_1=\frac{41}{5}+\frac{\Delta}{2},\qquad
\lambda_2=\cdots=\lambda_5=\frac{41}{5}-\frac{\Delta}{8}.
\quad}                                                 \tag{16}
\]
The weighted transverse centroids also vanish, so \(Xp=re_1\).
Equations (14)--(15) then imply
\[
(2G-J)p=-tp.
\]
The positive frame spectrum proves \(\operatorname{rank}X=5\).
Furthermore, \({\bf1}\notin\operatorname{range}X^{\mathsf T}\): if
\(\langle w,x_i\rangle=1\) on one layer, averaging over its zero-sum
transverse frame fixes the axial part, while subtracting within that
layer kills the transverse part; the three distinct layer heights would
then require the same scalar multiple of \(m-c,m,m+c\) to equal one.
Thus \(A=2G-J\) has inertia \((5,1,35)\), and \(\rho\) is the unique
eigenvalue of \(W=I-A\) above one.

This realization deliberately fails the kissing sign.  Two adjacent
points in the middle 27-layer have transverse inner product
\[
\frac12\left(\cos\frac{2\pi}{27}+\cos\frac{4\pi}{27}\right)>\frac12,
\]
since both angles lie strictly between \(0\) and \(\pi/3\).  Adding the
common axial contribution preserves the strict inequality.

The five frame eigenvalues are all well above the certified floor.
Moreover, writing the centered spectral second and third moments as
\(\mathcal V,\mathcal T\), (16) gives
\[
\mathcal V=\frac5{16}\Delta^2,\qquad
\mathcal T=\frac{15}{128}\Delta^3,\qquad
20\mathcal T^2=9\mathcal V^3.                         \tag{17}
\]
Thus the sharp rank-five cubic moment inequality is satisfied with
equality.  The frame potential is
\[
\operatorname{tr}\left((XX^{\mathsf T})^2\right)
=\frac{1681}{5}+\frac5{16}\Delta^2
\longrightarrow\frac{1681}{5}.                       \tag{18}
\]
At the same time \(\rho=42-\Delta\to42\).

This proves that the Perron-axis order statistics, (1)--(10), the exact
frame floor, trace 41, the complete nonnegative five-eigenvalue spectrum,
and the sharp cubic spectral inequality cannot force either a uniform
gap below 42 or a uniform gap above the Welch frame potential.

The exact sample \(r=1/100\) is stored in `certificate.json` and checked
without floating point by `verify.py`.

## 4. A global robust-depth lemma for \(D_5\)

The following elementary fact lets us test the all-directions endpoint,
not merely the distinguished Perron axis.

Choose one unit representative from each of the 20 antipodal root lines
of normalized \(D_5\):
\[
R=\left\{\frac{e_i+e_j}{\sqrt2},
          \frac{e_i-e_j}{\sqrt2}:1\leq i<j\leq5\right\}.
\]
Then
\[
\sum_{z\in R}zz^{\mathsf T}=4I_5,                    \tag{19}
\]
and distinct lines have squared inner product at most \(1/4\).

**Lemma.**  For every unit \(e\), at least eight lines \(z\in R\) satisfy
\[
|\langle e,z\rangle|>\frac1{300}.                    \tag{20}
\]

**Proof.**  Otherwise choose seven lines containing every line that
violates the non-strict reverse inequality, filling arbitrarily if
necessary, and let
\[
Q=\sum_{j=1}^7z_jz_j^{\mathsf T}.
\]
Then
\[
\operatorname{tr}Q=7,\qquad
\operatorname{tr}Q^2
=7+2\sum_{i<j}\langle z_i,z_j\rangle^2
\leq\frac{35}{2}.                                    \tag{21}
\]
If the largest eigenvalue \(\lambda\) of \(Q\) were at least \(39/10\),
Cauchy--Schwarz on the other four nonnegative eigenvalues would give
\[
\operatorname{tr}Q^2
\geq\lambda^2+\frac{(7-\lambda)^2}{4}
\geq\frac{1409}{80}>\frac{35}{2};                    \tag{22}
\]
the middle function is increasing for \(\lambda\geq39/10\).  Hence
\(Q\prec(39/10)I\).  By (19), the other 13 line projectors have sum
\[
4I-Q\succ\frac1{10}I.
\]
Their squared projections on \(e\) therefore sum to more than \(1/10\),
whereas the supposition makes the sum at most
\[
\frac{13}{300^2}<\frac1{10},
\]
a contradiction. \(\square\)

For each line in (20), exactly one of its two normalized \(D_5\) roots
has projection \(>1/300\), and its antipode has projection \(<-1/300\).
Thus the 40 roots have at least eight points in each strict tail in
every direction.  Removing one antipodal root line still leaves at least
seven in each tail.  Notice that all boundary inequalities have the
correct direction: projections equal to \(1/300\) are counted among the
13 small lines in the contradiction.

## 5. A noncentered common-Gram near-model

Start with all 40 normalized \(D_5\) roots and append a second copy of one
root \(y\).  This is an indexed 41-vector list, not a kissing code.  It has
\[
\sum_i x_i=y,\qquad
S:=XX^{\mathsf T}=8I+yy^{\mathsf T},
\]
so its frame spectrum is
\[
(9,8,8,8,8).                                         \tag{23}
\]
By Section 4 it has at least eight projections in each robust tail for
every direction.

Let \(\Delta\) be the smaller root of
\[
\Delta^2-59\Delta+2=0,
\]
and put
\[
\Delta=\frac{59-\sqrt{3473}}2,\quad
t=41-\Delta=\frac{23+\sqrt{3473}}2,\quad
\rho=t+1=\frac{25+\sqrt{3473}}2.                     \tag{24}
\]
Thus \(0<\Delta<1\) and \(41<\rho<42\).  Define
\[
p_i=\frac{1-\Delta\langle x_i,y\rangle}{t}.
\]
The \(D_5\) centroid is zero, so these positive weights sum to one.
Moreover,
\[
Xp=\frac{y-\Delta Sy}{t}
   =\frac{1-9\Delta}{t}y
   =\frac{\Delta}{2}y,
\]
where the last equality is exactly the quadratic equation in (24).
It follows that
\[
(2G-J)p=-tp,
\]
and all Perron identities of Section 2 hold with \(r=\Delta/2\).

The list spans \(\mathbb R^5\), and \({\bf1}\) is not in
\(\operatorname{range}G\) because the list contains antipodal pairs.
Consequently \(A\) has inertia \((5,1,35)\).  Hence \(\rho\) is its
unique eigenvalue of \(W=I-A\) above one and \(p\) is a positive top
eigenvector.

Exactly one hypothesis fails: the appended copy and the original root
have inner product \(1\).  Every other unordered pair has inner product
at most \(1/2\).  Equivalently, \(W\) has exactly one unordered negative
off-diagonal entry.  This model therefore retains global robust depth,
the common PSD rank-five Gram matrix, Lorentzian inertia, positive leading
eigenvector, and excellent frame conditioning, but it is not a
counterexample to the kissing problem.

## 6. The centered endpoint is compatible with robust depth

The endpoint \(\rho=42\) also has an exact common-Gram near-model.  Choose
orthogonal normalized roots
\[
r=\frac{e_1+e_2}{\sqrt2},\qquad
z=\frac{e_1-e_2}{\sqrt2}.
\]
Remove the antipodal pair \(\{r,-r\}\) from \(D_5\), and insert the
zero-sum equilateral triangle
\[
r,\qquad -\frac12r+\frac{\sqrt3}{2}z,\qquad
-\frac12r-\frac{\sqrt3}{2}z.                          \tag{25}
\]
There are 41 unit vectors and their centroid is zero.  The retained 38
\(D_5\) roots already give at least seven points in each strict robust
tail in every direction, by Section 4.

The frame operator is
\[
8I-\frac12rr^{\mathsf T}+\frac32zz^{\mathsf T},
\]
with spectrum
\[
\left(\frac{19}{2},8,8,8,\frac{15}{2}\right).         \tag{26}
\]
Thus it has rank five and easily satisfies the exact frame floor.
For \(p={\bf1}/41\),
\[
Xp=0,\qquad A{\bf1}=-41{\bf1},\qquad
W{\bf1}=42{\bf1}.                                    \tag{27}
\]
As before, the centered rank-five Gram matrix makes the inertia of \(A\)
equal to \((5,1,35)\).

Again the precise failure is a kissing sign, not a boundary issue:
the second triangle point has inner product \(\sqrt3/2>1/2\) with the
retained root \(z\).  Hence robust depth and all frame/Perron identities
are fully compatible with the centered endpoint once the off-diagonal
sign is relaxed.

## 7. What remains coupled

The three exact barriers isolate the missing mechanism.

* The scalar/frame family shows that applying robust depth only through
  Perron-axis order statistics and frame moments cannot bound
  \(\rho\) away from 42.
* The two \(D_5\) modifications show that even all-direction robust depth
  is compatible with the noncentered and centered common-Gram Perron
  structures.
* Each common-Gram near-model fails an explicitly identified
  off-diagonal kissing inequality.  Conversely, keeping the full common
  rank-five PSD Gram matrix **and** every off-diagonal kissing sign is
  exactly the original 41-code problem.

Therefore a successful continuation must use a genuinely coupled
sign/rank invariant (for example a common four-cycle or star-complement
constraint), rather than a further scalar estimate in
\((\rho,r,\|p\|,S)\).

## 8. Dependency map and verification

```text
robust cap at +/-1/300
          |
          v
two strict Perron tails --> variance lemma --> (8)
          |
frame floor + Perron moment identities ------> (10)
          |
          +--> exact family (12)--(18): rho -> 42, FP -> Welch

D5 line-frame identity + trace(Q^2) bound
          |
          v
global eight-per-tail lemma
        /   \
       v     v
D5+duplicate   centered triangle replacement
rho<42 model   rho=42 model
       \       /
        explicit failed kissing signs
```

Run:

```sh
python3 experiments/perron_robust_depth_hybrid/verify.py
python3 -m unittest \
  experiments.perron_robust_depth_hybrid.test_verify -v
```

The verifier uses only `json`, `fractions.Fraction`, exact quadratic-field
arithmetic, and exact Gaussian elimination.  No numerical eigenvalue or
solver status is used.

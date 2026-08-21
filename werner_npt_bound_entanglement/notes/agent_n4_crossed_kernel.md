# The crossed-kernel Hessian at four copies

## Checkpoint

**2026-07-28 19:34 PDT.**  A minimal negative rank-two projection
would force a local-effect Hessian to be positive definite on a
five-dimensional compression kernel.  This note records an exact
obstruction to a tempting shortcut and isolates a sharper conjecture.

The shortcut
\[
 \operatorname{inertia}_+{\cal N}_\ell\leq4
\tag{1}
\]
is false, even when the local support is three-dimensional and the
logical compression has full rank.  An exact six-term code has
\[
 \operatorname{inertia}{\cal N}_\ell=(6,3,0).
\tag{2}
\]
For this code the restriction to the compression kernel nevertheless
has inertia \((2,3,0)\).  Broad discovery searches have likewise always
found a nonpositive kernel direction.  Three simpler scalar substitutes
have now been refuted exactly: neither the unrestricted inertia, the
kernel trace, nor the kernel determinant has a universal sign strong
enough to finish the argument.  The viable missing statement is
therefore the crossed-kernel assertion
\[
 {\cal N}_\ell|_{\ker{\cal C}_\ell}\not\succ0,
\tag{3}
\]
not a bound on the inertia of the unrestricted Hessian.

## 1. Definitions and the descent implication

Let \(P=UU^\dagger\) be a rank-two projection on four qutrits and fix
one physical site.  On Hermitian \(3\times3\) matrices define
\[
 {\cal C}(A)=U^\dagger(A\otimes I)U
\tag{4}
\]
and
\[
 {\cal N}(A)=
 \operatorname{Tr}\!\left[
 (P\otimes P)(A\otimes A)
 \prod_{i=1}^4(F_i-\tfrac12I)
 \right].
\tag{5}
\]
If \(P\) were a negative minimizer of least local-support complexity,
the singular-filter argument gives
\[
 {\cal N}(A)\geq-F(P)\|A\|_{\rm op}^2>0
 \qquad(0\ne A\in\ker{\cal C}).
\tag{6}
\]
Since \(\dim_{\mathbb R}\ker{\cal C}\geq9-4=5\), (3) would rule out
every negative minimizer and prove the four-copy projection theorem.
The superficially stronger trace inequality
\[
 \operatorname{Tr}\bigl({\cal N}|_{\ker{\cal C}}\bigr)\leq0
\tag{7}
\]
would also suffice, but Section 3 gives an exact counterexample.

When \({\cal C}\) is onto, the orthogonal kernel projector is
\[
 \Pi_{\ker{\cal C}}
 =I-{\cal C}^\ast({\cal C}{\cal C}^\ast)^{-1}{\cal C}.
\tag{8}
\]
Thus the trace and all other spectral data of the crossed kernel are
finite rational functions of the code entries.  This makes exact
counterexample searches and algebraic factorization practical, but
the trace itself does not have the proposed sign.

## 2. Exact counterexample to the unrestricted inertia bound

At the first physical site take
\[
\begin{aligned}
 u&=\frac{-|1221\rangle+|2022\rangle+|1202\rangle}{\sqrt3},\\
 v&=\frac{|1122\rangle-|1022\rangle+|0202\rangle}{\sqrt3}.
\end{aligned}
\tag{9}
\]
Their computational supports are disjoint, so they are orthonormal.
All three first-site labels occur, and the compression in (4) is onto.

Use Hermitian coordinates in the order
\[
 (d_0,d_1,d_2,\Re01,\Im01,\Re02,\Im02,\Re12,\Im12),
\tag{10}
\]
where the off-diagonal basis matrices are not normalized.  Direct
expansion of (5) gives
\[
{\cal N}=
\begin{pmatrix}
1/144&1/12&-1/144&0&0&0&0&0&0\\
1/12&1/6&7/72&0&0&0&0&0&0\\
-1/144&7/72&1/144&0&0&0&0&0&0\\
0&0&0&0&0&0&0&-1/18&0\\
0&0&0&0&0&0&0&0&-1/18\\
0&0&0&0&0&1/36&0&0&0\\
0&0&0&0&0&0&1/36&0&0\\
0&0&0&-1/18&0&0&0&-1/18&0\\
0&0&0&0&-1/18&0&0&0&-1/18
\end{pmatrix}.
\tag{11}
\]
The upper \(3\times3\) block has inertia \((2,1,0)\).  Each of the
two displayed coupled \(2\times2\) blocks has inertia \((1,1,0)\),
and the two \(1/36\) entries are positive.  Hence
\[
 \boxed{\operatorname{inertia}{\cal N}=(6,3,0).}
\tag{12}
\]
Also
\[
 {\cal N}(I)=\frac{19}{36}>0.
\tag{13}
\]
Thus this example does not threaten the desired endpoint inequality;
it only disproves the proposed state-independent inertia bound.

The compression matrix is
\[
{\cal C}=
\begin{pmatrix}
0&2/3&1/3&0&0&0&0&0&0\\
1/3&2/3&0&0&0&0&0&0&0\\
0&0&0&1/3&0&0&0&-1/3&0\\
0&0&0&0&-1/3&0&0&0&1/3
\end{pmatrix}.
\tag{14}
\]
A rational kernel basis is
\[
\begin{aligned}
 &(1,-1/2,1,0,0,0,0,0,0),\\
 &(0,0,0,0,0,1,0,0,0),\quad
 (0,0,0,0,0,0,1,0,0),\\
 &(0,0,0,1,0,0,0,1,0),\quad
 (0,0,0,0,1,0,0,0,1).
\end{aligned}
\tag{15}
\]
In precisely this basis,
\[
 \boxed{
 {\cal N}|_{\ker{\cal C}}
 =\operatorname{diag}(-5/36,1/36,1/36,-1/6,-1/6).
 }
\tag{16}
\]
The crossed kernel therefore retains three negative directions even
though the unrestricted form has six positive directions.

The accompanying verifier reconstructs (11), (14), and (16) from
the codewords using exact arithmetic.

## 3. Exact failure of the kernel-trace shortcut

Take
\[
\begin{aligned}
u&=\frac{|1001\rangle+|1022\rangle+2|2202\rangle}{\sqrt6},\\
v&=\frac{2|0022\rangle+|0220\rangle}{\sqrt5}.
\end{aligned}
\tag{17}
\]
The first-site compression is onto.  In an exact rational kernel basis,
the generalized characteristic polynomial of the restriction, with the
Hilbert--Schmidt metric included, is
\[
-\frac5{209952}
(12z-1)^2(18z+1)(36z+1)^2.
\tag{18}
\]
Hence the five Hilbert--Schmidt eigenvalues are
\[
\left(-\frac1{18},-\frac1{36},-\frac1{36},
       \frac1{12},\frac1{12}\right).
\tag{19}
\]
In particular,
\[
\operatorname{Tr}({\cal N}|_{\ker{\cal C}})=\frac1{18}>0,
\qquad
{\cal N}(I)=F(P)=\frac{121}{450}>0.
\tag{20}
\]
Even the proposed signed repair
\[
\operatorname{Tr}({\cal N}|_{\ker{\cal C}})
\stackrel?{\leq}\frac18F(P)
\tag{21}
\]
fails, because the left side minus the right side is
\[
\frac1{18}-\frac1{8}\frac{121}{450}
=\frac{79}{3600}>0.
\tag{22}
\]
The restriction remains indefinite, exactly as required by (3).

## 4. Exact failure of a determinant-sign shortcut

One might next hope that the odd kernel dimension forces
\(\det({\cal N}|_{\ker{\cal C}})\leq0\).  This too is false.  Take
\[
\begin{aligned}
u&=\frac{-i|1212\rangle+|0010\rangle}{\sqrt2},\\
v&=\frac{i|2212\rangle+(-1+i)|0111\rangle
                   +(1-i)|1111\rangle}{\sqrt5}.
\end{aligned}
\tag{23}
\]
Again the first-site compression is onto.  The exact generalized
characteristic polynomial is
\[
-\frac3{102400000000}
(160z-3)(160z+7)(400z-1)^2(2400z+59).
\tag{24}
\]
The eigenvalues are therefore
\[
\left(-\frac7{160},-\frac{59}{2400},
       \frac1{400},\frac1{400},\frac3{160}\right),
\tag{25}
\]
and the determinant is positive.  Nevertheless the restriction has
two negative directions.  Also
\[
F(P)=\frac{163}{400}>0.
\tag{26}
\]

## 5. Current status

Discovery searches over dense and sparse complex codes found:

1. unrestricted positive inertia as large as six;
2. either sign for the kernel trace;
3. either sign for the kernel determinant;
4. no positive-definite restriction to \(\ker{\cal C}\).

Only the fourth item remains conjectural.  A proof must retain more
than a single symmetric spectral statistic.  Plausible exact forms are
a state-dependent negative test vector in the kernel, or a minimax
inequality which selects a low-dimensional principal subspace from
the joint data \(({\cal N},{\cal C})\).  The examples above are useful
stress tests: such a proof must handle kernel inertias \((2,3,0)\),
\((3,2,0)\), and, in generic dense cases, \((0,5,0)\), with the first
entry denoting positive directions.

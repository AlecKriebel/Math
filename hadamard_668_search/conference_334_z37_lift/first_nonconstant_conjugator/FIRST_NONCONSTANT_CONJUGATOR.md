# The first nonconstant \(z\)-adic conjugator layer

## Status

This checkpoint advances the semiregular \(C_{37}\) conference-matrix
route to \(H(668)\).  It does **not** construct a conference matrix or a
Hadamard matrix.

The main exact findings are:

1. the correct first nonconstant unitary-conjugator normal form has
   \(20+20=40\) essential parameters through degree two;
2. the pure first-higher rank-two family is impossible;
3. the much broader family supported on one common nondegenerate
   two-plane is impossible for every one of the 625 orbit quotients.

## Why \(z=\log(1+y)\) is the correct coordinate

Work in

\[
R=\mathbf F_{37}[y]/(y^{37}),\qquad x=1+y,\qquad z=\log x.
\]

The involution induced by cyclic reversal is \(z\mapsto-z\).  For a
matrix polynomial \(M\), write

\[
M^\dagger=M(-z)^T.
\]

A near-identity conjugator \(G\) preserves the required Hermitian
condition precisely when

\[
G^\dagger=G^{-1}.
\]

Since all integers \(1,\ldots,36\) are invertible, logarithm and
exponential are mutually inverse on the nilpotent ideal.  Thus \(G\) has
a unique logarithm

\[
G=e^K,\qquad K^\dagger=-K.
\]

Writing

\[
K=zA_0+z^2A_1+z^3A_2+\cdots
\]

diagonalizes the involution:

\[
A_r^T=(-1)^rA_r.
\]

In particular,

```text
A0 is symmetric;
A1 is skew-symmetric;
A2 is symmetric;
...
```

This corrects a potentially dangerous naive ansatz.  Merely replacing a
constant symmetric generator by `A0+y*A1` does not preserve unitarity.
Equivalently one may write

\[
K=z\mathcal A(z),\qquad
\mathcal A(-z)^T=\mathcal A(z).
\]

The first genuine extension is therefore

\[
K=zA_0+z^2A_1,\qquad A_0^T=A_0,\quad A_1^T=-A_1.
\]

## Exact low-layer parameterization

Let \(N_0=-T/2\pmod {37}\) be the square-zero constant matrix of the
certified quotient.  Before the trace correction begins at degree 18,

\[
N(z)=e^{-K}N_0e^K
     =N_0+zX+z^2Y+O(z^3)
\]

has

\[
X=[N_0,A_0],
\]

\[
Y=[N_0,A_1]+\frac12[[N_0,A_0],A_0].
\]

Consequently

\[
X^T=-X,\qquad Y^T=Y,
\]

and the square-zero equations are

\[
\{N_0,X\}=0,\qquad
\{N_0,Y\}+X^2=0.
\]

The exact ranks over \(\mathbf F_{37}\) are:

```text
Sym_9  --[N0,-]--> Skew_9     rank 20, kernel dimension 25;
Skew_9 --[N0,-]--> Sym_9      rank 20, kernel dimension 16.
```

The first skew tangent \(\{N_0,X\}=0\) has dimension 20 and is exactly
the first commutator image.  The homogeneous second symmetric tangent
\(\{N_0,Y\}=0\) has dimension 21.  Trace removes its one extra direction,
and its trace-zero part is exactly the 20-dimensional second commutator
image.  The diagonal projection of the second image has rank eight: all
nine second diagonal moments can move subject only to their zero sum.

Thus a fixed linear complement gives a 40-parameter normal form through
\(z^2\), twenty parameters in each parity.

There is also a clean gauge interpretation.  Left multiplication by

\[
H=\exp(zC+z^2D),\qquad C^T=C,\ D^T=-D,
\]

where the coefficients centralize \(N_0\) to the required order, changes
the logarithm by the BCH law

\[
A_0\longmapsto A_0+C,
\]

\[
A_1\longmapsto
A_1+D+\frac12[C,A_0].
\]

Choosing complements to the two centralizers gives the displayed
20-plus-20 slice.  This statement is a normal form through order two; it
does not assert a global classification of all degree-36 solutions.

## Binary diagonal target

The trace-corrected formal family is

\[
N=e^{-K}
\bigl(N_0+\eta z^{18}J+19y^{36}J\bigr)e^K,
\qquad \eta\in\{1,-1\}.
\]

Because \(K\) has zero constant term,

\[
y^{36}e^{-K}Je^K=y^{36}J
\]

in the truncated ring.  Remove this common terminal term and call the
remaining diagonal cyclic word \(r\).  A genuine binary diagonal block
must satisfy

\[
r(0)=0,\qquad r(t)\in\{18,19\}\quad(1\le t\le36).
\]

The number of nonzero positions with value 19 is exactly that diagonal
block's degree.  Every function-code intersection below uses this target.

## Pure first-higher rank two is impossible

Set \(A_0=0\) and suppose \(A_1=B\) is skew-symmetric of rank two:

\[
K=z^2B.
\]

Every rank-two skew matrix can be written

\[
B=uv^T-vu^T.
\]

With

\[
\Delta=(u^Tu)(v^Tv)-(u^Tv)^2,
\]

one has

\[
B^3=-\Delta B.
\]

Hence there are only four projective rational types:

1. split semisimple;
2. irreducible trace-zero semisimple;
3. \(J_3(0)\);
4. \(J_2(0)\oplus J_2(0)\).

For each type the verifier forms the similarity-invariant diagonal
function overcode

\[
W(B)=
\operatorname{span}\{
(e^{-z^2B})_{ar}(e^{z^2B})_{sb},
z^{18}(e^{-z^2B})_{ar}(e^{z^2B})_{sb}
\}.
\]

This deliberately forgets the specific matrices \(N_0\) and \(J\).
Nevertheless, in every rational type,

\[
W(B)\cap
\bigl(\{0\}\times\{18,19\}^{36}\bigr)
\]

consists of exactly the two Paley residue/nonresidue words, both of
weight 18.

The complete quotient census contains no quotient whose nine diagonal
degrees are all 18.  Therefore no pure rank-two first-higher generator
can work for any of the 625 quotients.

## The common nondegenerate two-plane pencil

A broader first family lets both coefficients act on the same
nondegenerate two-plane \(U\).  Let \(P=P^T=P^2\) be its orthogonal
projector and impose

\[
A_0=tP+S,\qquad A_1=B,
\]

\[
PS=SP=S,\qquad PB=BP=B,
\]

with \(A_0,A_1\) zero on \(U^\perp\), \(S^T=S\), and \(B^T=-B\).
Write

\[
A_0|_U=tI+S,\qquad \operatorname{tr}(S)=0,
\]

and let \(B=A_1|_U\ne0\).  Adjoint parity in dimension two gives

\[
S^2=\alpha I,\qquad
B^2=\beta I,\qquad
SB+BS=0,
\]

with \(\beta\ne0\).  Removing only the scalar gap notation, the active
traceless exponent satisfies

\[
(zS+z^2B)^2=(\alpha z^2+\beta z^4)I.
\]

Put

\[
\delta=\alpha z^2+\beta z^4,
\]

\[
c=\sum_n\frac{\delta^n}{(2n)!},\qquad
s=\sum_n\frac{\delta^n}{(2n+1)!}.
\]

Then

\[
c^2-\delta s^2=1
\]

and the entries of the full exponentials lie in

\[
\operatorname{span}\{1,\,
x^{\pm t}c,\,
x^{\pm t}zs,\,
x^{\pm t}z^2s\}.
\]

This gives a small exact diagonal overcode without choosing coordinates
for \(U\).

This parameterization is complete within its named scope: every
first-nonconstant pair supported on one fixed nondegenerate two-plane has
this form.  A nonzero skew-adjoint map in dimension two is invertible, so
the genuinely nonconstant case has \(\beta\ne0\).  The \(B=0\) boundary
is the already-excluded constant rank-two lane.

Decimation \(z\mapsto qz\), \(q\in\mathbf F_{37}^{\times}\), acts by

\[
(t,\alpha,\beta)\longmapsto
(qt,q^2\alpha,q^4\beta).
\]

There are:

```text
76 decimation orbits with t=0 and beta nonzero;
1,332 types after normalizing every t nonzero to t=1.
```

The first, deliberately very loose entry-product overcode gives:

```text
t=0:
  all 76 orbits have exactly the two weight-18 Paley words.

t nonzero:
  1,330 of 1,332 types have exactly the two weight-18 Paley words;

  (alpha,beta)=(5,32) has weights 14,18,18,22;
  (alpha,beta)=(19,20) has weights 12,18,18,24.
```

The overcode has dimension 18 when \(t=0\) and dimension 24 when
\(t\ne0\).  The nonzero-\(t\) census tests its \(2^{23}\) information
assignments by an exact meet-in-the-middle calculation.

Restoring the fact that the two matrices being conjugated, \(N_0\) and
\(J\), are symmetric gives an independent, much smaller overcode.  Write

\[
E_+=I+aP+bS+cB,\qquad
E_-=I+a'P+b'S+c'B.
\]

For any symmetric \(M\), reversal of a matrix product preserves its
diagonal.  Since \(P,S\) are symmetric and \(B\) is skew, every diagonal
entry of \(E_-ME_+\) lies in the span of only the following ten
coefficient functions:

\[
\begin{aligned}
1,&\quad a+a',\quad b+b',\quad c'-c,\quad a'a,\\
&a'b+b'a,\quad c'a-a'c,\quad b'b,\quad
c'b-b'c,\quad c'c.
\end{aligned}
\]

Allowing the ten matrix coefficients to vary independently, and doing the
same after multiplication by \(z^{18}\), is still a safe overcode.  Its
complete census is:

```text
t=0:
  dimension 12 for all 76 decimation orbits;
  exactly the two weight-18 Paley words in every orbit.

t nonzero:
  dimension 14 for all 1,332 normalized parameter types;
  1,330 types have exactly the two weight-18 Paley words;
  the same two exceptional types and four-word weight sets remain.
```

An independent polynomial-matrix calculation verifies all signs in this
ten-function reduction.  In particular, `c'-c` rather than `c+c'` is
forced because the diagonal of \(MB\) is the negative of the diagonal of
\(BM\) when \(M\) is symmetric and \(B\) is skew.  The two exceptions
are therefore genuine survivors of this safe diagonal overcode, not
artifacts of forgetting matrix symmetry.

## Intersection with all 625 quotients

The frozen canonical quotient dump has SHA-256

```text
c5d8765da49deb39c2ff3407b9d0f265e3ca56c1015d5b0075355c53ca60fb5b
```

Intersecting the symmetry-restored weight sets with the 111 diagonal
profiles gives:

```text
all-weight-18 types:                 0 quotient classes;
weight set {14,18,22}:               0 quotient classes;
weight set {12,18,24}:               4 quotient classes.
```

The four residual lexicographic permutation classes are

```text
107, 110, 222, 223
```

and all have diagonal-degree profile

```text
(12,12,18,18,18,18,18,24,24).
```

Only the parameter type

```text
t=1, alpha=19, beta=20
```

survives at the diagonal-overcode level.

The unique weight-12 and weight-24 words are complements.  The two
weight-18 words are the Paley pair.  Exhausting the five Paley choices
shows exactly five assignments for each of the two `6/3` trace
orientations, per quotient class.

Therefore the common nondegenerate two-plane family has been reduced to

```text
4 quotient classes
x 1 algebraic parameter type
x 10 trace-compatible diagonal-overcode assignments.
```

These forty formal assignments are the complete residue of this named
family under the symmetry-only overcode.  None is a binary support
witness.

## Restoring the fixed \(J\) term closes the residue

The exceptional parameter type has a further exact separation.  Let
\(F\) be the span of the ten ordinary coefficient functions above.  For

```text
t=1, alpha=19, beta=20
```

one has

```text
dim(F)=7;
dim(z^18 F)=7;
dim(F + z^18 F)=14.
```

Thus \(F\) and \(z^{18}F\) are in direct sum.  Every one of the four
exceptional binary words has a uniquely determined \(z^{18}F\)
component, independent of how generously the \(N_0\) contribution is
chosen inside \(F\).

Now restore only the fact that the \(z^{18}\) term conjugates the fixed
matrix \(J=\mathbf1\mathbf1^T\).  At coordinate \(i\), put

\[
p=(P\mathbf1)_i,\qquad
s=(S\mathbf1)_i,\qquad
b=(B\mathbf1)_i.
\]

The ten matrix coefficients multiplying \(z^{18}F\) are then forced to
be

\[
(1,p,s,b,p^2,ps,bp,s^2,bs,-b^2).
\]

The last sign follows from

\[
\operatorname{diag}(BJB)_i
=(B\mathbf1)_i(\mathbf1^TB)_i=-b^2.
\]

For each trace orientation \(\eta=\pm1\), the verifier exhausts all
\(37^3=50{,}653\) completely relaxed local triples \((p,s,b)\).
None realizes the required \(z^{18}F\) component of any of the four
exceptional words:

```text
eta=+1 survivor counts: 0,0,0,0;
eta=-1 survivor counts: 0,0,0,0.
```

This is stronger than a quotient-specific calculation.  It still ignores
all global projector identities and all \(N_0\) relations, so emptiness
is a safe obstruction.  Consequently the forty symmetry-overcode
assignments are spurious and the entire common nondegenerate two-plane
first-nonconstant family is impossible.

## Reproduction

From this directory:

```text
python3 verify_z37_yadic_frontier.py
python3 verify_first_nonconstant_gauge.py
python3 verify_exceptional_plane_fixed_j.py
python3 -m json.tool FIRST_NONCONSTANT_CERTIFICATE.json >/dev/null

clang++ -O3 -std=c++17 \
  search_first_nonconstant_plane_pencil.cpp \
  -o /tmp/search_first_nonconstant_plane_pencil
/tmp/search_first_nonconstant_plane_pencil
```

To replay the quotient intersection, first generate the promoted
canonical dump:

```text
clang++ -O3 -std=c++17 \
  ../census_z37_quotients.cpp \
  -o /tmp/census_z37_quotients
/tmp/census_z37_quotients --dump-canonical \
  > /tmp/z37_quotients_canonical.txt

python3 audit_first_nonconstant_plane_quotients.py \
  /tmp/z37_quotients_canonical.txt

shasum -a 256 -c FIRST_NONCONSTANT_ARTIFACT_SHA256.txt
```

On the M1 Pro used for the final audit:

```text
low-layer / pure-rank-two verifier:       0.31 s, 19.5 MB;
complete two-plane pencil census:         4.67 s,  5.3 MB;
fixed-J exceptional closure:              0.69 s, 18.0 MB;
quotient-profile intersection:            0.03 s, 19.7 MB;
baseline full y-adic frontier verifier:   6.88 s, 100.2 MB;
full 625-class quotient replay:          46.10 s, 59.0 MB.
```

These runs were sequential.  No check approached the 16 GB hardware
limit.

## Honest boundary

The result closes the pure rank-two higher term and the full common
nondegenerate two-plane pencil.  It does not exclude:

- a degenerate common support with a nonzero \(A_0\);
- coefficients whose active supports change with degree;
- rank at least three;
- a general binary semiregular \(C_{37}\) lift.

The next high-value calculation is the degenerate support
(\(J_3\) or \(J_2\oplus J_2\) leading type) with nonzero \(A_0\),
followed by generators whose active support changes between the two
degrees.

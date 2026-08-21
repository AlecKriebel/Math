# Exact audit of the binary fixed-conic endgame composition

**Completed:** 2026-07-26T10:41:51Z

## Verdict

\[
\boxed{\textbf{PASS}}
\]

Starting from the complete E7 fibres in
`fixed_conic_binary_repair_sympy`, every split-root and double-root
tangent orbit was solved through its terminal obstruction or binary
automorphism exit.  The displayed legacy families (13)--(36) span the
complete surviving fibres.  No omitted branch or counterexample was
found.

## 1. Method and fail-closed boundary

The strict checker imports and executes the sibling E7/E6 repair before
performing any endgame calculation.  Thus its inputs retain:

* all compatible coefficients of the twelve-parameter binary cubic
  \(V\);
* all eleven free coefficients in the complete E7 \(H_2\) fibre; and
* all nine entries of the arbitrary linear part \(L\).

For
\[
D(s)=\det(L+sJH_2+s^2JH_3+s^3JH_4),
\]
the checker constructs each required coefficient
\([s^k]D(s)\) directly by determinant multilinearity.  It does not load a
pre-solved legacy family until the equations from the complete fibre have
forced that family.

Every affine solve uses a constant rational coefficient matrix.  The only
nonconstant fixed minor is
\[
-262144K^3
\]
on the explicitly recorded nilpotent chart \(K\ne0\); the \(K=0\) fibre
is solved independently.  Square implications are used only over
\(\mathbb C\).  The checker contains no Python `assert` statements and is
run under `python -O`.

## 2. Split-root branches

### 2.1 Scalar tangent \(2A\)

The complete E7 fibre first gives four linear E6 relations
\[
v_9=2v_4,\quad v_0+v_{10}=2v_5,\quad
v_1+v_{11}=2v_6,\quad v_2=2v_7.
\]
The two endpoint E6 coefficients then become
\[
12v_4^2,\qquad12v_7^2,
\]
and the next endpoint coefficients force \(w_{12}=w_2=0\).
Consequently the complete cubic fibre is exactly (13), with parameters
\((U,V,X,Y)\).

The remaining E6 system has constant rank \(3\) in
\((\ell_2,\ell_5,\ell_8)\).  The \(r\)-dependent E5 coefficients have
constant rank \(3\) and force precisely the three missing relations in
(14).  The remaining E5 system has constant rank \(4\), leaving only
\(\ell_4,\ell_7\).

The four division-free E4 squares are exactly
\[
(S-2X)^2,\quad(T+2Y)^2,\quad
(B_0-UX+X^2)^2,\quad(B_2+VY+Y^2)^2.
\]
After these vanish, the remaining E4 coefficient is the square of
\[
B_1-C+UY+VX+XY.
\]
Thus (15)--(16) are complete, not a specialization.  E8 through E3 then
vanish identically, while E2 and \(\det L\) reproduce (17)--(19).
The two E2 coefficients force the factor of \(\det L\) to vanish.

### 2.2 Opposite-weight tangent \(pA_p-qA_q\)

The full E6 system forces exactly the six zero conditions and two linear
relations in (11), including the outer pivots \(w_{12}=w_2=0\).  Replacing
the remaining affine coordinate by the actual \(pr\)-coefficient of the
second target component gives exactly the legacy \(H_3,H_2\) family.

E6 has constant rank \(3\) in \(L\).  After that solve, E5 has rank \(4\)
in the six remaining entries and its complete compatibility list contains
the constant
\[
-64.
\]
This is equation (12), up to harmless sign.

### 2.3 Zero tangent

At zero tangent the complete E7 fibre is exactly
\[
H_3=V(p,q),\qquad
H_2=B(p,q)+r(\alpha A_p+\beta A_q).
\]
The diagonal/anti-diagonal stabilizer of \(pq\), together with \(r\)
scaling, gives the three support orbits in (21).

For \((1,0)\), E6 forces
\[
v_8=0,\quad v_2=-6v_7,\quad v_3=0,
\]
and the complete E5 compatibility contains \(8\).
For \((1,1)\), E6 additionally forces \(v_9=-6v_4\), and E5 contains
the three constants of (22), with magnitudes \(8,16,8\).

For \((0,0)\), every nonlinear homogeneous part is binary.  The exact
checker retains this independence of \(r\); the plane-plus-shear argument
then gives the automorphism exit.

## 3. Double-root branches

### 3.1 Scalar tangent \(2A\)

E6 first forces
\[
v_8=0,\quad v_9=2v_4,\quad v_0+v_{10}=2v_5,\quad
v_1+v_{11}=2v_6,\quad v_7=0.
\]
In the remaining coordinates \(Y=v_{11}-v_6\), E6 also gives
\[
w_2=3Y^2,\qquad
w_1=2w_8+2TY+6XY.
\]
The endpoint E5 coefficient is \(-24Y^2\), so \(Y=0\).  The other
\(r\)-dependent E5 coefficients give exactly (24), while the E6 and E5
linear ranks are \(3\) and \(4\).

E4 supplies the squares
\[
(S-Z)^2,\quad(T+2X)^2,\quad
(2B_0-UZ)^2,\quad(B_2+VX)^2,
\]
followed by the square of the final \(C\)-relation in (25).  Equations
(26)--(27) and the singular-linear-part exit then follow identically.

### 3.2 Semisimple tangent \(pA_p\)

Five direct E6 pivots reduce the full E7 fibre to an affine family with
three deviation parameters \(G,P,J\).  The E5 coefficients of
\(p^2qr^2,pq^2r^2,q^3r^2\) are respectively
\[
2G,\qquad2P,\qquad6J.
\]
Their vanishing leaves exactly (28)--(29); the remaining E5 relation is
the displayed \(T^2q^2\) coefficient.

The stacked E6/E5/E4 linear system has shape \(17\times9\).  A fixed
\(9\times9\) minor is exactly
\[
32768.
\]
Its unique solution agrees entry-by-entry with (30), satisfies every
unused equation, and has determinant zero.

### 3.3 Nilpotent tangent \(pA_q\)

The full E6 solve first forces
\[
v_{10}=w_{16},\quad
w_{10}=v_6-\frac32v_{11},\quad v_2=v_7=0.
\]
Put \(K=v_6\), \(J=v_{11}\), and \(G=v_{10}\).  E5 then gives, without
division,
\[
J=0,\qquad
w_{14}=\frac{G^2}{4},\qquad
w_8=\frac{GK}{2},\qquad
K(v_1-2K)=0.                                      \tag{N}
\]
This is exactly (31), with \(w_3=v_1-2K\).

On \(K\ne0\), (N) gives \(v_1=2K\).  The remaining E5 coefficient gives
\[
3K^2(G+v_0-2v_5)=0,
\]
and E4 gives
\[
-3K^2v_8=0,\qquad-3K^2(v_9-2v_4)=0.
\]
These are precisely (32), and the resulting family is exactly the first
legacy nilpotent family.  The fixed lower linear minor is
\(-262144K^3\), every unused equation vanishes, and the unique \(L\) is
singular.

On \(K=0\), no factor in (N) is divided out.  The second legacy family
retains every surviving coefficient.  E6 and E5 give
\[
\ell_1=\frac{G}{2}\ell_2,\qquad
\ell_4=\frac{G}{2}\ell_5,\qquad
\ell_7=\frac{G}{2}\ell_8,
\]
where here \(G=v_{10}\).  This is (33), so columns two and three of \(L\)
are dependent.  The essential rank-jump branch is therefore complete.

### 3.4 Zero tangent

The complete E7 fibre again has the directional form
\[
B(p,q)+r(\alpha A_p+\beta A_q).
\]
The lower-triangular stabilizer of \(p^2\) gives the three Borel orbits in
(34).

For the \(A_p\) orbit, E6 gives exactly (35), then E5 contains the
constant \(8\).  For the \(A_q\) orbit, E6 gives exactly (36), and E5
again contains \(8\).  The zero direction is binary and exits by the same
plane-plus-shear argument.

## 4. Retained checker

Run from `dimension_three_keller_degree/rung2_degree_bound`:

```sh
taxonomy_freeze/fixed_conic_binary_endgames_sympy/verify_strict.sh
```

The strict replay takes about eleven seconds on the recorded machine and
uses roughly 72 MB maximum resident memory.  A zero exit prints
`PASS binary fixed-conic fibre-to-endgame composition`.

No ledger, branch, commit, or remote state is modified.

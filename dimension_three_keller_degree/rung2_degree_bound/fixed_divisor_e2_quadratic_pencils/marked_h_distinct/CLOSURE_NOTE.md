# Exclusion of the marked-distinct fixed-quadratic frontier

**First candidate record (UTC):** 2026-07-26T00:01:30Z.
**Certified (UTC):** 2026-07-26T00:31:14Z.

> **Status.**  Certified internal structural theorem.  The thirteen-stratum
> denominator was frozen before the lower calculation.  The projective
> family and six endpoints have independent SymPy/PARI reconstructions.
> A clean-room dependency-free replay independently reconstructed the two
> discrete orbits and the assembled post-freeze bridge.  The parent row is
> now certified excluded.  This does not improve the universal degree floor.

> **Review and disclosure.**  This note is not peer reviewed and was
> produced with substantial AI assistance.  Exact checks are evidence about
> the encoded algebra, not peer review, a proof of novelty, or a verification
> by the mathematical community.

## 1. Statement

Let
\[
F=LX+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have degree at most four, with \(H_j\) homogeneous of degree \(j\).  Suppose
that legal linear source and target changes put its leading data in the
all-vertical form
\[
H_4=(h^2,hs,0),\qquad
s=\ell^2,\qquad
(H_3)_3=\ell r,                                      \tag{1}
\]
where:

- \(\langle h,s\rangle\) is a minimal quadratic pencil;
- \(s\) is its unique double-line member;
- \(h\ne s\) is the marked fixed quadratic gcd; and
- \([r]\in\mathbb P\langle h,s\rangle\), or \(r=0\).

### Theorem

Under these hypotheses, if \(F\) has nonzero constant Jacobian determinant,
then \(F\) is a polynomial automorphism.  More precisely, the nonzero
companion strata cannot have nonzero constant Jacobian determinant, while
the zero-companion strata are settled by the unconditional
quadratic-component automorphism theorem.

This is a theorem about the marked-distinct frontier (1), not about every
quartic leading form.  Combined with the separately audited marked-equal
theorem \(h=s\) and the certified top-obstruction bridge, it closes the
single frozen row `Q2-E2-A2-B1-D1-N1`.

## 2. The frozen denominator

The marked pair \((s,h)\), together with the projective companion \([r]\),
has exactly three pair types:
\[
(x^2,yz),\qquad
(x^2,x^2+yz),\qquad
(x^2,y^2+xz).                                       \tag{2}
\]
Their nonzero companion quotients are respectively
\[
3,\qquad\mathbb P^1,\qquad3.                         \tag{3}
\]
Including the zero companion gives thirteen stable strata:
\[
\boxed{4+5+4=13}.                                    \tag{4}
\]

For the middle family put
\[
h=x^2+yz,\qquad s=x^2,\qquad
r_{[u:v]}=uh+vs.                                    \tag{5}
\]
The frozen projective boundaries are
\[
\begin{array}{c|c|c}
\text{suffix}&[u:v]&r\\ \hline
\mathrm{CH}&[1:0]&h\\
\mathrm{CT}&[1:-1]&yz\\
\mathrm{CS}&[0:1]&s\\
\mathrm{CTAU}&uv(u+v)\ne0&h+(v/u)s.
\end{array}                                          \tag{6}
\]
The stabilizer acts trivially on this pencil line, so different `CTAU`
parameters are genuinely inequivalent.

The taxonomy (2)--(6) was derived twice independently and frozen before
the calculations below.  A lower pivot divisor must be handled by a fresh
chart; it cannot be appended silently as a new case.

## 3. Zero companions

If \(r=0\), then
\[
(H_4)_3=(H_3)_3=0.
\]
The third target component has degree at most two.  The unconditional
quadratic-component theorem therefore makes \(F\) a polynomial
automorphism.  This excludes the three `C0` strata from the counterexample
locus; it does not assert that Keller automorphisms cannot occur there.

## 4. Uniform exclusion of the middle projective family

On the finite chart \(u=1\), put \(k=v/u\).  For every \(k\ne0\), the
complete degree-seven normal form modulo two target shears and three source
translations is
\[
\begin{aligned}
H_4&=((x^2+yz)^2,x^2(x^2+yz),0),\\
H_3&=(Ax^3,Bx^3,x((x^2+yz)+kx^2)),\\
(H_2)_3&=Tx^2.
\end{aligned}                                        \tag{7}
\]
Two \(E_7\) maximal minors have residual factors
\[
q(k)=9k^2+6k-1,\qquad 3k-1.
\]
They cover every \(k\ne0\), since
\[
\frac12q(k)-\frac32(k+1)(3k-1)=1.                   \tag{8}
\]

Write the first two quadratic components in monomial order
\[
(x^2,xy,xz,y^2,yz,z^2)
\]
with coefficients \(a_i,b_i\), and write
\[
L=
\begin{pmatrix}
\ell_0&\ell_1&\ell_2\\
\ell_3&\ell_4&\ell_5\\
\ell_6&\ell_7&\ell_8
\end{pmatrix}.
\]
For
\[
\mathcal J(w)=L+wJH_2+w^2JH_3+w^3JH_4,\qquad
E_j=[w^j]\det\mathcal J(w),
\]
the twelve nonzero coefficients of \(E_6\) form four triangular chains.
They give
\[
\begin{gathered}
b_3=a_3=b_5=a_5=0,\\
b_1=2\ell_7,\quad a_1=-12k\ell_7,\quad
-36k^2\ell_7=0,\\
b_2=2\ell_8,\quad a_2=-12k\ell_8,\quad
36k^2\ell_8=0.
\end{gathered}                                       \tag{9}
\]
Since \(k\ne0\),
\[
a_1=a_2=a_3=a_5=b_1=b_2=b_3=b_5=\ell_7=\ell_8=0.
\tag{10}
\]
No factor from (8) is divided out in this step.

After (10), the last four useful \(E_5\) coefficients are
\[
\begin{array}{c|c}
x^2y^2z&-\ell_1-(6k+4)\ell_4\\
x^2yz^2&\ell_2+(6k+4)\ell_5\\
y^3z^2&-2\ell_4\\
y^2z^3&2\ell_5 .
\end{array}                                          \tag{11}
\]
Thus
\[
\ell_1=\ell_2=\ell_4=\ell_5=0.
\]
Together with \(\ell_7=\ell_8=0\), this leaves only the first column of
\(L\), so \(\det L=0\).

This excludes every `CTAU` value and also the finite boundary `CT`,
\(k=-1\).  The omitted charts \(k=0\) and \(u=0\) are rebuilt as `CH` and
`CS` below.

## 5. The six endpoint strata

The released endpoint calculation gives complete \(E_7\) normal forms for
the `CH` and `CS` companions in all three marked pairs.  Their \(E_6\)
compatibility ideals are:
\[
\begin{array}{c|c}
\text{endpoint type}&I_6\\ \hline
\mathrm{RT/H}&
(AC,AD,AE,AF,CE,DF,E^2,F^2)\\
\mathrm{RT/S}&(C^2,D^2)\\
\mathrm{RO/H}&
(AC,AD,AE,AF,CF+DE,EF,2DF-E^2,F^2)\\
\mathrm{RO/S}&(CD,D^2).
\end{array}                                          \tag{12}
\]

For either RT/H endpoint, (12) gives \(E=F=0\) and \(A(C,D)=0\).
If \(A=0\), polynomial left syzygies of \(E_5\) have values
\[
12C^3,\qquad-12D^3.
\]
Hence \(C=D=0\) on every branch.  The \(A\ne0\) solve and the fresh \(A=0\)
solve both force \(\det L=0\) at \(E_5\).

For the RO/H endpoint, (12) again gives \(E=F=0\) and \(A(C,D)=0\).
On \(A=0\), global \(E_5\) syzygies include
\[
-24D^3,\qquad -12C(6BD-C^2).
\]
They successively force \(D=C=0\).  All \(A\ne0\) branches and the
\(A=T=0\) boundary then force a singular \(L\) at \(E_5\).

There is one sharp branch:
\[
A=C=D=E=F=0,\qquad T\ne0.                            \tag{13}
\]
It has invertible examples through \(E_5\), so it cannot be discarded.
After the complete \(E_6/E_5\) solve, its determinant is divisible by
\(\ell_7\), while two literal coefficients of \(E_4\) are
\[
[xy z^2]E_4=-8\ell_8^2,\qquad
[x^2yz]E_4=-4\bigl(2(b_0-\ell_6)\ell_8-\ell_7^2\bigr).
\tag{14}
\]
Equation (14) gives \(\ell_8=\ell_7=0\), hence \(\det L=0\).

For the two RT/S endpoints, (12) gives \(C=D=0\), and the resulting
constant-rank \(E_5\) solve forces \(\det L=0\).  For RO/S, \(D=0\);
a global \(E_5\) syzygy has value \(2C^3/9\), so \(C=0\).  Fresh
\(A\ne0\) and \(A=0\) solves both force a singular \(L\).

Thus all six `CH/CS` endpoints are excluded.  Five die at \(E_5\), while
the sharp branch (13) dies at \(E_4\).

## 6. The two discrete open companions

For the rank-two reducible marked pair, the `CO` representative is
\[
(h,r)=(yz,x^2+yz).
\]
The raw \(E_7\) matrix has rank \(18\), with five legal gauge directions
and complete normal complement
\[
(x^3,0,0),\qquad(0,x^3,0),\qquad(0,0,x^2).           \tag{15}
\]
The \(E_6\) and \(E_5\) matrices have constant ranks \(10\) and \(4\).
Their complete solves zero the six off-axis entries of \(L\), so
\(\det L=0\).

For the rank-one smooth marked pair, take
\[
(h,r)=(y^2+xz,x^2+y^2+xz).
\]
Again the raw \(E_7\) rank is \(18\).  A complete normal complement is
\[
(x^3,0,0),\quad(0,x^3,0),\quad
(2z(y^2+xz),x^2z,xz).                                \tag{16}
\]
Let \(\rho\) multiply the last vector.  The \(E_6\) matrix has constant
rank \(10\) and no compatibility residual.  On \(\rho\ne0\), an \(E_5\)
rank-four minor is \(-1296\rho^2\), and the solve zeros the second column
of \(L\).  The pivot divisor \(\rho=0\) is rebuilt: its fresh \(E_5\)
matrix has rank four and forces \(\det L=0\) as well.

This excludes both `CO` strata.

## 7. Exhaustiveness and verification

The routes above account for the frozen denominator exactly:
\[
3\ \mathrm{C0}
+2\ \mathrm{CO}
+6\ \mathrm{CH/CS}
+1\ \mathrm{CT}
+1\ \mathrm{CTAU}
=13.
\]
The `CTAU` entry denotes the entire punctured parameter line, not one
orbit.  Its three projective boundaries are explicitly rebuilt.

The verification packages are:

- `quartic_survivor_search/`: exact SymPy/PARI uniform and endpoint
  reconstructions, sharp witness, modular regressions, and immutable-input
  guard;
- `endpoint_closure/verify_endpoint_closure_sympy.py`: a second exhaustive
  endpoint branch reconstruction;
- `co_closure/verify_co_closure_sympy.py`: raw \(E_7\) quotient,
  constant minors, and both \(\rho\)-charts for the two `CO` orbits;
- `../audit_marked_orbit_reconstruction/` and
  `../audit_marked_orbit_hostile_2/`: the two independent frozen-denominator
  reconstructions.

The assembled parent-row bridge is
`../../taxonomy_freeze/BRIDGE_Q2_E2_A2_B1_D1_N1_v1.md`; its clean-room
hostile replay is
`../../taxonomy_freeze/audit_bridge_q2_e2_v1/REPORT.md`.

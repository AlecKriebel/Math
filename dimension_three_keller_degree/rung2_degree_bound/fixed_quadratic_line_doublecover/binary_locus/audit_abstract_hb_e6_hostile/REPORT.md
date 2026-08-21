# Hostile audit: abstract binary-quartic Hilbert--Burch and \(E_6\) lemma

**Verdict: PASS.**

**Audit completed:** 2026-07-25T10:59:04Z.

The candidate lemma in `../ABSTRACT_BINARY_QUARTIC_HB_E6.md` is
mathematically correct under its intended homogeneous-piece setup.  I found
no counterexample over \(\mathbb C\), no omitted algebraic stratum, and no
sign error.  In particular, the \(R=0\) separation, the
\(\alpha/\beta\)-dependent power fibre, all six Hilbert--Burch/nullity rows,
the wedge determinant, the signed \(E_6\) formula, and the \(\delta=0\)
plane-shear exit all survive independent reconstruction.

There are two nonfatal exposition points:

1. For a literally standalone statement, the note should say explicitly
   that \(U,V,R\) are homogeneous cubics, \(A,B,T\) are homogeneous
   quadratics, and that the weighted determinant is formed from
   \(L_0+zJH_2+z^2JH_3+z^3JH_4\).  Those assumptions are already clear from
   the surrounding homogeneous-piece notation.
2. The height-two justification and the scalar rescaling in the power-fibre
   conclusion are compressed in the candidate proof.  Both are valid; the
   missing sentences are supplied below.

Neither point changes a conclusion or requires a new hypothesis.

## 1. \(R=0\) really is a separate boundary

With
\[
\alpha=J(Q,R),\qquad\beta=-J(P,R),\qquad\gamma=J(P,Q),
\]
the case \(R=0\) has
\[
(\alpha,\beta,\gamma)=(0,0,\gamma).
\]
Its three \(E_7\) block ranks are therefore
\[
(0,1,2),
\]
so its nullities are \((2,4,6)\), not any row of the nonexceptional table.
Moreover the degree convention
\((5-\delta,5-\delta,6-\delta)\) is inapplicable: here the gcd is
\(\gamma\), of degree six.

Geometrically, \(H_4=(P,Q,0)\) and \(R=(H_3)_3=0\) make the third component
of the full degree-four map have degree at most two.  It is nonconstant
because \(L_0\) is invertible.  The banked quadratic-component exit applies:
a quadratic submersion is a degree-at-most-two polynomial coordinate,
conjugation produces \((G_1,G_2,X_3)\) of degree at most eight, every plane
fibre is an automorphism by the unconditional plane lower bound, and
injectivity plus Ax--Grothendieck finishes.  This uses no form of the plane
Jacobian Conjecture.

Thus removing \(R=0\) before both the Hilbert--Burch and power-fibre
arguments is necessary and sufficient.

## 2. Height, minimality, and the Hilbert--Burch degrees

Assume \(R\ne0\) and that \(\alpha,\beta\) are constant-linearly
independent.  Let
\[
g=\gcd(\alpha,\beta,\gamma),\qquad \delta=\deg g,\qquad
(\alpha_0,\beta_0,\gamma_0)=g^{-1}(\alpha,\beta,\gamma),
\]
and put \(d=5-\delta\).

The two degree-five forms \(\alpha,\beta\) give \(\delta\le5\).  Equality
\(\delta=5\) would make \(\alpha_0,\beta_0\) two nonzero constants, which
are necessarily constant-linearly dependent.  Hence
\[
\delta\le4,\qquad d\ge1.                                      \tag{1}
\]
This resolves the only possible unit-ideal boundary.

The reduced ideal
\[
I=(\alpha_0,\beta_0,\gamma_0)\subset\mathbb C[p,q]
\]
is proper because its generator degrees are \((d,d,d+1)\) with \(d\ge1\).
No height-one prime contains \(I\), since such a prime would divide all
three reduced generators, contrary to their gcd being one.  Therefore
\(\operatorname{ht} I=2\).  Hilbert--Burch applies without any coprimality
assumption on the original \(P,Q\).

Let \(e_1,e_2\) be the total degrees of a homogeneous basis of the syzygy
module.  The exact graded resolution gives
\[
e_1+e_2=d+d+(d+1)=3d+1.                              \tag{2}
\]
This remains true if the displayed three generators are not a minimal
generating set for \(I\); a unit entry can occur in the presentation, but
the graded kernel is still free of rank two and the Hilbert-series identity
is unchanged.

A syzygy of total degree \(e\le d\) has zero \(\gamma_0\)-coefficient and,
at \(e=d\), only constant \(\alpha_0,\beta_0\)-coefficients.  Constant
independence excludes it.  Thus
\[
e_i\ge d+1.                                             \tag{3}
\]
The two gradient columns have total degree \(d+3\) and are independent
because their wedge is
\[
(\nabla_p,\nabla_q)^\wedge
  =(\alpha,\beta,\gamma)\ne0.
\]
If one \(e_i>d+3\), both gradient columns would have zero coefficient along
that basis vector and would be dependent over \(\mathbb C(p,q)\).
Consequently \(e_i\le d+3\).  Therefore
\[
k_i=d+3-e_i\in\{0,1,2\}.                              \tag{4}
\]

## 3. Wedge determinant and the removed gcd

Choose a homogeneous Hilbert--Burch basis \(N_1,N_2\), and write
\[
(\nabla_p,\nabla_q)=(N_1,N_2)C.
\]
The signed maximal minors of a Hilbert--Burch basis are a unit multiple of
the primitive row:
\[
N_1\wedge N_2=c(\alpha_0,\beta_0,\gamma_0),
\qquad c\in\mathbb C^\times.
\]
Wedge the displayed factorization.  Since the left side is
\(g(\alpha_0,\beta_0,\gamma_0)\),
\[
\det C=c^{-1}g.                                        \tag{5}
\]
Row \(i\) of \(C\) is homogeneous of degree \(k_i\); nonvanishing of the
determinant ensures neither row is identically zero.  Hence
\[
k_1+k_2=\deg g=\delta.                                 \tag{6}
\]

There is also an independent arithmetic check on (6):
\[
k_1+k_2=2(d+3)-(e_1+e_2)
       =2d+6-(3d+1)=5-d=\delta.
\]
Thus the wedge proof has no cancellation or primitivity gap.

## 4. Every \(k\)-shape and every nullity

At the three powers of \(r\), the coefficient triples in \(E_7\) have
degrees
\[
\begin{array}{c|c|c}
\text{block}&\text{coefficient degrees}&\text{total syzygy degree}\\ \hline
r^2&(0,0,-1)&d\\
r^1&(1,1,0)&d+1\\
r^0&(2,2,1)&d+2.
\end{array}
\]
Because the syzygy module is freely generated in degrees
\(e_i=d+3-k_i\):

- a \(k_i=0\) column contributes to none of these blocks;
- a \(k_i=1\) column contributes one constant multiplier to \(r^0\);
- a \(k_i=2\) column contributes one constant multiplier to \(r^1\) and
  two binary-linear multipliers to \(r^0\).

Together with \(k_i\in\{0,1,2\}\) and \(k_1+k_2=\delta\), this gives exactly
\[
\begin{array}{c|c|c}
\delta&\{k_1,k_2\}&(r^2,r^1,r^0)\text{ nullities}\\ \hline
0&\{0,0\}&(0,0,0)\\
1&\{1,0\}&(0,0,1)\\
2&\{1,1\}&(0,0,2)\\
2&\{2,0\}&(0,1,2)\\
3&\{2,1\}&(0,1,3)\\
4&\{2,2\}&(0,2,4).
\end{array}
\]
Multiplication of the reduced row by the nonzero gcd \(g\) changes no
polynomial kernel, including in these bounded homogeneous degrees.

The independent PARI certificate builds a primitive Hilbert--Burch matrix
for each of the six \(k\)-shapes, checks the generator degrees and
constant independence, multiplies by an explicit degree-\(\delta\) gcd,
and recomputes all three coefficient-matrix ranks.  It also checks the
gradient-column wedge with the gcd retained.

## 5. The \(\alpha/\beta\)-dependent power fibre

If \(\alpha,\beta\) are constant-linearly dependent, there are constants
\(\lambda,\mu\), not both zero, for which
\[
S=\lambda P+\mu Q,\qquad J(S,R)=0.
\]
The form \(S\) is nonzero, because \(J(P,Q)\ne0\) makes \(P,Q\)
constant-linearly independent.  Also \(R\ne0\) by the separate boundary
step.

Euler's identities give the exact polynomial relations
\[
\begin{aligned}
3R S_p-4S R_p&=qJ(S,R),\\
3R S_q-4S R_q&=-pJ(S,R).
\end{aligned}                                          \tag{7}
\]
Thus \(J(S,R)=0\) makes \(S^3/R^4\) constant in
\(\mathbb C(p,q)\).  Hence
\[
S^3=cR^4,\qquad c\in\mathbb C^\times.                  \tag{8}
\]
Unique factorization and \(\gcd(3,4)=1\) imply
\[
S=a\ell^4,\qquad R=b\ell^3
\]
for a linear form \(\ell\) and nonzero scalars \(a,b\).  Indeed, the common
base divisor has degree one because the displayed forms have degrees four
and three.  Choose \(L=b^{1/3}\ell\), so \(R=L^3\), and rescale the
dependence vector \((\lambda,\mu)\) to make \(S=L^4\).  This proves the
candidate's normalized conclusion without an unstated compatibility
between \(a\) and \(b\).

The audit also tested a nondegenerate exact power-fibre family with
\(J(P,Q)\ne0\) and a perturbation leaving the fibre.  No exceptional
\(S=0\), \(R=0\), or scalar-normalization branch remains.

## 6. Signed \(E_6\)

Write the weighted Jacobian as
\[
M(z)=L_0+z
\begin{pmatrix}A&v\\t&\tau\end{pmatrix}
+z^2\begin{pmatrix}C&u\\w&0\end{pmatrix}
+z^3\begin{pmatrix}D&0\\0&0\end{pmatrix}.
\]
Selecting all weight-six determinant terms gives:

- weights \(3+3+0\):
  \((\det D)(L_0)_{33}\);
- weights \(3+2+1\):
  \[
  \operatorname{tr}(\operatorname{adj}C\,D)\tau
  -w\operatorname{adj}D\,v
  -t\operatorname{adj}D\,u;
  \]
- weights \(2+2+2\):
  \(-w\operatorname{adj}C\,u\).

This is exactly the candidate formula.  Direct calculation also gives
\[
-w\operatorname{adj}D=(\alpha,\beta),\qquad\det D=\gamma,
\]
with the candidate's signs.  Re-expansion using honest homogeneous
polynomials verifies the equivalent formula
\[
\alpha A_r+\beta B_r+\gamma(L_0)_{33}
+\det(dP,dV,dT)+\det(dU,dQ,dT)+\det(dU,dV,dR).
\]

The certificate detects independent sign flips in the \(\beta\), \(\gamma\),
\(\tau\), \(w\operatorname{adj}D\,v\),
\(t\operatorname{adj}D\,u\), and
\(w\operatorname{adj}C\,u\) terms, as well as a sign flip in the
determinant-sum form.

## 7. The \(\delta=0\) exit

For \(\delta=0\), all three \(E_7\) blocks are injective.  Hence
\[
U_r=V_r=T_r=0.
\]
Every curvature term in \(E_6\) contains \(u\) or \(\tau\), so it vanishes,
and
\[
\alpha A_r+\beta B_r+\gamma(L_0)_{33}=0.              \tag{9}
\]
The coefficient of \(r\) in (9) is the injective
\((0,0,-1)\) syzygy problem, and the binary part is the injective
\((1,1,0)\) problem.  Therefore
\[
A_r=B_r=0,\qquad(L_0)_{33}=0.
\]
All nonlinear terms are binary.

Postcomposition by \(L_0^{-1}\) gives
\[
G=(p+n_1(p,q),\,q+n_2(p,q),\,r+n_3(p,q)).
\]
Its Jacobian determinant is the Jacobian of the first two coordinates.
That plane Keller map has degree at most four and is an automorphism by the
unconditional plane lower bound.  Recovering \(p,q\) first and then
\(r=G_3-n_3(p,q)\) gives the triangular inverse.  The audit retained
arbitrary invertible \(L_0\); no normalization of its \((3,3)\) entry is
used.

## 8. Independent exact certificate

Run:

```sh
./verify_strict_and_faults.sh
```

The strict PARI/GP run checks:

- \(E_8,E_7,E_6\) by a fresh weighted \(3\times3\) determinant expansion;
- the actual-gradient \(\alpha,\beta,\gamma\) orientation;
- the determinant-sum version of \(E_6\);
- the \(R=0\) ranks;
- primitive Hilbert--Burch matrices for all six \(k\)-shapes;
- every block nullity and both \(\delta=2\) possibilities;
- the wedge gcd;
- the \(\delta=5\) constant-dependence guard;
- the Euler/UFD power-fibre identities; and
- the \(\delta=0\) injections and a plane-plus-shear inverse.

Fourteen fail-closed mutations independently alter signs, ranks,
primitivity, the \(R=0\) boundary, the height boundary, the power fibre,
and the shear inverse.  Every mutation is required to exit nonzero through
the intended guard.

This audit was AI-assisted and is not peer reviewed.  Exact checks are
evidence about the encoded algebra, not peer review.  The mathematical
proof above, rather than finite testing, is what establishes the universal
claims.

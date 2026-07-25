# Candidate global taxonomy of quartic leading rows

**Recorded (UTC):** 2026-07-25T19:30:28Z.

**Status:** the fourteen-row leading list is proved below, but the global
freeze is not certified.  Incidence leaves and boundary charts are still
being inventoried, and the blinded derivation is pending.

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow\mathbb A^3_{\mathbb C}
\]
have total degree four and constant nonzero Jacobian determinant.  Thus
\(H_4\ne0\).  The degree-nine determinant identity is
\[
\det JH_4=0,
\]
so \(1\le\operatorname{rank}JH_4\le2\).

## Rank one

If \(\operatorname{rank}JH_4=1\), homogeneity and Euler's identity imply
\[
H_4=a\,h
\]
for a nonzero constant target vector \(a\) and a quartic form \(h\).
This is the single leading row `Q1`.  Its mandatory incidence refinement
uses the cubic pencil obtained by projecting \(H_3\) modulo
\(\mathbb Ca\); that refinement is not yet frozen.

## Rank two

For rank two, the affine cone image has dimension two and its projective
image is an irreducible rational curve.  In minimal-pair form,
\[
H_4=hA(p,q),\qquad e+ab=4.
\]
Here \(h\) is the component gcd of degree \(e\); \(p,q\) are coprime
homogeneous forms of common degree \(a\) and generate the relatively
algebraically closed pencil field; and \(A\) is a basepoint-free binary
triple of degree \(b\).  If the image curve has degree \(\delta\) and
the parametrization has generic degree \(\nu\), then
\[
b=\delta\nu.
\]

The positive-integer solutions of \(e+ab=4\), followed by the
factorizations \(b=\delta\nu\), give exactly thirteen rows:

| Stable ID | \(e\) | \(a\) | \(b\) | \(\delta\) | \(\nu\) | Leading mechanism | Current row status, not part of completeness proof |
|---|---:|---:|---:|---:|---:|---|---|
| `Q2-E0-A4-B1-D1-N1` | 0 | 4 | 1 | 1 | 1 | primitive quartic line pencil | open |
| `Q2-E0-A2-B2-D1-N2` | 0 | 2 | 2 | 1 | 2 | quadratic pencil followed by a line double cover | excluded, audited |
| `Q2-E0-A2-B2-D2-N1` | 0 | 2 | 2 | 2 | 1 | quadratic pencil followed by the Veronese conic | excluded, audited |
| `Q2-E0-A1-B4-D1-N4` | 0 | 1 | 4 | 1 | 4 | binary quartic line cover | open |
| `Q2-E0-A1-B4-D2-N2` | 0 | 1 | 4 | 2 | 2 | conic double cover | excluded, audited |
| `Q2-E0-A1-B4-D4-N1` | 0 | 1 | 4 | 4 | 1 | birational rational quartic curve | open |
| `Q2-E1-A3-B1-D1-N1` | 1 | 3 | 1 | 1 | 1 | fixed linear divisor times a primitive cubic pencil | open |
| `Q2-E1-A1-B3-D1-N3` | 1 | 1 | 3 | 1 | 3 | fixed linear divisor times a line triple cover | open |
| `Q2-E1-A1-B3-D3-N1` | 1 | 1 | 3 | 3 | 1 | fixed linear divisor times a rational cubic curve | excluded, audited |
| `Q2-E2-A2-B1-D1-N1` | 2 | 2 | 1 | 1 | 1 | fixed quadratic divisor times a primitive quadratic pencil | excluded, audited |
| `Q2-E2-A1-B2-D1-N2` | 2 | 1 | 2 | 1 | 2 | fixed quadratic divisor times a line double cover | open |
| `Q2-E2-A1-B2-D2-N1` | 2 | 1 | 2 | 2 | 1 | fixed quadratic divisor times a conic | excluded, audited |
| `Q2-E3-A1-B1-D1-N1` | 3 | 1 | 1 | 1 | 1 | fixed cubic divisor times a line | excluded, audited |

Together with `Q1`, the current candidate leading denominator is
\[
\boxed{14\text{ rows}: 7\text{ audited excluded and }7\text{ open}.}
\]
This denominator is not yet the F1 denominator because the mandatory
incidence-leaf manifests have not been frozen.

## Completeness of the leading list

For \(e=0,1,2,3\), the solutions of \(e+ab=4\) are
\[
\begin{array}{c|c}
e&(a,b)\\ \hline
0&(4,1),(2,2),(1,4)\\
1&(3,1),(1,3)\\
2&(2,1),(1,2)\\
3&(1,1).
\end{array}
\]
For \(b=1,2,3,4\), the positive factorizations \(b=\delta\nu\) are,
respectively,
\[
(1,1),\quad (1,2),(2,1),\quad
(1,3),(3,1),\quad
(1,4),(2,2),(4,1).
\]
Substitution gives the thirteen displayed rank-two rows with no
duplication.  A projective-point image is precisely the rank-one case
already assigned to `Q1`; \(H_4=0\) would make the total degree at most
three and is not a quartic row.

The structural input requiring independent audit is the minimal-pair
factorization and its relative-algebraic-closure clause, not this
elementary integer enumeration.

This document was prepared with AI assistance.  It is not peer reviewed,
and no exclusion or novelty claim follows from the candidate denominator.

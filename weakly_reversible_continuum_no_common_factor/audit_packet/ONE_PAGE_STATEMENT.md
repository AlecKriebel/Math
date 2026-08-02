# Specialist audit statement: reversible equilibrium continua without a common factor

## Problem and answer

**Problem.** Can a finite weakly reversible mass-action system have a genuine
positive-dimensional continuum of positive equilibria in one stoichiometric
compatibility class while the coordinate polynomials of its vector field have
no nonconstant common factor?

**Answer.** Yes. There is a reversible, one-linkage system on three species,
ten complexes, and ten reversible pairs, with positive integer rates and
stoichiometric subspace \(S=\mathbb R^3\). Its sole positive compatibility
class is \(\mathbb R_{>0}^3\), and it contains the compact positive ellipse

\[
L=z-x-y+1=0,
\qquad
Q=7x^2-2xy-16x+7y^2-16y+16=0.
\]

The coordinate gcd is one; the continuum is a height-two component rather
than a common-factor hypersurface.

## Main explicit theorem

Use complexes

\[
0,Z,3Z,Y+Z,3Y,X+Z,X+Y,X+Y+Z,2X+Y,3X
\]

with reversible edges

\[
01,04,06,17,24,27,29,34,59,89.
\]

In the directed order

\[
01,10,04,40,06,60,17,71,24,42,27,72,29,92,34,43,59,95,89,98,
\]

take the primitive positive integer rates

```text
(1160,10296,976,23,560,5977,1800,25,1629,1237,
 1,9152,653,1214,5368,1,5368,70,6039,915).
```

The resulting field is

\[
\begin{aligned}
F_1={}&-4697x^3+6039x^2y-9177xyz-5977xy+10736xz
       +1960z^3+1800z+560,\\
F_2={}&915x^3-6039x^2y-9177xyz-5977xy-3782y^3
       +10736yz+4888z^3+1800z+3488,\\
F_3={}&3712x^3+18304xyz-5368xz+3712y^3-5368yz
       -6848z^3-10296z+1160.
\end{aligned}
\]

Every point of the ellipse is positive, and

\[
(x,y,z)=\left(
\frac{t^2+3}{2(t^2-t+1)},
\frac{3t^2+1}{2(t^2-t+1)},
\frac{t^2+t+1}{t^2-t+1}
\right)
\]

parametrizes it rationally, with infinitely many distinct points already for
\(-1<t<1\). Exact computation gives

\[
F_i\in(L,Q),\qquad \gcd(F_1,F_2,F_3)=1.
\]

The steady ideal is radical. Over \(\mathbb Q\) it is the intersection of the
conic prime with a disjoint degree-15 maximal ideal; over an algebraic closure
the residual component consists of fifteen reduced isolated points.

## Complete fixed-support family theorem

For the same twenty directed reactions, all rate vectors whose three field
coordinates lie in \((L,Q)\) form a four-dimensional rational linear space.
Taking

\[
(a,b,c,d)=(k_{29},k_{43},k_{95},k_{98}),
\]

the remaining sixteen rates are the explicit rational linear forms recorded
in [`family/README.md`](../family/README.md) and certified by the canonical
\(21\times20\) matrix in
[`family/remainder_matrix.csv`](../family/remainder_matrix.csv). The family
is positive exactly when

\[
a,b,c,d>0,\qquad b<c,\qquad 192a+221c<154d.
\]

This positive cone is nonempty and relatively open in its four-dimensional
linear span. A nonempty Zariski-open subset of the family has gcd one even
after scalar extension to \(\mathbb R\) or \(\mathbb C\).
The explicit system above is the specialization
\((a,b,c,d)=(653,1,70,915)\); among positive integral members of this fixed
support and conic-preserving family, it simultaneously minimizes the maximum
rate and the sum of rates. This is not a global network-minimality theorem.

## Data, DOI, and exact replay

The complete two-specialization reaction table is
[`manuscript_v2_draft/rates.csv`](../manuscript_v2_draft/rates.csv), with a
human-readable table in Appendix A of
[`MANUSCRIPT_V2.md`](../manuscript_v2_draft/MANUSCRIPT_V2.md).

- Repository-wide Zenodo concept DOI: **10.5281/zenodo.21753404**. It groups
  unrelated releases from the `AlecKriebel/Math` monorepo and is not a
  paper-specific all-versions DOI.
- Cite this paper using its Version 2 version-specific DOI:
  **10.5281/zenodo.21753997**.
- This packet performs no deposit, publication, or external communication.

From the repository root, replay all Version 2 computational claims with one
command:

```sh
.venv/bin/python weakly_reversible_continuum_no_common_factor/manuscript_v2_draft/verify_v2_claims.py
```

The proof and computation remain open to specialist review; a DOI is a
citable disclosure identifier, not a correctness certificate.

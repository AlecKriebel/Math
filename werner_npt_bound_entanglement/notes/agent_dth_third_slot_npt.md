# The exact DTH pseudomoment violates final-slot PPT

## Result

Let \(\rho_*\) be the exact rational density pseudomoment certified in
`verification/certificates/dth_constrained_pseudomoment.json.gz`.  The
corrected first-level DTH relaxation requires

\[
\rho_*\succeq0,
\qquad
\rho_*^{\Gamma_1}\succeq0,
\]

where \(\Gamma_1\) transposes the first bivector slot.  It does not require
partial-transpose positivity on the final \(z\) replica.

The exact calculation in
`verification/verify_dth_third_slot_npt.py` proves

\[
\boxed{\rho_*^{\Gamma_5}\not\succeq0.}
\]

More precisely, in the local one-contravariant Schur type of highest weight
\((3,0,0)\), of multiplicity four, the global
\((3,0,0)^{\otimes3}\) restriction is a \(64\times64\) rational symmetric
matrix.  All 64 diagonal entries are nonnegative, but the principal minor
on multiplicity indices \((2,8)\) has strictly negative determinant.  Thus
there is no one-dimensional principal obstruction and the displayed
two-dimensional minor is the smallest possible principal-minor separator.

## Why this is the missing Segre condition

Every physical rank-one monomial has the form

\[
|(w\otimes w)\otimes z\rangle
\langle(w\otimes w)\otimes z|.
\]

It is a product density across the cut

\[
(\wedge^2\mathcal H)^{\otimes2}:\mathcal H_z.
\]

Consequently it is PPT under \(\Gamma_5\).  Convex combinations and local-
unitary twirls of physical monomials remain PPT under this cut.  The exact
negative two-by-two minor therefore separates \(\rho_*\) not merely from
rank-one densities, but from the entire convex cone of physical
Veronese--Segre moments.

This identifies a concrete omitted first-degree Segre localizer:

\[
\boxed{\rho^{\Gamma_5}\succeq0.}
\]

The existing obstruction shows that first-bivector PPT, the Pluecker and
Omega range equations, and the mixed support equation do not imply this
additional PPT condition.

## Scope

This exact NPT separator explains why the first corrected relaxation admits
the pseudomoment.  It does not show that the physical DTH inequality is
false.  Adding final-slot PPT is a strictly stronger relaxation; whether
that strengthened cone still contains a negative pseudomoment is a new
finite question.


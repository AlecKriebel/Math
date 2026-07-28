# Failed approaches and obstructions

This file records candidate constructions that fail, including the exact
reason and whether the failure is proved or only observed numerically.

## Imported lead: naive power-harmonic repair

The proposed identity equating powers of a first-harmonic polar unitary with
polar factors of corresponding powers appears to hold generally only for the
original and inverse harmonics. This is not yet accepted as a theorem in this
program; it must be proved symbolically or retained only as numerical
evidence.

## Unmodified standard two-input qudit self-test

The exact ideal tables of the standard Fourier-phase strategy are never
uniform over \(d^2\) pairs.  Their largest cell is

\[
\frac{1}{2d^3\sin^2(\pi/(4d))}>\frac1{d^2}.
\]

Thus its known rigidity theorem cannot by itself yield maximal global
randomness at one of the four existing input pairs.

## Separately bounded third-setting anchor

Perfectly correlating a third Bob measurement with either standard Alice
basis leaves the cross pair nonuniform:

\[
p_{\max}^{\rm cross}
=\frac1{d^3\sin^2(\pi/(2d))}>\frac1{d^2}
\quad(d\ge3).
\]

Allowing arbitrary real coefficients from the two original Alice PVM
algebras does not rescue the natural computational-MUB target by a
coefficientwise spectral bound.  Any operator in that span having a
computational eigenvector has a symmetric corner-block spectrum around the
corresponding eigenvalue, so that eigenvalue is nonextremal unless the
operator is scalar.

This rules out only the separately bounded exposure route, not a joint SOS.

An independent covariant calculation at \(d=3\) reached the same conclusion
in a different gauge.  For the Chu target vector \(q_b=Z^bq_0\), the real
Gram matrix of the map from the four-dimensional traceless Alice-projector
span to \((I-q_bq_b^\dagger)Kq_b\) has determinant \(1/81\).  Hence the only
operator in that span having \(q_b\) as an eigenvector is a scalar.  Finite
checks suggest a parity-dependent degeneracy through \(d=10\), but that
pattern is retained only as numerical evidence because no separate
all-dimensional proof was completed.

## Grouping the \(d^2\) known steering tests

The all-dimensional benchmark uses \(d^2\) Bob steering settings associated
with pairs of rank-one projectors.  A possible compression was to group, for
fixed index difference, the positive or negative eigenvectors of those
projector differences into one PVM.  Direct symbolic overlap calculations
and finite checks show that those eigenvectors are not mutually orthogonal
for \(d\ge3\), so they cannot be grouped into a projective setting by this
naive rule.  This is an obstruction to that ansatz, not a lower bound on the
number of Bob settings.

## Character-by-character binary composition

Decomposing a \(d\)-outcome test into binary games for the nontrivial
characters of \(\mathbb Z_d\) is attractive because each binary game can
certify one Fourier coefficient.  The corresponding optimal qubit planes
are not simultaneously realizable by powers of a single pair of
\(d\)-outcome observables in the tested constructions.  No compatible exact
SOS was found.  This remains a failed construction, not a theorem of
impossibility.

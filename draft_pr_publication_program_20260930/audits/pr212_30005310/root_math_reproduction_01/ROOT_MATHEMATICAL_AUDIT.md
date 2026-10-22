# Root mathematical audit: original and current PR212

This report records mathematical checks, not a priority verdict. The current
claim of prior coverage and its proposed disposition remain unaudited here.
The exact original/current native custody and source-scope gates are separate.
Date: 2026-10-17. Bounded mathematical audit100%; case workflow45%.

## Exact claim and result

The source's literal numerical implications at an adjacent elimination-ideal
transition are false under its displayed general colored-model definitions.
The submitted singleton K4,4 and tied-diagonal variant are admissible. Their
proofs establish I3 nonzero, I4 zero and WMLT2. The singleton's MLT4 is also
verified here by an independent construction, without treating a nonzero
ideal as a statistical lower bound or needing the cited theorem for truth.
These examples satisfy the cone-intersection antecedent. They do not refute
the Boolean SOS-or-intersection alternative and do not settle a four-cycle
restriction. Both submitted proof versions explicitly retain these limits.

## Submitted algebra and weak threshold

I read both full proofs and both distinct checker sources before execution.
Their submersion calculation is valid even though the submitted cyclic V
matrix is singular: U=I4 already guarantees full column rank. Cross variations
are freely set by dV^T=H-DV^T. Fixing the four left diagonal derivatives leaves
four independent symmetric sums on pairs12,23,34,41 to set the four right
diagonals. The checked nonzero24-square Jacobian determinant is256. Composing
with the surjection that sums the first two diagonal statistics gives rank23
with checked minor128. No determinantal primeness or real lifting theorem
is needed for the zero-ideal conclusion: every elimination polynomial
vanishes on the measured Gram image, which contains a real open set.

The cross-block determinant is an original4-minor and a nonzero polynomial
in the sixteen distinct edge statistics. Substituting statistic equations
proves actual elimination-ideal membership. It is not merely a polynomial
vanishing on a numerical sample. Tying diagonals does not affect this minor.

For the rank-two witness, the four left rows are e1 and right rows e2.
Its statistics match I8, including after the first two diagonal colors merge.
Within the proposed entrywise radius1/100 box, diagonal entries are at least
9801/10000 and each of four cross entries is bounded by202/10000. Zeroing
unobserved within-part entries yields a symmetric completion with positive
strict diagonal-dominance margin8993/10000. These bounds hold throughout
the box, giving an open set of PD completions and positive Gaussian
probability. The left/right two-row determinant has positive lower bound
1-2/100, so the data have rank exactly2 there. With one observation the
specified edge3--5 has a singular2-square principal submatrix. Its endpoint
diagonals remain singleton in the tied model. This excludes all rank-one
data, including zero entries, and proves WMLT2 in both models.

The actual rank-two witness is also a rank-at-most-three PSD lift of the
PD identity's statistics. Consequently every polynomial of I3 vanishes
there. This establishes the report's second antecedent directly and
excludes an everywhere nonvanishing signed-SOS ideal element at that same
positive-diagonal Cholesky point. It does not disprove Boolean exhaustion.

## Independently derived singleton MLT4

The pre-artifact ROOT_INDEPENDENT_MECHANISM_FREEZE_01.md gives the complete
continuity argument. The exact finite premises all passed in exact_checks.py.
It uses a different rank-four Jacobian witness with checked minor-256.
The nonzero minor defines a nonzero polynomial in data entries. Away from
its null set, the Jacobian adjoint has no nonzero concentration matrix K
with KX=0. Hence there is no PSD stress and the MLE exists almost surely.

At three samples use tetrahedral Y rows (+,+,+),(+,-,-),(-,+,-),(-,-,+),
each divided by2, and Z rows e1,e2,e3,0. Both have column Gram I3. The
positive weight equality Y^T D_a Y=Z^T D_b Z persists nearby: the six-square
coefficient minor for a1..a4,b1,b2 is-1/16, while b3=b4=1 are fixed. Thus
all weights stay positive and the common G stays PD on a neighborhood.
The block matrix with diagonal blocks D_a,D_b and cross block
-D_a Y G^-1 Z^T D_b is nonzero PSD, belongs to the singleton concentration
space, and annihilates X. PSD follows by normalization to orthonormal-column
U,V and the contraction UV^T. The resulting stress rules out any PD
completion on that whole neighborhood, of positive Gaussian probability.
The base stress has rank5 and all255 principal minors are nonnegative.
An independent nontrivial rational perturbation also has positive weights,
PD G, exact KX=0, rank5, and nonnegative Schur-complement principal minors.
This perturbation exercises the formula; the quantified open-neighborhood
claim follows from the invertible minor and continuity, not finite sampling.

A positive-probability failure set at3 excludes almost-sure existence there.
Adding data columns preserves a PD completion, so smaller almost-sure
thresholds are excluded too. Together with the upper bound4 this proves
MLT4. No MLT value is transferred to the tied-diagonal variant.

The PSD-stress criterion used here follows directly from the closed measured
PSD cone. Its closedness is justified by bounded measured trace; it is not
assumed for arbitrary PSD projections. Its interior equals the PD image.
Separation supplies a nonzero PSD concentration K orthogonal to the data,
equivalently KX=0. Conversely tr(KS)>0 for any nonzero PSD K and PD S,
precluding a matching PD completion. Identity belongs to both model spaces.

## Reproduction and boundaries

Actual independent runs: original author188 checks; current author188;
inherited independent1808. Exact-byte sandbox copies were used because both
submitted programs write beside __file__. Frozen custody files were not
executed in place. The inherited checker hardcodes its historical proof hash;
it is never treated as verification of the revised prose. Root's independently
authored finite certificates also passed. Receipts, full stdout and stderr
are retained in this folder. No Monte Carlo probability assertion is used.

The probabilistic convention is known mean, with n independent full-support
nondegenerate Gaussian columns and covariance proportional to XX^T. Unknown
unrestricted mean would require the effective n=N-1 sample conversion; no
such result is silently asserted. The four original report pages do not
explicitly state the mean convention, so it remains a documented convention
supported by the cited known-mean dependency.

Both new independent mathematical-family reports are now read and accepted,
with no mandatory repair. Root rehashed their8/7 authored selections and
replayed their source-reviewed exact standard-library programs in separate
copies:18 source/logic controls and all PSD certificates passed. The latter
also supplies a robust tied-model MLT4 proof, a strengthening outside the
submitted claims; it is not promoted as novel. Its rank12/13 stress-map minors
are469673776/28036176789375 and7313152/322254905625.

The revised colored-C4 mathematical route is also verified independently:
one vertex color, four singleton edge colors, I1 nonzero, I2 zero and
WMLT=MLT=1. COLORED_C4_DEPENDENCY_NOTE.md gives Root's full direct proof and
source reading; the standalone exact checker passed with Jacobian minor48.
Actual primary PDF pages were visually read and pinned separately. This
does not alter the original K4,4 example's four-cycle limitation or solve
the Boolean alternatives question.

No unresolved mathematical concern remains for these qualified numerical
claims. Priority classification, all publication/PR actions, workflow
completion and the next intake remain gated. This is not either required
future sequential whole-package publication review.

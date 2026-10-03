# Research log: five substantive approaches

## Approach 1: midpoint functional equation and eigenprojection

Used the exact Fourier/Mellin normalization to specialize the functional
equation at s=d/2. This proves equality of the two moments and kills the
negative Fourier eigencomponent in both dimensions. It does not determine
a value. This part was already in Cohn--Miller and the previous attempt.
Outcome: sound reduction, no new numerical evaluation by itself.

## Approach 2: quasimodular distributional summation

Searched for a continuous sampling functional whose value on a Gaussian is
-1/(2 pi^2 tau^2). The transformation anomaly of E2 squared alone has an
unwanted E2/tau term. Adding first-radial-derivative samples with coefficients
of E2 cubed cancels both unwanted terms exactly. Polynomial coefficient growth
makes the functional continuous on radial Schwartz space, and the published
Gaussian density lemma upgrades the Gaussian identity to a theorem.

Inserting Viazovska's positive eigencomponent leaves only the origin and the
first derivative at sqrt(2). Their contributions are 1/12, -7/360, and
1/360, summing to 1/15. Outcome: complete proof of the E8 subproblem.
The exact identity and nine radial Laguerre modes were checked independently;
these tests support but do not replace the proof.

## Approach 3: contour periods and real-axis deformation

Integrated the published positive-eigenfunction Gaussian contours against
the midpoint power. Then changed variables separately on the three finite
contours. Periodicity merges the first two, while the last two combine on
the imaginary axis. This produces two rapidly convergent real integrals
with Im(tau) at least 1/2 and fixes all signs and constants.

The E8 theorem now evaluates its period as 1152 pi i. The Leech real integral
numerically reproduces 0.1778609647296502766456461262418773568..., confirming
the primary-source prefix and the input decimal corruption. Outcome:
independent normalization check and exact Leech period representation;
no closed-form Leech identification. The quadrature is non-interval and is
not called a certified numerical proof.

## Approach 4: modular-weight lift to dimension 24

The Gaussian Fourier factor changes from tau^-4 to tau^-12. Multiplication
of the E8 summation ingredients by the weight-eight modular form E4 squared
restores the covariance calculation. Its inverse Gaussian functional is a
weighted sum of quartic tail integrals, not the midpoint r^11 moment.
The Leech positive eigenfunction has only three nonzero relevant samples,
and their exact evaluation gives 20/91.

Outcome: proved auxiliary identity, with a clearly different kernel. This
cannot be relabeled as the desired Leech Mellin value. Gaussian tests in
dimension 24 and exact rational arithmetic check the normalization.

## Approach 5: direct higher-depth scalar ansatz and its obstruction

Tried E2 to the sixth and seventh powers, the weights corresponding to
value and first-derivative samples in dimension 24. Canceling the initial
anomaly terms leaves four lower-order terms in addition to the desired
sixth power. Explicit polynomial expansion records them.

More generally the formal equation A(X)+A(X+y)-12(B(X+y)-B(X))/y=C y^6
forces A=6B' from the constant coefficient, then B'''=0 from the quadratic
coefficient, then C=0. Thus this specific coefficientwise polynomial
matching mechanism cannot produce a nonzero pure midpoint response.
Outcome: rigorous explanation of why the simplest extension of the successful
E8 mechanism fails; other methods are not excluded.

## Final mathematical disposition

- E8 midpoint value: proved for the normalized radial Schwartz magic function
- Equality of Fourier-paired midpoint values in both dimensions: known theorem
- Leech weighted-tail identity: proved, 20/91
- Leech midpoint identification: unresolved here
- Combined original question: partial progress after five substantive approaches
- Novelty/priority: unasserted; fresh independent audit required before publication

# Attempt 4: general estimation–testing reductions

Let F(P) be a measurable scalar functional in [0,M]. The same model class is used throughout.

## Estimation implies a tolerant test

If sup_P E_P|F_hat-F(P)|<=r, reject F(P)<=nu when F_hat>=nu+delta/2. Markov's inequality shows that both errors in testing

F(P)<=nu versus F(P)>=nu+delta

are at most 2r/delta. Thus delta>=6r suffices for errors at most 1/3, for every nu with a nonempty alternative. Under a uniform squared-error bound v, the analogous error bound is 4v/delta^2.

## A family of tests implies estimation

Take an integer K>=1 and delta=M/K. Assume, for each j=0,...,K-1, a test phi_j is available from the same n observations, with both errors at most alpha for

F(P)<=j delta versus F(P)>=(j+1)delta.

Set F_hat=delta sum_j phi_j. For any fixed F(P), all but at most one grid cell lie entirely below or above it. On those cells the expected indicator error is at most alpha. The remaining cell contributes at most delta, and replacing F(P) by its lower grid endpoint contributes less than delta. Therefore

sup_P E_P|F_hat-F(P)| <= 2delta+M alpha.

Independence between different threshold tests is not required; this follows from the triangle inequality and linearity of expectation.

If only constant-error tests are available, use k independent blocks, each of size n, and majority vote at every threshold. For base error at most 1/3, Hoeffding's inequality gives error at most exp(-k/18) (choose k odd). With k>=18 log(M/delta), k>=1, the risk is at most 3delta using kn observations. Again, the blocks may be reused across thresholds; only within-threshold replication needs independence.

## Why this did not close the problem

The reduction quantifies a general connection but requires a uniform collection of threshold tests. A theorem at nu=0, or a single tolerance value, does not provide that collection. The maximum of threshold difficulties can be very different from the difficulty at a specified null radius. No pointwise-in-nu rate formula, reference-dependent modulus, or matching density lower bound follows from these reductions alone.

Nor is the outer radius epsilon interchangeable with the gap epsilon-nu. For large nu, epsilon itself can be dominated by nu while the statistical estimation error tends to zero. Any claimed transition theorem must state which quantity is compared with an estimation rate. Attempts 1–3 and the final example consistently distinguish these quantities.

These are standard testing/estimation principles, proved here for clarity; no novelty is claimed. The failure to turn threshold reductions into sharp local complexity is a concrete remaining obstruction.

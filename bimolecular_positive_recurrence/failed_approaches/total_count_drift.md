# Failure of total-count one-step drift

For every bimolecular network,

    L |x| = constant/linear birth terms
            - degree-two molecularity-descent terms.

The formula does not imply negative drift near faces.  In the cycle

    0 -> A+B -> B -> 0,

at `(n,0)` the total-count drift is exactly `2*kappa_1>0`.  The subsequent
quadratic/linear restoration is delayed until `B` is produced.  Any proof
based only on the sign of `L|x|` is therefore invalid.

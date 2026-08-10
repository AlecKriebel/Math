# Proof audit

## Certified scope

The project proves the theorem for at most three dynamically active species
and at most two active linkage classes.  Inert singleton components are
removed.  The certified one-linkage and two-active-species theorems are used
only at their stated interfaces.

## Load-bearing interfaces

### 1. Physical Green occupation

All limiting fluxes come from finite-volume occupation of the original CTMC.
The upper workload-boundary flux is retained.  Virtual target marks are used
only for exact potential bookkeeping.

### 2. Terminal chart compactification

A coordinate that cannot be confined in a finite box with vanishing
normalized exit flux is promoted to the active set.  With three coordinates,
promotion terminates.  Bounded coordinate values, target marks, capped
availability, source flags and lattice data form a finite chart phase.

### 3. Interior activation

With three active coordinates every bimolecular source is physically
enabled.  Strict flux follows from the physical source-rate layer and compact
tied-rate ratios, not from a graph-only negative edge.

### 4. Actual-target activation

A linkage-wise terminal episode begins only after an actual channel of that
linkage fires.  A stale formal mark is never treated as physically enabled.
Within a padded finite shell, failure to reach the linkage target episode or
a declared exit would create a closed component in which that linkage never
fires; this reduces to the certified one-linkage theorem.  A finite
Dirichlet solution cancels waiting reward before the negative terminal
episode.

### 5. Atlas exhaustiveness

For two active coordinates, source-weight order changes only at ratios one
and two.  Four rational representatives cover all chambers and walls.  Each
of ten complexes has exactly three assignments: linkage 1, linkage 2, or
unused.  The independent C++ verifier checks the full ordered assignment
universe rather than only canonical representatives.

### 6. Exact workload-cone test

The common affine workload is the rational nullspace of all within-linkage
complex differences, with both active coefficients strictly positive.  The
bounded-coordinate coefficient may be signed.  No floating optimization is
used.

### 7. Deficiency-zero branch

The logarithmic complex-balance system has row rank `s+l`; deficiency zero
makes it surjective.  The product-Poisson measure is summable.  Weakly
reversible lifted return paths ensure that restriction to a closed class is
stationary.

### 8. Service systems

The workload `B-C` is exactly preserved by the mixed linkage.  Actual
strong-connectivity paths raise `C`.  The stopping time is the first net
increase of `C` relative to its trial start, not the first individual upward
reaction, so intervening downward moves cannot invalidate the endpoint
identity.  In a finite shell the killed CTMC has no closed nonabsorbing class
and hence finite mean absorption.

### 9. One-active finite phase

If `2A` is present, all its genuine channels strictly lower `A` at quadratic
rate.  Otherwise every linear channel is nonpositive.  A constant-rate birth
leaves an actual one-`A` target.  A competing linkage cannot consume its
bounded cofactor at linear order without using the same source complex;
consuming `A` is already service, while bounded-source theft is a lower-order
finite phase.  Exact finite Green elimination includes all such
interruptions.  A zero recurrent effective class is edgewise zero and yields
an affine phase invariant; it is not a Lamperti-critical class.

### 10. Shell-dependent duration

No uniform duration bound is asserted.  Every local trial occurs in a finite
killed shell and therefore has finite mean physical duration.  The inherited
shell-adapted Foster construction absorbs the finite Dirichlet corrections,
shell-dependent means and bounded seam overshoots.

### 11. Boundary and lattice classes

All paths consist of actual enabled channels in the selected closed class.
Permanent zeros, parity and other lattice restrictions are never relaxed.
A reaction capable of leaving a face is recorded as chart-exit flux.

### 12. Return and nonexplosion

Exclusion of escaping Green occupation gives finite mean positive return via
the inherited finite trace chain.  Population-increasing reactions have
source molecularity at most one, so their aggregate rate is at most linear;
comparison with a linear pure-birth process proves nonexplosion.

## Computer-assisted claims

The exact atlas and service-support universes are finite and explicitly
proved exhaustive.  Two independent implementations replay the atlas.  The
three-active calibration enumeration is adversarial only; the corresponding
mathematical step is analytic.  No random search or numerical trajectory is
theorem bearing.

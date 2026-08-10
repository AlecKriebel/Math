# Technical summary

## Result

Every finite bimolecular weakly reversible stochastic mass-action network on
at most three dynamically active species and at most two active linkage
classes is positive recurrent on every closed communicating class, for every
positive rate vector.

## Proof mechanism

1. **Terminal Green charts.** Infinite mean return would produce an escaping
   normalized physical Green occupation.  Fixed workload-cut balance retains
   any outward shell flux.  A finite chart records the active coordinates,
   bounded coordinate box, capped availability, target marks, lattice data,
   and a complete source-rate flag.

2. **Three active coordinates.** Every source is enabled.  The inherited
   first-changing-source theorem gives a strict negative physical source
   layer unless the scalar workload is a global invariant.

3. **Finite-shell linkage activation.** A linkage-wise rare terminal is used
   only after an actual channel of that linkage fires.  Within a padded finite
   shell, actual target following reaches the terminal or a structural exit.
   A finite Dirichlet correction cancels the waiting reward, after which the
   certified scalar envelope gives strict negative drift.  If the linkage
   never fires in a closed component, the dynamics reduces to the inherited
   one-linkage theorem.

4. **Two active coordinates.** The third coordinate is retained as a finite
   phase.  Up to active-species exchange there are four workload chambers.
   The direct exact atlas checks every one of the `3^10` complex assignments.
   Every shielded case has a common affine invariant, is deficiency zero, or
   is one of two service systems.

5. **Deficiency zero and service.** Deficiency-zero systems have a
   complex-balanced point for every positive rate vector and therefore a
   summable product-Poisson stationary measure.  In the two remaining systems
   the mixed linkage preserves `B-C`; the other linkage supplies finite-mean
   shell trials that lower `B-C` or promote the bounded coordinate.

6. **One active coordinate.** The bounded coordinates form a finite phase.
   A `2A` source gives direct quadratic descent.  Without `2A`, all linear
   transitions are nonpositive in `A`.  Actual creator-target clocks and
   finite Green elimination pair constant-rate births with linear service;
   zero complete reward is a bounded phase coboundary and hence an affine
   invariant, not a critical nonzero-variance branch.

7. **Return closure.** These alternatives exclude every terminal escaping
   Green occupation.  The inherited finite trace-chain and nonexplosion
   arguments give finite mean positive return and a unique stationary
   probability on each closed class.

## Exact finite certificate

The load-bearing atlas is replayed in two independent forms.

- The direct C++ verifier checks 187,488 nontrivial workload assignments.
  Among 446 shielded assignments, 382 admit a common affine invariant, 60 are
  deficiency zero, and four ordered assignments are the two service
  architectures.  No assignment is unclassified.
- The independent Python verifier reconstructs the reduced 29-class atlas:
  27 deficiency-zero classes and two service classes.

The service-support verifier checks all 1,606 strongly connected directed
supports of the four-complex service linkage and all 18 supports of each
three-complex linkage.

No floating-point search, simulation, or finite stationary truncation is
used as proof.

## Scope

The theorem allows arbitrary positive rate separation, deficiency,
stoichiometric rank, coordinate faces, siphons, signed intermediate
invariants, and lattice restrictions.  It does not cover three active
species with three or more linkage classes or molecularity greater than two.

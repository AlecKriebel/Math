# Result and remaining obstruction

## Disposition

Unsolved, 5/5 substantive approaches. The target is the existence question in Kourovka 21.39, unsolvedmath ID 2548. No complete solution is claimed.

## A precise countable target

Theorem 2.2 proves that if any example exists, a countably infinite example exists with no more automorphism orbits. Consequently one may search among unions of chains of finite groups without losing a positive answer merely through a cardinality restriction. This is an existence reduction, not an effective procedure for constructing the chain.

Such a group must simultaneously have:

1. finite exponent and finitely many element orbits under its full automorphism group;
2. no proper nontrivial characteristic subgroup;
3. no nontrivial finite quotient, equivalently failure of residual finiteness in the characteristically simple setting.

It is necessarily perfect and centerless, has finite commutator width, and every proper subgroup has infinite index. These facts are fully proved in PROOFS.md.

## Three boundary examples

The properties are individually compatible in several strong ways, but these constructions do not combine them all.

- The group of continuous A5-valued functions on Cantor space that take identity at a fixed point is locally finite and characteristically simple and has exactly eight automorphism orbits. Point evaluations separate its elements in finite groups, so it is residually finite.
- The McLain group over F_p on the rational order is locally finite and characteristically simple and has no nontrivial finite quotient. Dense triangular chains realize every p-power order, so it has infinitely many automorphism orbits.
- The countably infinite extraspecial group of exponent p, for odd p, is locally finite, non-residually-finite, and has exactly three automorphism orbits. Its finite residual is its order-p center, which is a proper characteristic subgroup.

The restricted direct sum of A5 is an additional negative control: its finite element-order spectrum is insufficient, because order-two elements supported on m coordinates have centralizer index 15^m.

## What was not bridged

The bounded-exponent perfect locally finite constructions recorded in the Kourovka archive are not automatically characteristically simple and do not automatically have finitely many automorphism orbits. No missing automorphism-extension theorem was supplied. Likewise, bounded-class generic nilpotent groups retain a proper center, and naive class-two amalgamation fails in an explicit finite example.

A p-group candidate, if used, cannot be pseudofinite: finite commutator width, perfectness, and a p-power exponent can be expressed together in a sentence having no nontrivial finite model. This exclusion applies to that construction route only. No assertion that every possible target must be a p-group is needed or made.

## Verification status

The complete authored arguments are in PROOFS.md. Standard-library code exhaustively checks A5 simplicity and the relevant conjugation orbits, small triangular commutator identities, regular-unipotent orders, extraspecial group laws and orbit actions, and two finite amalgamation obstructions. All 116,329 assertions pass, and deterministic re-execution matches CHECK_RESULTS.json byte-for-byte.

This package is an authored mathematical research record, not a formal proof-assistant development or human peer review. An independent reviewer must inspect the infinite constructions and the compactness argument before publication acceptance. The original problem remains open within the limits of this investigation.

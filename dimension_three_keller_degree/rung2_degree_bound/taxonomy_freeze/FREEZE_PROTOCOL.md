# Quartic-taxonomy freeze protocol

**Protocol opened (UTC):** 2026-07-25T19:30:28Z.

**Status:** active gate; the taxonomy is not frozen until the independent
derivation has been reconciled.  No quartic leaf may be promoted while this
gate is open.

This protocol separates three objects that earlier working notes sometimes
blurred:

1. a **leading row**, determined by the homogeneous quartic map \(H_4\);
2. an **incidence leaf**, determined by a declared finite list of invariants
   in the next homogeneous determinant identities; and
3. a **chart**, used only to cover a leaf without dividing away a boundary.

Subdividing a frozen leaf for computation does not change the denominator.
A newly discovered value of a declared invariant, degeneration not assigned
to a frozen leaf, or leading row not in the frozen list is a freeze
violation.

## Stable identifiers

- `Q1` denotes the rank-one leading row.
- `Q2-Ee-Aa-Bb-Ddelta-Nnu` denotes a rank-two curve-image row with
  \[
  e=\deg\gcd(H_{4,1},H_{4,2},H_{4,3}),\quad
  H_4=hA(p,q),\quad \deg(p,q)=a,\quad\deg A=b,
  \]
  and outer image/cover degrees \((\delta,\nu)\).
- A slash and `Lnn` denotes an incidence leaf.
- A slash and `Cnn` denotes a chart inside that leaf.

Identifiers are never reassigned.  A leaf may be marked excluded,
realized, open, or routed, but its identifier and the frozen denominator
remain unchanged.

## Freeze gates

The first release must contain all of the following.

1. A proof that the leading-row list is exhaustive.
2. A finite incidence-leaf manifest for every leading row.  Each manifest
   must name the invariants used to separate leaves and assign every
   degeneration to exactly one leaf.
3. A boundary-chart manifest for every leaf whose proof uses localization,
   normalization, denominator clearing, or a parameter pivot.
4. A second derivation performed without reading the exclusion work.
5. A written reconciliation of the two derivations.
6. A machine-readable denominator and a checksum of the frozen files.

The exclusions themselves are not evidence for completeness.

## Freeze-violation rule

If later work finds an unassigned case:

1. stop all quartic exclusions and construction searches;
2. record the case as a freeze violation, not as a new leaf;
3. invalidate the frozen completeness certificate;
4. repeat the independent derivation and reconciliation; and
5. issue a new version without altering the historical denominator.

Progress reports use only the most recently certified global denominator.

This protocol was prepared with AI assistance and is not peer reviewed.

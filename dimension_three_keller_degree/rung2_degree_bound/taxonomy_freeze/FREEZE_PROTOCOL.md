# Quartic-taxonomy freeze protocol

**Protocol opened (UTC):** 2026-07-25T19:30:28Z.

**Status:** version one frozen after blinded derivation, reconciliation,
hostile replay, corrected re-audit, and mandatory checksum verification.
Any alteration to a hashed artifact requires a new freeze version.

This protocol separates three objects that earlier working notes sometimes
blurred:

1. a **leading row**, determined by the homogeneous quartic map \(H_4\);
2. an **inclusive frozen leaf**, which in version one is exactly one
   canonical leading row and retains every lower-term incidence and
   continuous modulus preserving that row; and
3. a **pivot stratum**, used only as a fixed fail-closed coefficient
   partition so a calculation cannot divide away a boundary.

The attempted 68-bucket incidence refinement was rejected: it was neither
disjoint nor independently complete.  Because several rows have continuous
moduli, no finite orbit taxonomy is asserted.  Subdividing an inclusive
frozen leaf for computation does not change the denominator.  A leading
tuple not in the frozen list is a freeze violation; a new internal
degeneration is not a new global leaf.

## Stable identifiers

- `Q1` denotes the rank-one leading row.
- `Q2-Ee-Aa-Bb-Ddelta-Nnu` denotes a rank-two curve-image row with
  \[
  e=\deg\gcd(H_{4,1},H_{4,2},H_{4,3}),\quad
  H_4=hA(p,q),\quad \deg(p,q)=a,\quad\deg A=b,
  \]
  and outer image/cover degrees \((\delta,\nu)\).
- A slash and `Lnn`, when used in exploratory notes, denotes an internal
  computational subtype and is not part of the frozen denominator.
- A slash and `Cnn` denotes one of the 45 fixed locally closed coefficient
  pivot strata inside a frozen leaf.

Identifiers are never reassigned.  A leaf may be marked excluded,
realized, open, or routed, but its identifier and the frozen denominator
remain unchanged.

## Freeze gates

The first release must contain all of the following.

1. A proof that the leading-row list is exhaustive.
2. A declaration that each leading row is one inclusive leaf, containing
   all lower terms and all internal incidences preserving its canonical
   tuple.  No unproved finite incidence refinement may enter the denominator.
3. A complete fixed boundary-coverage device for every leaf.  Version one
   uses the 45 disjoint locally closed first-nonzero-coefficient pivot strata;
   any other normal-form proof must map back to them or be division-free.
4. A second derivation performed without reading the exclusion work.
5. A written reconciliation of the two derivations.
6. A machine-readable denominator and mandatory exact checksums of every
   frozen proof, audit, protocol, manifest, and verifier file.

The exclusions themselves are not evidence for completeness.

## Freeze-violation rule

If later work finds an unassigned case:

1. stop all quartic exclusions and construction searches;
2. record the case as a freeze violation, not as a new leaf;
3. invalidate the frozen completeness certificate;
4. repeat the independent derivation and reconciliation; and
5. issue a new version without altering the historical denominator.

Progress reports use only the most recently certified global denominator.

The version-one denominator is therefore intended to be
\[
14\text{ canonical inclusive leading leaves},
\]
not the rejected 68 exploratory buckets and not an orbit classification.

This protocol was prepared with AI assistance and is not peer reviewed.

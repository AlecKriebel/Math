# Freeze certificate: `Q2-E2` marked-companion taxonomy v1

**Certified (UTC):** 2026-07-25T23:28:00Z.

## Verdict

The immutable candidate
`FROZEN_Q2_E2_MARKED_COMPANION_v1.md` at SHA-256

```text
27e5a4f894ef523156abea389f89c2d4481d58d243c756b70386fdea10e9e01f
```

is **frozen as version one**.

It has three marked-pair types and thirteen stable internal strata:
\[
\boxed{4+5+4=13}.
\]
The middle `CTAU` stratum carries the actual parameter
\(\tau\in\mathbb C\setminus\{0,-1\}\); it contains infinitely many
inequivalent orbits.  The nonzero orbit-space shorthand is
\[
\boxed{3+\mathbb P^1(\mathbb C)+3}.
\]

This certificate freezes an internal parameterized taxonomy only.  It does
not exclude or promote the parent row `Q2-E2-A2-B1-D1-N1`, whose status
remains provisional.

## Independent evidence

1. A blinded clean-room reconstruction derived the same three marked-pair
   types, residual actions, projective modulus, and stable identifiers
   without reading the candidate slice package or the earlier readiness
   report.
2. A second hostile derivation sealed its source/target/translation action
   analysis before reading either candidate package.
3. The second audit then verified all thirteen stable strata and the
   coordinate conversion
   \[
   \theta=\frac1{1+\tau}.
   \]
   It checked the boundary correspondence
   `CH` \(\leftrightarrow\theta=1\),
   `CT` \(\leftrightarrow\theta=\infty\), and
   `CS` \(\leftrightarrow\theta=0\).
4. The dependency-free hostile wrapper rejected missing-stratum,
   wrong-coordinate, overlapping-boundary, and merged-modulus mutations.

The strict hostile run ends with:

```text
MARKED_ORBIT_HOSTILE_2_PASS_C4B821
MARKED_ORBIT_HOSTILE_2_STRICT_PASS_91A73E
```

## Frozen hashes

```text
27e5a4f894ef523156abea389f89c2d4481d58d243c756b70386fdea10e9e01f  FROZEN_Q2_E2_MARKED_COMPANION_v1.md
f5323cd2cc6e2133b7eae29b3d77d1f3dd820dac5b84332c6c71281ff536129a  audit_marked_orbit_reconstruction/REPORT.md
f800d30ab9ee2d594c36a62cf1750d101df43c5aebf205dfed47e44110cdb7b6  audit_marked_orbit_reconstruction/verify_marked_orbits_exact.py
b14987bbc1f804b787ef955986e56f7093b86a9a8f6f987762f3743d8aa72bef  marked_h_distinct/FREEZE_READINESS_COMPARISON.md
4024db40728b7ba90efb0bba8029e11a51310d2b8b9f47b113d16f820d3c1efd  audit_marked_orbit_hostile_2/REPORT.md
98bdf7296171b3c466742bd55caed612618d9fa4dbfec565cb4228b6a88aa76d  audit_marked_orbit_hostile_2/verify_marked_orbit_hostile_2.py
593c7d574b9d035e094bf9dbca9390a0bd0faed4c917fdf4c9407f8d1b1b4616  audit_marked_orbit_hostile_2/verify_strict.sh
bf62d6a11319f9d4214ede241c26f291b6651872f095cd57724f1964ed49e5d6  audit_marked_orbit_hostile_2/RESEARCH_LOG.md
```

Any change to the frozen taxonomy file requires version two and a fresh
hostile reconstruction.  Later lower-identity pivot divisors must be
handled division-free or recorded as an explicit versioned refinement; they
must not be silently absorbed into the denominator.

This certificate was produced with substantial AI assistance.  It is not
peer review.  Exact checks are evidence about the encoded orbit
classification and guards, not a verification by the mathematical
community.

# Provisional umbrella: exclusion of every exact-\(\delta=2\)
\(\{2,0\}\) Hilbert--Burch point

**Status:** all three pieces have exact dual-CAS certificates; hostile
mathematical replay is pending.  Do not promote this umbrella before
that audit.

**First recorded release (UTC):** 2026-07-25T12:32:17Z.

## Statement

In the binary fixed-quadratic line-double-cover row
\[
H_4=h(p,q)(p^2,q^2,0),
\]
no Keller counterexample with exact
\[
\delta=\deg\gcd(J(Q,R),-J(P,R),J(P,Q))=2
\]
has Hilbert--Burch shape
\[
\{k_1,k_2\}=\{2,0\}.
\]

## Exhaustiveness

`DELTA2_HB_STRATIFICATION.md` proves that every exact-\(\delta=2\)
\(\{2,0\}\) point is, up to the complete stabilizer and swap, in exactly
one of:

1. two ramification contacts at \(\kappa=16\);
2. one fixed root plus one ramification contact at \(\kappa=16/3\);
3. the exceptional coefficient locus on the doubled-root orbit
   \(\kappa=4\).

The three corresponding lower exclusions are:

- `DELTA2_KAPPA16_EXCLUSION.md`;
- `DELTA2_KAPPA16OVER3_EXCLUSION.md`;
- `DELTA2_KAPPA4_EXCLUSION.md`.

Each begins from the complete integrated \(E_7\) family and retains all
lower coefficients.  Each kills the genuine \(r^1\) tangent at \(E_6\).
The surviving branches then end in one of three certified ways:

- a zero column of the linear part;
- the unconditional degree-four plane-field/birational automorphism
  exit; or
- a nonzero \(E_4\) coefficient.

Thus, subject to hostile replay, every exact-\(\delta=2\) counterexample
in this binary row must have the remaining shape
\[
\boxed{\{k_1,k_2\}=\{1,1\}}.
\]

This umbrella does not exclude exact \(\delta=2\) itself, and it makes no
claim about \(\delta\ge3\) or the constant-dependent power fibre.

This work was developed with AI assistance.  It is not peer reviewed;
the exact certificates verify encoded algebra, not peer review.

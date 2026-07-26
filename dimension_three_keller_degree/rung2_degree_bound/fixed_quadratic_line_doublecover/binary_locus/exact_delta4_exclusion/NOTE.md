# Exclusion of the exact-\(\delta=4\) fixed-quadratic stratum

**First assembled (UTC):** 2026-07-26T06:45:00Z

**First certified release (UTC):** 2026-07-26T07:25:07Z

**Status:** certified exact-computation structural theorem; hostile assembly
audit passed; not peer reviewed.

> This is AI-assisted, exact-computation research. It is not peer reviewed.
> Exact checks are evidence about the encoded algebra, not peer review.

## Theorem

Work over \(\mathbb C\). In the frozen binary fixed-quadratic
line-double-cover row, write
\[
H_4=(P,Q,0),\qquad P=h(p,q)p^2,\qquad Q=h(p,q)q^2,
\]
and let \(R=(H_3)_3\). Put
\[
\alpha=J(Q,R),\qquad \beta=-J(P,R),\qquad
\gamma=J(P,Q),\qquad
\delta=\deg\gcd(\alpha,\beta,\gamma).
\]
There is no quartic Keller counterexample in the exact-\(\delta=4\)
stratum.

This is a theorem about one leading-shape stratum. It does not exclude the
other frozen families in the parent row, does not close any one of the
fourteen global quartic rows, and does not improve the universal
dimension-three total-degree floor of four.

## Exhaustive six-family bridge

The independently reconciled high-incidence denominator proves that the
exact-\(\delta=4\) stratum is the disjoint union, up to the frozen cover
stabilizer, of precisely these six normal-form families:

| Canonical reconciled ID | Normal form or modulus | Certificate |
|---|---|---|
| `D4-SF-21C` | squarefree, \(\kappa=-16/5\) | `D4-SF-21C` |
| `D4-SF-20CC` | squarefree, \(\kappa=16/5\) | `D4-SF-20CC` |
| `D4-SF-11CC` | squarefree, \(\kappa=16\) | `D4-SF-11CC` |
| `D4-DN-3` | \(h=L^2,\ R=L^3\) | `D4-DN-3` |
| `D4-DN-2C` | \(h=L^2,\ R=L^2(p-2q)\) | `D4-DN-2C` |
| `D4-DN-1CC` | \(h=L^2,\ R=L(2p^2+pq+2q^2)\) | `D4-DN-1CC` |

The first column is the canonical nomenclature in the blinded
\(19+6+1\) denominator. The certificate names now agree literally with
those IDs. `FAMILIES.json` binds each ID to one proof directory and one
distinct terminal marker; `verify_manifest.py` compares the six bindings
with the canonical denominator. A required-failure test deletes one entry
and must be rejected.

## Proof

The Hilbert--Burch argument and finite incidence enumeration in
`../delta_ge3_universal/NOTE.md` first produce the six exact-\(\delta=4\)
orbits. The blinded audit and reconciliation in
`../../audit_delta_ge3_denominator/` and
`../../delta_ge3_reconciliation/` independently recover the canonical
\(19+6+1\) denominator, the same six exact-\(\delta=4\) orbits, and their
boundary routing. Every independent exact-\(\delta=4\) point therefore lies
in one and only one of the six displayed orbits.

For each of the six rows, the corresponding family certificate starts
from a complete top-contact parameterization, retains arbitrary lower
coefficients, and proves that every contact chart either contradicts a
lower homogeneous Jacobian identity, forces the linear part to be
singular, or exits to an unconditional bounded-degree plane
automorphism. Each family wrapper has exact symbolic and independently
implemented checks, together with required-failure mutations. Therefore
none of the six exhaustive normal forms can be the leading data of a
quartic Keller counterexample.

## Exact verification

Run:

```sh
./verify_strict.sh
```

The aggregate wrapper:

1. checks the six-entry bridge against the frozen denominator;
2. requires a deleted-family mutation and optimized-Python run to fail;
3. reruns the independent denominator reconciliation; and
4. reruns all six fail-closed family certificates and requires their
   distinct terminal markers.

The aggregate terminal marker is:

```text
EXACT_DELTA4_SIX_FAMILY_EXCLUSION_STRICT_PASS
```

The independent hostile assembly wrapper in `audit_hostile/` reruns the
aggregate, checks that the containing global row remains open, and rejects
mutations of every canonical bridge field. Its terminal marker is:

```text
EXACT_DELTA4_HOSTILE_UMBRELLA_AUDIT_STRICT_PASS
```

The family-level proof directories remain the source of the detailed
identities. This umbrella note adds only the exhaustive classification
bridge and the six-family structural statement.

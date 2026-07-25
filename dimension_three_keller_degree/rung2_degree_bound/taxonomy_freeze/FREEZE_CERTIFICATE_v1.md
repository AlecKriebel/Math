# Quartic taxonomy freeze certificate, version 1

**Certified (UTC):** 2026-07-25T20:24:52Z.

## Verdict

\[
\boxed{\text{F1/F2 PASS: 14 canonical inclusive leading leaves are frozen.}}
\]

Every normalized exact-degree-four Keller map
\[
F=X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}
\]
has \(H_4\ne0\) in exactly one of the fourteen leaves recorded in
`FROZEN_TAXONOMY_v1.md`: one rank-one leaf and thirteen rank-two leaves
indexed by the canonical relative-closure tuple
\((e,a,b,\delta,\nu)\).  Every leaf retains all lower terms, continuous
moduli, and internal degenerations preserving that tuple.

The fixed boundary-coverage device is a disjoint partition into 45 locally
closed first-nonzero-coefficient pivot strata per leaf.  Counting empty
intersections gives 630 stable row/pivot IDs.  These are not asserted to be
Zariski-open charts or equivalence orbits.

## Independence record

The independent derivation in
`blind_independent/BLIND_TAXONOMY.md` was produced without reading any
quartic exclusion proof.  It recovered the same one-plus-thirteen leading
enumeration.  `RECONCILIATION.md` rejected the historical 68-bucket proposal
because it was not disjoint or independently complete, while certifying the
14-row relative-closure denominator.

`HOSTILE_FREEZE_AUDIT_v1.md` independently replayed the mathematics and
found repairable release-certificate defects but no missing leaf.
`HOSTILE_FREEZE_REAUDIT_v1.md` then passed the corrected normalization,
rank-one cone argument, relative-closure rationality, polynomial
factorization, canonicity, row enumeration, pivot partition, routing,
manifest synchronization, and fail-closed checksum logic.

Neither hostile audit inspected any exclusion proof.

## Machine certificate

`FROZEN_SHA256_v1.txt` records mandatory SHA-256 hashes for the taxonomy,
manifest, verifier, protocol, blind derivation, reconciliation, and both
hostile audits.  The fail-closed command

```sh
/usr/bin/python3 verify_frozen_manifest_v1.py
```

returned:

```text
PASS: frozen manifest schema, Markdown synchronization, finite arithmetic, and required checksums
```

The verifier checks the exact 14-row schema, stable ID-to-tuple encoding,
complete 13-tuple arithmetic, exact quartic monomial order, 45 pivot IDs,
630 declared intersections, Markdown/JSON row synchronization, status
strings, path safety, exact checksum filename set, and every digest.  It
does not prove the geometric arguments; those were replayed separately.

## Progress denominator and limitations

All future quartic progress is reported against exactly
\[
\boxed{14\text{ inclusive leaves}.}
\]
The manifest currently records seven leaves as `excluded-audited` and seven
as `open`, but this certificate does not audit or certify those exclusions.
Before using \(7/14\) as certified mathematical progress, each exclusion
must retain its own independent proof audit and its normal forms must map
back to the frozen pivot partition or use a division-free argument.

This freeze does not prove that any leaf contains a non-linear Keller map,
does not classify moduli or source/target orbits, does not improve the
universal total-degree floor of \(4\), and is not a novelty claim.

Any later leading tuple outside the frozen list is a freeze violation:
quartic work stops, this certificate is invalidated, and a new blinded
derivation and versioned freeze are required.  Internal computational
subtypes never enlarge the denominator.

## Disclosure

The taxonomy, scripts, and audits were produced with substantial AI
assistance under human direction.  No person was contacted.  This is not
peer review, and exact checks are evidence about the encoded finite data,
not verification of the universal geometric proof.

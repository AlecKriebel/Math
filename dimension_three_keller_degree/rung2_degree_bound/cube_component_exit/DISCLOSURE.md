# Disclosure

Draft freeze (UTC): `2026-07-26T07:53:50Z`.

First public release (UTC): `2026-07-26T08:13:13Z`.

## Provenance

This is an independent research draft extracted from a clean-room audit
of one normalized Keller family.  The general cube-component lemma was
recognized during that audit and then rewritten here without relying on
the candidate proof under review.

The derivation and documentation were AI-assisted.  Every algebraic
normal form used in the proof is reproduced in a dependency-free exact
verifier, and an independent hostile agent separately reconstructed the
rank \(2/1/0\) proof and found no missing pivot.  Its report and log are
preserved in `audit_hostile/AUDIT.md` and
`audit_hostile/RESEARCH_LOG.md`.  A second independent audit of the
hypotheses, fibrewise implication, and adjacent literature is preserved
in `audit_geometry/`.  The primary `verify_strict.sh` remains
the main verifier; `verify_all_strict.sh` requires both its
`CUBE_COMPONENT_EXIT_STRICT_PASS` marker and the hostile suite's
`CUBE_COMPONENT_HOSTILE_AUDIT_PASS` marker before printing the unique
aggregate marker `CUBE_COMPONENT_ALL_STRICT_PASS`.

No person was contacted, messaged, emailed, or otherwise approached
during this work.

## External mathematical inputs

The coordinate lemma itself is proved in full in this artifact.
The complex Keller corollary uses:

1. the plane low-degree result reported by
   Guccione--Guccione--Horruitiner--Valqui,
   [arXiv:2204.14178](https://arxiv.org/abs/2204.14178), whose abstract
   raises the possible-counterexample floor to \(108\);
2. the Ax--Grothendieck theorem.

The \(d\le35\) statement depends on accepting the first result.  The
audit verified the primary preprint and its exact numerical claim but
did not locate a peer-reviewed journal publication.  A conservative
\(d\le33\) version follows instead from Moh's established plane range
\(<100\).

The Keller hypothesis in the paper is not restricted to a literal
component: it is enough that some nonzero target-linear combination
\(\alpha\!\cdot\!F\) has cube leading form.  Extending \(\alpha\) to a
target \(\mathrm{GL}_3\)-change preserves the Keller property up to a
nonzero constant factor and makes its nowhere-zero gradient an actual
Jacobian row.

## Scope limitations

This artifact does not claim:

* that every three-dimensional Keller map is invertible;
* a global degree bound;
* an entire quartic denominator row;
* the generic `D3-SF-20C` family;
* the reciprocal \(z=1/3\) sheet;
* any frozen denominator entry not explicitly listed in `BRIDGE.json`.

The machine bridge reads the frozen denominator, checks its SHA-256 and
26-family count, and rejects a mutation that promotes `D3-SF-20C` from
one pivot to a whole-family claim.

## Novelty

Worldwide novelty is unresolved.  Search results found related
classification and variable-polynomial literature, but no source was
found stating this exact elementary lemma with cube leading form and a
degree-three coordinate inverse.  Failure to locate a source is not
evidence of priority.

No publication or priority claim should be made before a specialist
literature review.

This draft is not peer reviewed.  Exact checks are evidence about the
encoded algebra and frozen scope; they are not peer review.

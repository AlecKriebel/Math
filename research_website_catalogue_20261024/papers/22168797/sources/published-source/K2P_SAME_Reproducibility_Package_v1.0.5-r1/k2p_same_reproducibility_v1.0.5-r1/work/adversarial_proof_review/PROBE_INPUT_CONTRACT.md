# Corrected physical probe input contract

> **Historical checkpoint -- not current theorem authority.**  This document
> records the input-universe milestone before the one-/two-port probe closure
> was completed.  Its statements that probe closure or the global theorem was
> still blocked describe that earlier checkpoint only.  Current authority is
> `work/probe_coherence_corrected/probe_coherence_certificate.json`, its
> independent replays, and
> `work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md`,
> as bound by `work/final_theorem_release/RELEASE_LOCK.json`.

## Verdict and claim boundary

**PASS for the input universe; not yet a PASS for probe closure.**  The
machine-readable contract independently binds every currently closed physical
equality-anchor record to all physical one-port attachment sites on both sides.
It does not assert that the resulting one- and two-port probe children have all
been classified.  The global theorem therefore remains blocked until the
separate corrected probe computation returns zero unresolved records and
coherent parent restriction on every surviving equality edge.

The authoritative artifact is `probe_input_contract.json`.  Its independent
replay is `verify_probe_input_contract.py`; the fast fail-closed structural
replay and mutations are `verify_probe_input_structure.py` and
`test_probe_input_mutations.py`.  Routine mutation runs require a disposable
caller-owned report, for example
`.venv/bin/python -B work/adversarial_proof_review/test_probe_input_mutations.py
--output /tmp/k2p-probe-input-mutations.json`; the canonical report may be
replaced only with the explicit maintainer override.

## Equality-anchor census

The contract contains 176 uniquely identified physical equality-anchor
records:

| Origin | Ports | Records |
|---|---:|---:|
| four-port direct terminals | 4 | 26 |
| physical completions of omitted four-port terminals | 5 | 17 |
| theta2 direct anchors | 5 | 24 |
| theta2 one-role restorations | 6 | 40 |
| theta2 two-role restoration paths | 7 | 32 |
| cycle direct anchors | 3 | 24 |
| cycle fully restored anchors | 4 | 12 |
| three-port tree identity | 3 | 1 |
| **Total** |  | **176** |

There are 143 labelled isomorphism records and 33 ordinary-triangle records.
The theta2 seven-port layer has 32 distinct restoration-path records but 16
upstream topology-anchor IDs; the contract gives every path record a unique
record ID and preserves the upstream ID as provenance.  Thus the earlier
duplicate-ID ambiguity is removed without discarding a restoration path.

The omitted four-port terminal recursion was regenerated from the raw ledger,
not copied from the revoked probe package.  Starting from 55 terminal classes
and 80 raw members, it tests 564 exact children: 543 are exact-topology `none`,
four equality children retain a further omitted role, and 17 terminate as
physical equality anchors.  The four newly recovered ordinary-triangle
anchors are:

| Raw ID | Canonical class | Target | Permutation | Restored source site |
|---:|---:|---:|---:|---|
| 67161 | 439 | 2798 | 9 | insertion `i3`, segment 2 |
| 67167 | 441 | 2798 | 15 | insertion `i4`, segment 3 |
| 67401 | 499 | 2808 | 9 | insertion `i5`, segment 2 |
| 67407 | 501 | 2808 | 15 | insertion `i6`, segment 3 |

Each raw row is a `retained_terminal` with status `triangle` and a null
`restoration_obligation_id`.  Consequently these four rows lie outside the
997 restoration-parent classes, 2,540 physical member roots, and 36,568
first-child edges in corrected restoration forest v3.  They repair the
omitted-terminal probe input and do not contradict that forest.

## Physical edge-site lemma

Let a binary rooted representative have (k) labelled boundary leaves and
(r) reticulations.  If (t) is its number of non-root tree vertices, equality
of indegree and outdegree sums gives

\[
  2+2t+r=t+2r+k,
  \qquad t=k+r-2.
\]

The rooted representative therefore has

\[
  2+2t+r=2k+3r-2
\]

arcs.  Suppressing the artificial degree-two root merges its two outgoing
arcs into one semi-directed mixed edge, leaving exactly

\[
  2k+3r-3
\]

physical attachment sites.  Every such edge is present in the contract.
They partition as follows:

* one root-suppressed incoming-boundary segment;
* (k-1) other pendant arms;
* (2r) reticulation-incoming edges, one for each reticulation parent
  incidence; and
* (k+r-3) remaining unheaded core edges.

This includes the edge classes omitted by the revoked
`internal_candidates` grammar: pendant arms, both incoming edges at every
reticulation, and the segment on which the artificial root was inserted.

For the last class, the two rooted arcs leaving the artificial root are not
two physical sites.  Subdividing either half by a new labelled leaf and then
suppressing the artificial root produces the same labelled semi-directed
subdivision of the underlying mixed edge.  The contract verifies this exact
semi-directed isomorphism separately on the source and target graph of all
176 anchor records, for 352 exact root-half checks.  This supplies the needed
root-movement quotient without assuming that root-tail arcs can simply be
dropped.

Across the 176 records there are 2,206 source sites and 2,206 target sites.
The first-probe universe is the per-anchor Cartesian product, not merely the
matched sites under the parent map; it contains 29,964 source-site/target-site
pairs.  The stored parent transport is a separate coherence datum.  It is the
unique exact labelled incidence transport for the isomorphism or ordinary
triangle parent and maps every source mixed edge bijectively to a target mixed
edge.  A child equality transport must restrict to this fixed parent
transport after forgetting the new label.

An omitted physical leaf in a full network is attached by subdividing exactly
one physical semi-directed edge and adding its pendant arm.  The edge-site
enumeration and root-half quotient therefore place its source and target
attachments in the stated Cartesian product.  No separate bounded
root-adjacent, pendant-arm, or reticulation-incoming case remains outside the
probe universe.

## Required downstream classifier

Every one- and two-port child must be processed in this order:

1. exact labelled isomorphism or ordinary-triangle relation;
2. strict displayed-quartet separator;
3. direct full-map (T_i) search over every retained triple and all three
   orientations, with no rooted `triple_type` gate; and
4. a certified bridge-multihomogeneous algebraic separator, or an explicit
   unresolved result.

The old rooted-restriction type is finder metadata only and may never be used
as a proof.  In particular, the corrected computation must not reintroduce
the `raw4424` false tree/sunlet classification.  It must also retain all 176
anchor records, all 29,964 first-probe pairs, and exact restriction of every
surviving child transport to its parent transport.

## Falsification targets

The mutation harness rejects omitted or duplicated anchor records, restoration
of the old 172-record census, reassignment of raw 67161, omission of a pendant,
reticulation-incoming, or root-suppressed site, splitting the artificial-root
halves, a false root-half relation, a wrong site transport, a wrong edge-count
formula, rooted/topology-first or `triple_type` classifier reintroduction,
ordered-row omission, upstream binding corruption, and the named `raw4424`
regression.  It first requires clean structural and full production replays,
then requires return code one, the exact case-specific semantic diagnostic,
and no success artifact for each attack.  Optimized Python is itself rejected
explicitly; it is not treated as a positive qualification mode.

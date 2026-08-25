# Adversarial audit of coherent-probe closure

> **Historical checkpoint -- not current theorem authority.**  The blocked
> status and input-only authority below record the interval after the first
> probe oracle was revoked but before the corrected one-/two-port package was
> completed.  Current authority is
> `work/probe_coherence_corrected/probe_coherence_certificate.json`, the
> independent replay under `work/global_proof_adversary/probe_full_audit`, and
> `work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md`,
> as bound by `work/final_theorem_release/RELEASE_LOCK.json`.

## Current verdict

**Probe input universe: PASS.**

**Full one-/two-port probe classification: BLOCKED pending the corrected
all-primitive computation.**

The former 172-anchor certificate under `work/probe_coherence_closure` is
revoked and must not be consumed. Its rooted internal-arc grammar omitted
physical edge sites, and its topology-first classifier missed four exact
ordinary-triangle anchors. No census or terminal conclusion from that package
is theorem input.

## Corrected frozen input

The authoritative input is `probe_input_contract.json`, schema
`k2p-root-invariant-probe-input-contract-v2`. It contains:

* 176 uniquely identified physical equality-anchor path records;
* 143 labelled isomorphisms and 33 ordinary-triangle relations;
* 2,206 physical source sites and 2,206 physical target sites;
* 29,964 per-anchor Cartesian source/target first-probe pairs;
* all pendant arms, all reticulation-incoming edges, and one
  root-suppressed mixed segment per graph; and
* a unique exact parent transport and a bijection of physical edge sites for
  every anchor record.

The origin census is 26 four-port direct, 17 four-port restored, 24 theta2
five-port, 40 theta2 six-port, 32 theta2 seven-port paths, 24 cycle three-port,
12 cycle restored four-port, and one ordinary three-port tree record. The
theta2 seven-port layer has 32 path records but 16 upstream topology IDs; v2
uses the path ID in the record ID, preventing accidental collapse.

The four exact ordinary-triangle repairs have raw IDs 67161, 67167, 67401,
and 67407. They are omitted-role expansions of retained four-port triangle
terminals. They are not restoration-parent rows and therefore do not
contradict corrected restoration forest v3.

## Root-invariant physical-site theorem

A binary rooted representative with (k) boundary labels and (r)
reticulations has (2k+3r-2) rooted arcs. Suppressing its artificial root
merges two arcs, so it has exactly (2k+3r-3) semi-directed mixed edge sites.
The contract enumerates all of them. The two root-outgoing arcs represent one
site: insertion on either half followed by root suppression is exactly
semi-directed-isomorphic. This was replayed on both graphs of every anchor,
for 352 exact checks.

The parent transport is coherence data, not a restriction of the candidate
universe to matched edges. The corrected first-probe universe is the full
Cartesian product at each anchor. A child equality transport is acceptable
only when it restricts to the fixed parent transport after forgetting the new
label.

## Independent replay

`verify_probe_input_contract.py` does not import the builder. It reconstructs
all graphs from raw upstream locators, independently reruns the 55-class,
80-member omitted-terminal recursion, recomputes every exact relation and
incidence transport, re-enumerates all mixed edges, and verifies every
root-half quotient and site transport.

Its report `probe_input_independent_verification.json` is PASS with payload

```
96d14bae9b20646abfe64b85a7ac0f61377182f75479031f621ea0dbe2096fce
```

and zero missing, extra, unresolved, or incoherent records.

`test_probe_input_mutations.py` rejects 20/20 adversarial corruptions with
zero survivors and passes the original contract under optimized Python. Its
payload is

```
bc49b296948537cf172c9e4c6b7f5f676cd2ddd4a9c1b455304d6b0cdccf835d
```

The mutations include omission of the four repaired triangle paths,
collapse of theta2 k7 paths sharing an upstream topology ID, omission of
pendant/reticulation/root sites, root-half splitting, wrong parent or site
transport, rooted/topology-first and `triple_type` reintroduction, the named
raw4424 regression, ordered-row omission, and upstream binding corruption.

## Conditions for promotion

The corrected full probe output must consume v2 and classify all 29,964
first-probe pairs. For each surviving equality record it must then enumerate
the complete second-probe Cartesian product, retain exact parent restriction,
and terminate with zero unresolved or incoherent records. Classification
order is exact labelled iso/ordinary triangle first, strict quartet second,
full-map (T_i) over all triples and orientations third, and a certified
bridge-multihomogeneous algebraic fallback otherwise. Rooted restriction
types and `triple_type` gates are forbidden as proof.

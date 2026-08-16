# Rejected Outcome Q — immutable historical record

**Disposition:** rejected; no file in this directory supports the active
paper.

Outcome Q defined `Root_clean(N)` as the unrestricted fibre of rooted
networks that collapse to a mixed graph `N` after iterative degree-two and
parallel-edge cleanup. Nested hidden zipper refinements then give a
non-tree-child rooted preimage of even an ordinary tree. Consequently the
proposed universal class `S_TC(clean)` is empty under its printed definition.
That is not the admissible-rooting class of the baseline paper.

The one-step zipper JC tensor identity in the rejected package remains an
algebraically valid identity. It does **not** identify the admissible-rooting
universe of the active theorem and is not used by the manuscript,
dependency graph, metadata, or active verifiers.

## Exact counterexample

The rooted network has arcs

```text
r -> P,  r -> Q,  P -> Q,  P -> p,  Q -> q,
p -> q,  p -> L1, q -> t,  t -> L2, t -> L3.
```

It is:

- binary: `r` has bidegree `(0,2)`; `P,p,t` have `(1,2)`;
  `Q,q` have `(2,1)`; and the labelled leaves have `(1,0)`;
- acyclic, as witnessed by the order `r,P,Q,p,q,t,L1,L2,L3` after
  reordering incomparable vertices;
- LSA-valid: only `r` lies on every root-to-leaf path;
- level two: its only nontrivial top block has precisely the two
  reticulations `Q,q`;
- not tree-child, because reticulation `Q` has reticulation child `q`;
- cleaned to the ordinary three-leaf tree: suppressing the root exposes a
  duplicate `P-Q` edge; identifying and suppressing it exposes a duplicate
  `p-q` edge; identifying and suppressing that leaves the star at `t`.

The independent exact checker is
`adversarial_audit/independent/double_zipper_counterexample.py`.

## Provenance

- Original archive: `original_package/STC_JC_Convention_Closure_Outcome_Q_Final.zip`
- Original archive SHA-256:
  `abb83eff03996b7b95520ace2491c233daa4a9634ef1a771d51dc703dbf97f14`
- Rejected-audit commit:
  `838f958543cbcb1bf76b076931b39e1ad43a50e5`
- Rejected-audit branch: `codex/stc-jc-outcome-q-audit`
- Adversarial report SHA-256:
  `805597945ae5ba29b3e610c36d41189d55119338397a23b832bf1cf21f49127b`
- Independent checker SHA-256:
  `167d68c29c64bae67fcfcdfa31c4c5fa2f7b5e9853510538ab0e2740c9939dd1`

The original package, cloud-imported source, manuscripts, zipper scripts,
certificates, metadata, transcripts, exact Git bundle, local adversarial
review, and double-zipper checker are preserved below. They are historical
inputs only.

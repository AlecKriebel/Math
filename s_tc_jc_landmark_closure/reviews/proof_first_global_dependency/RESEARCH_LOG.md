# Research log

## 2026-08-12 — proof-first global dependency audit

- Read the candidate global proof and the independently reviewed convention,
  primitive-core, cut, incidence-quotient, localization, root-reduction,
  arbitrary-subdivision, and ordinary-triangle documents.
- Ran no topology census or local-algebra search.
- Reduced Outcome P to one full-factor local blob-containment lemma
  `L_blob`, with source and target incoming presentations chosen
  independently.
- Found one omitted synthesis step: cut splits recover an unmarked component
  tree and do not by themselves distinguish an ordinary median from a
  three-port blob.  A full three-port blob is necessarily a three-sunlet, and
  the already verified arm-homogeneous invariant `F=abc-t^2` repairs the
  omission in both containment directions.
- Rejected use of `G=a-bc` for this marker: although valid in the fixed-gauge
  two-active cut proof, it is not invariant under arbitrary port-incidence
  scaling.
- Clarified the `K4-e` proof wording.  In the suppressed mixed graph the root
  is correctly absent and the no-omnian count has two tails; in a rooted
  restatement the inserted root is a third possible tail, still fewer than
  the four incoming arcs.  The theorem conclusion and exact rooting census
  remain intact.
- Rejected a proposed shortcut that bridge-decomposes a triangle-bearing
  theta into a sunlet and a triangle-free remainder; the third theta path
  reconnects both triangle poles, so necessity remains part of `L_blob`.
- Found no additional nonlocal lemma after the repair.  Both cut inclusions,
  the exact incidence quotient, analytic peeling, no-compensation, root
  reduction, and simultaneous local-`T` gluing are already closed.
- Rejected two overclaims: physical bridge recovery and the assertion that
  every `T` orientation realizes every fixed generic distribution.
- Recorded a safe proof-first finite fallback bound of twelve tensor ports;
  did not assume any stored census terminal or the certificate-specific
  attained bound of ten.

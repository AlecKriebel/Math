# Bernoulli lower-bound audit log

Assigned scope: audit the source Bernoulli cost lower bound and its finite-model,
planar, and deterministic rank-surgery inputs; never assume the source theorem.
Source checkout is read-only. All artifacts are confined to this review folder.

## 2026-10-07T04:29:29Z checkpoint

Completion estimate for this assigned audit: 80%.

- Independently read the complete source proof in planar.tex, rank-surgery.tex,
  finite-models.tex, compression.tex, deployment.tex, group-actions.tex,
  introduction.tex, and conclusion.tex, plus provenance README/INPUTS.
- Source HEAD is adc7f1241b42e322a6451854ab7e4b4c146bf78a; source worktree is clean.
- No counterexample or unsupported implication has yet been identified in
  the lower-bound chain. This is a provisional review outcome, not a formal
  machine-checked proof certification.
- Important potential circularity checked: H in rank surgery is the *actual*
  subgroup of D, and the displayed relative presentation has inverse maps
  on generators. Its embedding is consequently legitimate.
- Exact eta parameter is alpha/100. Chose alpha=2^-61 for an elementary
  certificate using K < 3^97 96^4 and exact integer comparison.
- Requested an independent no-context planar-only falsifier, preserving its
  independence from this provisional outcome. Its result is pending.
- No external communication and no git mutation have been performed.

Strongest provisional result: the reviewed source lower bound has survived
one independent full-chain read; the remaining audit gap is the second
adversarial planar read and integrated parent-level validation, including
the separate L2-Betti bridge and priority/provenance assessment.

## 2026-10-07T04:35:26Z checkpoint

Completion estimate for this assigned audit: 100%.

- The independent planar falsifier completed its no-context review and
  accepted the original lemma under exactly the stated assumptions. No
  counterexample or unsupported transition was identified. Its full
  line-referenced memo is in `planar_falsifier/AUDIT.md`.
- Rechecked all source hashes against the manifest; they are unchanged.
- Exact arithmetic certificate passed with
  alpha=1/2305843009213693952 and
  eta=1/230584300921369395200.
- Independently checked the child's optional bipartite curvature
  strengthening: inner-inner edges join opposite disk signs, so inner
  face walks have even length at least four. Replacing their corner
  weights by 1/2 yields matching intervals of length at least m-2.
  This enhancement is preserved separately and does not alter the source
  or the proof of the requested original bound.
- No external communication and no git mutation were performed.

Strongest final result of this assigned audit: the complete supplied
Bernoulli lower-bound proof supports Cost(R_X)>=1+eta with the exact
positive eta above, with no unresolved lower-chain proof gap identified
after a full read and a second independent review of its most delicate
planar input. This result is inherited from the source; the requested
follow-on L2-Betti bridge and novelty assessment remain parent-level work.

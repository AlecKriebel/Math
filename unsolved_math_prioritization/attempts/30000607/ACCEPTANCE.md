# Acceptance of bounded prior-result coverage

Problem 30000607 / OWR-1386-014. 11 October 2026 UTC.

Verdict: ACCEPT_PRIOR_ASYMPTOTIC_WITH_REPAIRS_AND_FINITE_PARTIALS; ORIGINAL_ALL_N_TARGET_UNRESOLVED.

AI-assisted, unrefereed authored reconstruction and editorial acceptance. This edition is based on one source/proof reconstruction plus an internal AI review of its three reports; it does not claim a second independent mathematical audit, external human peer review, or formal proof-assistant certification. It is not a computational reproduction package.

Jie Han's arXiv:1404.1136v3 proves that, for every fixed k≥3 and all sufficiently large nondivisible n, minimum codegree at least floor(n/k) guarantees a matching of that size. This is a credited prior theorem. The complete source, quantifier and dependency reconstruction is retained in AUDIT.md; the explicit extremal replacement and bounded finite-n approach are retained in PROOF.md. All three underlying authored reports were read in full by an internal AI reviewer. This editorial acceptance does not supply a second independent mathematical audit.

Acceptance includes two local corrections to the displayed extremal proof: count the exact number of surviving vertices rather than charging a multi-A edge as one, and retain the independent-set rounding or replace it by a valid coarse bound. A supplied elementary dense-partite lemma, proved by a second-moment argument and Hall's theorem, replaces the deeper concentration dependency for the actual dense remainder. The original Pikhurko route and its unaudited McDiarmid/Talagrand boundary remain explicitly described. Neither the printed defects nor these repairs amount to a rejection of Han's asymptotic theorem or a blanket judgment on any paper.

Rigorously covered finite families are k=2 for all n≥2, k≥3 with k<n<2k, and k≥3 with n=3k−2 or 3k−1. The space-barrier lower bound holds throughout the domain. These results plus the fixed-k asymptotic theorem do not settle the literal unrestricted all-n question. The precise residual upper-bound family is k≥3, n=kq+r, q≥2, 1≤r≤k−1, n<N(k), excluding q=2 with r in {k−2,k−1}. No numerical or smallest N(k) is supplied. For fixed k the residual range is finite; over unbounded k it is not one finite set. Uncovered here does not mean proved open throughout the worldwide literature.

Eight historical floating-point MILP infeasibility outcomes and one time-limited run have no exact UNSAT certificate and establish no additional finite cases. Historical exact finite consistency checks supplement the written proofs; they are not proof-assistant verification. This edition rechecks byte integrity and editorial retention, without rerunning mathematical programs or reinspecting source bodies.

No mathematical novelty, all-n resolution, full foundational audit, external human peer review, or formal proof certification is claimed. All mathematics is accepted only in the explicit scope and relative to the standard foundations stated in the reports. Authored prose and bounded public-source metadata are distributed; source documents, source code, datasets, raw diagnostics and private coordination material are excluded.

# PR117: proposed priority disposition, not an executed closure

The incoming PR117 head is `8163ee0dc7a0f944570925984cef2dc0fb291ad8`, problem 30001234, literal `claimed_solved`, original ledger 1/5. The mathematical/source gate passes. The original candidate remains unchanged, and no substantive proof-search turn has been added.

## Exact prior and scope bridge

Shunsuke Takagi, *Adjoint ideals and a correspondence between log canonicity and F-purity*, Algebra & Number Theory 7(4) (2013), 917–942, DOI [10.2140/ant.2013.7.917](https://doi.org/10.2140/ant.2013.7.917), gives an explicit prior counterexample in Example 4.4, printed p.940. The actual official PDF is 1,075,287 bytes, SHA256 `6ada6b6669124acda5bb4b0bd25a98d07b39808c07e7d41c1f0ae1ba49e085e5`, from https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf. Root read the complete operative matrix definition on p.937, Remark 4.3 on p.939 and Example 4.4 on p.940, and inspected all three rendered pages. Copyrighted source bodies and renders remain private and excluded.

The published ideal consists of `x1*y2-x2*y1`, `x2*y3-x3*y2`, and `x1*y3-x3*y1`. PR117's third generator is the negative of the last one; multiplication by the nonzero scalar -1 preserves the ideal and polynomial-ring minimality. The question has no complete-intersection restriction on this binomial ideal. Remark 4.3 specializes to its exact program for ambient X=A^6: c=0 makes the extra ambient equality 0=0. Each of the three generators has two monomials. The nine constraints are the six exponent caps and the three paired-generator caps.

Write the PR coordinates as z=(mu1,mu2,mu3,nu1,nu2,nu3). The published paired coordinates are sigma=(mu1,nu1,mu2,nu2,nu3,mu3), the zero-based permutation (0,3,1,4,5,2). The last pair is swapped because of the sign reversal of the third generator. This bijection preserves rational nonnegativity, all nine inequalities, the objective, optimality, and the cardinality of every augmented-image fiber. In particular, the exact existential requirement for an optimizer whose augmented image is shared by no other optimizer is the same assertion.

Example 4.4 explicitly says that this ideal does not satisfy the assumption in Remark 4.3; it also records origin log canonical threshold 2 and program maximum 3. This is an explicit published answer to the same question, rather than a new deduction from an unrelated threshold formula or an absence-of-search-hits inference. The bounded finding establishes an exact prior by 2013; it does not assert the earliest possible discovery date. A family has located an earlier arXiv version, whose date and body remain subject to its final sealed audit and root authentication.

## Valid content and reasonable repair

PR117 independently supplies a correct elementary derivation of the full rational optimal segment z(t)=(t,t,t,1-t,1-t,1-t), t in Q intersect [0,1], with every image equal to the all-ones vector. Its algebraic hypotheses and both endpoint partners are verified. The full-face exposition and reproducibility checks are useful added detail. We have not established a substantive new theorem or a new resolution of the original open question beyond the already published counterexample. A new written explanation or code is not, by itself, evidence that the original negative answer is novel.

Reasonable repair consists of correcting attribution/status and preserving this valid exposition and the diagnostic guard repair. The guard-only diagnostic copies use explicit exceptions in normal and optimized execution; the historical candidate, checkers, ledger, source, and reviews stay frozen. A further novel mathematical problem would require a separately defined target and permitted research budget; it cannot be silently substituted into this PR.

## Proposed authorized outcome and remaining work

Subject to a fresh independent adversarial disposition review and root authentication of the sealed priority evidence, classify the exact target `already_solved`, post the detailed prepared comment, and close PR117 without merging. Do not prepare a preprint, publish a Zenodo record, create a DOI, or add a publication tracker row for PR117. Native assessment must be additive and bound to the exact source/prior pair, preserving the original 1/5 ledger and all other records. No closure, native assessment or completed-PR increment has yet occurred.

Reject a tempting earlier-date inference from Yuen (2006): its cited Theorem 5.1/Corollary 5.3 assume r>s>=3, which excludes the 2-by-3 case even after transposition. An earlier guessed MSP p05 URL was a different article and was rejected. Neither is evidence for this exact priority finding.

Progress at this proposal: mathematical/source audit 100%; exact-prior analysis 90% pending final seals/fresh adversary; PR workflow 55%; program 19/99 completed (19.19%), 11 published; persistent goal remains active. Root main/index writer remains released pending the other chat's actual checkpoint release. This file is a proposal, not a receipt for any future action.

# Virtual homology route: final partial research report

2026-10-24 22:00 UTC. Original Kourovka21.125(b) research outcome: **unsolved**. Best estimate toward a negative Hydra discovery: **3%**. Completion of the limited rank-five obstruction audit: **100%**. No original complete resolution or publication is claimed.

## Strongest independently checked result

In the ordinary rank-five Hydra group there is an explicit subgroup
\[
K=\langle L,t^8\rangle\le G_5,\qquad [G_5:K]=512,
\]
where \(L\le F_5\) is the64-sheeted graph subgroup specified by six binary edge flips in `INDEX512_DELTA.md` and `FINITE_COVER_HOMOLOGY.md`. It admits an integral homomorphism
\[
\lambda:K\longrightarrow\mathbb Z,\qquad\lambda(a_1^2)=1.
\]
Thus \(K\) retracts onto \(\langle a_1^2\rangle\). The same subgroup has integral characters nonzero on powers of each standard generator, all ten elementary free-fiber commutators, and the four recorded left-associated commutators. There are19target entries and18distinct words. For the target words in this package, the commutator convention is **\([x,y]=xyx^{-1}y^{-1}\)**, explicitly encoded in the certificate; the separate parent Engel notes use the opposite convention.

The index512certificate gives a concrete counterexample to persistent homological invisibility of these candidates. It is **not** a RAAG embedding, special cube complex, RFRS chain, or proof that all cyclic subgroups are virtual retracts. It does not settle the Hydra question at rank5 or any other rank.

The originally frozen index1024subgroup remains correct; the separate index512delta uses a smaller already-valid monodromy power. No minimal-index claim is made. Specific smaller powers1,2,4fail to preserve this particular based fiber subgroup, with independently checked closed-loop witnesses; other subgroups at other indices are not excluded.

## Independent adversarial verification

`review/COCYCLE_ADVERSARIAL_REPORT.md` and `review/COCYCLE_AUDIT_HASHES.json` record the fresh independent verdict: **PASS, no blocking mathematical objections**. The reviewer built the graph directly from the six binary flips, implemented signed path substitution independently, generated the targets independently, and verified2880integer cell identities and19exact target evaluations for each of the original and improved certificates. A separate transitive full Hydra permutation action verifies5120original relator instances at index1024 and2560at index512. Eight deliberately corrupted certificates were rejected. The reviewer also found explicit closed-loop witnesses for the lower monodromy-power failures.

The original frozen input manifest remains historical. The review identifies the later index512delta separately and hashes both. Parent review also reran the direct standalone verifier. No independent human peer review is claimed.

## Failed approaches and remaining mathematical gap

Base abelianization kills \(a_1,\ldots,a_{m-1}\). Characteristic finite abelian fiber covers can continue to kill \(a_1\) in rational coinvariants. A particular repeated-character tower also misses it through three further doublings at rank5. Those observations fail to imply a virtual obstruction: choosing a different invariant character immediately yields the verified detecting cover.

The general obstruction target was a single nontrivial element whose every nonzero power is rationally homologically trivial in every finite-index subgroup containing it. Such an element would obstruct virtual RFRS. No such element has been obtained. Conversely, a finite list of visible words supplies neither universal visibility nor the residual chain required for an RFRS proof. The remaining gap is this universal all-covers or all-elements statement; replacing it with a finite cover search is not a mechanism for solving it.

Auxiliary exact characteristic-cover matrix tables through rank6 and the mod-3control through rank4 are reproducible by the author scripts. Their ranks were not independently certified by the fresh rank-five reviewer and are treated as computational controls only. They are not needed for the central concrete certificate.

## Rank-six auxiliary delta

An already-running search found a128-sheeted fiber cover preserved by \(\theta^{16}\), producing an index2048subgroup of \(G_6\). Six direct integral cochains detect the first closing powers of all six standard generators. Their values are14,28,2,7,14,1 on the powers2,4,2,4,4,2respectively. The direct solver-free verifier checks4608edge identities. The value14on \(a_1^2\) proves visibility; no retraction onto exactly that cyclic subgroup in this same subgroup is asserted. A separate fresh independent delta review has now passed: `review/RANK6_DELTA_REVIEW.md` and its hashed receipt confirm all768edge endpoints,4608integer cells, and six signed first-power evaluations. It is a separately accepted partial control; it does not change the rank-five verdict or support any RFRS/specialness conclusion. No further search is planned.

## Record and reproduction

`rank5_cocycle_certificate_index512.json` with `verify_cocycle_certificate.py` is the shortest direct accepted verification package. The fresh independent implementation is `review/independent_cocycle_audit.py`. The long author search and matrix calculations are unnecessary to check the accepted finite-index claim.

The parent obstruction package was independently reviewed only after this investigation's main artifacts were frozen. That separate audit is in `../review/AUDIT.md`, with a complete independent exact permutation census through degree8 and uniform-construction checks through rank129. It does not certify these homology calculations and was not used to discover this cover.

All work here was developed and checked with AI agents and exact computer arithmetic. No external individual was contacted, no manuscript was submitted, no upload or DOI was created, and no tracker entry was added. No novelty or first-priority claim is made for these finite partial observations.

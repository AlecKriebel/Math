# PASS 2 source and exact-law scope audit

## Verified counting source

Miklós Bóna, *The limit of a Stanley–Wilf sequence is not always rational, and layered patterns beat monotone patterns*, arXiv:math/0403502v2, 13 May 2004; later J. Combin. Theory Ser. A110 (2005),223–235. Primary PDF: https://arxiv.org/pdf/math/0403502v2 . The recovered PDF has151738 bytes and SHA-256 `217fc489503f5a3c6a60b06c14ff29713b2ad9087c8f8f8875aeae1ce4da579f`.

Page7, Proposition5.1 supplies the canonical left-to-right-minima deletion rule when the inner forbidden pattern q starts with1. Theorem5.4, through the hypotheses of Lemma5.3 on the same page, states

`L(1 direct-sum q)=(1+sqrt(L(q)))^2`

under that starts-with1 hypothesis. Theorem5.2 specializes this to `beta_d=I_d direct-sum231`, with `L(beta_d)=(d-1+sqrt8)^2`. These are credited enumeration facts, not new asymptotic geometry claims.

The hypothesis matters twice: it validates canonical deletion and the cited growth equality. For example,34152 avoids1342, but deleting its left-to-right minima3,1 leaves452, whose standardization is231. Therefore a deletion claim for arbitrary q would be false. The source theorem does not imply growth9 for1342 by starting from231, and does not imply growth16 for1324 by starting from213.

## Canonical injection versus ambient overcount

For a permutation p, record the positions S and values V of its non-minimum entries, together with their standardization sigma. This triple reconstructs p uniquely: place sigma using S and V, then put the unused values in decreasing order in the unused positions. If q starts with1, p avoids1 direct-sum q if and only if sigma avoids q.

Proof of the nontrivial direction: the first entry of a q occurrence among the non-minima is its minimum; a preceding smaller entry exists because it is not a left-to-right minimum. This supplies the initial1. Conversely any1 direct-sum q occurrence has every q entry preceded by a smaller entry, so that occurrence survives deletion.

The valid canonical triples are only a subset of all triples with |S|=|V|=k and sigma in Av_k(q). The ambient number at fixed k is `binom(n,k)^2*|Av_k(q)|`. An arbitrary ambient triple may fail to have the designated complementary entries as its exact minima. It must not be described as an exact uniform generator of Av_n(1 direct-sum q).

For an upper bound on the count of geometrically bad actual permutations, however, the canonical injection into bad ambient triples is enough. In that ambient family the subsets S and V are independent and uniformly distributed when k and sigma are fixed. Hypergeometric allocation concentration is applied there, before any validity conditioning, and the resulting bad tuple count is divided by the actual class size. Matching exponential growth rates make the exponentially smaller bad count negligible even if the valid fraction itself has non-polynomial subexponential losses.

## Protected-tail source boundary

Henning Arnór Skeggi Úlfarsson, *Protected tails and polynomial-time enumeration of permutations avoiding a direct sum of an increasing pattern and231*, arXiv:2609.15642v2,1 October2026, https://arxiv.org/abs/2609.15642v2 . Its exact recurrence and sampler are enumeration inputs; the sampled heatmap and its finite-size total-variation guarantee are not a permuton limit theorem.

The number of intervals in its scan stack is not Bóna's geometric tree height. The increasing permutation avoids every beta_d and is scanned with at most one interval after its first d-trigger; its permuton is diagonal rather than anti-diagonal. Hence a bound on that stack length alone cannot provide the required deterministic geometric implication.

The current candidate instead uses canonical minimum deletion and matching growth to transfer the PASS1 exponential weak-concentration result. Its full written proof requires a separate pinned review; this scope note does not accept an unseen draft.

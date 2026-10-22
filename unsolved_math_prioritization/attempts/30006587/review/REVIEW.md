# Independent source and algebra review: the multiple-Eisenstein derivative formula

**30006587 / OWR-14299909-002. Verdict: PASS_SOURCE_MATCH_AND_SCOPED_ALGEBRA; full analytic proof certification remains on hold.**

The July 2026 three-author preprint states and proves the exact original derivative conjecture. The submitted package accurately records that external resolution claim, its normalization, and the limits of the local audit. No mandatory correction to the frozen source record is required. This review does not certify every all-depth analytic realization and regularization dependency, and does not convert a submitted preprint into a peer-reviewed publication.

Covered SOURCE_STATUS.md SHA-256:
**440edf90c25d16eeb424699d88a4c93f81a079040e753915925a9773e8ed7a60**.
The author’s mathematical source record was not edited.

## Exact theorem and version match

The complete [Oberwolfach report](https://ems.press/content/serial-article-files/53601?nt=1), Bachmann's contribution on printed pp.449–450, uses the classical lattice series with every entry at least two, including two. The horizontal lattice limit is inside the vertical limit. Its ordinary harmonic product has a positive merge term. With the specified Drop1 map, it defines θ as minus Drop1 applied to the harmonic-minus-shuffle discrepancy with z₂. The requested operator is 2πi times the τ derivative.

I independently read the source contribution and visually inspected its displayed conjecture. In particular the factor is not 1/(2πi). Substituting q=exp(2πiτ) gives (2πi)² q d/dq on the unnormalized G-series. The normalization in the submitted record is correct.

The full [v2 manuscript](https://arxiv.org/pdf/2602.08176v2) has Main Theorem D(ii) on printed pp.8 and 30 with exactly these all-at-least-two indices, the same θ and the same derivative. Its proof on p.30 was read and visually checked. Main Theorem C explicitly identifies the auxiliary realization with the classical lattice series on this subspace; this identification is necessary, rather than an optional change of normalization.

The [current arXiv record](https://arxiv.org/abs/2602.08176) independently confirms the three authors, 42 pages, and upload of v2 on 13 July 2026. The document's 14 July date is distinguished from its upload date. The [author's current publication list](https://www.henrikbachmann.com/publications.html), dated 25 September 2026, still lists it as submitted. The earlier February two-author version contains the conjecture instead. No withdrawal or later journal version was found in this bounded check.

The all-relations equality in v2 Conjecture 1.8 is separate and remains labelled conjectural. The broader multiple-1 Drop1 statement in Conjecture 4.9 is likewise unnecessary for the displayed derivative theorem. Neither is resolved by this package.

## The reconstructed cancellation is valid with its inputs

I checked the stated harmonic/shuffle conventions, the divided powers in the lower variables, Theorem 4.7, Lemma 4.8 and the final proof of Main Theorem D against the full v2 text.

A literal shuffle of an all-at-least-two word with xy introduces at most one index 1, never at the first position. The full exceptional contribution is exactly the double sum in equation (3) of the submitted record, including coefficient 2k_j. Once Lemma 4.8 is applied, the sum over insertion positions telescopes from the j-th lower-index increment to zero at the terminal position. Thus the correction is 2∂w. Since Drop1 fixes the harmonic product w*z₂, the resulting congruence is
\[
\theta(w)\equiv 2\partial w-\varphi(w)\equiv\partial w\pmod I.
\]
The unit has both sides zero. No free-algebra derivation property of θ is assumed; the manuscript itself explicitly records its nonzero derivation defect before passing to evaluated relations.

The one-1 formula used by the checker is the actual Theorem 4.7 with the quasi-shuffle antipode, whose signed reverse-and-merge description agrees with the paper. It is not an arbitrary replacement map selected merely to preserve zeta values. The quoted congruence additionally depends on the finite harmonic/diamond identities and the corresponding independence theorem. The package labels these dependencies accurately.

For coefficient extraction, differentiating u^(d+1)/(d+1)! times v^k produces k u^d/d! times v^(k−1). Thus the coefficient is k, without an extra d+1. In depth one the stated swap coefficient d!/(k−1)! is consistent with the divided-power basis and squares to the identity after swapping the indices.

## Why the analytic hold is substantive

I read the full v2 definitions and argument in Section 3.2, especially the modified multitangent series, block factorization, recovery of the classical series, swap statement and derivative identity. The fixed-coefficient decay mechanism and derivative bookkeeping in the submitted record agree with those displayed formulas. The zero Fourier constant of the modified nonempty multitangent blocks is essential. For a fixed coefficient and compact upper-half-plane set, exponential decay multiplied by finitely many polynomial factors is sufficient for the stated local normal-convergence argument.

The coordinate blocks in a deconcatenation are disjoint. A same-coordinate mixed derivative therefore has no cross-block term. Within a factorized block, the middle multitangent piece contains the relevant v-variable while the corresponding u-derivative acts on the exponential. In the terminal bi-zeta factor each coordinate lies in either the u-piece or the v-piece, so its same-coordinate mixed derivative is zero. These checks support the claimed normalization and differential mechanism.

The all-depth swap transfer is more than this bookkeeping: v2 Theorem 3.19 invokes an analogous mould manipulation from Bachmann–Burmester's published Theorem 6.26. Together with regularized multitangent and diamond-basis inputs, it is part of the realization theorem needed to annihilate I. I have not independently reconstructed that entire chain at every depth. The published combinatorial realization alone would not identify the classical analytic G-series. The author's hold therefore marks a real boundary of this audit; it is not an allegation that the preprint contains an error.

## Exact controls and disposition

All **1,111 submitted assertions** reproduce byte for byte in the preserved author replay. A separate standard-library checker passes **1,946 exact controls**, using position-selection shuffles rather than the author's recursive shuffle routine, terminal telescoping, divided-power coefficient extraction and the first 81 exact Fourier coefficients of the classical weight-two identity. In normalized variables g_k=G_k/(2πi)^k, the latter reads q g₂'=5g₄−2g₂² and confirms the derivative scaling independently.

These finite controls establish no all-depth analytic realization theorem. The full theorem is an external preprint result, attributed to Bachmann, Kanno and Maesaka; no campaign discovery is claimed.

**Queue recommendation for this audit:** retain **unsolved with an external-preprint-resolution/source hold**, zero new-discovery approaches and the one logged validation family. The public description should prominently say that an exact full resolution is posted in v2, so “unsolved” is not misread as a claim that the literature still lacks a proof. An unqualified already_solved classification would exceed this audit's validation scope. A future decision to treat posted, unaudited external theorems as already_solved would be a repository status convention, not an additional mathematical conclusion supplied here.

No mandatory change to the frozen source record is required. Preserve both its positive source finding and its explicit proof-certification limit.

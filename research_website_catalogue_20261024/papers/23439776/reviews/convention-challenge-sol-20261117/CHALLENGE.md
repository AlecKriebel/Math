# Focused historical-coordinate challenge

Date: 2026-11-17 (America/Los_Angeles).

Checkpoint: assigned finite challenge 100% complete. This is not an assessment of overall manuscript validity, a global scientific PASS, or a publication recommendation.

## Question and independent reading scope

Does the difference between the A2 example in Schumann's OWR 20/2021 contribution and the reduced-word seed conventions used by the D4 note establish a substantive historical-chart identification gap?

I read the native manuscript, the actual OWR contribution body, the KS2022 publisher body and arXiv body, and the GKS2017v1 body. I did not read current family reports, final verdicts, or derivations. Before root released the checkpoint hold, I wrote no files and ran no substantive verification programs. This document records the primary-source reasoning already reported to root during that hold. No paper repair, D4 recomputation, or new research claim is supplied here.

## A2 calculation and exact coordinate swap

For the word (1,2,1), KS2022 Eq. (3), Definitions 7–8, and the actual Example 3 quiver give horizontal arrow 1→3 and inclined arrow 2→1; vertices 2 and 3 are frozen. I directly viewed the publisher's Example 3 image. Write y_j=X_j^{-1}.

Vertex 3 is already optimized for root 1, so W_1=y_3. Mutating at vertex 1 optimizes vertex 2. The initial pairing is b_21=1, hence KS Eq. (3) gives

    X'_2 = X_2 (1+X_1^{-1})^{-1},
    (X'_2)^{-1} = y_2 (1+y_1).

Thus W_2=y_2(1+y_1). GKS2017v1 Example 5.3 explicitly displays the same positive-root summands.

OWR printed p. 1124 instead displays inequalities -x_2≥0, -x_3≥0, -x_1-x_3≥0, grouping the singleton under root 1 and the latter pair under root 2. These are exactly the preceding monomial inequalities under the permutation of the two frozen coordinate labels X_2↔X_3. This permutation preserves coordinatewise absolute exponent bounds, the number of monomials, and inequality irredundancy. The A2 discrepancy therefore does not by itself exhibit a different substantive chart or defeat the D4 consequence.

## Older mutation formula inconsistency

GKS2017v1 §4.2.1 defines positive pairing as arrows from the first vertex to the second, and Definition 5.1 uses incoming optimization with inverse frozen-coordinate normalization. Its Eq. (20), however, uses the pairing in the opposite order to KS2022 Eq. (3).

Taking that older formula literally at vertex 1 gives X'_2=X_2(1+X_1), so pulling back the optimized inverse coordinate would give y_2/(1+X_1). This contradicts the same GKS version's explicit Example 5.3 expression y_2(1+y_1). Consequently the reversed-pairing formula does not supply a coherent alternative historical potential convention. This is a source inconsistency, not a proposed correction to either paper. The native note explicitly chooses KS2022 Eq. (3).

## Actual source bridge

GKS2017v1 §4.2.2 supplies the same horizontal/inclined arrow construction, including Dynkin adjacency. Definition 7.1 specifies the chamber map on the positive-index coordinates; Theorem 7.5 identifies the string functions with the potential summands pulled back by that map, and Corollary 7.7 gives the cone identification.

KS2022 Definition 9 gives those positive-index chamber-map exponents. Proposition 5's proof expressly invokes GKS Theorem 7.5 and the right diagram of Lemma 7.4, specializing the negative-index X variables and the lambda variables to 1. This is a primary-body specialization bridge to the reduced setup, rather than an inference from common names alone. OWR Theorem 1 explicitly cites GKS for its string-cone/cluster-cone identification.

## Bounded conclusion and exact limitations

The focused A2 objection is resolved at the level needed to assess that objection: its displayed discrepancy is an exact coordinate permutation preserving both conjecture properties. Actual GKS/KS source formulas and KS's explicit specialization support the same reduced-word construction. No coherent materially different historical chart emerged from the examined bodies.

OWR does not supply a general vertex-to-coordinate labeling dictionary. I have not established such a dictionary from OWR alone, and no such additional claim is needed to dispose of the exhibited A2 permutation objection. The final published GKS body was not obtained: its DOI redirected to an inaccessible Elsevier endpoint, and ScienceDirect returned an access error. The accessible arXiv record lists only v1; a supposed v4 was not used. The GKS PDF text was available, but attempted web screenshots did not yield inspectable images; no claim of viewing its pictures is made. The KS Example 3 picture was successfully retrieved and viewed in memory, without saving a copy.

This challenge does not independently verify the D4 mutation computation, facet certificates, novelty, or the complete historical claim. Those remain outside this assigned finite review.

## Primary sources and retrieval locations

- OWR 20/2021, Schumann contribution, printed pp. 1123–1125: https://ems.press/content/serial-article-files/46898 . Also read the existing primary web-extract-only file `papers/23439776/reviews/adversarial-sol/PRIMARY_OWR_CONTRIBUTION.txt`.
- KS2022 journal article, Eq. (3), Definitions 7–9, Example 3, Proposition 5: https://link.springer.com/article/10.1007/s10801-022-01144-z . Corroborating primary arXiv body: https://arxiv.org/html/2109.14439v1 .
- KS Example 3 quiver image viewed directly: https://media.springernature.com/lw231/springer-static/image/art%3A10.1007%2Fs10801-022-01144-z/MediaObjects/10801_2022_1144_Equ45_HTML.png .
- GKS2017v1, §§4.2.1–4.2.2, Definition 5.1, Example 5.3, Definition 7.1, Theorem 7.5, Corollary 7.7: https://arxiv.org/pdf/1711.07176 . Version record: https://arxiv.org/abs/1711.07176 .
- Published GKS access attempts, unsuccessful: https://doi.org/10.1016/j.aim.2020.107178 and https://www.sciencedirect.com/science/article/pii/S0001870820302048 .

No outreach was prepared or initiated. No native source, public artifact, global workbook, or Git state was changed by this challenge.

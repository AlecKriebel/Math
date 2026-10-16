# Independent exact-source review: 5100008 / k117

**Verdict: PASS — exact published resolution, correctly scoped and credited.**
Recommended disposition: `already_solved`, 0/5 new author proof turns. No mandatory correction to the frozen correction. This is a source-status audit, not a new discovery or a human peer-review claim.

## Frozen object and independence

Reviewed STATUS_CORRECTION.md, SHA256 `96c4ccce66ba5e5a387ed57b6adfe75e4ebcdcca2f30de8d6d9ebc6682fbd2dc`, from author package frozen_artifacts.json SHA256 `045a19d84c100fef1c60a1bb9ef18024121f20847ed09194b90d7e421ae89e39`. All five frozen author-file hashes were recomputed and matched. The exact imported statement and prior report, source manifest, continuity record and research log were read. I did not edit those artifacts.

Independently accessed the publisher article and its complete current PDF, in addition to the author's full DNB-hosted published PDF and preprint. The theorem/proof page and both original invariant tables were inspected visually. This is not an abstract/snippet-only identification. The older OPEN-TRIAGE report's lack-of-proof finding is historical and is superseded by the verified theorem; it was not a prior campaign proof attempt.

## Primary theorem match

Stachel, *On the motion of billiards in ellipses*, European Journal of Mathematics8 (2022),1602–1622, DOI10.1007/s40879-021-00524-2, Theorem5.6 on p.1621 explicitly identifies k117 and gives both full positive-length products as k_e^(N/2). The parameter k_e is the common difference of the squared outer and caustic semiaxes. Lemma5.1 defines the two contact-segment lengths. The preprint carries the same result as Theorem10. The arXiv-v11 and 2021 published invariant tables retain the k117 label/formula, unlike some nearby area rows.

The theorem and its proof are available at [the publisher](https://link.springer.com/article/10.1007/s40879-021-00524-2), with [complete PDF](https://link.springer.com/content/pdf/10.1007/s40879-021-00524-2.pdf). The local publisher PDF has SHA256 `9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8`; the author's DNB PDF has a different binary hash, but the checked theorem, proof, definitions and equation numbering agree. Their different pagination/header versions must not be described as byte-identical.

## Independent mathematical checks of the application

1. **Indexing.** Let Q_i be the contact on P_iP_(i+1). The imported outgoing segment l_i is exactly Stachel's l_i. The imported remaining segment r_i equals Stachel's r_(i+1), not r_i. The cyclic product over all N indices is unchanged by this permutation. There is no reversal of a length sign.
2. **Scale and exponent.** Write lambda=a²−a_c²=b²−b_c²>0. It has units of length squared. A product of N lengths therefore has the units of lambda^(N/2), as the theorem says. The half-period product in the additional N=0mod4 statement is not the requested full product; its exponent N/4 must not be substituted.
3. **Primitive and star scope.** In canonical coordinates the vertex increment is4tauK/N and the intervening contact has offset2tauK/N. For primitive even N, gcd(N,tau)=1 forces tau odd. When N=4n, n vertex steps change the parameter by tauK. When N=4n+2, the offset to the relevant contact is again tauK. Modulo the real period2K of dn, both are K. Thus the quarter-period pairing used for the product is valid for admissible star windings, not just tau=1.
4. **Two typographical slips do not change the deduction.** The paper's signed2K shift for dn is false as printed; dn has period2K. Also the last proof's remaining-case notation must use N=4n+2 to match the cited pair indices. The frozen correction explicitly warns about both, and its formula uses the correct identities. No repaired theorem beyond the stated result is being inferred.
5. **Positive root.** Products are strictly positive in the nested nondegenerate elliptical setting. If a proof step yields R²=lambda^N, the allowed root is unambiguously R=lambda^(N/2). No signed-length interpretation or zero-area exception enters.
6. **Boundaries.** Ordinary polygon area and angle representative are irrelevant. Orientation reversal interchanges the two products. Repetition of an even primitive orbit raises the formula to the repetition power. Doubling an odd primitive orbit does not satisfy the primitive-even assumption. The correction properly avoids hyperbolic/degenerate caustics. The original invariant source assumes a>b; no noncircular hypothesis is lost. If the circular limiting case is separately included, every contact bisects a chord and each half-length is sqrt(lambda), giving the same formula directly.

The theorem's “billiard motion” varies the starting point within the fixed outer/caustic pair. Neither fixed perimeter alone nor an invariant of another derived polygon is being substituted for that family. All N factors are present in each requested product.

## Independently authored controls

independent_check.py was written separately for this audit, not adapted from an author verifier. It performs:

-36 exact rational controls on genuine four-period configurations, checking Euclidean segment lengths and both products
-8,901 high-precision assertions, at65 decimal digits, across54 primitive families, three phases each, with30 star families; checks include outer/inner conic equations, tangent incidence, contact position, both full products and cyclic indexing
-A deliberately nonprimitive N=6,tau=2 negative control: the odd primitive orbit doubled fails the enlarged formula by relative0.000256228537537995 at the tested phase, confirming the exclusion is substantive

All controls PASS; maximum normalized residual8.379838536e−64. These finite checks are diagnostics, not substitutes for the published theorem. No assertion that they certify all ellipses or all periods is made. The source correction contains no author numerical proof to replay.

## Publication disposition

The frozen correction completely matches the source-normalized target. Retain its published attribution and0/5 count. The author performed a readiness/literature correction rather than a new proof search; independent review and these checks do not create author proof turns. Do not promote a broader literal interpretation allowing arbitrary repeated odd orbits or hyperbolic caustics. No outreach, remote publication, queue change, merge or release was performed by this reviewer.

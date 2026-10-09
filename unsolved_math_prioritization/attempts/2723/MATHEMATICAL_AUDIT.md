# KP-1.64: clause-specific audit of published branched-cover counterexamples

Checked 9 October 2026 UTC. Record 2723; KP-1.64.

Edition note: this is the complete authored source-based AI mathematical audit, with provenance-only edits documented in PROVENANCE.md. Its pre-acceptance chronology is retained. The subsequent independent review and current accepted scope are in ACCEPTANCE.md.

**Audit-stage conclusion, before separate independent acceptance:** published results give counterexamples to clause (a), and to clause (c) whenever its branched-cover hypothesis includes the double cover. Clause (b), requiring a Stein-fillable cyclic cover of some order strictly greater than two, is not settled by the inspected Brejevs–Wand result or the other sources checked here. Do not mark the complete three-part problem solved. No acceptance was issued at this audit stage; the subsequent acceptance is recorded separately.

A convenient single witness is the positive transverse closure of

\[
 b_6=(\sigma _1\sigma _2)^6\sigma _1^5\sigma _2^{-21}\in B_3.
\]

It is a knot, its induced contact double branched cover is Stein fillable, its transverse self-linking number is -7, and its entire oriented smooth knot type is nonquasipositive. The last assertion needs an additional argument; it does not follow just from nonquasipositivity of this one braid. The short arguments are given below.

This is verification of existing mathematical results and their direct scope consequences, not a new original-proof campaign. Zero fresh substantive proof-search turns are charged. The audit was read-only; preparation of this theoretical edition adds no mathematical proof-search approach.

## 1. Source restoration and the three different assertions

The full primary problem is K3, printed/PDF page 62, in the Berkeley permission-watermarked author preliminary version:

https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

Its retained bytes were rehashed and its page 62 was freshly rendered and visually inspected. The catalogue's AIM `kirbylistrep.pdf` is a four-page workshop summary, not the numbered full problem list. That link must not support an assertion about the exact clauses.

The following mathematical formulation preserves the source's quantifiers without reproducing its prose. Let T be a positively transverse oriented link in the standard cooriented contact sphere. Let \(\xi_{T,n}\) denote the canonical induced contact structure on its **cyclic** n-fold branched cover. Write QP(T) when T is transversely isotopic to the closure of a quasipositive braid, allowing any braid index.

- (a): For every such T, does Stein fillability of \((\Sigma_2(T),\xi_{T,2})\) imply QP(T)?
- (b): For every such T, does \(\exists n>2\) for which \((\Sigma_n(T),\xi_{T,n})\) is Stein fillable imply QP(T)? The hypothesis is existential in n. It is not a hypothesis about all cover orders.
- (c): Does the stated Stein-fillability hypothesis force the slice-Bennequin inequality to be sharp for the given transverse link? For a knot this means \(\operatorname{sl}(T)=2g_4(K)-1\), where K is its oriented smooth knot type and g4 is the smooth four-ball genus.

The source does not repeat a cover order in (c). We therefore distinguish the precise conclusions: the twofold instance of (c) is false; consequently the unrestricted implication allowing an order-two cover is false. A separately imposed restriction n>2 in (c) is not resolved here. This is not a claim that every possible fixed higher-cover formulation of (c) has been refuted.

The words “given transverse link” matter. Optimizing self-linking over a smooth link type changes the assertion. Smooth isotopy to some quasipositive link also differs from transverse isotopy to a quasipositive braid closure. Our preferred witness happens to disprove even the weaker smooth-link-type conclusion, but we prove that separately.

For links, the slice-Euler-characteristic convention concerns smooth, properly embedded, oriented surfaces in B4 with the prescribed oriented boundary and no closed components. Using the knot b6 avoids any ambiguity about connected versus disconnected bounding surfaces.

## 2. What Brejevs–Wand actually proves

Vitalijs Brejevs and Andy Wand, *Stein-fillability and positivity in the mapping class group*, Journal of Symplectic Geometry **24**(2) (2026), 467–477, DOI **10.4310/JSG.260607013316**, first online **17 June 2026**.

Verified publication record: https://eprints.gla.ac.uk/348867/ . It explicitly marks the article published and refereed. The arXiv v2 comment still says “to appear”; that is stale publication metadata.

Inspected mathematical text: arXiv:2405.07707v2 (9 July 2025) and the institutional accepted-version PDF https://eprints.gla.ac.uk/348867/1/348867.pdf . The accepted file has seven manuscript pages plus one institutional deposit leaf, eight PDF pages total. It is not the eleven-page final publisher layout. Comparison of the two extracted texts found the manuscript body agrees apart from the arXiv first-page layout/stamp; the accepted copy appends the deposit leaf. Final publisher-PDF identity has not been established or claimed.

Their Theorem 1 has the following full operative hypotheses. On a once-punctured torus S, take simple curves a,b intersecting once and a boundary-parallel curve delta. For **every integer k>=0**, set

\[
 \phi_k=t_\delta t_a^5t_b^{-(15+k)}.
\]

The contact structure supported by (S,phi_k) is Stein fillable, although phi_k has no factorization into positive Dehn twists on this page. Their associated braid is

\[
 b_k=(\sigma_1\sigma_2)^6\sigma_1^5\sigma_2^{-(15+k)}.
\]

The relevant group isomorphism sends sigma1 to t_a and sigma2 to t_b, and the chain relation sends \((\sigma_1\sigma_2)^6\) to t_delta. No additional L-space, quasialternating, fibered-branch-knot, or higher-cover hypothesis appears in this theorem.

### 2.1 Full proof structure and the nonpositive-monodromy input

The entire manuscript argument, including the proof on pages 4–6 and the surgery Figure 2, was read. It has three logically distinct steps.

1. **Nonquasipositivity in B3.** With Delta=sigma1 sigma2 sigma1, their Lemma 5 conjugates b0 to

   \[
   b'_0=\Delta^{-11}\sigma_1^7(\sigma_2^2\sigma_1^2)^7.
   \]

   This has reduced-standard-form parameters p=-11, m=15, and exponent sum e=-33+7+28=2. Orevkov's necessary inequality is \(0<p+m<2e\). Here p+m=4=2e, violating the strict upper bound. For k>0, if b_k were quasipositive, then b0=b_k sigma2^k would be quasipositive because the quasipositive braids form a monoid. Thus none of the b_k is quasipositive.

   The precise imported result was checked in Orevkov, *Algorithmic recognition of quasipositive braids of algebraic length two*, Journal of Algebra 423 (2015), 1080–1108, author manuscript, Section 6, Proposition 6.5(b), including its proof and Lemmas 6.1–6.3. Its “reduced” condition permits (i) at most one syllable, (ii) (1,1) with even p, or (iii) syllable count congruent to p modulo two with all exponents at least two. The displayed b0' satisfies (iii). In this non-all-2 case the obstruction follows from the quasipositive Murasugi–Tristram bound and the signature/nullity formula of Lemma 6.2. No run of Orevkov's C algorithm is needed or was performed.

2. **Positive mapping classes versus QP(3).** Brejevs–Wand Theorem 3 imports Ito–Kawamuro Theorem 3.2. The actual publisher proof at pages 316–317 was read, not merely the statement. For a once-punctured torus, positive twists about nonseparating curves are conjugates of t_a; boundary twists are positive products by the chain relation. Thus the group isomorphism restricts to an isomorphism between QP(3) and the positive-twist monoid. The lack of a positive factorization is on the **specified page**. Stein fillability requires a positive factorization on some supporting open book after suitable stabilization, not on this particular one.

3. **Tightness plus an all-tight-structures Stein theorem.** These are separate inputs, detailed next. Nonvanishing of a Floer contact invariant alone is not being used as a Stein-fillability criterion.

### 2.2 Tightness: exact substitution into Baldwin

Baldwin, *Heegaard Floer homology and genus one, one boundary component open books*, J. Topology 1(4) (2008), 963–992, Theorem 4.2(1), uses h=(xy)^3 and monodromies

\[
 h^d xy^{-a_1}\cdots xy^{-a_m},\quad a_i\ge0,\quad\text{some }a_j>0.
\]

The contact invariant is nonzero exactly when d>0 in this family. Substitution for phi_k is **d=2, m=5, (a1,...,a5)=(0,0,0,0,15+k)**. All hypotheses hold. Hence the supported xi_k is tight. It would be wrong to impose the different L-space condition of Baldwin Theorem 4.1, which in this case allows only d in {-1,0,1}; our d=2 manifolds are not in that L-space subfamily.

The current unversioned arXiv download is explicitly v2, 10 May 2008, and was pinned. Theorem 4.2 is a compilation rather than a new proof in that paper. Its relevant positive-twist/tightness source is Baldwin's earlier *Tight contact structures and genus one fibered knots*, published AGT 7 (2007), 701–735. The retained v3 preprint's Theorem 1.2, Section 3 proof of Theorem 3.2, its Lemmas 3.4–3.6, and the determinant appendix were read. The contact-invariant proof starts with a positive-monodromy lens-space case, applies surgery-exact-triangle injectivity inductively through the nonnegative exponents, then adds a positive boundary twist. It establishes nonvanishing for the type-I family with at least one boundary twist, exactly the regime used here. Foundational Floer and contact-surgery theorems remain cited results, not newly re-proved foundations.

### 2.3 Oriented surgery identification and actual Stein fillability

Brejevs–Wand page 6 and Figure 2 identify the underlying oriented 3-manifold as

\[
 Y_k\cong \Sigma_2(\widehat b_k)\cong \operatorname{Wh}(5,-15-k).
\]

The diagram first uses a -1/2-framed blow-up downstairs, then an Akbulut–Kirby double-cover surgery presentation with a five-chain whose framings are four -2's and one -17-k, together with a threaded -1 unknot. A blow-down, a +1 blow-up, and four subsequent blow-downs give Whitehead surgery coefficients +5 and -15-k. Figure 2 was freshly rendered and viewed in full. Its final Whitehead-link clasp convention was compared with Figure 1 of the Min–Nonino published version. These are ordinary orientation-preserving surgery moves; they are not being claimed to be contact Kirby moves.

The topological diffeomorphism alone does **not** identify xi_k with a chosen Stein-fillable structure on that manifold. The crucial imported theorem says **every tight structure** on this oriented manifold is Stein fillable, so it applies to the transported xi_k.

The dependency now has its own verified final publication:

Hyunki Min and Isacco Nonino, *Tight contact structures on a family of hyperbolic L-spaces*, Geometriae Dedicata **220:45** (2026), DOI **10.1007/s10711-026-01097-8**, first online **4 July 2026**, accepted 3 June 2026. Institutional published/refereed record: https://eprints.gla.ac.uk/390111/ . The actual 42-page published PDF was downloaded from https://eprints.gla.ac.uk/390111/1/390111.pdf . Its Theorem 1.6 retains the hypotheses

\[
 n\in\mathbb Z,\quad n\ge5,\qquad
 r\in ((-\infty,0)\cup[2,4)\cup[5,\infty))\cap\mathbb Q.
\]

Every tight contact structure on M(n,r)=Wh(n,r) is Stein fillable. Set n=5 and r=-15-k. Both conditions hold for every k>=0. In particular, the title's reference to hyperbolic L-spaces does not restrict the theorem to positive r or to L-spaces.

For these **negative-r** cases, the proof is especially direct once classification is available:

- Proposition 3.1 and Figure 8 give only negative contact surgeries (trefoil coefficient r-1, other components -1), hence Stein fillings.
- Proposition 3.2 constructs Psi(r) different structures via the negative continued-fraction stabilization choices and distinguishes their boundary contact invariants.
- Theorem 4.8's negative-r branch gives at most Psi(r) tight structures. It decomposes a tight filling into C_n(1) and N_r(1); Lemmas 4.4–4.5 control thickening and the contact structure on C_n(-1/m), while Lemma 4.7 counts the solid-torus structures. Thus the constructed Stein-fillable structures exhaust the tight ones.
- Section 5's proof of Theorem 1.6 focuses on the additional positive-r cases because negative-r Stein fillability is already in Proposition 3.1. Reading only Section 5 without Section 3 would miss that point.

The theorem, full Section 5 proof, negative-r constructions and classification argument, and the proofs of the immediate thickening/counting lemmas were read in their bodies. The relevant final-version lemmas use boundary-setwise isotopy and internally exclude boundary-parallel half Giroux torsion in the tight filling decomposition. These are ingredients of the classification theorem, not additional hypotheses to add to Theorem 1.6. This audit does not purport to re-prove all of convex-surface classification or the foundational Giroux/Honda results imported by those proofs.

The 2023 preprint was also downloaded before the publication record was found. The final version corrects and expands some intermediate exposition (for example the opening “no boundary parallel dividing arcs” assumption in Proposition 4.12), and renumbers the negative-slope proposition from 4.15 to 4.16. The final negative-r theorem and construction, rather than a stale preprint-only statement, support this audit.

## 3. The induced contact cover is the one in the problem

This bridge is essential. Let T_k be the positive transverse closure of b_k in the standard contact sphere, braided around the standard disk-open-book binding. The double cover of a disk branched at three points has Euler characteristic -1 and one boundary component, hence is a once-punctured torus. A positive half-twist about adjacent branch points lifts to a positive Dehn twist. Therefore the lifted monodromy is phi_k.

Harvey–Kawamuro–Plamenevskaya, *On transverse knots and branched covers*, IMRN 2009(3), 512–546, arXiv:0712.1557v1, Section 2.5 and Section 3.1/Lemma 3.1, supplies the **contact** identification for transverse links, not just an underlying topological cover. Section 2.5 starts with the canonical pullback contact form away from the branch locus and its standard local smoothing near it, and identifies its contact isotopy class with the lifted open book. Lemma 3.1 and its complete proof compute the lift of each positive half-twist as p-1 right-handed twists; for p=2 this is a single twist. The construction explicitly permits links.

Ito–Kawamuro, *Positive factorizations of symmetric mapping classes*, J. Math. Soc. Japan 71 (2019), 309–327, Section 1.1, restates the contactomorphism for the special cyclic covering whose meridians all map to 1 modulo the cover degree. Its motivation paragraph is phrased for knots; the original Harvey–Kawamuro–Plamenevskaya source removes any link-scope ambiguity.

Thus

\[
 (\Sigma_2(T_k),\xi_{T_k,2})\simeq (Y_k,\xi_k)
\]

as oriented cooriented contact manifolds. Applying Brejevs–Wand gives Stein fillability of the actual structure asked about in K3. No arbitrary contact structure on the same smooth 3-manifold has been substituted.

## 4. From a non-QP braid to a non-QP transverse link: clause (a)

The following two statements are needed together:

1. The transverse Markov theorem of Orevkov–Shevchishin says that two braids represent transversely isotopic links exactly when they are related by braid conjugations and positive Markov stabilizations/destabilizations. Their complete short author manuscript, including the monotone-isotopy/bad-zone proof, was read. Its title is *Markov theorem for transversal links*, JKTR 12 (2003), 905–913.
2. Orevkov's *Markov moves for quasipositive braids*, C. R. Acad. Sci. Paris I 331 (2000), 557–562, proves preservation of quasipositivity under positive **destabilization**, the nontrivial direction. The full five-page author manuscript proof was read. Positive stabilization and conjugation preserve it immediately. Hayden's published Theorem 2.2 and Remark 2.3 provide the same precise closed-braid formulation.

If T_k were transversely isotopic to any QP braid closure, this sequence would imply b_k is QP. Section 2.1 contradicts that. Consequently **every T_k, k>=0, is a counterexample to (a)** once the contact-cover bridge in Section 3 is included.

For the preferred witness k=6, the braid-level obstruction is even simpler: e(b6)=-4, whereas a product of positive-generator conjugates has nonnegative exponent sum. Thus (a) can be checked for this witness without Orevkov's reduced-standard-form obstruction, though the latter was checked to reconcile the entire published family.

Negative Markov moves must not be inserted into this argument. They preserve a smooth link type but generally change its transverse class and are not quasipositivity-preserving in the required direction.

## 5. Slice-Bennequin sharpness: explicit refutation of the twofold clause (c)

For every k,

\[
 e(b_k)=12+5-(15+k)=2-k,\qquad
 \operatorname{sl}(T_k)=e(b_k)-3=-1-k.
\]

This is the usual Bennequin braid formula, stated explicitly in Harvey–Kawamuro–Plamenevskaya (2.1) and Hayden Section 2. The permutation of (sigma1 sigma2)^6 is the identity. For even k, the remaining permutation is the product of the two adjacent transpositions, a 3-cycle; hence T_k is a knot. For odd k there are two components.

Take any **even k>=2**. For every connected smooth orientable surface F in B4 with boundary T_k,

\[
 -\chi(F)=2g(F)-1\ge-1>-1-k=\operatorname{sl}(T_k).
\]

In particular \(\operatorname{sl}(T_k)<2g_4(K_k)-1\). The Stein-fillable induced double cover is already proved. These are explicit strict slice-Bennequin counterexamples. No slice-genus calculation, concordance invariant, slice-disk obstruction, connected-link convention, or conjectural sharpness converse is needed.

For b6 the numbers are sl=-7 and \(2g_4(K_6)-1\ge-1\). The gap is at least six. This numerical consequence of the published family is authored here as scope verification; the Brejevs–Wand paper itself does not state K3 clause (c) in these words. It is not represented as a new original result or a new campaign turn.

This refutation concerns the fixed transverse representative, exactly as stated in the question. We do not infer it solely from nonquasipositivity: that would improperly invoke the still-distinct converse between slice-Bennequin sharpness and quasipositivity.

## 6. Entire smooth link-type nonquasipositivity: a separate checked argument

Non-QP of b_k alone does not prove non-QP of its smooth closure type. A smooth representative may require negative Markov moves. The following establishes the stronger conclusion for an ample explicit subfamily, including b6.

Hayden, *Minimal braid representatives of quasipositive links*, Pacific J. Math. 295(2) (2018), 421–427, Theorem 1.2, proves that any quasipositive **oriented link type** has at least one quasipositive minimal-braid-index representative. The theorem does not assert that every minimal representative is quasipositive. Its full proof in Section 3 was read: generalized Jones puts a QP representative on the right edge of the minimal-braid cone, opposite stabilizations give embedded annuli, simplification reaches the cone vertex, and all moves on the QP side are QP-preserving positive destabilizations and exchange moves.

The generalized Jones theorem, Hayden Theorem 2.1, says that if q has minimal braid index b for the same oriented link type as an n-strand braid beta, then

\[
 |e(\beta)-e(q)|\le n-b.
\]

An independent primary proof was read in LaFountain–Menasco, *Embedded annuli and Jones' conjecture*, AGT 14 (2014), 3589–3601, arXiv:1302.1247v2: full Proposition 1.1 proof and Proposition 3.2 proof. These establish the opposite-stabilization embedded-annulus statement and the nested braid cones. The theorem is about oriented link type, with one representative minimal, not about arbitrary pairs of nonminimal braids.

Suppose now the smooth oriented link type of b_k is QP, and choose Hayden's QP minimal braid q. Since b_k has three strands, \(1\le b\le3\), while \(e(q)\ge0\). For **k>=5**, \(e(b_k)=2-k\le-3\), so

\[
 |e(b_k)-e(q)|\ge3>2\ge3-b,
\]

contradicting generalized Jones. Therefore **the entire oriented smooth link type is nonquasipositive for every k>=5**. In particular the even subfamily k>=6 consists of nonquasipositive knots.

This audit does not claim that this same short bound determines smooth link-type quasipositivity for k=0,1,2,3,4. No such determination is necessary: b6 is already a single witness for (a), for the twofold version of (c), and for the stronger whole-knot-type non-QP conclusion. This explicit boundary prevents a blanket family claim from being silently inferred from a braid-level theorem.

## 7. Why this does not settle the higher-order clause (b)

The proven filling is for the cyclic double cover. Neither Brejevs–Wand's positive-genus page extensions nor the ordinary three-manifold surgery calculation produces, for T_k, a Stein-fillable cyclic n-fold contact branched cover with n>2. Extending an open-book page by 1-handles does not identify the new open book as the special cyclic lift of the same branch link at a prescribed higher degree.

Likewise, Stein fillability of a twofold contact cover does not, without further argument, provide a Stein filling for a higher branched cover. One would need the relevant branch locus and covering action to extend compatibly over a suitable filling. This extension is exactly the extra structure that cannot be assumed here. A simple noncyclic cover, a cover over a different branch link, and existence of an unrelated Stein-fillable structure on the underlying manifold would all miss the hypothesis.

Ito–Kawamuro's higher-order positive-factorization theorems have deck-symmetry/root/subsurface hypotheses, and start with positive factorizations, not arbitrary Stein fillability. They do not provide the missing implication.

A bounded fresh literature check also inspected Kegel–Nonino, arXiv:2603.25805v1, *Transverse knots determined by their cyclic branched covers*, especially Theorem 1.6 and its Section 6 proof. Its construction gives transverse n-twins, including smoothly different knots, but does not establish a common Stein-fillable cover with one branch knot QP and the other non-QP. It therefore does not settle (b). The raw PDF says 30 March 2026 while the HTML generated display says 24 August 2026 under the same v1 identifier; this audit pins and uses the raw PDF rather than treating those dates as evidence of a revised theorem.

**Disposition:** (b) is unestablished by these sources and by this audit. This is a bounded status conclusion, not an assertion that no result anywhere could settle it.

## 8. Prior source inspection and effort accounting

Earlier source-inspection records and retained public source bytes were reused, with their recorded reading boundaries, rather than downloading the full K3 book or the two Brejevs–Wand manuscript copies again.

The earlier source inspection made no proof acceptance. It had read theorem/bridge scopes, not completed this clause-by-clause transfer. An earlier blanket-open converse assessment is superseded only in the twofold and fixed-transverse-sharpness respects explained above.

This is verification of existing results, with zero new proof-search approaches. It supplies no further mathematical result under the surviving clause (b), and preparation of this edition starts no new proof-search attempt.

## 9. Evidence, inspection limits, and review boundary

`SOURCE_CATALOGUE.json` records genuine raw PDF byte counts and SHA256 values, source versions, fresh versus reused acquisition, publication status, the recorded acquisition times and public responses, and the text and pixel inspection scopes. `READING_LOG.json` distinguishes rendered-and-viewed pages from merely generated images. `STATUS.json` and `CLAUSE_DISPOSITION.json` record the current accepted clause-specific conclusions after the separate review described in ACCEPTANCE.md. The acquisition and inspection history is attributed to the original source audit; byte identities were rechecked for this edition without claiming a new source-reading pass.

The Springer DOI page failed in the web tool; no bypass of a denied source occurred. The separately public institutional page explicitly provided the published PDF, which was retrieved through that authorized public route. No final JSG publisher PDF was claimed. Some Type-3-font extraction/render warnings occurred in the old transverse-Markov source; the key proof pages were visually inspected and legible.

The complete relevant Brejevs–Wand proof and immediate imported mathematical statements/proofs were checked, with the actual induced-contact and transverse-isotopy transfer made explicit. This is a source-based mathematical audit, not formal verification or a new proof of the entire foundational contact/Floer literature. At this audit stage, separate independent review of the proof chain and elementary consequences was required before acceptance; the subsequent review is recorded in ACCEPTANCE.md.

### Recommended concise disposition after independent review

“Previously published counterexamples refute KP-1.64(a) and the twofold slice-Bennequin-sharpness implication in (c). The knot closure of (sigma1 sigma2)^6 sigma1^5 sigma2^-21 gives a Stein-fillable induced double contact cover, sl=-7, and a nonquasipositive entire smooth knot type. The some-n>2 clause (b), and any separately restricted higher-order sharpness variant, remain unresolved by this audit. Existing-result verification; no new proof-search turns.”

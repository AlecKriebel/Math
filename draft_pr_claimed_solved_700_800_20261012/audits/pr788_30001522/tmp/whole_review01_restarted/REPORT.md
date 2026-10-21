# First completed whole-preprint review, PR788 / problem30001522

Verdict: **PASS for the stated classical explanatory note; zero required repairs and zero blocking mathematical, statement, attribution, metadata or package issues found. Historical priority remains unresolved.** The accepted result is the literal fixed-space answer to the printed Hanke question, with the stronger exact rank calculation given in the manuscript. This is an adversarial mathematical assessment with reproducibility checks, not a proof-assistant certificate or an exhaustive predecessor exclusion.

This fresh review session is `whole_review01_restarted`. The earlier reviewer lost during environment restart had no terminal sealed report and is not counted as a completed review. This report does not adopt its unfinished work. No current other-shard agent was consulted. No source, release artifact, branch, Git index, tracker, external account or publication state was changed. The observed branch is `main`; the original supplied proof budget remains2/5, with zero new substantive proof-search turns. All new material stays in this review folder or its separate scratch folder.

## Independent target and evidence order

Before reading the manuscript, original candidate proof, or root/peer outcomes, I read the complete `SELECTED_PUBLIC_RECORD.json` and independently retrieved the official [OWR32/2010 PDF](https://ems.press/content/serial-article-files/46287). Printed1912 defines the two actual-space free-action ranks and asks for one finite connected complex with abelian fundamental group, trivial action on all higher homotopy groups, finite-dimensional total rational homotopy, and a strict free-p-rank/free-toral-rank gap for infinitely many primes. The fixed-space and prime quantifiers, action category, hypotheses, counterexample tests and success criteria were frozen in `INDEPENDENT_TARGET_FREEZE.json`, SHA256 `bf353fd1373ac6ba8a842ebb11820558c7a75bdbec348b261ea0f1fce1a9fce5`.

I subsequently read the entire manuscript, README, metadata, original proof and substantive historical/current mathematical and priority reports. Their verdict labels were not premises in the mathematical assessment below. The official printed question was visually checked; the complete Hanke contribution1912–1915 was read. The publisher records2March2011 publication of journal/report year2010, as the manuscript explains. The initial problem record's older status assessment is not treated as a current worldwide-open certificate.

The review binds original head `3412d5a074c3f3a03f75735a9ccf1755e172204a`, all48 immutable original files, and the closed192-file preprint source. The parent supplied the authenticated restoration commit `37d9627971b4b224aa62fcd50528cbc97bb0a8cc`; I independently checked the supplied source and release bytes against the external pins, rather than fetching that Git commit anew. Eligibility says exactly `claimed_solved`, draft PR788, original budget2/5. No other problem was reviewed.

## Mathematical claim audit

### One actual finite complex and every homotopy hypothesis

For the real-matrix closed subgroup SO(3) of SU(3), the quotient W is a closed connected smooth5-manifold. A finite smooth triangulation realizes its actual underlying space as a finite complex. Transport of actions through that homeomorphism is allowed: the printed question does not require simplicial actions preserving the chosen triangulation.

The fibration SO(3)→SU(3)→W, with π1(SU3)=π2(SU3)=0 and π1(SO3)=Z/2, gives π1(W)=0 and π2(W)=Z/2. Thus abelian π1 and its trivial integral action on every higher homotopy group hold automatically. Hurewicz gives H2(W;Z)=Z/2. Simple connectivity gives orientation. Integral Poincare duality and universal coefficients yield H0=H5=Z, H2=Z/2 and all other homology zero. In particular H3 homology is zero; H3 integral cohomology contains the Z/2. The manuscript maintains this distinction.

Rational Hurewicz applies via the torsion Serre class to the simply connected finite-type W despite its integral π2 torsion. Vanishing reduced rational homology below degree5 forces vanishing lower rational homotopy and a nonzero rational degree5 Hurewicz class. After clearing denominators it is represented by an actual sphere map S5→W. This map is an isomorphism on rational homology in every degree, so rational Whitehead gives the asserted rational homotopy equivalence. Since5 is odd, total rational homotopy is exactly one-dimensional, in degree5. The homotopy Euler characteristic is−1. No homotopy replacement is used to define W's ranks.

### Fixed circle, every odd cyclic order, and the prime-three boundary

D(z)=diag(z,z,z⁻²) is a smooth injective circle homomorphism into SU3 and acts by left multiplication on right cosets. Fixing a coset implies conjugacy of D(z) into SO3. A real orthogonal3×3 matrix of determinant1 has an unpaired real eigenvalue1. Hence a stabilizing z must satisfy z=1 or z²=1. This necessary condition is already enough to prove freeness of every odd-order finite subgroup simultaneously. The same W and embedding are fixed before the prime is chosen.

For a primitive cube root z, D(z) is scalar, but has no eigenvalue1. Thus p=3 has no hidden central kernel or fixed coset. At z=−1 the displayed matrix lies in SO3 and fixes the identity coset, so the circle is genuinely almost free rather than free. The trivial group at odd order1 causes no exception. Every higher odd prime power and every odd composite order is covered by the same proof, independently of finite sampling. The free-action restriction to odd cyclic subgroups supplies the required infinite prime set.

Yeroshkin's exact arXivv2 Proposition4.2 pp.6–7 and the conjugate SO3 embedding p.3 were independently read. Its conjugate real inclusion defines the same homogeneous-space situation; the bar over the third weight in the displayed source formula was visually checked. Specializing its weights to(1,1,−2) supplies exactly the classical isotropy used here. No new circle action is claimed.

### The tangent characteristic number is reconstructed correctly

The tangent isotropy representation is the conjugation action on i Sym₀(R3), from the Lie algebra decomposition. It is not being replaced by the standard3-dimensional associated SO3 bundle. A coordinate rotation acts as a fixed line and rotation planes of weights1 and2. Consequently the induced loop in SO5 has parity1+2=1 mod2.

The boundary π2(W)→π1(SO3) is an isomorphism. Pullback along its generator sphere therefore has the nontrivial SO5 clutching class and nonzero w2. Integral Hurewicz maps this sphere onto the generator of H2(W;Z)=Z/2; coefficient reduction remains nonzero since H1=0. Thus the sphere detects the nonzero x∈H²(W;F2), proving w2(W)=x. Its being torsion in integral homotopy does not prevent mod-two detection.

For0→Z/2→Z/4→Z/2→0, the degree2 UCT has no Ext(H1,−) term. The map is Hom(Z/2,Z/4)→Hom(Z/2,Z/2); both possible values0 and2 reduce to0. The connecting map Sq¹ is therefore nonzero on x. H³(W;F2) is one-dimensional, so Sq¹x=y. Orientation and Sq¹w2=w1w2+w3 yield w3=y. Complementary one-dimensional mod-two Poincare duality makes xy the nonzero top class, evaluating to1.

Debray–Yu's independently fetched author-hosted arXivv2 pp.20–22 agrees with every required class and attribution. Its tangent and principal-bundle classes are explicitly distinguished. The manuscript reconstructs the needed tangent number rather than assuming a principal-bundle computation implies it. This direct derivation also avoids dependence on an unread older calculation for mathematical validity.

Boundary checks include replacing Z/2 by Z/4 in the coefficient Hom calculation, where reduction becomes surjective and the same Bockstein inference fails; replacing weights1,2 by an even parity pair likewise removes the nontrivial clutching conclusion. Neither invalid replacement appears in the paper.

### Arbitrary continuous involutions and tori

The finite quotient argument covers all continuous free involutions. Every element acts by a homeomorphism. A coordinate chart small enough to be disjoint from its translate gives an evenly covered quotient chart. The quotient is compact Hausdorff, second countable and locally Euclidean of dimension5. Smoothness, local linearity, triangulability and an integral quotient orientation are unnecessary.

A local homeomorphism pulls the topological tangent microbundle back to the source tangent microbundle, by the local diagonal construction. Thom classes and Steenrod squares give natural mod-two Stiefel–Whitney classes; on the smooth W they agree with its ordinary tangent classes. Hence every wi(W) is a pullback from the quotient. Over F2, the fundamental-class pushforward of a degree-two covering is0. Every top-degree product of these classes must evaluate to0, contradicting the proved w2w3 number1.

Thus rk2(W)=0. Every positive-rank torus has an involution, and restriction of a free action to any subgroup stays free. Therefore rkT(W)=0 for arbitrary continuous torus actions. The proof never assumes a continuous circle quotient is a manifold, a free action is smoothable, or every action is homogeneous/isometric. It never borrows the admissibility hypothesis of Kuhn–Lloyd's surrounding chromatic theorem.

The lemma's degree and characteristic are material: an odd-degree cover has mod-two degree1, so this transfer argument deliberately does not obstruct the odd cyclic actions. A nonfree involution would not give the covering argument. These boundaries are respected.

### Arbitrary-action upper bound at every odd prime

For odd p, the integral homology gives precisely H⁰=H⁵=Fp and zero other fiber cohomology. An E=(Z/p)² action is trivial on each line since its automorphism group has order p−1. Thus the Borel bundle has the asserted untwisted two-row, first-quadrant Serre sequence. An arbitrary continuous action suffices for this associated bundle and spectral sequence; no cellular or homogeneous hypothesis is needed.

Only d6 connects rows5 and0. Multiplicativity, including the usual harmless grading sign, makes its bottom image exactly the principal ideal(f), f=d6(u) of total degree6. No subsequent differential can affect that bottom row. The quotient by exterior generators is a genuine surjection R/(f)→Fp[t1,t2]/(f̄), even when f has exterior terms or is a zero-divisor in R. It assumes neither f≠0 nor f̄≠0.

If f̄=0, the target is the polynomial ring. If nonzero it is a homogeneous binary cubic. Multiplication by it injects ordinary degree m−3 into degree m over every field; quotient dimension is(m+1)−(m−2)=3 for m≥3. This holds also at p=3 and for reducible cubics. The target, and hence the bottom row, has unbounded nonzero total degrees. The finite first-quadrant filtration in each total degree excludes a convergence loophole. Additive or multiplicative extensions cannot erase a nonzero associated-graded group.

Freeness makes W→W/E a principal finite covering and W/E a closed topological5-manifold. The Borel map to W/E is a numerable associated bundle with contractible fiber EE, hence a homotopy equivalence (a cohomology equivalence would already suffice). Singular cohomology of this paracompact5-manifold vanishes above5 without a triangulation assumption. This contradicts the bottom row. Restriction excludes every rank≥2 elementary abelian group. Together with the explicit cyclic action, rkp(W)=1 for every odd p.

At p=2, extra fiber rows invalidate this two-row argument; the manuscript treats2 separately. With just one polynomial variable a nonzero cubic quotient is finite-dimensional, so the argument does not falsely exclude the actual rank-one actions. There is no unsupported compactness/convergence of finite group actions to a torus, and no equivalent hidden central problem is substituted for the proved obstruction.

## Attribution, exact versions and novelty limits

The official OWR question, specified Debray–Yu author body, Yeroshkinv2, Kuhn–Lloydv1/v2, Mundetv1 and paginated version of record, and CWYv3 were independently retrieved. Read scopes, hashes and actual access failures are recorded in `SOURCE_READ_LEDGER.json`. These are targeted body reads, not whole-paper re-proofs of every chromatic/surgery/rigidity result.

Kuhn–Lloydv1 Theorem9.1 p.27 explicitly uses Wu's nonbounding property to rule out a free involution. V2 Example2.25 p.12 retains it while the surrounding fixed-set assertions explicitly discuss admissibility. The paper credits this old obstruction and gives its own continuous-category proof. The original48-file audit lemma already cited Kuhn–Lloyd; the current paper does not falsely claim that citation was absent from the entire original candidate.

Mundet's2021v1 Theorem1.14 p.7 and Section15, and the journal Theorem1.11 printed806 and full Section13 printed833–836, confirm regular self-covers of every odd degree. The cover is pulled back from the degree-d circle cover, so its deck group is cyclic, not merely an unspecified order-d group. For every odd prime it supplies an actual free Cp action on the same underlying CWY example, and CWY excludes continuous circle actions. This is an earlier free finite-versus-circle gap, as the manuscript, README and public metadata all now say.

CWYv3 p.8 gives π1(T(h))=π1(V)⋊Z and a centerless kernel π1(V). It is nontrivial, for example because the stated noninner monodromy of order2 cannot occur for the trivial group. A nontrivial centerless group is nonabelian; the semidirect product and any product with H retain it as a subgroup. The examples therefore fail Hanke's abelian π1 hypothesis, independent of assumptions about H's dimension or presence. Dismissing them merely by an effective-versus-free distinction would be wrong; the present artifacts make the correct distinction throughout.

Publisher-deposited Crossref metadata independently confirms the Debray–Yu, Yeroshkin, Mundet and CWY journal fields. The official EMS landing page and exact Kuhn–Lloyd PDF versions supply the other bibliographic checks. The Mundet online2024 and volume2026 dates coexist. The specified2025 Debray–Yu body is later than its2024 journal article, and the manuscript explicitly uses that body's locators. CWY's journal PDF and DOI page returned403; exact arXivv3 body plus publisher-deposited bibliographic metadata are the evidence actually read here. Journal/preprint byte equality is not established.

There is one optional precision observation, **O1**, not a required repair: Debray–Yu's PDF has arXivv2 margin/header22July2025 and an internal Date line23July2025. The manuscript's22July version label unambiguously identifies the arXiv version, and all cited locators/content match. If editing later, spelling this as “arXivv2, header22July2025; internal date23July2025” would preserve both dates. The similarly different internal Date on Mundetv1 does not change its10December2021 submission label. These are version/date distinctions, not priority reversals or mathematical defects.

This session did not rerun every historical priority search, independently read all older books/theses/originals, or prove completeness of an index. The bounded negative predecessor finding is properly qualified. The title, abstract, body, README and both metadata/deposit representations claim neither firstness nor a new manifold/action/ingredient, certified novelty, an absence theorem, or current worldwide-open status. The explanatory classical-note framing and unresolved-priority language are supported. The proof does not by itself meet a stronger goal of certifying a novel mathematical contribution; the paper does not claim to do so.

## Reproducibility, custody and all six release files

Source MANIFEST SHA256 is `bdfe29cd2a46d035cda5d83a101775283125c17b1f432b0f0f0994b5ba0819ff` for192 files including itself. Its closed inventory authenticates all original48 Git-blob/SHA256 identities and the expanded authored source; that is distinct from third-party-body custody. PDF SHA256 is `5fba96718011f0b080ff49d8471b6cf2f0b0a0aad3dd74272065f13d10483284` and TeX SHA256 is `9f871713cb010b18612e7135d17f1a1090838f94e1c9e2fc6c17ee95399bd2a7`.

The exact six files from `PACKAGE_INVENTORY.json` are:

| File | Bytes | SHA256 |
|---|---:|---|
| paper.tex |14088|9f871713cb010b18612e7135d17f1a1090838f94e1c9e2fc6c17ee95399bd2a7|
| output/pdf/paper.pdf |82411|5fba96718011f0b080ff49d8471b6cf2f0b0a0aad3dd74272065f13d10483284|
| source-and-verification.zip |401565|f51350c5d744ec1ed90e95cbab1d17fc79e8a1f9bb4221513f2d120a2192d0db|
| zenodo-deposit.json |5581|80a911845ae7c969d05abb23a634e03fc58b7abe03d6deeec3da79165bda96e3|
| zenodo-metadata.json |5385|c4e0ea6f03a9b34fa65b342850026c71c5e3c3869a8a1b18fa0cb551a006948c|
| zenodo-upload-kit.zip |461672|6d5b1d3b579d65cb971ca9b9f2dedb4ca14c780a1bd92ebccc2b412cdeedfad9|

Both Python3.14.6 and bundled3.12.14 rebuilt all six byte for byte in independent scratch outputs. The original source was unchanged. This is deterministic packaging with the exact PDF as input; a newly typeset PDF need not have identical timestamps/bytes, as the README correctly states. No fresh TeX compilation was needed to test that limited packaging claim. Source ZIP contents, ZIP safety/CRC and original nested authored archives were inspected; no full third-party PDFs/text renders were found in the nested ZIP members inspected. The upload kit/deposit names and metadata are coherent and specify only paper.pdf plus source-and-verification.zip for upload.

The portable source checker passed `--replay` under both interpreters. Each run verifies183 authored input bindings and ten normal/optimized replay processes. It records76 external evidence bindings but **zero historical external files rehashed** and `primary_body_custody_replayed=false`. This review did not restore that entire76-file bank and does not claim its optional custody replay. Historical path-bound programs and RAM-location receipts are preserved records; core remapping authenticates their authored inputs without pretending to run omitted primary-body checks. Current staging is ordinary APFS.

This session independently obtained8 primary PDFs and extracted texts for the exact reads above. Its optional fresh-evidence ledger binds23 files:8 PDFs,8 texts and7 selected primary-page renders. These fresh files stay outside this flat authored packet. Optional `--primary-root` in this review's checker verifies precisely those23 fresh files, not the historical76. Core review verification requires no third-party bodies.

Every source file was authenticated. A separate structural scan parsed114 JSON files with duplicate-key/nonfinite rejection, parsed32 Python ASTs and checked4 nested authored ZIPs. `SUPPORTING_MATERIAL_REVIEW_SCOPE.json` distinguishes full substantive reads from structural/integrity inspection; it does not claim line-by-line mathematical reading of every192-file receipt and script. Historical acceptance records are preserved and not promoted to formal proof certification.

New independent finite diagnostics check5 exact tangent commutators, parity, coefficient-reduction boundaries,523776 nonidentity residues across cyclic orders1–1024, and7856 exact multiplication matrices for all3104 nonzero binary cubics over F3,F5,F7 in specified degrees. These are model/algebra diagnostics only. They do not prove the topology or an infinite-prime quantifier by extrapolation. The universal statements rest on the explicit arguments above.

Eighteen source integrity controls passed in normal/optimized modes on temporary copies: relocated positives and wrong external pin, altered original proof, altered PDF, extra/missing source member, source symlink, altered executable helper, and unavailable historical bodies. The last rejection is useful evidence that missing-body custody cannot silently pass. The new review checker has additional independently run packet corruption controls described in its receipt. All external pins must come from outside the checked archive; a self-contained manifest cannot authenticate its own replacement.

## Visual review and final scope

All4 exact frozen PDF pages were viewed with `view_image`. Independent Poppler rendering at scale1250 produced byte-identical images to the provided page1–4 PNGs, binding that visual inspection to the exact PDF. Typography, equations, theorem, references, authorship/ORCID, date/version, page numbers and paragraph continuations are legible, with no clipped text, overlaps, blank pages or missing glyphs. The source and rendered claims agree. The unrefereed/AI-use/CC-BY statements appear in the manuscript and metadata with appropriate limits.

No required action remains for this review. The strongest verified claim is the full fixed-Wu-manifold theorem and its literal answer to the printed existence problem. No novel-result, historical firstness, complete source-body recovery, external human peer-review or proof-assistant certification is inferred. The optional date observation and all access/read limits are retained for the next reviewer.

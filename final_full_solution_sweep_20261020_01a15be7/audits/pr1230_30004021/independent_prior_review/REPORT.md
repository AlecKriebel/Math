# Independent full prior-result audit: PR #1230 / 30004021 / OWR-16635-009

**Verdict: ACCEPT the exact affirmative prior result with explicit established-theorem imports.** The two simple graded W-algebra quotients over C are both conformally isomorphic to L_{−4/3}(sl2), for standard Dynkin conformal vectors, with central charge −6. No unresolved specialization-specific gap or theorem repair was found. This internal AI review is independent of the older packet and its finite checker. It is not a claim of external human peer review, proof-assistant certification, new authorship or historical firstness. Review family 100% (closed after final custody replay); overall sweep estimate 79%.

All new work is confined to this review directory. Closed PR1219 artifacts and seals were preserved. No service write, Git ref/index/cursor change, upload, communication with people or accounting completion occurred. Root must read and adopt the full report and exact proposal before any later authorized action.

## 1. Fresh capture, duplicate clearance and primary identities

Before mathematical inspection, I made my own GWS CLI read-only numeric-grid request for spreadsheet `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, gid 1254632077, all 43 columns A:AQ. It returned 191 rows including the header. Full private raw response is pinned by GWS_CLEARANCE.json, SHA-256 `fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1`. Exact problem/PR/DOI/arXiv/author/title/original-report and equivalent W-algebra/vertex-algebra/collapsing/central-charge searches found no lead. Generic “nilpotent” hits 75 and 149 concern deformation functors and component-group cellularization, respectively, and are unrelated. Problem/description semantics were reviewed across the 191 rows. This clears current tracker leads, not worldwide priority. Exact four literal cells are in LITERAL_FOUR_CELL_PROPOSAL.json; B is intentionally empty; nothing has been appended.

Fresh read-only GitHub capture binds OPEN/draft head `92652a37a6f0508ea34a0e8b14a7722c7d99530a`, base `4b27092a448d53b61408355ce44ec38d103a1ce4`. Every one of the 8 added remote blobs was fetched at that head and independently checked by Git blob SHA and SHA-256. The entire body and all 8 files were read. There is no QUEUE edit. PR_BINDING.json records exact lengths, paths and hashes, including PROOF.md (12,404 bytes) SHA `b4a285860f3f510daefaf9d2a1e6668be1c7af39b5d2b33d9c70d47a48625410`, AUDIT.md (10,291 bytes) SHA `d364d38c4a615c11e378bf192cd32fd13446e6ef9d88804aa3bfa7e70a092dcb` and ACCEPTANCE.json (2,352 bytes) SHA `2d805b4ab1641bfc82dd8254334c42654bf4e466fb6602fdf47dc88681218aa7`. All 7 public manifest payload entries agree; the body separately pins the manifest itself.

I independently fetched these primary bodies:

| Source | Bytes | SHA-256 |
|---|---:|---|
| Original OWR 52/2018 EMS PDF |756,610|b33ed36eaa470877bc6cfb5b45b1019564f568925ea9d94e8dc7ee355879976e|
| AVM arXiv:2102.13462v3 PDF |821,728|2349653f92ebfa2499ad28e82aaba943ddca51b9da95b2231fb052692cc64cfc|
| Published Forum Math. Sigma PDF |2,001,476|882e6fc9af404f7d5c1c5816e24c0b046753b394c4f7a899f301903df0b0726f|
| Crossref record |14,549|b88222829783bfbaef3b9f17d57af56ca9e8270b14e3cba03bab937835ef1e81|

The [journal DOI](https://doi.org/10.1017/fms.2024.81) freshly returned HTTP 200 and resolved to Cambridge’s exact article. Crossref identifies Tomoyuki Arakawa, Jethro van Ekeren and Anne Moreau, the exact title, Forum of Mathematics, Sigma 12 (2024), article e95, and online publication 8 November 2024. The published first page gives accepted 26 July 2024. The [current arXiv record](https://arxiv.org/abs/2102.13462) lists v3 dated 21 February 2023, prior versions v1/v2, and the same journal DOI/reference. The relevant theorem and proof were compared between v3 and the actual journal PDF; they match in mathematical content, with the second proof part on v3 p.47 and journal p.48. No complete 92-page textual or byte-equivalence audit is claimed.

The whole PDFs were retrieved, but relevant proof inspection is bounded: original PDF 41–43 (printed 3121–3123); published definitions/context 6–16,18–30,34–36,40–41,43–44 and full target theorem/proof 46–48, plus relevant bibliography 90–92. The principal-input statement in Proposition 3.7 and its Kac–Wakimoto attribution were read; no recursive audit of the original affine character papers was performed. Published 19,46,48 and original 41,43 were visually inspected. The v3 counterpart 46–48 was read for theorem/version correspondence. This is not an all 92-page proof audit or an audit of unrelated tables/examples.

## 2. Exact original question and theorem scope

The [original Moreau contribution](https://ems.press/content/serial-article-files/46773?nt=1#page=43), joint with Arakawa, defines universal W^k and simple quotient W_k on printed 3121. Printed 3123 conjectures W_{−7+7/3}(sl7,f_(3,2,2))≅W_{−4+4/3}(sl4,f_(2,2)). The subscripts and partitions were independently read visually. Replacing these by universal W-algebras would change the question and would be false: their Slodowy slices have dimensions 18 and 7.

The published AVM Theorem 8.8(2), p.46, covers f of partition (q^m,(q−1)^2), with n=q*mtilde+stilde, stilde=q−2, m=mtilde−1, and admissible k=−n+p/q. At p=n it identifies the simple quotient with L_{−2+2/q}(sl2). For q=3 the two instances are:

|n,p,q|k|mtilde,stilde,m|chosen partition|dense associated partition|
|---|---|---|---|---|
|7,7,3|−14/3|2,1,1|(3,2,2)|(3,3,1)|
|4,4,3|−8/3|1,1,0|(2,2)|(3,1)|

Both gcds with 3 are 1; p=n meets the type A admissibility bound p≥h∨=n. All ambient and residual levels are noncritical. The correct condition is f∈overline(O_k), visibly printed in the journal statement/proof. Dominance gives (3,2,2)<(3,3,1) and (2,2)<(3,1). Neither chosen f lies in the dense associated orbit. Consequently the nonzero-reduction cover is available, whereas a dense-orbit/lisse argument would misapply the hypothesis.

The m=0 boundary must be treated honestly. The table’s generic C×sl_m×sl2 expression and its necessity argument through a scalar level cannot be read literally for (2,2). The actual centralizer is exactly sl2. The affirmative result required here is independently reconstructed below using only that factor and Theorem 3.10. No claim about the entire general “if and only if” necessity proof is needed. Likewise Conjecture 8.11 literally has 1<m although its following paragraph names an m=1 example; this conjecture is not a premise anywhere in this audit.

## 3. Independent structural route, not numerical inference

Let V_n be the simple W quotient at the stated level/partition and let Vtilde_n=H^0_DS,f(L_k(sl_n)). The actual published Theorems 3.2 and 4.3 say the associated variety is the nilpotent orbit closure and the reduction is nonzero precisely when f lies in it. The standard exact quotient construction then gives a graded, conformal surjection Vtilde_n→V_n. L_k(sl_n) is a finitely generated object of KL_k, so Theorem 4.3’s ordinary/vanishing hypotheses apply. No general conjecture asserting reduction simplicity is required.

In Dynkin grading, the PBW construction gives positive generating weights and vacuum-only degree 0, hence conical grading with finite pieces. Proposition 4.2 supplies self-duality. Its proof reduces to the trace condition for the triple centralizer; semisimple-factor traces vanish and the extra seven-dimensional center’s trace vanishes, also checked directly below. For n=4 there is no center. These facts are established before any affine-map conformality conclusion.

Decompose the defining triple modules as E3⊕(E2⊗C²) and E2⊗C². Their trace-zero multiplicity centralizers are C⊕sl2 and sl2. The sl2 multiplicity matrix units provide genuine Lie algebra embeddings. Applying the standard corrected-current construction (published (32),(34), not a guessed map from numerical invariants) yields homomorphisms

    V^{−4/3}(sl2) → W^{k_n}(sl_n,f_n) → V_n.

For explicit diagonal data, choose

    x7=(1,1/2,1/2,0,−1/2,−1/2,−1), t7=(0,1,−1,0,1,−1,0),
    x4=(1/2,1/2,−1/2,−1/2),          t4=(1,−1,1,−1).

These are derived from independently constructed rational sl2 triples, not merely entered as root counts. The checker verifies all commutators and explicitly constructs the multiplicity sl2 raising/lowering matrices centralizing the triple. Solving simultaneous commutator equations independently verifies centralizer dimensions 4/3 and centers 1/0.

The ambient normalized form is trace, Tr(t²)=4, whereas the normalized sl2 Cartan norm is 2. The induced current form is

    phi(t,t)=k Tr(t²)+(Tr_g(ad t)²−Tr_g0(ad t)²−Tr_g1/2(ad t)²)/2.

Complete matrix-unit summation gives trace triples (56,16,8) and (32,16,0). Dividing phi(t,t) by 2 yields respectively 2k+8=−4/3 and 2k+4=−4/3. The nonzero level also prevents all currents from disappearing in the unital simple quotient. For n=7 the center vector z=(4,−3,−3,4,−3,−3,4) has Tr(z²)=84, trace triple (1176,0,392), and form 84(−14/3)+(1176−392)/2=0. Its positive-degree adjoint trace and Tr(xz) both vanish. No scalar factor is invented at n=4.

The affine Sugawara vector is weight 2 and killed by L1=(omega_V)_(2), as required by published (35)/Theorem 3.10. One can check this on the sl2 factor alone: its currents are weight 1; self-duality and vacuum-only degree 0 force L1 of a current to vanish because the invariant pairing pairs it with L_(−1)vacuum=0. Applying L1 to the quadratic Sugawara vector leaves the contraction sum of brackets of dual current bases, which is zero by invariance. The denominator ell+h∨=2/3 is nonzero. This uses no Sugawara vector for a zero-level abelian algebra and does not assume the map is already conformal.

The actual published criterion is Theorem 3.10, pp.19–20: an admissible affine map into a conical self-dual conformal V, with those Sugawara conditions, and a surjective cover admitting w=0 and matching growth, factors through a finite simple-affine extension. If the cover also has the vacuum asymptotic dimension, it is exactly L_ell(g). All these structural premises, not simply c/g/A equality, are necessary in the present proof.

Its written proof was inspected. Proposition 2.9 first proves conformality from growth via the coset Virasoro vector; the c=0 radical case is treated separately, rather than assuming c=0 forces a trivial coset. Theorem 3.5 then uses self-duality and the generating affine singular vector, together with Lemma 3.6’s projective-cover/Casimir multiplicity bound, to descend through the maximal affine ideal. Theorem 3.3 supplies complete reducibility. Corollary 3.9 supplies positive asymptotic dimensions of ordinary constituents; the vacuum constituent is present once, and the cover bounds the total asymptotic dimension from above. Equality with the vacuum leaves no extra constituent. These steps make the isomorphism deduction substantive; they are not consequences of a numerical match in isolation.

## 4. Independent exact asymptotics and conformal checks

Proposition 4.10(1) applies to the ambient principal-admissible vacuum module and our nonzero reductions. It gives w=0 and

    g_Vtilde=dim(sl_n^f)−n(n²−1)/(pq).

The transposed chosen partitions are (3,3,1) and (2,2); their squared-column sums minus 1 give 18 and 7. Independent rational commutator nullspaces confirm both dimensions. Thus 18−48/3=2 and 7−15/3=2.

For asymptotic dimension, at p=n the finite Weyl sine product cancels the n-dependent lattice factor. The identity Π_(d=1)^(n−1)(2sin(pi*d/n))^(n−d)=n^(n/2) follows exactly by pairing d and n−d, squaring, and using Π_(d=1)^(n−1)2sin(pi*d/n)=n from the roots-of-unity factorization at 1. All factors are positive. Since |P/Q|=n for type A, |P/(nq)Q|^(1/2)=n^(n/2)q^((n−1)/2). The surviving expression is

    A_Vtilde = Π_(alpha>0,grade>0)2sin(pi*grade/3)
               / [2^(r_half/2) 3^(r0+(n−1)/2)].

Every positive root e_i−e_j was independently enumerated; the exact counts are:

|case|grade0|grade1/2|grade1|grade3/2|grade2|total|
|---|---:|---:|---:|---:|---:|---:|
|sl7,(3,2,2)|2|8|6|4|1|21|
|sl4,(2,2)|2|0|4|0|0|6|

The four nonzero sine factors are exactly 1,sqrt3,2,sqrt3. For sl7 the numerator is 16*3^(7/2), denominator 16*3^5; for sl4 they are 9 and 3^(7/2). Both give 3^(−3/2)=sqrt3/9. The checker evaluates these in Q(sqrt3), with no floating trigonometry. Direct left-adjusted-pyramid counts (6,12,3) and (2,4,0) give the same dimension. This independently supplies the omitted case-specific calculation in Lemma 8.6’s “similar arguments” sentence and avoids importing a grading-independence claim without checking the Dynkin instance. In particular the half-integral Dynkin grading for sl7 is retained consistently with self-duality.

For the residual affine sl2 level −4/3=−2+2/3, Corollary 3.9 gives w=0, g=(1−2/6)*3=2 and A=2/(3*sqrt12)=3^(−3/2). Thus all structural and asymptotic premises of Theorem 3.10 hold for each target, giving

    W_{−14/3}(sl7,f_(3,2,2)) ≅ L_{−4/3}(sl2) ≅ W_{−8/3}(sl4,f_(2,2)).

Conformality comes from the criterion, not a postulated match of central charges. Independently, published (21) gives c=dim g0−dim g1/2/2−12|rho−(k+n)x|²/(k+n). The data (dim g0,dim g1/2,shift-square) are (10,8,7/3) and (7,0,13/9), giving −6 in each case. The affine charge is 3(−4/3)/(2/3)=−6. Universal W-algebra slice dimensions 18≠7 reject a universal-algebra reinterpretation.

## 5. Exact import and verification boundary

Named established inputs are used with their actual hypotheses checked; their original proofs are not recursively certified:

- W construction/PBW/current formulas: Kac–Roan–Wakimoto [57], Kac–Wakimoto [60], De Sole–Kac [31/34]; AVM pp.21–22 and 27–28. The Dynkin grading and noncritical parameters are explicit.
- Associated varieties, nonvanishing and exact reduction: Arakawa [10], AVM Theorems 3.2/4.3 and type A formula (45); the proper orbit-closure inclusions and KL_k vacuum-module scope were checked.
- Dynkin self-duality: Arakawa–van Ekeren [14], as used in AVM Proposition 4.2 and Lemma 5.5; the trace condition and exact centralizers were checked.
- Admissibility/ordinary complete reducibility and principal affine character asymptotics: Arakawa [8], Kac–Wakimoto [59,61], Kac’s Infinite-Dimensional Lie Algebras [54]; AVM (9),3.3,3.7,3.9 and 4.9–4.10. Numerators 7,4,2 and denominator 3 meet each criterion; the vacuum weight and root products are explicit.
- Structural conformality/descent: AVM Proposition 2.9, Theorems 3.5/3.10 and Lemma 3.6. Their written proofs and usage were read. Underlying Virasoro structure/asymptotics [43,58], coset result Lepowsky–Li [67], Kac–Kazhdan [55], Arakawa–Fiebig [16] and primitive-vector multiplicities Moody–Pianzola [72] remain named imports. This is not a finite-computation proof of projective-cover theory or affine character formulas.

The source bibliography identities were independently read. Neither Allegra’s thesis, row/column-removal results, Conjectures 4.4/8.11, full reduction simplicity, nor W-algebra rationality is a missing premise: the quotient cover and Theorem 3.10 suffice. No new general collapsing family is established here.

check_independent.py is newly written, dependency-free and read-only. It constructs rational triples and multiplicity sl2 matrices, solves actual commutator nullspaces, enumerates every root, computes trace forms, exact Q(sqrt3) products, orbit dominance, admissibility, growth and charges, and validates captured PR/source/tracker pins. Deliberate false dense-orbit membership, a spurious m=0 scalar, omission of half-degree trace/sine terms and universal-W equality are rejected. Finite checks support only these finite applications and custody; the imported VOA results are not machine-proved. No source-author program was executed.

The public arXiv support endpoint returns a 94,790-byte gzip containing a single 381,477-byte TeX source, not a tar archive. It was decompressed and read as text only. No separate code/data package was identified for this analytic type A result. GAP4 references in the paper concern exceptional-type tables outside this pair. The exact DOI HTML body is retained compressed to save disk, with both raw and stored hashes in PRIMARY_RECEIPT.json.

Historical assertions in the PR about authentication of 25 old audit members and prior checker outputs were read as metadata; those older private bodies were not reacquired or their old checker rerun. This fresh acceptance rests on the actual original question, actual published theorem/structural route, exact current eight blobs and new independent finite checks. It does not certify every historical preparation claim.

## 6. Credit, dates and proposed accounting

AVM’s published p.48 explicitly credits Francesco Allegra for the n=7,q=3,s=4 example and names partition (3,2²). Their bibliography [6] says 2019. The [Sapienza catalog](https://iris.uniroma1.it/handle/11573/1344407) separately reports a defense date 11 February 2020 and no attached files. Both facts were freshly checked; the dates are not interchanged, and no thesis theorem or proof is claimed as inspected. The catalog is attribution/context evidence, not the proof dependency.

ALIASES_AND_CLEARANCE.json records target IDs, EMS/report DOI variants, the exact journal DOI and Cambridge identifiers, the same-paper bare arXiv ID 2102.13462 plus version aliases, and separate Allegra thesis/catalog identifiers. v1/v2 are metadata aliases only; their actual proofs were not read. The exact A:D proposal uses the existing journal DOI, B empty, AVM authorship plus Allegra’s earlier-example attribution, the simple-quotient/Dynkin/C scope, the complete structural proof boundary, and AI attribution limited to this internal review. It makes no new upload, project-authorship, exhaustive-priority or independent external human peer-review claim.

Root must read the full report, proposal, alias clearance and checker outputs and explicitly adopt them before later accounting. A future action needs fresh state/duplicate guards; the present review remains read-only and accounting incomplete.

# PR1281 / 30004145 — independent original/prior review01

Accept the full original nine-point plane M-cubic component-fundamental-group dichotomy, with the complete genus-one proof supplied in the pinned PR independently verified. The exact cubic answer is already explicitly stated by Oleg Viro in *Round dances of points on a curve*, printed p.1289 of the published Oberwolfach report. Recommend an existing-publication row identifying that actual source statement through DOI10.4171/OWR/2019/21. No new publication, novelty, first-resolution or invented separate proof-paper identity is warranted.

This is an AI-assisted independent internal audit, not conventional external human review, referee certification or proof-assistant verification. No people, other agents or chats were contacted. No source-author code was executed. No credentials, service writes, CASE/cursor changes, Git/index/ref/worktree mutations or uploads occurred. The only network operations were uncredentialed public primary-source reads. Root adoption and publication readiness remain false. Own review completion100%; overall research goal80%.

## Exact input and source identity

Head `f76be6cc96afc990dfe894b117681cdac95ff10f` contains the seven actual attempt files listed in `INPUT_BINDING.json`. They were copied from already present immutable Git objects, with independent Git blob SHA1 and SHA256/size checks. All seven files were fully read: PROOF, AUDIT_REPORT, SOURCE_MANIFEST, AUDIT_MANIFEST, ACCEPTANCE_BINDING, README and PUBLICATION_MANIFEST. Their manifests agree with the copied payloads. No QUEUE path is among these files. The 12,644-byte proof has SHA256 `5abae18f46bdd010b72f0824d549d3043bf97aafeaef1733ec3581a95de0c751`.

The original catalog identity is30004145 / OWR-16933-007. [Viro's primary contribution](https://ems.press/content/serial-article-files/46800#page=45), pp.1288–1289 / PDF44–45, defines Emb(A,X) using simple real divisors that remain in one linear-equivalence class. Here simple means reduced with distinct support points; all support points lie on the real curve. Despite its notation, the object is a space of unordered divisors, not an arbitrary labelled embedding space or a parameter space of chosen equations for the second cubic.

The specific warm-up target is a nonsingular projective real M-cubic X, d=9, and a transverse totally real intersection divisor A cut by another cubic. It asks whether the fundamental group of the component based at A is trivial and how the answer depends on the support distribution. The source immediately gives the answer: support on one real component gives trivial fundamental group; support meeting both gives the infinite cyclic group. These are the exact original cases, not a replacement problem in higher genus or the larger real symmetric-product locus containing conjugate pairs.

The same contribution has broader questions about general curves and trace homomorphisms, and a separate §3 theorem concerning the larger real part of a complete linear system. Those are distinct from the specific component-pi1 target. This review does not claim a full higher-genus or general trace-theorem audit. The source's wording credits Ayşegül Öztürkalan for initial examples and observations leading to the cubic picture. It does not identify her as the sole author of a general theorem or as author of the full covering-space proof supplied in this PR.

## Fresh publication authentication

At 2026-10-22 10:03UTC, the actual [EMS PDF](https://ems.press/content/serial-article-files/46800) returned HTTP200,626,191bytes, SHA256 `bc813c4ac357dda41371e3309349b8cb07b01879994657cff3d9f0680647b90d`. It exactly matches the submitted source pin. Both contribution pages were freshly extracted and visually inspected, including title/byline, complete definition, exact cubic dichotomy, attribution, larger-space distinction and displayed trace lemmas. The contribution is short and was read in full; this is not a claim to audit all64pages of the report.

The [publisher record](https://ems.press/journals/owr/articles/16933), the [DOI resolution](https://doi.org/10.4171/OWR/2019/21), and the [Crossref primary deposit](https://api.crossref.org/works/10.4171/OWR/2019/21) were freshly retrieved successfully. DOI resolution leads to the actual publisher record. The bibliographic container is *Tropical Geometry: new directions*, Oberwolfach Reports16(2019),no.2,pp.1245–1308. The report's bibliographic byline lists Ilia Itenberg, Hannah Markwig, Grigory Mikhalkin and Eugenii Shustin; the actual embedded contribution carries Oleg Viro's byline and title. The DOI belongs to the containing report. It is not a newly discovered separate DOI for a Viro/Öztürkalan full-proof paper.

A minor metadata discrepancy is preserved: EMS explicitly gives publication4June2020; the current Crossref deposit gives print publication3June2020. Both differ from the volume's2019bibliographic year. The review does not silently reconcile the one-day difference or claim an exact universal release timestamp. This has no bearing on the prior printed cubic statement or the mathematics. The proposed row uses the bibliographic report identity without asserting a disputed day.

The primary source already contains the full original answer as an explicit result statement. It supplies short trace lemmas but does not print the detailed covering/slice/equal-spacing proof audited here. The correct accounting distinction is therefore: existing published target statement, plus a complete independently checked internal verification. One must neither dismiss the DOI merely because it is also the original source nor describe that report as containing the full PR proof or a separately authored general theorem.

`SOURCE_REVIEW.json` records exact source bodies, read scope, primary metadata and accepted standard inputs. Bounded searches located the same primary report and related talk announcements, without establishing an exhaustive publication history. No historical-firstness claim follows. Source PDFs, extractions, landing pages, Crossref metadata and rendered evidence are retained only as private local review evidence; no source-body redistribution is authorized here.

## Independent proof review

Let E be a smooth projective geometrically connected real genus-one curve with real points. Fix a reduced effective totally real divisor A of positive degree d. Let C1,…,Ck be precisely its occupied real components, with exact positive counts m1,…,mk. Work in A's fixed divisor class and retain these counts. The claimed space F_A consists of unordered reduced totally real divisors with that distribution and class.

**Algebra and real descent.** Choose a real origin O. Riemann–Roch gives a unique effective point for each degree-one line bundle: the canonical bundle is trivial and a negative-degree inverse has no sections. Tensoring a degree-zero line bundle with O(O) identifies Pic0 with E. With the usual holomorphic Abel map and elliptic group law, two degree-d effective divisors are linearly equivalent exactly when their elliptic sums coincide. These are standard genus-one inputs, with the needed Riemann–Roch mechanism explicitly provided. A bare unsupported higher-genus Abel-fiber claim is not substituted.

There is no hidden extra real-equivalence obstruction for these real divisors. If D−A=div(f) overC, conjugation preserves that divisor, so c=bar(f)/f is a nonzero constant on the projective connected curve. Conjugating again gives c bar(c)=1. Choose λ with λ/bar(λ)=c. Then bar(λf)=bar(λ)c f=λf, so λf is a real rational function with the same divisor. Conversely, real equivalence implies complex equivalence. Thus the complex elliptic-sum criterion describes the required real class as well. The scalar's direction is essential and is checked explicitly.

**Topological space.** A fixed-distribution reduced real configuration is a product B=∏UConf_{m_i}(C_i). Disjoint small arcs around support points give the local product charts, so no point labels are retained. Component counts are locally constant, hence each distribution is open and closed in the reduced totally real configuration space. The zero-divisor map from the complex projective complete linear system to Sym^d(E(C)) is continuous and injective, with image exactly the effective fixed-class locus. A pair of sections with the same zero divisor differs by a constant. Compact source and Hausdorff target make this map a homeomorphism onto its image. Restriction gives the same topology on F_A. No extra section-scaling circle or labelling factor occurs. Real descent also identifies the real fixed-class interpretation without introducing nonreal conjugate pairs.

**Component offsets.** The compact connected one-dimensional identity group E(R)^0 is a circle. Fix one Lie-group isomorphism φ:R/Z→E(R)^0 and choose b_i∈C_i. Every point on C_i is uniquely b_i+φ(t). A divisor of the chosen distribution has elliptic sum

\[
\sum_i m_i b_i+\phi\!\left(\sum_{i,j}t_{i,j}\pmod1\right).
\]

The first term is fixed, including every contribution from a nonidentity coset. A has the same offset. Consequently its fixed divisor class becomes the single circle equation ∑t_{i,j}=α mod1. This uses neither a global splitting of E(R) nor an arbitrary independent orientation for each circle. Dropping the fixed-count assumption would invalidate the offset cancellation.

**Actual unordered-circle universal cover.** For m≥1 define

\[
U_m=\{x\in\mathbb R^m:x_1<\cdots<x_m<x_1+1\}.
\]

For m=1 this isR. It is nonempty open convex. Reducing coordinates modulo1 and forgetting order maps it onto UConf_m(S1). The affine map

\[
T_m(x_1,\ldots,x_m)=(x_2,\ldots,x_m,x_1+1)
\]

preserves the set and residues. Every lift of one configuration is an m-term window in the same bi-infinite increasing sequence of real lifts, so all lifts are uniquely T_m^n x. Importantly,

\[
T_m^m x=x+(1,\ldots,1),\qquad s_m(T_mx)=s_m(x)+1.
\]

One cyclic turn changes the sum by1, not m. Full simultaneous rotation by one unit is T_m^m, a different loop. Weighting a deck generator by the count would compute the wrong fiber components and kernel.

This is a covering map, beyond just a description of fibers. For a base configuration choose disjoint small arcs and a cut outside those arcs. Configurations with one point in each arc have a unique ordered real-lift chart for each cyclic starting point/integer height. Its complete inverse image is the disjoint union of T_m^n translates, each mapping homeomorphically to that neighborhood. Thus U_m is a universal cover, with full deck groupZ. The action is free because the sum changes by n. It remains free at evenly spaced configurations: equality of unordered residues is not equality of real lift tuples. Compact-set sums bound n, proving proper discontinuity together with the local disjoint-sheet charts.

**Slice and quotient topology.** Take U=∏U_{m_i}, G=Z^k, and total real sum s=∑s_i. G acts blockwise, with s_i(zx)=s_i(x)+z_i and s(zx)=s(x)+∑z_i. If c lifts α, then the inverse image of the fixed-class locus is the disjoint union of slices H_n={s=c+n}. Every slice is nonempty: translate all coordinates of one occupied block by (c+n−s(x))/m_i. The cyclic inequalities are unchanged. Each slice is convex and relatively open in its hyperplane, of dimension d−1, hence contractible.

The exponent-sum map G→Z is onto. All slice indices form one orbit, so H=H_0 maps onto the entire F_A. Its exact stabilizer is

\[
K=\{z\in\mathbb Z^k:\sum_i z_i=0\}.
\]

The restriction H→F_A is itself a covering. Take a product lift chart V at a point of H small enough that s(V)⊂(c−1/2,c+1/2), and let W be its image in B. The fixed-class portion of V is precisely V∩H, since it must have sum c modulo an integer. In another sheet zV that portion is z(V∩H), lying on H_{∑z_i}. Exactly the sheets indexed by K lie back in H. Thus F_A∩W is evenly covered by these relative sheets, proving H/K≅F_A in the actual subspace topology. There is no reliance on an unjustified set-theoretic quotient identification.

The K-action is free, and the vector of individual block sums bounds all possible integer translates meeting a compact subset of H. It is properly discontinuous even though total sum is constant: total sum alone would not suffice to bound K; the individual block sums do. Since H is connected and simply connected, it is the universal cover and π1(F_A)=K≅Z^(k−1), with basis e_i−e_k.

**Independent gap-coordinate/strong-retraction check.** In one block put g_j=x_{j+1}−x_j for j<m and g_m=x_1+1−x_m. All gaps are positive and sum1. The pair (s_m,g) determines the tuple uniquely through

\[
x_1=\frac{s_m-\sum_{j=1}^{m-1}(m-j)g_j}{m},\qquad
x_j=x_1+\sum_{\ell<j}g_\ell.
\]

Thus U_m is the product of a real sum-coordinate with the interior of the gap simplex; for m=1 the simplex is a point. T_m adds1 to the sum and cyclically permutes the gaps. Contract the gap vector linearly to (1/m,…,1/m), keeping the sum fixed. Positivity stays strict and cyclic permutation commutes with the homotopy. In the original coordinates this is the PR's map

\[
r_m(x)_j=\mu+\frac{j-(m+1)/2}{m},\qquad\mu=s_m/m.
\]

It preserves the sum, fixes equally spaced tuples, and satisfies r_m(T_m^n x)=T_m^n r_m(x), including negative n. The full affine straight-line homotopy is equivariant and fixes that target at every time. Applying it to each block preserves H and descends to a strong deformation retraction of H/K onto the equal-gap locus. Its block sums range over {a∈R^k:∑a_i=c}; K translates them by integral vectors of sum0. The quotient is exactly a (k−1)-torus, with no finite rotational-isotropy quotient. This supplies a separate coordinate check of the homotopy type.

**Full connected component and cubic specialization.** Any connected subset in the reduced totally real locus has fixed component counts. Conversely every nonempty fixed-count fixed-class locus is connected, being the image of convex H. It is therefore the entire connected component based at A, not merely a selected path family. A real genus-one curve has at most two real components. Degree1 gives a single point; k=1 gives a contractible component; k=2 gives a circle homotopy type and π1=Z.

A nonsingular plane M-cubic is genusone with two real components. Its given transverse totally real cubic intersection provides d=9 and a fixed divisor class. The proof applies to that given A. It does not require the cutting cubic itself to be nonsingular or retain its equation as an extra parameter. It also does not assert that every arbitrary count distribution can be realized in that plane-cubic class: admissibility is conditional on the given A. For any admitted A, one occupied real component gives trivial π1 and both occupied components giveZ, matching the exact source dichotomy. No central unsupported claim remains for this target.

## Falsification families and limits

| Family | Potential defect tested | Resolution |
| --- | --- | --- |
| Algebra/descent | Complex equivalence may miss real equivalence; nonidentity components may shift the class | Explicit conjugation/scalar descent; common identity-circle chart retains fixed coset offsets. |
| Unordered topology | Emb notation may mean labelled points; m=1 or symmetric configurations may cause different deck group | Source definition is divisors; local arc charts give cyclic lift cover; sum change detects every nonzero exponent even at regular polygons. |
| Fiber arithmetic | Deck map may be weighted by counts, yielding gcd components or extra finite factors | A cyclic shift changes sum by1. Weighted kernels explicitly both exclude valid loops and admit invalid ones. |
| Slice topology | Fibers as sets may not identify the topology; action might fail properness on a fixed-sum slice | Explicit restricted evenly covered charts; all block sums, not just total sum, bound translates. |
| Retraction | Equal spacing might move the class, fail equivariance or create finite isotropy | Gap-simplex contraction preserves sum and commutes with cyclic permutation; full strong homotopy fixes target and descends. |
| Original/prior identity | Cached partial status might override actual source, or source DOI might be mistakenly rejected as only a question DOI | Fresh primary body already states exact target answer; same containing-report DOI legitimately identifies it. Full PR proof and source statement/bylines remain distinct. |

Higher genus would replace the single genus-one Abel constraint by a different Abel–Jacobi problem; nothing here resolves it. Collisions remove strict gap inequalities and change topology. Nonreal pairs leave the totally real configuration locus. Varying the class removes the fixed sum. Labelled points or chosen cutting-cubic equations introduce different spaces. No conclusion about these extensions or the full collection of all distribution components is claimed.

## Source-closed finite diagnostics

`check_review.py`, SHA256 `dd67fb25a56af719100245ca8e0e74f5f4f9ce725de9957911bf3a82c3897c44`, was read before execution and frozen with26local source/control/identity pins plus6external root anchors. `CONTROL_INPUTS.json` supplies rational lifts, including one-point blocks, skew and symmetric configurations, degrees through9, signed turns, varied real sum slices and nonidentity coset charts. No floating point, source-author program or service call is used.

Normal,−O and−OO each pass with the same counts:162signed cyclic-deck cases,810homotopy-equivariance cases,48exhaustively enumerated small lift windows,92local order-chart perturbations,5real-descent scalar cases,945product-slice/deck cases,135kernel elements,2,835compact integer-translate bounds,27nonidentity-offset models and189offset/deck consistency checks. These are finite arithmetic diagnostics, not proofs of covering theory, algebraic geometry or topology by sampling. Sampled model distributions do not certify realizability by actual plane cubic intersections.

Seven wrong-science controls are rejected per mode: count-weighted one-block sum, a weighted kernel excluding a valid loop, a weighted kernel admitting an invalid loop, artificial symmetric-configuration stabilizer, omitted real rescaling, collisions, and a sum-changing anchored equal-spacing map. A separate unconditional deliberate failure exits1 in each mode; every positive run exits0. Guards use explicit exceptions and survive optimization. No failed positive run occurred in this effort. `VALIDATION.json` and `private/replays` retain all exact commands/statuses/output bytes/hashes. The written universal argument above is decisive.

## Aliases, local packages and accounting

The complete root-provided09:51:19UTC snapshot was independently replayed across all returned cells: requested A1:AQ1178,43columns;191rows including header,190data rows and maximum4nonempty returned columns. This is a fresh alias analysis of the supplied point-in-time read, not a second credentialed live GWS request or eventual concurrency clearance. No source-report DOI/problem/title match occurs.

Six raw substring/broad-word leads are retained in full in `ALIAS_SCAN.json`. The raw author substring Viro hits row171 inside environmental; the full row concerns random-walk concentration, not the author or real cubics. A symmetric-product substring hits asymmetric products in row158's brace-algebra description. Divisor hits in rows59/109 concern elliptic-billiard analytic methods, row138 polynomial divisibility of a forest determinant, and row184 divisor relations for canonical maps of complex surfaces. All are reasoned distinctness recommendations requiring root adoption before any later action, not automatic service exemptions. The scan records the raw Viro hit rather than silently reporting zero raw hits.

A bounded default-visible Markdown/JSON/text search under audits/eligibility/raw-pr1281 finds the current PR/root/input records. It does not enumerate hidden or archived packages, prove absence of another account publication, or certify historical novelty. No old source archive was copied. Root must freshly adopt every relevant semantic lead and recheck live ledger/publication sources after intervening changes before any actual accounting action.

`LITERAL_FOUR_CELL_PROPOSAL.json` is exactly one array of four literal strings: A uses OWR-16933-007 /30004145 and the exact primary contribution page; B is empty; C is the existing containing-report DOI; D credits Viro's explicit original statement and the limited Öztürkalan contribution, identifies the report's metadata byline, and distinguishes the independently checked PR proof. The row retains the genus-one/fixed-class/fixed-distribution scope, source-access facts, lack of novelty claim and AI-assisted internal-review status. There is no separate invented publication, DOI, proof attribution or byline.

This package is proposal-only. Root has not adopted its science, literal row or lead adjudications. No former PR1131 operations clearance or other-batch adoption is reused. No real external action is authorized by these diagnostics or this review.

## Closed result

The full original target is covered as a previously published explicit cubic result statement, with complete independent proof verification in the fixed PR. The proof also establishes the stated positive-degree genus-one fixed-distribution theorem, without a novelty claim. Metadata limitations and statement/proof distinctions remain explicit. Root must adopt separately; `publication_ready=false`, `root_adopted=false`, `new_publication=false`.

`MANIFEST.json` closes every public/private payload by exact size/SHA256. Only the manifest and separately hashed final `SEAL_CHECK.json` are excluded to avoid self-reference. `AUTHENTICATED_INPUTS.json` binds every tested source/control/identity input; final readback reruns the source-anchored checker and exact membership checks. The assigned25MiB allocation cap is enforced. Private primary evidence remains local. All64closed PR1273 payloads and77closed PR1267 payloads were read back unchanged; the older operations and25-row proposal were not edited. Own completion100%; overall80%; no services were mutated.

# Independent original-scope, mathematics and prior review: PR1346

**The full submitted family certificate is mathematically valid. The literal original existence question also has an authenticated earlier positive answer.** These are separate findings. For each n≥3, the specified nice balanced integer four-ray drawings of K_{3,n} and K_{4,n} satisfy the exact inequality for every simultaneous assignment of all A_e, with q(n)=⌊n/2⌋⌊(n−1)/2⌋ and 2q(n) crossings. This does not establish a new published theorem: no earlier publication of the full family statement was authenticated, and no novelty follows from that bounded search. An existing-publication row is proposed only for the bare existential question, with precise joint credit. No new full-family/source-only row is proposed.

## Immutable input and original question

The reviewed head is `7ec4c729be1a0c6d0efd374f988376e043a490de`, actual PR base `75d6dd1608d97e63cd9660d1a0f863ddb0f6cde1`. All28 changed paths and native blobs match INPUT_PINS.json:27 attempt files and QUEUE.md. The complete PR description matches SHA-256 `5d5aa452a8823efbe4fe0570be175e53f2cca416555d7b71a44358c32838d859`. The complete15,940-byte proof matches `6ec0d8fbf2e583e02fd775e24be762144d09ae3e8de9a835a80856e27527746e`. Its full text, README, mathematical acceptance and final source-scope adjudication were read. Code was treated as read-only source; no claimant program, replay wrapper, test suite or downloaded program was executed. Historical package results were not counted as new evidence. The initial attempted comparison with the current checkout's merge-base was rejected; the subsequent exact comparison uses the inventory's actual PR base.

The primary original is László A. Székely, *Variants of the Crossing Number Problem*, §2, printed983/physical59, in [OWR17/2005, *Discrete Geometry*](https://ems.press/journals/owr/articles/822). The actual [publisher PDF](https://ems.press/content/serial-article-files/45990?nt=1) was freshly retrieved, extracted and read on pp.982–984, with p.983 also visually inspected. Its1,987,522 bytes and SHA-256 `f0200fe70e287441d0fd3dbb0b6b564f4ed5bbdc04eb7513612ad0edf7fa95dc` match the historical pin. The question asks whether there are graphs admitting theoretical verification of the criterion and suggests the Zarankiewicz drawing as a candidate. It does not demand a classification, every K_{m,n}, every drawing, or a prescribed time bound. The cached catalog's broader-looking “for which graphs” wording must be read against this explicit existential sentence. Its exact statement hash matches the catalog: `d1f16eab9d8204e6426505a5c647003708d09e8bd33080a76c1a666c2cd1efb8`.

The source assumes a simple graph and a touching-free drawing with no adjacent crossings and at most one crossing per pair. The submission verifies the stronger normal/nice convention, including no triple interior crossings. It is therefore within scope. A positive nonplanar example, or the accepted infinite family, suffices for the literal question. Requiring unrestricted complete bipartite graphs would add a hypothesis absent from the source.

## Independent all-width reconstruction

Let X have m=3 or4 vertices and Y have n≥3. Put floor(m/2) X vertices at (−i,0), the rest at (i,0); split Y analogously between (0,−j) and (0,j). All radii are consecutive positive integers. Join every X vertex to every Y vertex by its segment.

An edge interior lies entirely in its open quadrant, so contains no vertex. Adjacent segments have distinct supporting lines and disjoint interiors. Independent segments have distinct axis intercepts and hence distinct supporting lines, meet at most once, and any meeting is transverse. A crossing requires both X endpoints on one ray and both Y endpoints on one ray. Reflect to intercepts u<U and v<V in the positive quadrant. Only the near-to-far matching crosses, at

\[
\left(\frac{uU(V-v)}{UV-uv},\frac{vV(U-u)}{UV-uv}\right).
\]

Both coordinates are positive and strictly less than u and v respectively. The other matching is disjoint: its inner segment has x/U+y/V<1, whereas the outer segment has equality. This proves the crossing characterization in both directions, for all radii.

A triple interior intersection would lie in one quadrant, involve no adjacent pair, and therefore require three X vertices on that quadrant's horizontal ray. Each such ray has at most two X vertices. Thus the exact integer drawing is already nice; no unproved generic perturbation is needed. Distinct crossing pairs also have distinct crossing points. The crossing count is

\[
\left[\binom{\lfloor m/2\rfloor}{2}+\binom{\lceil m/2\rceil}{2}\right]
\left[\binom{\lfloor n/2\rfloor}{2}+\binom{\lceil n/2\rceil}{2}\right]
=(m-2)q(n).
\]

The special m=3,4 bound is essential. With three X vertices on one ray, segments of intercept pairs (1,15),(2,10),(3,9) concur at (1/2,15/2). They occur already at m=5,n=29 in the analogous integer placement. No arbitrary-m niceness inference is justified.

Let P be the unordered pairs of vertex-disjoint edges. Choosing two endpoints on each side and one of two matchings gives |P|=2·binom(m,2)·binom(n,2). For each edge e, A_e is an arbitrary subset of V\e; there are no compatibility conditions. Define p(e,f) by the parity of the two endpoint-set intersections, c(e,f) by the drawing's crossing bit, and b=c XOR p. If N_ij counts pairs with c=i,p=j, then

\[
\operatorname{wt}(b)-\operatorname{wt}(c)=N_{01}-N_{11}.
\]

Consequently the required direction is exactly wt(b)≥wt(c), equivalently N_11≤N_01. Ordered-pair counts, adjacent pairs and ordinary crossing multiplicities are not substituted.

Take any induced H=K_{3,3}. Its X vertices split2+1 between rays, while its Y vertices split r+(3−r). Its baseline number of crossings is binom(r,2)+binom(3−r,2), either1 or3. Therefore Σ_{P(H)}c is odd.

Introduce each allowed membership z_e(v) as an independent Boolean variable. In Σ_{P(H)}p, a variable outside H has coefficient0. A variable with e and its nonendpoint v inside H appears once for each independent partner edge through v. There are precisely two choices for that partner's other endpoint. Its integer coefficient is2, so its coefficient modulo2 vanishes. This establishes the identity in **all variables simultaneously**; intersecting effects of switches cancel by addition in F_2. Hence Σ_{P(H)}b is odd for every full assignment.

For m=3 group b by unordered Y pairs and let w_yz be the resulting integer weight (0≤w_yz≤6). Each Y triple satisfies w_yz+w_yt+w_zt≡1 mod2. Thus the complement F of the support graph of positive weights is triangle-free. For an edge uv in any triangle-free graph, N(u) and N(v) are disjoint and d_u+d_v≤n. Summing over its f edges gives Σd_v²≤nf; Cauchy–Schwarz gives4f²≤n²f. Deal separately with f=0, divide otherwise, then use integrality to obtain f≤⌊n²/4⌋. Therefore

\[
\operatorname{wt}(b)=\sum w_{yz}\ge\binom n2-\lfloor n^2/4\rfloor=q(n).
\]

This uses only necessary parity conditions, but proves that every vector satisfying those conditions has the lower bound. There is no unsupported assumption that all such vectors are geometrically realizable. Equivalently, r_yz=w_yz mod2 satisfies r_yz=1+t_y+t_z for some vertex labels t, so within-class pairs already contribute at least binom(s,2)+binom(n−s,2), minimized at a balanced split. Both arguments are uniform in n.

For m=4 restrict the **same** assignment to each of four X triples, intersecting A_e with that subgraph's vertex set. All endpoints relevant to p remain inside, so every restricted bit equals its original bit. Each restriction has weight≥q(n), even if its X radii are nonconsecutive; the geometric argument uses only ray positions and order. Every independent pair has two X endpoints and belongs to exactly two of these four triples. Hence2wt(b)≥4q(n), yielding wt(b)≥2q(n). Independence among the four restricted assignments is neither claimed nor needed.

This proves the all-A criterion before any crossing-number consequence is used. Counts are positive at n=3 and unbounded; n=1,2 are outside the asserted range and have q(n)=0. No ordinary- or pair-crossing formula is a premise.

## Published criterion and source-proof check

The fresh145,630-byte publisher PDF of Székely, [*An Optimality Criterion for the Crossing Number*](https://amc-journal.eu/index.php/amc/article/download/43/30), AMC1(2008),32–37, SHA-256 `8b3aa3e994a205cab0e64c1b4a978807229514cd5096da3737ba6b1244c30d44`, was read in full. [DOI10.26493/1855-3974.43.506](https://doi.org/10.26493/1855-3974.43.506) was authenticated against Crossref title, author, volume, pages and publication date. Printed33 and35 were visually checked.

Theorem1 is exactly the all-assignment criterion, equivalent to CR-IODD optimality for normal drawings. Normal comparator drawings may have adjacent or repeated crossings. If the baseline is nice, iocr(D)=cr(D), so

\[
\operatorname{iocr}(G)\le\operatorname{cr}(G)\le\operatorname{cr}(D)
=\operatorname{iocr}(D)=\operatorname{iocr}(G).
\]

The accepted drawings meet all its hypotheses. Therefore the iocr and ordinary cr values are q(n) and2q(n), respectively, without limiting comparator drawings to nice or straight-line ones.

**A source-label clarification is necessary when reading the proof, not a correction to its theorem statement.** On printed35, equation9 has the form N/2−W(D)/2, with W the ordered weighted Q-sum. Consequently equations10–11, W(D′)≤W(D), express iocr(D)≤iocr(D′). The accompanying sentence calls this optimality of D′, although D is the drawing chosen optimal immediately above. Reading that sentence as optimality of D against arbitrary D′ repairs the label. This is our checked interpretation, not an authenticated author-issued erratum. The paper itself also notes an older sign typo in its reference[5]; that older body was not independently retrieved here.

The direct bit derivation bypasses the label issue entirely. For any comparator parity vector c′=c XOR p, iocr(D′)−iocr(D)=N_01−N_11. The standard elementary drawing-parity mechanism gives precisely these p: after aligning vertex locations, a generic edge homotopy changes independent crossing parity only when the moving edge passes a nonendpoint vertex; that toggles all independent partners incident to the vertex. Tangencies create/remove crossings in pairs. Conversely a thin finger detour of e around v realizes that elementary switch, crossing other edges along the path twice and incident edges at v once. Paths may be chosen off vertices and off e; planar Jordan-arc complements are connected. Repeating detours and a small general-position adjustment gives normal final drawings. Thus all incidence assignments are attainable and all normal comparator parities are covered. These familiar plane-topology facts are the geometric content of the paper's Q encoding; no independent proof of every standard general-position/Jordan-arc fact is claimed.

The new exact diagnostic on two disjoint edges checks equation9 and the label distinction in normal/-O/-OO: an uncrossed D and a one-crossing D′ have W=1 and−1, respectively. The displayed inequality is true, D is optimal, and D′ is not. The criterion statement itself correctly accepts only the uncrossed baseline. This is an explicit falsification of the misread label, not of Theorem1.

## Earlier positive answers and precise credit

Pelsmajer, Schaefer and Štefankovič, [*Removing Even Crossings*](https://ovid.cs.depaul.edu/documents/tutte.pdf), author manuscript dated4October2006, was freshly recovered (142,640 bytes, SHA-256 `8e54b9b68584482ec94f0debdc2afe39058bb73105b774fdff67cf16578c41d1`). Theorem1.2 and Remark1 explicitly record iocr(K_5)=iocr(K_{3,3})=1 and credit Székely's earlier algebraic treatment, with classical Hanani/Tutte and Kleitman/Harborth attribution. An additional [author-hosted Elsevier-produced journal-layout copy](https://www.cs.rochester.edu/~stefanko/Publications/JCTB%20-%20removing.pdf),221,983 bytes, SHA-256 `c0f4fb06892af127c1c941f2a03bea846ac2505a4b4e369d49a0d180258fa0ce`, confirms the same passages. Its PDF metadata title is the exact DOI; no byte equivalence to a live Elsevier-server PDF is asserted. Crossref and the publisher record authenticate [10.1016/j.jctb.2006.08.001](https://doi.org/10.1016/j.jctb.2006.08.001), JCTB97(4)(2007),489–500.

The essential strong Hanani–Tutte proof and its even-edge removal input were inspected in the actual source: contract an even edge while preserving rotations; handle even loops by inside/outside redrawing; then process independently-even cycles, splitting vertices when necessary and decreasing Σd(v)^3. The split separates regions bounded by a processed cycle and creates no independent odd pair. This is not merely abstract metadata. No full audit of unrelated odd-crossing≤3 applications is claimed. For the bare positive example, the established theorem together with the elementary nonplanarity of K_{3,3} and its nice one-crossing drawing already gives iocr=1. Székely's criterion then supplies the exact theoretical all-A verification. Thus by the authenticated published theory the original **existence** question has a prior affirmative answer; the PR must not be called its first solution.

The same authors' [*Removing Independently Even Crossings*](https://www.cs.rochester.edu/~stefanko/Publications-new/J20.pdf), SIAM JDM24(2010),379–393, [DOI10.1137/090765729](https://doi.org/10.1137/090765729), was also freshly recovered (234,579 bytes, SHA-256 `d4bc9a3b84222f5484273fa70b5fa190772cb3204ba20ca7073f5f1bc15cf7d3`). Its definitions, Lemmas2.1–2.3 and full Theorem3.1 proof chain on pp.381–393 were inspected: stable redrawing, vertex splits, reduction to two disjoint i-odd pairs and finite rotation/block cases. Its conclusion is iocr≤2 implies cr=iocr, not iocr≤3. The separate older ocr≤3 theorem must not be relabeled. This supplies further established positive cases, but is unnecessary for the unbounded-family proof and does not prove it by numerical substitution.

Eppstein, [*The Effect of Planarization on Width*](https://jgaa.info/index.php/jgaa/article/download/paper468/2483/2290), JGAA22(3)(2018),461–481, [DOI10.7155/jgaa.00468](https://doi.org/10.7155/jgaa.00468), was recovered and Lemma1's actual statement and complete argument on466–468 read. It proves a **pair-crossing** formula for K_{3,n}, using the classical axes drawing and an induction credited to Zarankiewicz/Kleitman. It is close precedent, but not an independent-odd theorem. The present coefficient identity supplies the stronger all-assignment input independently. Mantel's bound is likewise classical and proved above; the geometry and numerical counts are not claimed new.

No2026 unrestricted ordinary-crossing manuscript is a premise, and none was downloaded or mathematically audited. No full generalized Petersen, Norine dissertation or unrestricted K_{m,n} result is inferred from uninspected dependencies or bibliographic leads.

## New exact diagnostics, integrity and limits

The independent stdlib checker uses exact intercept-line equations, rational intersections, raw set intersections, integer coefficient counts and F_2 incidence columns. It does not reuse the claimant's orientation predicates or checker routines. Per mode, normal/-O/-OO agree byte-for-byte:20 geometry cases (m=3,4;n=3,…,12),630 local K_{3,3} restrictions with every incidence coefficient checked,288 complete simultaneous assignments, four exhaustive triangle-free graph maxima through n=6, and13 deliberate error controls. At K_{3,3}, its36 elementary switch columns all have weight2; their coordinate graph on18 pairs is connected and has rank17. Thus their image is exactly the even-parity subspace and the baseline coset has minimum weight1, without enumerating2^36 assignments or writing large test worlds.

The39 error checks across three modes reject ordered-pair counts, wrong baseline parity, discarded allowed variables, a coefficient1 instead of2, wrong image rank, omitted partner incidence, adding individual switch weights instead of XOR, wrong restriction multiplicity, wrong odd-width balancing, a ceil-for-floor Mantel bound, m=5 niceness extension, and confusion among ordinary/pair/independent-odd or adjacent crossings. The separate source-label diagnostic also passes in all three modes. All substantive validation uses explicit runtime guards. Finite tests corroborate, and do not replace, the universal argument.

The fresh read-only numeric-gid1254632077 check requested43 columns and returned191 response rows. Only broad crossing-keyword hits concerned Wajnryb's Artin quotient and a cube-move immersion problem; their full metadata is distinct. No exact target alias was returned. Response positions are not physical sheet row assertions. Bounded searches of independent-odd, CR-IODD, K3,n/K4,n and complete-bipartite terminology authenticated the papers above, not a published full-family all-A result. No absence/novelty claim follows. No claim is made to have re-audited historical large datasets or every source in the original packet.

All28 head inputs and nested manifest bytes are retained privately; a new independent hash pass checks the claimant's main and nested local bindings without executing its code. Fourteen earlier own audit packets, including PR1337, were rechecked at exact seals and member hashes and remain unchanged. Source and ledger bodies are private. The full closed seal covers every physical file and nested manifest, excluding only its own exact filename. Added allocation remains below5MiB.

## Row and final disposition

One qualified four-literal-cell existing-publication proposal is supplied, with B blank and the authenticated Székely2008 criterion DOI in C. Its A asks the literal existence question; D jointly credits Székely's criterion and Pelsmajer–Schaefer–Štefankovič's recorded prior K_{3,3}/K_5 values, gives both DOI/source links and PR1346, and explicitly disclaims full-family coverage by those DOI papers. The criterion's source-label clarification and the exact access limits are disclosed. This is an application of credited prior theory, not a new full-family publication or a claim that one cited DOI independently proves every step. No source-only or new-family row is proposed without authenticated publication provenance.

There is no remaining mathematical gap in the submitted all-n, all-assignment family theorem or original existential coverage. The exact remaining gap is publication/priority provenance for the full infinite family; this bounded audit does not settle it. The result is not a graph classification, an arbitrary-drawing certificate, or an unrestricted K_{m,n} theorem. This review is automated/AI verification, not conventional external human peer review or formal proof-assistant certification. No service, Git, queue, PR, CASE, shared-state, publication or external-contact write occurred.

# Structural reductions priority audit: PR1280 / problem 30003587

Initial independent assessment, 2026-10-18. Scope is the full finite-abelian diagonal quasi-free target, including periodic graph presentations and nonouter actions. This report is a bounded priority audit, not a novelty certificate.

## Verdict

**No verified structural source found here states or, without the additional fixed-algebra and untwisting steps, implies the whole target. Statement priority remains unresolved. Substantial reduction-level and proof-mechanism overlap is positively established.**

In particular, the return-graph corner construction is an immediate special case of Crisp–Gow's 2004 contraction theorem. The diagonal-inner/coboundary argument and its periodic-orbit test occur in Matsumoto's 2000 paper. An earlier coefficient-inner characterization under aperiodicity is in Katayama–Takehana's 1997 report. Thus neither the mere use of a return corner nor the MASA-to-periodic-product mechanism should be promoted as an independently new mechanism.

The candidate can be described, subject to mathematical verification outside this priority audit, as a reduction of the full question to the Barlak–Szabó outer aperiodic theorem using explicit fixed-algebra corner transfer and a compatible inner-kernel untwist. Whether that exact combination had already been recorded is not settled by a negative search.

## Target and falsification criteria

Let E be a finite strongly connected graph that is not a directed cycle, A=C*(E), and G finite abelian. An edge-diagonal action fixes p_v and sends S_e to chi_e(g)S_e. For every g, the desired implementers are unitaries u_(g,n) in A^alpha with Ad(u_(g,n)) converging pointwise in norm to alpha_g. There is no requested approximate multiplication law between g and h.

A successful prior-theorem challenge must handle all of the following:

1. Graph period d may exceed one.
2. Some nonidentity group elements may act inner, and the action may be nonfaithful.
3. The sequence for each element must be fixed by the entire original group.
4. A nonequivariant stable graph-algebra isomorphism is insufficient unless it transports the action and the required implementing unitaries.
5. Approximate innerness alone is insufficient. Approximate representability has additional coherent representation relations and cannot be inferred from strong approximate innerness here.

The original question is confirmed in the body of the official [OWR2017/42 PDF](https://ems.press/content/serial-article-files/46706), printed p.2621/PDF p.21, Question 1. The displayed Theorem 2 retains both outerness and aperiodicity. Its prose explicitly distinguishes classification-based approximate innerness from the question's fixed-algebra implementers.

## Positive prior results and exact mappings

### 1. Matsumoto 2000: the diagonal-inner mechanism and periodic obstruction

Kengo Matsumoto, *On automorphisms of C*-algebras associated with subshifts*, J. Operator Theory 44 (2000), 91–112. [Publisher PDF](https://jot.theta.ro/jot/archive/2000-044-001/2000-044-001-005.pdf).

Actual body inspected: §3 setup, printed p.97/PDF p.7 (condition (I)); Lemma 5.14 and Proposition 5.15, printed p.109/PDF p.19; Proposition 6.4, printed p.111/PDF p.21. Proposition 6.4 was also visually inspected.

Lemma 5.14 identifies inner diagonal automorphisms lambda(U) with diagonal coboundaries U=v phi(v*) and explicitly obtains diagonal membership of the implementer from maximal abelianness. Proposition 6.4 uses periodic points to obstruct innerness when the phase product around their orbit is nontrivial. This is the same central mechanism as the first part of candidate Lemma 1.

The applicable assumptions are important. The diagonal argument uses the paper's condition (I), already assumed in §3. For the candidate's graph, pass to the edge Cuntz–Krieger matrix L(e,f)=1 when r(e)=s(f). A finite strongly connected noncycle graph has the exit condition; its edge shift satisfies the needed condition (I). The diagonal coincides with the graph path diagonal under the canonical identification. No matrix primitivity is required by the Lemma 5.14/Proposition 6.4 diagonal-coboundary argument. The stronger condition (D) appearing in the neighboring Theorem 5.16 belongs to the full outer-automorphism exact sequence; it should not be silently imposed on, or removed from, the wrong statement.

**Checkable consequence for the full periodic case.** Take U=sum_e z_e S_e S_e*. If the edge-diagonal automorphism is inner, Proposition 6.4 forces product(z_e)=1 around every closed edge path, by evaluating its periodic infinite repetition. Choose a directed path theta_v from b to v. Comparing theta_v e eta with theta_w eta, for a return path eta from w to b, gives z_e=z_(theta_w)/z_(theta_v). Therefore t_v=z_(theta_v)^(-1) gives z_e=t_s(e) conjugate(t_r(e)). This is a short finite-graph consequence of the old periodic obstruction. The path-comparison deduction is made here; it is not attributed verbatim to Matsumoto.

**Priority classification:** a prior proof mechanism and a prior theorem from which the vertex-coboundary lemma follows by an elementary finite-graph argument. It does not itself prove strong approximate innerness of a finite group action or construct the final original-fixed-algebra implementers.

### 2. Katayama–Takehana 1997: coefficient-inner quasi-free automorphisms

Yoshikazu Katayama and Hiroaki Takehana, *On automorphisms of generalized Cuntz algebras*, RIMS Kokyuroku 1003 (1997), 81–93. [Official report PDF](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1003-6.pdf). A later same-title journal article is recorded as Int. J. Math. 9 (1998), 493–512, DOI [10.1142/S0129167X9800021X](https://doi.org/10.1142/S0129167X9800021X). The inspected theorem numbering belongs to the 1997 report, not to an uninspected journal body.

Actual body inspected: Proposition 1.2, printed p.82/PDF p.2; Proposition 2.6, printed p.89/PDF p.9 and proof on p.90/PDF p.10. Proposition 2.6 visually inspected.

Proposition 2.6 treats a full finite-type Hilbert bimodule over a finite-dimensional abelian coefficient algebra, with dimension greater than one and coefficient algebra X-aperiodic. It characterizes inner quasi-free automorphisms by trivial coefficient automorphism and coefficient-inner form Ux=uxu*. For the graph correspondence over C(E^0), this becomes the vertex-coefficient implementation in the aperiodic regime. Proposition 1.2 explicitly ties X-aperiodicity to aperiodicity of the finite adjacency matrix.

**Priority classification:** older structural overlap with candidate Lemma 1 under aperiodicity; not a source removing graph period. It is not a finite-group strong-approximate-innerness theorem.

### 3. Crisp–Gow 2004: the exact return-graph corner is already a special case

Tyrone Crisp and Daniel Gow, *Contractible subgraphs and Morita equivalence of graph C*-algebras*, [arXiv:math/0404542v1](https://arxiv.org/abs/math/0404542v1), dated 29 April 2004 in its actual PDF. The inspected source is the original 10-page preprint. Later publication metadata points to Proc. Amer. Math. Soc. 134 (2006), beginning p.2003, DOI [10.1090/S0002-9939-06-08216-5](https://doi.org/10.1090/S0002-9939-06-08216-5); publisher PDF acquisition was refused with HTTP 403, so journal body identity is not assumed.

Actual body inspected: Theorem 3.1, preprint pp.2–3; proof pp.5–8. Theorem's first page visually inspected.

The theorem removes a selected acyclic subgraph T and creates one edge for every path from the retained vertex set G^0 back to G^0 whose intermediate vertices lie in T^0. It identifies the resulting algebra with a full corner, and its proof specifies the canonical map of new edge generators to the original path operators.

**Complete hypothesis check for candidate Lemma 4's corner.** Let d be the graph period, V_0,...,V_(d-1) the cyclic classes, retain G^0=V_0, and remove T^0=E^0 minus V_0. Every edge advances the cyclic class. A path staying in T has length at most d-2, so T is finite and acyclic, and T has no infinite paths. The original finite graph has no singular vertices and no acyclic infinite tails. The theorem's condition (a) is vacuous because no infinite path can leave V_0 and stay forever in T; conditions (b)–(d) range over T-infinite paths and are vacuous. Its new paths are exactly the first-return paths of length d. Thus the new graph is precisely the candidate's F, and its corner projection is p=sum_(v in V_0) p_v. For d=1 take the identity corner instead.

The proof's generator map S_(new beta) -> S_beta intertwines the original edge-phase action with the return-path phase product. Equivariance is a direct check of these formulas, not an additional theorem stated by Crisp–Gow. Primitivity of F follows from the usual period decomposition and remains a separate elementary graph fact.

**Priority classification:** the candidate's return-corner construction itself is a direct, checkable special case of an older theorem. This does not by itself transfer strong approximate innerness through the corner, since that transfer needs fullness in A^alpha, not merely A.

### 4. Crisp 2005/2008 and Bates–Pask 2003/2004: broader corner infrastructure

Tyrone Crisp, *Corners of graph algebras*, [arXiv:math/0503626](https://arxiv.org/abs/math/0503626), PDF carrying arXiv v1 dated 28 March 2005 and manuscript date 1 February 2008; later J. Operator Theory 60 (2008), 253–271. [Publisher PDF](https://jot.theta.ro/jot/archive/2008-060-002/2008-060-002-003.pdf). Inspected preprint: Definition 3.1, Theorem 3.5, pp.4–5; Lemma 3.6, p.6; Theorem 4.6 and Corollary 4.9, pp.13–14; Proposition 4.11, p.15. It constructs graph models for vertex corners and identifies fixed algebras of labelling coactions as corners of skew products. Its voltage-law discussion is relevant background, not a theorem giving original-action fixed implementers.

Teresa Bates and David Pask, *Flow equivalence of graph algebras*, [author-hosted July 2003 preprint](https://documents.uow.edu.au/~dpask/index_files/papers/ssejournal.pdf); published ETDS 24 (2004), 367–382, DOI [10.1017/S0143385703000348](https://doi.org/10.1017/S0143385703000348). Lemma 2.2, preprint pp.3–4, characterizes fullness of a vertex corner by saturated hereditary reachability.

**Priority classification:** old graph-corner and Morita infrastructure. None of these body passages establishes the whole target.

### 5. Kodaka–Teruya 2015: a genuinely stronger-looking Morita theorem with extra coherence

Kazunori Kodaka and Tamotsu Teruya, *The strong Morita equivalence for coactions of a finite-dimensional C*-Hopf algebra on unital C*-algebras*, Studia Math. 228 (2015), 259–294, DOI [10.4064/sm228-3-4](https://doi.org/10.4064/sm228-3-4). [Publisher PDF](https://www.impan.pl/shop/publication/transaction/download/product/91245); [arXiv:1510.01826](https://arxiv.org/abs/1510.01826).

Actual publisher body inspected: Definition 6.2 and Theorem 6.3, printed p.287/PDF p.29; Corollary 6.4, printed pp.289–290/PDF pp.31–32. Also arXiv body Lemma 3.13, Corollary 3.14 and Proposition 3.15, pp.11–12, inspected to distinguish innerness from strong innerness.

Corollary 6.4 preserves the Rokhlin property and approximate representability under strong Morita equivalence of the stated twisted coactions. Definition 6.2 imposes both implementation and comultiplication compatibility. For an ordinary finite-group action interpreted as a C(G)-coaction, the latter includes the coherent multiplication relations for the group implementers. It is not the target's independent per-g implementation condition.

Corollary 3.14(i) does give a general innerness-invariance framework for weak coactions; via the invariant full-corner bimodule it supports the standard individual-innerness transfer used in candidate Lemma 2. This is an overlap in background generality, not a substitute for checking fixed membership in candidate Lemma 3.

**Blocked shortcut:** applying Corollary 6.4 after Barlak–Szabó would require first upgrading Barlak–Szabó's strong approximate innerness to approximate representability. No such upgrade is supplied in the applicable generality. This transfers the missing point to a stronger unsupported claim.

### 6. Izumi duality and Cuntz-algebra results: property and presentation limits

Masaki Izumi's own [2003 RIMS report](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1332-2.pdf), *Classification of finite group actions on classifiable C*-algebras*, RIMS Kokyuroku 1332 (2003), 26–33, Definition 2.6 and Lemma 2.7, printed p.28/PDF p.3, give the coherent fixed-sequence representation definition and the Rokhlin/approximate-representability duality. Its Theorem 5.1, printed p.32/PDF p.7, gives arithmetic conditions for approximate representability of quasi-free prime-power cyclic actions on O_n. Those conditions underscore that approximate representability cannot simply be inserted as a synonym for strong approximate innerness.

Barlak–Szabó's inspected [arXiv v3](https://arxiv.org/abs/1708.08258v3), p.3, identifies Izumi 2004 Proposition 5.6(2) as its Cuntz-algebra predecessor. The Izumi 2004 original body was not acquired in this audit; a guessed author URL returned 404 and the DOI open failed. No claim of original-body inspection of Proposition 5.6 is made.

A Kirchberg–Phillips isomorphism from a CK algebra to a convenient presentation does not make the transported action quasi-free in that presentation. Classification-based approximate innerness already appears immediately before the original OWR question. It cannot answer the stronger question by itself.

## Route matrix

| Route | Verified overlap | Status for the whole target | Exact remaining gap |
|---|---|---|---|
| Periodic first-return corner | Crisp–Gow 2004 Theorem 3.1, direct special case | Corner step subsumed | Whole-action-fixed approximate-implementer transfer |
| Inner phases / diagonal coboundary | Matsumoto 2000 Lemma 5.14, Proposition 6.4; elementary path comparison | Mechanism subsumed | Coordinated action reduction and final fixed algebra |
| Coefficient-inner quasi-free characterization | Katayama–Takehana 1997 Proposition 2.6 | Aperiodic overlap | Its X-aperiodicity does not cover original period directly |
| Ordinary innerness under invariant full corners | Kodaka–Teruya weak-coaction Morita framework; standard module argument | Background overlap | Does not provide fixed-sequence implementers |
| Strong approximate innerness via approximate representability Morita invariance | Kodaka–Teruya 2015 Corollary 6.4 | Blocked as a direct shortcut | Unproved coherent upgrade |
| Vertex representation untwist on all G | Finite graph coboundary splitting is elementary | Exact construction not located in a primary body here | Prior recording of all-group extension and fixed-algebra restoration |
| Pinching/polar step | Standard finite-dimensional relative-commutant perturbation | Exact combined use not located | Prior result with original alpha-fixed unitaries |
| Classification / UCT / Cartan models | Gives background approximate-inner or model information | Blocked as a direct shortcut | Equivariance and fixed implementers in the given action |

The pinching step is a standard averaging/polar perturbation mechanism: once beta fixes every vertex projection, implementing beta_g makes commutators with those projections tend to zero; block compression and polar decomposition restore exact commutation. Not locating this exact application is not evidence that the perturbation technique is novel.

## Counterchecks and rejected false implications

- Strong approximate innerness can fail for an inner finite-group action. On M_2, let Z_2 x Z_2 act by conjugation with the Pauli matrices X and Z. The automorphisms commute although X and Z anticommute; the whole fixed algebra is scalar. Its scalar unitaries implement only the identity. Thus neither pointwise innerness nor a general projective inner kernel suffices. The graph diagonal setting supplies the specific commuting vertex potentials needed to avoid this obstruction.
- The Pauli example is also why an unspecified removal of a projective inner kernel is not a theorem. The candidate's all-group D_g is a concrete splitting, and all D_g are fixed by the original action.
- An arbitrary exterior equivalence need not preserve the exact original fixed algebra. The candidate itself recognizes this. A result preserving approximate representability under genuine equivariant Morita equivalence is not a licence for a different exterior-equivalence claim.
- No use is made of a claim that graph simplicity implies adjacency primitivity. Periodicity is genuinely present.
- A graph algebra being isomorphic or stably isomorphic to another graph algebra does not ensure equivariant preservation of diagonal quasi-freeness.
- A search hit for *Norm-close group actions on C*-algebras* (1981), Theorem 3.4, uses the phrase “strongly approximately inner” for single AF automorphisms in older terminology. Its search passage alone was not treated as Izumi's finite-group fixed-algebra property.
- Some seminar/lecture-note search passages state a Rokhlin duality using compressed terminology. They were not used to replace Izumi's explicit coherent definition.

## Search, source access, and exposure

The work used 80 literal public search queries across initial discovery, snowballing from Matsumoto's references to Evans and Katayama–Takehana, and from Crisp's references to Crisp–Gow, plus counterqueries for corners, Morita equivalence, projective kernels, cocycle perturbations, periodic matrices, Livšic/cohomology, and fixed-algebra implementers. SEARCH_LOG.json records the literal queries. Results were used as leads; positive mathematical findings above rest on primary bodies.

Zacharias 2000 remains a material unresolved access gap: the author's [Glasgow repository record](https://eprints.gla.ac.uk/70793/) explicitly has no full text. Its chapter DOI is [10.1007/978-3-642-57288-3_15](https://doi.org/10.1007/978-3-642-57288-3_15). No theorem-level negative conclusion is drawn about that chapter.

Evans's 1982 *Gauge actions on O_A*, [publisher PDF](https://jot.theta.ro/jot/archive/1982-007-001/1982-007-001-005.pdf), was acquired; it has no embedded text. Local OCR of all 22 pages was performed. Its introduction and statement-level keyword inventory were examined; the inspected focus is gauge crossed products, K-theory and stable models, not a verified fixed-algebra implementation theorem. This is a limited body inspection, not a claim to have audited every proof. Evans's 1980 *On O_n* was a searched bibliographic lead, not an acquired body.

Before this initial seal the agent read only the assigned candidate's submitted PROOF.md, submitted SOURCE_METADATA.json and SOURCE_VERIFICATION.md, plus directory filenames needed to locate them. It did not read other priority-family findings, root mathematical reports, the current edition, prior independent-audit text, or acceptance conclusions. The task assignment itself supplied the parent's preliminary mathematical PASS and the proposed reduction outline. Two messages from root concerned shared disk space only; neither supplied mathematical or priority findings. No external person was contacted.

All third-party PDFs, OCR, screenshots and raw provider responses are retained only in the local exclusion directory. Public outputs contain authored paraphrases, literal public queries, source URLs and acquisition/inspection metadata. One raw search-batch write failed under storage pressure; that is disclosed and no successful raw preservation is asserted for it. No source-author software was executed. OCR/render tools were local generic utilities.

This audit made no git changes, commits, pushes, release, current-edition edit, or outreach. The bounded-search verdict must not be converted into a “no prior source exists” statement. The strongest verified result is the positive mechanism/substep overlap above; the exact remaining question is whether an older primary theorem or an explicitly recorded combination already supplies both missing-hypothesis removals with original whole-action-fixed implementers.


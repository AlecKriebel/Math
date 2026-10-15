# Independent priority and volume-obstruction audit

UTC report checkpoint: 2026-10-14T04:11:33.050298+00:00
Own bounded audit completion estimate: 90%. Full mathematical priority is unresolved; this percentage measures this family's bounded audit, not progress toward proving originality. No campaign counts are changed.

## Target and success criteria

The supplied candidate, PR184 head `fbd6561971368a0867df83453454427863d7f910`, claims a fixed closed oriented hyperbolic 3-manifold M, a fixed a>0, and smooth cooriented taut foliations F_N with GV(F_N)[M]=N a for every finite integer N, with the same embedded transverse circle meeting every leaf. Compact leaves of genus at least two are allowed. The proposed mechanism is a compact-support Diff_c^infinity(R) surface suspension with product endpoint collars, inserted repeatedly into a fixed pseudo-Anosov mapping torus. This report does not re-audit the candidate proof or assume its correctness as evidence about earlier literature.

An earlier full answer must supply unbounded ordinary GV on a fixed closed hyperbolic M with ordinary tautness, or a theorem whose checked hypotheses entail that consequence. General foliations with Reeb components, varying ambient manifolds/covers, projective-only invariants, or nonzero values without unboundedness do not suffice. A contradictory theorem must cover arbitrary smooth cooriented taut foliations on the relevant fixed hyperbolic M.

## Strongest verified findings

**No applicable contradiction and no earlier full target consequence was established in the personally read corpus. Priority remains bounded and unresolved.** This is not a claim of firstness, exhaustive search, or a proof that no such antecedent exists.

1. **The exact question permits compact higher-genus leaves.** In Calegari, *Problems in foliations and laminations of 3-manifolds*, arXiv:math/0209081v1, 8 September 2002, Definition 1.1 defines tautness by one circle meeting every leaf. Printed p.25, Question 10.6 asks about ordinary GV and ambient hyperbolic volume; it imposes no minimal-leaf or projective-transverse hypothesis. Its triangulation remark is not an explicit numerical inequality. The exact reference [46] is Gabai 1999, not his 2000 combinatorial-flow paper. [Primary version](https://arxiv.org/pdf/math/0209081v1)

2. **A real fixed-manifold finiteness theorem exists, but for RP1 foliations.** Brooks-Goldman, *The Godbillon-Vey invariant of a transversely homogeneous foliation*, Trans. AMS 286(2), December 1984, 651-664, Theorem 3 on p.656, assumes RP1 transverse structure and finitely generated fundamental group. Theorem 1 supplies rigidity for smooth families of those structures. Section 6, pp.661-662, bounds the corresponding class through lifted PSL(2,R) holonomy and winding-number control. These are restrictions on transverse geometry, not consequences of ordinary tautness or ambient hyperbolicity. Nothing in the supplied target asserts them. Theorem 5's circle-bundle bound has further ambient assumptions. [DOI](https://doi.org/10.1090/S0002-9947-1984-0760978-9) [Author-uploaded primary PDF](https://www.researchgate.net/profile/William-Goldman-2/publication/303491802_The_Godbillon-Vey_invariant_of_a_transversely_homogeneous_foliation/links/57813baf08ae5f367d3930da/The-Godbillon-Vey-invariant-of-a-transversely-homogeneous-foliation.pdf)

3. **The later homogeneous extension preserves this distinction.** Álvarez López-Nozawa, *Secondary characteristic classes of transversely homogeneous foliations*, arXiv:1205.3375v4, 21 May 2015, §§1.1-1.3, pp.2-4: Theorem 1.1 concerns projective structures; Theorem 1.2 and Corollary 1.3 concern specified (G,G/P) transverse structures. The selected versions do not promote finiteness to arbitrary Diff_c^infinity(R) holonomy. This source was independently found/read before the root's later hint naming it. [Primary v4](https://arxiv.org/pdf/1205.3375v4)

4. **Hyperbolic representation-volume rigidity is a different invariant.** Bucher-Burger-Iozzi, arXiv:1205.1018v1, 4 May 2012, pp.3-4, defines Vol(rho) by pulling back the hyperbolic isometry-group volume class. Theorem 1 requires a lattice embedding into Isom+(H^n), n>=3, and a representation into that same group; it bounds |Vol(rho)| by Vol(M). A general foliation's ordinary GV is not identified with this pullback merely because its ambient manifold is hyperbolic. This is an actual primary volume-bound theorem with an inapplicable identification step. [Primary v1](https://arxiv.org/pdf/1205.1018v1)

5. **Boundedness of individual top-degree classes gives no uniform foliation bound.** Gromov, *Volume and bounded cohomology*, Publ. Math. IHES 56 (1982), 5-99, §1.1, printed pp.16-17, establishes duality of the singular-cohomology sup seminorm and the simplicial norm. Deduction for connected closed oriented hyperbolic M: if u[M]=1, then ||u||_infinity=1/||M|| and hence

   `||GV(F)||_infinity = |GV(F)[M]| / ||M||`.

   Thus every individual ordinary GV class on such M is bounded. A uniform bound over F requires a uniform bound on these seminorms; the mere fact that they are finite supplies none. It would be incorrect to dismiss the target by saying every bounded class has a single universal bound, or to assert that the individual ordinary GV class on a closed hyperbolic M is necessarily unbounded. [Primary scan](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/435.pdf)

6. **The available normal-triangulation context bounds a foliated norm.** Calegari, *The Gromov norm and foliations*, arXiv:math/0007120v1, 19 July 2000, Definition 2.2.3 and Theorem 2.2.1, pp.5-6, gives a fixed-M upper bound K(M) on the foliated Gromov norm of taut foliations, using Gabai's common-triangulation theorem. Section 3.3, p.18, explains fine and virtually fine triangulations. This is primary evidence for Calegari's context, not a personal read of Gabai's proof. Neither inspected passage gives a uniform bound for ordinary GV on transverse simplices. Inferring a GV bound transfers the central issue to that unsupported uniform estimate. That inference route is blocked until a new quantitative mechanism is supplied. [Primary v1](https://arxiv.org/pdf/math/0007120v1)

7. **Two additional apparent obstructions have different meanings of taut/hyperbolic.** Walczak's 1 July 2012 primary slides, slides 6 and 11, require minimality of the first foliation in an ordered transverse pair; the GV obstruction on slide 11 concerns the reversed pair (F^t,F). Rovenski-Walczak, arXiv:1909.13250v1, 29 September 2019, pp.5-6, Definition 2/Theorem 1/Corollary 1/Example 3, requires the transverse distribution D^t to be harmonic and orthogonal to D; in dimension three its vector field must be geodesic and orthogonal to ker(omega). This is stronger than ordinary tautness of D. The 2022 publication was identified (DOI 10.1016/j.difgeo.2022.101851), but this audit's theorem evidence is the 2019v1 body. [2012 slides](https://webhome.auburn.edu/~kuperkm/dynamicsKrakow2012/Krakow_01_07_2012_PWalczak.pdf) [2019 primary v1](https://arxiv.org/pdf/1909.13250v1)

   Separately, Hurder-Langevin, arXiv:1403.0494, personally inspected Theorem 1.1/Corollary 1.2 and Definition 2.3, pp.3 and 8. Its hyperbolic resilient leaf is a contracting-holonomy and return-orbit condition. It is not a statement that the ambient manifold carries a hyperbolic metric, and it yields no ambient-volume bound in those inspected statements. [Primary body](https://arxiv.org/pdf/1403.0494)

## Actual Gabai retrieval gap

Gabai, *Essential laminations and Kneser normal form*, J. Differential Geometry 53(3) (1999), 517-574, [DOI 10.4310/jdg/1214425637](https://doi.org/10.4310/jdg/1214425637), is the exact reference. Publisher/author bibliographic metadata was read, but the actual paper body was **not obtained or read**. Modern Euclid .full/.pdf, legacy download/pdfview/DOI routes and download parameter variants returned anti-bot HTML; attempted International Press paths failed; author/course catalog and YMSC title-search leads supplied no body. HTML saved with a .pdf suffix is expressly not a PDF read. Calegari's primary accounts and other authors' theorem attributions do not substitute for Gabai's body.

Consequently this audit does not assert the precise full hypotheses or all consequences of Gabai 1999. A later audit should obtain an accessible legitimate copy and inspect its main normal-form theorems and any regularity/GV discussion. No external communication or outreach draft was made.

## Family status and exact remaining gaps

| Mechanism | Evidence | Status | Exact gap |
|---|---|---|---|
| Projective/homogeneous finiteness | Brooks-Goldman body; Álvarez López-Nozawa v4 body | Inapplicable as a general contradiction | Need an additional theorem imposing the special transverse structure on this candidate |
| Hyperbolic representation volume | Bucher-Burger-Iozzi v1 body | Inapplicable as a general contradiction | Need an identification of ordinary GV with the relevant representation-volume class |
| Gromov duality/common triangulation | Gromov body; Calegari2000v1 body | Inference to uniform GV bound blocked | Uniform control of the GV pairing on admissible simplices is unsupported |
| Gabai exact original theorem | Correct reference identified; direct body unavailable | Unresolved primary-body access | Read original main theorem/proof and inspect regularity assumptions |
| Pair-tautness/resilient-leaf obstruction | 2012 slides; 2019v1; Hurder-Langevin body | Does not establish contradiction | Target has ordinary tautness, not harmonic/geodesic prescribed transverse distribution; ambient hyperbolicity differs from holonomy hyperbolicity |
| Earlier full target answer | Bounded search and above targeted bodies | Unresolved priority | No personally verified earlier source giving all fixed-M, hyperbolic, ordinary-taut, unbounded-GV hypotheses |

The fiber-foliation GV=0 observation is not used as a new result here. No positive ambient-volume lower bound for ordinary GV is asserted. No theorem of universal vanishing for ordinary taut foliations is asserted. No theorem of firstness is asserted.

## Integrity and scope

The initial assessment and read/search ledger were sealed before inspecting any sibling/root priority outcome. No original SOURCES.md/review, sibling priority report, or root priority outcome was read at any stage. Only a filename inventory of the allowed root_primary_sources_private directory was viewed after the initial seal; no bodies there were imported or read. Later scientific hints from root were limited to source leads and are recorded in the ledger.

All source bodies, extracted text, rendered pages, downloaded HTML/metadata, and raw data are under `private/` and excluded from the exact safe public-own allowlist. Only authored audit documents and integrity manifests are allowlisted. All work was confined to this assigned folder; no Git, index, branch, remote, PR, tracker, release, Zenodo, tab/editor, original seventeen-file, or campaign-count mutation occurred. The report is a local unpublished research audit.

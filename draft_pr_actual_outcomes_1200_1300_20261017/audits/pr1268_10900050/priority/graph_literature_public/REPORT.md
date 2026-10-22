# Independent priority audit, family B — broader algebraic graph literature

**Verdict: PRIORITY UNKNOWN.** The accepted mathematical claim remains a complete counterexample to the *printed* Long Question 7.2, with its stated conventions. This audit found established antecedents for the unit-clique bound and ideal-coset coloring method. It did not locate an older explicit negative answer, or a printed stronger theorem covering the whole counterexample, in the inspected source scopes. Neither finding establishes novelty, firstness, current openness, or a discovery lineage.

This is the initial independent seal. I read the assigned submitted proof, historical source/literature records, governing instructions, and mathematical gate. I did not read other current priority families or root priority findings. Candidate knowledge and the root's requested terminology/priority cautions were present from the start; this was not a blind reconstruction. No outside person was contacted. No Git, branch, index, PR, publishing, or other service writes were performed.

## Target and falsification criteria

The target is Question 7.2 of [Delp–Hoffoss–Manning, arXiv:1512.04620v1](https://arxiv.org/pdf/1512.04620v1), PDF pp. 5–7. Its field setup uses the full integer ring of a totally real number field and imposes no PID premise. Allowed prime-graph differences are units or **prime elements**, meaning generators of nonzero prime ideals. They are not all irreducibles. The extra unit-surjectivity requirement defining Lenstra–Hurwitz cliques is excluded from this graph.

The submitted example is \(O=\mathbb Z[\sqrt {10}]\), with the nonprincipal prime \(P=(2,\sqrt {10})\), \(O/P\cong\mathbb F_2\), and both clique numbers equal to 2. The displayed right side is \(2\cdot2=4\). The input MATH_GATE.json is PASS; this family is a priority audit, not a replacement mathematical gate.

Evidence defeating an exact novelty claim would include (a) an older explicit answer to this exact question; (b) an older theorem whose actual assumptions and actual graph definition imply this entire example; or (c) a printed treatment of this same example and conclusion without naming the question. An elementary argument assembled during this audit is not category (a) or a backdated instance of (b).

## Search coverage

The query ledger records **59 literal search strings**, UTC execution times, provider, result scope, and returned entries where separately attributable. Q001–Q004 were one pooled response and are labelled accordingly. Searches covered unit-difference/unitary Cayley graphs; prime-element/Cayley/prime-difference terminology; real quadratic and discriminant-40 variants; nonprincipal-prime-ideal coloring; irreducible-difference variants; older arithmetic graphs; exact Lenstra–Hurwitz terms; the thesis; and a later citing paper. Search snippets were discovery aids only. Relevant primary leads were read to the specified scope or marked inaccessible.

All downloaded papers, HTML, extracted text, page images, and raw search responses are under locally ignored ignored_local/. The source ledger separates full file retrieval from actual reading scope. A file being downloaded does not mean every page was read. Searches sampled returned responses and did not exhaust result pagination or the scholarly record.

## Established background and the exact gap

**The unit component is classical.** [Lenstra, *Euclidean Number Fields of Large Degree* (1977)](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1977b/art.pdf), printed p. 242, defines the minimum proper-ideal quotient size \(L\) and proves \(2\le M\le L\le2^n\) in Proposition (2.2). Its proof uses distinct residues modulo a proper ideal. The page image was checked because extraction incorrectly rendered several non-strict inequalities as strict ones. Consequently the unit-clique value 2 here is a direct specialization of an old theorem after supplying the norm-two ideal. It is not a new unit-clique theorem.

[Győry (1980)](https://publi.math.unideb.hu/paper/3543/download/10_5486_PMD_1980_27_3-4_05.pdf), printed pp. 229–232, treats complements of graphs defined using bounded norm and \(S\)-units. Printed p. 231 gives the corresponding bound on clique size in the complementary graph and explicitly attributes the relevant unit case to Lenstra. These scanned pages were read visually. [Győry (1982)](https://publi.math.unideb.hu/paper/3598/download/10_5486_PMD_1982_29_1-2_08.pdf), pp. 79–81, begins with general complement Cayley graphs but specializes its main results to a finite set multiplied by a finitely generated multiplicative group. That is a definition and hypothesis boundary, not a theorem about adjoining all prime-element differences.

**The coset-coloring mechanism must receive full background credit.** [Akhtar et al. (2009)](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v16i1r117/pdf/), §6, Proposition 6.1, proves clique/chromatic equality for finite commutative rings using independent ideal cosets. The proposition and proof were inspected as text and page image. [Kiani–Molla Haji Aghaei (2012)](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v19i2p10/pdf/) studies finite rings throughout; §3 computes clique/chromatic quantities via matrix-ring factors. These results concern unit-difference graphs on finite rings, not the prime-augmented infinite integer ring.

[Defant, arXiv:1412.3054v2](https://arxiv.org/pdf/1412.3054v2), PDF pp. 1–7, studies unitary Cayley graphs of finite Dedekind-domain quotients. Lemma 3.1 uses reduction modulo prime ideals; Fact 4.1 characterizes bipartiteness by a residue field of size 2, and Fact 4.2 states clique/chromatic equality with the least relevant residue-field size. The formula page was checked visually. This is particularly close background for residue coloring, but its vertices and connection set are those of a finite quotient unit graph. It does not itself supply a statement about all prime elements of \(O\).

The remaining prime-graph step is routine ideal theory: a nonprincipal nonzero prime ideal in a number ring contains neither units nor prime elements. A contained principal nonzero prime would, by maximality, equal that ideal. Thus reduction modulo \(P\) properly colors the prime graph too. This deduction plus the known unit bound yields the submitted example. It should be described as an elementary application of classical facts. **No novelty claim is permitted for a generic ideal-coloring lemma, or for the nonprincipal-ideal exclusion argument.** I did not find an older printed source stating the full graph conclusion in the scopes actually read; this statement is a search result, not a proof of historical absence.

## Closest paper family and later leads

The [16-page Long–Thistlethwaite manuscript](https://web.math.ucsb.edu/~long/pubpdf/LenstraHurwitz.pdf) fixes the required convention on PDF p. 1 and at the opening of §3, p. 9. Theorem 3.1, p. 10, is worded with a minimum **principal**-ideal norm; its proof chooses a generator. Its quadratic corollary bounds prime cliques by 8 when 2 is inert and 4 when 2 splits, and does not state the norm-two nonprincipal case or the submitted negative answer. The [17-page author manuscript](https://web.math.ucsb.edu/~long/pubpdf/LenstraHurwitz2.pdf), pp. 1, 10–11, retains the relevant definitions and principal-ideal wording. The current copies were fingerprinted separately; their exact dating and equivalence to the journal version were not established by this family.

The [publisher record](https://www.sciencedirect.com/science/article/pii/S0022314X15003686) identifies *Journal of Number Theory* 162 (2016), 564–577, DOI 10.1016/j.jnt.2015.11.002. Direct retrieval returned 403. This audit does not attribute manuscript-only wording to an inspected version of record.

[Daniel S. Lopez's 2018 SJSU thesis](https://scholarworks.sjsu.edu/etd_theses/4974/), DOI 10.31979/etd.3bc5-77v2, is a strong unresolved lead. The institutional record and abstract were read; they discuss prime-power extensions of the class-number-one criterion. The actual institutional download link (article=8521) returned 403 through both retrieval routes. An initial unsuccessful probe used the wrong article number and was corrected from the record HTML. **The thesis body was not inspected, and no inference about whether it contains the counterexample is made.**

[Capuano–Checcoli–Mula–Terracini (2026)](https://link.springer.com/article/10.1007/s10231-026-01670-8), DOI 10.1007/s10231-026-01670-8, was followed from a citation lead to primary publisher text. The introduction, Theorem 5.6 and its introductory citation, and reference 23 were inspected. The Long–Thistlethwaite citation is to their Hurwitz-type approximation Theorem 2.1, rather than to a clique-equality resolution. This reading does not certify every part of that article.

## Terminology checks that prevent false priority matches

| Primary source read | Actual object | Relevance boundary |
|---|---|---|
| [Győry–Hajdu–Tijdeman, 2013 author text / 2014 article](https://math.unideb.hu/sites/default/files/inline-files/ght131114.pdf), introduction and §§2–6 | Difference graphs of \(S\)-units; finite representability over localized integer rings | Genuine unit-difference ancestry; no adjoining all prime elements |
| [Chen–Fu–Guo, arXiv:2003.00729v1](https://arxiv.org/pdf/2003.00729v1), pp. 1–2 | Prime differences among \(1,\ldots,n\) in \(\mathbb Z\) | Different vertex ring and excludes the unit differences |
| [Radchenko, arXiv:1807.03726v1](https://arxiv.org/pdf/1807.03726v1), pp. 1–2 | Euclidean distance 1 in finitely generated planar additive groups | Metric unit distance, not invertibility in a ring |
| [Chudnovsky et al., author text](https://web.math.princeton.edu/~mchudnov/primeCayley.pdf), pp. 1–3 | “Prime” means absence of nontrivial homogeneous vertex sets | Graph decomposition terminology, not prime-element differences |

Other search results included unit graphs defined using **sums**, zero-divisor/annihilator graphs, character-degree prime graphs, and quadratic-unit graphs over finite rings. These were excluded by definition; survey and aggregator snippets were not used as theorem evidence.

The irreducible convention would invalidate this exact coloring obstruction: in the submitted ring, 2 is irreducible but is not a prime element and belongs to \(P\); \(0,1,2\) form a triangle if irreducibles are allowed. This boundary follows from the supplied elementary proof, not from relabelling an unrelated prime graph.

## Permitted paper and metadata wording

A defensible title is **“An elementary counterexample to the printed equality in Long's Question 7.2.”**

Suggested statement: “For the graphs in Question 7.2 of Delp–Hoffoss–Manning (2015), interpreted using Long–Thistlethwaite's prime-element convention, the full integer ring of \(\mathbb Q(\sqrt {10})\) has unit and prime clique numbers 2, while its least nonzero prime-ideal norm is 2. Hence the displayed inequality is strict. The proof applies the classical ideal-residue bound for unit cliques and a routine nonprincipal-prime-ideal obstruction. We make no claim of novelty or priority.”

Credit Lenstra (1977), Proposition (2.2), for the old unit-clique ideal bound; cite Győry's arithmetic-graph work and the finite-ring coset-coloring literature as background where discussed. Credit Long for the question and Long–Thistlethwaite for the prime-clique framework. Cite Lopez as a related thesis only with its stated access limit, or inspect it before describing its detailed contents. Preserve Alec Kriebel's supplied ORCID if author metadata is prepared.

Do not use “first,” “new coloring lemma,” “previously unknown,” “resolves a currently open problem,” “independently discovered,” or a prior-discovery attribution without additional evidence. The mathematical negative answer can be stated without any of those historical claims.

## Remaining gap and release boundary

The exact remaining priority gap is historical: whether earlier full texts, including the inaccessible thesis or other unindexed work, already state the example or a theorem giving the complete prime-graph conclusion under the exact conventions. The unit part and the generic method are established background. This bounded audit cannot close the historical gap by additional inference alone. Priority and publication clearance remain false/unknown pending root synthesis and the commissioned cross-audit. This seal authorizes no publication, PR action, or merge.

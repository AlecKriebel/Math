# Inspected statement ledger

Checked 2026-10-07 UTC / 2026-10-06 PDT. This ledger records statement scope, not proof certification. PDF hashes and download times appear in DOWNLOAD_MANIFEST.json.

## Exact reductions

**Dell–Husfeldt–Wahlén (2010), expanded Dell–Husfeldt–Marx–Taslaman–Wahlén (2012/2014).** Section 3, Figure 3 replaces a positive integer weight by a directed source-to-sink path gadget of size O(log W), using binary expansion. Internal vertices have loops to cover vertices outside the chosen path. This is the permanent formulation of logarithmic weight removal. Splitting directed vertices into left/right copies with identity matching edges recovers the two-terminal matching formulation. That last equivalence is our explicit deduction; the original source need not use our signature notation. [ECCC TR10-078](https://eccc.weizmann.ac.il/report/2010/078/), [expanded v1](https://arxiv.org/html/1206.1775v1).

**Goldberg–Jerrum (2006/2008).** Section 4.5, Lemma 7 implements fixed rational n1/n2 using two internal vertices, bundles of n1 and n2 parallel edges, and one final edge. The both-used/neither-used counts are n1 and n2; partial use is impossible. Size is unary in these integers. The target binary bound requires additional machinery. The relevant text was checked in both arXiv v1 and v2. [Original v1](https://arxiv.org/html/cs/0605140v1).

**McQuillan (2013).** Section 7.2 explicitly defines edge weights and vertex fugacities as ratios of nonnegative integers encoded in binary. Lemma 25 implements the diagonal two-edge signature diag(p,q) by an unweighted matching circuit in polynomial size. Lemmas 26–27 remove fugacities and construct a simple unweighted G and computable positive integer C satisfying #PM(G)=C Z0(phi). The proof replaces edges by circuits, removes loops, and subdivides every edge into a three-edge path to remove parallel edges. Setting fugacities to zero gives exactly our weighted perfect-matching partition function. [Section 7.2, v1](https://arxiv.org/html/1301.2880v1).

**Cai–Liu (2019/2020).** The explanation after Theorem 1.2 cites McQuillan Proposition 5 for equivalence of nonnegative weighted perfect matchings and ordinary #PM. This citation corroborates established usage. [Primary preprint](https://arxiv.org/html/1904.10493), [ICALP publication](https://doi.org/10.4230/LIPIcs.ICALP.2020.23).

**Curticapean–Marx (2016).** Section 4, Method 2 gives an O(log² W) unweighted undirected integer gadget with pathwidth 2, citing Dell et al. The structural restriction explains why this size should not be confused with the unrestricted logarithmic directed construction. [Author-hosted SODA paper](https://www.cs.bme.hu/~dmarx/papers/curticapean-marx-soda2016-permanent.pdf).

## Sampling

**Jerrum–Valiant–Vazirani (1986).** Section 6, Theorem 6.3: for a self-reducible p-relation, an FPRAS for its count gives a fully polynomial almost-uniform generator. Their generator definition has a failure outcome and pointwise probability control. It is not automatically the always-feasible TV sampler specification of this project. The present deletion-based sampler and random-bit implementation must establish that specification. [Journal DOI](https://doi.org/10.1016/0304-3975(86)90174-X).

## Restricted hafnian comparators

**Rudelson–Samorodnitsky–Zeitouni, 1409.3905v2.** Theorem 1.2 assumes a d-regular graph with d>=alpha n+2, strongly expanding through n(1-alpha)/(1+kappa/4) and gives log error at most C n^(1-epsilon), with probability of larger error at most n^(-D). Theorem 1.9 instead uses a symmetric stochastic matrix, strong expansion of its large-variance graph, minimum degree and an upper bound n^(-theta) on entries; error is C n^(1-epsilon theta). Theorem 1.2(2) and Theorem 1.10 include spectral-gap improvements. These are structural approximation bounds, not unrestricted relative-error schemes. [Theorems in v2](https://arxiv.org/html/1409.3905v2), [journal DOI](https://doi.org/10.1214/15-AOP1036).

**Barvinok, 1601.07518v5.** Theorem 2.1 fixes d>0 and considers all real symmetric 2n by 2n matrices with entries in [d,1]. A polynomial approximates log hafnian within epsilon; its degree is O_d(log n-log epsilon), and it is computable in n raised to that degree. Thus the displayed bound is quasi-polynomial and its constants depend on the fixed lower bound. [Theorem 2.1 in v5](https://arxiv.org/html/1601.07518v5).

**Yi, 2609.04079v1.** Theorem 1.1(a) fixes 0<gamma<1/2 and 0<theta<=1; off-diagonal entries are zero or in [theta,1], and support degree is at least (1/2+gamma)n. The deterministic output is between exp(-epsilon) haf(A) and exp(epsilon) haf(A), with bit time n^{O_gamma,theta(1)} epsilon^{-O_gamma,theta(1)} poly(L_A+L_epsilon). Corollary 1.3 covers full support. [Theorem 1.1 in v1](https://arxiv.org/html/2609.04079v1).

## Source companion and provenance

**OpenAI entropy companion at the project pin.** Introduction Theorem thm:main gives N/512^n <= approximation <= N for binary integer multiplicities, with zero detected exactly and polynomial bit time. Section 05, sections/05-weighted.tex, gives q*-(2m-2)/ln 2 <= log2 Z_beta <= q* for finite real beta. These are different guarantees from relative-error weighted approximation. The section files, all appendices, and bibliography were inspected for FPRAS/sampler duplication. [Pinned manuscript](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Entropy-and-Face-Dimension-of-the-Perfect-Matching-Polytope-September-23-2026/main.pdf).

**Qi Ge (2011).** Question 7.6, printed p. 147, asks about an FPRAS for positively weighted perfect matchings of general graphs. This establishes historical question provenance only. [Institutional thesis record/download](https://urresearch.rochester.edu/fileDownloadForInstitutionalItem.action?itemFileId=64405&itemId=19183).

## Source citation custody

The source preprint READMEs supply author {{OpenAI}}, year 2026, full manuscript titles, and manuscript-specific @misc keys. references.bib preserves these author/title/year fields and records the reproducible pin. The paper must identify the base FPRAS as cited external work. No Lean directory name certifies its semantic scope, and none of the follow-on theorem is claimed formalized by this audit.

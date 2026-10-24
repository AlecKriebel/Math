# Kourovka Notebook 21.133 — prior negative solution located

Source: official 21st edition, October 2026 update 3, modified 20 October 2026, printed p. 199, zero-based PDF index 198. Proposer: M. Trombetti.

> Does a group need to have a subnormal abelian series if every countable subgroup of it has such a series?

The latest official main notebook is unstarred and its updates-only file has no entry for 21.133. A recent primary preprint and the current AGTA problem collection nevertheless supply a negative resolution; the unstarred marker is not used to infer openness.

https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf

## Terminology and complete quantifiers

The target is countable recognizability of the classical group class SJ. The earlier problem posed by F. de Giovanni and M. Trombetti as ADV–2B, *Advances in Group Theory and Applications* 2 (2016), pp. 127–128, explicitly defines SJ using a subnormal series of arbitrary order type with abelian factors. This is not restricted to a finite solvable series or to a well-ordered ascending series.

The exact current definition is given in Definition 2.5 of Brescia–Di Siena–Ingrosso–Trombetti, arXiv:2610.05415v1:

A general abelian series is a linearly ordered family of subgroups containing 1 and G, closed under unions and intersections of subchains, with normal abelian factors B/A at adjacent terms A<B; every nonidentity element must occur in a jump B\A. To be an SJ-series, every term must furthermore be subnormal of **finite defect in the whole ambient group G**. There is no uniform bound on those finite defects and no requirement that every term be normal in G. For H<=G, finite defect means existence of some finite chain H=H_d normal H_(d-1) normal ... normal H_0=G.

The hypothesis concerns every countable subgroup C<=G, each with a series and defects measured inside C; it does not provide one common series across all countable C. No topology, local finiteness, finite generation, cardinal bound on G, or uniform series type is assumed. A full negative answer must exhibit a non-SJ group with every countable subgroup SJ. A result about adjacent normality alone, a finite series, or an ascending series would change the target. In particular no SI/SJ notation is silently interchanged. In the standard SI convention all series terms are normal in the whole group, a stronger requirement; the independent source check identifies this definition in Hartley, Canadian J. Math. 28 (1976), p. 1308. The property in the original predecessor problem is explicitly SJ.

Original predecessor problem:
https://www.advgrouptheory.com/journal/Volumes/2/ADV%20Perspectives%20in%20Group%20Theory%20-%20an%20open%20space.pdf

## Published prior resolution and current status corroboration

M. Brescia, B. G. Di Siena, E. Ingrosso, M. Trombetti, *The group class SJ is not countably recognizable*, arXiv:2610.05415v1, submitted 4 October 2026. The Main Theorem constructs a group G which is not SJ although every countable subgroup is SJ. Definition 2.5 supplies the exact terminology above; Proposition 5.1 proves the global obstruction and Proposition 5.5 proves the countable-subgroup conclusion. The paper's proof uses a construction indexed by omega_1 and amalgamated products, not an additional continuum hypothesis in the statement. No original counterexample is claimed here.

https://arxiv.org/abs/2610.05415
https://arxiv.org/html/2610.05415v1

The current AGTA Open Problems PDF, obtained by direct HTTPS on 24 October 2026, explicitly marks the SJ question solved by these four authors, records the negative answer, and links this preprint. Two independent direct downloads produced SHA256 d18ce9a125ec79382792e97793ff80e46084b2d7ffd1e52d7bc58374d37eac81. This contemporaneous primary status supersedes the older unstarred notebook marker for the selection decision. The web tool's cached extraction of the same PDF URL was stale and omitted the solved annotation; the raw current PDF, saved text, and independent visual check are the evidence used.

https://www.advgrouptheory.com/OpenProblems.pdf

Outcome: **already_solved**, prior negative solution identified. Our screen verifies source scope and the current attribution; it does not claim that we independently audited every inference of the 22-page proof, secured journal acceptance, established prize award, or performed independent human peer review. No substantive new research, publication, or DOI.

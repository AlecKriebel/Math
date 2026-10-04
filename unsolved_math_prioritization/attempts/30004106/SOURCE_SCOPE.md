# Source gate: 30004106 / OWR-16776-002

## Exact problem, with both coefficient fields distinguished

David Benson's complete contribution, “Completing the representation ring of a finite dimensional Hopf algebra, II,” is on printed pp847–849 of OWR14/2019. The question is on p849/PDF9, visually inspected. The report was published 27February2020, though its volume year is2019.

Let G be a finite group and k a field of characteristic p. The relevant unresolved setting is modular characteristic p>0 dividing |G|. The split Green ring a(G;k) is the free abelian group on isomorphism classes of indecomposable finite-dimensional kG-modules. Its relations use direct sums, and multiplication is tensor product over k with diagonal G-action. It is not the Grothendieck ring with all short-exact-sequence relations.

Complexify this ring over Z:

    A_0=C tensor_Z a(G;k).

This C is the scalar field for functional analysis; it does not change the characteristic-p coefficient field of the modules. For x=sum_i c_i[M_i], set

    ||x||=sum_i |c_i| dim_k M_i,
    x*=sum_i conjugate(c_i)[M_i*].

Duality is the contragredient k-linear dual. The norm completion A is a commutative unital Banach *-algebra, concretely the dimension-weighted l¹ space on the indecomposable basis. Even if the indexing set is uncountable, each element has countable support.

The exact question is whether A is always symmetric:

    for every x in A, spectrum_A(x*x) is contained in [0,infinity).

Equivalently, every unital continuous complex character s:A->C satisfies s(x*)=conjugate(s(x)). On the split ring, these are the dimension-bounded species, |s([M])|<=dim_k M for every module M. The conjugation bars were checked visually; omitting them in extracted text changes the problem.

This is not symmetry of a finite-rank integral order, not ordinary characteristic-zero character theory, and not a p-adic or augmentation-adic completion. No algebraic-closure assumption on k is imposed in the OWR statement. The ordinary case (characteristic zero or p not dividing |G|) is already positive and is not the full target.

Official source: https://ems.press/journals/owr/articles/16776 and https://ems.press/content/serial-article-files/46794?nt=1. The requested UnsolvedMath numeric URL was inaccessible through the web tool; its pinned record agrees with the primary definition and question.

## Quotients and consequences are different targets

The report also defines quotients by closed spans of representation ideals, particularly projective modules and the maximal representation ideal. The stable/projective quotient A_proj, the maximal quotient A_max and its further C*-completion must not be identified with A. An injective continuous map into a C*-algebra need not preserve spectra or make the original Banach algebra symmetric.

The reported consequence gamma_X(M tensor M*)=gamma_X(M)^2 is one implication of symmetry. A result about positive module growth alone is not silently treated as the reverse implication, which would require control of all complex linear combinations and their characters. Likewise, semisimplicity or a statement about the nil/Jacobson radical is not itself symmetry.

## Primary literature and version qualification

1. Benson, *Modular representation theory and commutative Banach algebras*, arXiv:2008.13155v2,30April2022. This120-page accepted manuscript still states Question5.15.2 on printed/PDF111. Sections2.9,3.3–3.4 and4.1–4.2 give the exact involution, character criterion and modular Green-ring conventions; Proposition3.4.2 is on p55. The linked author-hosted banach-book.pdf is an older123-page layout whose PDF metadata says11June2020, not an independently newer2026 edition. It has the question at p113 and was inspected separately. The later arXiv version controls version-sensitive references in this packet.

2. The monograph was published as Memoirs of the AMS298(1488),2024, DOI10.1090/memo/1488. Official AMS publication information was located; full publisher PDF retrieval was not available here. The accepted primary manuscript is therefore the accessible full-text reference, not falsely represented as a byte-identical published edition.

3. Kua–Lim, *Tensor Products and the Stable Green Ring of the Symmetric Group Algebra F S_p*, arXiv:2603.11533v3,24August2026, gives explicit tensor decompositions modulo projectives and Benson–Symonds invariants for that particular symmetric group. Its introductory scope was checked. This is a special group/family result and does not claim the universal Banach-algebra symmetry theorem.

4. David He, *Growth problems for representations of finite groups*, arXiv:2408.04196v2,4February2025, studies the number of indecomposable summands in tensor powers and its asymptotics. Its principal statements were read. That count, even for faithful modules, is not a proof that all bounded species respect duality. No general symmetry conclusion is imported from it.

Additional primary-search checks distinguished tensor-category symmetry, symmetric Frobenius Green rings and unrelated quiver or ordinary-character results from the present analytic symmetry question. No complete general resolution was located in this bounded search. This is not a novelty certificate or an exhaustive claim about all literature.

## Prior-attempt gate

At main efd29c05204703acca9a0860812f54b94fae54b1, rank410 is queued0/5. Exact-ID/alias and Green-ring/representation-ring queries found no matching repository issue, PR or commit. Target-path histories were empty. Commit-message checks across475 mirrored refs and names across426 live branches found no matching prior attempt or invalidation. Related imported records concerning locally analytic vectors and Banach crossed products have different mathematical statements. No claim of exhaustive full-text reading of every Git blob is made.

Disposition: eligible for up to five genuine author turns on the exact modular Banach *-algebra symmetry question. Source retrieval, version comparison and this gate consume zero turns.

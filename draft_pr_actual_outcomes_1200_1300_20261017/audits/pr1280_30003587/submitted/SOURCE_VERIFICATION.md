# Source verification and supplementary checks

Checked 11 October 2026. This public editorial supplement accompanies the AI-audit-accepted proof. It preserves the mathematical content of the supplement to the frozen audited proof, SHA256 00ec1535e8dea4958ba73c5afd37758a678c4f7430746318d1761d4056e04e5f (14,337 bytes). See EDITORIAL_CHANGE_MAP.json for exact editorial changes. No external human peer review or formal proof-assistant certification is claimed.

## Exact external inputs

### Barlak–Szabó

“On diagonal quasi-free automorphisms of simple Cuntz-Krieger algebras,” arXiv:1708.08258v3 (3 October 2018), subsequently Math. Scand. 125 (2019), 210–226. Public DOI: https://doi.org/10.7146/math.scand.a-114823 . Version URL: https://arxiv.org/abs/1708.08258v3 .

The verified PDF and text extraction were inspected without modifying the source material. Definition 2.5 on p10 requires implementers fixed by the entire action, separately for each group element; it does not require approximate representation relations. Corollary 2.7 on p13 assumes aperiodicity and outerness. Corollary 2.8 on pp14–15 supplies precisely the finite strongly connected aperiodic graph version used in the candidate proof. Proposition 1.8(2), pp6–7, diagonalizes the slightly broader abelian quasi-free definition.

### Diagonal MASA

Alan Hopenwasser, Justin R. Peters, Stephen C. Power, “Subalgebras of graph C*-algebras,” New York J. Math. 11 (2005), 351–386.
- Publication page: https://nyjm.albany.edu/j/2005/11-18.html
- Publisher PDF: https://nyjm.albany.edu/j/2005/11-18.pdf
- Theorem 5.2: printed p360, PDF page10. Visually inspected and text checked.
- The path-direction conventions and translation between exits/entrances and sinks/sources are explicitly explained in §2, printed p354, PDF page4.

Roberto Conti, Jeong Hee Hong, Wojciech Szymański, “Endomorphisms of graph algebras,” arXiv:1101.4210v3 (27 August 2012), J. Funct. Anal. 263 (2012), 2529–2554.
- https://arxiv.org/abs/1101.4210v3
- https://arxiv.org/pdf/1101.4210v3
- §2.1 p5 states the MASA fact directly in the candidate proof's convention: no sinks and every loop having an exit. It cites Hopenwasser–Peters–Power Theorem5.2.

### Graph uniqueness and nonzero generators

Alex Kumjian, David Pask, Iain Raeburn, “Cuntz-Krieger algebras of directed graphs,” February1998 author preprint; published Pacific J. Math.184 (1998),161–174, DOI https://doi.org/10.2140/pjm.1998.184.161 .
- Author's publication list: https://documents.uow.edu.au/~dpask/index_files/page0001.html
- Author-hosted PDF: https://documents.uow.edu.au/~dpask/index_files/papers/ckaodg.pdf
- Theorem3.7, preprint p12, visually inspected: graph locally finite, no sinks, exit condition(L), and a graph family with all edge generators nonzero imply the desired isomorphism. Every one of these hypotheses holds for the return graph.
- Theorem1.2, p5, establishes nonzero universal graph generators.
- §1, pp3–4, supplies the source/range convention, edge matrix, and the correspondence between a 0–1 vertex matrix and its graph edge matrix.

The author-preprint pagination is deliberately distinguished from publisher pagination. A guessed MSP PDF address returned404; that failed attempt is not treated as a retrieved article.

### Fixed-point simplicity

Akitaka Kishimoto, “Outer automorphisms and reduced crossed products of simple C*-algebras,” Comm.Math.Phys.81 (1981),429–435, DOI https://doi.org/10.1007/BF01209077 . Its publisher abstract was checked at https://link.springer.com/article/10.1007/BF01209077 and states simplicity of the reduced crossed product for discrete pointwise outer actions on a simple algebra. The original PDF was **not** acquired: a Project Euclid request returned a non-PDF HTML response; the Springer PDF link resolved to the subscription page. No security challenge was executed and no paid access attempted.

The author-uploaded original article OCR was subsequently inspected at https://www.researchgate.net/publication/225983054_Outer_automorphisms_and_reduced_crossed_products_of_simpleC-algebras . Its §3, Theorem3.1 (printed p434), explicitly includes the case of simple A and each nonidentity group element acting outer, with simple reduced crossed product as conclusion. This is a text-level inspection of the original article, not a claim to have downloaded its PDF.

A current, freely accessible primary paper gives a directly inspectable statement of the exact fixed-point fact:

Siegfried Echterhoff and Mikael Rørdam, “Inclusions of C*-algebras arising from fixed-point algebras,” Groups Geom.Dyn.18 (2024),127–145, DOI https://doi.org/10.4171/GGD/743 . Publisher PDF: https://ems.press/content/serial-article-files/42588 .

Its printed p127 explicitly states fixed-point simplicity for a finite outer action on a simple algebra, following the crossed-product corner observation. Printed p129 identifies the cited crossed-product result as Kishimoto Theorem3.1. The p127 statement was text- and visually inspected; p129 was text-inspected. Nothing beyond this established background fact is borrowed from that paper.

## Elementary confirmation of the fixed-point corner step

For a finite action α:G↷A, let B=A⋊_αG and let λ_g denote its implementing unitaries. Put e=|G|^{-1}Σ_g λ_g. Then e is a projection and

    eae=E_α(a)e,

where E_α(a)=|G|^{-1}Σ_gα_g(a). Since λ_g e=e, every element of eBe has the form ce with c∈A^α. The map c↦ce is a *-homomorphism A^α→eBe. The coefficient expectation E_A:B→A gives E_A(ce)=c/|G|, so it is injective; the preceding spanning identity makes it surjective. Thus a simple crossed product has simple A^α. This verifies exactly the background step used to make the cyclic-class projection full in the fixed algebra; it does not require graph aperiodicity.

## Elementary confirmation of return-graph primitivity

Let E be finite strongly connected and d the gcd of its closed-walk lengths. Fix b. The gcd of lengths of closed walks based at b is also d: connecting b to and from any other vertex compares a closed walk there with the same route omitting that walk. Choose finitely many based closed walks with lengths ℓ_1,…,ℓ_t whose gcd is d. Their concatenations realize the additive semigroup generated by these lengths.

The positive integers ℓ_i/d have gcd1, so their nonnegative semigroup contains all sufficiently large integers. For completeness, choose one generator a. The residues of the generators span the finite group Z/aZ; a submonoid of a finite group is a subgroup, so every residue has a nonnegative combination representative N_r. Every sufficiently large integer in residue r is N_r+ka with k≥0 and is therefore in the semigroup.

Cyclic classes are defined by directed path length modulo d from b; the residue is independent of the selected path, since concatenating a fixed return path gives two closed walks. Every edge advances one class. Given u,v in the class of b, choose paths u→b and b→v, both with lengths divisible by d. Inserting the based closed walks shows that all sufficiently large multiples of d occur as lengths of paths u→v. Taking a maximum over finitely many u,v gives a common threshold. Consequently the length-d return graph has strictly positive adjacency powers eventually; it is primitive.

This also makes explicit why merely taking a power of the original matrix without restricting to one cyclic class would not suffice.

## Original-question alignment

The original OWR report (2017/42), printed p2621, explicitly assumes no zero rows or columns. Its diagonal quasi-free definition fixes each generator's range projection, so each generator is already an eigenvector. The full queued question contains neither outerness nor aperiodicity. Those two assumptions are removed by the authored reductions, not attributed to the original published theorem.

## Search and novelty limits

Targeted current searches for “diagonal quasi-free,” inner/outer graph actions, strong approximate innerness, periodic/aperiodic graphs, and full-corner reductions returned the cited Barlak–Szabó theorem and background papers. No prior explicit combined statement was located in that bounded search. This neither establishes novelty nor exhausts the literature. The reduction has since been accepted in an independent AI mathematical audit. No priority claim is made.

Source-author code was not run. This packet contains authored mathematics and public bibliographic and verification metadata. It does not reproduce source PDFs, text extracts, inspection images or raw finite-check data.

# Source-only criteria for the first fresh PR311 preprint review

This document was prepared from the independently obtained original EMS report alone, before access to the prepared package, any candidate proof/code, or any root, sibling, or inherited report. A freeze manifest records the actual UTC seal time, measured SHA-256, size, and mode. No inherited mathematical conclusion has been adopted.

## Source and actual read scope

Original: Steffen Lauritzen, "Two open problems in graphical models of algebraic nature", in Oberwolfach Report 55/2022, Algebraic Structures in Statistical Methodology, printed pages 3125–3127; whole-report DOI 10.4171/OWR/2022/55; source URL https://ems.press/content/serial-article-files/46992.

Independent download: private/source/lauritzen_46992.pdf, 600619 bytes, SHA-256 56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65. The PDF contains 50 pages. I rendered PDF pages 5–7 (zero-based 4–6) at 160 dpi and personally visually read the complete Lauritzen contribution on those pages, including the continuation, second problem, and bibliography. I have not read the remaining report as a complete source. A web open automatically returned some surrounding text; that incidental text is not evidence of full-report review.

## Exact mathematical target

Let G=(V,E) be a finite simple undirected graph, with binary sample space {0,1}^V. A probability mass function is a nonnegative counting-measure density p with sum_x p(x)=1. Lauritzen defines M(G) by every global separation implication for finite disjoint A,B,C subset V.

For zeros, conditional independence is understood by the finite polynomial equations
p_ABC(a,b,c) p_C(c) = p_AC(a,c) p_BC(b,c)
for all a,b,c, where each density is the appropriate marginal. A conditioning fiber with zero probability imposes no division and makes both sides zero. Any proof that silently assumes positive conditioning masses must establish an independent zero-fiber reduction.

His M_F(G) uses factors on all complete vertex subsets. His M_I(G) instead has the displayed exact product p(x)=product_{e in E} psi_e(x_e), using only the original graph's edges. Factors in the preceding factorization definition are real-valued. This does not obstruct nonnegative-factor analysis: since p is nonnegative, replacing each real factor by its absolute value preserves the full product, including zeros. This reduction must be justified, not silently attributed as an extra source assumption.

M_2(G) consists of distributions in M(G) satisfying, for every pair of complete binary configurations x,y,
p(x vee y) p(x wedge y) >= p(x) p(y),
with coordinatewise join/meet. Zeros are allowed; no strictly positive-density assumption appears. In particular the positive support is nonempty and closed under meet and join. Checking only some coordinate rectangles on a possibly nonrectangular support is not automatically a substitute for this whole-lattice definition.

Conjecture 1 asserts that M_I(G) intersection M_2(G) is closed under pointwise limits, for every fixed finite graph G. Equivalently, given any sequence p_n from that same graph and model, with p_n(x) -> p(x) at every x, the limiting probability density must again have finite real (equivalently nonnegative) factors on E and satisfy MTP2 and the global Markov property.

Finite-state limits preserve probability normalization/nonnegativity. The MTP2 inequalities and global Markov marginal polynomial equations are closed. Thus the substantive remaining conclusion is exact original-edge factorization of the limit. A result for strictly positive densities alone does not handle the central zero-support boundary.

## Literal isolated, empty, and normalization conventions

If v has no incident edge, the displayed edge product does not depend on x_v. Consequently every member of the literal M_I(G) has independent uniform isolated bits. Adding arbitrary unary potentials at isolates enlarges that literal source class and requires an explicit restriction or reduction back to the source.

If E is nonempty, a separate positive normalization scalar can be absorbed into any one edge factor. Unary terms at nonisolated vertices can be absorbed into an incident edge. Both statements must also cover factors that contain zeros; absorption is multiplication by a finite scalar/function, with no prohibited division.

If V is nonempty and E is empty, the conventional empty product equals 1 at every configuration, whose total mass is 2^|V|. Under the exact displayed source formula, M_I(G) is therefore empty, and Conjecture 1 is vacuously true. Introducing a Z^{-1} in the empty-edge case changes this literal convention to the uniform law; an extension may be mathematically harmless, but the attribution must say which convention is being used.

If V is empty, the sample space is a singleton, the edge product is 1, and its unique probability law is MTP2 and globally Markov. Empty sets among A,B,C give trivial conditional-independence conditions. Disconnected graphs require the appropriate independent component factorization, as well as uniform isolates for the literal source class.

## Success criteria and adversarial checks

A complete resolution needs a proof for arbitrary finite graphs and arbitrary real-density sequences in the source class, with exact finite factors on original edges at the boundary. Any coordinate contraction, auxiliary graph, quotient interaction, density/aggregate coupling correspondence, or flow construction must return to E by a proved finite construction, preserve p on and off the entire support, and establish normalization exactly.

Every nontrivial structural bridge must have stated assumptions, a checkable derivation, and the exact gap if only partial. Candidate proof steps to scrutinize include support characterization, local/global Markov equivalence with zeros, density-to-log transformations, gauge and constant terms, bounds on limiting coefficients, residual sign/flow allocation, elimination of auxiliary edges, and degenerate equal/forced coordinates.

Falsification of Conjecture 1 needs one fixed finite G, an explicit sequence in M_I(G) intersection M_2(G), a verified limit, and a proof that no original-edge product exists for that limit. A globally Markov MTP2 law lacking edge factorization, by itself, is insufficient unless membership in the relevant closure is proved. Counterexamples to Conjectures 2 or 3 have different targets and must not be represented as a refutation of Conjecture 1.

Useful boundary tests include V empty; E empty with nonempty V; one edge; an edge plus isolates; disconnected components; point masses; forced coordinates; equality blocks; implication constraints; zero conditioning fibers; vanishing normalizers; and saturated MTP2 equalities. Tests should include meaningful negative/mutated cases, not only favorable examples.

Finite enumeration and portable runner results can verify bounded checks and reproducibility. They cannot prove an arbitrary-graph theorem. Exact output comparison must be independent of a runner's own assertion logic. Numerical tolerances, raw outputs, actual argv/stdout/stderr/exit status, and input fingerprints must be recorded honestly.

Any supplementary facial-support result and any counterexample must receive their own mathematical review. Prior-framework comparisons require source-supported content, bibliographic accuracy, and explicit distinction between an independently verified new proof and a claim of novelty. Bounded negative searches cannot certify novelty. Submission usability includes complete citations, theorem scope matching the abstract and title, reproducible instructions, legible full-PDF rendering, and accurate unrefereed/AI disclosure.

## Source-only status

These criteria fix what must be established; they make no claim that the unreleased package establishes it. The independent first conclusion is frozen separately.


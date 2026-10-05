# Frozen source-only comparison criteria

Frozen at: 2026-10-04T16:59:16.924019+00:00
Approach family: graphical exponential-family boundary/support geometry; exact theorem specialization.
No candidate, root report, sibling report, or inherited report has been read.

## Primary source and body-read scope

Steffen Lauritzen, Two open problems in graphical models of algebraic nature, Oberwolfach Report 55/2022. Independently retrieved https://ems.press/content/serial-article-files/46992. Original bytes: 600619. SHA-256: 56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65.
Visually inspected full PDF pages 5, 6, and 7, corresponding to printed pages 3125, 3126, and 3127. Scope includes the entire factorization discussion and all five references; the subsequent Gaussian discussion was inspected to separate it from Conjecture 1.

## Exact comparison claim

For every fixed finite vertex set V and fixed simple undirected graph G=(V,E), the set M_I(G) intersect M_2(G) is closed for pointwise convergence of probability mass functions on {0,1}^V. M_2 means globally G-Markov and MTP2; zeros are permitted. M_I means the ORIGINAL-edge product p(x)=product over e in E of psi_e(x_e), with each psi_e:{0,1}^e -> R taking finite real values. The source does not require positivity or nonnegativity of individual factors. It does not use logarithmic parameters or require every density to be strictly positive.

A full prior theorem or deduction must preserve:

1. Finite binary product space, arbitrary fixed G, including cycles, disconnected graphs, isolates, and V empty.
2. A sequence of normalized distributions in this same intersection and a pointwise limit in the same intersection, without taking limits across graphs.
3. Global conditional-independence Markov semantics at zero cells, not merely pairwise polynomial constraints where they cease to imply global Markov.
4. MTP2 for all pairs x,y, interpreted directly by the four-cell inequality with coordinatewise meet and join, including zeros.
5. Existence of finite real ORIGINAL-edge factors for the limit. Divergent log-parameters, clique factors, factors on added edges, or a member of a closure/extended family alone do not discharge this requirement.
6. Exact equality of the normalized mass function with the product. The displayed definition contains no separate Z, no separate unary factors, and no separate constant factor. A scalar can be absorbed into an existing edge factor when E is nonempty; each nonisolated unary factor can likewise be assigned to an incident edge. Isolated coordinates cannot carry arbitrary unary factors under this literal definition.
7. Boundary support must be handled explicitly. Positive Hammersley-Clifford or interior exponential-family results require a new bridge to the zeros case unless the cited prior source already supplies it.

## Literal empty/isolate conventions

The ordinary empty product is 1. Thus when E is empty and V is nonempty, the literal M_I is empty because p(x)=1 at all 2^|V| cells cannot normalize. When V is empty, the sole configuration has mass 1 and the closure assertion holds. When E is nonempty, every member of literal M_I is constant over each isolated coordinate, and its isolated-coordinate marginal is uniform and independent; limits retain that constraint. These are source-literal consequences, not amendments to the source definition. If an author convention silently allows a normalizer or unary terms, that broader convention must be disclosed and reduced separately to the displayed original-edge formula wherever possible.

## Priority decision labels

A. Prior explicit result: a source body actually states this full claim or an equivalent one.
B. Routine specialization/corollary: a cited prior theorem entails the full claim by a short hypothesis-preserving argument recorded here; the earlier theorem need not literally state it.
C. New substantive bridge: a candidate supplies a genuinely unstated and nonroutine support-to-original-edge-factor argument beyond the located theorems. This is a judgment about inspected sources, not an assertion of global historical novelty.
D. Search absence: no overlap located within named queries/body scope; does not establish novelty.

A support-only theorem that yields full clique factorization is weaker than the original-edge conclusion unless pairwise support/value reductions are established. A toric closure description is weaker than finite factorization unless its support conditions ensure finite factors. Transfer to an equivalent or stronger unsupported support assertion is a blocked route.

## Falsifiable priority checks

Construct exact mappings among {0,1} and {-1,1}, log-linear/Ising parameters, supports, exposed faces, global Markov assumptions, and edge-factor supports. Check whether any theorem concerns all supports or only strict positivity; whether its pairwise interactions are restricted to E; whether finite support zeros arise from actual finite edge factors or only parameter limits; whether unary/normalization/isolate conventions match. Locate each theorem and proof in body text and retain private originals and full retrieval streams. At least one explicit boundary example must be analyzed in the comparison report.

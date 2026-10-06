# Frozen independent source criteria: lattice / algebra / factorization family

Freeze time: 2026-10-04 15:55:48 UTC.
Scope: PR311, problem 30005303. This file was written before candidate release.
No candidate mathematical file, PR body, prior review, other family's findings, or candidate code has been read. The imported source record served only to locate and cross-check the original. The original publisher PDF, pages 3125-3126, controls the mathematical scope.

## Authentication and exact source scope

- Publisher: https://ems.press/journals/owr/articles/11695865
- Publisher PDF: https://ems.press/content/serial-article-files/46992
- DOI: 10.4171/OWR/2022/55.
- Report: *Algebraic Structures in Statistical Methodology*, Oberwolfach Reports 19 (2022), no. 4, pages 3121-3170; publisher date 27 July 2023.
- Contribution: Steffen Lauritzen, *Two open problems in graphical models of algebraic nature*, begins at page 3125; the factorization conjectures are at page 3125 and the strengthened lattice-support conjecture is at page 3126.
- Original state space is exactly finite binary X={0,1}^V; G is a finite simple undirected graph. Any general finite-chain statement is an extension requiring separate proof, not part of source authentication.
- Original PDF SHA256: 56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65.
- Imported source record SHA256: 07eea9fc56a9b58a853935ed18d8096c889dedb2fabc01f8d17aa79f20bf6b15.
- The source's real-valued factors can be replaced by their absolute values without changing a nonnegative product density. Zeros remain meaningful; infinities are not permitted.

M(G) denotes globally Markov probability laws: every graph separation A perpendicular B given C, for disjoint subsets of V, implies the corresponding conditional independence. M_+(G) is its strictly positive part. M_F(G) consists of laws that are products of factors indexed by complete subsets of G, including singleton factors. M_E(G) is the pointwise closure of M_F(G), equivalently the closure of M_+(G). M_I(G) is the source's displayed edge-only product model. M_2(G) consists of globally Markov laws satisfying p(x join y)p(x meet y)>=p(x)p(y) for every x,y.

The two exact mathematical targets are:

1. For every finite binary graph G, M_I(G) intersect M_2(G) is closed under pointwise convergence of probability densities.
2. For every such G, M_2(G) is contained in M_F(G).

These are independent claims. Refuting (2) does not refute (1). The source additionally proposes that every globally Markov law with lattice support factorizes; that stronger assertion also needs independent scrutiny.

## Required boundary cases and success criteria

- Zeros and degeneracy are central: never apply log p outside its support or invoke strictly positive Hammersley-Clifford as if positivity survived a limit.
- Global Markov is required. Pairwise conditional independence can become vacuous on deterministic supports and is not an adequate substitute.
- Isolated vertices: the displayed edge-only formula forces densities to be constant in isolated coordinates. Allowing arbitrary unary factors changes the convention. A proof may use the usual unary-and-edge model if it separately returns to the literal convention. For E empty and V nonempty, the literal empty product is 1 and does not normalize; the displayed edge-only probability family is empty, hence trivially closed. V empty has the singleton law.
- Strict positivity is already handled by ordinary factorization; the proposed advance must treat support zeros.
- Complete graphs make (2) trivial; trees/chordal graphs are weak controls. Cycles, equality blocks, and deterministic implications are essential controls.
- A closure proof must prove edge factorization of the limit, not merely membership in M_E(G), clique factorization, global Markov, or MTP2.
- A factorization refutation must specify a normalized law, certify full global Markov and full MTP2, and exhibit an exact obstruction covering arbitrary permitted real finite factors.
- Distinguish model-image factorization from its toric/topological closure. A necessary toric binomial may refute both but support-only arguments may not.
- Do not assume claimed_solved, novelty, or correctness from the imported status. Priority is a separate later question.

## Source-first lattice route for claim (1)

The following route was derived independently from the original source before candidate access.

**Binary lattice representation.** A nonempty support S closed under meet and join has bottom b and top t. For each free coordinate i (b_i=0,t_i=1), let m_i be the meet of all s in S with s_i=1. Write i=>j if (m_i)_j=1, equivalently s_i<=s_j throughout S. Then S is exactly the set of vectors in [b,t] satisfying these implications. Indeed, for a putative permitted x, joining b with all m_i for which x_i=1 reconstructs x. Mutual implication yields equality blocks; implication between blocks is a finite partial order. Pins and equality blocks are genuine boundary cases.

**Global Markov forces graph realization of support constraints.** For free i,j with i=>j, let n_j be the join of all support states with s_j=0. The states l=n_j and h=n_j join m_i agree outside
D={k: i=>k=>j}, and differ from 0 to 1 precisely on D. Both are in S. If a graph separation across D permits choosing h on the component containing i and l on that containing j, positivity of the two conditional marginal events plus global Markov forces the forbidden i=1,j=0 state into S. Consequences:

- Each equality block induces a connected subgraph of G (take i,j in different components of the block; then D is that block).
- Every cover relation between distinct equality blocks has at least one G edge between those blocks (then D consists exactly of the two blocks).

Thus all support constraints can be realized using unary pins and edge-projection constraints: connected equality edges and one implication edge per cover suffice. S equals the set of states whose unary and edge projections occur in S. This conclusion concerns support and does not imply that arbitrary log weights on S factorize.

**Finite linear algebra completes the proposed closure route.** If p_n is edge-factorizing, globally Markov, and MTP2 and p_n tends pointwise to p, then the finite polynomial CI equations and MTP2 inequalities survive the limit. Thus supp(p) is a lattice with the graph realization above. On S=supp(p), all p_n are eventually positive. The vector log p_n restricted to S lies in the fixed finite-dimensional column space of the edge design matrix (using log absolute local factors). That column space is closed, so log p restricted to S also lies in it. Exponentiate a finite solution for the occurring edge cells, set forbidden local cells to zero, and use graph realization to recover p everywhere. Under the literal convention, isolated coordinates remain uniform in the limit and can be removed before this argument.

Audit obligation after release: check every step of any candidate against this independent support/linear-algebra route. In particular, a claim that global Markov plus lattice support already guarantees factorization is false by the exact control below. The linear-algebra step uses the approximating factorizing sequence and cannot be dropped.

## Independently derived exact falsification control for claim (2)

Take the chordless six-cycle G with vertices 1,...,6 and edges 12,23,34,45,56,61. Let
S={(a,a,b,b,c,c): a,b,c in {0,1}}.
Give weight 2 to (1,1,1,1,1,1), weight 1 to each other point of S, and weight 0 elsewhere. Normalize by Z=9.

**MTP2.** S is a meet/join sublattice. If either input is outside S, the right side of the MTP2 inequality is zero. On S, the law is proportional to 2^(abc). The only nonunit weight is the maximal state; two distinct supported inputs neither equal to the maximal state have product 1 while the meet/join product is at least 1. Comparable inputs give equality. Hence every inequality holds.

**Full global Markov.** The equality blocks are the adjacent pairs {1,2},{3,4},{5,6}. Removing vertices belonging to at most one block leaves a connected six-cycle or path, so such a set cannot separate two nonempty vertex sets. Every nontrivial separator therefore fixes at least two of the three latent bits. Given any positive-probability separator assignment, at most one bit is random. Since the members of a remaining free equality block are adjacent, that block cannot meet both separated sets. One of the two subvectors is deterministic conditional on the separator, which certifies conditional independence. Zero-probability separator assignments need no conditional definition; the corresponding marginal minors vanish.

**Exact factor obstruction.** C6 has no cliques of size above two. Restricting any clique factor to S yields a function of at most two of a,b,c. Therefore cancellation forces
p(000)^* p(011)^* p(101)^* p(110)^*
= p(001)^* p(010)^* p(100)^* p(111)^*,
where p(abc)^*=p(a,a,b,b,c,c).
Each pair cell appears once on each side and each singleton cell appears twice. All involved densities are positive, so no finite factor can vanish on an involved projection. The actual products are 1/9^4 and 2/9^4, yielding residual -1/6561. This refutes arbitrary clique factorization, even allowing signed real factors. Because the polynomial identity survives limits, the example also lies outside M_E(G). It disproves the source's claims (2) and (3), while being compatible with (1).

**Independent exact computation.** source_control_exact.py reads no candidate file and uses integer weights. source_control_result.json records 4,096 MTP2 comparisons, 252 ordered nonempty global separations, and 68,352 conditional independence minors; all checks pass. The factorization obstruction is the exact integer residual -1 before normalization.

This example is a mandatory positive falsification control for later candidate review. A purported universal affirmative proof of (2) must fail somewhere; a proposed counterexample should be checked without relying on its own checker.

## Read bounds, mechanisms, and release gate

Read so far: the expressly allowed source_record.json; original publisher metadata; the original PDF (mathematical pages 3125-3126 visually inspected, source text read to authenticate definitions); the PDF skill; this family's own newly written control and outputs. No other local research material was read.

Mechanism family: binary sublattice representation, implication covers, graph separators, edge design linear algebra, and algebraic factor cancellation. Evidence: authenticated original definitions; independent proof sketches; a formal exact C6 construction plus exhaustive integer CI/MTP2 checks. Status: source-only criteria complete. Exact remaining gap: no candidate released; no candidate correctness, full claimed scope, or novelty assessment performed. A general finite-chain extension is not established here.

Freeze this file at mode 0444 and record its SHA256 separately. Await an explicit parent release before reading any candidate or reviewer material. Never contact individuals, mutate Git, or write remotely.

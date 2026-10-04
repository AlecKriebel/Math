# Source-only falsification criteria — independent reviewer 02

This document is frozen before access to any proposed manuscript, candidate proof, package, scientific code, root review, or sibling review. The only mathematical input is the personally read Lauritzen contribution in OWR 55/2022, printed pages 3125–3127, PDF pages 5–7 (zero-based pages 4–6), DOI [10.4171/OWR/2022/55](https://doi.org/10.4171/OWR/2022/55). The original PDF was independently downloaded from [EMS](https://ems.press/content/serial-article-files/46992); it is 600619 bytes, SHA256 `56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65`.

All three page images were personally viewed in full. The Lauritzen contribution ends after its five references on printed page 3127; the following contribution by a different author is outside this review's source target. Text extraction is auxiliary evidence and was also read, with no truncated output. Rendered pixels, extracted text, download headers and full command records are retained under the ignored `private/` directory. This public document contains my formulations and deductions, rather than a reproduced primary body.

## 1. Exact source hypotheses and literal conventions

There are two themes and four numbered conjectures. Before seeing the candidate, I cannot infer which of them it claims to settle.

### Binary factorization theme

Let `V` be finite, `G=(V,E)` a simple undirected graph, and `X={0,1}^V`. A density is a real function `p` on this finite state space satisfying `p(x) >= 0` and `sum_x p(x)=1`. Projections are denoted `x_A`. The source's Markov requirement is the global one: for each triple of disjoint vertex sets `A,B,C`, graph separation of `A` and `B` by `C` implies conditional independence of the corresponding random variables given `X_C`. Let `M(G)` be the resulting probability distributions, and `M_+(G)` those that are strictly positive on every binary configuration.

The source's general factorization family `M_F(G)` is the set of Markov distributions representable as `p(x)=product_{A in C(G)} psi_A(x_A)`, where `C(G)` consists of all complete vertex subsets, and the displayed factor codomain is `R`. Singleton subsets are complete. Any assumption of nonnegative factors or factorization solely over maximal cliques must be justified as equivalent for the intended scope; it is not the literal definition. The source defines `M_E(G)` as the pointwise closure of `M_F(G)`, equivalently of `M_+(G)`, and displays `M_+(G) subset M_F(G) subset M_E(G) subset M(G)`. These displayed relationships are source statements, not independently established theorems in this source-only stage.

The source's `M_I(G)` is the subclass using only graph edges: `p(x)=product_{e in E} psi_e(x_e)`. There is no separately displayed unary factor or partition function. Arbitrary edge-factor constants can incorporate a normalizing constant when at least one edge exists; this does not justify silently adding unary terms. In particular, if `v` is isolated, the literal product has no dependence on `x_v`, so any representable probability law has a uniform independent coordinate at `v`. If `E` is empty and `V` is nonempty, the literal empty product is one and fails normalization, hence the literal family is empty. For `V` empty, the state space is a singleton and the empty product is a probability law. These are direct deductions from the displayed convention. Any alternative convention must be labelled and reconciled explicitly.

The positivity condition is the family of inequalities

`p(x join y) p(x meet y) >= p(x) p(y)` for every `x,y in X`,

with coordinatewise maximum and minimum. `M_2(G)` denotes the globally Markov distributions satisfying this condition. The source permits zero probabilities. A nonzero support satisfying these inequalities is closed under meet and join: both entries on the right are positive for support points, forcing both entries on the left to be positive. This deduction does not prove factorization.

The hypotheses to assess are:

1. For every finite simple undirected graph, `M_I(G) intersect M_2(G)` is closed under pointwise limits. More explicitly, every pointwise limit of a sequence of normalized, globally Markov, totally positive, literal edge-factorized distributions is again normalized, globally Markov, totally positive, and literal edge-factorized.
2. Every law in `M_2(G)` is in `M_F(G)`.
3. Every globally Markov law whose support is closed under coordinatewise meet and join is in `M_F(G)`.

On a finite state space, pointwise convergence is coordinatewise convergence in a finite-dimensional simplex. Nonnegativity, normalization and the displayed positivity inequalities survive such limits directly. Global Markov constraints can be written as polynomial conditional-independence identities, so their continuity can be checked without dividing by zero-probability conditioning events. These deductions isolate a possible difficulty in conjecture 1: obtaining the same literal edge factorization at the boundary. They are not a proof of that remaining implication. A proof of conjecture 2 or 3 need not establish the stronger edge-only conclusion required by conjecture 1. A result about ordinary Ising models with freely added fields does not automatically match conjecture 1.

### Gaussian descent theme

The source uses an empirical covariance matrix `S` and a precision matrix `K`; the primal objective is `log det K - tr(KS)` on positive definite graph-constrained precision matrices. The dual minimizes `-log det Sigma - d` over positive definite covariance matrices agreeing with `S` in graph-specified entries. The source displays those entry constraints using `E(G)`. A candidate must make its edge-versus-diagonal convention explicit: covariance diagonals must be addressed, and an implicit loop/diagonal convention must not become an unnoticed mathematical hypothesis. The source does not supply a formal schedule, initialization rule, covariance genericity assumption, or detailed generalized-inverse convention.

Writing `N=bd(u)` for a vertex's neighbours, the displayed update sets the complementary column entries to

`Sigma_tilde[bd^c(u),u] = Sigma[bd^c(u),N] Sigma[N,N]^- S[N,u]`.

The neighbouring block uses `S[N,u]`; the source discusses singular blocks and denotes a generalized inverse by a superscript minus. A candidate must specify the complement relative to the vertex being updated and enforce symmetric row/column updates. An inverse existing at strictly positive definite states does not justify substituting an arbitrary singular generalized inverse without checking range conditions.

The source presents Schur-complement determinant and rank expressions, then discusses a strict residual inequality that can raise rank by one. It says full-rank `S` gives convergence and cites a maximum-likelihood-threshold result associated with empty graph cores. Those cited claims are source attributions whose exact primary scope would require independent checking after the gate; the three source pages alone are not a substitute for those primary theorems.

Conjecture 4 concerns convergence to the MLE when `rank(S) >= n` and the `n`-core of the graph is empty. A candidate must quantify `n`, specify whether the covariance inputs are all such matrices or a generic/sample class, and define convergence, updates and permissible starting states. An empty `n`-core by itself is a graph property; a rank bound alone is not an articulated general-position assumption. A counterexample to an overbroad existence paraphrase, a proof of existence, and a proof of convergence are different deliverables.

## 2. Mathematical acceptance and falsification criteria

For any claimed resolution, the manuscript must state an exact theorem with quantified graph, distribution or matrix class and all extra assumptions. Its target must be matched to the relevant source conjecture, with narrowed or altered variants identified in the title, abstract and conclusions. The theorem must follow by a complete proof, or a claimed refutation must exhibit an exact counterexample meeting every hypothesis and failing the actual conclusion. Computation on finitely many graphs cannot certify an all-graph theorem.

For the binary theme I will challenge:

- All zero and boundary probabilities, conditioning events of probability zero, disconnected graphs, isolated vertices, no-edge graphs, the empty vertex set, single edges, complete graphs, and deterministic or reduced support laws.
- Signed versus nonnegative factor conventions; normalizing constants; the exact family of factors; marginal versus joint support; empty factors; and whether an edge's factor can be chosen consistently for every state.
- Support closure under meet and join in the entire cube, rather than merely closure of selected projections; graph separation for all disjoint triples; whether local/pairwise Markov properties are silently substituted for global Markov at zero probabilities.
- Claims passing from conditional odds ratios to global factorization, from a support description to a compatible collection of factors, from local constraints to nonlocal identities, or from clique factorization to edge factorization. Each bridge requires an independent argument with its assumptions checked.
- Limit arguments: whether normalizers remain meaningful, parameters diverge, cancellations are permitted, support changes are covered, and the proposed representation belongs to the same literal model. Compactness of the probability simplex is not compactness of edge parameters.
- Any additional conclusion (support classification, parameterization, approximation, uniqueness, complexity bound) separately. A correct principal theorem does not certify an unsupported extra derivation.

For the Gaussian theme I will challenge:

- Positive definiteness and semidefiniteness, symmetry, empirical-data feasibility, specified-entry preservation, singular neighbourhood blocks, isolated vertices, zero diagonals, disconnected components, empty blocks and rank-deficient initializations.
- Range conditions for Schur complements and generalized inverses; independence of generalized-inverse choice; whether the determinant/rank identities hold on the stated singular class; whether the update can leave the feasible cone.
- Diagonal and edge conventions, update schedules, fairness of schedules, attainment and uniqueness of the MLE, the core/rank/existence bridge, and generic versus universal covariance quantifiers.
- The difference between monotone objective values, rank increases, feasibility, accumulation-point optimality and convergence of the full sequence. Rank can stop increasing before convergence is proved, and a dual objective at singular states may be undefined.
- Numerical instability near singularity, scale and units, termination conditions, and whether empirical tests confirm only a restricted implementation.

I will reject a route as an unresolved proof if it simply restates the desired conclusion in an equivalent lemma, invokes a stronger unsupported factorization or convergence claim, reasons in a circle, or assumes a missing compatibility condition. A verified special case will be retained as a special case with its exact gap.

## 3. Artifact and priority acceptance criteria

These criteria are requirements for checkable research rather than claims about an unseen package.

- Personally read the entire released manuscript, all mathematical proofs and meaningful expected-result content, all scientific code, and every released PDF page. Audit title/abstract/theorem matching, author/ORCID/date/DOI/version metadata, supplement references and bibliography consistency.
- Map every computational claim to exact inputs, algorithm, expected outputs and assertion logic. Separate a primary-source reading, a mechanical pin/array check, a validated finite computation, and an all-graph mathematical proof in the report.
- Preserve released input byte counts and SHA256 pins; enumerate archive members and required dependencies; make a fresh copy at a different location and reproduce there. Use full command stdout/stderr, actual argv/cwd/start/end/exit, input and code pins. Failures remain in the evidence, with actual timestamps and no invented history.
- Compare expected results independently of the package runner's own logic. Exercise meaningful corruptions or negative cases that test coverage (altered claimed result, missing/replaced data, changed graph/model convention, malformed pin, or invariant-breaking input as applicable). A runner that merely repeats its own assertions is insufficient independent verification.
- Check platform/path assumptions, external dependencies, nondeterminism, exact versus floating-point arithmetic, numerical conditioning, missing archive files and stale generated artifacts. A successful run cannot certify a proof without proof review.
- Check bibliography entries and precise scope of primary results independently. Attribute earlier definitions and mechanisms accurately. Distinguish a documented new deduction from a new all-graph theorem or alleged first solution. Bounded literature searches cannot certify novelty or priority, and unread primary bodies cannot be reported as personally verified.
- Inspect full PDF pages visually for missing formulas, glyph errors, clipping, page count, false citation or metadata, and consistency with source text. A text extraction is insufficient visual evidence.
- Keep copyrighted primary bodies, extracts, pixels and raw command/search streams private. Public findings contain original deductions, compact source links and fingerprints. No outside communication, external-app writes, Git/index/ref changes, scientific shared-file changes or publication is authorized for this reviewer.
- Before promotion, state all findings and exact remaining gaps. Any blocking correctness, source-target, credit, scope, or reproducibility concern requires repair and another new whole independent review under the parent's repeated-review process. A source-only freeze cannot certify correctness or novelty.

## 4. Evidence limits of this freeze

I have independently obtained and personally visually read only the stated primary contribution. I have not checked its five cited primary bodies, proved the four conjectures, read any candidate, run any candidate computation, inspected any release archive, or evaluated any novelty claim. The most that this stage establishes is a source-grounded review contract. The freeze's `0444` modes are reversible measured filesystem permissions, not immutable storage, human peer review or formal proof-assistant certification.

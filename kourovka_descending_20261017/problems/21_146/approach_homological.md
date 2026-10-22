# Kourovka 21.146: preliminary homological and priority audit

Checkpoint: 2026-10-17 13:20 America/Los_Angeles (20:20 UTC).

Scope of this checkpoint: preliminary audit only, as requested by the coordinating
research agent while the descending selection remains above 21.146. No original
solution is asserted. Best-guess progress toward an independently verified,
original complete resolution of this problem: **5%**. A directly overlapping
prior complete claim now requires priority assessment before original research
on this candidate could be promoted.

## Exact target and immediate quantifier reduction

The coordinating agent supplied the official 21st-edition statement (6 October
2026 version, printed p. 198): for each integer n >= 3, does every group of type
F_(n-1) embed into a group of type F_n, or even into one of type F_infinity?
Here F_k means existence of a classifying space with finite k-skeleton.

Every input is finitely presented, since n-1 >= 2. Consequently the stronger
statement

> Every finitely presented group embeds into a group of type F_infinity

would answer both questions for every n simultaneously. The statement that all
finitely presented groups embed into one fixed F_infinity group is stronger
still. No decidability hypothesis on the word problem is present in the target.

## Directly overlapping recent primary-source claim

**OpenAI, _A universal group of type F_infinity_, dated 23 September 2026,
Theorem 1.1, p. 1** claims a single F_infinity group containing every finitely
presented group. Thus its claimed theorem implies the full answer above without
any additional mathematical input. This is a prior complete claim, not merely
an answer to the decidable-word-problem subclass. It must be considered in the
priority audit. It has **not** been independently verified in this checkpoint;
neither `already_solved` nor `solved_verified` is assigned here.

Primary manuscript at a pinned repository revision:

https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-universal-group-of-type-F-infinity-September-23-2026/paper.pdf

Locally preserved under `literature/`:

- `prior_claim_universal_Finfinity_20260923.pdf` (18 pages).
- Its text extraction, for reproducible searches.
- A provenance JSON recording retrieval, latest path commit, and SHA-256.

The manuscript's geometric conclusion depends principally on its ascending-torus
Theorem 5.1 and the controlled integral-chain filling Proposition 6.2; those are
the appropriate targets if a full independent audit is later required. Merely
finding the claimed theorem does not verify those steps or establish acceptance
by independent researchers.

## Recent established research context and blocked route

Francesco Fournier-Facio and Matthew C. B. Zaremsky, _Finiteness properties and
Higman's rope trick_, arXiv:2607.21727v1, specifically identifies Kourovka 21.146
in its introduction. Its Theorem B proves that the standard Higman rope-trick
overgroup has infinite-dimensional rational H_3 when G=F/R is infinite and
R is nontrivial, regardless of how strong the ambient finiteness properties are.
Thus that particular construction cannot supply F_3 overgroups for these inputs.
Its Theorem A gives only a conditional reduction from recursively presented
FP_n overgroups to F_n overgroups. That hypothesis is not a completed solution.

Primary source: https://arxiv.org/html/2607.21727v1

**Route status:** ordinary Higman rope trick is blocked in the above range by an
actual homological obstruction. Reusing it without a materially new mechanism
would transfer the central problem rather than solve it. The prior September
claim explicitly proposes a different mechanism; its validity is not assessed
here.

## Independently checkable homological sanity check

The failure of type F_n for the subgroup itself cannot disprove the existence of
an F_n or F_infinity overgroup. An elementary illustration also shows why
infinite-rank homology of a subgroup does not suffice.

Let P_m be the product of m rank-two free groups, with generators a_i,b_i in
factor i. Send every generator to 1 in Z, and let K_m be the kernel. The ambient
P_m has a finite classifying space X, a product of m two-petal roses.
Let Y -> X be the associated infinite cyclic cover, which is K(K_m,1), and put
R=Z[t,t^-1]. Its cellular chain complex is the tensor product over R of m copies
of the two-term complex

    R a_i + R b_i  -->  R,
       a_i,b_i     |->  t-1.

Replace the degree-one basis by x_i=a_i and y_i=b_i-a_i. Then d x_i=t-1 and
d y_i=0. In degree m the basis tensor y_1 tensor ... tensor y_m is a cycle.
Its R-span injects into H_m(Y;Z), since there are no cells in degree m+1 and
this tensor is a member of a free R-basis. Consequently H_m(K_m;Z) contains
Z[t,t^-1] and has infinite abelian rank, although K_m is a subgroup of the type
F (hence F_infinity) group P_m.

This computation is exact; no floating-point experiment is used. The classical
additional theorem that K_m is F_(m-1) is the Stallings--Bieri finiteness theorem;
it is not reproved in this preliminary note. Even without using that additional
theorem, the calculation refutes the general inference that infinite subgroup
homology prevents embedding in an F_infinity group.

For these same K_m, an embedding into an F_m group cannot be a group retract:
if r composed with i is the identity, then the induced map on H_m splits, making
H_m(K_m;Z) a direct summand of the finitely generated abelian group H_m of the
ambient F_m group, which is impossible. This obstructs only retract-based
constructions, not the embeddings asked for in the problem.

## Elementary obstruction audit

- Cardinality does not distinguish the inputs from possible targets: finite
  presentations form a countable set, and every input here is finitely presented.
- Lack of recursive presentability cannot be used against these inputs: a finite
  presentation is recursive. The computational difficulty of the word problem
  is a different property and is not a hypothesis in 21.146.
- Infinite integral cohomological dimension alone cannot obstruct type
  F_infinity. For example C_2 has RP^infinity as a classifying space, finite in
  each skeleton, despite its nonzero integral cohomology in infinitely many
  dimensions. A finite-dimensional ambient classifying space is not requested.
- The existence of an acyclic overgroup by itself says nothing about the
  finiteness of the projective resolution or higher skeleta; those are precisely
  the extra properties that would need proof.

## Outcome and remaining gap

No new solution, counterexample, or publication candidate was obtained. A strong
prior complete claim was located and preserved. The exact next priority question
is whether that September 2026 manuscript's proof withstands independent review
or has a publicly documented correction, withdrawal, or fatal gap. Until that is
resolved, an originality claim for solving 21.146 would be premature. The
homological observations above eliminate elementary obstruction arguments and
the standard rope-trick route; they do not resolve the actual embedding question.

This file is separate from QUEUE.md and PR workflows. No outreach, Git mutation,
publication, or tracker update was performed.

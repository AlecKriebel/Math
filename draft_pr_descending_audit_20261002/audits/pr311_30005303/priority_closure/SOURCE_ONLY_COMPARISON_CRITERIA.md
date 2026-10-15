# Source-only comparison criteria: PR311 / problem30005303 / Conjecture 1

Frozen actual UTC: 2026-10-04T16:30:32.661746+00:00
Status: independent source-first stage, before candidate release. Estimated completion of the historical-priority audit: 10% (source authentication and specification only).

## Read scope and provenance

Read only the task instructions, the PDF skill, and publisher source https://ems.press/content/serial-article-files/46992 . The publisher PDF has 600619 bytes and SHA256 56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65, independently measured. Read the full relevant contribution in text and visually inspected printed 3125-3126 (PDF pages 5-6); the references continue on printed 3127. No candidate proof or code, old priority gate/report, root artifact, sibling artifact, or other-family artifact has been read. No independent literature was read before this freeze. The private folder is excluded by this audit folder's .gitignore. Source binaries, extracted text, renderings, and captures remain private.

## Exact source claim

For every fixed finite vertex set V and simple undirected graph G=(V,E), let X={0,1}^V and let p be a normalized probability mass function on X. M(G) consists of distributions satisfying every global separation implication A separated from B by C => X_A independent of X_B given X_C, for disjoint A,B,C. Conditional independence at zero-probability conditioning values is interpreted by the standard unconditional cross-product equations (or only at conditioning values of positive mass).

M_F(G) permits factors over all complete vertex subsets, including singletons. M_I(G) is explicitly the class with the displayed literal formula p(x)=product_(e in E) psi_e(x_e), using only original edges. The source allows real-valued factors. Because p is nonnegative, replacing each real finite factor by its absolute value preserves p, so requiring finite nonnegative edge tables is equivalent. Zeros are allowed; neither extended real values nor cancellation of 0 times infinity counts as a finite factorization.

M_2(G)=M(G) intersect MTP2, where p(x join y)p(x meet y)>=p(x)p(y) for every x,y in X. Conjecture 1 says M_I(G) intersect M_2(G) is closed under pointwise limits in the normalized finite probability simplex. Thus for every sequence p_n of normalized MTP2 edge-factorizing distributions on the same G, if p_n(x) tends to p(x) for every x, the limiting p has finite nonnegative factors on those same original edges and remains MTP2/global Markov.

The finite simplex makes pointwise, Euclidean, and total-variation convergence equivalent, and finite summation preserves sum p=1. Normalized limits must not be replaced by unconstrained pointwise limits of unnormalized weights, since normalization can carry divergent scales and create nontrivial zero supports.

## Immediate source-only deductions, not priority findings

MTP2 is a finite collection of polynomial weak inequalities and therefore is closed. Global Markov is a finite collection of polynomial marginal cross-product equations and therefore is closed, including boundaries. Nonnegative edge-factorization implies global Markov by separating the factors across the graph separation. Consequently the substantive target is preservation of finite original-edge factorization at zero cells. Compactness of the distribution simplex alone cannot establish compactness of a finite factor representation: factor gauges can diverge.

MTP2 implies its positive support is closed under coordinatewise meet and join. Lattice support by itself does not establish edge representability. The source's Conjecture 3 is stronger and concerns clique factorization; Conjecture 2 likewise concerns all globally Markov MTP2 distributions and clique factorization. Neither is automatically equivalent to Conjecture 1, and clique factorization on graphs with larger cliques does not imply pairwise factorization.

## Literal edge-only and isolate conventions

If V has an isolated vertex, the literal product over E is independent of that coordinate. Any source-model distribution therefore gives each isolated bit its uniform law, independently of the rest. Limits preserve this exact condition. A conventional Ising theorem permitting arbitrary unary factors on isolates needs an explicit specialization to the uniform isolated law.

If E is nonempty, global normalization can be absorbed in any edge table. Every unary factor at a nonisolated vertex can also be absorbed in one incident edge; hence conventional finite pairwise-plus-unary factorization specializes to the literal source model when isolated vertices are independent uniform. This absorption is not available for E empty. When E is empty and V is nonempty, the literal empty product is 1 on every configuration and is not a normalized mass function, so M_I(G) is empty and Conjecture 1 is vacuous. If V is empty, the literal empty product is the unique normalized distribution. These cases must not be silently replaced by a uniform p=2^(-|V|) obtained from an unstated prefactor.

## What prior results would actually resolve the target

An earlier theorem explicitly asserting closedness of the same normalized finite nonnegative attractive binary edge model on every finite graph, with a stated isolate conversion, is directly equivalent.

An earlier boundary/extended-exponential-family theorem would resolve the target only with a checkable specialization that supplies finite nonnegative factors on the original graph at every allowed zero-support boundary point. A representation with extended parameters, a limit of positive potentials, an exposed-face exponential family, new edges after contraction, latent variables, or arbitrary clique potentials alone is insufficient.

A theorem for strictly positive attractive Ising distributions can be enough only if it proves the above finite-factor conclusion for all normalized boundary limits AND a verified density argument places every zero-containing source-model MTP2 distribution in that positive attractive family closure. Both steps must be checked; strict positivity cannot be silently assumed.

An earlier factorization theorem from the toric closure needs its actual support criterion plus a proof that every source-model MTP2 limit satisfies that criterion for the original edge incidence matrix. Equality with a toric variety or membership in extended Markov closure is weaker than finite monomial parameterization.

An earlier support theorem could provide the key if it shows that every relevant limit support is exactly an intersection of constraints on original edges (and allowed uniform isolates), and establishes finite pairwise representation of positive values on that support. A distributive-lattice representation, implications on arbitrary pairs, or graph-cut representation on an auxiliary graph needs an explicit localization and weight reconstruction argument.

A classical theorem plus a short genuinely routine specialization may defeat novelty even if the exact conjecture was not mentioned. This finding requires the actual primary statement, hypotheses, dates, and the complete specialization, not a citation title, metadata, negative search, or proof that the target was later called open. Conversely classical ingredients are not an already-solved finding if the required finite-factor/localization step remains unsupported or equivalent to the target.

## Falsifiable adversarial checks

Check graphs with triangles, nonchordal cycles, disconnected components, isolated vertices and E empty. Check point masses, tied-variable support, one-sided implications, supports with nonlocal equality or implication constraints, and zeros that make conditional independence vacuous. Check finite versus infinite potentials, normalized partition functions tending to zero or infinity, unary field divergence, simultaneous coupling/field divergence, and cancellations of leading energies. Check whether contraction creates an interaction absent from the original graph, whether a result uses an auxiliary graph, and whether support constraints or positivity assume away the boundary issue. Check that any claimed equivalence covers both inclusions, the same graph, the same finite state space, and the same normalization.

## First independent conclusion

The authenticated source states Conjecture 1 with literal edge-only finite real factors and nonnegative boundary distributions. It identifies finite factorization at zeros as the substantive issue. I have no source-only evidence that this was solved earlier or remains unsolved now. Priority status is undetermined pending candidate release and independent primary-literature audit. The criterion above is frozen before reading the candidate, so later comparisons must preserve this exact target and explicitly label any stronger, weaker, or convention-adjusted statements.

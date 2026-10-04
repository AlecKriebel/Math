# Source and scope gate

Problem: **4000010 / AMR-039-0010**, “Functional inequalities,” rank 553. Checked **2026-10-04 UTC**.

## Identity and primary question

The [catalogue page](https://www.unsolvedmath.com/problems/4000010) was attempted with the web reader and direct HTTP. The web reader could not open it; direct HTTP returned 403. The record was recovered from the public [UnsolvedMath dataset](https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json), revision `372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`. Only the target row was retained locally. Its title, numerical identifier, AMR identifier, proposer, source item, and proposed year agree with the task.

The complete [primary problem-list PDF](https://www.yann-ollivier.org/rech/publs/problems_curvmarkov.pdf) was downloaded. Its title page says May 2008. Problem J is on printed p. 3; that page was read as extracted text and visually inspected. In our own words, it asks how the positive-coarse-Ricci concentration results can be recast as functional inequalities when fully Gaussian tails are unavailable, considering small-scale/small-measure corrections and a quadratic-then-linear transport cost. It refers to Bobkov--Gotze duality and Gozlan--Leonard. The adjacent Problem I separately concerns weakening local concentration assumptions and retaining a continuous-time scale.

The question does **not** specify a unique proposed cost, a numerical optimal correction, or one fixed list of quantifiers. We must distinguish a concrete sufficient theorem, a counterexample to one strengthened interpretation, and resolution of the whole exploratory question.

The recovered record labels the item partially solved and includes an automatically generated partial-progress assessment. Those labels were treated only as discovery leads. Neither they nor generated claims were accepted as proof that the item remains open or is solved.

## Primary literature and complete proof checks

1. **Ollivier**, *Ricci curvature of Markov chains on metric spaces*, JFA 256 (2009), 810--864, [DOI 10.1016/j.jfa.2008.11.001](https://doi.org/10.1016/j.jfa.2008.11.001), [full published PDF](https://math.uchicago.edu/~shmuel/QuantCourse%20/Metric%20Space/Olliver,%20Ricci%20curvature%20of%20markov%20chains.pdf). Definition 18, the discussion before Theorem 33, all of Theorem 33's proof including Lemma 38, Remarks 35--37, and the relevant binomial/Poisson discussion were checked. The finite Laplace window already appears in this proof. PROOF.md reconstructs the needed argument with explicitly justified stationary limits and the exact geometric sum. It does not claim a new concentration theorem. The source also warns that a reset kernel can have curvature one and arbitrary tails.

2. **Djellout--Guillin--Wu**, *Transportation cost-information inequalities and applications to random dynamical systems and diffusions*, Annals of Probability 32 (2004), 2702--2732, [DOI 10.1214/009117904000000531](https://doi.org/10.1214/009117904000000531), [author preprint](https://arxiv.org/abs/math/0410172). Proposition 2.10 and its full proof on preprint pp. 11--12 were read. It proves the invariant-measure T1 result under a uniform transition T1 assumption and a strict W1 contraction. The paper uses the convention `W1^2 <= 2 C H`; PROOF.md uses `W1^2 <= B H`, so its `B` is twice that `C`.

3. **Eldan--Lee--Lehec**, *Transport-entropy inequalities and curvature in discrete-space Markov chains*, [arXiv:1604.06859v2](https://arxiv.org/abs/1604.06859v2), revised 27 December 2016, later published in *A Journey Through Discrete Mathematics* (2017). Theorem 1.5, Corollary 1.8, both complete proofs in Sections 2.1--2.3, and the prior-work acknowledgment on p. 4 were read. The acknowledgment credits Djellout--Guillin--Wu Proposition 2.10. The theorem assumes uniform one-step T1 and does not require reversibility. The graph corollary uses transition-support diameter at most two. It is not a theorem giving a Gaussian bound for arbitrary positive-curvature kernels.

4. **Fathi--Shu**, *Curvature and transport inequalities for Markov chains in discrete spaces*, Bernoulli 24 (2018), 672--698, [DOI 10.3150/16-BEJ892](https://doi.org/10.3150/16-BEJ892), [full author copy of the published article](https://www.normalesup.org/~mfathi/docs/BEJ892_final.pdf). The introductory setup, Theorem 1.13, and the complete Section 5 proof through Lemma 5.1 were read. The setup is a reversible graph-distance chain with normalized rates. Section 5 explicitly distinguishes this result from unrestricted Gaussian concentration in Ollivier's setting. Its weak quadratic transportation conclusions elsewhere have a different curvature hypothesis; we do not transfer them to coarse Ricci curvature by assumption.

5. **Gozlan--Leonard**, *A large deviation approach to some transportation cost inequalities*, PTRF 139 (2007), 235--283, [DOI 10.1007/s00440-006-0045-y](https://doi.org/10.1007/s00440-006-0045-y), [author manuscript](https://leonard.perso.math.cnrs.fr/papers/2007-Gozlan-Leonard-A%20large%20deviation%20approach%20to%20some%20transportation%20cost%20inequalities.pdf). Definitions of transportation and norm-entropy inequalities, Theorem 3.7 and its complete convex-duality proof, Corollary 3.14, and Theorems 3.15 and 3.17 were read. The distinction between a function of the optimal cost and a nonlinear cost inside the coupling integral is essential here. PROOF.md proves directly the elementary direction it uses, rather than importing an unchecked tensorization or nonlinear-cost implication.

These checks establish prior results and the scope distinction. The literature search is bounded and is not a historical-priority certification or an exhaustive proof of present-day openness.

## Actual previous-attempt checks

Read-only searches in `AlecKriebel/Math` checked all-state PRs for `4000010`, `AMR-039`, `Functional inequalities`, `Ollivier`, and `transport-entropy`; no matching target PR was returned. Repository content searches for `4000010` and `AMR-039-0010`, a commit search for `4000010`, and a branch search for `4000010` likewise returned no target attempt. Search-index absence alone is not conclusive.

The actual `problems/` Git tree at SHA `8f72e77ed517ba2424b4e74b324cda525e6373c3` was separately fetched recursively: 652 entries, `truncated=false`, with no path matching the target ID, AMR code, Ollivier, or functional-inequality title. The repository root listing and `AGENTS.md` were also inspected. An initial whole-repository recursive-tree request failed with a transport error; it was not represented as a completed check.

The [queue](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md) was independently fetched and recorded this exact row as rank 553, queued, 0/5, with blank Chat, Findings, and DOI cells. Queue status alone was **not** used to infer an absence of earlier work. No matching existing attempt was found in these bounded checks.

## Source integrity and redistribution boundary

Local reading-copy SHA-256 hashes:

- Problem-list PDF: `71e7841243d4652cfb28db8e133fba2169e388c5d90aacc6f61c566dd1986173`
- Ollivier published PDF: `f251b6135895d53bb3aaa325d676c4100bac3eb62da86a45e09aacbd4546cab2`
- Djellout--Guillin--Wu preprint PDF: `f8987ae8eff9f9454bf047305e65d10f0529c27d53981c79d0385d3c9301b651`
- Eldan--Lee--Lehec v2 PDF: `df791508f2c0b04de7ffe112fc9533e03626eb8266e573d418711494e043acc2`
- Fathi--Shu published PDF: `54aa71335653a3f0c5c4f032816c67cf8c91d40dd6660e7653e49a4b58d4a6ca`
- Gozlan--Leonard manuscript PDF: `204eba78208cc5089f3cec01ab353b91eb6f2a996002aec5c42fa544d613c1b5`

The public candidate contains authored mathematical prose, source metadata, the attempt log, and original small verification code/results. It excludes source PDFs, extracted full texts, screenshots, datasets, catalogue rows, private context, and unrelated material. Its exact bytes are listed in FROZEN_MANIFEST.json.

## Gate verdict

**Source identity and scope are established for a partial-results package.** No source-verified full prior resolution or new full resolution is claimed. The correction-free nonlinear transportation cost has a complete counterexample; that stronger variant is not equated with the whole original item. Independent review of the frozen mathematics and these limits is required before any remote publication.

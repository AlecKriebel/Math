# Adversarial screening of FUSF follow-ups

Checkpoint: 2026-10-24 23:08 UTC. Screening completion: 100%; progress toward solving either proposed new problem: 0%. This is a bounded plausibility/shortcut audit, not a claim of novelty or a new research result.

## Verdict and ranking

1. **Highest conceptual payoff:** decide whether there is an infinite connected locally finite simple vertex-transitive graph X with E deg FUSF(X²) > E deg FUSF(X). A verified increasing example, combined with the existing decreasing example, would establish that squaring has no universal sign. A universal nonincrease theorem would be stronger still. This is a sharp residual question, not an evidence-backed conjecture. Its difficulty is presently unassessed: the single decreasing example gives no evidence for universal nonincrease. Cayley graphs cannot supply the increasing example because their expected degree is invariant under change of finite generating set.
2. **Best concrete analytic program:** determine the large-n behavior of f(n)=E deg FUSF(G^n) for the binary grandparent graph G. Establishing convergence with an identified limit and a rate, or a genuinely unexpected alternative, could support a paper if it introduces a reusable analytic mechanism. More values or better bounds for isolated n would be an incremental extension of the current computation. The value 3 is a natural comparison value, but current evidence does not justify publishing it as a conjectured answer.
3. **Low standalone value:** merely certify f(3), f(4), or a few more strict decreases. Useful diagnostics, but not the proposed paper-level contribution by themselves.

## Metric check and the missing-shell obstruction

Let z be the first common ancestor of x,y toward the distinguished end, with a=d_T(x,z) and b=d_T(y,z). Then

    d_G(x,y) = ceil(a/2)+ceil(b/2).

Upper bound: follow each ancestor arm using jumps of length two and, if needed, one. Lower bound: every G edge changes tree distance by at most two, so at least ceil((a+b)/2) edges are needed. This already matches the upper bound unless a,b are both odd. In that remaining case, a path of (a+b)/2 G edges would have to use only length-two tree jumps without backtracking. One such jump would cross z between its two downward branches, which is not an ancestor–descendant edge of G. One extra step is therefore necessary. This proof includes a=0 or b=0 and x=y.

Consequently

    T^(2n-1) ⊆ G^n ⊆ T^(2n),

and the exact missing pairs from T^(2n) have tree distance 2n and both LCA arms odd. For fixed x, an arm pair a,b>0 with a+b=2n gives 2^(b-1) choices of y. Summing b=1,3,...,2n-1 gives

    missing degree = (4^n-1)/3,
    degree T^(2n) = 3(4^n-1),
    degree G^n = (8/3)(4^n-1).

Thus the missing pairs are exactly **one ninth** of the incident edges of T^(2n), for every n. They are not a vanishing edge-density perturbation. The degrees check against the manuscript: 8 at n=1 and 40 at n=2.

The tree-power sandwich does not squeeze f(n). Rayleigh monotonicity controls free resistance of a fixed pair when edges are added. Expected forest degree also sums the new incident edges. Indeed, T⊂G⊂T² already gives expected degrees 3, (24−√2)/7, 3, so graph inclusion cannot supply the needed scalar monotonicity. Nor can mere rough isometry: these same three graphs are roughly isometric.

This does not refute convergence to 3. It isolates the exact gap: a uniform analytic control on the summed free-resistance defect, accounting for a fixed-density anisotropic outer shell and the infinite free boundary. The finite-current upper-bound method alone has not supplied that control.

## What is and is not established

- The manuscript proves f(1)>f(2). Its certified upper bound f(2)≤3.208526010913748780 does **not** establish f(2)>3.
- No monotonicity of f(n), existence of its limit, approach from above, or rate is currently justified by the cited evidence.
- All T^m have expected degree 3: realize T as the Cayley graph of Z₂*Z₂*Z₂ and T^m using the word ball as its finite generating set; expected FUSF degree is group-invariant, and FUSF(T)=T.
- The end-preserving group makes every G^n vertex-transitive. Any assertion about the *full* automorphism group of every power would require its own proof; it is unnecessary for posing the asymptotic question.
- For a sign claim, finite certificates must prove an upper bound for the smaller side and a compatible lower bound or exact value for the larger side. A string of finite-exhaustion upper bounds cannot by itself establish a new increasing example.

## Public-page recommendation

Either question can appear now as a carefully labeled future direction, if the site is meant to record plans. Neither should be described as an established worldwide open problem, a new theorem, or a guaranteed paper project based on this bounded screen. Prefer the increasing-example question for a short public list; use the asymptotic program if a concrete continuation is desired. Safe formulations:

> Can squaring ever increase expected FUSF degree on an infinite connected locally finite simple vertex-transitive graph?

> What is the large-power behavior of expected FUSF degree for the binary grandparent graph? Does it converge, and if so, to what value and at what rate?

Avoid “prove that the degrees decrease to 3” until evidence for both parts exists. The currently verified metric observation is elementary support for the investigation, not itself a paper-level advance.

## Primary-source screen and its limits

Read the local released manuscript and the opening statements of the following primary sources. Targeted web searches for FUSF, squaring/powers, and monotonicity returned no directly matching result. That is only a bounded negative search, not an exhaustive priority assessment.

- Pete–Timár, *The Free Uniform Spanning Forest is disconnected in some virtually free groups, depending on the generator set*, arXiv:2006.06387v2, pp. 1–2: explicitly distinguishes group-invariant expected degree from generator-dependent component counts. https://arxiv.org/pdf/2006.06387
- Benjamini–Lyons–Peres–Schramm, *Uniform Spanning Forests*, corrected author version 27 January 2009: established free/wired/electrical framework. The screen does not claim a full reread of all 72 PDF pages. https://rdlyons.pages.iu.edu/pdf/usf.pdf
- Tang, *Weights of uniform spanning forests on nonunimodular transitive graphs*, arXiv:1908.09889v2, introductory Theorem 1.3: grandparent FUSF connectivity and branching/heaviness, not the degree asymptotic under graph powers. https://arxiv.org/pdf/1908.09889

No outreach, repository-wide edits, Git actions, site edits, or long computations were performed.

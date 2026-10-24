# Kourovka 21.125 — authoritative source contract

Audit date: October 24, 2026 UTC. This file preserves the exact mathematical domain; original research on the remaining Hydra case has not begun in this audit task.

## Source and attribution

Latest main PDF linked by the official Notebook website: 21st edition, October 20, 2026 file `21tkt-3.pdf`, printed **p.198**, problem **21.125**. It names **M. Bridson** in the problem heading and is signed **I. Soroko**. The preceding problem 21.124 defines virtually special using a finite-index subgroup isomorphic to the fundamental group of a special complex in the sense of Haglund–Wise (2008). A special complex need not be compact. A stronger demand for virtual **compact** specialness is not part of 21.125.

Authoritative URL: https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf

## Complete mathematical statement, with notation normalized

For a finite-rank free group \(F_m\) and \(\varphi\in\operatorname{Aut}(F_m)\), assume its polynomial growth degree is \(m-1\). The Notebook defines this explicitly by taking some, equivalently any, free basis \(X=\{x_1,\dots,x_m\}\) and requiring
\[
\max_{1\le i\le m}|\varphi^n(x_i)|_X\asymp n^{m-1},
\]
where \(|g|_X\) is minimal length in the basis elements and their inverses.

(a) Must \(F_m\rtimes_\varphi\mathbb Z\) be virtually special?

(b) In particular, are all the Hydra groups
\[
G_m=\langle a_1,\dots,a_m,t\mid t^{-1}a_1t=a_1,\quad
 t^{-1}a_it=a_i a_{i-1}\ (2\le i\le m)\rangle
      =F_m\rtimes\mathbb Z
\]
virtually special?

There is no CAT(0) hypothesis in (a). It must not be imported from the adjacent, different problem 21.124. The displayed nonempty basis requires positive rank; rank zero has an undefined displayed maximum. The statement imposes no lower bound beyond that. For \(m=1\), the mapping tori are the rank-two free abelian group and Klein bottle group, both virtually special. For \(m=2\), all free-by-cyclic groups are already known virtually special, hence this subclass is excluded from original-solution claims.

## Critical actual-word versus outer-growth issue

The displayed metric is **actual word length**, not cyclically reduced length/conjugacy-class length. Replacing \(\varphi\) by an inner twist leaves the mapping torus isomorphic but may change the actual growth degree. `GROWTH_METRIC_SCOPE.md` gives the complete elementary calculation: an inner twist of the established non-virtually-special rank-three Gersten example has actual growth \(\Theta(n^2)\), so it meets the literal numerical hypothesis of (a). The same outer automorphism has cyclic growth degree one. Fresh independent verification of this scope finding remains a promotion gate.

Thus one must distinguish these targets:

1. The literal (a), with the explicit actual-word metric: negative by a re-presentation of a known example, subject to independent review of this recorded implication.
2. An alternative outer/cyclic degree \(m-1\) variant: a different statement; no complete known answer was located in this bounded audit. It is not an authenticated correction to the Notebook.
3. The separate Hydra family (b): the stated representatives are triangular and have the indicated actual degree; the inner-twist counterexample does not answer their virtual specialness.

The 2021 proposer comments sheet reports Hydra virtual specialness established for \(m\le4\), without providing the full proof there. Those ranks are already claimed prior work and must not be presented as original. The unresolved research scope of (b) is therefore provisionally \(m\ge5\), unless later literature supplies more cases. No full proof for all ranks was located.

## Success criteria and prohibited substitutions

A full affirmative (a) would require every admissible rank and automorphism; one valid counterexample answers the universal question negatively. A full affirmative (b) would cover every positive rank; a negative answer requires one specific Hydra group proven not virtually special. Resolving (a) alone is not a resolution of both subquestions.

Virtual specialness is stronger than merely acting freely on a CAT(0) cube complex; no finite-dimensional, proper, or cocompact property follows solely from the word “free.” Conversely failure of cocompact cubulation excludes virtual compact specialness and does not by itself exclude the noncompact specialness asked here. Hyperbolic Hydra groups in Brady–Dison–Riley are different groups: their established virtual specialness does not settle (b). Brady–Soroko's special Hydra analogues are also not the entire original family.

This source contract and preliminary literature audit do not establish novelty. No paper, Zenodo deposit, tracker update, git action, or external communication has been performed in this subtask.

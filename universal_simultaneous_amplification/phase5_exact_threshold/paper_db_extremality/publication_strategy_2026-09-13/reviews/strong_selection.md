# Independent strong-selection and low-order review

Checkpoint: 2026-09-14 00:40 UTC (2026-09-13 local). Bounded review completion: 100%. This is a publication-readiness assessment, not a claim that the open global extremality problem is solved. No manuscript changes or external communications were made.

## Scope and conclusion

I read sections 02, 05, 06 and appendices B and C directly, before consulting prior review dispositions. I independently reconstructed the strong-selection coefficient and checked the triangle formula against exact first-step systems. I also checked the prior theorem against its primary publication. Within this scope I found **no substantive proof defect or overclaimed quantifier**. The strongest additional reliability evidence from this review concerns the complete-support expansion and triangle theorem. The printed K4 positivity argument is sound conditional on its stated elimination identities; I did not independently regenerate the complete K4 symbolic elimination in this bounded review.

## Strong-selection theorem

The proof has the right normalization and orientation: weights are source-to-target; the stochastic kernel is indexed target-to-parent. At zero inverse fitness, every singleton has extinction probability 1/n, whereas every mutant set of size at least two fixates on complete directed support. Every transient state has a route to absorption, so finite-state analytic perturbation applies even though the stochastic interpretation itself only uses nonnegative inverse fitness.

Differentiating the first-step equations correctly gives zero first-order extinction for sets of size at least three. The pair coefficient is (a_ij+a_ji)/(n(n-2)). At a singleton the changing holding time contributes the O_i/n² term; omitting that term would produce a wrong answer, but the paper includes it. Averaging gives total incoming heterogeneity divided by n²(n-2). The pairwise squared-difference identity is an exact identity, and its equality condition is incoming-column constancy, not global equality of all displayed directed weights. Incoming-column normalization therefore removes precisely the equality gauge the theorem identifies.

The n=3 boundary works: the pair transitions directly to the absorbing full state. The n=2 exception is necessary and correctly separated. Vanishing weights cannot be substituted into the complete-support asymptotic formula: its constants need not remain controlled there. The paper treats this boundary separately. Uniform singleton initialization, looplessness, fixed weights, and fixed n are essential hypotheses and are stated.

The source-component argument is correct. Multiple source components prevent fixation from a singleton. With one proper source component, a singleton outside it cannot fixate, and an initial mutant inside it must reproduce before its own death. The stated bound follows. This proof does not incorrectly assume eventual absorption into only the two consensus states for arbitrary reducible kernels.

A possible simplification, **not a correction**, is to use the same elementary first-gain argument on every initial vertex of any incomplete directed support:

    rho(P,r) <= (1/n) sum_i s_i^+/(s_i^+ + 1) < (n-1)/n.

At least one missing directed edge makes the last inequality strict. In fact its gap is at least 1/[n²(n-1)]. This proves eventual suppression for every incomplete support directly, without a condensation-DAG case split. Tkadlec et al. should still receive credit for the earlier, sharper noncomplete-support result. The existing presentation is correct and does not need to be changed merely to use this shortcut.

## Independent exact computation

I wrote an independent in-memory rational-arithmetic solver, importing no project solver or discovery script. For each nontrivial mutant subset S, it constructs the transition probabilities directly by uniformly selecting the dead target v and using mutant-parent probability a/(a+epsilon*b), where a is total incoming mutant weight and b incoming resident weight. It solves the zeroth-order extinction system and its derivative over Python Fractions.

For n=3,4,5,6, take zero diagonal and W_ij = (3i+7j+ij) mod 17 + 1 off diagonal, using indices 0 through n-1. The averaged extinction derivatives obtained directly were:

| n | Exact derivative |
|---|---|
| 3 | 1403/1260 |
| 4 | 684893/565760 |
| 5 | 482772331/306306000 |
| 6 | 199161601/103783680 |

Each exactly equaled T_dir/[n²(n-2)]. Every singleton zeroth-order extinction was exactly 1/n, and every subset of size at least three had exactly zero first derivative. These are independent finite-size checks, not an all-n proof; the manuscript argument supplies the latter.

For triangles I independently built the six transient-state equations, solved the fixation probabilities, and computed the determinant. I checked equation (6.5) including the normalization P_r = L det(M)/3 on all 27 triples (a,b,c) in {1/3,1,3}³ and all five fitness values {1/2,1,1001/1000,2,10}: **135 exact rational checks passed**. Here M is three times the transient I-Q matrix, exactly the paper’s holding-step-free six-equation matrix. Repeated/equal weights were treated as separate labeled factors in L. Checks below fitness one and at neutrality are identity/boundary tests, not extensions of the stated strict-suppression theorem.

## Low-order algebra and quantifiers

The triangle M-matrix is strictly diagonally dominant with positive diagonal, so its determinant has the required positive sign. The centered identities for U,V,W,Z and the decompositions of A,D,E are algebraically consistent. Nonuniform positive weights imply U>0 and E>0, which supplies strictness for every r>1. At neutrality the fixation difference vanishes as required.

For the K4 appendix, the orbit transition rates match the direct death–Birth rule. As usual, transitions outside the allowed count rectangle are interpreted as zero. The 1+3 expression has a square equality factor and positive remaining coefficients. The 2+2 substitution uses d=(sqrt(x)-sqrt(y))²>=0 and g=sqrt(xy)>0; the only apparently negative grouped coefficient is rewritten as a strictly positive sum. Thus the claimed equality class x=y=1 follows from the displayed coefficient representation. The families do not cover arbitrary six-edge weighted K4, and the paper explicitly says so.

Appendix C correctly separates local all-direction optimality at a single fitness from eventual suppression for each fixed kernel. Neither statement gives a uniform neighborhood or uniform strong-selection threshold across population sizes. The open growing-family question remains open under these results. The fixed-graph ledger is understood with the model’s n>=2, loopless row-stochastic assumptions; for n=2 the only kernel is J_2.

## Exact novelty relative to prior work

Primary source checked: [Tkadlec, Pavlogiannis, Chatterjee and Nowak (2020), Limits on amplifiers of natural selection under death–Birth updating](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007494).

The prior paper’s model assumes strong connectivity. Its Theorem 1 proves eventual suppression on noncomplete directed/weighted support and supplies a threshold of 2N². The immediately following paragraph explicitly leaves weighted complete graphs as the residual possible universal amplifiers. Therefore the present complete-support heterogeneity coefficient, equality characterization and resulting closure address a real residual case. The prior result should not be summarized as already proving the present complete-support statement, nor should the present paper advertise all eventual-suppression theory as new. The introduction currently handles that distinction well.

The author’s own predecessor already publicly released the strong-selection and low-order pieces. The manuscript explicitly discloses and integrates them. Their incorporation is not an independent additional novelty event; the paper-level impact assessment should count the integrated theorem suite and especially the new fitness-two local theorem, subject to its separate verification.

## Publication and Lean implications

These sections supply a credible specialist contribution. **Conditional paper score: 7/10 (strong specialist)** if the separate all-n full-directed local-curvature argument withstands review. The strong-selection closure alone is useful but close to an explicitly remaining case of an established theorem; combined with low-order certificates it is closer to **6/10** than a major-subfield breakthrough. I see no basis in these sections alone for **8/10**. An eventual global all-kernel extremality theorem, a uniform structural theorem, or broad uptake of a reusable technique could change that assessment; those are not current results.

Full Lean formalization is not a publication prerequisite for these sections. The finite-state perturbation argument is short, and exact rational/certificate replay supplies useful checkability for the algebra. Formalizing only the final polynomial inequalities would certify a narrow layer while leaving the Markov-chain-to-polynomial derivation outside the kernel. If resources are limited, prioritize a coherent independent verification of the full all-n Hessian proof and external specialist assessment before a large Lean project. A scoped Lean project could later target the normalized strong-selection theorem end to end, but its infrastructure cost should be judged against its limited extra publication value.

The next publication-facing action is to make the new-versus-prior theorem boundary and the proof/certificate dependency map easy for a specialist reader to assess, then seek substantive mathematical feedback through the human user. There is no correctness reason in the reviewed sections to defer journal submission for months, await citation counts, or complete Lean first. Timing remains conditional on the separate local-theorem and reproducibility reviews.

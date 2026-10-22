# Source and theorem interfaces

Checked 9 October 2026 UTC. This is a bounded primary-source review, not a worldwide novelty or openness certificate. The candidate's proof is self-contained apart from standard rational LP, submodular minimization, and exact polyhedral oracle results listed below.

## Exact target

Michele Conforti, *Combinatorial Mixed-Integer Programming*, Oberwolfach Report 51/2008, printed pp. 2904–2905, Problem 1.

https://ems.press/content/serial-article-files/46195

The model has rational demands, a specified integer-coordinate set, and unrestricted real signs. The problem asks about linear optimization and convex-hull membership. Its arbitrary-real wording for the query is made finite by the explicit rational binary input model in the candidate. The report already records polynomial algorithms for trees and the half-integral setting; it explains the dependence of a formulation on the common denominator. Its different Conjecture 2 concerns intersection of subtree hulls and is not this target. The report's short-certificate remark by itself does not supply all bit-size or oracle-equivalence hypotheses.

## Prior network formulation

M. Conforti, M. Di Summa, F. Eisenbrand, L. A. Wolsey, *Network Formulations of Mixed-Integer Programs*. Author manuscript dated 11 March 2008; journal version Mathematics of Operations Research 34 (2009), 194–209.

https://www.math.uwaterloo.ca/~bico/bellairs/network.pdf
https://doi.org/10.1287/moor.1080.0354

Read the abstract/introduction, the network-dual reformulation, Theorems 5 and 7, Corollary 8, the exponential-fractionality discussion, and Sections 7.5 and 8. The tractable structural class has at most two nonzeros per row after appropriate sign changes. The NP-completeness theorem concerns mixed network flows and two nonzeros per column. Corollary 8 is polynomial in the numerical denominator D, which is insufficient for arbitrary binary rational input. None of these prior assertions supplies the general polynomial algorithm claimed by the candidate.

## Projected formulations

M. Conforti, L. A. Wolsey, G. Zambelli, *Projecting an Extended Formulation for Mixed-Integer Covers on Bipartite Graphs*, Mathematics of Operations Research 35 (2010), 603–623. The inspected author manuscript is dated November 2008, revised November 2009.

https://personal.lse.ac.uk/Zambelli/papers/mix-tree.pdf
https://doi.org/10.1287/moor.1100.0454

Read the original model and the general-complexity discussion in the introduction, and inspected the named network-dual equivalence/formulation interfaces. This is the exact free-sign model. The manuscript explicitly leaves general optimization complexity unknown and describes a formulation polynomial in |E| and the numerical k. Its later special-set facet descriptions do not themselves settle the general binary-input question. The publisher metadata verifies the journal identity; the privately retained PDF is the distinct author manuscript, not asserted byte-identical to the version of record.

## Algorithmic dependency: submodular minimization on a ring family

Alexander Schrijver, *A Combinatorial Algorithm Minimizing Submodular Functions in Strongly Polynomial Time*, JCTB 80 (2000), 346–355, especially Section 6 of the author manuscript, pp. 6–7.

https://homepages.cwi.nl/~lex/files/minsubm6.pdf
https://ir.cwi.nl/pub/2108

The interface needs a rational-valued submodular oracle on a ring family, its minimal member, and its minimal member containing each ground element when one exists. Section 6 was read completely. It reduces such minimization to ordinary submodular minimization, rather than assuming unknown feasible oracle arguments can be discovered for free. Candidate Sections 4–6 provide the exact value oracle and all the domain data on at most 2n² elements. The finite checker does not implement this polynomial algorithm; the candidate invokes the established theorem.

## Algorithmic dependency: exact optimization to separation

M. Grötschel, L. Lovász, A. Schrijver, *Geometric Algorithms and Combinatorial Optimization*, second edition, Theorem 6.4.9.

https://link.springer.com/book/10.1007/978-3-642-78240-4

The required exact theorem for well-described, possibly unbounded rational polyhedra was also inspected in the author exposition M. Grötschel and J. Nešetřil, *The Mathematics of László Lovász*, Section 11, printed p. 32:

https://www.zib.de/userpage/groetschel/pubnew/groetschel-nesetril.pdf

Candidate Section 7 proves closed rational polyhedrality and a polynomially computable facet-size bound. Its optimizer returns exact rational minimizers or detects unboundedness. The application uses strong optimization to strong separation, hence membership. It does not equate arbitrary strong-membership and optimization or rely on an unchecked weak-oracle reduction. The full book proof is an established dependency, not independently re-proved here.

Independent-audit addition: the actual 1988 book was subsequently retrieved and inspected at https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf. Definitions 6.2.1–6.2.2 (printed pp. 162–163) and Theorem 6.4.9 with its proof (printed pp. 179–180) supply the same required established result. Strong optimization may return a nonvertex exact optimum and improving recession directions. The current proof records this verified earlier edition and interface; this is no new dependency.

## Related convexity literature and attribution boundary

Takamatsu, Hara and Murota, *Continuous/Discrete Hybrid Convex Optimization and Its Optimality Criterion*, 2004; author English translation, Proposition 2 and Theorem 1.

https://kzmurota.fpark.tmu.ac.jp/paper/THM04hybridLenglish.pdf

This earlier work proves preservation of discrete L-natural convexity after minimizing out continuous variables and supplies an optimality criterion. It explicitly lists development of an optimization algorithm as future work. Thus partial-minimization convexity is prior mathematical machinery, not claimed as a newly invented principle in this packet. The final candidate uses an elementary explicit proximity bound and a finite submodular domain rather than needing an unverified L-convex scaling algorithm interface.

Yu and Küçükyavuz, *Convexification of classes of mixed-integer sets with L-natural-convexity*, arXiv:2511.19754v2, revised 9 September 2026.

https://arxiv.org/abs/2511.19754v2

The introduction and scope were inspected. It treats epigraph convexification, mixing sets, continuous mixing sets, and variants, and credits the older hybrid-convexity literature. No exact general free-sign bipartite classification was identified there in this bounded reading. This is an arXiv manuscript, with no journal/referee status inferred.

Murota's 2009 survey was inspected as background, but no theorem from it is essential to the frozen proof:

https://kzmurota.fpark.tmu.ac.jp/paper/DCAbonn09.pdf

The 2024/2026 Kawase–Nishimura–Sumita hybrid result concerns symmetric strictly convex minimization on a Minkowski sum of an integral base-polyhedron and an M-convex set. Its hardness conclusion cannot be transferred to this difference-constraint linear objective model:

https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2024.96

## Limits

No exact prior full classification was located in this bounded check. That is not a novelty guarantee. The separate subtree-hull conjecture and inaccessible indexed claims about it were neither adopted nor re-investigated as this problem. No mathematical disposition was transferred from unrelated network-flow, unsplittable-flow, or mixed M-convex problems.

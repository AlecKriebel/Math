# Individual candidate assessments

These are desk assessments, not verified readiness decisions. All success estimates are subjective and low-confidence. Most corpus entries have not received this review.
The live order is in [QUEUE.md](QUEUE.md); these notes include demotions and review holds as well as promising candidates.

## 30004033 — Fractional Coloring of Subcubic Triangle-Free Planar Graphs

Code: `OWR-16763-006`. EV: 0.0960; sensitivity range 0.0144–0.3600. Impact 6/10; assumed full-solution probability 2.00%; validity/open/novelty prior 80%.

**Why this priority:** A precise extremal claim with exact finite counterexample certificates and reusable coloring methods. Long history and a recent 11/4 bound make a full proof substantially harder than a small-instance search.

**Exact remaining gap:** The universal 8/3 bound, not the proved 11/4 or nonplanar 14/5 bounds.

**First check or experiment:** Recover the 2025 proof and its excluded configurations; compare exact fractional-coloring LP certificates on small planar subcubic graphs. A finite search only resolves the claim if it finds a verified counterexample.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2019/1), [2](https://www.advancesincombinatorics.com/article/133707-11-4-colorability-of-subcubic-triangle-free-graphs)

## 30000162 — Recognition and Eutaxy Testing of Bacher Matrices

Code: `OWR-782-003`. EV: 0.0910; sensitivity range 0.0126–0.3570. Impact 4/10; assumed full-solution probability 3.50%; validity/open/novelty prior 65%.

**Why this priority:** Recognition, reconstruction, and eutaxy connect explicit integer matrices with convex feasibility. Symbolic linear algebra and exact optimization give useful AI tools.

**Exact remaining gap:** An algorithm with the source-required scope and speed; small-dimensional recognition alone does not settle the full target.

**First check or experiment:** Recover the definition of Bacher matrix and input encoding; derive necessary reconstruction constraints and test them on known lattice examples.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2005/01), [2](https://jamartin.perso.math.cnrs.fr/Publications/weakeut.pdf)

## 30005440 — Multiplicative p-Groups of Braces

Code: `OWR-12697693-011`. EV: 0.0750; sensitivity range 0.0100–0.3000. Impact 5/10; assumed full-solution probability 2.50%; validity/open/novelty prior 60%.

**Why this priority:** Finite group data and algebraic certificates offer a concrete search route; brace realization also has structural significance.

**Exact remaining gap:** The record bundles classification and a minimum counterexample. Finding a single group is not a full resolution of the bundle.

**First check or experiment:** Separate classical from skew braces in the source, identify known counterexamples, and estimate the exact search needed to certify minimality. Stop if the full classification cannot be scoped within budget.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2023/9)

## 30003445 — Minimal Flat Extension Orders for Truncated Moments

Code: `OWR-15219-015`. EV: 0.0600; sensitivity range 0.0080–0.2400. Impact 4/10; assumed full-solution probability 2.50%; validity/open/novelty prior 60%.

**Why this priority:** Moment matrices permit exact rank and positivity checks; instance-sensitive extension bounds could be useful beyond a single example.

**Exact remaining gap:** A precise instance-sensitive estimate; a successful numerical extension is neither a worst-case theorem nor a minimality certificate.

**First check or experiment:** Recover representability hypotheses and the meaning of estimate; test rational low-degree sequences with exact PSD/rank certificates.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2017/14)

## 30004906 — Approximating Maximum Nonsymmetric Principal Subdeterminants

Code: `OWR-8415356-017`. EV: 0.0585; sensitivity range 0.0081–0.2295. Impact 6/10; assumed full-solution probability 1.50%; validity/open/novelty prior 65%.

**Why this priority:** A quantitative determinant approximation target has clear algorithmic and proof artifacts. Numerical counterexamples can expose failed exchange inequalities.

**Exact remaining gap:** The general nonsymmetric 2^{O(k)} approximation guarantee; do not confuse approximation ratio with running time in the dataset summary.

**First check or experiment:** Read the workshop formulation and subsequent local-search results; test candidate exchange inequalities on small rational matrices with PSD symmetric part.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2021/53)

## 30001163 — Equality Cases for Universal Eigenvalue Mean Inequalities

Code: `OWR-3389-016`. EV: 0.0405; sensitivity range 0.0045–0.1755. Impact 3/10; assumed full-solution probability 3.00%; validity/open/novelty prior 45%.

**Why this priority:** A sharp equality question is narrower than proving a new inequality and may yield to tracing equality conditions.

**Exact remaining gap:** Existence or nonexistence of a domain attaining the exact displayed inequality; boundary conditions and normalizations must be checked.

**First check or experiment:** Recover the source derivation and audit each equality condition before computing spectra.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2009/06)

## 20001225 — Markov-basis complexity depends on representation

Code: `AIM-COMPUTATION-0063`. EV: 0.0050; sensitivity range 0.0006–0.0210. Impact 5/10; assumed full-solution probability 0.20%; validity/open/novelty prior 50%.

**Why this priority:** Representation and output-size conventions are not fixed; the prior report expressly leaves the general complexity question open.

**Exact remaining gap:** No verified route to the complete source problem within the fixed budget.

**First check or experiment:** Inspect exact source and prior report; require a new mechanism before launching a full attempt.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://aimath.org/WWN/compalgstat/compalgstat.pdf)

## 20001228 — Equality constraints do not characterize hidden-variable models

Code: `AIM-COMPUTATION-0066`. EV: 0.0050; sensitivity range 0.0006–0.0210. Impact 5/10; assumed full-solution probability 0.20%; validity/open/novelty prior 50%.

**Why this priority:** A general hidden-variable model description needs a precise representation and complexity target; elementary equality obstructions do not solve it.

**Exact remaining gap:** No verified route to the complete source problem within the fixed budget.

**First check or experiment:** Inspect exact source and prior report; require a new mechanism before launching a full attempt.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://aimath.org/WWN/compalgstat/compalgstat.pdf)

## 30002178 — Lower Bounds for Sums of Roots of Unity

Code: `OWR-12014-013`. EV: 0.0039; sensitivity range 0.0005–0.0153. Impact 6/10; assumed full-solution probability 0.10%; validity/open/novelty prior 65%.

**Why this priority:** Algebraic-number computations provide examples, but a bound uniform in the conductor and arbitrary fixed m is a deep global target.

**Exact remaining gap:** A polynomial lower bound for every fixed m, not just an isolated small m or finite conductor range.

**First check or experiment:** Compare norm-based exponential bounds with the required polynomial bound; reject routes that merely restate a separation conjecture.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2012/42)

## 20001254 — Prime-factor advice in power-residue quotients

Code: `AIM-COMPUTATION-0092`. EV: 0.0030; sensitivity range 0.0004–0.0126. Impact 6/10; assumed full-solution probability 0.10%; validity/open/novelty prior 50%.

**Why this priority:** Finding residue advice is the central difficulty; a reduction assuming that advice supplies no solution mechanism.

**Exact remaining gap:** No verified route to the complete source problem within the fixed budget.

**First check or experiment:** Inspect exact source and prior report; require a new mechanism before launching a full attempt.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://aimath.org/WWN/primesinp/primesinp.pdf)

## 30004914 — Deterministic Optimization of Top-$k$ Perfect-Matching Edges

Code: `OWR-8415356-025`. EV: 0.0028; sensitivity range 0.0004–0.0105. Impact 7/10; assumed full-solution probability 0.05%; validity/open/novelty prior 80%.

**Why this priority:** Demoted after literature check: the apparent optimization target is polynomial-time equivalent to Exact Matching under the relevant weight assumptions.

**Exact remaining gap:** General deterministic derandomization; restricted graph classes or equivalent reformulations do not resolve it.

**First check or experiment:** Read the reduction and identify a materially new mechanism before investing in the full target.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://arxiv.org/abs/2209.09661), [2](https://arxiv.org/abs/2510.12552), [3](https://doi.org/10.3929/ethz-b-000675444)

## 30002066 — Random Triangulations and Exchangeable Clique Complexes

Code: `OWR-11786-022`. EV: 0.0025; sensitivity range 0.0003–0.0105. Impact 5/10; assumed full-solution probability 0.10%; validity/open/novelty prior 50%.

**Why this priority:** Sampling triangulations and classifying homotopy groups are separate broad tasks requiring individual formalization.

**Exact remaining gap:** No verified route to the complete source problem within the fixed budget.

**First check or experiment:** Inspect exact source and prior report; require a new mechanism before launching a full attempt.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2012/24)

## 30000785 — Explicit Polynomial Maps Escaping Low-Degree Images

Code: `OWR-1587-005`. EV: 0.0020; sensitivity range 0.0002–0.0084. Impact 8/10; assumed full-solution probability 0.05%; validity/open/novelty prior 50%.

**Why this priority:** Explicit elusive-map constructions touch major algebraic complexity barriers; keyword-level constructibility is misleading.

**Exact remaining gap:** No verified route to the complete source problem within the fixed budget.

**First check or experiment:** Inspect exact source and prior report; require a new mechanism before launching a full attempt.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2007/31)

## 30004556 — Maximal Proof-Search Algorithms on Natural Tautology Sets

Code: `OWR-2654830-011`. EV: 0.0018; sensitivity range 0.0002–0.0073. Impact 7/10; assumed full-solution probability 0.05%; validity/open/novelty prior 50%.

**Why this priority:** General maximal proof-search algorithms are a foundational complexity target with no concrete short route identified.

**Exact remaining gap:** No verified route to the complete source problem within the fixed budget.

**First check or experiment:** Inspect exact source and prior report; require a new mechanism before launching a full attempt.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2020/34)

## 20002355 — A promise-to-total bridge for effective bounds on finite integral point sets

Code: `AIM-LOGIC-0131`. EV: 0.0015; sensitivity range 0.0002–0.0063. Impact 6/10; assumed full-solution probability 0.05%; validity/open/novelty prior 50%.

**Why this priority:** The prior report transfers the difficulty to a height or outside-box oracle, leaving the central existence question unsupported.

**Exact remaining gap:** No verified route to the complete source problem within the fixed budget.

**First check or experiment:** Inspect exact source and prior report; require a new mechanism before launching a full attempt.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://aimath.org/WWN/hilberts10th/hilberts10th.pdf)

## 30003049 — Polynomial Algorithms for Mean-Payoff Games and Linear Programming

Code: `OWR-14215-001`. EV: 0.0008; sensitivity range 0.0001–0.0034. Impact 8/10; assumed full-solution probability 0.02%; validity/open/novelty prior 50%.

**Why this priority:** Two major unrestricted algorithmic problems are bundled together; solving easy instances gives no short route.

**Exact remaining gap:** No verified route to the complete source problem within the fixed budget.

**First check or experiment:** Inspect exact source and prior report; require a new mechanism before launching a full attempt.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2016/7)

## 30003833 — Inverse-Galois and Decidability Problems for Profinite Groups

Code: `OWR-16166-010`. EV: 0.0007; sensitivity range 0.0001–0.0029. Impact 7/10; assumed full-solution probability 0.02%; validity/open/novelty prior 50%.

**Why this priority:** Several broad Galois and profinite-group problems are bundled into one record.

**Exact remaining gap:** No verified route to the complete source problem within the fixed budget.

**First check or experiment:** Inspect exact source and prior report; require a new mechanism before launching a full attempt.

**Holds:** None detected; readiness review still required.

**Sources:** [1](https://doi.org/10.4171/owr/2018/25)

## 20000603 — Log-curvature obstructions and exact interpolation for n at most 2

Code: `AIM-ANALYSIS-0135`. EV: 0.0480; sensitivity range 0.0032–0.2400. Impact 4/10; assumed full-solution probability 4.00%; validity/open/novelty prior 30%.

**Why this priority:** Prior AI work offers a possible root-semigroup route, but the literal existence question can be read as already refuted for arbitrary data. A general characterization or n=3 result would be a separately scoped contribution.

**Exact remaining gap:** Full feasibility characterization versus merely reproducing low-degree cases or a known obstruction.

**First check or experiment:** Recover source interpretation, independently check the prior n<=2 proof, and define the unsolved target explicitly.

**Holds:** target_scope_review

**Sources:** [1](http://aimpl.org/hyperbolicpoly/1/), [2](https://math.hawaii.edu/~tom/mathfiles/interp.pdf)

## 30001067 — Rotational Matching Complexity for Planar Point Sets

Code: `OWR-2090-020`. EV: 0.0300; sensitivity range 0.0020–0.1500. Impact 4/10; assumed full-solution probability 2.50%; validity/open/novelty prior 30%.

**Why this priority:** Parametric assignment has computational experiments, but the attached literature assessment discusses matroid connectivity rather than rotational matching.

**Exact remaining gap:** Correct literature status and full multi-part target.

**First check or experiment:** Recover the report passage and derive the sinusoidal cost envelope; audit known bounds.

**Holds:** statement_literature_mismatch

**Sources:** [1](https://doi.org/10.4171/owr/2008/44)

## 30001497 — Hilbert Polynomials of Homogeneous Ideals

Code: `OWR-4340-008`. EV: 0.0200; sensitivity range 0.0020–0.1200. Impact 2/10; assumed full-solution probability 5.00%; validity/open/novelty prior 20%.

**Why this priority:** The short Hilbert-polynomial existence statement and the attached literature assessment describe different-looking targets. Classical numerical characterization may already settle the literal question.

**Exact remaining gap:** Recover the actual ring, grading, and constraints before treating an easy construction as novel.

**First check or experiment:** Locate the original passage and check classical Hilbert-polynomial admissibility.

**Holds:** statement_literature_mismatch

**Sources:** [1](https://doi.org/10.4171/owr/2010/27)

## 30001382 — Nonmonotonicity of Expected Random Simplex Volume

Code: `OWR-4136-005`. EV: 0.0120; sensitivity range 0.0012–0.0720. Impact 2/10; assumed full-solution probability 3.00%; validity/open/novelty prior 20%.

**Why this priority:** Later primary work settles failure of monotonicity in dimension three. The specific half-ball construction may still be a distinct target, but its impact and novelty need reassessment.

**Exact remaining gap:** Whether this exact pair of bodies was analyzed; do not claim a new resolution of the general three-dimensional question.

**First check or experiment:** Compare the proposed half-ball family against the later counterexample construction.

**Holds:** later_resolution_scope_review

**Sources:** [1](https://www.mathematik.uni-osnabrueck.de/fileadmin/mathematik/documents/AG_Analysis/kunis/KuReRe18.pdf), [2](https://doi.org/10.4171/owr/2009/53)

## 30003187 — Sublinear Membership Testing in Two-Generator Matrix Groups

Code: `OWR-14745-006`. EV: 0.0105; sensitivity range 0.0009–0.0495. Impact 3/10; assumed full-solution probability 1.00%; validity/open/novelty prior 35%.

**Why this priority:** Potentially concrete, but sublinear depends critically on whether input size means bit length or sum of absolute entries.

**Exact remaining gap:** Align source complexity convention, determinant-one promise, fixed versus input K, and existing algorithms.

**First check or experiment:** Compare the 2017 membership algorithm to the OWR wording before attempting anything.

**Holds:** complexity_model_review

**Sources:** [1](https://shpilrain.ccny.cuny.edu/2x2matrices.pdf), [2](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.51)

## 20001350 — Finite-kernel entropy rescaling and obstructions to intermediate SFT spectra

Code: `AIM-DYNAMICAL_SYSTEMS-0008`. EV: 0.0025; sensitivity range 0.0003–0.0105. Impact 5/10; assumed full-solution probability 0.10%; validity/open/novelty prior 50%.

**Why this priority:** A classification for all relevant amenable groups remains open; the displayed normalization and sign conventions also require source correction.

**Exact remaining gap:** No verified route to the complete source problem within the fixed budget.

**First check or experiment:** Inspect exact source and prior report; require a new mechanism before launching a full attempt.

**Holds:** formulation_review

**Sources:** [1](http://aimpl.org/groupdynamorigin/2/)


# Final source-gate disposition for 30001005

Checked 3 October 2026 UTC. This is a source-scope assessment, not a proof attempt.

## Recommendation

**Hold the catalogue entry for source repair; do not mark the original problem solved, and do not start a five-turn campaign on an invented residual.** Retain the audited classical counterexample to universal smoothing for unrestricted locally finite integral Brakke flows, allowing noncompact data. Its dimension is \(n=7\). Preserve `original_selected_flow_problem_resolved: false` and `turns_used: 0`.

The gate fails for a concrete reason: the record changes an announcement with a selected-flow qualification into a given-flow, high-dimensional conjunction without specifying the weak-flow class. The accompanying assertion that the unrestricted dimensional statement remains open is not justified by the cited sources. There are related mathematical questions, but they cannot be substituted for this record without choosing additional hypotheses and a new exact conclusion.

This recommendation is not a claim that no open problem exists in this area. It is a conclusion about the evidence needed to authorize this exact entry as an open research target.

## A. Four distinct assertions

1. **Given-flow universal statement.** For every allowed initial hypersurface and every allowed flow from it, require both expander asymptotics and short-time smoothness. This is the quantifier structure of the pinned catalogue's “let ... be a mean-curvature flow” formulation. It does not specify which weak flows are allowed. Under the unrestricted integral-Brakke interpretation, the stationary cone disproves the smoothing clause.
2. **Existence of a selected smoothing flow.** For every datum, construct at least one smooth evolution. One nonsmoothing flow is not a counterexample to this assertion. The original certificate's opening inadvertently used this existential phrasing; it has been corrected in this revision.
3. **Canonical outermost flows.** Construct the inner and outer flows from the level-set evolutions of the two regions and ask about their short-time behavior. These are specific choices, not all Brakke evolutions.
4. **Forward asymptotics alone.** Ask whether parabolic blow-ups are expanders, or whether they converge uniquely to the cone's outermost expanders. This removes the smoothing clause, requires a convergence mode, and can make sense for singular limits. It is not the catalogue conjunction.

The four statements are not interchangeable. In particular, a singular cone can satisfy exact expander scaling without ever becoming smooth.

## B. Original OWR announcement: what is and is not specified

Source: Ilmanen, *Relative Expander Monotonicity and MCF with Singular Initial Data*, [OWR report 34/2008](https://ems.press/content/serial-article-files/46179), printed p.1937, PDF page 5.

The datum is a hypersurface with isolated points modeled on regular hypercones. The abstract considers a flow from it, asks separately about asymptotic expansion and smoothness, and announces three theorems. The first has all-dimensional self-expanding tangent flows. The second has an all-dimensional construction with compact-replacement-minimizing expanders. The third asserts smoothness only for **the flows of Theorem 2**, in \(n\leq6\).

The one-page contribution gives no formal weak-flow definition, no compactness requirement, no modern inner/outer-flow definition, and no convergence topology. It does not explicitly pose an \(n\geq7\) open conjecture. It is therefore impossible to recover a unique modern selected-flow class merely by reading its opening sentence. Nor can its all-dimensional Theorem 1 announcement be silently reclassified as an unresolved theorem because a full proof was not found.

The catalogue added the high-dimensional restriction to its cleaned statement and combined the two questions. Those changes do not produce a source-certified open target.

## C. The 2003 conjecture cited by the modern resolution

Ilmanen's [*Problems in Mean Curvature Flow* (2003), Problem 16](https://people.math.ethz.ch/~ilmanen/classes/eil03/problems03.pdf) is in the section on surfaces in \(\mathbb R^3\). It asks for construction of a smooth short-time evolution from an isolated singular point with smooth tangent cone. The primary-source indexed text was accessible; a complete web-rendered PDF was not. This access limitation is explicit.

The 2024 paper identifies its Theorem 1.3 as resolving this conjecture. Consequently, describing Problem 16 itself as an open \(n\geq7\) problem would lose both its original dimension and its constructive quantifier. This does not mean the 2008 abstract and the 2003 problem are identical formulations.

## D. Precisely identified modern theorem regimes

Source: Chodosh–Daniels-Holgate–Schulze, [*Mean curvature flow from conical singularities*](https://link.springer.com/article/10.1007/s00222-024-01296-8), Invent. Math. 238 (2024), 1041–1066. Full publisher text inspected.

The data are embedded hypersurfaces smooth off the conical points, with smooth embedded closed links and smooth convergence to the tangent cone away from its vertex. Inner/outer flows are time slices of the boundaries of the space-time level-set evolutions of complementary closed regions. Their Brakke representatives are unit-regular cyclic limits from one-sided smooth approximations, as in §§2.3 and 4. They are not arbitrary Brakke flows. Section 4 presents the compact-region case; footnote 3 explicitly permits noncompact data in the extended framework.

For \(2\leq n\leq6\), Theorems 1.2–1.4 give short-time outermost regularity, local smooth convergence of rescaled outermost slices to the corresponding expanders, and uniqueness when the cone does not fatten. The paragraph following Theorem 1.2 extends the results to higher dimensions **assuming smooth outermost expanders**. Theorem 4.1 also states convergence of the associated dilated Brakke flows. These are established regimes, not remaining targets.

Section 2.6 permits singular sets of dimension at most \(n-7\) in higher-dimensional outermost expanders. That is a regularity limitation, not a statement that all higher-dimensional cones regularize or that a specific singular-limit conjecture is currently open.

## E. Cones themselves versus perturbations of cones

For initial data exactly equal to a cone, uniqueness of the level-set flow and scaling equivariance imply

\[
F_t(C)=\sqrt t\,F_1(C).
\]

Thus canonical cone evolution already has exact set-theoretic self-similarity in every dimension. The formula alone gives no smoothness. The difficult-looking extension would concern a general hypersurface merely tangent to a cone, identification of its forward limits with particular singular outermost expanders, and possibly uniqueness of those limits. Those are additional choices, not contained in the formula.

The modern paper's §1.2 discussion of difficulties with forward monotonicity is explicitly about a **method**. The authors then prove their smooth-expander result using barriers. That methodological discussion must not be quoted as a declaration that their proved theorem remains open, or used by itself to certify the higher-dimensional singular-expander extension as a distinct current open problem.

## F. Forward-asymptotic literature checked

### F1. A historical general conjecture

Ilmanen's [1998 lecture notes](https://math.jhu.edu/~js/Math745/ilmanen.mcflow.pdf), printed pp.24–25, conjecture subsequential self-expanding limits of forward parabolic blow-ups for mean-curvature flows, including singular flows. This is an actual historical conjecture, unlike the unsourced inference from a dimension cutoff. It is much broader than the catalogue entry, does not assert smoothing, and its short formulation still does not fix a modern admissible weak-flow class. The notes also distinguish a flow that is not exactly self-similar from its limiting behavior under blow-up.

This historical statement does not by itself certify a precise current residual for the 2008 entry. Its status cannot be read off from an unsuccessful search for a general theorem.

### F2. A proved forward-asymptotic result with trapping

Bernstein–Wang, [*Relative expander entropy in the presence of a two-sided obstacle and applications*](https://arxiv.org/abs/1906.07863), Adv. Math. 399 (2022), 108284, Theorem 1.6, provides subsequential measure convergence to a possibly singular expander for flows from a regular cone satisfying its two-sided expander-trapping hypothesis. The theorem statement was available in the [primary NSF-hosted indexed text](https://par.nsf.gov/servlets/purl/10516097); the full PDF did not render in this source pass. We therefore use only that displayed scope, not an uninspected proof. The trapping hypothesis cannot be dropped or inferred for arbitrary conical initial data.

### F3. Non-self-similar evolution does not refute asymptotic expansion

Chen's [2022 preprint](https://arxiv.org/pdf/2212.10798), Theorems 1.1–1.2, constructs and analyzes flows from cones via ancient rescaled flows tending to smooth expanders. They can be non-self-similar while still asymptotic to an expander as time tends to zero. His §5 derives subsequential convergence using trapping; the setup preceding Propositions 5.2–5.3 uses \(2\leq n\leq6\). Smoothness and genericity enter the stronger classification/uniqueness results. These do not establish unrestricted singular-outermost forward-limit uniqueness in high dimension, and they are not counterexamples to the catalogue's asymptotic clause.

### F4. A different explicitly described unresolved issue

Daniels-Holgate's [2023 thesis](https://wrap.warwick.ac.uk/id/eprint/184820/1/WRAP_Theses_Daniels-Holgate_2023.pdf), introduction, printed pp.5–6 (PDF pp.13–14), explicitly describes as unknown whether non-self-expanding flows from cones can occur as forward tangent flows at conical singularities formed from smooth compact initial data. It also says the thesis's methods do not apply to singular expanders.

The first question has actual historical support, but it concerns a flow before and after formation of a conical singularity, includes a compact smooth initial condition, and is not restricted to the catalogue's \(n\geq7\) range. It is not the same as uniqueness of singular outermost-expander limits. Its current unresolved status was not authenticated by the inspected later sources. We therefore record it as related context, not substitute it as this campaign's target.

### F5. Later primary-source checks

The [2025 non-canonical-flow preprint](https://arxiv.org/html/2510.06979v1) constructs interior Brakke flows in fattening level-set evolutions; its Theorem 1.1 is an existence result, with an explicit weaker starting-data convention for generalized hypersurfaces. It does not identify a high-dimensional singular-expander forward-asymptotic theorem or pose the catalogue's conjunction.

The author’s later [backwards-uniqueness paper, revised January 2026](https://arxiv.org/abs/2507.16805), concerns agreement before an asymptotically conical singular time. [The 2025 closeness paper](https://arxiv.org/abs/2503.11522) likewise gives a backwards rigidity result. [Shao–Zou's 2025 paper](https://arxiv.org/abs/2507.19428) concerns positive-genus expanders in \(\mathbb R^3\). Their displayed abstracts do not settle or formulate the proposed high-dimensional residual. Full proofs of these three papers were not claimed read.

These are bounded checks of relevant current sources. Absence of a matching theorem or conjecture in this set is not a proof of global mathematical open status.

## G. Why there is no five-turn campaign yet

An authenticated remaining target would need, at minimum:

- the specified weak-flow class and its initial-data convergence;
- the geometric hypotheses and dimension range;
- whether the task is existence, all-flow behavior, or a particular outermost selection;
- the precise conclusion and topology of forward convergence;
- a primary source identifying that assertion, and a defensible current-status check.

The supplied catalogue does not determine these choices. The original OWR selection is incompletely specified; the modern smooth-outermost regimes are proved; the unrestricted Brakke smoothing version is classically false. A new statement obtained by deleting smoothing, adding outermost selection, allowing singular limits, and choosing a convergence topology would materially replace the problem.

**Operational disposition:** retain a `blocked`/source-repair hold at zero turns, attach the narrow classical-obstruction certificate, and continue the queue rather than spend five attempts on a newly invented question. No original-problem solution, new theorem, PR, queue mutation, or remote write is certified by this document.

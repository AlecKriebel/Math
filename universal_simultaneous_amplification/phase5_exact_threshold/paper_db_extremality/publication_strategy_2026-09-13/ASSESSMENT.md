# Publication assessment: SimAmpA

Assessment date: September 13, 2026 (Pacific). Scope: this paper only, not the other papers in the supplied workbook.

**Recommendation: 7.3/10 conditional impact. Circulate selectively now, prepare the journal submission in parallel, and aim to submit between September 28 and October 5. Do not make full Lean formalization a submission prerequisite.** The dates are a practical feedback window, not a journal rule or a prediction of acceptance.

The public title is **Local Complete-Graph Optimality at Fitness Two and Strong-Selection Rigidity under Death–Birth Updating**. The workbook uses an earlier title. [Zenodo version 1.0.0](https://doi.org/10.5281/zenodo.22089748) contains the R4 manuscript and reproducibility package. All five public file checksums match the local files, including the PDF and complete referee package. The UTC deposit date is August 25; the recorded August 24 is correct in Pacific time.

## What was reviewed and what the paper establishes

I read the manuscript's model, seven sections, and three appendices, examined its proof/certificate structure, checked its relationship to the primary literature, and commissioned independent adversarial checks of the two main proof families under the repository's research policy. Historical referee records provide additional evidence but are not journal peer review. This task does not claim a fresh end-to-end replay of the frozen package or kernel verification of every theorem.

The model matters: finite loopless graphs, uniform choice of death site, fitness-weighted competition among incoming neighbors, and uniform initial singleton. Normalizing incoming weights yields a row-stochastic kernel P, with the dead target indexing the row. Rescaling all incoming weights at one target has no effect on the process.

| Contribution | Mechanism and scope | Assessment |
|---|---|---|
| Strict local maximality at fitness two | For each n≥3, every nonzero normalized directed tangent direction has negative fixation Hessian at the complete kernel. The neighborhood may depend on n. | Main new theorem and principal reason for specialist interest. |
| Strong-selection rigidity | For fixed complete directed support, the leading deficit is E(P)/[n²(n−2)r], with E a sum of nonnegative squared relative weight differences. E vanishes precisely for the complete normalized kernel. | A sharp equality statement and quantitative closure of an explicit remaining case. |
| Fixed finite graph conclusion | Complete-support expansion plus noncomplete-support obstruction excludes a single finite strict amplifier for every r>1. | Meaningful closure, but most of the noncomplete-support obstruction is prior work. |
| Low-order global results | All positive undirected triangles and two symmetric weighted K4 families suppress for every r>1 unless uniform. | Useful exact supporting results, not a general four-vertex classification. |

The fitness-two proof is substantive. A fair-geometric number of potential parents turns each update into a Boolean OR, giving a union-valued ancestry dual. Its stationary coverage law gives rho=m/n. A marked one-sample chain gives the inverse mean as a stationary collision observable. Stationary perturbation then reduces curvature to a quadratic resolvent expression. Symmetry splits the full tangent space into standard, symmetric-balanced and antisymmetric-balanced components. These are distinct directed perturbations, not just an undirected edge-weight calculation.

The difficult sign step is genuinely all-order: the standard sector uses a finite rational base and analytic tail; the antisymmetric sector uses a monotone Poisson-gradient recurrence; the symmetric sector uses exact solves for N=3,…,39, rational margins for every N=40,…,287, and analytic bounds for N≥288, where N=n−1. Finite samples alone would not establish the theorem. The paper states these boundaries explicitly.

Independent reviewers freshly reconstructed the original forward chain and reproduced all eight displayed normalized sector eigenvalues at n=3,4,5, with zero first derivatives. They also independently reproduced all 248 finite symmetric-phase margins and both all-order discriminant coefficient lists. Separate exact rational calculations checked heterogeneous directed strong-selection coefficients at n=3,4,5,6 and the triangle formula at 135 rational test cases. These provide independent consistency checks, not a substitute for the all-order proof. Fresh review did not exhaust every general-n quotient/boundary identity, all small-order symmetric solves, or the complete K4 eliminations; these remain precisely stated verification limits, not identified errors.

The two major open questions remain open: global complete-graph maximality at r=2, and existence of one growing graph family that eventually amplifies each fixed r>1. The fixed-graph threshold can depend on the graph; neither limit can be exchanged with population size. At n=2 the loopless kernel is unique. Missing edges and self-loops cannot silently be folded into the positive-kernel local proof.

## Impact score

**7.3/10**, with a reasonable judgment range of **6.8–7.6**. This is not a statistical confidence interval. It uses the workbook's stated question: importance within the actual subfield assuming the theorem is correct, novel, and published. Your independent status and use of AI do not enter this conditional score.

The score belongs in the “strong specialist result” band. The full directed all-n local theorem and collision formulation make it more substantial than a narrow finite computation. [Tkadlec et al. (2020)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007494), Theorem 1 and the immediately following paragraph, explicitly leave weighted complete graphs as the remaining fixed-graph possibility. Closing that case deserves credit. It should not be presented as the original discovery of death–Birth transience generally.

I would lower the existing ChatGPT score from 7.8 to 7.3 because the broader global and growing-family questions are not solved, and the biological consequences remain within a particular finite-population updating model. No demonstrated broad adoption of the new method yet supports an 8-level “major subfield advance.” The current public version is worth a serious specialist submission without adding another theorem. Lean would improve assurance, not automatically raise this conditional importance score.

A targeted current-literature search found no clear duplication of the full theorem, but cannot certify exhaustive novelty. A superficially related August 2026 [replacer paper](https://arxiv.org/abs/2608.06552) studies a different neighborhood-aware phenotype in a Birth-death model; its r≥2 bound is not this death–Birth local-extremality statement.

## Best next step and relevant readers

The immediate priority is focused field feedback on novelty and the proof's central reductions. The sheet records a Zenodo upload, but no external feedback or correspondence for this row. That is not proof that nobody has been contacted.

| Priority | Relevant researcher | Why their input would be useful |
|---|---|---|
| First | [Josef Tkadlec](https://sites.google.com/view/pepa-tkadlec/research) | Coauthor of the 2020 obstruction. Best direct fit for whether the complete-support closure and its framing answer the residual question correctly. |
| Second | [Ben Allen](https://www.emmanuel.edu/emmanuel-mathematical-biology-research-embr) | Works on structured-population evolution and general mathematical formulations; coauthor of the transient-dB-amplifier work. Particularly relevant to the fixation/ancestry interpretation and biological positioning. |
| Alternate | [Andreas Pavlogiannis](https://cs.au.dk/~pavlogiannis/) | Coauthor of the same obstruction, with interests in formal verification and evolutionary graph theory. Particularly relevant if the computational certificate structure is the main feedback need. |

These are suggestions for the human user's own decision, not claims of availability, willingness, or endorsement. Start with two closely matched readers rather than a broad campaign. The useful material is the current DOI, PDF and existing claim-to-code map; expert attention should focus on the new theorem, exact prior-work boundary and hardest proof bridge. All external communication remains with the human user. No outreach has been drafted or initiated.

For public comment, the DOI supplies a stable version that readers can discuss, but the deposit alone does not establish that field specialists have read it. Private expert feedback can improve the paper even if nobody produces a public comment. Public recognition should not become a condition for submission.

Use the next two to three weeks for this feedback opportunity and a small submission-readiness pass. Update stale local submission metadata that still assumes bioRxiv, point data/code availability directly to the current DOI and full R4 package, retain the earlier-release provenance, and ensure title/abstract/version agree across submission materials. The public files themselves already match the repository. Keep the explanation of what r=2 local optimality means for fixation prominent. The existing author summary is a useful starting point. Verify author location, abstract length and final source/PDF on the actual submission copy, then replay that frozen copy if it changes.

If a substantive objection arrives, resolve it before submission. If nobody replies, submit on the planned schedule once the ordinary checks are complete. Silence is neither validation nor a reason to wait indefinitely. Do not wait for the companion paper, arXiv endorsement, full Lean, or a solution of the global conjecture.

## Lean: useful selectively, not the next publication gate

**A focused formal certificate would materially strengthen the computer-assisted part. A full formalization is not currently the best use of resources solely to improve journal acceptance.** Acceptance also depends on novelty, clarity and biological/mathematical significance, none of which Lean establishes. The journal's [submission guidance](https://link.springer.com/journal/285/submission-guidelines) expressly accommodates unaffiliated authors and requires disclosure of substantive LLM use; it does not list a proof assistant as a requirement. Preserve the manuscript's candid AI disclosure and human accountability statement.

The strongest first target is the finite symmetric-sector lemma: certify every rational solve and positivity margin across the stated finite ranges, using equations that match the manuscript. Prefer proof-checking exact solution witnesses to implementing an entire computer-algebra system. The success criterion is a theorem with the exact range and positivity conclusion, checked without proof placeholders or unproved bespoke assumptions. The code-to-paper correspondence must be audited separately.

Next priorities would be the quotient-to-physical-Hessian normalization, the polynomial/tail inequalities, and the standard-sector base cases. Formalizing only a convenient sum-of-squares identity in the strong-selection section is a reasonable learning pilot, but would leave the principal computer-assisted trust burden untouched. The complete local theorem would additionally require the Markov-chain/coverage identities, differentiability, full tangent decomposition and all three signs. A theorem assuming these difficult bridges is only conditional formalization.

Lean distinguishes proof terms checked by its kernel from native evaluation with a larger trust base. An axiom report and a precise list of formalized claims should accompany any deliverable; see the official [axiom documentation](https://lean-lang.org/doc/reference/latest/Axioms/) and [tactic reference](https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference/). No Lean implementation was attempted here, so there is no reliable time or cost estimate. Start with a bounded certificate pilot if desired, assess its actual cost, and continue submission work independently.

## Journal and submission timing

The workbook's journal choices stand. Journal of Mathematical Biology is well matched to rigorous new mathematical tools for biological systems, including stochastic processes and graph theory; its [scope](https://link.springer.com/journal/285/aims-and-scope) also asks authors to make the biological meaning accessible. Theoretical Population Biology remains a sensible second choice, with a stronger emphasis on the biological insight from the theory; see its [publisher description](https://shop.elsevier.com/journals/theoretical-population-biology/0040-5809). Neither fit assessment predicts acceptance.

Aim for **September 28–October 5, 2026**, after addressing any concrete feedback and completing the submission-copy checks. An earlier submission is reasonable if those tasks finish sooner. There is no need to wait until the preprint is several months old. Springer Nature's [preprint policy](https://support.springernature.com/en/support/solutions/articles/6000258807-preprints) permits preprints and does not treat them as prior publication. Lack of arXiv or bioRxiv access therefore does not block this route.

## Recorded changes and limits

Only the SimAmpA row is assessed. The revised workbook updates its ChatGPT impact score and rationale, recommended next action, dated Updates entry, and actual preprint server. The Claude score and average formula are retained, so the new arithmetic average is 7.25. Journal choices, unrelated papers and review-completion flags are not re-evaluated. The workbook's earlier title is retained as the user's identifier and its updated public title is recorded in the Updates cell.

This is a publication-strategy assessment with substantial targeted mathematical review, not a replacement for independent human refereeing. No theorem-changing defect has been identified in the reviewed portions. The exact remaining external uncertainty is whether specialists agree with the novelty, significance and full proof/certificate argument.

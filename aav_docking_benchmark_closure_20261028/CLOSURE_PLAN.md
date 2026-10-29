# How to conclude the AAV docking benchmark

Assessment date: 28 October 2026 (America/Los_Angeles).
Upstream audited: [e9d39e3ef1c58647c2bf9dea7dfc90f823198791](https://github.com/Wyattkriebel/AAV-Docking-Benchmark/tree/e9d39e3ef1c58647c2bf9dea7dfc90f823198791).
Status: closure assessment complete; benchmark hypotheses remain untested by the committed docking evidence.

## Recommendation

Finish a bounded, reproducible evaluation of named workflows under specified information and assay conditions. The scientific product should say **when docking works, what fails, and whether scores distinguish independently measured binding alternatives**. A finite study cannot settle universal reliability of all molecular docking algorithms.

The repository already has a strong [protocol](https://github.com/Wyattkriebel/AAV-Docking-Benchmark/blob/e9d39e3ef1c58647c2bf9dea7dfc90f823198791/PROTOCOL.md). The immediate need is to make its design executable, freeze its claims and ground truth, and earn the conclusions with held-out evidence. No experimental performance result follows from a protocol alone.

## What the repository establishes today

- It contains an explicitly true-site-informed AAV9 Vina pilot, geometric/learned pocket outputs, source structures and a proposed confirmatory design.
- Both deposited AAV9 mmCIF inputs are two-byte blank CRLF files. The pilot reads `data/raw/`, while coordinates are deposited directly under `data/`.
- The preparation stage writes receptor PDB files; docking expects receptor PDBQT files. The conversion stage is absent.
- No docking pose files, run metadata, pose metrics or summary results are committed. The pocket outputs alone do not estimate docking accuracy or specificity.
- Therefore the strongest supported present conclusion is that the study is designed in substantial detail, but its scientific answer has not been demonstrated in this repository.

See CODE_AUDIT.md and code_audit/checks.json for independent checks. All 23 retrieved source blobs match upstream Git hashes; see SNAPSHOT_VERIFICATION.json. The snapshot is a local read-only audit copy, excluded from the research-note publication.

## Three claims require three kinds of evidence

| Claim | Required ground truth | Confirmatory endpoint |
|---|---|---|
| The workflow finds a site for a known binder | Experimentally supported sites in the relevant biological assembly | Blind/predicted-site Top-1 and Top-5 recovery, interface coverage and credible surface-patch baselines |
| It returns and ranks the correct pose | Chemically valid, sufficiently complete ligand coordinates with local structural support | Receptor-aligned ligand RMSD, contacts and physical validity, with Top-1/5 and best retained candidate |
| Its scores discriminate molecular recognition | Independently tested binders and tested low/no-binding alternatives in the same assay context | Within-target discrimination or quantitative ranking, compared with size/charge baselines and evaluated on held-out data |

An incorrect pose of a known binder is a **structural decoy**, not a tested nonbinding glycan. An unoccupied surface in one structure is not automatically a biologically impossible site. The original question conflates these possibilities unless they are evaluated separately.

Keep structural-reference and assay-reference cohorts separate when necessary. Require their intersection only for claims that jointly depend on both kinds of ground truth. This avoids discarding useful data merely because every complex lacks every endpoint.

## A concrete route to completion

### 1. Resolve scope and overlap before the large run

Audit the new [ProtGlycanDock paper](https://arxiv.org/html/2610.26009v1), posted 19 October 2026. It already evaluates ten methods with protein/glycan holdouts on a much larger structural dataset. It excludes structures with more than four protein chains, and its Vina arms use predicted receptors and pockets. These choices make assembly and equal-information comparisons relevant distinctions, but do not prove novelty.

The candidate contribution is a controlled link between **assembly completeness, input information, retained-pose coverage/ranking, and assay-backed specificity**. A generic leaderboard or failure-case taxonomy alone is substantially overlapped. Limit claims to the tested methods, or justify a small contemporary baseline extension after the overlap audit.

### 2. Make the development pipeline independently reproducible

Restore valid inputs with versioned downloads and checksums; use a consistent directory layout; supply receptor preparation and atom-change logs; provide one correct command sequence. Add meaningful metric controls: native coordinates give zero RMSD and full native contacts, a known translation produces the expected pose error, atom loss fails visibly, and valid receptor/symmetry transforms preserve the appropriate score.

Reproduce a released external example and the small development cohort before freezing the larger comparison. AAV9 galactose is a useful diagnostic, but a monosaccharide cannot validate glycosidic torsion treatment. This stage is implementation validation, not confirmatory accuracy evidence.

### 3. Freeze references, cohorts, metrics and decisions

Create machine-readable ledgers for complex/family identity, assembly, ligand graph/stereochemistry, atom map, local reference quality, apo/holo provenance, assay labels and exclusions. Distinguish atomic-pose, site-only and assay-only references. Keep reference-derived coordinates/restraints out of blind inputs.

The proposed 24–36 complexes and at least 12 families are a starting inventory, not a statistical guarantee. Choose the intended precision and minimum useful performance before test scoring; size or narrow the claim accordingly. Reserve an untouched cohort if development changes the procedure.

### 4. Run paired comparisons that can explain the outcome

Prioritize predicted-site versus true-site information, ligand-stripped holo versus independently solved apo, and complete neighborhoods versus deliberately incomplete assembly controls. Apply comparable information and budgets to each method. Report failures and unsupported chemistry in the eligible-case denominator, alongside conditional accuracy.

Preserve candidate identities and use a common pool for scorer comparisons. Measure whether near-native candidates are present and whether they are highly ranked. Without access to pre-ranking candidates, an absent near-native returned pose is only “no near-native pose returned”; it does not uniquely identify internal sampling failure.

A native-pose scoring control may expose scoring inconsistency, but is never counted as a docking success. No unvalidated simulation or energy minimization can create missing experimental binding labels.

### 5. Close the specificity arm with qualified public assays

Find tested positives and tested alternatives first, then freeze the evaluation panel. Preserve assay concentration, glycan presentation/linker, valency, ionic conditions and detection limits. Do not pool array signal, binding affinity and cell transduction as one endpoint; do not infer a dissociation constant from docking energy.

Report raw performance and within-target size/charge-matched performance. Matching changes the question and can remove a real contribution of charge, so show both. If claiming a usable classifier, fix its threshold on development data and measure held-out sensitivity/specificity, rather than reporting ranking alone.

[Mietzsch et al. 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC3958061/) is a candidate missing source for assay-qualified controls. It excluded AAV9; its labels cannot be transferred between serotypes. Public structures and qualified public assay data may suffice for this evaluation. If relevant labels cannot be recovered, a structural paper can finish, but the specificity part of the original question remains open.

### 6. End with predeclared positive, negative or inconclusive conclusions

For a useful-performance floor q, a lower confidence bound above q supports the scoped reliability claim; an upper bound below q supports inadequate reliability in that regime; an interval crossing q is inconclusive. For an improvement claim use a prespecified paired margin, not merely a higher point estimate. A descriptive benchmark need not invent a utility threshold.

Average seeds within complexes, then use family-aware summaries and paired uncertainty. Seeds, poses and capsid symmetry copies are not independent biological replications. As an optimistic independent-binomial illustration, even 12/12 successes gives only a 73.5% two-sided 95% lower bound. This is not a direct confidence interval for fractional family-macro outcomes. It shows why a small all-success pilot cannot certify near-universal reliability.

Reproduce every aggregate table from archived inputs and raw outputs; have an independent adversary inspect leakage, atom maps, density uncertainty, exclusions, symmetry, ranking and assay interpretation. Freeze the result when the predefined precision and quality gates are met. Do not keep adding test cases until a favorable result appears.

## What a complete answer would look like

A completed report could state, with actual estimates and intervals: “On held-out families, workflow M recovers sites and poses at measured rates in each information regime; ranking succeeds or fails conditional on retained candidate quality; its scores do or do not discriminate tested binding alternatives beyond the stated baselines.”

Mixed outcomes are scientifically complete if the relevant estimates are adequately supported. A validated counterexample can refute an absolute claim that a favorable docking score guarantees the native interaction. It cannot establish failure of every algorithm or low average performance.

No percentage of the eventual biological discovery can be inferred responsibly from the existing pilot. This assessment is complete; the exact remaining work is reference/assay curation, pipeline repair, frozen confirmatory execution and independent reproduction.

## Supporting independent assessments

- CODE_AUDIT.md — code/data evidence, exact line references and static checks.
- SCIENTIFIC_CLOSURE.md — ground truth, public evidence sources and limits of biological inference.
- STATISTICAL_CLOSURE.md — estimands, uncertainty calculations and falsifiable decision rules.
- RESEARCH_LOG.md — timestamped checkpoints and completion estimates for this assessment.


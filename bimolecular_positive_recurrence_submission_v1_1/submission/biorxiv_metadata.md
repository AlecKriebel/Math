# bioRxiv metadata candidate

This sheet prepares a possible bioRxiv submission under Systems Biology. It
does not claim that the manuscript is eligible, screened, accepted, or posted.

## Core metadata

**Title:**
Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible
Stochastic Reaction Networks

**Author:**
Alec Kriebel

**Affiliation:**
Independent researcher

**Corresponding author:**
Alec Kriebel, <me@aleckriebel.com>

**ORCID:**
<https://orcid.org/0009-0001-9320-500X>

**DOI:**
None. No preprint deposit or DOI registration is authorized by this package.

**Abstract**

Weak reversibility is conjectured to imply positive recurrence for stochastic
mass-action systems. We prove the conjecture for bimolecular networks with one
linkage class, removing the earlier requirement that every species occur in a
pure unary or pure-double complex. For every positive rate vector and every
initial population, weak reversibility makes the reachable set a closed
communicating class. Each nonabsorbing class is positive recurrent, whereas
an absorbing singleton carries its point-mass law; consequently every class
has a unique stationary probability distribution. The closure statement
follows by lifting directed return paths of complexes to population states.
For recurrence, the proof marks the target of the most recently fired channel
and applies a log-factorial potential after subtracting that target. Its
increment is exactly the logarithm of a target/source falling-factorial ratio,
so following the carried target has zero reward. Finite target-following paths
propagate the negative drift of a rare terminal source, while a normalized-log
compactification and a bimolecular top-complex alternative rule out all other
divergent sequences. The same return-cycle construction recovers nonexplosion
directly. Multiple linkage classes and molecularity above two remain open.

**Subject category:**
Systems Biology.

**Result category:**
New Results. The new result is a mathematical theorem about stochastic
biochemical reaction-network models; it is not an experimental result.

**Keywords:**
stochastic reaction network; systems biology; chemical master equation;
positive recurrence; mass-action kinetics; weak reversibility;
continuous-time Markov chain; Foster--Lyapunov method.

**Significance summary:**
Use `submission/biorxiv_significance_summary.md`.

## Scope and research-material declarations

**Life-science relevance:**
The paper studies stochastic mass-action CTMCs used for low-copy-number
biochemical reaction networks. It proves a rate-independent structural
criterion for stationary molecule-count laws. Weak reversibility makes the
population set reachable from any initial state a closed communicating class;
under the additional one-linkage and bimolecular hypotheses, every such class
has a unique stationary probability law. No claim is made that all
biochemical models satisfy these restrictions.

**Data:**
No empirical biological dataset was collected or analyzed. The mathematical
proof is universal. Deterministic code outputs and exact finite calibration
cases accompany the paper, but finite computation is not a substitute for
proof.

**Code and supporting materials:**
The Version 1.1 archive contains the standalone verifier, tests, stable output,
release manifest, reviewer supplement, and clean-clone transcript. Its intended
immutable public package URL is
<https://github.com/AlecKriebel/Math/tree/bimolecular-positive-recurrence-v1.1/bimolecular_positive_recurrence_submission_v1_1>.

**Ethics:**
Not applicable: the work involves no human participants, animals, patient
information, identifiable data, or biological specimens.

**Funding:**
This research received no specific grant from any funding agency in the
public, commercial, or not-for-profit sectors.

**Competing interests:**
The author declares no competing interests.

**Generative-AI use:**
The manuscript contains a concise declaration. Full system, model, date,
access-route, and use details are in
`supplement/ai_use_full_statement.md`, with an intended stable tagged link at
<https://github.com/AlecKriebel/Math/blob/bimolecular-positive-recurrence-v1.1/bimolecular_positive_recurrence_submission_v1_1/supplement/ai_use_full_statement.md>.
Rejected approaches are not part of the final proof. No AI system is an
author, and no independent expert human validation is claimed.

## License and prior-online status

The package reserves rights in the manuscript. bioRxiv offers several reuse
licenses and a no-reuse option. The no-reuse option is consistent with the
present `LICENSE.md`; any Creative Commons selection requires a deliberate
author decision after checking journal compatibility. This sheet does not
make that selection.

Versions 0.3 and 1.0 have been publicly available as unrefereed repository/web
preprints. Version 1.1 has not been deposited on a preprint server. Disclose
the related public versions if a submission interface asks about prior online
versions or text overlap.

Before any deposit, recheck bioRxiv's current screening, duplicate-posting,
version, permanence, licensing, and journal-preprint rules and choose the
posting route deliberately. No upload is authorized by this package.

## Screening risk

bioRxiv accepts mathematical work only when directly relevant to the life
sciences, and its screening guidance emphasizes research manuscripts with new
data or result outputs. The paper has direct systems-biology model relevance
and a new theorem with exact computational artifacts, but no empirical
dataset. Eligibility is therefore a screening judgment, not a fact established
by this package. If bioRxiv declines the manuscript as primarily mathematical,
arXiv is the natural preprint route.

## Policy sources checked 10 August 2026

- bioRxiv scope, categories, posting permanence, and licensing:
  <https://www.biorxiv.org/about-biorxiv>
- bioRxiv screening procedures:
  <https://connect.biorxiv.org/news/2022/06/13/screening_procedures>

The official scope includes Systems Biology and says mathematical work should
be posted only when directly relevant to the life sciences. The screening
description asks whether a submission presents biological research, checks
article type and completeness, and detects material that has appeared online.
Once posted, a bioRxiv article is citable and ordinarily cannot be removed.

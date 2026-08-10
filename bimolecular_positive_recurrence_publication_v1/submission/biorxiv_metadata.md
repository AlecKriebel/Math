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
mass-action systems. For binary networks with one linkage class, this was
previously known under the additional requirement that every species occur in
a pure unary or pure-double complex. We remove that requirement. For every
positive rate vector, the minimal continuous-time Markov chain restricted to
each closed communicating class is nonexplosive. Every nonabsorbing class is
positive recurrent, while an absorbing singleton carries its point-mass law;
hence every closed class admits a unique stationary probability distribution.
The proof marks the target of the most recently fired reaction channel and
applies a log-factorial potential to the residual population obtained by
subtracting that target. Its increment is exactly a target/source
falling-factorial ratio, so following the carried target has zero reward.
Finite directed paths propagate the negative drift of a rare terminal source.
A normalized-log compactification and an exhaustive bimolecular top-complex
alternative either supply such a source or produce a stoichiometric invariant
that precludes divergence within the class. The result is class-wise and does
not address multiple linkage classes or molecularity above two.

**Subject category:**
Systems Biology.

**Result category:**
New Results. The claimed new result is a mathematical theorem about stochastic
biochemical reaction-network models; it is not an experimental result.

**Keywords:**
stochastic reaction network; systems biology; chemical master equation;
positive recurrence; mass-action kinetics; weak reversibility;
continuous-time Markov chain; Foster–Lyapunov method.

**Significance summary:**
Use `submission/biorxiv_significance_summary.md`.

## Scope and research-material declarations

**Life-science relevance:**
The paper studies stochastic mass-action CTMCs used to represent
low-copy-number intracellular, signaling, enzymatic, gene-regulatory, and
synthetic biochemical networks. It proves a parameter-independent structural
criterion for stationary probability laws within closed communicating
classes. The exact restrictions—weak reversibility, one linkage class, and
molecularity at most two—are stated prominently; no claim is made for all
biochemical models.

**Data:**
No empirical biological dataset was collected or analyzed. The mathematical
proof is universal. Deterministic code outputs and exact finite calibration
cases accompany the paper, but finite computation is not presented as a
substitute for proof.

**Code and supporting materials:**
The Version 1.0 archive contains the standalone verifier, tests, stable output,
release manifest, and clean-clone transcript. A public immutable repository
link should be entered only after the Version 1.0 tag exists and has been
verified.

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
`supplement/ai_use_full_statement.md`. No AI system is an author, and no prior
independent expert human validation is claimed.

## License and prior-online status

The current package reserves rights in the manuscript. bioRxiv offers several
reuse licenses and a no-reuse option. The no-reuse option is consistent with
the present `LICENSE.md`; any Creative Commons selection requires a deliberate
author decision after checking journal compatibility. This sheet does not make
that selection.

Version 0.3 has been publicly available as an unrefereed repository/web
preprint. Version 1.0 has not been deposited to a preprint server. Disclose the
related Version 0.3 record if the submission interface asks about prior online
versions or text overlap.

Do not submit Version 1.0 simultaneously to bioRxiv and arXiv. bioRxiv's
published screening description says submissions are automatically checked
for material already online, including material on another preprint server;
the public pages reviewed here do not provide affirmative authorization for a
duplicate cross-server record. Choose one server first and recheck current
duplicate-posting and version rules immediately before deposit.

## Screening risk

bioRxiv accepts mathematical work only when it has direct relevance to the
life sciences, and its screening guidance emphasizes research manuscripts
with new data or results outputs. The paper has direct systems-biology model
relevance and a new theorem with exact computational artifacts, but no
empirical dataset. Eligibility is therefore a screening judgment, not a fact
established by this package. If bioRxiv declines the manuscript as primarily
mathematical, arXiv is the natural preprint route.

## Policy sources checked 9 August 2026

- bioRxiv scope, categories, posting permanence, and licensing:
  <https://www.biorxiv.org/about-biorxiv>
- bioRxiv screening procedures:
  <https://connect.biorxiv.org/news/2022/06/13/screening_procedures>

The official scope includes Systems Biology and says mathematical work should
be posted only when directly relevant to the life sciences. The screening
description asks whether a submission presents biological research, checks
article type and completeness, and detects material that has appeared online.
Once posted, a bioRxiv article is citable and ordinarily cannot be removed.

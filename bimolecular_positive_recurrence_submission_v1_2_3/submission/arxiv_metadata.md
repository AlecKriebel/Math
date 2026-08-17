# arXiv fallback metadata

Use this route only if bioRxiv declines the paper or the bioRxiv plan is
abandoned before posting. Do not post the same manuscript to both preprint
servers. This is not evidence of submission, endorsement, moderation, or
acceptance.

## Core metadata

**Title:**
Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible
Stochastic Reaction Networks

**Author:**
Alec Kriebel

**Affiliation:**
Independent researcher

**ORCID:**
<https://orcid.org/0009-0001-9320-500X>

**Correspondence:**
<me@aleckriebel.com>

**Abstract**

Weak reversibility is conjectured to imply positive recurrence for stochastic
mass-action systems. We prove the conjecture for finite bimolecular networks with one
linkage class, removing the earlier requirement that every species occur in a
pure unary or pure-double complex. Under weak reversibility, the states
reachable from each initial population form a closed communicating class.
Under the additional one-linkage and bimolecular hypotheses, for every positive
rate vector each nonabsorbing reachable class is positive recurrent, whereas
an absorbing singleton carries its point-mass law; consequently every
reachable class has a unique stationary probability distribution. The closure statement
follows by lifting directed return paths of complexes to population states.
For recurrence, the proof marks the target of the most recently fired channel
and applies a log-factorial potential after subtracting that target. Its
increment is exactly the logarithm of a target/source falling-factorial ratio,
so following the carried target has zero reward. Finite target-following paths
propagate the negative drift of a rare terminal source, while a normalized-log
compactification and a bimolecular top-complex alternative rule out all other
divergent sequences. The same return-cycle construction recovers nonexplosion
directly. Multiple linkage classes and molecularity above two remain open.

**Comments**

> 15 pages; no figures. Includes a deterministic verification package and
> supplementary note. This is an unrefereed preprint.

**Report number:**
None.

**Journal reference:**
None.

**DOI:**
None. Do not enter a repository tag, commit, or bioRxiv DOI as a journal DOI.

## Subject categories

**Requested primary category:** `q-bio.MN` — Molecular Networks.

The official taxonomy describes this category as covering gene regulation,
signal transduction, proteomics, metabolomics, and gene and enzymatic
networks. The manuscript studies long-run stability of stochastic
mass-action CTMCs used for low-copy-number biochemical reaction networks, so
this is the requested primary category.

**Requested cross-list:** `math.PR` — Probability.

The theorem concerns countable-state continuous-time Markov chains, positive
recurrence, random-time Foster arguments, and regenerative occupation, making
`math.PR` the requested secondary category.

Category assignments remain subject to arXiv moderation. If moderators regard
the life-science connection as insufficient for `q-bio.MN`, the conservative
alternative is primary `math.PR` with a requested `q-bio.MN` cross-list. No
endorsement has been obtained or is claimed; a first submission or a new
category may require endorsement.

## Mathematics Subject Classification and keywords

**MSC 2020:** Primary 60J27; secondary 60J28, 60J74, 92C42.

- 60J27: continuous-time Markov processes on discrete state spaces;
- 60J28: applications of continuous-time Markov processes on discrete state spaces;
- 60J74: jump processes on discrete state spaces;
- 92C42: systems biology, networks.

**Keywords:** stochastic reaction network; systems biology; chemical master
equation; positive recurrence; mass-action kinetics; weak reversibility;
continuous-time Markov chain; Foster--Lyapunov method.

## Files to prepare for a possible deposit

- top-level TeX source: `manuscript/main_arxiv.tex`;
- canonical content: `manuscript/paper_content.tex`;
- bibliography: `manuscript/references.bib`;
- any local class/style assets required by the clean build;
- no validation environments, caches, logs, or unrelated preservation files.

The source archive must compile in arXiv's environment, use portable file
names, contain every referenced asset, and avoid absolute local paths. Preview
the arXiv-generated PDF before completing any submission.

## Licensing and posting sequence

The package reserves rights in the manuscript. The conservative arXiv choice
is the arXiv.org perpetual, non-exclusive license to distribute, unless the
author deliberately chooses a Creative Commons license after reviewing
journal compatibility. Confirm the license in the submission interface; this
sheet makes no license selection.

Do not use this fallback while a bioRxiv submission is pending or after it has
posted. Before any arXiv deposit, recheck duplicate-posting, version, licensing,
and journal-preprint rules. Corrections should normally be submitted as a new
version of the same record rather than as a new paper.

## Policy sources checked 16 August 2026

- arXiv submission guidelines:
  <https://info.arxiv.org/help/submit/index.html>
- arXiv category taxonomy:
  <https://arxiv.org/category_taxonomy>
- arXiv endorsement rules:
  <https://info.arxiv.org/help/endorsement.html>
- arXiv licensing and permanence:
  <https://info.arxiv.org/help/license/index.html>
- arXiv cross-listing guidance:
  <https://info.arxiv.org/help/cross.html>
- MSC 2020 official classification:
  <https://msc2020.org/MSC_2020.pdf>

The official guidelines state that submissions should be topical, refereeable
scientific contributions; authors are expected to self-submit; TeX is the
preferred format; all submissions are moderated; and new submitters or new
categories may require endorsement.

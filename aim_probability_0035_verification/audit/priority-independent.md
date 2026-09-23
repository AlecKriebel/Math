# Independent scope and priority audit

Audit date: 23 September 2026 UTC (22 September 2026 in the user's timezone).
Auditor: a separately assigned Codex agent. This is an independent approach within
the same coordinated AI workflow, not independent-person or journal review.

**Decision: the originality/priority gate is not clean.** The supplied candidate
reproduces a publicly archived result dated 6 September 2026, including its graph,
update schedules, exact gap and substantive proof reduction. This is a positive
identification of prior disclosure, not an inference from unsuccessful searching.
This audit cannot identify the person behind the prior publication's credited
author, Anonymous, or decide whether that person is the current user. If it is the
user's existing work, the appropriate action is verification or revision of that
work with its publication history preserved. Otherwise the present contribution
is a reproduction/verification, not a new discovery of the counterexample.

Checkpoint completion estimate: **100% for this bounded scope/priority decision**;
no claim of exhaustive historical priority coverage. Mathematical arithmetic is
being checked separately and is not assumed from publication status.

## 1. What claim the historical question asks

Holroyd's primary paper, *Some circumstances where extra updates can delay
mixing*, arXiv:1101.4690, defines the update operation and comparison on page 1:
a finite deterministic sequence of single-site updates, with each chosen spin
resampled from its conditional Gibbs law. Page 4, final paragraph of Section 3,
asks about the ferromagnetic Potts model from a constant configuration, after
explaining a distinct antiferromagnetic counterexample. This is the scope to
which the proposed q=3 witness applies. [Primary paper](https://arxiv.org/pdf/1101.4690).

The logical target can therefore be written as the universal statement that for
every finite graph, finite ferromagnetic Potts parameters, constant initial
configuration, deterministic update word and predetermined subsequence, the full
word ends no farther from the full Gibbs measure in total variation than the
subsequence. A single strict reversal with q=3 refutes that universal statement.
No quantifier requires every site to be visited by the comparison horizon.
Leaving D unupdated is permitted; fixing D in the Gibbs reference measure would
be a different problem. An infinite fair continuation can be appended after the
comparison time without changing the finite-time counterexample.

This statement does not entail an averaged random-scan counterexample, a
worst-initial-state mixing-time improvement, a result for each q>=4, minimality,
or improved practical simulation. The nine scheduled opportunities and the
eight actual resamplings in the censored process refer to the same horizon.

The [original AIM page](http://aimpl.org/markovmixing/1/) was successfully read
directly using **plain HTTP**. It identifies this as Spin Systems Problem 1.5,
attributed to Yuval Peres, and asks the deterministic-deletion question from all
green, explicitly suggesting q=3. The section defines the Potts Gibbs weight with
the same equal-edge exponential convention used in the candidate. A compact
extraction, retrieval timestamp and whole-page SHA-256 are retained in
`sources/priority-aim-original.json`. The HTTPS variant fails certificate hostname
validation, so this is direct current-source readback over HTTP, not a
cryptographically authenticated HTTPS retrieval. Holroyd corroborates its scope.

The provided UnsolvedMath ID is linked locally to numeric ID 20002593. Both of
those website endpoints returned HTTP 429 to this auditor. Independently
retrieving the [pinned UnsolvedMath dataset](https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/b9437975f3c873f635a13c48f8b022f5ba80898a/problems.json)
confirms the same statement and AIM attribution. The extracted entry and
whole-source SHA-256 are in `sources/priority-original-statement.json`. Its
August status predates the September counterexample and cannot establish the
problem's current open status. The local catalog's differing title is a research
summary rather than a verbatim problem title.

## 2. Exact prior publication and independently checked date records

The earlier work is **Anonymous, *A five-vertex counterexample to ferromagnetic
Potts censoring*, version 0.1.0-candidate**, DOI
[10.5281/zenodo.22546547](https://doi.org/10.5281/zenodo.22546547).
It is explicitly unrefereed. That qualification limits assurance; it does not
erase its publicly documented disclosure.

| Evidence | Observed record | Meaning |
|---|---|---|
| [Zenodo API](https://zenodo.org/api/records/22546547) | Created `2026-09-06T17:16:10.220042+00:00`; modified `2026-09-06T17:16:10.427156+00:00`; publication date `2026-09-06` | Archive service metadata, not solely a date typed into a manuscript |
| [DataCite API](https://api.datacite.org/dois/10.5281/zenodo.22546547) | Created `2026-09-06T17:16:10.000Z`; registered `2026-09-06T17:16:11.000Z` | DOI registration corroborates the prior date |
| [GitHub release](https://github.com/ipitchford/potts-censoring-counterexample/releases/tag/v0.1.0-candidate) | Published `2026-09-06T17:15:44Z` | Separate hosting service's release record |
| [Pinned commit](https://github.com/ipitchford/potts-censoring-counterexample/commit/5fd6df0bac10901bdbe29e651bfec119c122a3b4) | `5fd6df0bac10901bdbe29e651bfec119c122a3b4`, author/committer timestamp `2026-09-06T17:13:17Z` | Stable content identity; unsigned git timestamps alone are not authenticated publication dates |
| [Evidence Press](https://www.evidencepress.org/releases/potts-censoring-counterexample/) | Dated 6 September 2026; links the same release and DOI | Public exposition identifying the mathematical object |

These observations establish a documented disclosure before this verification
request. They do not prove the earliest-ever discovery date or authenticate the
identity of Anonymous. Repository account ownership is not scholarly authorship.

The ZIP was downloaded directly from the Zenodo record and matched its published
MD5 checksum `bc5b85e128712e7783b026cef1ef78fd`. Its SHA-256 and retrieval URL are
recorded in `sources/priority-package-receipt.json`. The mathematical Markdown
was read from that ZIP; its extracted-file SHA-256 is retained. The ZIP and full
copied manuscripts were removed after inspection to keep this audit compact.
The prior executable code was not run by this auditor.

## 3. Overlap with the submitted candidate

The immutable package's `SOLUTION.md` contains the following features, all also
present in the supplied candidate:

| Feature | Prior source location | Candidate relationship |
|---|---|---|
| Edges AB, AC, AD, BC, BE, DE; three colors; activity 30; all-zero start | Section 1 | Identical witness |
| Full word C E B C B A E B E; deletion of seventh opportunity | Section 1 | Identical comparison |
| Positive gap numerator `7905357280856578194954129502105` and denominator `766036711510586802141859485820665762204` | Section 1 | Identical exact result |
| Partition polynomial and Z=2207656998 | Section 3 | Same polynomial and integer |
| H/J kernels and R, F, Q marginal formulas | Sections 2 and 4, equations (1)-(3) | Same formulas and intermediate variables |
| Unnormalized stationary marginal on D=0 and common final E factor | Sections 3-4 | Same compression mechanism |
| TV equal to 2/3 plus positive marginal deficits | Section 4, equation (5) | Same identity |
| Fourteen representatives and every displayed sign, including the asymmetric 112 row | Section 5 | Identical sign certificate |
| Both exact TV fractions and denominator ratio 55,022 | Section 5 | Identical arithmetic conclusion |

Pinned source: [SOLUTION.md](https://github.com/ipitchford/potts-censoring-counterexample/blob/5fd6df0bac10901bdbe29e651bfec119c122a3b4/SOLUTION.md).
The prior package licenses its original prose and research data CC0 and original
code MIT; the component license and compact witness JSON are retained. Those
rights do not establish novelty.

The candidate's transfer-matrix derivation of the partition polynomial is a
different exposition from the prior manuscript's direct counting. No separate
novel research claim follows merely from deriving the same elementary polynomial
in this way. The candidate itself acknowledges a recently posted source for the
same witness, although its pasted citation placeholders do not identify it.

## 4. Search bounds and adjudication

Queries inspected included `"Potts" "censoring" "counterexample"`,
`"AIM-PROBABILITY-0035"`, the quoted exact gap numerator,
`ferromagnetic Potts censoring Holroyd counterexample`, and
`"censoring" "Potts model" green`. The exact duplicate was examined in its
primary public archive, independent DOI registration record and pinned repository
content. Holroyd was read directly for the statement's semantics. Returned
unrelated results were not used as evidence. The earlier package's own novelty
report was inspected for provenance, not adopted as proof of priority.

This is not an exhaustive MathSciNet, zbMATH, citation-network, unpublished-work
or world-literature search. No individual was contacted, and no outreach was
prepared. Further searches cannot make the identified prior disclosure disappear;
they could only uncover still earlier work or clarify attribution.

**Publication gate:** correctness may pass while originality fails. Subject to
the separate exact verification, this is a complete negative answer to the
universal deterministic finite-word question. It is not cleared as a new
resolution attributable to the current verification effort. A new resolution
paper, new priority claim or new DOI package should not be prepared on the premise
that this counterexample is unpublished. A clearly attributed verification
report can legitimately preserve the new checking work.

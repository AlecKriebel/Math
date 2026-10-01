# Exact source and prior-work gate

30003427 / OWR-15218-003, rank 259; source gate completed 2026-10-01 UTC.
The full pinned record was read. No separate upstream research report exists.

## Original target and model

The OWR report is volume 14 (2017), report 13, published January 2018,
DOI 10.4171/OWR/2017/13. Gerhold's contribution, joint with Gülüm,
is printed pp.696–698. Page 697 was visually inspected. It assumes finite
probability spaces and discrete dates, asks for multiple-maturity necessary
and sufficient conditions, and asks for the smallest spread bound. It
expresses uncertainty about whether simple conditions exist; it imposes no
formal polynomial-time or short-form output requirement.

The final Gerhold–Gülüm paper is Mathematical Finance 30 (2020), 377–402,
DOI 10.1111/mafi.12230, first online November 11, 2019. The full v2 arXiv
manuscript and final publisher article/XML were inspected at Definitions
2.1, 2.2, 2.4, Lemma 2.7, Theorem 4.3 and the conclusion. The final complete
XML is available from the official Europe PMC API. Direct PMC webpage and
some publisher math-image/PDF retrieval attempts failed; no such failed
access is represented as full-PDF access.

In discounted units there is a distinct reference process R_t for cash
settlement and a shadow martingale Z_t. The model has strictly positive
stock bid prices, R_t lies in the stock spread, and so does Z_t. Epsilon
consistency bounds the discounted spread by epsilon at all dates including
zero, and additionally imposes R_t>=epsilon for positive dates. Equivalently
for a constructed model one can use R_t>0, Z_t>0 and |R_t−Z_t|<=epsilon,
then choose the bid/ask as their min/max. The known strike restriction
k_(t,i)>epsilon is an auxiliary assumption for the paper's explicit main
inequalities, not part of Definition 2.4 itself. A criterion can either
retain all epsilon>=0 or explicitly intersect with that usual range.

The bank account is deterministic and positive. Calls are finite in number,
quoted at time zero with positive bid/ask bounds, and are cash settled. The
reference is not assumed to be a martingale or the arithmetic midpoint.
There is no fixed physical measure to preserve. A consistent model and its
probability law are themselves the existence objects. No real transaction,
portfolio recommendation, or financial action is part of this research.

## Existing results and recent literature

Gerhold–Gülüm already solve one maturity and give a semiexplicit multiple-date
criterion through unknown marginal laws and a peacock approximation theorem.
It is not replaced here by a one-date result.

Minhyeok Lee, arXiv:2607.27649v1, July 30, 2026, is a recent primary preprint
on the exact reference/shadow architecture. Its abstract, model and theorem
statements were read in full PDF. It claims a correction to the executable
calendar-vertical-basket convention, a two-date insufficiency counterexample,
and a two-date operator. It does not claim the arbitrary-date consistency
and minimal-bound characterization sought here. Those claims are prior
context, not independently certified premises of the present argument.

The finite-tree mechanism is classical conditional Carathéodory/martingale
Tchakaloff compression. Beiglböck–Nutz, *Martingale Inequalities and
Deterministic Counterparts*, EJP 19 (2014), Theorem 5.1, gives the familiar
(n+k+1)^T support bound. Our direct finite-tree proof keeps reference prices
as adapted auxiliary coordinates rather than pretending they are functions
of the shadow-price path. Quantifier elimination is the classical effective
Tarski–Seidenberg theorem, as stated in Basu's survey, Theorem 2.1 and
Section 2.1. No novelty, priority, or tractable-computation claim is made.

## Prior campaign gate and count

Exact ID PR search, bid/ask PR search, branch search, committed main-path
history and local all-ref commit-title search found no prior Alec/campaign
attempt. Related-target groups contain no exact match. Row 259 was queued
0/5. Published upstream work is credited prior literature, not prior Alec
work. Source retrieval itself is zero substantive turns. The subsequent
finite-tree reduction, algebraic criterion and attainment analysis form
substantive author turn 1; it is not hidden in the source count.

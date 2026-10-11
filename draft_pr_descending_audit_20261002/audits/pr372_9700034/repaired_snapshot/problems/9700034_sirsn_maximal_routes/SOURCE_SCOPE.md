# Exact source and prior-attempt gate: 9700034

## Question and version

For a SIRSN, with U_i independent uniform points in the unit disc and
independent of the network, under which additional assumptions, if any,
is E sup_i len R(0,U_i) finite?

Aldous's 2012 manuscript arXiv:1204.0817v1, dated April 5, labels this
Open Problem 34 in §8.4.3, printed p.50. The published paper is Electronic
Journal of Probability 19 (2014), paper 15, 1–41,
DOI 10.1214/EJP.v19-2920; its §8.4.3, printed p.38, renumbers this as
**Open Problem 8** without changing the mathematical request. The published
question page was rendered and visually inspected. Both complete PDFs and
the maintained primary problem page were retrieved; exact bindings are in
SOURCE_MANIFEST.json. The original asks about a countably sampled maximum,
not a supremum over an uncountable collection of unspecified route versions.

## SIRSN axioms that cannot be replaced silently

The published §§2.2–2.3 specify finite-length non-self-intersecting feasible
routes, reversal symmetry and pairwise route compatibility: two routes
meeting twice coincide between the meeting points. Finite-dimensional
network laws are consistent, translation/rotation/scale invariant, and
measurable as functions of the endpoint configurations. Independent Poisson
samples define feasible subnetworks. The unit-distance route length D has
finite first moment; the endpoint-truncated major-road intensity p(1) is
finite and scales as p(r)=p(1)/r. Finite sampled-network edge intensity ell
follows. Merely requiring ell finite instead gives a weak SIRSN.

Routes are prescribed. The source expressly does not require that they
minimize Euclidean length or any specified cost. Route compatibility does
not entitle us to assume a triangle inequality for route lengths. The
measurable FDD formulation also does not automatically provide a jointly
measurable continuum routing map. Proofs here will use the countable sampled
setup, or explicitly state any stronger realization assumption they need.

## Prior and related work gate

The requested unsolvedmath page returned an internal web error. The exact
record and its prior report were read in the pinned catalog at revision
37e53eabe540fb458758e198be61634bd02ee008. The prior is OPEN-TRIAGE: literature
search and statement recovery only, with no substantive mathematical attempt.
At main efd29c05204703acca9a0860812f54b94fae54b1, rank397 is queued0/5.
Exact-ID all-state PR, branch, commit and all-ref path searches found no
attempt. Main code search found assignment metadata only. The read-only
local inventory contains 468 refs.

Related campaign results were inspected and are distinct: draft PR41,
9700035, studies expected full spanning-network length under an extra
fourth-tail condition; its full proof and source qualifications were read.
Draft PR304, 9700031, studies traffic local finiteness and intrinsic road-size
moments; its final theorem/scope and source audit were read. Neither proves
the expected maximum from one root. Those results are not re-counted as
independent discoveries in this target.
https://github.com/AlecKriebel/Math/pull/41
https://github.com/AlecKriebel/Math/pull/304

## Current primary context and credit

Aldous's maintained SIRSN problem page continues to point to the general
questions and to later Poisson-road constructions. His published Proposition
3.1 and §3.7 give a deterministic bounded-stretch estimate for the binary
hierarchy model, which already implies this expected maximum is finite in
that particular model. That application is credited, not a new solution.

Kahn, *Improper Poisson line process as SIRSN in any dimension*, Annals of
Probability 44(4) (2016), 2694–2725, DOI 10.1214/15-AOP1032, arXiv:1503.03976v3,
proves a uniform random travel-time diameter bound in Theorem 3.1. Theorem
5.1 and its full proof give Euclidean route-length moments below gamma−1;
Remark 5.1 indicates a uniform ball interpretation. Those sources are the
credited basis for a carefully stated uniform-length corollary, not a claimed
new construction. Time length and Euclidean arclength must be distinguished.
Its stronger conjectured moments in Remark 5.1 are not assumed.

Blanc–Curien–Kahn, arXiv:2407.07887v1 (2024), published PLMS 131 (2025),
e70070, develops confluence, non-pausing geodesics and their local structure
in the concrete Poisson-road model. The primary abstract and the prior
source audit were checked for scope; no unrestricted SIRSN maximum theorem
is inferred from them. Exact-phrase searches located no general solution.
This is a bounded literature check, not a priority or global status certificate.

The source gate uses 0 substantive author turns. A conditional theorem for
one model or under extra assumptions will not alone justify reporting that
the ordinary SIRSN axioms settle the full general question. No outside
individual is contacted. Raw sources and imported records remain local.

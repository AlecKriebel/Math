# Independent adversarial audit of the priority bridge

Completed UTC: 2026-10-15. Completion estimate for this bounded audit: 100%.

## Finding and limits

I could not falsify the claimed mathematical coverage by earlier results. Every
candidate chain weight is an exact finite-dimensional specialization of proved
earlier Plancherel dynamics, and Nica's 2014 version already prints the relevant
Schur chain law. The bridge from the 1993 random pile-top ranks to that coherent
tableau law is valid, including the distinction between insertion and recording
tableaux. No unproved degeneration, unspecified correlation, or invariant-law
equation is left in this derivation.

This supports **complete earlier automatic mathematical coverage** of the
candidate's central stationary-law formula. It does not establish that an earlier
author explicitly announced an answer to the question posted in February 2018,
that the exact rational enclosure or submitted software appeared earlier, or that
the proposer has endorsed the interpretation of “fairly explicit.” These are
different provenance questions. I make no queue mutation or global historical
closure claim. A new exposition, explicit application, source correction, or
verification implementation can still be useful.

An additional, independent 2001 finite Bessel-determinant route also survives;
its proof and a mandatory correction to a tempting false intermediate assertion
are in `LRW_ADVERSARIAL_ADDENDUM.md`. The conclusion above does not depend on that
additional route.

## Scope and independence

The initial `PRELIMINARY_CHALLENGE.md` was saved before reading any prior family
reports. I read the supplied candidate and provisional root reconstruction,
then primary sources. Root subsequently supplied Nica-version and LRW leads and
reported a flaw in another draft. I did not inspect that draft or any other
family report. My exact controls and proofs below were independently written.
All writes are confined to this shard. No external outreach, Git/index/ref write,
provider write, classification change, or paper preparation occurred.

The hypothesis tested was: every finite joint survival probability of the
candidate is an explicit consequence of earlier proved objects and transition
laws. Equality of single-time marginals alone was expressly insufficient. The
success criteria were all-index/all-threshold identification, every factorial in
the chain weight, proper boundary cases, and no unproved process limit.

## Primary-source ledger and exact locations

The JSON source ledger pins retrieval times, byte lengths, and SHA-256 hashes.
All copied PDFs were independently hashed, and the 1993, 1999, and 2004 copies
were subsequently retrieved directly and verified byte-identical. Nica v1/v4 and
LRW 2001 were directly retrieved. Relevant central displays were rendered and
visually inspected rather than inferred from OCR alone.

| ID | Primary source | Relevant locations |
| --- | --- | --- |
| S0 | [Aldous problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/left_Hamm.html) | Exact finite-particle dynamics, unique invariant-law statement, question and February 2018 posting history |
| S1 | [Aldous-Diaconis 1993 unfinished notes](https://www.stat.berkeley.edu/~aldous/Research/OP/patience.pdf) | Printed 2: small-label patience compatibility; 10: P-row/pile-top identity and RSK bijection; 12: coherent Q-tableau probabilities; 36-37: ranks B, independent Poisson marks, (41)-(42) |
| S2 | [Aldous-Diaconis 1999](https://www.stat.berkeley.edu/~aldous/Papers/me86.pdf) | Printed 417-418: RSK bijection, insertion algorithm, full top-row identity; 427: leftmost-pile process discussion |
| S3 | [Borodin-Olshanski math-ph/0402064v2](https://arxiv.org/pdf/math-ph/0402064v2) | Printed 3: up probabilities; 4-5: independent size driver and (1.9); 6: Remark 1.5, Definitions 2.1-2.2; 7: Theorem 2.3 |
| S4a | [Nica 1404.4015v1](https://arxiv.org/pdf/1404.4015v1) | Printed 5: Theorem 3.2 and Remark 3.3; 7-11: counting proof; 13-14: Theorem 4.1, exact rectangle interpretation |
| S4b | [Nica 1404.4015v4](https://arxiv.org/pdf/1404.4015v4) | Printed 5: theorem with genuine right-exponent typo; 6: correct Schur expression; 8-12: counting proof |

The [arXiv version record](https://arxiv.org/abs/1404.4015v4) dates v1 to
15 April 2014 and v4 to 29 March 2017. Current rendered title pages carry later
compilation dates (v1: December 2024; v4: September 2021). I therefore distinguish
version provenance from current PDF rendering dates, and explicitly checked the
v1 theorem content. I do not assert that today's exact PDF bytes existed in 2014.
The BO version record dates v2 to 29 September 2004. The 2013 BO no-proofs note is
not used as a covering theorem.

## 1. The P/Q objection is real but does not break the bridge

Smallest-value restriction and restriction to the first positions are different.
For the word `(2,3,1)` and q=2, the first two positions have insertion shape `(2)`,
whereas deleting values above 2 gives `(2,1)` with shape `(1,1)`. Thus one must not
replace P-restriction by forward insertion in the original permutation.

Here is the needed finite identity, proved directly from the insertion algorithm
in S1/S2:

> Inserting a word and then retaining only tableau entries at most q gives the
> same tableau as first deleting all word entries above q and then inserting.

Proof by induction on word length: inserting a value above q bumps only larger
values, so cannot alter any retained entry. Inserting a value at most q follows
exactly the same bumping path among retained entries. At the first row where the
next bump would exceed q, the restricted insertion appends its current value;
the full insertion thereafter bumps only values above q and cannot change the
restricted tableau. This also covers the case where the path creates a new row.

For a uniform permutation of n, its subword on labels 1,...,q is uniform in S_q.
The RSK bijection gives, for any fixed standard tableau t of size q and shape mu,

    P(P_q=t) = f^mu / q!.

The finite identity shows exact consistency under small-label restriction, so
these laws define a coherent infinite standard tableau T. Its first row is
exactly the compatible pile-top rank sequence B from S1. This is a finite exact
identification, not a deduction from an asymptotic shape theorem.

Every fixed first-row entry B_r is finite almost surely. For completeness, realize
the relative order of labels by independent uniform marks U_i. Divide q labels
into r successive label blocks of size at least floor(q/r), and divide the mark
interval into r successive intervals of length 1/r. If each label block supplies
a mark in its matching interval, there is an increasing subsequence of length r.
For r>=2 the failure probability is at most

    r (1-1/r)^floor(q/r) -> 0.

The r=1 case is immediate. Thus no mass at an infinite rank was suppressed.

## 2. Independent Poisson marking and the exact stationary representation

S1 explicitly introduces independent rate-one Poisson spatial arrivals Gamma
before equation (42). Independence is substantive: arbitrary coupling of ranks
and arrivals would not justify the subsequent equivalences.

It can also be checked directly. A unit Poisson field on `(0,infinity) x (0,1)`
can be generated by rate-one spatial arrivals Gamma_n with independent uniform
vertical marks U_n. These marks generate all finite uniform permutations used
above, while Gamma generates the sorted locations. Hence the entire coherent
tableau T, and therefore B, is independent of Gamma. The pile-top locations are
Gamma_(B_r), jointly for every finite list of r.

S1 is unfinished and its surrounding derivation must not be promoted as flawless:
the printed transformation on page 36 has an incorrect spatial sign and the
subsequent coupling mean bound is unsafe. A claim that those pages contain a
clean correct printed proof would be false. The rank representation itself has
an independent finite geometric justification, and the corrected transformation
is immediate to check: if Z_i(t) are ordinary empty-start Hammersley pile tops,

    Y_i(s)=exp(s) Z_i(exp(s)),
    #{i:Y_i(s)<=x}=L(x exp(-s),exp(s)).

The event change `(u,v)->(uv,log v)` has unit Jacobian, gives velocity Y_i between
events, and preserves nearest-right jumps. The area-preserving rescaling
`(u,v)->(exp(a)u,exp(-a)v)` makes Y stationary. At s=0 its row is Gamma_B.
Finite-prefix autonomy gives the exact finite-k generator in S0. This repairs
the source typo without requiring a process degeneration or a new invariant-law
equation; it is the same classical Poisson/patience geometry.

## 3. The horizontal BO process gives all joint laws, not just marginals

S3 allows nonnegative u' and nonpositive v' provided they do not vanish together;
Remark 1.5 expressly includes horizontal pure-birth paths. For C(x)=(x,1),
equation (1.9) gives size birth rate 1 and death rate 0. The jump is chosen by

    p_up(mu,nu)=f^nu / ((|mu|+1) f^mu)

for a one-box extension. The size process is the independent Poisson driver in
the construction. Theorem 2.3 identifies this shape path with RSK of the nested
rectangles `(0,x) x (0,1)`. No stationary hyperbola process is substituted.

The same up probability follows directly from the coherent tableau: for a
particular extension t+ of t, the ratio of its two coherent probabilities is
`[f^nu/(n+1)!]/[f^mu/n!]`. It depends only on the two shapes. Thus the complete
tableau path and the BO shape path have identical finite-dimensional laws.

Let N(x) be the count of the independent spatial arrivals by x, and let lambda(x)
be the shape of labels at most N(x) in T. Pathwise,

    Gamma_(B_r)>x  iff  B_r>N(x)  iff  lambda_1(x)<=r-1.

This is simultaneously true for every queried pair (r,x). It closes the
all-time/all-threshold gap that matching Plancherel marginals alone would leave.

There is no delicate x=0 entrance issue. At any positive x_1 the source explicitly
gives the initial law M_(x_1). Start there and multiply the later transitions.
Its explicit initial mass is algebraically the same as the virtual transition
from the empty diagram over length x_1. One need not invoke any limiting theorem
at the open-quadrant boundary.

## 4. Every candidate weight follows with all factorials intact

Write n=|mu| and d=|nu|-|mu|. Along one specified d-step extension path the
product of BO up probabilities telescopes to

    (f^nu/f^mu) n!/(n+d)!.

There are f^(nu/mu) such paths. The independent d-birth probability supplies the
additional `exp(-Delta) Delta^d/d!`, giving

    P_Delta(mu,nu)=exp(-Delta) Delta^d/d!
                  * f^(nu/mu) * f^nu/f^mu * n!/(n+d)!.

Multiplying successive transitions (and the explicit initial marginal) yields
for `empty=lambda^0 subset ... subset lambda^m`, with d_j the size increments,

    exp(-x_m) f^(lambda^m)/|lambda^m|!
      * product_j [Delta_j^d_j f^(lambda^j/lambda^(j-1))/d_j!].

Using the classical exponential skew specialization converts this exactly to
`exp(-x_m) D_1(lambda^m) product_j D_(Delta_j)(lambda^j/lambda^(j-1))`.
No factorial disappears except through the displayed telescoping. In particular,
omitting the independent birth d! produces twice the correct raw weight for
`empty->(2)` over Delta=1 (`1/2` instead of `1/4`).

Summing these nonnegative weights under arbitrary conditions
`lambda^j_1<=r_j-1` gives every submitted survival event. Nonmonotone r_j are
permitted because the event identity is pointwise. Equal shapes have d=0 and
unit empty-skew weight. Repeated thresholds combine by the minimum index;
nonpositive thresholds are vacuous. Transposition preserves skew-tableau counts,
so the fixed determinant dimension in the candidate is a direct reformulation.

At terminal size n, removing every shape constraint gives raw mass x_m^n/n!,
because the independent size driver is Poisson. Thus positivity, normalization,
absolute convergence, and an explicit exponential tail bound are consequences of
the same earlier law. The particular shared-normalizer rational enclosure is a
useful elementary consequence; I did not find it asserted in the inspected source
pages and do not claim its exact prior publication.

## 5. Nica is stronger than ingredient chronology

S4a Theorem 3.2 already prints the full normalized Schur chain product, and
Remark 3.3 prints its skew-dimension specialization. Its counting proof uses
independent Poisson strip counts, uniform permutations, and the RSK bijection;
Theorem 4.1 identifies the diagram trajectory with nested rectangles. This is
the actual finite-dimensional formula, not merely a list of available tools.

For the candidate's largest threshold a=x_m, put theta=sqrt(a). The map

    (u,v)->(u/theta, theta v)

preserves area and all coordinate comparisons, sends `(0,a)x(0,1)` to the
theta-square, and sends each prefix rectangle to width x_j/theta and full
height theta. Use Nica's positive branch in reversed threshold order, with
observation time s_j=theta-x_j/theta and terminal shape lambda^m at time 0.
The unobserved left branch contributes D_theta(lambda^m); the right branch gives
the factors D_(Delta_j/theta)(lambda^j/lambda^(j-1)). Thus its exact chain mass is

    exp(-a) D_theta(lambda^m)
      * product_j D_(Delta_j/theta)(lambda^j/lambda^(j-1)).

Homogeneity gives a factor theta^n from the first term and theta^(-sum d_j)
from the rest. Since sum d_j=n, they cancel exactly, leaving the candidate weight.
There is no large-square limit. Empty observation lists can equivalently be
replaced by the deterministic empty endpoint shapes; no observation is forced
into a forbidden time domain.

The v4 theorem's right-product exponent really prints `|mu^j/lambda^(j+1)|`,
although its dimension and factorial use `mu^j/mu^(j+1)`. It may even reference an
undefined lambda when the two observation counts differ. A literal uncorrected
quotation would be wrong. This is a local transcription error, not a missing
mechanism: v1's theorem already has the correct Schur product; v4 Remark 3.3 has
it as well; and the source's counting lemmas independently derive it. The proof
also contains some copied index mistakes; the finite conditioning/counting
argument above checks the intended statement without trusting those indices.

## 6. Adversarial objection disposition

| Objection | Disposition and checkable reason |
| --- | --- |
| Small-value P restriction was confused with prefix Q restriction | Real danger, rejected as a gap after the direct bumping proof; `(2,3,1)` is a negative control against the false shortcut |
| B was specified only by a one-row limiting asymptotic | Rejected: exact finite restriction law and uniform RSK probabilities determine every finite tableau restriction; the elementary block bound prevents infinite ranks |
| Poisson marks might depend on B | Rejected: both S1's independence statement and the marked-Poisson construction establish independence |
| Horizontal BO paths are inadmissible | Rejected: explicit derivative inequalities and Remark 1.5 include them |
| BO needs an unproved entrance at zero | Rejected: start from explicit M_(x_1) at x_1>0 and use transitions |
| Matching one-time Plancherel measures is insufficient | Accepted general objection, resolved here by actual coherent up transitions and independent Poisson counts |
| The Schur formula could hide missing factorials | Rejected: full transition multiplication and exact negative factorial control check them |
| Nica v4 literally displays the candidate formula correctly | Rejected: the exponent typo must be disclosed; v1 and the proved corrected product close the mathematical route |
| S1's source proof is free of errors | Rejected: its spatial sign and coupling quantitative estimate are unsafe; the correct representation is separately established |
| Old theorems must already name the February 2018 problem | Not a mathematical requirement for automatic coverage; remains a provenance limitation if a registry requires a named published solution |
| The submitted precise certificate/software has been shown earlier | Not established; no such historical assertion is made |

## 7. Exact controls and remaining gap

`finite_controls.py` uses only Python's standard library and exact integers and
rationals. `FINITE_CONTROL_RESULTS.json` records successful checks of:

- 409,113 P-restriction identities across all 46,234 permutations of sizes 0-8;
- 2,459 exact shape-chain frequencies from 5,914 permutations of sizes 0-7;
- 8,664 factorial-determinant/Young-lattice comparisons through terminal size 10;
- 5,757 three-threshold chains comparing candidate, BO, and Nica weights;
- raw size masses, nonmonotone index constraints, and negative P/Q and factorial
  controls.

These finite checks are falsification controls rather than substitutes for the
general proofs above. The remaining gap is historical/editorial: whether a label
such as “already solved” is reserved for an earlier explicitly announced solution
or also includes an exact specialization and short identification from earlier
proved results. There is no central mathematical gap left in the latter sense.

The strongest supported assessment is therefore: the candidate gives a valid,
explicit presentation and certified computation of an already determined law;
its central formula does not require a new mathematical mechanism beyond the
earlier proved results. No conclusion relies on search silence, the mere order
of ingredient dates, the still-open wording on S0, or an unproved 2013 limit.

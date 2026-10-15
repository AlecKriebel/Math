# Independent blocker-geometry analysis, sealed before prior diagnostics

Audit target: PR 19, exact head `f1053196b6405623d5f5d8611289939765918d72`, problem 30006390 (duplicate 30006391). Input: the 13-file source snapshot, with `BASELINE.md` SHA-256 `9e0a930e61d849799c4395024c85d4f9c75b63ae2172321ef78ebf643f283c82`.

This note and `fresh_affine_checks.py` were prepared before reading the candidate's scripts, results, earlier reviews, root-agent findings, or sibling-agent findings. Inputs read were root `AGENTS.md`, snapshot `BASELINE.md`, and `source_records.json`. This is an audit of a partial result, not a new attempt at either central conjecture. All writes remain in `blocker_family/`; no Git mutation, installation, outreach, publication, DOI action, or tracker change was performed.

## Exact hypotheses and target

Let a finite nondegenerate projective plane have order integer q >= 2, point set P, and line set L. We use only: every line has q+1 points; every point has q+1 incident lines; two distinct points determine exactly one line; two distinct lines meet in exactly one point; and |P|=|L|=n=q^2+q+1. These follow from the usual finite-plane axioms and do not require coordinates, a field, Desargues' theorem, or prime-power order. The source's prime-power assumption guarantees the familiar examples, but the deductions are valid in every plane that exists. No claim that all existing orders are prime powers is used.

R is formed by independent Bernoulli(1/2) **point** variables. Define tau(R) as the minimum |B| over B subset R meeting every nonempty L intersect R. R itself is always feasible, so tau is defined for every R, including tau(empty)=0. The conjectural targets are tau(R)/q tending to infinity in probability, and the stronger high-probability Omega(q log q) lower bound. The baseline Bruen bound is not either target: (q+sqrt(q)+1)/q tends to 1.

## Reduction, exceptions, and minimality

Write E for every L intersect R being nonempty, and F for no line being contained in R. For a single line, each exceptional probability is 2^(-(q+1)), so a union bound gives P(not E) <= n2^(-(q+1)) and P(not F) <= n2^(-(q+1)). Both bounds tend to zero uniformly in the choice of the plane. They need not be useful for small q.

For B subset R, B intersect (L intersect R)=B intersect L. On E, meeting all sections is therefore exactly being an ordinary blocker. On F, every blocker contained in R contains no entire line. These are distinct conditions: E is needed to justify the ordinary-blocker reduction; F is needed to invoke the nontrivial bound. A realization R containing a whole line can have tau(R)<=q+1, since a whole line meets every line. Removing F silently would make the deterministic lower claim false.

Every finite ordinary blocker contains an inclusion-minimal ordinary blocker, by repeatedly removing dispensable points. Equivalently, B is inclusion-minimal if and only if each b in B has a tangent line L with L intersect B={b}: deleting b fails exactly when such a witness exists. This characterizes all minimal blockers; no size classification or field-specific structure is assumed. A line is itself minimal. Consequently, a minimal blocker containing a whole line is exactly that line, because the line is already a smaller blocker unless equality holds.

For every real k>=0, with integer thresholds interpreted as floor(k), on E we have tau(R)<=k if and only if R contains some minimal ordinary blocker of size <=k. This uses all minimal blockers, including lines. It does not require F. The family M_q(k) is deterministic once the plane is fixed, and P(B subset R)=2^(-|B|). Hence

P(tau(R)<=k) <= P(not E) + sum over B in M_q(k) of 2^(-|B|).

The entire-line members contribute exactly n2^(-(q+1)) to this weighted sum. Minimality eliminates all their supersets from the family, but does not constrain the number of nontrivial minimal blockers. Showing that the weighted sum tends to zero at k=Cq, for every fixed C, is a sufficient route to the growing lower bound. It is not necessary: the containment events may overlap. No estimate controlling that sum for all fixed C>1 is supplied in the candidate. This is the exact remaining combinatorial gap.

## Independent Bruen derivation

Let B be an ordinary blocker with no whole line, k=|B|. Incidence counting gives k(q+1)>=n. Since n/(q+1)=q+1/(q+1), integrality gives k>=q+1. Set a=k-q-1>=0.

For each line L, choose x in L outside B; this choice uses the no-whole-line assumption. The other q lines through x must each meet B outside L. Their outside-L portions are disjoint, since any two meet only at x, and x is not in B. Thus |B outside L|>=q and r_L=|B intersect L|<=k-q=a+1. Since B blocks all lines, 1<=r_L<=a+1.

Multiply r_L<=a+1 by the nonnegative r_L-1 to obtain r_L(r_L-1)<=(a+1)(r_L-1). Sum over all n lines. Unique point joins count each ordered pair of distinct B-points once, so sum r_L(r_L-1)=k(k-1). Regular point degrees give sum(r_L-1)=k(q+1)-n. Therefore

k(k-1)<=(a+1)(k(q+1)-n).

The substitution k=q+a+1 gives k(q+1)-n=a(q+1)+q and

(a+1)(a(q+1)+q)-(q+a+1)(q+a)=q(a^2-q).

The inequality implies q(a^2-q)>=0. Since q>0 and a>=0, a>=sqrt(q), establishing the exact integer statement k>=q+ceil(sqrt(q))+1. No equality-case theorem is needed. No minimality assumption was used: the bound holds for every blocker with no line. On E intersect F this bound holds for every admissible B and hence tau(R); it has probability at least 1-2n2^(-(q+1)).

This is the classical Bruen bound and cannot be claimed as novel. Primary publisher metadata corroborates the prior papers: A. Bruen, *Blocking Sets in Finite Projective Planes*, SIAM J. Appl. Math. 21(3), 380–392 (1971), DOI [10.1137/0121041](https://epubs.siam.org/doi/10.1137/0121041), whose references include Bruen's *Baer subplanes and blocking sets*, Bull. Amer. Math. Soc. 76 (1970), 342–344. The accessible publisher page provides metadata; this audit's universal bound is established by the displayed proof, rather than by assuming a theorem from inaccessible full text. An AMS PDF fetch returned HTTP 403 and was not used as evidence.

## Boundary and model falsification checks

For R empty, tau=0 and E fails. For R contained in a line, every retained point p has another line through p whose section is exactly {p}; all such p must be chosen. Thus tau(R)=|R|, including the whole line boundary. This explicitly prevents extending the high-probability Bruen conclusion to arbitrary realizations.

At q=2 the good event E intersect F is empty in PG(2,2): the independent enumeration below finds no nontrivial blocker. This does not contradict an asymptotic statement; the union-bound lower probability is vacuous there. At q=3, the three sides of a triangle with their three vertices removed form a 6-point nontrivial minimal blocker. The direct enumeration confirms tau=6 and realizes the integer bound q+ceil(sqrt(q))+1. At q=2 the same construction is a whole line; treating it as a nontrivial example would fail.

Distinct lines meet in one point, so their union has 2q+1 points. Therefore P(L intersect R=M intersect R=empty)=2^(-(2q+1)), twice the product of the marginal probabilities. More structurally, if B is an ordinary blocker, conditioning on B subset R already guarantees every line section is met by B. Independent deletion of incidences is a different random model; its per-line product mechanism cannot transfer to shared random point variables. No independence of line failures is used in the blocker union bound or in the alteration upper bound.

## Independent exact computation before seal

`fresh_affine_checks.py` constructs PG(2,2) and PG(2,3) as affine planes plus q+1 direction points, using y=mx+b, vertical lines, and the line at infinity. This differs from the usual homogeneous-vector construction and does not import candidate code. The plane axioms, including a quadrangle, are checked explicitly.

For each R, it enumerates **every** B subset R and computes its set of covered lines directly. The exact transversal optimum is the smallest B whose covered-line set equals that of R. No ordinary-blocker or minimal-blocker reduction enters this optimization. Independent subset-minimum transforms then find the smallest ordinary and minimal ordinary blockers in R, and compare the results. This provides a direct falsification check of the reduction and minimality equivalence, rather than merely repeating the derivation's implementation.

All 8,320 retained point subsets were covered, with 1,596,510 direct (R,B) candidates examined and 104,600 counted assertions passing. The finite certificates contain the affine incidence systems, all transversal values, and every minimal ordinary blocker. PG(2,2) has 7 minimal blockers, all lines of size 3. PG(2,3) has 13 minimal lines of size 4 and 234 minimal nontrivial blockers of size 6; its 468 nontrivial blockers have sizes 6 and 7. The good-event counts are 0/128 and 468/8192, respectively.

The script also checks the local Bruen inequality on every finite nontrivial blocker, each algebraic and incidence identity, exact empty-event dependence on every line pair, first-moment upper bounds at every integer threshold, all subsets-of-a-line boundaries, tangent witnesses, complement independence, and whole-line minimality. These finite observations do not establish any growing asymptotic lower bound.

## Scoped preliminary verdict

PASS for the universal blocker geometry, algebra, event-qualified lower bound, all-minimal-blocker equivalence, and explicit remaining counting gap. No mathematical repair was identified in this family. The result is a correct, classical partial baseline; neither central conjecture is resolved. Candidate diagnostics and claimed assertion totals remain to be reproduced after this seal. Container hypotheses and source normalization are separate audit families and are not certified by this preliminary verdict.

# Hostile review: two-step transition-kernel obstruction

Date: 2026-07-25 16:42 PDT

## Verdict

**ACCEPTED.**

The online transition-kernel reformulation, forced-state stopping criterion,
two-step private-region theorem, compact obstruction certificate, and
\(C_7\) strictness example are proved from the stated one-guard model.  The
computational counts were independently reproduced, but remain explicitly
classified as finite **observations**, not proofs of nonexistence outside
their recorded populations.

The revised note accurately attributes Burger et al.'s 2004 finite- and
infinite-order predecessors and does not claim that a general finite-horizon
construction is novel.  Its delimited campaign contribution is the forced
maximum-independent-state/private-region specialization, complement
translation, and recorded measurements; even that specialization is not
categorically claimed absent from all prior literature.

Severity census:

| Severity | Count | Disposition |
|---|---:|---|
| Critical | 0 | none |
| High | 0 | none |
| Medium | 0 | none |
| Low | 1 | dependency-manifest note below |

An initially exposed low-severity issue in the otherwise-unused
`legal_dominating_successors` helper was repaired before this verdict.  The
final helper rejects malformed configurations, out-of-range attacks, Boolean
integers, and occupied attacks.  The finder, certificate verifier, theorem,
and recorded counts were never affected.

## Final frozen hashes

| Artifact | SHA-256 |
|---|---|
| `math/lemmas/two_step_transition_kernel.md` | `c17254fbf868541b392aba0b058f21dae65d6db7f919e2b8947910679c520961` |
| `src/search/two_step_obstruction.py` | `fcc8d27f9b7d838afafd2208762361750e4e373c81dcb477263dbc6534209e38` |
| `tests/test_two_step_obstruction.py` | `2ce8bfd1fab7006927c413d48c9179b5b3f2737730c6a3c4fa5e45c9f7dd4329` |
| `results/two_step_obstruction_measurement.json` | `8cbbe566c10a390593ec56afa2d2a454804540083264835f9738fbe86081f591` |
| edge-toggle input ledger | `a32505df6ba67479b5908a91711d21babb14fd8ac50cdfd0f0b92fc1001d4319` |
| pinned `geng` binary | `588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1` |
| hostile independent probe | `0455d2352af1da63865afbd34afd94473bb7a57cb8675e9992c0de7500d7b8d5` |
| hostile mutation probe | `a503548bf4815059a52dfd09bb66744a891343ed34c55daa1e55345579472abe` |

## Prior-art and quantifier audit

Burger, Cockayne, Gründlingh, Mynhardt, van Vuuren, and Winterbach,
*Finite Order Domination in Graphs*, JCMCC 49 (2004), 159--175, introduced
smart \(q\)-secure domination.  Their Definition 9 quantifies over a complete
problem sequence and then a complete response sequence:

\[
  \forall(r_1,\ldots,r_q)\ \exists(u_1,\ldots,u_q).
\]

The paper's conclusion explicitly describes the entire problem sequence as
known in advance and proposes one-at-a-time revelation as a different future
model.  In particular, at horizon two the offline first response \(u_1\) may
depend on the future attack \(r_2\).

The kernel audited here is the adaptive-online truncation of the campaign's
eternal-family definition:

\[
  \forall r_1\ \exists u_1\ \forall r_2\ \exists u_2.
\]

Here \(u_1\) must be chosen before \(r_2\) is revealed.  These quantifier
orders are not interchangeable.  Klostermeyer and Mynhardt's 2016 survey,
*Protecting a Graph with Mobile Guards*, explicitly classifies eternal
domination as the adaptive-online problem and distinguishes it from a
predefined offline attack sequence.

The revised lemma correctly presents Burger et al.'s smart finite-order work
as related prior art, not as an equivalent online theorem; it also cites their
infinite-order follow-up as historical predecessor without importing its
offline finite-horizon quantifiers.  It makes no categorical novelty claim
for the general online kernel.  The mathematical audit below concerns the
online alternating-quantifier statement only.

## Proof audit

### Kernel hierarchy

For \(\mathcal X\subseteq\mathcal C_k\), the operator \(\Phi\) has exactly the
required quantifiers:

\[
 D\in\Phi(\mathcal X)
 \iff
 D\in\mathcal C_k\ \text{and}\
 \forall r\notin D\ \exists u\in D\cap N(r):
 (D-\{u\})\cup\{r\}\in\mathcal X.
\]

Thus attacks are only unoccupied, exactly one occupied vertex \(u\) is
removed, \(u\) is adjacent to the attack, and the attacked vertex is added.
Membership in \(\mathcal X\subseteq\mathcal C_k\) also requires the successor
to dominate.

At depth two, the nesting
\(\mathcal K_2=\Phi(\Phi(\mathcal C_k))\) has the online order
\(\forall r_1\exists u_1\forall r_2\exists u_2\).  The first successor must
belong to \(\mathcal K_1\), so the chosen \(u_1\) must work against every
possible later attack, not merely against one already known \(r_2\).

\(\Phi\) is monotone.  Since \(\mathcal K_1=\Phi(\mathcal K_0)\subseteq
\mathcal K_0\), monotonicity inductively makes
\(\mathcal K_{j+1}\subseteq\mathcal K_j\).  Finiteness forces stabilization,
and the stable set is a fixed point and hence an eternal family when
nonempty.  Conversely, closure of any eternal family \(\mathcal F\) proves
inductively that \(\mathcal F\subseteq\mathcal K_j\) for every \(j\).
Therefore the stable kernel is the greatest eternal \(k\)-family.

The interpretations are exact:

- \(\mathcal K_0\): every dominating \(k\)-configuration;
- \(\mathcal K_1\): every secure dominating \(k\)-configuration; and
- \(\mathcal K_2\): every configuration whose every first attack has a
  response in \(\mathcal K_1\).

### Forced-state stopping criterion

Under \(\alpha(G)=k\), the general bound
\(\alpha(G)\leq\gamma^\infty(G)\) and the kernel lemma give

\[
 \gamma^\infty(G)=k\iff\mathcal K_\ast\ne\varnothing.
\]

If an eternal \(k\)-family exists, repeatedly attack unoccupied vertices of
an independent \(k\)-set \(S\).  No guard already on \(S\) can be adjacent to
the attacked vertex of \(S\), so each legal response increases
\(|D\cap S|\) by exactly one.  The process reaches \(S\).  Hence every maximum
independent \(k\)-set belongs to every eternal \(k\)-family, including
\(\mathcal K_\ast\).

This proves the stated equivalence between nonempty stable kernel and
some/every maximum independent set surviving.  If even one such state is
deleted at a finite round, it cannot lie in the descending limit; equality is
impossible and integrality gives \(\gamma^\infty(G)\geq k+1\).

### Private-region swaps and the two-step theorem

For a dominating \(D\), unoccupied \(r\), and adjacent guard
\(u\in D\cap N(r)\), removing \(u\) can uncover exactly the vertices in

\[
 P_D(u)=\{x:N[x]\cap D=\{u\}\}.
\]

Adding a guard at \(r\) covers all of them exactly when
\(P_D(u)\subseteq N[r]\).  This establishes the swap criterion used at both
plies.

When \(\alpha=\gamma^\infty=k\), every maximum independent set \(S\) is
forced into an eternal family.  Closure after a first attack \(r\) supplies
an adjacent guard \(u\) and a dominating successor \(D\); the first
private-region containment follows.  Closure from \(D\) after every
unoccupied second attack \(t\) supplies an adjacent guard
\(v\in D\cap N(t)\) and a dominating second successor; the second containment
follows.

The explicit adjacency condition on the second guard is essential and is
present.  Unlike \(S\), the intermediate state \(D\) need not be independent,
so private-region containment alone need not imply adjacency.

The compact certificate is the exact contrapositive: for one forced
\((S,r)\), every legal first guard either gives an immediately
non-dominating state or gives a dominating state with a named unoccupied
second attack for which every adjacent second guard gives a non-dominating
state.  This proves \(S\notin\mathcal K_2\), and therefore
\(\gamma^\infty\geq k+1\).  No fixed-point computation is used in that
certificate.

### Complement form

For \(H=\overline G\) with \(\alpha(G)=3\), independent triples of \(G\) are
triangles of \(H\).  A triple dominates \(G\) exactly when no outside vertex
of \(H\) is adjacent to all three vertices.  Replacing adjacency in \(G\) by
nonadjacency in \(H\) yields all three displayed complement conditions.  The
document correctly labels this two-ply condition necessary, not sufficient.

### \(C_7\) strictness

The seven rotations of \(\{0,2,4\}\) are all maximum independent triples of
\(C_7\).  The four responses in the table dominate, so rotation shows that
every maximum independent triple passes the one-step condition.

For attack \(1\) from \(\{0,2,4\}\), move \(0\to1\) misses vertex \(6\);
the only dominating first move is \(2\to1\), yielding \(\{0,1,4\}\).
Attack \(3\) then has only guard \(4\) adjacent, and \(4\to3\) leaves vertex
\(5\) undominated.  Thus the specified state is in \(\mathcal K_1\) but not
\(\mathcal K_2\), proving strictness.  The hostile probe reconstructed all
seven maximum triples and these responses without campaign code.

## Source and verifier audit

The finder enumerates every maximum independent state and every unoccupied
first attack.  It scans exactly the guards in the state adjacent to that
attack.  A first successor is formed by removing that one guard and adding
the attacked vertex.  It is accepted only if it dominates and is secure
against every unoccupied second attack.  Security scans exactly the adjacent
occupied second guards and requires a dominating successor.

Consequently, the implementation also realizes the online quantifiers: it
accepts a first response only after checking that same response against all
second attacks.  It does not choose a different first response after learning
the second attack, as an offline
\(\forall(r_1,r_2)\exists(u_1,u_2)\) test could.

The certificate verifier recomputes \(\alpha\), maximum independence, legal
first-guard and second-guard sets, domination, occupancy, adjacency, and an
explicit undominated witness for every failed swap.  It requires exact tuple
types, exact record counts, unique guard keys, and exact equality with the
recomputed guard sets.  Invalid values fail closed under the guarded
exception types.

`reviews/two_step_transition_hostile_mutations.py` submitted 28 decisive
mutations, including:

- negative, Boolean, out-of-range, nonmaximum, and nonindependent states;
- occupied, Boolean, and out-of-range attacks at both plies;
- missing, duplicated, wrongly typed, and nonadjacent guards;
- false and out-of-range undominated witnesses;
- missing, mixed, and doubly populated failure modes; and
- list-for-tuple substitutions.

All 28 were rejected.  Seven malformed/occupied calls to the hardened
successor helper also raised `ValueError`.  The mutation run completed in
about 0.001 seconds.

All six source tests pass in 0.104 seconds.  In addition to \(C_7\), \(C_6\),
tamper, and helper tests, the suite compares the finder with an explicit
\(\mathcal K_2\) oracle on every labeled graph through order five.

## Independent computational replay

`reviews/two_step_transition_hostile_probe.py` imports no campaign Python
module.  It implements a fresh strict graph6 decoder, graph adjacency as
tuples of `frozenset` objects, ordinary-set domination and independence,
independent gamma/alpha checks, a fresh three-clique-partition backtracker,
one- and two-ply predicates, and a fresh full eternal fixed point.

Against the final bound result it independently reproduced:

| Edge-toggle outcome | Graphs |
|---|---:|
| selected population | 8,587 |
| one-step rejected | 4,169 |
| additional second-step rejected | 3,892 |
| total two-step rejected | 8,061 |
| survives two steps | 526 |

It also streamed the complete pinned `geng -qc` output:

| Order | Connected unlabeled | Static targets | One-step | Additional second-step | Survivors |
|---:|---:|---:|---:|---:|---:|
| 5 | 21 | 0 | 0 | 0 | 0 |
| 6 | 112 | 0 | 0 | 0 | 0 |
| 7 | 853 | 5 | 2 | 3 | 0 |
| 8 | 11,117 | 78 | 51 | 27 | 0 |
| 9 | 261,080 | 1,569 | 1,134 | 435 | 0 |

The independent replay also found no eternal three-guard graph among these
static targets and verified that the two-step test rejected no independently
eternal state.  It completed in 61.713 seconds (61.76 seconds real) with
maximum resident set size 26,329,088 bytes.

The production result was regenerated after helper hardening, with unchanged
counts.  It records 94.032 seconds wall time and peak resident size
26,279,936 bytes.

These are measurements of the frozen populations.  They do not prove that
all graphs of a higher order fail the condition, that the 526 survivors are
eternal, or that the universal conjecture holds.

## Low-severity reproducibility note

The measurement JSON pins the main measurement source, edge-toggle ledger,
and `geng` binary, but it does not list hashes for imported
`search/private_obstruction.py` and `verifier_a/core.py`.  This does not affect
the accepted theorem or the independently reproduced final counts, and the
eventual repository commit will freeze those dependencies.  For a standalone
archive, include a complete runtime source manifest or environment hash.

## Accepted claim boundary

Proved:

> If \(\alpha(G)=\gamma^\infty(G)=k\), every maximum independent \(k\)-set
> lies in \(\mathcal K_2\), equivalently every first attack has a legal
> dominating response that is itself secure.  A compact certified violation
> proves \(\gamma^\infty(G)\geq k+1\).

Observed and independently reproduced:

> The recorded depth-two filter removes 8,061 of the 8,587 selected
> edge-toggle rows and all static \(\gamma=\alpha=3<\theta\) targets through
> connected-unlabeled order nine.

Not proved:

- sufficiency of membership in \(\mathcal K_2\);
- a complete order-10-or-higher nonexistence result; or
- resolution of the gamma--theta conjecture.

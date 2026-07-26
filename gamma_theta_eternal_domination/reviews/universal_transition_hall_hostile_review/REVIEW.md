# Hostile review: transition/restoration/Hall lane

Date: 2026-07-26 (PDT)

## Frozen target

- Note:
  `math/working/universal_transition_private_neighborhood_attack.md`
- SHA-256:
  `71384d66373ab4cbffa7ced60973971cf39b72a0315eac31ad522abd1afa2f47`
- Model audited: attacks only at unoccupied vertices; exactly one adjacent
  guard moves to the attacked vertex; every family state dominates.

## Verdict

**ACCEPT.**

The restoration lemma, viable-list Hall theorem, static obstruction
corollary, and Proposition 5.1 are sound as stated.  I found no import of an
all-guards model, no occupied-attack step, and no circular use of the
gamma--theta conjecture.  The note correctly stops short of claiming either
a universal proof or a finite-order advance.

During review, the official replay log no longer hashed the current evidence
JSON.  The maintainer identified an accidental default-output replay and
rebound the log to the unchanged mathematical payload.  The archival issue
is now resolved; details are below.

## Hostile proof audit

### Theorem 3.1: restoration

For fixed \(u\in U=S-D\), every requested restoration vertex is unoccupied
when attacked.  Independence of \(S\) prevents every currently occupied
vertex of \(S\) from responding, so each response consumes one of the
remaining outside guards and restores one distinct vertex of \(S\).  After
\(|U|-1\) attacks the state is \(S-u+x\), with \(x\) one of the original
outside positions.  The final attack at \(u\) is unoccupied and can only be
answered by \(x\), proving \(ux\in E(G)\); family membership already proves
that \(S-u+x\) dominates.  Thus \(u\in L_S(x)\).

The proof correctly restarts from \(D\) for each choice of \(u\).  It claims
only coverage of \(U\) by the lists, not one common restoration sequence or
an injective assignment, so no quantifier is being exchanged.

### Theorem 4.1: Hall

When the vertices of an independent outside set \(X\) are attacked from
\(S\), a guard previously moved to \(X\) cannot answer a later attack in
\(X\).  Hence the responses remove \(|X|\) distinct guards of \(S\) and
produce \(D=(S-U)\cup X\) with \(|U|=|X|\).  Theorem 3.1 then gives
\(U\subseteq\bigcup_{x\in X}L_S(x)\).  Applying the same inequality to
every subset of \(X\), which remains independent, is exactly Hall's
condition.  This argument is online and uses only one guard per response.

Corollary 4.2 is also valid, provided its explicitly stated premise
\(\alpha(G)=k\) has been certified independently: failure of Hall rules out
an eternal \(k\)-family, while \(\alpha\leq\gamma^\infty\) supplies the
integer lower bound.

### Proposition 5.1: exact static equivalence

The forward implication is immediate from the clique fibers and
\(\alpha\leq\theta\).  Conversely, a partition into \(k=\alpha(G)\) cliques
meets the maximum independent \(k\)-set \(S\) once in every part.  Every
vertex of \(P_S(s)\) must lie in the part containing \(s\), since it is
nonadjacent to all other representatives.  Therefore every outside vertex
assigned to the \(s\)-part has all of \(P_S(s)\) in its closed
neighborhood, including the harmless case where the two vertices coincide.
The one-swap criterion gives membership in \(L_S(x)\).  No eternal-family
assumption is hidden in this proposition.

The proposition is an exact reformulation of the missing global
compatibility, not progress by itself toward proving that compatibility;
the source makes this boundary explicit.

## Independent replay

I reran

```text
python3 -I -B -W error \
  math/working/universal_transition_private_probe.py \
  --max-order 9 --minimal-family-max-order 6 \
  --output /tmp/universal_transition_private_hostile_replay.json
```

The replay completed successfully and reproduced:

- 3,585 equal-parameter graphs through order 9;
- 37,358 maximum-independent reference states;
- zero viable-list Hall violations;
- 87 inclusion-minimal families through order 6, eight with a static-label
  obstruction; and
- 78 minimum-cardinality families through order 6, with zero observed
  static-label obstructions.

It also reproduced the declared `C7`, `C15`, `E]~o`, `FUzro`, and
`J@l|bfNuVK_` witnesses.  The replay differs from the current evidence JSON
only in the nondeterministic elapsed-seconds field.

Probe SHA-256:
`e531e19ee32d7540b5691dc2488676b234e7fa63d5a6a2e27bda6c3dfbdea05e`.

## Resolved archival correction

At the first review pass,
`results/universal_transition_private_probe.log` recorded evidence SHA-256
`08c80c48...`, while the current
`results/universal_transition_private_probe.json` hashed to

```text
771738d7f2d3b0f384c2276f4ac4bb7fc1da18c285f169f7c606184539f09841
```

The maintainer confirmed that the JSON had been replayed accidentally through
the probe's default output; the mathematical payload was unchanged apart
from elapsed time.  The official log now records the displayed JSON hash and
the matching elapsed time.  Its frozen SHA-256 is
`1e0ac23f8e622dd5797142b64e013152d311f7cd03e56214809216d2f5dac7c5`.
The finite evidence bundle is therefore internally bound.

No literature-novelty or publication-priority judgment is made.

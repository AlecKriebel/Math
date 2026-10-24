# Independent source/priority challenge: Kourovka21.121

UTC:2026-10-24T23:36:10Z. Source-audit completion **100% for the bounded scope
below**; mathematical discovery **0%**. Verdict: **part(b)'s provisional
eligibility was not refuted**. Part(a) is prior solved work. No complete prior
answer to(b), or existing theorem implying it for every abstract p-Jordan
group, was located. This is not a proof of exhaustive absence or a novelty
certificate.

## Independence and comparison

`INDEPENDENT_BASELINE.md` and `INDEPENDENT_KNOWN_SCOPE.md` were written before
reading the existing21_121/priority conclusions. They derive the quantifiers
and distinguish the known results from directly inspected primary sources.
Only afterward did I compare the preparation. Its scope agrees with these
independent findings; no substantive source-contract correction is needed.
The parent's frozen preparation manifest was independently checked, together
with all24 source records and four reused official-cache files. The checker
does not execute or import the author's preparation checker.

## Exact remaining target

The authoritative entry is21.121, C. Shramov, printed page197 of the current
21st Notebook. The [official October update](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-3.pdf)
was freshly downloaded here; its complete problem block agrees with the main
Notebook cache. The star and editorial negative-answer note attach to(a).
The official repository likewise links(a). These facts are corroboration;
the absence of a star on(b) is not the sole basis of this audit.

Fix a prime p. The group Gamma is arbitrary and abstract. For **each** finite
H<=Gamma one needs a subgroup A normal in H, abelian, and of order prime to p,
with `[H:A]<=J*|H_(p)|^s`. The same J and s work for all such H; they may depend
on Gamma and p. A need not be normal in Gamma. The notation H_(p) denotes a
Sylow-p subgroup, not all p-elements or the verbal power subgroup. Its order
is the p-part of |H|.

The target(b) is `inf E_p(Gamma)<=3`. It permits an exponent-dependent constant
at every `3+epsilon`; it does not require a bound at exactly3. A genuine
counterexample must have a finite infimum strictly bigger than3, not merely
fail attainment at3. The real-exponent convention and degenerate bounded
Sylow cases are recorded in the independent baseline. They yield no new
counterexample. The published positive finite infima in(a) avoid the issue.

Finite-factor constructions must also control **every subgroup** of each
factor. Intersecting a normal abelian p'-subgroup with a subgroup preserves
normality and p'-order but does not replace the overgroup's Sylow-p order by
the subgroup's smaller Sylow-p order. Ignoring that change can invalidate an
otherwise plausible ambient p-Jordan claim.

## Why the known counterexamples and restricted theorems do not close(b)

* **Jayadevan:** both the September14 record22751568 and October16
  record23421603 give the admissible exponent set `(1,infinity)` for the
  constructed groups, so their infimum is1. The all-finite-subgroup quantifier
  is explicit. I checked both cached API metadata records and independently
  matched each PDF's MD5 with its reported file checksum. The extracted
  mathematical texts coincide after removing the original affiliation and
  normalizing whitespace. The author exposition was independently retrieved
  and agrees with that theorem scope. This is prior(a), not a counterexample(b).
* **Kinyon--Urban:** the official-hosted [mathematical PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf)
  is version4 of September19, although the Notebook cites the September17
  preprint. Its sections3.45 and4.3 separate(a) from(b). The latter retains
  soluble or normal-Sylow assumptions in exponent-two bounds and gives a
  nonsoluble exponent `log60/log4<3`. Its finite-kernel permanence requires the
  stated generalized p-Jordan hypothesis. It expressly leaves the unrestricted
  bound unresolved. No claims in those proofs were silently promoted to all
  abstract groups.
* **Larsen--Pink:** [Theorem0.4](https://people.math.ethz.ch/~pink/ftp/LP5.pdf)
  is cubic for finite subgroups of GL_n in characteristic p, with fixed n and
  a constant depending on n. It does not bound the dimensions needed to
  represent arbitrary finite subgroups of an arbitrary p-Jordan Gamma.
  Brauer--Feit is the earlier representation-theoretic source, not a separate
  universal abstract-group cubic theorem.
* **Hu:** [1804.10946v2](https://arxiv.org/html/1804.10946v2), Definitions1.2/1.6
  and Theorems1.5/1.7, retains a distinction between generalized p-Jordan
  control of p'-subgroups and the full p-Jordan property. The algebraic-group
  theorem supplies an upper exponent under algebraic hypotheses. Its coarse
  upper exponents above3 are not lower bounds for the optimal infimum. Its
  product and extension estimates cannot be read as exact optimal exponents.
* **Chen--Shramov:** the current [rank-two Cremona result,
  2509.15522v3](https://arxiv.org/abs/2509.15522), revised March30,2026,
  sharpens constants inside that geometric class. The earlier2024 paper also
  distinguishes abelian conclusions from nilpotent ones. Neither removes the
  geometric hypotheses to settle(b).
* **Additional implication checks:** Bajpai--Dona's current
  [2411.11632v2](https://arxiv.org/html/2411.11632v2), Theorem1.2, still starts
  with a finite subgroup of GL_n. Tracey's [2105.10998v2](https://arxiv.org/abs/2105.10998)
  concerns p-element proportions with representation/permutation hypotheses;
  it is not a universal p-Jordan exponent theorem. Their titles do not supply
  a missing abstract-group implication.

## Search coverage, access limitations, and residual uncertainty

Queries covered the exact number/subpart, p-Jordan exponent/infimum, upper
bound three, arbitrary/all groups, counterexamples, generalized and historical
"strongly p-Jordan" terminology, and recent linear/geometric papers. Scope
was checked at the actual definitions or theorem statements wherever used.
Search-engine results from aggregators and unrelated uses of the integer
21.121 were discarded rather than treated as evidence. Domain-limited
MathSciNet/zbMATH searches found no useful exact record; their direct research
databases were not exhaustively queried. Unindexed, unpublished, or subsequent
work cannot be excluded.

My fresh Zenodo public/API requests returned403, and the author-linked GitHub
API path returned404. I did not bypass these responses. After preserving the
independent baseline, I used the preparation's already authenticated primary
API/PDF cache and independently verified metadata, checksums, dates and the
mathematical text comparison. This is explicitly a cached-primary check, not
a claim of a successful new live Zenodo retrieval. The successful fresh
official PDF and author-page bytes match the corresponding preparation files.

No Lean source archive was built; no exhaustive adversarial audit of the
published proof packages is claimed. Only the original problem, attribution,
known result scope and absence of a located complete(b) implication were
audited. No outside person or unrelated agent was contacted; no queue, PR,
publication, Git or tracker operation occurred.

The result supports selecting **only21.121(b)** for research, subject to the
parent's own source gate. It does not select a theorem to assume, certify
originality of a future result, or mark any new mathematical problem solved.

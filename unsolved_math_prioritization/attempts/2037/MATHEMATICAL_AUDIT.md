# Erdős 302: bounded audit of established partial results

Audit date: 10 October 2026. Credit: Stijn Cambie (elementary lower construction), Dmitry Khanukov (corrected two-sided manuscript, padding argument, hierarchical upper certificate), Donald Della Pietra (upstream structured construction and analytic formal developments), and the earlier upper-bound authors identified below. This is an audit of prior work, not a new target attempt, novelty claim, or solution of the extremal-density problem.

This AI-assisted audit edition is unrefereed. It preserves the recorded mathematical disposition and substantive arguments of the 10 October 2026 audit. All source-inspection and finite-check descriptions below are historical audit results. Edition preparation checked the retained evidence identities but did not rerun mathematical programs, execute Lean or third-party code, or install dependencies. No human referee review, journal acceptance, formal certification, or exhaustive priority search is claimed.

## Disposition

1. **Accept the known negative answer to the subsidiary half-density conjecture.** Cambie's construction proves `liminf f(N)/N >= 5/8`, and therefore disproves `f(N) = (1/2 + o(1)) N`.
2. **Accept the stated upper bound by an independently authored finite checker plus the audited mathematical transfer:**
   `limsup f(N)/N <= 140803024/163562355 = 0.860852266403232...`.
   All finite inputs needed for this implication were regenerated or checked exactly in this audit. No author-supplied program or Lean development was executed.
3. **Accept Khanukov's lower padding implication, with the upstream witness explicitly conditional in this audit.** Its precise hypothesis is the structured witness stated below. The literal upstream interfaces and their assembly agree with that hypothesis. **Hold unconditional independent acceptance of `5/8 + delta`**, because the full upstream analytic proof closure has not been independently replayed or mathematically verified end to end here. This is a verification hold, not a demonstrated counterexample or a claim that the source's theorem statement contains an extra assumption.
4. No convergence theorem, exact limiting density, full solution, or new explicit numerical improvement above `5/8` is accepted or claimed.

## 1. Exact problem and historical answer

Let `f(N)` be the largest size of a subset of `{1,...,N}` that contains no **three pairwise distinct** integers `a,b,c` with `1/a = 1/b + 1/c`. Positivity is part of the ambient interval. Allowing equal tails changes the problem: the prohibited pair would include `a,2a`.

The original reference is Erdős and Graham, *Old and New Problems and Results in Combinatorial Number Theory* (1980), printed p. 37. The historical source review retained the complete author-archive book and inspected the cited page. The [official problem record](https://www.erdosproblems.com/302) and Khanukov's bibliography attribute the following construction to Cambie; this audit makes no priority claim.

Take all integers greater than `N/2`, together with all odd integers at most `N/4`. Its cardinality is exactly

`N - floor(N/2) + floor((N+4)/8) = 5N/8 + O(1)`.

Here is a complete verification. Order the distinct tails as `b<c`. The equation implies `a<b<c` and `2a<c<=N`, so the head cannot belong to the upper half. Thus it is odd and at most `N/4`. The identity `bc=a(b+c)` forces both tails to be even: both other parity patterns contradict the identity modulo 2. They consequently lie in the upper half. Hence `1/b+1/c<4/N<=1/a`, a contradiction. This proves the claimed lower bound, regardless of the status of any later manuscript.

## 2. Pinned release and source identity

The primary audited work is Dmitry Khanukov, *Two-sided computer-assisted progress on Erdős Problem 302*, corrected version 0.2.0-preprint, dated 13 September 2026, preliminary and unrefereed.

- [Corrected release](https://github.com/khanukov/erdos302/releases/tag/v0.2.0-corrected-preprint)
- Exact release commit: `3e400a3807d22f711c7998f9537f49991925231a`
- Annotated tag object: `e0a90a9a75ff8d9f005df148c61fe27e77fddfd7`; its target was read and matches that commit
- [Complete 10-page PDF](https://github.com/khanukov/erdos302/releases/download/v0.2.0-corrected-preprint/erdos302-v0.2.0-preprint.pdf): 257164 bytes, SHA-256 `41aa056d67a4f242d15cd150abf954fc23011b27fcdbbb2a80d2535b20274c3a`
- Complete TeX: 25656 bytes, SHA-256 `c2d2c460f9ba73f5ab9af917d8e1712658e3127b9f063ccd4066855cd58c59f1`
- [Exact certificate JSON](https://github.com/khanukov/erdos302/blob/3e400a3807d22f711c7998f9537f49991925231a/certificates/q139708800/certificate.json): 2705728 bytes, SHA-256 `ca682b3e13d5fb5e6bc2e6ff5935718dbf0fb5a6a7b6a37f568edbdfafb89036`

The release API's public asset digests agree with these bytes. All manuscript sections, proofs, caveats, and bibliography were inspected through its complete text and TeX; PDF pages 3, 7, and 8 were additionally rendered and visually checked in this audit. The historical source review also recorded inspection of PDF page 2. The source repository main commit observed during the 10 October 2026 audit was `a60f43511ce0741ef6e80bdb9b620c5bf854f81c`. Its additional explicit-lower overlay is outside the released qualitative theorem audited here and is not silently imported into this acceptance.

## 3. Upper finite certificate: complete independent reproduction

For `Q=139708800=2^7*3^4*5^2*7^2*11`, regenerate the sorted divisors other than 1. There are 719. A triple is encoded only when `a<b<c` and `bc=a(b+c)`. Two independently written enumeration paths, one solving for `c` from `a,b` and the other for `a` from `b,c`, agree on exactly 12675 triples.

A configuration consists of a support whose induced hypergraph requires at least a stated number of deleted vertices. Each edge has demand 1. For the smaller divisor tile `Q0=3360`, the audit independently solves the minimum hitting-set problem for **all 47 prefixes**, supplies actual covers, and proves optimality by exhaustive include/exclude branching. The 21 first thresholds are

`6,12,24,30,40,42,56,84,96,105,120,140,210,224,240,336,420,560,1120,1680,3360`.

The search discards a triple containing a mandatory pair, forces singleton edges, and uses a disjoint-edge lower bound. Otherwise it splits on whether a chosen vertex belongs to the cover. Both branches are exhaustive. The terminal budget test precedes the empty-instance test; all returned covers are checked. This is a separately authored algorithm, not execution or import of the author's exact verifier. Its result was also compared with brute-force subset enumeration on 320 deterministically generated hypergraphs of up to eight vertices, with additional singleton and pair controls.

Each of the 96 divisors `m` of `Q/Q0=41580` scales each certified base prefix into `Div(Q)`. Multiplication is injective and preserves the reciprocal identity in both directions. All mapped base edges were explicitly checked, producing 2016 valid configurations in addition to the 12675 edges. The reconstructed numbered configuration digest is

`b6d0d19a51029400cc63e8cca5a4b7e1da99f7d4e6b62a479d5ed92cb8a1eafa`.

The certificate was treated solely as untrusted JSON data. Every index, support containment, rational sign, rational denominator, duplicate ID, per-vertex load, objective, prefix endpoint, ordering, and target/threshold ledger was checked. All 271 rational packings pass. There are 274 certified cover levels because three prefixes raise the certified lower bound by two. The exact reciprocal threshold sum is

`S = 3251333/4989600`.

The checker and all controls pass under normal Python, `-O`, and `-OO`. Sixteen deliberate corruptions are rejected, including insufficient objective, overloaded vertex, negative weight, zero denominator, duplicate ID, out-of-prefix support, inflated demand, wrong endpoint, missing/duplicated certificate, changed base threshold, digest, ledger, density, final bound, and objective metadata. This establishes the finite certificate without relying on floating-point optimization, a third-party solver, author-produced executable results, or a Lean cache.

## 4. Upper transfer: audited mathematical proof

If configurations `(S,r)` receive nonnegative weights and the total load at every vertex is at most 1, every cover `C` satisfies

`sum r*y <= sum |C intersection S|*y <= |C|`.

Consequently objective strictly greater than `k-1` forces integral cover size at least `k`. This verifies the interpretation used by the checker; no equality with a large-tile minimum cover number is assumed.

For each fixed positive `R`, restrict multiplier valuations at a prime `p^e || Q` to `0,e+1,...,(R-1)(e+1)`, with no restrictions at other primes. If `md=m'd'` for divisors `d,d'` of `Q`, reducing each valuation modulo `e+1` recovers the same valuation of `d,d'`; hence `d=d'` and `m=m'`. Thus the multiplier blocks are pairwise disjoint.

For this finite set of valuation options, elementary CRT and inclusion-exclusion give multiplier counting function `rho_R*x + O_{Q,R}(1)`, with

`rho_R = product_p (1-1/p)*sum_{j=0}^{R-1} p^{-j(e+1)}`.

For a triple-free set in `{1,...,N}`, the omissions in each truncated block form a cover. If `t_k` denotes the audited nondecreasing level ledger, that block contributes at least `sum_k 1_{m*t_k<=N}` omissions. Disjointness allows summation without double counting. With `R` fixed, dividing by `N` and taking `N` to infinity gives omitted lower density at least `rho_R*S`. Only afterwards let `R` tend to infinity. This avoids an unjustified uniform error term in `R`.

The exact product is `rho=23520/110143`; hence omitted lower density is at least `22759331/163562355` and the stated limsup upper bound follows. Convergence of `f(N)/N` is neither used nor proved.

## 5. Lower padding: fully audited conditional implication

The required upstream assertion is: for fixed `L`, fixed auxiliary parameters, and every sufficiently large `N`, a set `C_N` exists with

- all-distinct reciprocal-relation avoidance for every tail length at least two;
- each point either odd with `N<3n` and `2n<N`, or in the closed top half `N<=2n`;
- cardinality at least `(1/2 + rho_L/24)N`, where `rho_L=phi(P_L)/P_L` and `P_L` is the product of **all** primes below `L`, including 2.

For `O_N` the odd integers with `4n<=N`, the two sets are disjoint. If a forbidden triple in `C_N union O_N` has head in `C_N`, the head cannot be in its top half since `2a<N`. Its low-band position puts both larger tails beyond `N/4`, so all three points are in `C_N`, impossible. If the head is in `O_N`, the parity calculation forces both tails to be even. They cannot belong to either odd layer and thus satisfy `b,c>=N/2`. Distinctness makes at least one reciprocal inequality strict, giving `1/b+1/c<4/N<=1/a`, again impossible. The closed-half boundary is handled correctly.

Since `|O_N|>=N/8-1`, the result has size at least `(5/8+rho_L/24)N-1`. Positivity of `rho_L` and `N>=48/rho_L` give the eventual lower bound with `delta=rho_L/48`. No numerical `L` is furnished or needed for this conditional inference.

## 6. Exact upstream source and semantic audit

The lower project uses:

- [Della Pietra EP301](https://github.com/donalddellapietra/erdos-301-proof/tree/789c6f045dbc81da3811031247d186a7128dafce), commit `789c6f045dbc81da3811031247d186a7128dafce`
- [Della Pietra EP327 analytic library](https://github.com/donalddellapietra/erdos-327-proof/tree/a7201442f71af90a8e7b930f993c8eec69f685cf), commit `a7201442f71af90a8e7b930f993c8eec69f685cf`
- `teorth/mathlib4` commit `da1f94df976c7cd38117281c57d6ee3046c8d104`
- Lean `v4.33.0-rc1`.

This differs from the upper project's Lean `v4.27.0` and stock Mathlib pin `a3a10db0e9d66acbebf76c5e6a135066525ac900`. Complete Lake manifests, including all ancillary exact package revisions, were retained and hashed. No dependencies were installed.

The audit read the literal `Relation`, `Admissible`, `LowBand`, `TopBand`, `roughThirdSet`, repaired-carrier construction, numerical budget structure, and downstream maximum definition. They have the required positivity, all-pairwise-distinctness, tail-length quantification, interval bounds, and cardinality semantics. The downstream wrapper `exists_structured_roughThird_witness` obtains its witness from `exists_eventualRoughThirdBudgets`; it does not simply invoke an abstract EP301 density theorem and infer the extra structure.

The exact cardinality ledger is top loss at most `rho_L*N/48`, low source at least `rho_L*N/12`, and bad low heads at most `rho_L*N/48`. Their combination is the required `rho_L*N/24` excess. The upstream parameter choice fixes `L>=17` before the eventual `N` threshold. The density product includes 2, so no factor-of-two ambiguity is present.

All 26 EP301 Lean modules (3771 lines) and all 92 EP327 Lean modules (30683 lines) at these pins were acquired as data and checked against their repository Git blob IDs. A comment/string-aware lexical guard found no `sorry`, `sorryAx`, `admit`, `axiom`, `opaque`, `unsafe`, or `native_decide` token in these sources. This is a source guard only; it is not a Lean parser, transitive axiom computation, proof-term check, or full review of those 34454 lines.

The upstream human EP301 manuscript was read in full. Its analytic route cites Tenenbaum's *Introduction to Analytic and Probabilistic Number Theory*, third edition (2015), Theorem III.3.5, and de la Bretèche–Tenenbaum, [*Mean values of arithmetic functions and application to sums of powers*](https://arxiv.org/abs/2403.19320v6), Theorem 3.1. The latter source was retrieved in full and its actual uniformity conditions and root-density statement inspected. The geometrical localization, parametrization `a=trs,b=tr(r+s),c=ts(r+s)`, parity, finite density ledger, and strict numerical parameter window check out; the five strict margins were independently recomputed with rational logarithm bounds.

Crucially, the upstream Lean proof is **a different quantitative analytic route**, using a finite weighted sieve and residual estimates proved in the EP327 library, rather than simply treating the two published analytic theorems as imported axioms. It also uses a different parameter point (`A_h=1.000001`, `q_h=2.48933`) from the human manuscript (`A_h=1.0001`, `q_h=2.48909`). Agreement of the final existence statements does not license conflating these two proof chains.

The [EP327 exposition PR #1](https://github.com/donalddellapietra/erdos-327-proof/pull/1), open at the 10 October 2026 historical inspection, was checked: the listed changes include manuscript, Python verification exposition, and PDF material, and no Lean file. The pin was not silently advanced.

## 7. Exact remaining holds

**H-L1, upstream mathematical closure:** this audit has not independently verified all estimates and uniform constants needed by the EP301 human analytic route against a complete primary copy of Tenenbaum's cited theorem, nor the entire separate EP327 finite-sieve/centered-tail/residual formal argument. Acceptance of the unconditional new lower bound cannot be based merely on the correct padding proof, matching interfaces, lexical scans, finite proxy experiments, or positive parameter margins.

**H-L2, formal reproduction:** no local Lean build, source rebuild of the upstream closure, `leanchecker --fresh`, or local axiom-report reproduction was performed. The [exact-release Verify run](https://github.com/khanukov/erdos302/actions/runs/34734328134) is a successful push run for the exact release commit, and its listed lower and upper jobs succeeded. These are verified public CI metadata and author-side evidence, not this audit's own proof replay. The reported axiom allowlist is `propext`, `Classical.choice`, `Quot.sound`. The lower author workflow's cached `.olean` inputs, their serialization, the prerelease Lean kernel/toolchain, the Mathlib fork, OS, and hardware remain disclosed trust boundaries. The upper independent mathematical acceptance above does not need this replay.

Closing the lower hold requires a pinned full formal replay with semantic checks and reported trust boundaries, or a complete mathematical audit of an adequate upstream analytic route. Neither closure is supplied by this edition.

## 8. Prior ingredients and prohibited transfers

Wouter van Doorn's direct `9/10` bound, his transferable five-point `25/28` argument, Xinjun Wang's EP301 divisor-tile method, and the anonymous July 2026 `373/420` partial note are prior ingredients, not new findings here. Their original priority/status beyond the cited source records is not adjudicated by this audit.

In particular, EP301 forbids all tail lengths, and its admissible sets form a subset of EP302's. An upper bound for EP301 therefore does **not** automatically upper-bound EP302. Wang's `667/806` theorem is not imported. The independent checker instead recomputed the two-tail hypergraph on nontrivial divisors of 720 and found cover thresholds

`6,12,24,30,40,48,90,120,144,180,240`.

Their reciprocal sum is `293/720`; the multiplier density is `120/403`; the valid specialized comparison is therefore `2125/2418`. This is exactly the corrected distinction made by Khanukov. EP303's coloring problem and EP327's differently formulated problem are not treated as duplicate solutions.

## 9. Publication scope and verification boundary

This edition supplies authored mathematical audit and acceptance prose, citations, and public verification metadata. It does not distribute executable checkers, Lean modules, certificate contents, raw datasets, copied manuscripts, source-derived images, or detailed test outputs. The complete public certificate remains available at its credited upstream URL; this edition reports its pinned identity and the historical independent check results, rather than providing a self-contained executable reproduction package.

No third-party program, Lean development, or mathematical checker was executed during edition preparation, and no dependencies were installed. The accepted upper bound rests on the recorded independent exact checks and audited mathematical transfer. The unconditional lower improvement remains on H-L1/H-L2 hold. No claim of independent human referee review is made.

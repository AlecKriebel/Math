# Independent audit: Erdős 156 interval saturation

Audit date: 2026-10-21 UTC. Outcome: the elementary lemmas and finite certificate below pass. They do not resolve the every-N cubic-root upper-bound problem. No novelty or exhaustive literature-priority claim is made.

## Exact convention and criterion

Use ordinary Sidon: unordered pair sums include repeated summands. Let S be Sidon and x∉S. A new equality must involve x. A collision between x+a and x+b cancels to a=b; a collision between 2x and x+a forces x=a. The only genuine possibilities are x+c=a+b with a,b,c∈S, or 2x=a+b with a,b∈S. In the first, c∉{a,b}, because otherwise x∈S. In the second, a≠b for the same reason. Both equations conversely give distinct unordered pairs and hence violate Sidon. Therefore both triple and midpoint blockers are necessary for an exact test. For S={1,3}, x=2 is blocked solely by its midpoint equation and would be missed by a triple-only test.

## Counting audit

For k=|S|, there are k[binom(k+1,2)−k]=k²(k−1)/2 allowed triple expressions: choose c, then an unordered pair with repetition from S\{c}. Integer midpoint expressions number binom(e,2)+binom(o,2), where e,o are the even and odd element counts. Union bounding these expressions and S gives, for maximal S in an interval of length N,

2N ≤ k³+k−2eo ≤ k³+k.

Duplicate or out-of-interval expressions only weaken this bound and cause no invalid inference. Consequently g(N)≥(2N)^(1/3)−O(N^(−1/3)). This is a necessary bound, not a sufficient criterion for existence at a proposed size. Translation swaps parity counts at most, preserving eo.

## Difference-budget audit

Let S⊂[1,N] be Sidon, U the points that can individually be added to S, and D a finite set of positive integer distances. Suppose every x∈U has a seed anchor s∈S such that |x−s|∈D. Any Sidon extension T⊃S satisfies

|T\S| ≤ |D\Δ(S)| ≤ |D|,

where Δ(S) is the set of positive differences of S. Indeed, positive differences of an ordinary integer Sidon set are unique. For each x∈T\S choose one seed anchor; the resulting unordered pairs {x,s} differ for distinct added x because x is outside S. Their differences are distinct and cannot already occur within S. Finiteness allows a maximal extension. The empty-seed case is harmless: the covering hypothesis then forces U empty.

In particular, if every initially addable point has a residue modulo q represented by S, use D={q,2q,...,floor((N−1)/q)q}. This gives a maximal extension of size at most |S|+floor((N−1)/q). No claim that modular maximality alone establishes that hypothesis is allowed. The local Ruzsa source inspected in this audit already uses a signed-difference completion argument; the positive-difference version is a constant tightening/reformulation, not logarithm removal or a verified new result.

## Lifting and interval pitfalls

- A modular ordinary Sidon set with one lift per residue remains integer Sidon. Integer maximality does not follow, because modular collisions need not be equalities over integers.
- Explicit negative control: {0,1} is maximal ordinary Sidon modulo 5, but {0,1,3} is integer Sidon inside {0,...,4}. The modular obstruction for 3 includes 2·3≡0+1, not an integer equality.
- Arbitrary interval truncation does not preserve maximality: {0,3,4} is maximal on {0,...,6}, but its restriction to {0,1,2} is {0}, which is not maximal.
- Taking several translated copies generally destroys Sidon by repeating differences. A proof must supply actual integer blockers in the target interval, not merely congruences.
- A selected-length construction still needs a justified every-N argument; truncation or a modular covering assertion cannot substitute for it.

## Finite verification and exact scope

`independent_audit.py` uses direct unordered-pair-sum uniqueness and imports nothing from the research solver. It exhausts every subset of {0,...,N−1} for 1≤N≤15, checks the blocker equivalence against direct one-point addition, and checks the parity inequality on every maximal set. It obtains g(N)=1,2,2,2,3,3,3,3,3,3,4,4,4,4,4, agreeing with the author's independent run after translation. This is finite evidence only.

The eight-element certificate A={8,48,68,69,71,75,104,120}⊂[1,144] passes separate direct checks: 36 distinct unordered pair sums; all 136 absent points fail one-point extension; every saved witness is valid. It proves existence of this saturated eight-element set. It does not independently verify that length 144 is the largest possible for eight elements, nor prove g(144)=8.

Audited certificate SHA256: e5d8dc74ef03f2f63664544c89c246b0ed332b3e80f9070d9f62dfbf79e247af.
Independent verifier SHA256: 6b7406b8281cf2c8d7cb3cac2dd9b8d25c8284736b2a0ffcd2b00256269e6a22.
Independent results SHA256: 015595fea27430015fdded5f1c9f86fc9763f0482f120d3f8e5e36285cbfceb5.

The artifact hashes bind only the listed versions; subsequent edits require re-audit. Source-status caveats remain those recorded in SOURCE_GATE.md: open status is not a guaranteed exhaustive contemporary literature verdict.

## Additional draft-lemma checks

The completion lemma permits a free exception set H: remove the at most |H| added points belonging to H, then apply the same injection to the others. Thus the bound becomes |D\Δ(S)|+|H| without disjointness assumptions on the translates or H.

The random-lift objective p+1+floor((N−1)/q)+N exp(−c′p³/N) follows by using outside-residue exceptions as H and the seed-residue multiples as D. Its requirement of logarithmic p³/N applies only to making that displayed upper estimate small by individual-exception repair, not to all realizations of the random model or to all possible repairs.

The interpolation lemma is valid. When extending a saturated seed on [1,n] to [1,m], all added marks must lie in an interval of length L=m−n. For L≥1 their binom(t,2) distinct positive differences lie in {1,...,L−1}. Solving the resulting quadratic gives the stated floor bound. Gaps O(n_j^(2/3)) therefore preserve an O(N^(1/3)) upper bound if such a seed family exists. Bounded successive ratios alone do not guarantee those gaps. No seed family is established here.

The audit assesses these mathematical deductions and local finite computations. It does not independently establish the exhaustive literature-priority or preprint-optimality questions, both of which the draft disclaims.

## Final accepted version

Accepted mathematical research draft: `FIVE_APPROACHES.md`, SHA256 9966638acb7172020b0681535c5204f600338aaaeba0793885ea7dc6eedd1e89. Two wording fixes were requested and verified: remove an unsupported smallest-example adjective; say bounded ratios alone do not guarantee the interpolation gap condition. No unresolved mathematical correction remains in this version.

The author's `checks.py` was read and rerun successfully by this reviewer. SHA256 00b27fa0aa73dfcc610dae860a52fe24e4dfedf64722d081f2d845d7e335e837. It tests all subsets through N=16, with 65,470 one-point blocker checks and 1,864 maximal sets. Its `checks_results.json` SHA256 2306b86a0797292dc915eb633821d0a63757f6c1498d69466ac6585b932163ed was unchanged by the rerun, as was the N144 certificate. The separately written independent enumerator remains limited to N≤15, as explicitly stated above. Rerunning the author's N≤16 implementation is not represented as an independent second implementation for N=16.

Acceptance scope: elementary mathematical lemmas, limitations, finite regression results, and N144 existence certificate only. The asymptotic problem remains unresolved; no eight-mark threshold optimality or novelty has been certified.

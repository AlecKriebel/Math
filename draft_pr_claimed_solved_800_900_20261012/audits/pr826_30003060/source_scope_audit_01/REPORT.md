# Independent source and scope audit: PR #826 / 30003060

Frozen candidate head: `286cc67c0727b4decfd4f261a0591cd8823ebce9`. This audit concerns source compatibility and scope. It does not grant novelty, firstness, worldwide-open-status, human-review, or formal-verification clearance.

## Disposition

**Pass for a negative answer to the complete unrestricted equivalence as written in the frozen target and in the original OWR contribution. No fatal source/definition mismatch found.** The positive-characteristic free-algebra example attacks its forward implication, so it need not settle the reverse implication to refute that equivalence.

**Do not promote this as resolving the characteristic-zero converse or as proving the unique historical intended scope.** BLS's surrounding discussion supplies substantial characteristic-zero context. The candidate's explicit separation of its unrestricted negative answer from the characteristic-zero question is essential.

## Exact target and original source

I read the entire frozen `complete_target_record.json`, including its background, literature assessment, sources, original/clean statements, verification fields, and inherited `prior_research` (empty). The title emphasizes deriving Koszulness from vanishing, but the complete statement asks an iff without a field restriction. Its dated background describes the converse as open and says the forward implication is proved; the latter description omits the characteristic-zero hypothesis of BLS Theorem 6.4. That background is a secondary triage assertion, not a replacement mathematical statement.

I independently downloaded the official [EMS report](https://ems.press/journals/owr/articles/14218) and inspected Solotar's entire contribution, printed pp.479–481, one-based PDF pages31–33, including the adjacent-talk boundaries. Its conclusion includes this 18-word excerpt:

> a quadratic algebra A is Koszul if and only if its higher Koszul homology annihilates in positive degrees.

The talk itself contains no characteristic-zero restriction, finite-dimensional-algebra restriction, or alternative coefficient convention. The report introduction supplies none either. The finite-dimensional-vector-space discussion on p.481 concerns duality; it is not stated as a general condition on all algebras. The following talk's independent conventions do not apply retroactively.

Together with the BLS definition of quadratic algebra over a base field, the unrestricted literal claim is:

`For every field k and quadratic k-algebra A, A is Koszul iff HK^hi_q(A)=0 for every q>0.`

The word “every” formalizes the unrestricted standalone reading; it is an interpretation of the stated general claim, not evidence about the authors' unstated intentions.

## Definition compatibility

The original [BLS v1](https://arxiv.org/abs/1512.00183v1), dated 1 December2015, predates the February2016 workshop. The [published paper](https://doi.org/10.1017/S0017089517000167), Glasgow Math.J.60(2018),361–399, retains the relevant conventions. Exact PDFs match all three corresponding hashes in the candidate metadata.

| Issue | Primary location and finding | Consequence |
|---|---|---|
| Field / relations | v1 §2 p.4; final §2 p.364: base field and vector space, with any subspace `R⊂V⊗V` | `R=0` is permitted. |
| Finiteness / connectedness | No global finite-dimensional `A` assumption; quadratic grading has `A_0=k` | `k<x,y>` is connected and locally finite; its two-dimensional `V` also meets any relevant finite-generation restriction. |
| Ordinary Koszul complex | v1 §§2.1–2.2 pp.5–6; final pp.364–365 | For `R=0`, only `W_0=k,W_1=V` remain, and `b(a⊗v)=av−va`. |
| Cocycle | v1 §3.3 p.11; final p.369 | `e_A(v)=v`; no changed derivation is being substituted. |
| Higher differential | v1 §5.2 p.20; final p.377, Definition5.1 | `HK^hi(A)` uses coefficients `A` and the left cap action of `e_A`. It is defined in every characteristic. |
| Free algebra in the paper | v1 §7 p.29; final §7 p.385 | The authors explicitly treat `T(V)`, `dim V≥2`, as Koszul of global dimension1. |

The characteristic-not-two assumption for a general derivation in §5.1 is expressly removed for the fundamental cocycle in §5.2. It cannot exclude the candidate's characteristic-two example. Nor is the candidate using homology with trivial coefficients: BLS treats that separately.

The cap sign also agrees. In v1 §5.2 the representative is `(-1)^(q−1) x_q a⊗x_1…x_(q−1)`; for a cycle this equals `a x_1⊗x_2…x_q`. The published §5.2 uses the second expression. At `q=1`, the left cap initially gives `[va]`, and `[va]=[av]` in `HK_0=A/[A,A]`. Thus the candidate's `delta([a⊗v])=[av]` is compatible, including characteristic2. Sums must satisfy the cycle condition; this reasoning does not require each summand separately to be a cycle.

## Conjuncts and the independent logical check

BLS Conjecture6.5 (v1 p.24; final p.380) includes `HK^hi_0(A)≅k` as well as positive-degree vanishing. OWR states only the latter. This is a real formulation difference, but not a mismatch fatal to this example: a Koszul algebra with `HK^hi_1≠0` refutes the forward implication of either version. In characteristic zero, BLS Theorem6.4 proves the degree-zero condition for every quadratic algebra, so it is automatic there.

As an independent compatibility deduction, for `A=T(kx⊕ky)`, `HK_2=0`. In characteristic2, `z=x⊗y+y⊗x` is a nonzero tensor, `b(z)=0`, and `delta[z]=[xy+yx]=0`. No ordinary boundary enters degree1 and no higher boundary enters from `HK_2`. Hence `[z]≠0` in `HK^hi_1`. This uses precisely the original coefficients, cocycle and signs. For characteristic `p>0`, the orbit of `x^(p−1)y` has `p` distinct rotations; its orbit sum gives the same telescoping kernel calculation and cap image `p[w]=0`. The computation refutes the unrestricted forward implication without making any claim about its converse.

## Characteristic-zero context: evidence and limit

Both v1 p.24 and final p.380 explicitly impose characteristic zero in Theorem6.4. The subsequent prose asks for a proof possibly removing the characteristic hypothesis, and calls Conjecture6.5 the “converse of this theorem.” Their introduction and the discussion comparing higher Hochschild homology likewise invoke characteristic-zero results. This is positive evidence for reading the central intended research difficulty as the characteristic-zero converse; it must not be erased.

However, neither version makes characteristic zero a global convention, §5.2 deliberately works in every characteristic, Conjecture6.5's standalone hypotheses do not impose it, and OWR's whole contribution does not mention it. These facts justify the candidate's explicitly limited negative answer to the unrestricted text. They do **not** prove that the authors intended an unrestricted conjecture, and they do **not** establish that they intended only characteristic zero. The historically intended domain remains underdetermined by these documents. An unqualified “the BLS characteristic-zero conjecture is solved” would be a fatal overstatement; the inspected proof expressly avoids it.

## Evidence and remaining boundaries

`SOURCE_LEDGER.json` records hashes, byte sizes, versions, exact page mappings, and inspected/rendered pages. `QUERY_LOG.json` records online retrieval and searches. Ten key pages were rendered and visually checked; all raw PDFs, complete extractions, metadata and images remain in this audit's ignored `private_sources`.

No historical audit verdicts were consulted. Candidate `PROOF.md`, its source metadata and the frozen manifest were inputs to be checked, not independent authority. No Git/queue mutation or external communication occurred. The source scan found the paper's higher **cohomology** calculation for free algebras (Proposition7.4), which is not the candidate's higher-homology counterexample. This audit performed no deep priority census and draws no novelty or current global-status conclusion.

The strongest source-scope result is the fully qualified literal negative answer above. The exact remaining mathematical gap is the characteristic-zero reverse implication; the exact interpretive gap is unique historical intended scope. Neither gap invalidates the literal unrestricted counterexample, and neither is resolved by it.

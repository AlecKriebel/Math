# Fresh source-quantifier and model-obstruction review

PR623, problem 30001184 / OWR-3392-012. Scope: fixed general dilation, its
expectation GNS representation, forward generation, and logical coverage of
the negative answer. Review family: source quantifiers plus independent
finite-dimensional representation obstruction. No earlier PASS used.

## Verdict and highest verified claim

**The candidate is a valid counterexample to the universal two-stage claim
under the source's explicit forward-generation hypothesis.** Failure of its
first stage is decisive for that conjunction, rather than an easier unrelated
subclaim. The construction satisfies the source's general-dilation definition,
and its exact failure is independently supported by an infinitesimal argument
on the finite-dimensional GNS image. No mathematical defect was found in the
candidate proof reviewed here.

**The wider search for a useful sufficient definition of “not too big” is not
settled.** The packet honestly leaves stronger/incomparable conditions and
extension conditional on kernel invariance open. If `claimed_solved` means a
negative answer to forward generation and all logically weaker hypotheses,
the scope is defensible. If it means a positive sufficient minimality theorem
for the whole source research program, it is unsupported. These are different
interpretations of the bundled target; no queue or publication decision was
made by this shard.

## Input authentication

Supplied immutable PR head:
`947442c091ae617804c6a0d07b98ff2c50368798`.

The snapshot's `packet/PROOF.md` SHA-256 is
`f2a1b3b4233c2850d8dd79ba17b464d74343aa66e7d22d12104d17fc5470e8a3`.
Independent `git show` of the exact same repository path at the supplied head
produced that SHA-256. The bytes therefore match the immutable Git object.
The native snapshot is an ordinary directory in the shared main checkout;
its inherited working-copy HEAD is not the PR input identity.

Official PDFs were downloaded, hashed, and read independently. OWR printed
pp.497–499 and 542–543 were rendered and visually inspected, including the
expectation arrows. The later v2 paper's p.34 was rendered too. Full text and
PDFs remain under ignored `sources.private/`, renders under ignored `tmp/`.
`SOURCE_HASHES.json` gives reproducible source identities; exact candidate
identity is included in `VERDICT.json`.

## Source interpretation (primary evidence)

The [official OWR report](https://ems.press/content/serial-article-files/46209),
pp.497–498, permits C*- or von Neumann algebras and defines general dilation
by `p theta_t i=T_t`, with `i p` a conditional expectation. The p.498 diagram
has the expectation pointing upward from A to B. Its definitions distinguish
unital and weak dilations. Printed p.542's `p:B→A` is reversed: the adjacent
p.543 diagram, p.498 definition, and GNS discussion all require `p:A→B`.

The first module problem, pp.542–543, concerns a given general dilation. Its
two necessary stages are kernel descent and extension on the same GNS module.
It explicitly offers generation by the embedded algebra and its time shifts
as an example of being small enough, asks a proof or counterexample, and
requests a good formulation of smallness. Its next open problem concerns an
automorphic dilation's future part and is separate. No faithfulness, corner,
strongness, normality, or differentiability requirement is imposed on this
C*-algebra alternative.

The [Skeide–Sumesh v2](https://arxiv.org/pdf/1210.7491v2), §5 p.34, makes the
extension question precise by requiring an endomorphism on B^a(E) to send the
left action of a to the left action of theta_t(a). That is fixed-action
intertwining. Its surrounding speculative CPH discussion and earlier existence
results do not replace a given expectation's GNS representation.

The [Shalit–Skeide v3](https://arxiv.org/pdf/2003.05166v3), Appendix B(i)
pp.211–213, separates general compression, strong `p theta_t=T_t p`, weak
corner dilation, and full weak/module dilation. Its substantive dilation
results are expressly about weak dilations. Thus “Markov implies strong” in
that restricted category cannot be imported into this general unital example.

## Adversarial hypotheses tested

| Potential loophole | Independent finding |
|---|---|
| General dilation secretly requires `p theta_t=T_t p` on all A | The primary definition requires only `p theta_t i=T_t`; later primary terminology separates strongness. Exact witness proves the example is not strong, as admitted. |
| Source only covers weak/corner dilations | It expressly says general dilation. A nontrivial unital embedding cannot here be weak: its corner would be 1 and its expectation the identity. |
| Nonfaithful expectation is forbidden | No such restriction appears; the source's first stage expressly handles a nonfaithful GNS left action. |
| Only a null vector is shown, not a representation kernel | The fibre evaluation image is all M2 and the diagonal expectation is faithful on positive matrices. The entire GNS action is left matrix multiplication; its kernel is exactly zero evaluation. |
| A is an artificially enlarged unrelated algebra | A is defined as the C*-algebra of the observed forward translates, and those translates generate it exactly. The ambient continuous field is only a construction tool. |
| A Markov process law for all multitime moments is implicitly required | No such law is part of the inspected general-dilation definition. It could be a stronger proposed repair, which must be stated separately. |
| Continuity or Markov law holds only at sampled times | Compactness gives point-norm continuity for theta, and the exact complementary-idempotent calculation gives `P_s P_t=P_(s+t)` for every nonnegative real pair. |
| Finite-dimensional GNS or module fullness permits extension | Full E has B^a(E)=M2⊕M2, but kernel descent already fails. The independent derivation argument forces failure before extension. |
| A different GNS realization might avoid the failure | Cyclic GNS realizations are bilinearly unitarily equivalent. For this fixed p their representation kernels agree. |
| Some alternate dilation of the same T might work | That possibility is open and irrelevant to universal descent for the given quadruple. The candidate explicitly does not exclude alternate dilations. |
| Counterexample must separately defeat the extension stage | A counterexample to either conjunct defeats the asserted universal conjunction. No invariant-kernel extension counterexample is claimed. |
| Negative answer produces useful weaker sufficient minimality | It proves none exists if “weaker” means logically implied by forward generation. It gives no positive stronger or incomparable theorem. |
| Normal von Neumann version follows by bidual | Not established. Bidual continuity needs fresh proof. The C*-alternative suffices for the source's disjunctive setting. |

## Independent reconstruction and falsification attempts

`DEDUCTIONS.md` supplies the complete fibre-evaluation mechanism, reconstructs
the continuous group and generated restriction, identifies the full GNS module,
and proves the exact positive witness. It also gives an independent argument
which does not depend on the packet's chosen witness:

1. If the fixed GNS kernel were invariant for all t, its finite image M2 would
   inherit a norm-continuous unital endomorphism semigroup beta.
2. A continuous finite-dimensional semigroup is differentiable. An elementary
   integral identity proves this without an inner-implementation theorem.
3. Its infinitesimal map is a derivation. Since q is a projection,
   `Delta(delta(q))=0`.
4. The prescribed compression has `T'_0(q)=diag(-1/2,+1/2)`.

The contradiction independently forces a kernel obstruction. This explains
why the finite GNS image, rather than mere nonfaithfulness, defeats the proposed
descent. The explicit time is s=log(2); the coefficient in
`theta_s(a)(0)=d Q` is `d=3(sqrt(5)-1)/16>0`. This exact formula has substantial
positive margin. The code in `check_scope.py` checks the cocycle, compression,
semigroup identities, and witness on a finite sample, plus a matrix derivation
sanity check. `CHECK_RESULTS.json` records successful checks. Finite sampling
is supplementary evidence; the continuum identities are proved analytically.
The first overly strict `1e-13` cocycle tolerance failed at approximately
`3.53e-13`: differently associated floating input sums near the square-root
cusp amplified cancellation. A documented conservative `1e-11` bound passes.
The exact cocycle identity telescopes with no numerical limit; the positive
witness itself passed the original `1e-14` bound. This is a numerical-check
limitation, not evidence against the analytic construction.
A separate run with 50-digit decimal base-flow sums reduces the cocycle error
to approximately `3.33e-16`, confirming that input associativity was the cause.

## Quantifiers and the exact remaining gap

Let G be the stated forward-generation condition. The verified statement is
an admissible general dilation satisfying G but lacking fixed-GNS descent.
Thus the source's explicitly suggested `G ⇒ (descent and extension)` universal
claim is false. Forward generation is a precise meaningful condition, so its
failure is not just a pathological example outside every suggested notion.
Indeed A is the smallest theta-invariant C*-subalgebra of the ambient algebra
containing D: any such subalgebra must contain every theta_r(D), hence A.

For each H such that `G ⇒ H` on admissible dilations, the same counterexample
has H and fails the desired conclusion. This is the exact negative answer to
the curated “what weaker hypotheses suffice?” clause if “weaker” has its usual
logical meaning. It says nothing about hypotheses incomparable to G or stronger
conditions involving multitime moments or the expectation. Merely labelling
such a different condition “minimality” does not make it logically weaker.

The genuine unfilled portion of the broader source program is finding useful
additional compatibility/minimality assumptions under which the fixed descent
and extension succeed. The conditional extension problem after descent is
also unfilled. These gaps must be retained in any release or title whose scope
could otherwise imply a general sufficient minimality classification.

## Repairs and blocked routes

No repair is needed for the negative forward-generation theorem. A precise
description should emphasize a fixed unital general C*-dilation and failure of
descent. Avoid claiming all module dilations, weak dilations, faithful cases,
or the conditional extension conjecture are defeated.

Two genuine first-stage restrictions exclude the example: faithful p makes
the GNS representation faithful; strongness plus surjective theta gives
invariance by applying `p theta_t=T_t p` to every right multiple. Their proofs
are in `DEDUCTIONS.md`. Neither proves the extension stage, and they are not
weaker than G.

The exact kernel-invariance implication printed at the end of the packet is
a necessary compatibility test, correctly labelled as a reformulation. Using
it as the supposedly useful sufficient minimality theorem would transfer the
first-stage problem to itself. That route is blocked absent a new mechanism.
Likewise a product-system theorem constructing some dilation of T does not
solve the specified fixed-GNS intertwining requirement.

## Limits of this review

No comprehensive priority audit was performed. The inspected 2013-v2 and
2020/2023-v3 passages are used for definitions and quantifiers, not as evidence
of first discovery. No other individual or other-shard agent was contacted,
no external messages were sent, and no PR, queue, remote, native packet, or
publication was modified. All generated artifacts are in this review folder.

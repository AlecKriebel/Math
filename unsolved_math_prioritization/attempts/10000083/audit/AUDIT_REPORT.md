# Independent source and scope audit for linear time graph covering

**Target:** UnsolvedMath 10000083 / AMR-099-0083, rank 446.

**Audit date:** 2026-10-03 UTC.

**Verdict:** PASS for the frozen source-status certificate. Recommend
`already_solved`, `0/5`, for the intended asymptotic conjecture. HOLD any
unqualified claim that the literal every-n, no-prefactor statement is true.

This is an independent source and scope audit of the local author packet.
It is not a new proof, a priority claim, formal verification, or a complete
independent reconstruction of the imported proof. No remote writes or changes
to the frozen source packet were made.

## Frozen material checked

The original local audited manifest had SHA256
`0655e99bee36e4c6abe892ea3a9c4c8a9bb1a5caa1f127ddccd1abf76cb636a3`.
The public-only author file inventory is recorded in `../AUTHOR_MANIFEST.json`.

All eight public files and both primary PDFs match the lengths and SHA256
hashes recorded in the original local manifest. The PDFs are not distributed
here. The main certificate,
`../KNOWN_RESULT.md`, has SHA256
`02f65139b9952eaa5c9395aefcbe58ef8876bffbf398dbbd277a80a73599a48b`.

The audit read all eight public files, the extracted relevant primary text,
and rendered images of Benjamini p.9 and Dubroff-Kahn pp.1 and 4. It read the
core Dubroff-Kahn argument through section 5. The separate campaign-history
and duplicate gate was not independently repeated in this audit.

Running `../verify.py` reproduced `../verification.json`
byte-for-byte. Those exact-arithmetic controls check finite examples only;
they are not evidence for the difficult asymptotic theorem.

## Original conjecture and target identity

The relevant source is Itai Benjamini, *Random Planar Metrics*, section 4.1,
PDF p.9. The cover-time conjecture is an **unnumbered conjecture following
Conjecture 4.1**, not Conjecture 4.1 itself. This was checked in the primary
text and visually on the rendered page. The recovered primary copy is at
[Berkeley](https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/benjamini_rpm.pdf).

The original covering formulation has this quantifier order: each fixed
finite C admits c < 1, uniformly over graphs G of size n without double
edges, such that covering in Cn steps has probability smaller than c^n.
It does not separately specify the initial law or an explicit n-threshold.
The mathematically relevant positive-time version takes C > 0 and an
exponential base 0 < c < 1.

Conjecture 4.1 itself concerns the largest vacant component on uniformly
transient transitive graph sequences. Neither transitivity, planarity, nor
uniform transience is imposed on the subsequent covering conjecture. The
frozen packet correctly distinguishes these questions.

The catalogue input record states the simple-graph covering target, with
an at-most inequality and no large-n threshold. A strict upper bound in the
imported theorem is sufficient for the catalogue's non-strict inequality
once the large-n qualification is restored. The pinned input record, rather
than an independently retrieved live catalogue body, is the wording source
used for this audit.

[Weizmann's institutional publication record](https://weizmann.elsevierpure.com/en/publications/random-planar-metrics/)
confirms the corresponding ICM 2010 contribution, pp.2177-2187, DOI
[10.1142/9789814324359_0140](https://doi.org/10.1142/9789814324359_0140).
The imported triage report's Saint-Flour parenthetical is not the provenance
of the primary text checked here. No claim about a separate lecture text is
needed.

## Resolution and exact applicability

The directly checked resolution is Quentin Dubroff and Jeff Kahn,
*Linear cover time is exponentially unlikely*,
[arXiv:2109.01237v2](https://arxiv.org/abs/2109.01237v2), Theorem 1.1.
The theorem expressly allows any initial law. Its usage conventions specify
finite connected simple graphs and ordinary discrete-time random walk.
Page 4 expressly assumes sufficiently large n and permits inconsequential
integer-rounding conventions. Thus epsilon(C) > 0 and n0(C) are uniform over
the graph and initial law. Setting c(C) = exp(-epsilon(C)) gives the
certificate's asymptotic conclusion.

For the certificate, define tau_cov as the least integer t such that
{X_0, ..., X_t} is the whole vertex set. A real deadline Cn means
floor(Cn). This convention is appropriate for the displayed theorem.
Disconnected graphs have zero full-cover probability. Making isolated
vertices absorbing handles the otherwise undefined transition without
changing that conclusion. The one-vertex case is separately covered by the
finite-size warning below.

The packet's graph class is finite, undirected, unweighted, loopless and
simple. It does not assert a corresponding theorem for arbitrary directed
or weighted chains, and no such extension is needed.

The [earlier same-title paper, arXiv:1011.3118](https://arxiv.org/abs/1011.3118),
by Benjamini, Gurel-Gurevich and Morris, proves the bounded-maximum-degree
case, with degree dependence in the exponent. It must not be confused with
the general Dubroff-Kahn result.

[Rutgers's publication record](https://www.researchwithrutgers.org/en/publications/linear-cover-time-is-exponentially-unlikely/)
and the [publisher's issue listing](https://www.imstat.org/publications/aop/aop_53_1/aop_53_1.pdf)
corroborate *Annals of Probability* 53(1), January 2025, pp.1-22,
DOI [10.1214/24-AOP1699](https://doi.org/10.1214/24-AOP1699).
Theorem numbering and detailed proof checks here refer to arXiv v2; the
journal proof was not compared line-by-line. Bounded title/author/correction
searches found no correction contradicting the resolution. This is not an
exhaustive no-correction assertion.

## Depth and limits of proof inspection

The core proof through section 5 was inspected at the argument and dependency
level. The small-transition theorem feeds an induced-chain partition
criterion. High-degree and slow-range cases are handled separately, while
the remaining graphs admit the needed partition. This supports the claimed
applicability and uniformity, rather than merely matching an abstract title.
It does not establish that every estimate was independently reconstructed.

A nonblocking typo is present in v2 Theorem 2.3: its displayed inequality
for the expectation of a bounded supermartingale and its limit is reversed.
The correct direction is E(X_infinity) <= E(X_s). In Lemma 3.1 the proof uses
the correct direction, E(S_infinity) <= E(S_0). Accordingly, this displayed
typo is not a gap in the certificate's imported conclusion. It must not be
silently reproduced in any later proof exposition.

## Finite size distinction and valid repairs

For C = 1 and G = K_2, a walk from either vertex visits the other vertex at
time 1 with probability 1. It therefore covers by Cn = 2 with probability 1,
which exceeds c^2 for every 0 < c < 1. The literal every-n, no-prefactor
formulation is false. This remains a counterexample if the starting vertex
is not counted as a visit, since the first two steps visit both vertices.
Under the certificate's time-zero convention, the one-vertex graph also
has cover probability 1.

The omission of an explicit n-threshold occurs in Benjamini's informal
original wording as well as in the catalogue. It is not solely a catalogue
transcription issue. The known resolution is of the intended asymptotic
formulation, with the later paper's explicit large-n convention preserved.

The two valid formulations are:

1. For each C > 0, there are 0 < c(C) < 1 and n0(C) such that, for all
   n >= n0(C), all simple n-vertex graphs, and all initial laws,
   P(tau_cov <= floor(Cn)) < c(C)^n.
2. An all-n form permits a finite prefactor A(C):
   P(tau_cov <= floor(Cn)) <= A(C)c(C)^n.

From the first, A(C) = c(C)^(-n0(C)) suffices for the second: for smaller n
the right side is at least 1, and for larger n it exceeds the established
bound. The equivalence is existential in the constants; it does not promise
an optimal exponent or useful numerical estimates. This elementary repair
does not solve a new research problem.

## Controls and evidence boundaries

The verifier checks K_2 from both starts at one, two and three steps; the
one-vertex time-zero case; a disconnected graph with an isolated vertex;
and K_3 at two steps, whose cover probability is 1/2. It also checks the
concrete inequality (99/100)^2 < 1. Exact rational arithmetic avoids
floating-point ambiguity in these finite controls.

The control file is correctly labelled as supplementary. It neither verifies
the general theorem nor supplies its epsilon(C). The source packet credits
the difficult uniform bound wholly to Dubroff and Kahn.

## Required handling and recommended disposition

- No mandatory mathematical repair to the frozen certificate is identified.
- Preserve the finite-size qualifier wherever `already_solved` is used.
- Preserve the distinction between an imported theorem, a source/scope
  certificate and an independently reconstructed or formally verified proof.
- Optional editorial clarification: say explicitly that the original informal
  wording also lacks an n-threshold, rather than leaving readers to infer
  that this defect first arose in the catalogue.
- Tie checked theorem numbering to arXiv v2 and keep the journal-comparison
  limitation visible.
- This source-status work supports `0/5` new substantive proof-attempt turns.
  Campaign-history absence and prior-attempt eligibility remain the subject
  of the separate gate, not an independently repeated finding of this audit.

**Final disposition:** PASS for credited prior resolution of the intended
asymptotic target; HOLD for any unqualified assertion that its literal
every-n, no-prefactor version is true. No frozen source bytes were changed.

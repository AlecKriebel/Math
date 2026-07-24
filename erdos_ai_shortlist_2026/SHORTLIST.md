# Ten tractability-first Erdős problems for separate AI attacks

**Status date:** 2026-07-24
**Explicit exclusion:** Problem #84
**Scope:** Identification and screening only. No solution attempt was made.

## Bottom line

No honest literature screen can promise that an unsolved problem is
“solvable” by one more AI run. These are the ten highest-yield bets I found:
they have the best combination of a crisp finish line, a plausible finite
certificate or focused structural gap, moderate prerequisite load, and a
reasonable chance of producing a *full* result rather than another numerical
record.

The ranking is deliberately first-mover-sensitive. It is based on the
2026-07-23 snapshot of the
[`teorth/erdosproblems` database](https://github.com/teorth/erdosproblems/commit/1fddae4643fac0308db2e557876b78072e30f2e1),
all 609 entries then marked open, every entry marked decidable, falsifiable,
or verifiable, the live problem discussions, and a fresh literature and
public-agent-work audit.

Ranks 1–4 are the cleanest dispatches. Ranks 5–8 are serious but more
theoretical. Ranks 9–10 are the best remaining high-risk bets.

## Ranked shortlist

| Rank | Problem | Exact result that would settle it | Why it made the list | First-mover warning |
|---:|---|---|---|---|
| **1** | [#106 — square packing](https://www.erdosproblems.com/106) | Decide whether the maximum total side length of \(k^2+1\) non-overlapping squares in the unit square is \(k\), for every \(k\). A single exact configuration with total \(>k\) disproves it. | The first exposed case is only \(k=3\): ten squares. A strict counterexample has a short, independently checkable real-algebraic certificate. This is the best one-shot discovery target. | Two users are marked working, and a 2026 paper studies the conjecture, but no proof claim is posted. |
| **2** | [#7 — odd distinct covering system](https://www.erdosproblems.com/7) | Exhibit a distinct covering system whose moduli are all odd, or prove none exists. | A positive answer is one finite list of congruences with an exact coverage certificate. The search is discrete and has strong necessary conditions, which is unusually suitable for solver-guided mathematical discovery. | Twenty-one comments, two marked workers, and several failed AI/formal attempts. It is tractable in *format*, not known to be small. |
| **3** | [#197 — two permutable AP-avoiding classes](https://www.erdosproblems.com/197) | Partition \(\mathbb N\) into two sets and give a permutation of each containing no monotone 3-term arithmetic progression, or prove this impossible. | A recursive or finite-state construction plus an induction would be a complete, compact certificate. Three classes are known to suffice; the two-class question is crisp, formalised, and has no worker or comment on the live page. | Recent work studies nearby permutation-avoidance questions, but I found no direct claim on this problem. |
| **4** | [#156 — small maximal Sidon sets](https://www.erdosproblems.com/156) | Construct, for all large \(N\), a maximal Sidon subset of \(\{1,\ldots,N\}\) of size \(O(N^{1/3})\). | The lower exponent is forced by a simple count, while Ruzsa's construction is only \(O((N\log N)^{1/3})\). It is a single logarithmic-factor construction gap, with zero comments and no marked worker. | A public agent task has been seeded, but it currently shows no investigation. The gap has survived since 1998. |
| **5** | [#128 — sparse halves of triangle-free graphs](https://www.erdosproblems.com/128) | Decide whether every \(n\)-vertex graph in which every \(\lfloor n/2\rfloor\)-vertex induced subgraph has more than \(n^2/50\) edges must contain a triangle. One finite triangle-free counterexample settles it negatively. | Fixed-order counterexamples admit exact graph and exhaustive half-set certificates. The conjectured constant is sharp, so computation can expose the missing extremal structure even if the answer is positive. | Two users are marked working and formalising. This is a live race and needs an exact certificate, not a numerical heuristic. |
| **6** | [#864 — one exceptional Sidon sum](https://www.erdosproblems.com/864) | Prove that a set \(A\subseteq\{1,\ldots,N\}\) with at most one repeatedly represented pair-sum has \(\lvert A\rvert\le(1+o(1))(2/\sqrt3)\sqrt N\), or beat that constant by construction. | The lower construction matches \(2/\sqrt3\); the elementary public upper bound is \(\sqrt2\). One exceptional sum imposes visible structure, and exact extremal data provide useful conjecture material. | Fresh exact data reached \(N=100\) in July 2026, and a public agent task exists, though no investigator or full-proof claim is visible. |
| **7** | [#1016 — minimum-edge pancyclic graphs](https://www.erdosproblems.com/1016) | If an \(n\)-vertex pancyclic graph has \(n+h(n)\) edges, prove \(h(n)\ge\log_2 n+\log_*n-O(1)\). | The known bounds differ only by the \(\log_* n\) term. The finish line is precise, and the problem reduces conceptually to how a Hamilton cycle plus few chords can realise all cycle lengths. | Quiet—one bibliographic comment and no marked worker—but the iterated logarithm signals a delicate multiscale proof. |
| **8** | [#624 — images of subset maps](https://www.erdosproblems.com/624) | With \(H(n)\) defined as the *minimum* threshold for a map \(f:\mathcal P(X)\to X\) whose restriction to every \(Y\) of size at least \(H(n)\) hits all of \(X\), prove \(H(n)-\log_2n\to\infty\). | The requested conclusion is only an unbounded additive gap, and Alon's constant-fraction image-deficiency result suggests a focused amplification or entropy theorem. The statement is formalised and has essentially no public work. | The live prose omits the minimisation, so the normalized definition must be used. Alon's strongest ingredient is recorded as a personal communication. |
| **9** | [#273 — covering by moduli \(p-1\)](https://www.erdosproblems.com/273) | Exhibit a distinct covering system all of whose moduli are \(p-1\) for primes \(p\ge5\), or prove none exists. | Like #7, a positive answer is a finite exact-cover certificate. The arithmetic restrictions are elementary enough for a combined SAT/ILP and theorem-discovery agent. | A July 2026 AI-assisted project proved that primes \(p\le877\) cannot suffice and reported failed searches. This is the most competitive item retained. |
| **10** | [#19 — Erdős–Faber–Lovász](https://www.erdosproblems.com/19) | Prove that an edge-disjoint union of \(n\) copies of \(K_n\) has chromatic number \(n\), for every \(n\). | The conjecture is known for \(n<10\) and for all sufficiently large \(n\), so only finitely many orders remain in principle. Each fixed order is a finite incidence-type and graph-colouring certification problem; the first uncovered order is \(n=10\). | The large-\(n\) theorem has no practical cutoff on the page. Checking \(n=10\) alone would be an advance, not a full solution; a conclusive AI must make the cutoff effective or find a uniform proof. |

## Dispatch interpretation

The ten should not all receive the same kind of prompt:

- **Exact witness/counterexample agents:** #106, #7, #128, and #273.
- **Explicit construction agents:** #197 and #156.
- **Structural proof agents:** #864, #1016, #624, and #19.

For every computational target, require exact data and an independently
checkable certificate. A floating-point configuration, a long search with no
witness, or verification of a few more cases is not a solution.

## First alternate

[#944 — critical edge sets in vertex-critical graphs](https://www.erdosproblems.com/944)
is the strongest alternate. Results from 2025 reduce the full problem to
\(k=4\), but a full solution must handle **every** \(r\), not just produce one
graph for \(r=1\). Moreover, a June 2026
[paper](https://arxiv.org/abs/2606.18462) is already attacking that first
subcase with computation and Lean-checked lemmas. Use #944 instead of #19
only for an AI particularly strong at extending recent graph constructions
and if the race risk is acceptable.

## Problems deliberately not selected

- **#84:** excluded by instruction.
- **#1199:** the database was stale; a
  [full affirmative preprint](https://arxiv.org/abs/2607.17333) was submitted
  on 2026-07-19.
- **#123:** solved and Lean-verified in July 2026 after some public task
  listings had already cached it as open.
- **#475:** intrinsically attractive, but a public GPT-5.5 proof-candidate and
  certificate package appeared in May 2026.
- **#23:** a June 2026 computer-assisted
  [preprint](https://arxiv.org/abs/2606.28041) already proves the conjecture
  for the first forty multiples of five and actively develops the likely
  route.
- **#64, #488, #993:** finite counterexample formats, but already crowded by
  active human/AI searches.
- **#19's fellow “decidable” problems:** most have enormous or unspecified
  finite cutoffs; #506, #547, and #556 also have defects in their literal
  displayed statements.

## Confidence calibration

This is a ranking of *relative* tractability, not a forecast that ten AIs will
produce ten proofs. Recent large-model screening illustrates the base-rate
problem: in the Aletheia/Gemini study, many plausible outputs collapsed under
technical and literature review before only a small number of meaningful
results remained
([arXiv:2601.22401](https://arxiv.org/abs/2601.22401)).
The practical standard should therefore be: exact statement, current
literature audit, proof or certificate, independent adversarial review, and
only then a public claim.

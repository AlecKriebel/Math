# Skeptical screen of six ordinary-open Erdős problems

**As of:** 2026-07-24 (America/Los_Angeles)
**Database snapshot checked:** `teorth/erdosproblems` commit
[`1fddae4643fac0308db2e557876b78072e30f2e1`](https://github.com/teorth/erdosproblems/commit/1fddae4643fac0308db2e557876b78072e30f2e1),
dated 2026-07-23. Live problem and forum pages, primary papers, arXiv, and OEIS
were checked read-only on 2026-07-24. No one was contacted.

## Bottom line

Of the requested six, **#864 is the strongest top-ten candidate**: the target
is crisp, the constant gap is modest, one exceptional sum should impose useful
structure, and exact extremal data now reach `N=100`. **#624 is also worth a
slot**, after repairing the live page's missing minimization in the definition
of `H(n)`. **#1016 is a plausible theory-first reserve** and ranks close to,
but slightly above, #19 for a research AI; put #19 above it if the separate
agent is optimized for finite certification rather than proof discovery.

Do **not** use #791 as a “conclusively solve this conjecture” prompt: its
specific asymptotic conjecture was disproved long ago, while the surviving
instruction “Estimate `g(n)`” has no crisp completion criterion. #849 is
perfectly well posed but is a famous, deep Diophantine collision problem, not
a tractability pick. Most importantly, **#1199 was solved in a preprint posted
2026-07-19**, five days before this screen; the database snapshot is stale on
that point.

Ranking the six requested problems against the two clean baselines #19 and
#551:

| Rank | Problem | Top-ten suitability | Decisive reason |
|---:|---:|---|---|
| 1 | [#864](https://www.erdosproblems.com/864) | **Yes—best of these** | Crisp matching upper bound, small constant-factor gap, strong one-exception structure, and useful exact data; current activity is computational rather than a proof race. |
| 2 | [#624](https://www.erdosproblems.com/624) | **Yes, with normalized statement** | Weak divergence target and an existing constant-fraction deficiency theorem suggest an amplification/entropy route; formally encoded and nearly no public activity. |
| 3 | [#1016](https://www.erdosproblems.com/1016) | **Reserve / theory-first** | A precise `log_* n` lower-order gap and a sparse Hamiltonian-cycle-plus-chords model make it conceptually AI-friendly, though technically delicate. |
| 4 | [#19](https://www.erdosproblems.com/19) | **Clean fallback** | Finite in principle, with first uncovered order `n=10`, but no explicit large-`n` cutoff makes small-case certification non-conclusive. |
| 5 | [#551](https://www.erdosproblems.com/551) | **Lower fallback** | Crisp and uncrowded, but even small surviving Ramsey instances are enormous and the asymptotic constant is not explicit. |
| 6 | [#791](https://www.erdosproblems.com/791) | **Exclude from a conclusive list** | The yes/no subquestion is already false; “Estimate” leaves a decades-old constant gap without specifying what counts as a solution. |
| 7 | [#849](https://www.erdosproblems.com/849) | **Exclude on tractability** | Crisp, but it is Singmaster's problem in disguise; the hard small-`k` edge regime survives major modern work. |
| 8 | [#1199](https://www.erdosproblems.com/1199) | **Remove—already solved** | A 2026-07-19 preprint states and proves exactly the requested positive answer. |

## 1. #864 — almost-Sidon sets with one exceptional sum

**Exact live statement.** “Let \(A\subseteq\{1,\ldots,N\}\) be a set such
that there exists at most one \(n\) with more than one solution to \(n=a+b\)
(with \(a\leq b\in A\)). Estimate the maximal size of \(A\). In particular,
is
\[
|A|\leq (1+o(1))\frac{2}{\sqrt3}N^{1/2}?
\]”

**Current state.** The page gives the matching Erdős–Freud lower construction:
start with a Sidon set \(B\subseteq[1,N/3]\) and take
\(B\cup\{N-b:b\in B\}\). Thus proving the displayed upper bound would
determine the asymptotic maximum, not merely improve a bound. A forum argument
posted by Desmond Weisenberg on 2025-08-11 gives the clean weaker estimate
\[
|A|\leq(\sqrt2+o(1))\sqrt N
\]
by splitting around the exceptional sum into two Sidon-type pieces.
[Problem](https://www.erdosproblems.com/864) ·
[forum](https://www.erdosproblems.com/forum/thread/864?order=newest)

**Live activity.** The site shows 2 comments, 0 proof claims, and no
working/difficult/tractable flags. Terence Tao linked exact-search work in
October 2025. [GitHub issue 143](https://github.com/teorth/erdosproblems/issues/143)
records AI-assisted bitset enumeration through `N=69` and observes—but does
not prove—that extremizers often resemble \(S\cup(k-S)\).
[OEIS A389182](https://oeis.org/A389182) now gives exact terms through
`N=100`, extended by Alper Ferudun on 2026-07-12 and updated on 2026-07-22.
That is real and very recent computational activity, so “uncrowded” should not
be overstated, but there is no public full-proof claim or marked researcher.

**Crispness and burden.** A complete result is unambiguous: prove the proposed
upper bound, which matches the construction. Prerequisites are moderate:
classical Sidon bounds, additive energy/difference counting, and structural
stability. The exact data and the single permitted collision give a separate
AI concrete material for conjecturing a stability lemma. The main risk is
that more exhaustive search will not control cross-sums asymptotically.
Nevertheless, the gap between constants \(2/\sqrt3\approx1.1547\) and
\(\sqrt2\approx1.4142\), plus the visible reflection structure, makes this the
best research bet in this screen.

## 2. #624 — universal images of subset maps

**Exact live statement.** “Let \(X\) be a finite set of size \(n\) and
\(H(n)\) be such that there is a function
\(f:\{A:A\subseteq X\}\to X\) so that for every \(Y\subseteq X\) with
\(|Y|\geq H(n)\) we have \(\{f(A):A\subseteq Y\}=X\). Prove
\(H(n)-\log_2n\to\infty\).”

**Statement normalization.** Literally, “be such that” does not uniquely
define `H(n)`: if one threshold works, larger ones do too. The intended
quantity is the **minimum** threshold over all admissible maps. The
[DeepMind formalization](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/624.lean)
uses this minimum/infimum formulation. Any delegated prompt should copy that
definition rather than the ambiguous live prose.

**Current state.** Erdős and Hajnal proved
\[
\log_2n\leq H(n)<\log_2n+(3+o(1))\log_2\log_2n.
\]
The page says Erdős noted that even \(H(2^k)\geq k+1\) was open; Alon then
gave a pigeonhole proof. More significantly, the remarks say Alon proved by
personal communication a stronger Erdős–Gyárfás conjecture: for a fixed
`k`-set \(Y\), a constant fraction of the possible images can be forced
missing, with a complementary construction attaining more than a quarter of
the \(2^k\) possibilities. [Problem](https://www.erdosproblems.com/624) ·
[forum](https://www.erdosproblems.com/forum/thread/624?order=newest)

**Activity.** The page was last edited 2025-10-27, shows 1 correction/deleted
comment, 0 proof claims, and no reaction flags. Its own warning says the
literature may be incomplete. Searches through the current public literature
found no direct 2026 attack or claimed solution; the strongest ingredient
quoted by the page remains a personal communication.

**Crispness and burden.** After normalization, the desired divergence is a
weak and exact finish line. The existing constant-fraction loss for
power-of-two-scale restrictions suggests that an AI could search for an
amplification, tensoring, averaging, or entropy argument. The formal encoding
is useful for checking definitions, though it does not make an asymptotic
proof automatic. Prerequisites are moderate to high: extremal set systems,
probabilistic method, and entropy. Brute force is not a route—the choice space
contains \(n^{2^n}\) maps—and the unpublished/personal-communication component
may be hard to reconstruct. Even so, this is low-crowd, has a modest target,
and deserves a top-ten slot.

## 3. #1016 — minimum excess edges in a pancyclic graph

**Exact live statement.** “Let \(h(n)\) be minimal such that there is a graph
on \(n\) vertices with \(n+h(n)\) edges which contains a cycle on \(k\)
vertices for every \(3\leq k\leq n\). Estimate \(h(n)\). In particular, is
\[
h(n)\geq\log_2n+\log_*n-O(1)?
\]”

**Current state.** The page records the known sandwich
\[
\log_2(n-1)-1\leq h(n)\leq\log_2n+\log_*n+O(1).
\]
Bondy announced both bounds without details; Griffin supplied the published
lower bound in 2013, and the first cited published proof of the upper bound is
in a 2016 book by Gyárfás, Korándi, and Wagner. An AI-assisted literature audit
posted by Tao on 2025-10-18 corrected the attribution and found no resolution.
[Problem](https://www.erdosproblems.com/1016) ·
[forum](https://www.erdosproblems.com/forum/thread/1016?order=newest)

Alon and Krivelevich's 2025 paper on pancyclic subgraphs of random graphs
independently restates the deterministic lower bound and the known
\(n+(1+o(1))\log_2n\) edge scale; it does not close this second-order gap.
[Published paper](https://doi.org/10.1137/23M1598969) ·
[author PDF](https://www.math.tau.ac.il/~krivelev/pancyclic-rg.pdf)

**Activity and fit.** The page was last edited 2025-12-27 and shows 1 comment,
0 proof claims, and no reaction flags. No direct 2026 progress was found.
A conclusive proof of the displayed lower bound would match the stated upper
bound to \(O(1)\), giving a very clear theorem. Conceptually, a sparse
pancyclic graph can be viewed as a Hamilton cycle plus only \(O(\log n)\)
extra edges, turning possible cycle lengths into a constrained combinatorial
representation system. That representation is promising for automated lemma
search and small-instance SAT experiments.

The negative is the same feature that makes the problem interesting:
\(\log_* n\) effects usually come from delicate recursion and are invisible
to modest computation. Prerequisites are moderate to high—extremal graph
theory, pancyclicity, chord systems, and recursive counting. This is a strong
theory-first reserve, but not a certificate-first task.

## 4. #791 — restricted additive 2-bases

**Exact live statement.** “Let \(g(n)\) be minimal such that there exists
\(A\subseteq\{0,\ldots,n\}\) of size \(g(n)\) with
\(\{0,\ldots,n\}\subseteq A+A\). Estimate \(g(n)\). In particular is it true
that \(g(n)\sim2n^{1/2}\)?”

**Current state.** The particular conjecture is already false: Mrose
constructed sets with \(g(n)^2\leq(7/2+o(1))n\). The page gives the current
constant gap
\[
(2.181\ldots+o(1))n\leq g(n)^2
\leq(3.458\ldots+o(1))n,
\]
with the lower bound due to Yu (2015) and the upper bound due to Kohonen
(2017). [Problem](https://www.erdosproblems.com/791) ·
[forum](https://www.erdosproblems.com/forum/thread/791?order=newest) ·
[OEIS A066063](https://oeis.org/A066063)

**2026 literature/activity.** The page shows 2 comments, 0 proof claims, and
no reaction flags; its comments are bibliographic/corrective. Melvyn
Nathanson's May 2026 preprint,
[“Problems in additive number theory, VII: The structure of additive
\(h\)-bases for \(n\)”](https://arxiv.org/abs/2605.26425), discusses this
area, calls attention to forgotten literature, and explicitly proposes
problems partly for AI, but does not settle this asymptotic constant.
Weltge and Zyhalko's contemporaneous
[work on finite additive 2-bases](https://arxiv.org/abs/2605.19449) is further
evidence that the area is active, not a resolution of #791.

**Why not shortlist it.** “Estimate” does not say whether an improved bound,
existence of an asymptotic constant, or an exact constant constitutes a
solution. The only crisp yes/no clause has already been answered negatively.
An AI could productively optimize constructions, run SAT/integer programs,
or mine older papers, but a “conclusive solution” prompt would be ill-defined
without replacing Erdős's page with a new conjecture. The prerequisite burden
is high and specialized (restricted additive bases/postage-stamp methods),
and exact computation only reaches small `n`.

## 5. #849 — prescribed multiplicity of binomial coefficients

**Exact live statement.** “Is it true that, for every integer \(t\geq1\),
there is some integer \(a\) such that
\[
\binom nk=a\qquad(1\leq k\leq n/2)
\]
has exactly \(t\) solutions?”

**Current state.** This is the multiplicity form of Singmaster's problem. The
page gives `a=120` for three solutions and `a=3003` for four; no example with
five or more is known. Erdős and Singmaster believed the answer is negative,
indeed that the number of representations is absolutely bounded.
[Problem](https://www.erdosproblems.com/849) ·
[forum](https://www.erdosproblems.com/forum/thread/849?order=newest)

The major modern result of Matomäki, Radziwiłł, Shao, Tao, and Teräväinen
proves at most two representations in the interior range
\(k\geq\exp((\log n)^{2/3+\varepsilon})\) for sufficiently large values.
It expressly leaves the difficult small-`k` edge regime, and its effective
bounds are too large for numerical closure.
[arXiv](https://arxiv.org/abs/2106.03335) ·
[published article](https://academic.oup.com/qjmath/article/73/3/1137/6563541)

**Activity and fit.** The site shows 0 comments, 0 proof claims, and no
reaction flags, and the statement has been formally encoded. That quiet page
is misleading: the underlying question is famous and has attracted
high-powered analytic and Diophantine work. The finish line is crisp—a
construction for every `t`, or a proof that some `t` is impossible—but either
direction appears much harder than its elementary wording. Prerequisites
include Diophantine equations, \(p\)-adic/analytic number theory, and often
algebraic curves. An AI can search for new collisions or organize known
families, but finite search cannot rule out representations. This is a poor
“most tractable” selection.

## 6. #1199 — Owings's monochromatic sumset question

**Exact live statement.** “Is it true that in any 2-colouring of
\(\mathbb N\) there exists an infinite set \(A\) such that all elements of
\(A+A\) are the same colour?”

**Live-status correction.** The 2026-07-23 database snapshot still labels
this open, but the preprint
[“A positive answer to the Owings's sumsets question”](https://arxiv.org/abs/2607.17333)
by Wen Huang, Zhengxing Lian, Song Shao, Rongzhong Xiao, Leiye Xu, and Shuhao
Zhang was submitted on **2026-07-19**. Its abstract states exactly that every
2-colouring of the positive integers admits an infinite \(B\) for which
\(B+B\) is monochromatic. This is a direct full positive answer, using
topological dynamics and ultrafilters, rather than a merely adjacent result.

The problem page still shows 3 comments, 0 proof claims, and two likes, which
illustrates why current literature checks are essential.
[Problem](https://www.erdosproblems.com/1199) ·
[forum](https://www.erdosproblems.com/forum/thread/1199?order=newest)
Regardless of journal status, another team has publicly posted the claimed
solution, so this cannot satisfy the user's goal of being first. Remove it.

## Comparison with #19 and #551

[#19](https://www.erdosproblems.com/19) remains the better **finite,
certificate-oriented** fallback. The Erdős–Faber–Lovász conjecture is known
for `n<10` and all sufficiently large `n`; `n=10` is the first uncovered
order, and each fixed incidence structure becomes an `n`-colorability CSP on
at most `n²` vertices. Its fatal qualification is that the large-`n` theorem
has no practical explicit cutoff on the page, so verifying `n=10` is not a
full resolution.

[#551](https://www.erdosproblems.com/551) is also crisp and finite in
principle, but less tractable. The known cycle-versus-clique Ramsey results
bound the surviving `(n,k)` pairs only through an unspecified asymptotic
constant, and even the illustrative diagonal case `(7,7)` concerns
two-colourings of the 666 edges of `K_37`. It requires a major structural
reduction before an M1-scale certificate is credible.

On balance, the recommended order is **#864, #624, #1016, #19, #551**. If
the delegated AI is a SAT/formal-certificate specialist rather than a
theorem-discovery system, swap **#19** and **#1016**. For the requested
top-ten list, include **#864 and #624**, use **#1016** only if a theory-first
reserve is needed, and exclude **#791, #849, and #1199**.

## Addendum: final screen of #944, #123, and #778

**Checked live on 2026-07-24.** For the user's requirement of a *full*,
first-to-solve result, the revised order around the cutoff is
**#864, #624, #1016, #19, #944, #551, #778**, with **#123 excluded as
already solved**. #944 can replace #551 if another slot is needed, but it
should not displace #864 or #624. Its finite-search hook is materially less
than a full solution.

### #944 — critical edge sets in 4-vertex-critical graphs

The live problem asks whether, for every \(k\geq4\) and \(r\geq1\), there is
a \(k\)-vertex-critical graph in which every critical edge set has more than
\(r\) edges. [Problem](https://www.erdosproblems.com/944) ·
[forum](https://www.erdosproblems.com/forum/thread/944?order=newest)

This has narrowed sharply: Martinsson–Steiner and then
[Skottova–Steiner](https://arxiv.org/abs/2508.08703) proved the result for
every \(k\geq5\) and \(r\geq1\), with a quantitative
\(f_k(n)=\Omega_k(n^{1/3})\) bound. Only \(k=4\) remains. That gives a clean
full target—construct such graphs for **every** \(r\), or prove failure for
some \(r\)—and a substantial 2025 scaffold to adapt.

The trap is that even \(r=1\), Dirac's 1970 conjecture, is still open. Finding
one 4-vertex-critical graph with no critical edge would be a major,
machine-checkable advance, but would **not** by itself solve #944 for all
\(r\). The most recent public work is Alper Ferudun's June 2026
[computational/structural paper](https://arxiv.org/abs/2606.18462): it rules
out a 6-regular witness through 15 vertices, proves exact 6-edge-cut
restrictions, and supplies Lean-checked cores, while explicitly stopping
short of even the \(r=1\) case. Thus the topic has an active first mover
outside the site despite the page showing only 2 comments, 0 proof claims,
and nobody marked working.

[SciNet's #944 entry](https://api.scinet.pub/p/a4945b3d-0873-4313-91fb-a80072c23732)
was seeded on 2026-07-14, rates tractability `3/5`, and currently shows 0
investigations/agents. Its acceptance criteria correctly distinguish a
finite \(r=1\) witness as an **advance** from the all-\(r\) result needed for
full resolution. Conclusion: #944 has better current leverage than #551 and
is worth a last-slot theory/construction attempt, but rank it below #19 for a
strict full-problem and first-mover screen.

### #123 — already solved twice by AI

The corrected live statement asks whether
\(\{a^kb^\ell c^m:k,\ell,m\geq0\}\) is \(d\)-complete for all pairwise
coprime integers \(a,b,c>1\). The live page is now **PROVED (LEAN)**.
[Problem](https://www.erdosproblems.com/123) ·
[proof claims](https://www.erdosproblems.com/forum/thread/123/proof-claims)

Colin Snyder submitted a full GPT-5.6/custom-harness proof on 2026-07-15; the
site accepted it as correct, and the supplied Lean 4 development uses no
`sorry`. Principia Math submitted a different GPT-5.6/Opus-4.8 proof and
formalization on 2026-07-20, also claiming the stronger clustered-summand
conjecture. This is not merely recent competition: the original target has
already been won.

[SciNet's #123 entry](https://api.scinet.pub/p/ce672d54-cba4-4f4c-8a7c-a0d21dd608fc)
still says open with 0 investigations because it was seeded on 2026-07-14
from a page fetched on 2026-07-13, immediately before the accepted proof.
Its `4/5` tractability rating is therefore stale evidence, not a candidate
recommendation. Exclude #123 categorically.

### #778 — three edge-colouring games bundled together

The page poses three games: the unbiased largest-clique game, the biased
two-for-one clique game, and a maximum-degree game.
[Problem](https://www.erdosproblems.com/778) ·
[forum](https://www.erdosproblems.com/forum/thread/778?order=newest)
A clean theorem can be stated for each game, but “solve #778” is ambiguous:
settling the flagship clique game still leaves two displayed questions. A
true page-level resolution would need the winner and a uniform strategy for
all stated \(n\) in all three variants.

Recent progress is substantial and human-led. Malekshahian and Spiro proved
that Bob wins the first game for a set of \(n\) of density at least \(3/4\),
and the degree game for density at least \(2/3\); their paper was revised in
2025 and [peer-reviewed in the *Journal of Graph
Theory*](https://ora.ox.ac.uk/objects/uuid%3A9860b403-00c0-47a1-9a2e-609494faec80)
in May 2026. Cambie and Provoost's
[2025 preprint](https://arxiv.org/abs/2505.03497) gives further observations
and particular behavior. The site has only 1 comment and 0 proof claims, but
those two current research teams make the apparent low activity misleading.

Each fixed \(n\) is a finite perfect-information game, yet the game tree has
\(\binom n2\) plies and the conjecture is uniform in \(n\); small-\(n\)
minimax certificates cannot finish it. The existing density implications
(an Alice win at \(n\) forces Bob wins at the next three values in the first
game) do not reduce the remaining set to finitely many cases.
[SciNet's #778 entry](https://api.scinet.pub/p/2325b8ed-d542-4e2b-b2b7-b1b58bbffd2c)
was seeded on 2026-07-14, rates it `3/5`, and has 0 investigations/agents, but
its proposed computation delivers only advances. On full-problem
tractability and first-mover risk, #778 ranks below #551 and should not enter
the ten.

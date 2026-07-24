# Screen of the nine `decidable` Erdős problems

**As of:** 2026-07-24 (America/Los_Angeles)
**Database snapshot checked:** `teorth/erdosproblems` commit
[`1fddae4643fac0308db2e557876b78072e30f2e1`](https://github.com/teorth/erdosproblems/commit/1fddae4643fac0308db2e557876b78072e30f2e1),
dated 2026-07-23. All nine entries below are marked `decidable` there. I also
fetched the live problem and forum pages read-only on 2026-07-24.

## Bottom line

“Decidable” here means *proved for all sufficiently large parameters, leaving
finitely many instances*. It does **not** mean that the surviving finite check
is remotely feasible. Of these nine, only **#475** is a clean, relatively
uncrowded first-choice target. **#580** has the best demonstrated AI/SAT
foothold, but another GPT-assisted team has already claimed the cases through
`n=19`. **#19** is the best clean fallback. Problems **#506, #547, and #556
should not be presented as unsolved as literally written**: the live forum/site
already records statement defects.

Ranking for the stated goal—an AI-first *conclusive* result on one M1/16 GB
machine, with “being first” included in the score:

| Rank | Problem | Recommendation | Main reason |
|---:|---:|---|---|
| 1 | [#475](https://www.erdosproblems.com/475) | **Best of this group** | Clean finite-field CSP; first range not covered by the stated theorems begins at the tiny case `p=17, t=13`; no one marked working and no proof claim. |
| 2 | [#580](https://www.erdosproblems.com/580) | **Promising but already raced** | Exact SAT reductions exist and a GPT-5.6-assisted partial proof claims all `n≤19`; however no usable large-`n` cutoff is given. |
| 3 | [#19](https://www.erdosproblems.com/19) | **Clean fallback** | First uncovered order is `n=10`, and each fixed instance is a finite coloring CSP on at most `n²` vertices; the unknown asymptotic cutoff is the real barrier. |
| 4 | [#551](https://www.erdosproblems.com/551) | **Theory-first only** | Clean and uncrowded, but its finite instances are Ramsey searches of hundreds of Boolean edge variables and the large-`n` constant is not explicit on the page. |
| 5 | [#848](https://www.erdosproblems.com/848) | **Do not choose if “first” matters** | Extremely active (48 comments), already an AI showcase, and the best forum threshold still leaves a gap up to roughly `2.64×10^17`. |
| 6 | [#742](https://www.erdosproblems.com/742) | **Not M1-realistic** | The published “large `n`” cutoff is reported as a tower of twos of height about `10^14`; brute force cannot bridge it. |
| 7 | [#556](https://www.erdosproblems.com/556) | **Exclude as written** | Literal statement is false at `n=3`; intended repair is `n≥4`, after which the surviving three-color Ramsey search is still enormous. |
| 8 | [#547](https://www.erdosproblems.com/547) | **Exclude as written** | Literal statement is false for the one-vertex tree; one user is also marked “currently working.” |
| 9 | [#506](https://www.erdosproblems.com/506) | **Exclude until reformulated** | The page itself says the nondegeneracy hypothesis is unclear; the literal version allows all points collinear. There is no unique target theorem to claim. |

## Evidence by problem

### 1. #475 — valid orderings in \(\mathbb F_p\)

**Exact live statement.** “Let \(p\) be a prime. Given any finite set
\(A\subseteq\mathbb F_p\backslash\{0\}\), is there always a rearrangement
\(A=\{a_1,\ldots,a_t\}\) such that all partial sums
\(\sum_{1\le k\le m}a_k\) are distinct, for all \(1\le m\le t\)?”

**Current remarks.** Graham proved `t=p−1`. The page records proofs for
`t≤12` and `p−3≤t≤p−1`. It says all sufficiently large primes are now covered
only by combining four different regimes: small sets (Bedert–Kravitz, improved
by Costa–Della Fiore), medium sets (Pham–Sauermann), large sets
(Bedert–Bucić–Kravitz–Montgomery–Müyesser), and very large sets
(Müyesser–Pokrovskiy). The page expressly warns that its literature coverage
may be incomplete. [Problem](https://www.erdosproblems.com/475) ·
[forum](https://www.erdosproblems.com/forum/thread/475?order=newest)

**Why finite.** Only finitely many primes lie below the implicit large-prime
threshold; for fixed `p` there are only `2^(p−1)` candidate sets and finitely
many orderings.

**Scale/barrier.** The results quoted on the page already cover every set for
`p≤13`. The first parameter not covered by those statements alone is
`p=17, t=13`: only \(\binom{16}{13}=560\) sets, although a naive `13!`
ordering loop per set is wasteful. This is excellent for DP/SAT discovery and
certificate generation on an M1. The conclusive obstacle is not the first few
primes; it is extracting explicit, overlapping constants from four
asymptotic arguments, or finding one direct argument that removes the
threshold.

**Crowd/fit.** 3 comments, 0 claimed proofs; Alfaiz likes it; nobody is marked
working, difficult, or tractable. **Best candidate here**, provided the
separate AI is told to seek a uniform proof or explicit threshold—not merely
to verify `p=17`.

### 2. #580 — the literal vertex version of the \(n/2\)-\(n/2\)-\(n/2\) conjecture

**Exact live statement.** “Let \(G\) be a graph on \(n\) vertices such that at
least \(n/2\) vertices have degree at least \(n/2\). Must \(G\) contain every
tree on at most \(n/2\) vertices?”

**Current remarks.** The page attributes the conjecture to Erdős, Füredi,
Loebl, and Sós, gives the Ajtai–Komlós–Szemerédi approximate form, and says
Zhao proved it for all sufficiently large `n`; it also mentions the
Komlós–Sós generalization. [Problem](https://www.erdosproblems.com/580) ·
[Zhao’s paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v18i1p27)

**Why finite.** Zhao leaves finitely many `n`; for fixed `n`, both the host
graphs and the relevant trees form finite sets.

**Scale/barrier.** A direct check at `n=20` starts from `2^190` labeled host
graphs and includes 106 unlabeled trees on 10 vertices, so reductions are
essential. The large-`n` theorem uses dense extremal/regularity machinery and
the page supplies no explicit `n₀`, so extending a small SAT frontier cannot
by itself finish the problem.

**Crowd/fit.** The live site shows 2 comments and **one partial proof claim**.
The claim, submitted 2026-07-14 by Rafik Zeraoulia using OpenAI GPT-5.6
Thinking, asserts a computer-assisted proof of the literal vertex formulation
for every `n≤19`, using four CaDiCaL UNSAT certificates after structural
reductions; it explicitly does not cover the stronger classical edge
formulation. [Proof-claim page](https://www.erdosproblems.com/forum/thread/580/proof-claims).
This is strong evidence that an M1-scale certified workflow is viable, but it
also means the race is already underway.

### 3. #19 — Erdős–Faber–Lovász

**Exact live statement.** “If \(G\) is an edge-disjoint union of \(n\) copies
of \(K_n\) then is \(\chi(G)=n\)?” (The page lists a `$500` prize.)

**Current remarks.** Hindman proved `n<10`; Kahn obtained
\(\chi(G)\le(1+o(1))n\); Kang–Kelly–Kühn–Methuku–Osthus proved the answer yes
for all sufficiently large `n`. The remarks also list special cases and a
later generalization. [Problem](https://www.erdosproblems.com/19) ·
[forum](https://www.erdosproblems.com/forum/thread/19?order=newest)

**Why finite.** The large-`n` theorem leaves finitely many `n`. For a fixed
`n`, the union has at most `n²` distinct vertices and pairwise cliques meet in
at most one vertex, hence only finitely many incidence types; each type gives
an `n`-colorability CSP.

**Scale/barrier.** The first case not covered by the general result quoted on
the page is `n=10`, with at most 100 vertices. Symmetry-aware SAT is plausible
for selected incidence types, but there is no numerical large-`n` cutoff on
the page. A proof of `n=10` would be interesting but would not close the
problem; a conclusive attack must either quantify the asymptotic proof and
bridge every remaining `n`, or find a uniform argument.

**Crowd/fit.** 8 comments, 0 claimed proofs; holyterror likes it; nobody is
marked working/difficult/tractable. The comments are mostly status,
bibliographic, and typo discussion. Clean and uncrowded, but substantially
harder than the small first instance suggests.

### 4. #551 — cycle versus clique Ramsey numbers

**Exact live statement.** “Prove that
\[
R(C_k,K_n)=(k-1)(n-1)+1
\]
for \(k\ge n\ge3\) (except when \(n=k=3\)).”

**Current remarks.** Bondy–Erdős proved the identity for `k>n²−2`,
Nikiforov for `k≥4n+2`, and Keevash–Long–Skokan for
\(k\ge C\log n/\log\log n\), hence for all sufficiently large `n`.
[Problem](https://www.erdosproblems.com/551) ·
[forum](https://www.erdosproblems.com/forum/thread/551?order=newest)

**Why finite.** The large-`n` theorem bounds `n`; for every surviving `n`, the
Bondy–Erdős result bounds `k` by `n²−2`. Thus only finitely many `(n,k)` pairs
remain, and each is a finite red/blue edge-coloring check.

**Scale/barrier.** Even the representative diagonal instance `(n,k)=(7,7)`
asks about colorings on 37 vertices, i.e. \(2^{\binom{37}{2}}=2^{666}\) raw
colorings. The site gives no explicit value of `C` or resulting `n₀`. SAT can
probe cases and find extremal structure, but a blind exhaustive closure on
16 GB is unrealistic.

**Crowd/fit.** 1 comment, 0 claimed proofs, and no reaction flags. This is a
better “be first” target than the active problems, but it needs a theoretical
reduction rather than a finite sweep.

### 5. #848 — sets for which \(ab+1\) is never squarefree

**Exact live statement.** “Is the maximum size of a set
\(A\subseteq\{1,\ldots,N\}\) such that \(ab+1\) is never squarefree (for all
\(a,b\in A\)) achieved by taking those \(n\equiv7\pmod{25}\)?”

**Current remarks.** The page gives van Doorn’s asymptotic density bound
`0.108…`, Weisenberg’s improvement to about `0.105`, and Sawhney’s solution
for all sufficiently large `N`, including stability near density `1/25`.
[Problem](https://www.erdosproblems.com/848) ·
[Sawhney note](https://www.math.columbia.edu/~msawhney/Problem_848.pdf) ·
[forum](https://www.erdosproblems.com/forum/thread/848?order=newest)

**Why finite.** Sawhney leaves finitely many `N`; for fixed `N`, there are
`2^N` subsets.

**Scale/barrier.** The forum initially identified an explicit threshold
\(\exp(1420)\). GPT-5.4-assisted notes then successively reduced the claimed
threshold; the latest number posted on 2026-03-23 is
\(N_0=2.64\times10^{17}\). That number is forum work, not incorporated into
the main remarks. A separate attempted computation to `10^7` reportedly took
almost a day and was later assessed as likely incorrect; in any event it
cannot bridge the gap by linear scaling. The viable route is a new analytic
inequality or a certificate that covers huge intervals, not enumeration.

**Crowd/fit.** 48 comments, 0 formal proof claims on the site; TerenceTao and
BorisAlexeev mark it tractable. Multiple GPT/Claude-assisted efforts, public
repositories, threshold-optimization notes, and formalization attempts
already exist. It is demonstrably AI-suited but very poor for the goal of
being first.

### 6. #742 — Murty–Simon diameter-two critical graphs

**Exact live statement.** “Let \(G\) be a graph on \(n\) vertices with
diameter \(2\), such that deleting any edge increases the diameter of \(G\).
Is it true that \(G\) has at most \(n^2/4\) edges?”

**Current remarks.** The page attributes the conjecture to Murty and Plesnik
(with alternate historical attributions), notes the complete bipartite
extremizer, and says Füredi proved it for sufficiently large `n`.
[Problem](https://www.erdosproblems.com/742) ·
[forum](https://www.erdosproblems.com/forum/thread/742?order=newest)

**Why finite.** Füredi leaves finitely many `n`; every fixed `n` has finitely
many graphs.

**Scale/barrier.** Later literature reports that Fan handled `n≤24` and
`n=26`, while Füredi’s cutoff is a tower of twos of height about `10^14`.
[Haynes–Henning–van der Merwe–Yeo summary](https://eudml.org/doc/268952).
Already `n=25` has `2^300` labeled graphs before criticality and isomorphism
reductions. The tower-sized interval makes “finite check” purely logical, not
computational.

**Crowd/fit.** 1 comment, 0 claimed proofs, no reaction flags; the conjecture
statement is formalized. Low crowd is outweighed by the quantitative barrier.

### 7. #556 — three-color Ramsey number of a cycle

**Exact live statement.** “Let \(R_3(G)\) denote the minimal \(m\) such that
if the edges of \(K_m\) are 3-coloured then there must be a monochromatic copy
of \(G\). Show that \(R_3(C_n)\le4n-3\).”

**Statement defect.** A 2026-07-13 forum comment points out that the displayed
statement is false at `n=3`: \(R_3(C_3)=17>9\). The intended conjecture is
`n≥4`. This correction had not been incorporated into the live statement as
of the access date. [Problem](https://www.erdosproblems.com/556) ·
[forum](https://www.erdosproblems.com/forum/thread/556?order=newest) ·
[linked OEIS entry](https://oeis.org/A389335)

**Current remarks/finite reduction.** Łuczak proved asymptotic bounds;
Kohayakawa–Simonovits–Skokan proved the intended claim for sufficiently large
odd `n`, and Benevides–Skokan proved \(R_3(C_n)=2n\) for sufficiently large
even `n`. Hence only finitely many corrected cases remain.

**Scale/barrier/activity.** The linked OEIS entry tabulates exact values only
for `n=3,…,8`. A raw `n=9` upper-bound check colors 528 edges of `K_33`, a
space of \(3^{528}\approx10^{252}\). The site has 2 comments, 0 claimed
proofs, and no reaction flags. **Do not shortlist the current literal
problem.** After adding `n≥4`, it remains a major multicolor Ramsey task, not
an M1 brute-force job.

### 8. #547 — Ramsey numbers of trees

**Exact live statement.** “If \(T\) is a tree on \(n\) vertices then
\(R(T)\le2n-2\).”

**Statement defect.** The forum records that the literal statement fails for
the one-vertex tree: \(R(K_1)=1\) but \(2n-2=0\). The intended statement needs
`n≥2`. [Problem](https://www.erdosproblems.com/547) ·
[forum](https://www.erdosproblems.com/forum/thread/547?order=newest)

**Current remarks/finite reduction.** The page says the result follows for
large `n` from the announced, unpublished Erdős–Sós proof, and independently
from Zhao. It lists paths, stars, double stars, and the 2025 bounded-maximum-
degree theorem of Montgomery–Pavez-Signé–Yan. For fixed `n`, there are
finitely many trees and \(2^{\binom{2n-2}{2}}\) two-colorings to inspect.

**Scale/barrier/activity.** At `n=10`, even before isomorphism reduction there
are \(10^8\) labeled trees and \(2^{153}\) colorings of `K_18`. No explicit
large-`n` threshold is given. 3 comments, 0 claimed proofs; ferraripower both
likes it and is marked currently working. **Exclude as written and avoid for
a first-to-publish race.**

### 9. #506 — minimum number of determined circles

**Exact live statement.** “What is the minimum number of circles determined
by any \(n\) points in \(\mathbb R^2\), not all on a circle?”

**Statement defect.** The page itself says a nondegeneracy condition is
clearly intended—perhaps “not all on a line,” or the stronger “no three on a
line.” Those are materially different problems. Under the literal wording,
an all-collinear set is allowed and determines no circles. There is therefore
no clean unsolved theorem to hand to another AI without first changing the
problem. [Problem](https://www.erdosproblems.com/506) ·
[forum](https://www.erdosproblems.com/forum/thread/506?order=newest)

**Current remarks/finite reduction.** Under Elliott’s “not all on a circle or
a line” assumption, the corrected Purdy–Smith lower bound
\[
\binom{n-1}{2}+1-\left\lfloor\frac{n-1}{2}\right\rfloor
\]
is best possible for `n>393`; small `n` remain. The page notes Segre’s
projected-cube obstruction at `n=8`. Thus a chosen intended variant has the
only explicit modest cutoff in this nine-problem set. Fixed-`n` existence
questions are decidable by real quantifier elimination/incidence-type
enumeration.

**Scale/barrier/activity.** The cutoff still permits up to 786 coordinate
variables, with circle coincidences among millions of triples; generic CAD
or order-type enumeration is far beyond 16 GB. A June 2026 AI-assisted forum
post gives an exact 18-circle `n=8` construction and says a fuller dataset and
code will follow, so there is also quiet active competition. The page shows 2
comments and 0 proof claims. If the human first fixes a precise
nondegeneracy convention, this becomes computationally interesting; it is
not a valid “unsolved Erdős problem as stated” candidate.

## Suggested handoff

If only one separate AI is available, give it **#475** and require:

1. a literature-complete restatement of the four large-prime regimes;
2. explicit constants/overlap or a uniform replacement argument;
3. certified finite checks beginning at `p=17`, with independently checkable
   witnesses/certificates; and
4. a hard stop against reporting small-prime verification as a full solution.

If running a second effort, use **#580** only with awareness of the July 2026
partial claim and make the target a general structural reduction or explicit
bridge to Zhao’s range, not merely `n=20`.

# Acceptance audit of the fixed start matching obstruction

## Publication edition: finite numerical certificate omitted

This prose-only edition preserves the complete general divisibility-closure
and rough-part derivations and reports the accepted finite claim. The numerical
Hall witness, its neighbor lists, matching assignments, full finite slack-table
entries, supplementary exact-value dataset, executable code and raw certificates
are omitted. The finite claim, including E(16)=40 and H(16)=24 and the success
of every tail in the defined family at endpoint 39, cannot be independently
reproduced from this edition alone. It is not a complete self-contained proof
of the finite claim or a full computational reproduction package. Published
hashes, aggregate counts and match results identify separately audited evidence;
hashes alone do not prove the omitted arithmetic. The general structural
arguments are written out in full and do not depend on finite regression tests.

## Decision

Accept the mathematical note as a partial structural result and a finite obstruction to the proposed exact smooth-tail criterion. No mathematical correction is required. The accepted note has SHA-256 ad1242fb0073b53d830ceba350db7d1db2e62a4c41849649cdeb11f84e73ea66 and 11323 bytes.

The result does not solve the fixed-start asymptotic problem, improve its known bounds, establish novelty, or refute asymptotic sufficiency of a suitably formulated smooth-tail condition. These limitations are stated accurately in the note.

## Problem and conventions

The object under review is the least integer length H(n) permitting distinct multiples of 1 through n in the fixed interval (n,n+H(n)]. Its absolute endpoint is E(n)=n+H(n). The word “fixed” concerns the starting point n; an assertion about the worst starting point is a different assertion.

The 1980 source defines its one-variable f(n) as E(n), while its f(n,m) measures a length. This distinction is visible on printed page 147. The 1992 restatement on printed page 36 uses an open right endpoint. For integral lengths the open-endpoint minimum is H(n)+1, because the integers strictly below n+L are exactly those at most n+L−1. The candidate uses the closed convention consistently.

## General mathematical arguments

### Divisibility closure

For any left set A, let its upper closure consist of all b at most n divisible by some a in A. This closure contains A. Every multiple of such a b is already a multiple of a, so its right neighborhood does not grow; the reverse neighborhood containment follows because A is contained in its closure. Consequently the deficiency cannot decrease. Any failed Hall inequality therefore has a divisibility-upward-closed witness. The argument applies also when the right interval is empty and has no unstated large-n assumption.

### Rough-part fibers

For prime q, separate the factors of an integer at the threshold q, placing primes at least q in the rough part. If k>x/q and k divides j≤x, the quotient j/k is a positive integer strictly smaller than q. It cannot contribute any prime at least q. Thus every permitted edge stays in one rough-part fiber.

For a fiber with rough part d, put N=floor(n/d) and X=floor(x/d). Division by d gives left integers s≤N whose prime factors are below q and right integers N<t≤X with the same smoothness property. The lower left cutoff is exactly s>X/q: since sq is integral, dsq>x is equivalent to sq>floor(x/d). This checks the potentially delicate floor and strict endpoint in Lemma 2. Divisibility is preserved in both directions. Right vertices not incident to a left vertex may be retained without changing Hall deficiencies.

Given a deficient upper set with least element m, choose a prime q>x/m. All its elements lie in the restricted graph. Different fibers have disjoint neighborhoods, so at least one fiber is deficient. If a belongs to that fiber and a divides b≤n, then b/a≤n/a≤x/a<q; hence the rough part of b equals that of a. Its divided set is therefore an upper set in the stated smooth fiber. This proves the corollary, without implying a useful uniform bound on the chosen q.

### All cutoff and dilation quantifiers

For d≤16, write N=floor(16/d). On the finite set of possible s values, every real smoothness cutoff y≥1 is equivalent to one of 1 or the primes at most N. In particular, y=1 includes s=1 through the declared convention P⁺(1)=1. Every real u≥0 is equivalent to h=min(floor(u),N), since the strict inequality s>u is equivalent to s>floor(u) for integral s. This covers cutoff equality, cutoffs between successive integers or primes, and empty tails. There are no remaining real-parameter cases.

Every neighbor of a dilated member ds is a multiple of d. Dividing all vertices by d therefore maps its actual neighborhood exactly into the interval (floor(16/d),floor(39/d)], with no extraneous right vertices. For d=2 through 16 the full normalized graph has a matching. Restricting that matching to any permitted subset proves the required inequality for every smooth tail, including any overlapping descriptions of the same tail. For d>16 no positive s is possible. The proof thus covers every positive integer dilation, rather than only the displayed values by example.

## Independent finite verification

An independently authored standard-library checker was used. No candidate program was imported or executed. Its checks use explicit failures and remain active under Python normal, -O, and -OO modes.

- Recomputed all 119 entries in the original note's undilated slack table from the actual divisibility neighborhoods. Every entry agrees and is nonnegative.
- Directly checked all 249 canonical parameter triples across d=1 through 16, in addition to the general reduction of the real cutoffs.
- Constructed independent matchings for all 15 normalized dilation graphs and checked all six small matching assignments printed in the original note.
- Recomputed the seven-element Hall witness and its complete six-element neighborhood at endpoint 39. The witness is upward closed.
- Checked the candidate's assignment at endpoint 40 and constructed a second assignment independently. The maximum matching sizes at endpoints 39 and 40 are 15 and 16 respectively. Thus E(16)=40 and H(16)=24.
- Exhaustively checked all 65536 left subsets at endpoint 39 as a redundant finite check.
- Independently validated the 302 supplementary exact-value certificates for n=1 through 300, 1000, and 10000, using a successful matching at E and a complete deficient neighborhood at E−1. These additional values are not premises for an asymptotic conclusion.
- Checked the general formulas on 9680 finite rough-part graphs, 42998 floor-normalized fibers, and 38914 closure cases. These finite checks supplement the general proofs above; they do not replace them.
- Rejected twelve malformed certificate controls in every optimization mode, including repeated images, wrong interval endpoints, false divisibility, omitted neighbors, nondeficient sets, and length/endpoint confusion.

The numeric payloads, executable checks, and raw certificates are retained separately from this public report. The public verification metadata contains hashes, byte counts, coverage, and outcomes.

## Source attribution and asymptotic limits

Printed page 150 of Erdős–Pomerance gives the lower constant 2/√e. Printed pages 154–155 give the sharpened upper constant √r/(1−r), where exp(−r)=r; the earlier Theorem 3 gives constant 2. These constants and the defining equation were checked visually against the source PDF rather than accepted from OCR. Subtracting n from the endpoint changes neither leading constant on the stated diverging scales.

The displayed lower and upper bounds imply H(n)=n(log n)^(1/2+o(1)): after taking logarithms of H(n)/n, the lower bound differs from (1/2)log log n by at most (1/2)log log log n plus a bounded term, and the upper bound differs by a bounded term. Dividing by log log n gives the exponent. This is a consequence of the cited bounds, not a new asymptotic equivalent.

The original lower-bound smooth-number obstruction is a necessary-condition argument. The candidate does not attribute an exact sufficiency claim to that paper. The finite obstruction instead disproves the stronger, proposed criterion that passing every set in the specifically defined family T(d,y,u) always guarantees a matching. It does not refute every possible criterion involving smooth numbers, eventual sufficiency, or sufficiency with an asymptotic loss.

The retained van Doorn note and the Chen–Korsky v2 definitions and theorem statements concern a maximum over starting points. Their results have not been used to close the fixed-start gap. This audit checks attribution and scope; it does not independently re-prove the cited external analytic number theory or the uniform-start papers. No new literature search, current-status assertion, absence-of-other-work assertion, or novelty determination is part of this acceptance.

## Corrections and accepted use

Required mathematical corrections: none.

The safe characterization is “a checked divisibility-closure and rough-part reduction, with a finite counterexample to exact sufficiency of all full smoothness/size tails and their positive integer dilations.” Retain the family definition and the finite/asymptotic distinction whenever summarizing the result. The problem remains unresolved by this work.

## Public sources

1. Paul Erdős and Carl Pomerance, *Matching the natural numbers up to n with distinct multiples in another interval*, Proceedings A 83(2) / Indagationes Mathematicae 42 (1980), 147–161. [Author-hosted paper](https://math.dartmouth.edu/~carlp/PDF/matching.pdf).
2. Paul Erdős, *Some of my forgotten problems in number theory*, Hardy-Ramanujan Journal 15 (1992), 34–50. [Journal paper](https://hrj.episciences.org/125/pdf).
3. Wouter van Doorn, *On the length of an interval that contains distinct multiples of the first n positive integers*, Integers 26 (2026), A7. [DOI](https://doi.org/10.5281/zenodo.18154085).
4. Kaizhe Chen and Samuel Korsky, *Improved Bounds for Distinct Multiples in Intervals*, arXiv:2607.26450v2 (2026). [Versioned record](https://arxiv.org/abs/2607.26450v2).

## Edition and review statement

This AI-assisted work is unrefereed. Acceptance refers to an independent
internal AI audit of the original note and its separate numerical evidence.
No external human peer review, journal acceptance or formal proof-assistant
certification is claimed. No mathematical correction was required. No novelty,
priority, asymptotic improvement, eventual obstruction, or full solution is
claimed. The fixed-start asymptotic question remains unresolved by this work.

This edition preserves the complete general structural proofs, the exact finite
claim and all substantive scope qualifications. It omits numerical proof
payloads and explicitly distinguishes the reported finite verification from
the written general arguments. Original sealed candidate and audit packages
are unchanged. Historical source inspection and verification are reported as
such; preparation of this edition checks byte integrity and publication
structure only, without new mathematical computation or scholarly-source
retrieval/inspection. Copied source documents, source text and images, datasets,
raw certificates, executable code and private coordination material are not
distributed.

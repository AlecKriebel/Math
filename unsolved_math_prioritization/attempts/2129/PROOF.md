# Distinct strict-smooth components: a sharper finite obstruction

## Publication edition: computational evidence omitted

This prose-only edition includes the complete general reduction proof and
independent mathematical audit, and reports the accepted finite computation.
The actual numeric witness N, raw certificate, residues, component sequence,
checker code and detailed computational logs are omitted. Consequently these
files are not an executable or full computational reproduction package: the
reported equality f(N,500)=208 cannot be independently recomputed from this
edition alone. Hashes, counts and match results identify the separately audited
material; hashes alone do not prove the arithmetic assertion. The general
partition and safe-lift arguments are fully written below.

**Target:** EP-461 / problem 2129.
**Outcome:** a rigorously checkable finite obstruction, not a solution of the uniform lower-bound question. No novelty or optimality claim is made.

## 1. Exact problem and domain

For a positive integer (m) and a positive integer (t), define

\[
s_t(m)=\prod_{\substack{p\mid m\\p<t}}p^{v_p(m)},\qquad
f(n,t)=\bigl|\{s_t(n+i):1\leq i\leq t\}\bigr|.
\]

The product is over primes, uses their **full** valuations, and an empty product is 1. Values, rather than prime factors or valuation entries, are counted. The boundary is (p<t), not (p\leq t).

Erdős–Graham, *Old and New Problems and Results in Combinatorial Number Theory* (1980), printed pp. 91–92, splits (n+i=a_i b_i) with the prime factors of (a_i) below (t) and those of (b_i) at least (t). The displayed minimum on p. 92 is over (t), with (n) unrestricted; no condition (n>t) is imposed. We retain the intended all-(n) uniform question. The natural domain where all the positive-integer components above are defined is (n\geq0); if natural-number notation instead starts (n) at 1, all the minima and obstructions below are unchanged by periodicity. No claim concerning (s_t(0)) or negative integers is needed.

The question is whether one absolute (c>0) satisfies (f(n,t)\geq ct) throughout this domain. The book reports a lower bound of order (t/\log t), without supplying its proof on these pages.

## 2. Exact finite reduction

For each prime (p<t), let (q_p=p^{e_p}) be the least power of (p) satisfying (q_p\geq t), and put

\[
M_t=\prod_{p<t}q_p.
\]

Empty products are 1. The following familiar reduction is included with a complete proof; a closely related period reduction is already present in the public July 2026 working report [2]. It is not claimed as new here.

**Lemma 1 (large values cannot repeat).** If (s_t(n+i)=s_t(n+j)=a) for (i\ne j), then (a\mid(i-j)), and consequently (a<t).

**Proof.** Both (n+i) and (n+j) are divisible by (a); their nonzero difference has absolute value at most (t-1). ∎

**Lemma 2 (partition, not merely cardinality).** For any admissible (n), the two lists

\[
(s_t(n+i))_{i=1}^{t},\qquad(\gcd(n+i,M_t))_{i=1}^{t}
\]

induce exactly the same equality partition of the positions. Thus

\[
f(n,t)=\bigl|\{\gcd(n+i,M_t):1\leq i\leq t\}\bigr|.
\]

**Proof.** Write (a_i=s_t(n+i)) and (g_i=\gcd(n+i,M_t)). If (a_i=a_j), their prime exponents truncated at (e_p) agree, so (g_i=g_j). Conversely, suppose (i\ne j) and (g_i=g_j=g). Since (g\mid(i-j)), we have (g<t). No prime exponent in (g) can equal (e_p), since that would give (g\geq q_p\geq t). Therefore every exponent in both (a_i,a_j) is strictly below (e_p), and truncation changed neither number: (a_i=g=a_j). ∎

In particular (f(n,t)), though its numerical singleton labels need not be periodic, has period (M_t). Every residue class has a positive representative, so minimizing over (n\geq0) or over (n\geq1) gives the same result. The Chinese remainder theorem permits independent selection of (n\bmod q_p).

## 3. A smaller exact search space by domination

The following elementary normal form reduces the finite search without relaxing the exact problem. Its mathematical proof, rather than the heuristic optimizer, justifies the reduction. No literature-priority claim is made.

Fix (p<t), put (q=q_p) and (h=q/p<t). For each residue (r_0\bmod h), the possible lifts modulo (q) are

\[
r_0,r_0+h,\ldots,r_0+(p-1)h.
\]

Call a lift **safe** if no position (1\leq i\leq t) satisfies (r+i\equiv0\pmod q). Choose just one safe lift when any exist; when none exist, retain all (p) lifts. Let (R_p) denote the resulting set.

**Lemma 3 (domination).** The global minimum of (f(n,t)) can be attained by CRT data with (n\bmod q_p\in R_p) for every (p<t).

**Proof.** Work with the gcd labels in Lemma 2. Hold every other prime coordinate fixed. Two lifts of (r_0\bmod h) have identical (p)-valuation data below (v_p(h)). At positions divisible by (h), their truncated (p)-factor is (h), except at a possible position divisible by (q), where it is (q). Because (q\geq t), there is at most one such position.

If a safe lift exists, replacing any unsafe lift by the chosen safe one changes only the label at that one position, removing a factor (p). Before this change its label was at least (q\geq t), and was therefore a singleton by the same divisibility argument as Lemma 1. Changing one singleton into any new value cannot increase the number of distinct labels: it either remains a singleton or merges with an existing class. Two safe lifts give identical truncated patterns. The CRT realizes the replacement while preserving all other prime coordinates. Make these non-increasing replacements one prime at a time. Applying this to any global minimizer proves the assertion. ∎

**Lemma 4 (exact count).** The retained number of lifts is

\[
K_p(t)=|R_p|=h+(p-1)\max\{0,t-(p-1)h\}\leq t.
\]

**Proof.** Among the (t) consecutive positions, the number with a specified residue modulo (h) is either (\lfloor t/h\rfloor) or (\lceil t/h\rceil). Since (h<t\leq ph), this is at most (p). Each such position rules out one different lift, so a residue (r_0\bmod h) has no safe lift exactly when it occurs (p) times. There are (\max(0,t-(p-1)h)) such residues. Each contributes (p) retained lifts instead of one, yielding the formula.

If the maximum is zero, (K_p=h<t). Otherwise write (t=(p-1)h+r), with (1\leq r\leq h). Then (K_p=h+(p-1)r\leq(p-1)h+r=t), because ((p-2)r\leq(p-2)h). ∎

Consequently the exact minimum may be sought in at most (\prod_{p<t}K_p(t)\leq t^{\pi(t-1)}) CRT tuples. This is only a finite reduction; it provides no uniform lower bound. At (t=500), the product of the exact (K_p)'s has 219 decimal digits, whereas (M_t) has 424. Neither space was exhausted.

## 4. Certified finite obstruction

**Computational arithmetic theorem.** There is a positive 424-digit integer (N) such that

\[
f(N,500)=208.
\]

Its independently generated CRT witness, the explicit integer, all 500 full smooth components, and two descriptions of the equality partition were audited in a separate, undistributed computational package. The search used the normal form above and is not part of the proof of this equality. A separate standard-library checker establishes:

1. The residue table contains exactly the 95 primes strictly below 500, each with the prescribed least prime-power modulus and a valid residue.
2. Iterative CRT reconstructs a positive integer (N) satisfying every congruence.
3. Repeated exact division of each (N+i) by every prime below 500 retains **all** prime multiplicities, without exponent caps.
4. The resulting 500 integers have 208 distinct values: 154 singleton labels and 54 labels occurring more than once.
5. For each pair of positions, equality of the full components agrees with equality of the independent gcd labels from Lemma 2.
6. Every repeated value is less than 500, and the collision excess is (500-208=292).

The comma-separated decimal component sequence, with no spaces or terminal newline, has SHA-256

`4385fb237f33199a49c7587402874c7de5fa1fdd4e439b8da82211a8ccaa53af`.

The complete numerical witness is required to reproduce the arithmetic theorem. This authored note deliberately records its statement, proof method, and verification metadata separately from that witness; the note alone is not a replacement for the computational certificate.

**Corollary.** If (f(n,t)\geq ct) holds for all admissible (n,t), then

\[
c\leq\frac{208}{500}=\frac{52}{125}=0.416.
\]

**Proof.** Substitute (n=N,t=500) into the proposed uniform inequality. ∎

This is sharper than the previously advertised (218/500=0.436) obstruction in [2]. Fresh independently authored code also verifies that earlier certificate and its published sequence hash. The new value 208 is **not** asserted to be minimal at (t=500), nor is the upper coefficient 0.416 asserted to be best known in all literature.

## 5. Exact residual question and stopping point

Put

\[
A_d(n)=\#\{1\leq i\leq t:s_t(n+i)=d\}\quad(1\leq d<t).
\]

Lemma 1 gives the exact identity

\[
f(n,t)=t-\sum_{d<t}(A_d(n)-1)_+.
\]

The unresolved uniform question is whether there exists an absolute (\delta>0) such that every (t), and every admissible (n) (equivalently every CRT tuple modulo (M_t)), satisfies

\[
\sum_{d<t}(A_d(n)-1)_+\leq(1-\delta)t.
\]

Alternatively, a negative solution requires a sequence (t_j\to\infty) with corresponding (n_j) and (f(n_j,t_j)/t_j\to0). A single finite obstruction supplies neither conclusion. The normal-form lemmas do not supply that missing inequality. No improved uniform lower bound, asymptotic counterexample, full solution, or novelty claim is made. This bounded attempt ends with the verified finite obstruction and exact search-space reduction.

## Sources

[1] P. Erdős and R. L. Graham, *Old and New Problems and Results in Combinatorial Number Theory* (1980), printed pp. 91–92. https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf

[2] Patrick White + Claude, AI-disclosed working report, *Erdős problem #461 — wave 5w*, dated 2026-07-26. https://www.erdosproblemaday.com/report/461 . Used as the source of the earlier finite-period result and numerical claim; arithmetic was checked independently rather than trusting its executable program.

[3] Thomas F. Bloom, *Erdős Problem #461*. https://www.erdosproblems.com/461 ; discussion https://www.erdosproblems.com/forum/thread/461 . Direct retrieval returned 403 during this attempt; a search-index copy of the discussion was available. No fresh live open-status assertion is based on that cached copy.

## Edition and review statement

This AI-assisted work is unrefereed. Acceptance means an independent internal
AI audit of the stated partial results; no external human peer review, journal
acceptance or formal proof-assistant certification is claimed. No mathematical
correction was required. The numerical result improves the specified earlier
218/500 example, with no global novelty, priority or optimality assertion.
The existence of a positive uniform lower coefficient remains unresolved by
this work.

The complete mathematical arguments and their qualifications are preserved.
Editorial changes add distribution/review framing, remove workflow wording,
and clarify references to the separate computational evidence. Original sealed
candidate and audit packages are unchanged. Historical verification and source
inspection are reported as such; preparing this edition performs byte-integrity
and publication-structure checks only, with no new mathematical computation or
scholarly-source retrieval/inspection. Copied source documents, source text and
images, executable code, raw datasets and private coordination material are not
distributed. In particular, the numeric witness N is not included. This is a
prose-only edition, not a self-contained computational certificate.

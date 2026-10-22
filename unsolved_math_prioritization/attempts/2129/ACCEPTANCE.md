# Independent acceptance: distinct strict-smooth components

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

**Problem:** Erdős #461 / problem 2129.
**Decision:** accept the finite arithmetic obstruction and the exact safe-lift reduction. No mathematical correction is required. This is partial progress, not a solution of the uniform positive-coefficient problem.

## Accepted statements

For positive integers $m,t$, let $s_t(m)$ be $\prod_{p<t}p^{v_p(m)}$, where $p$ runs over primes and full valuations are used, and let $f(n,t)$ count the distinct whole values of $s_t(n+1),\ldots,s_t(n+t)$. The empty product is 1. The admissible interval domain is $n\geq0$; all conclusions also hold when $n\geq1$ is required.

1. The supplied positive 424-digit integer $N$ satisfies **$f(N,500)=208$**. Independently reconstructed CRT data and full repeated division agree with every supplied component.
2. Therefore every universal constant satisfying $f(n,t)\geq ct$ must obey **$c\leq52/125=0.416$**.
3. The earlier public working report's integer independently gives $f(n,500)=218$, and its advertised component hash matches. Thus the new certificate lowers that particular finite upper bound from 0.436 by exactly 0.020. It is not certified as the best bound in the literature or the minimum at $t=500$.
4. With $q_p=p^{e_p}\geq t$ the least qualifying power and $M_t=\prod_{p<t}q_p$, the full components and the labels $\gcd(n+i,M_t)$ induce the same equality partition.
5. Keeping one safe lift modulo $q_p$ for each base residue modulo $q_p/p$, or every lift when no safe one exists, preserves an attainable global minimum. The exact number retained for prime $p$ is

\[
K_p(t)=h+(p-1)\max\{0,t-(p-1)h\}\leq t,\qquad h=q_p/p.
\]

## Independent computation

Only newly authored Python standard-library code was executed. Candidate and third-party programs were neither imported nor executed. There was no new search for improved residues or numerical optimization.

The audit independently generated the 95 primes below 500 and their least prime-power moduli. It reconstructed both integers in two ways: the direct CRT sum with modular inverses, and incremental CRT in reverse prime order using an independently implemented extended Euclidean inverse. The reconstructions agree and satisfy every residue. The candidate is the positive least nonnegative representative, has 424 digits, and lies below its 424-digit modulus.

For each of the 500 positive integers in the candidate interval, repeated division extracted the full smooth component without exponent caps. Exact integer comparisons, not hashes alone, matched the supplied sequence and repeated-position classes. There are 154 singleton values and 54 repeated values. The collision excess is 292. Every repeated value is below 500. The full-component partition equals the independent gcd partition. The candidate residues also satisfy the safe-lift normal form.

The canonical component serialization is comma-separated decimal ASCII, with no spaces or terminal newline. Its SHA-256 is:

`4385fb237f33199a49c7587402874c7de5fa1fdd4e439b8da82211a8ccaa53af`

The previous certificate gives 167 singleton values, 51 repeated values, and collision excess 282. Its matching sequence SHA-256 is:

`1c76b4e40b5bc9e8afe9cbdbbd1e67b4fae4c69dc91d322625da534d88b1781d`

Three executions, using normal Python, `-O`, and `-OO`, produced byte-identical successful audit results. All checks use explicit exceptions and survive assertion removal. Eleven altered-certificate controls were rejected, including changed counts, integer, component, prime list, modulus, residue, hash, ratio, and partition flag.

Independent structural regressions covered all 3,714 residue states for $1\leq t\leq7$, including $n=0$; 65,749 position-pair comparisons; and 8,114 safe-lift replacements. Every old equality survives replacement, and the distinct count never increases. Another 675 prime/threshold cases verify the exact retained-pattern count, including all primes below 500. Fourteen strict-prime-boundary tests, a high-multiplicity test, and the empty-product test pass. These checks corroborate the proofs; the proofs are not inferred from them. The ancillary candidate claim about minimum values through $t=8$ was not needed or re-exhausted in this audit.

## Source and domain review

The authenticated scan of Erdős and Graham's 1980 monograph was visually inspected at printed pages 91–92, represented by the retained page images numbered 87–88. It places primes below $t$ in the first component and primes at least $t$ in the complementary factor. No $n>t$ condition is present. The printed minimum is over $t$, with $n$ unrestricted; the accepted formulation is the intended uniform all-$n$ question.

The dated July 26, 2026 AI-disclosed working report was directly opened as rendered text for comparison. Its printed integer and sequence hash agree with the independently checked earlier certificate. It already contains the finite-period reduction. Neither priority for that reduction nor novelty for the safe-lift argument is claimed here. Current live tracker status was not independently established by this audit.

## Scope and residual problem

The candidate manifest and all 20 listed members matched the supplied hashes and byte counts, with no extra candidate files except the manifest and its detached hash. The source verification collection's manifest and all 125 listed members also matched. These integrity checks authenticate the audited material; they do not independently prove every historical execution statement in the candidate's source narrative.

The numerical witness, raw certificates, residue tables, component lists, and executable code remain separate from this authored report. The report and hashes are not a self-contained replacement for the full computational certificate. Anyone reproducing the arithmetic must also receive that certificate through an authorized channel.

The unresolved question is still whether there is any absolute $c>0$ such that $f(n,t)\geq ct$ for every admissible $n,t$. A single finite example supplies no sequence with $f(n_j,t_j)/t_j\to0$, and the normal form supplies no uniform lower bound. No full solution, asymptotic counterexample, optimality, or literature-wide novelty is accepted or asserted.

## Public sources

- P. Erdős and R. L. Graham, *Old and New Problems and Results in Combinatorial Number Theory*, Monographies de L'Enseignement Mathématique 28 (1980), printed pp. 91–92. https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf
- Patrick White + Claude, *Erdős problem #461 — wave 5w*, AI-disclosed working report, July 26, 2026. https://www.erdosproblemaday.com/report/461
- Thomas F. Bloom, *Erdős Problem #461*, problem locator; not a fresh status verification. https://www.erdosproblems.com/461

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

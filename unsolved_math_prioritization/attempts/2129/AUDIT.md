# Proof audit of the finite reduction

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

Fix an integer $t\geq1$. For each prime $p<t$, let $q_p=p^{e_p}$ be the least power at least $t$, and put $M_t=\prod_{p<t}q_p$. All numbers in the interval $n+1,\ldots,n+t$ are positive when $n\geq0$.

## 1. Equality partitions and periodicity

If two distinct positions share their full smooth component $a$, then $a$ divides their difference, which lies in absolute value between 1 and $t-1$. Hence every repeated full component is less than $t$.

Write $a_i=s_t(n+i)$ and $g_i=\gcd(n+i,M_t)$. Equal $a_i$'s certainly give equal $g_i$'s by truncation of each prime exponent. Conversely, if distinct positions have $g_i=g_j=g$, then $g\mid(i-j)$ and $g<t$. If any exponent of $g$ reached its truncation level $e_p$, then $g\geq p^{e_p}\geq t$, a contradiction. Thus no exponent in either full component is truncated, and $a_i=g=a_j$. This proves exact equality of partitions, not merely their cardinalities.

The gcd list depends only on $n\bmod M_t$, so the partition and $f(n,t)$ are periodic. Numerical singleton labels need not be periodic. Every residue class has a positive representative, including the zero class represented by $M_t$. Thus restricting $n\geq0$ to $n\geq1$ changes neither the possible partitions nor the minimum. For $t=1,2$, the prime product is empty, $M_t=1$, and all components equal 1; the same argument remains valid.

## 2. Direction of the safe-lift domination

Fix $p<t$, $q=q_p$, and $h=q/p<t$, with every other prime coordinate fixed. Lifts of one residue modulo $h$ have identical divisibility by lower powers of $p$. At positions divisible by $h$, the truncated prime factor is $h$, except that an unsafe lift has one position with factor $q$. There can be at most one such position because the interval has length $t\leq q$.

A safe lift has no $q$-divisible position. Replacing an unsafe lift by a safe one changes exactly that one old gcd label, dividing it by $p$. The old label was at least $q\geq t$. Because it divides its corresponding interval integer, it cannot have appeared at a second position: otherwise it would divide a nonzero difference of size at most $t-1$. It was therefore a singleton.

Changing a singleton can either leave a singleton or merge it into an existing class. It cannot split an existing class, and cannot increase the number of classes. Equivalently, every old equality remains an equality: the new partition is coarser. This is the direction needed to retain a global minimum. It is not a claim that the new full smooth component always divides the old full smooth component for arbitrary CRT representatives; the proof operates on the gcd labels and then transfers their partition cardinality to full components.

Two safe lifts for the same base residue produce exactly the same truncated prime-factor vector. Therefore one representative suffices. When no safe lift exists, all lifts must remain available. Independent CRT coordinates allow one prime to be changed without altering any other prime coordinate. Starting with a minimizer modulo the finite modulus and making these non-increasing changes one prime at a time yields a minimizer inside the retained product set.

## 3. The exact number of retained lifts

For a fixed base residue modulo $h$, each of its occurrences among the $t$ consecutive positions forbids one lift modulo $q=ph$. The forbidden lifts are distinct because the positions differ by less than $q$. A base residue lacks a safe lift precisely when it occurs $p$ times.

If $t\leq(p-1)h$, no base residue occurs $p$ times. All $h$ base residues contribute one safe lift. If $t>(p-1)h$, write $t=(p-1)h+r$ with $1\leq r\leq h$. Exactly $r$ base residues occur $p$ times, while the other $h-r$ contribute one lift each. The total is therefore

\[
K_p(t)=h+(p-1)\max\{0,t-(p-1)h\}.
\]

In the second case,

\[
t-K_p(t)=(p-2)(h-r)\geq0.
\]

In the first case $K_p(t)=h<t$. This proves $K_p(t)\leq t$, including $p=2$. When $q=t$, every lift is unsafe and the formula gives $K_p=t=q$, as it should.

At $t=500$, the product of retained counts has 219 decimal digits and $M_t$ has 424. These sizes were independently recomputed. Neither product space was exhausted by this audit; no minimum at 500 follows from them.

## 4. The coefficient cap and exact residual statement

The accepted positive witness gives $208\geq500c$ for any putative universal lower-bound coefficient, hence $c\leq52/125$. The direction is an upper bound on allowable coefficients. It does not negate the existence of a smaller positive coefficient.

Let $A_d(n)$ be the multiplicity of the full component $d$, for $1\leq d<t$. Since larger components are singletons,

\[
f(n,t)=t-\sum_{1\leq d<t}(A_d(n)-1)_+.
\]

Thus a positive uniform coefficient is equivalent to a uniform positive fraction left after collision excess. A negative solution would require ratios tending to zero along thresholds tending to infinity. To justify the threshold condition, note that $f(n,t)\geq1$; on any bounded set of thresholds $t\leq T$, the ratio is at least $1/T$. A finite certificate cannot resolve this asymptotic question.

## Citation and provenance limits

The definition was checked against Erdős and Graham, *Old and New Problems and Results in Combinatorial Number Theory* (1980), printed pp. 91–92: https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf . The public working report https://www.erdosproblemaday.com/report/461 already supplies the closely related finite-period argument. The proofs above are independently audited mathematical prose; no copied source document or computational dataset is included in this note. No priority claim is made.

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

# Current smallest open gate

## 1. A valid global physical-time closure theorem

Augment the population CTMC by the actual target $T$ of the last reaction
and use the common residual-factorial potential

\[
 V(x,t)=\sum_i\log((x_i-t_i)!).
\]

It is proper because target molecularity is at most two.

Let $\mathsf A$ be a finite library of strong-Markov physical episode rules.
For an episode $a\in\mathsf A$, write

\[
 D_a(x,t)=\mathbb E_{x,t}
 \bigl[V(Z_{\tau_a})-V(x,t)+\eta\tau_a\bigr],
 \qquad \eta>0.
\]

Assume endpoint integrability. If every divergent marked-state sequence has
a subsequence and one fixed $a\in\mathsf A$ for which $D_a\to-\infty$,
then

\[
 K=\{z:\min_{a\in\mathsf A}D_a(z)>-1\}
\]

is finite. Selecting a minimizing episode outside $K$ and summing the
conditional inequalities only through bounded trace indices gives

\[
 \mathbb E_z N_K+\eta\mathbb E_z T_K\le V(z).
\]

A finite-set trace argument and nonexplosion then give CTMC positive
recurrence. This theorem neither counts skipped reactions nor assumes a
finite inactive environment.

For a current target linkage that contains a same-linkage terminal complex
whose source probability tends to zero, the inherited bounded target-path
calculation supplies exactly such an episode: its expected residual reward
tends to −∞ and its physical duration is uniformly bounded.

## 2. Exact seam closed; first residual fast phase

The former smallest obstruction

\[
 L_0=\{2B,A+B\},\qquad
 L_1=\{C,A+C,B+C\}
\]

is now closed without target conditioning. A network-dependent factorial
potential balances the order-$N^2$ neutral linkage to at most linear positive
drift, while the catalyst-scaled monomolecular linkage contributes at most
$-kN\log\log N+KN$. The same argument and an autonomous-clock product branch
cover all seven compatible positive-invariant shielded supports. See
`certified_exact_shielded_seam.md`.

The first unresolved arbitrary pairing is instead

\[
 L_0=\{B,2A,B+C\},\qquad
 L_1=\{0,A,C\},\qquad h=(1,2,0).
\]

Here $L_0$ preserves $q=A+2B$ and is deficiency zero in isolation, but the
full system has deficiency one. For a concrete pair of directed cycles, the
natural complex-balanced factorial potential has positive generator drift
$n^2\log2-O(n\log n)$ at $(A,B,C)=(n,n^2,0)$. The missing estimate is a
shell-uniform Poisson corrector or killed resolvent that averages the fast
$L_0$ phase, whose stationary $A$ scale is $\Theta(\sqrt q)$, while charging
all $L_1$ shell changes and the unbounded Poisson $C$ coordinate. See
`remaining_fast_phase_corrector.md`.

## 3. Exceptional service needs a proper seam correction

For

\[
 \{C,2C\}\quad\&\quad\{0,A,2A,B+C\}
\]

the atlas descends $W=B-C$, not the proper potential $V$. There are exact
blocks for which service plus the next dominant mixed-linkage reaction has
zero residual-$V$ reward while $W$ falls by one. A linear correction
$\alpha W$ preserves properness when added to the superlinear $V$, so a
network-dependent potential $V+\alpha W$ is a plausible repair. It still
requires a two-region proof:

- bounded $C$, large $B$: use signed service;
- large $C$: use the quadratic $2C\to C$ drift.

The seam cannot use a shell-independent upward-$C$ service time. For
$C\rightleftarrows2C$, the mean time to move from $n$ to $n+1$ grows
factorially, and its stationary average is infinite. The trace policy must
switch to quadratic downward control at large $C$.

## 4. Countable phases: useful only after a closure alternative

If a leading two-active environment is genuinely closed, its single
population coordinate has degree at most two. Weak reversibility and closure
then suggest an immigration-death/logistic Lyapunov or a conserved phase.
Likewise, a genuinely closed one-active degree-one cofactor process strips to
a unimolecular network on complexes $0,B,C$, hence a product-Poisson open
class or a finite conservative class.

An arbitrary projected source layer need not be closed or weakly reversible.
For example, the weakly reversible cycle

\[
 A\to A+C\to2C\to A

\]

has a leading $A$-scale projection with upward $C$ motion while its
quadratic return lies at a slower scale. A valid lemma must prove the exact
alternative: promotion/killing/rank exit, or genuine closure under all
same-layer outgoing channels and actual targets. It must also control the
growth of any countable-phase Poisson corrector.

## 5. Certification status

No C3 counterexample is known. The global theorem remains plausible, but the
residual fast-phase corrector and the exceptional-service seam are not
consequences of the certified finite atlas. Until both are proved, there is
no T3-2 preprint suitable for arXiv.

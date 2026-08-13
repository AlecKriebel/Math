# The raw SS-446 invariant, deficiency-zero, and service composition

**Proof-first terminal-chart theorem and exact support identity, 2026-08-12
PDT.**  This note closes the raw shielded/shielded branch of the exact
two-active Q/U/C/S classifier.  The stochastic proof has only three symbolic
ingredients: a common linear invariant, the deficiency-zero product form, and
the already proved literal signed-service seam.  Finite computation is used
only to show that those ingredients exhaust the 446 support--workload
incidences.

No orientation, rate vector, population state, reaction history, or
population box is enumerated.

## 1. Frozen scope and dependencies

After fixed-class projection and linkage merging, fix a two-active chart with
active coordinates $A,B\to\infty$ and bounded coordinate $C$.  The reduced
binary complex universe is

\[
 {\cal C}_2=\{0,A,B,C,2A,2B,2C,A+B,A+C,B+C\}.          \tag{1.1}
\]

The two linkage supports are disjoint and have at least two vertices.  Each
physical reaction graph is arbitrary subject to strong connectivity, and all
labelled rates are fixed and positive.  The ordered classifier and its raw
AA/mixed/SS trichotomy are frozen at

```text
research_notes/proof_first_quc_classifier_bridge_and_raw_trichotomy.md
SHA-256 014a317602b60c765dc9a9eb98f0921ba3fd8f779221e271e0dd7f53e245f54c
```

The literal signed-service theorem and its independent exact-support audit
are frozen at

```text
research_notes/signed_service_seam_full_proof.md
SHA-256 4ec0ae7007184f2c5bda82bd55df5707d2c3570c7fdf2683ad87b97f75930738

research_notes/proof_first_exact_physical_seams_independent_audit.md
SHA-256 e7e76b76cd1371f98d19da0a1f5362ab4a0696548fba62028b29ccd2950617c9
```

The current primary-literature audit for the deterministic deficiency-zero
theorem, the class-restricted stochastic product form, and complex-balanced
nonexplosion is frozen at

```text
research_notes/proof_first_publication_primary_literature_audit.md
SHA-256 48f34724ed2a23d62de8e28f769a003ed0ff19d0a73caa1f38a09d5b9dc0a1d4
```

Section 4 also gives the shorter binary-network nonexplosion proof directly,
so the SS composition does not extend the citation beyond its audited scope.

The finite set identity in this note is reproduced by

```text
src/raw_ss446_composition_certificate.py
SHA-256 7376b9fd3913145d7ff806c6622db0aad9a8f5ffb1be413cfde108c16fa7eaf2

tests/test_raw_ss446_composition_certificate.py
SHA-256 d212e126d113600179c37c3e16648d2485b4b3fbfda336c99cb0e4e34821f49a
```

## 2. Exact raw SS set identity

For each frozen workload

\[
 (1,1,0),\qquad(2,3,0),\qquad(1,2,0),\qquad(1,3,0), \tag{2.1}
\]

take every ordered pair of disjoint nontrivial supports and retain the pair
exactly when both ordered classifier outputs are S.  The result is 446
support--workload incidences on 322 distinct ordered support pairs.

Apply the following disjoint priority to the physical support pair:

1. a common invariant strictly positive in all three coordinates;
2. otherwise, a common invariant positive in the two active coordinates;
3. otherwise, full-network deficiency zero;
4. otherwise, literal membership in the signed-service seam.

The exact incidence partition is

\[
\begin{array}{c|r|r}
\text{branch}&\text{incidences}&\text{distinct ordered pairs}\\ \hline
\text{strictly-positive invariant}&18&18\\
\text{active-chart invariant only}&364&268\\
\text{full deficiency zero}&60&32\\
\text{literal signed service}&4&4\\ \hline
\text{total}&446&322.
\end{array}                                                \tag{2.2}
\]

There is no residual row.  With rows sorted by workload and the two support
payloads, dictionary keys sorted, and compact JSON encoding, the raw and
branch-annotated fingerprints are respectively

```text
842920b5280d96c96e49e0b0b959d548acb2ac43a5dfee4ab110346958acc45f
8870e74f85a50608b2f5586c87a3dc73cf825ae292df41063b77ebae7e1924e3
```

These are support identities only.  The analytic meaning of each branch is
proved next.

## 3. The two invariant branches

For a support pair $L_1,L_2$, let $S$ be the span of all within-linkage
reaction differences.  If $q\in S^\perp$, every physical reaction preserves

\[
                              q\cdot x.                 \tag{3.1}
\]

This statement is independent of orientation and rates because every edge
has both endpoints in one linkage support.

If $q_A,q_B,q_C>0$, then a fixed population class lies in one level set of
(3.1), whose intersection with ${\mathbb Z}_{\ge0}^3$ is finite.  The
18 first-branch incidences therefore have finite classes.

For the second branch, choose $q_A,q_B>0$, with no sign condition on
$q_C$.  On the fixed two-active chart, $C$ lies in a bounded finite phase.
Hence the term $q_CC$ is bounded, whereas

\[
                       q_AA+q_BB\longrightarrow\infty. \tag{3.2}
\]

This contradicts constancy of (3.1) on the fixed communicating class.  Thus
the 364 active-invariant incidences cannot carry the alleged two-active
terminal escape.  This is a chart-local exclusion, not a claim that the
active-only invariant is a proper global Foster function.

## 4. The deficiency-zero branch

Each reduced network in the third branch is weakly reversible because its two
linkage graphs are strongly connected.  Full deficiency zero therefore gives,
for every positive labelled rate vector, a positive complex-balanced vector
$c\in(0,\infty)^3$.  On each closed irreducible population class $\Gamma$,
the class-restricted product form is

\[
 \pi_\Gamma(x)=Z_\Gamma^{-1}\prod_{i=A,B,C}{c_i^{x_i}\over x_i!},
 \qquad x\in\Gamma.                                  \tag{4.1}
\]

It is summable because its mass over $\Gamma$ is bounded by its mass over
all of ${\mathbb Z}_{\ge0}^3$, namely $\exp(c_A+c_B+c_C)$.

Nonexplosion also follows directly from binaryity.  A reaction whose source
has molecularity two cannot increase total population because every target
has molecularity at most two.  Every population-increasing reaction therefore
has source degree zero or one, so its aggregate positive-growth rate is at
most $K(1+|x|_1)$, with bounded jump size.  Comparison with a linear pure
birth process proves nonexplosion.

The normalizable invariant probability and irreducibility then give positive
recurrence of every closed class in all 60 deficiency-zero incidences.

## 5. The exact four signed-service rows

The last branch contains exactly four ordered incidences, all at
$h=(1,3,0)$:

\[
\begin{array}{c|c}
L_1&L_2\\ \hline
\{C,2C\}&\{0,A,2A,B+C\}\\
\{0,C,2C\}&\{A,2A,B+C\}\\
\{A,2A,B+C\}&\{0,C,2C\}\\
\{0,A,2A,B+C\}&\{C,2C\}.
\end{array}                                               \tag{5.1}
\]

Thus there are two unordered physical support pairs.  Both are literal cases
of the frozen signed-service theorem: the pure support is exactly
$\{C,2C\}$ or $\{0,C,2C\}$, and the mixed support is exactly one
of its displayed signed supports.  The independent seam audit passes that
theorem for arbitrary strongly connected orientations and positive rates.
It proves classwise positive recurrence and nonexplosion in physical time.

No support deletion, support inclusion, or monotonic extension is used.  In
particular, the theorem's explicit exclusion of unproved strict supersets of
the pure-$C$ linkage remains in force.

## 6. SS-446 composition theorem

Combining Sections 2--5 gives the exact result.

> **Theorem 6.1 (raw SS-446 exhaustion).**  Every incidence in the frozen
> raw SS output falls in exactly one of the following branches, in the
> priority of Section 2:
>
> 1. a strictly-positive common invariant, giving a finite fixed class;
> 2. a common invariant positive in both active coordinates, excluding the
>    fixed two-active terminal chart;
> 3. weak reversibility and full deficiency zero, giving a nonexplosive
>    class-restricted product-form positive recurrent chain; or
> 4. one of the two literal unordered signed-service networks in (5.1),
>    covered by the frozen physical-time theorem.
>
> The four branches contain $18,364,60,4$ support--workload incidences,
> respectively, and their union is the complete 446-row SS set.  No raw SS
> incidence remains.

This theorem is local to the exact reduced two-active chart.  The active-only
invariant is used only to contradict that chart's escape; the other three
branches are classwise.  The theorem does not claim that recurrence is
monotone under adding reactions or complexes, and it does not follow a
structural exit into a different chart with a different potential.

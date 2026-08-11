# The exact 1,227-pair fourth-power composition

## 1. Scope and frozen inputs

This note composes the exact one-active selector with the physical-time
interface proved in
`research_notes/universal_fourth_power_one_active_interface.md`.  It makes
no claim about the 795 support pairs left outside this selector and no
global T3-2 claim.  An independent audit replayed the composition below at
pre-promotion note SHA-256
`652e41ccd7ae36183862a798fcdfd3bd5acf92ab2528bb356816d14df003b09a`
and returned **PASS** (confidence 0.91).

The inputs are:

1. the affine-feasibility and exact-tier selector in
   `src/one_active_phase_shape.py`, which gives 1,227 support pairs and
   3,297 affine-feasible failing incidences, every one of them one-active;
2. the arbitrary-strong-orientation resistance theorem in
   `research_notes/one_active_arbitrary_orientation_graph_theorem.md`;
3. the all-23 killed-resolvent, random-overshoot, moving-boundary, and
   common-fourth-power theorem in
   `research_notes/universal_fourth_power_one_active_interface.md`; and
4. the all-species reflected target and physical-time gluing theorem in
   `research_notes/all_species_reflected_debt_target.md`.

Fix one support pair, an arbitrary strongly connected directed graph on
each nontrivial linkage support, arbitrary strictly positive rate
constants, and one closed irreducible population class \(\Gamma\).  No
constant below is required to be uniform over different rate vectors or
different classes.

Use the single population potential

\[
 \mathcal F(x)=K+\sum_{i=1}^3\log(x_i!),
 \qquad G=1+\mathcal F\ge1,
 \qquad W(x)=G(x)^4.                                \tag{1.1}
\]

Thus the linear correction is \(\ell=0\) in every chart.  The function
\(W\) is proper on \(\mathbb N_0^3\).

## 2. Fixed-class descriptor dichotomy

> **Lemma 2.1 (classwise bad-sequence extraction).**  Let the support pair
> belong to the 1,227-pair selector.  Every divergent population sequence
> \(x_n\in\Gamma\) has a subsequence satisfying exactly one of the
> following alternatives.
>
> 1. It realizes an Anderson--Kim passing descriptor, and
>    \(\mathcal L W(x_n)\to-\infty\).
> 2. It realizes one of the 3,297 selected one-active failures.  After
>    relabelling, its active coordinate \(X_n\to\infty\), while the two
>    inactive integer coordinates are fixed on a further subsequence.

### Proof

The exact source/D-tier extraction has finitely many descriptors.  Pass to
a subsequence realizing one of them.  A state sequence contained in the
affine class of \(\Gamma\) can realize only an affine-feasible descriptor;
this is the necessity direction of the stoichiometric gate theorem.  By
definition of the 1,227-pair selector, every nonempty affine-feasible
failure is one-active.  Any other descriptor passes the universal
top-source/top-D criterion, and Section 2 of the universal fourth-power
note gives \(\mathcal L W(x_n)\to-\infty\).

For a one-active exact tier, atlas identity (8.6) says that a coordinate
belongs to the active mask exactly when its population diverges.  Thus any
diverging nominally inactive coordinate makes the exact descriptor
at-least-two-active and hence passing.  The remaining inactive integer coordinates are bounded and
therefore constant after one more subsequence.  This is a state-sequence
fixed-width tube, not a claim that a tight distribution has finite
support.  \(\square\)

The usual contradiction now gives a finite-exception generator bound on
the passing part: otherwise choose a divergent sequence with
\(\mathcal L W>-1\) and apply Lemma 2.1.  In fact the stronger bound
\(\mathcal L W\le-cW^{3/4}\) is available on every passing subsequence, so
the concave transform from the universal note controls its physical exit
time as well as its endpoint \(W\)-moment.

The orientation quantifier is already included.  On a fixed class, every
exact descriptor is either affine-infeasible (and therefore impossible),
universally passing (and handled by the common \(W\)), or one of the
selected affine-feasible one-active failures.  For any actual orientation,
a descending row may use the generator drift directly; every remaining
failing orientation is covered by the graph theorem, which quantifies over
all strong orientations of the selected supports.  Positive rate constants
change only the classwise constants, not the resistance or tier
alternatives.

There is also a genuinely finite statewise bad-tube decomposition on the
fixed class.  Otherwise, for every \(M\) and every finite set one could
choose a non-\(W\)-good state whose second-largest coordinate exceeds
\(M\).  Such a sequence has two diverging coordinates; Lemma 2.1 extracts
an at-least-two-active passing subsequence, a contradiction.  Hence there
are \(M_\Gamma<\infty\) and a finite set \(K_0\) such that every
non-\(W\)-good state outside \(K_0\) lies in one of the finitely many tubes

\[
 G=\{x\in\Gamma:\mathcal L W(x)\le-1\},
 \qquad
 B_{X,e}=\{x\in\Gamma\setminus(K_0\cup G):(x_i)_{i\ne X}=e\},
 \qquad e\in\{0,\ldots,M_\Gamma\}^2.                \tag{2.1}
\]

Taking a minimum over these finitely many tubes makes the local episode
constants uniform on \(\Gamma\).  This finite family is derived from the
state-sequence contradiction; it is not inferred from tight occupation
marginals.

## 3. Reachable marked bad tubes

Fix a reference \(x^\circ\in\Gamma\).  On every physical reaction
\(x\mapsto x+\zeta\), update all three reflected marks by

\[
 D_i^+=(D_i+\zeta_i)^+,
 \qquad H_i=X_i-D_i.                                \tag{3.1}
\]

Then \(0\le D_i\le X_i\) and \(H_i\le x_i^\circ\) pathwise.  Consider a
one-active bad-tube subsequence from Lemma 2.1, with active coordinate
\(X\).

If \(D_X=0\), then

\[
 X=H_X\le x_X^\circ.                                \tag{3.2}
\]

Together with the fixed inactive coordinates, this contradicts divergence.
Equivalently, the \(D_X=0\) part of every fixed-width tube is a finite
class-dependent exception.  Thus every divergent reachable marked bad
tube has \(D_X>0\).

The graph theorem separates the remaining rows into a strict old-debt
reduction alternative and a frozen/no-history alternative.  A no-history
base is, by definition, incompatible with a physical history carrying
\(D_X>0\).  A completely frozen population is an absorbing singleton; if
\(\Gamma\) is nontrivial it is absent, and if \(\Gamma\) is that singleton
positive recurrence is immediate.  Consequently every divergent marked
bad-tube sequence which actually occurs uses one of the service
alternatives.

Family II causes no hidden uniform-box requirement.  Its apparent
spectator is an exact invariant \(a_\Gamma\) on the fixed class.  The cap
label \(2\) means \(a_\Gamma\ge2\), not \(a_\Gamma=2\).  The killed Green
and carrier constants may depend on this fixed value.  Families I and III
have the origin base, direct-active rows use their killed exponential phase,
and the 222 wholly-top rows use the audited open Poisson block.

## 4. The common-potential episode

> **Lemma 4.1 (one-active physical episode).**  Outside a finite subset of
> the reachable marked class, every one-active bad-tube state with
> \(D_X>0\) admits an all-reaction physical stopping time \(\tau>0\) such
> that
> \[
>  {\mathbb E}_{x,d}
>  [W(X_\tau)-W(x)+\tau]\le-1.                       \tag{4.1}
> \]
> Its endpoint and duration satisfy the uniform-integrability conditions
> required for localization on that fixed class.

### Proof

The arbitrary-orientation theorem gives aggregate down resistance
\(m\le2\), a strictly positive leading down coefficient, and no same-base
up coefficient through resistance \(m\).  In the wholly-top open family,
the separate Poisson regeneration theorem replaces word resistance by its
effective aggregate value \(m=0\).  Proposition 4.2 and Theorem 4.1 of the
universal fourth-power note turn these inputs into the repeated physical
kernel.

Neutral base endpoints telescope before the first nonneutral return.  A
nonboundary up endpoint has all conditional moments of its random active
overshoot and inactive factorial cost; no deterministic overshoot bound is
used.  A moving-boundary endpoint, including a simultaneous down/up tie, is
charged by the endpoint-weighted three-interruption estimate and lands in
an at-least-two-active passing region.  The successful endpoint strictly
reduces the already-positive reflected debt.  These estimates give (4.1)
for all sufficiently large active levels in each extracted fixed-width
tube.

If no finite exception made (4.1) valid throughout the reachable bad-tube
set, choose a divergent sequence where it failed.  Lemma 2.1 fixes a
template and the inactive base data on a subsequence; the classwise local
theorem then gives (4.1), a contradiction.  This also proves the required
endpoint and duration uniform integrability by the same bad-sequence
argument.  \(\square\)

## 5. Pair-level theorem

> **Theorem 5.1 (the exact 1,227-pair branch).**  For every
> support pair in the one-active selector, every strongly connected
> orientation of its linkage supports, every positive rate vector, and
> every closed irreducible population class, the physical mass-action CTMC
> is positive recurrent.

### Proof

Work on the reachable all-species marked class and use \(W\) from (1.1).
Lemma 2.1 gives \(\mathcal L W\le-1\) outside a finite set and the one-active
bad tubes.  Section 3 and Lemma 4.1 show that every reachable bad-tube state outside
a finite set has positive selected debt and the physical episode (4.1).
These are exactly the hypotheses of the all-debt finite-target gluing
theorem.  The marked chain therefore hits a finite marked set in finite
mean physical time.  Its physical projection is finite and has a finite
mean positive return; irreducibility promotes this to positive recurrence
of every state in \(\Gamma\).

It remains only to justify nonexplosion.  Every population-increasing
reaction has source molecularity zero or one: a binary source already has
the maximal allowed target molecularity and cannot increase total
population.  Hence the total positive population drift rate is at most
\(C(1+\lVert x\rVert_1)\).  Stopping at total-population levels and applying
Gronwall gives nonexplosion.  Quadratic reactions which do not increase
total population cannot generate infinitely many jumps inside a finite
population sublevel, because that sublevel contains finitely many states
with bounded total rate.  \(\square\)

## 6. Exact disjoint contribution

The executable selector in
`src/one_active_prospective_composition.py` gives the following frozen
arithmetic:

\[
\begin{array}{c|r|r|r}
&\text{positive}&\text{signed}&\text{total}\\ \hline
\text{candidate one-active set}&1076&151&1227\\
\text{already certified overlap}&15&0&15\\
\text{new disjoint contribution}&1061&151&1212\\
\text{remainder after contribution}&759&36&795.
\end{array}                                         \tag{6.1}
\]

The overlap is exactly the already-certified critical one-active
15-pair branch; the candidate set has zero overlap with every other
certified branch.  The frozen pair fingerprints are

```text
candidate_1227       3ab28358663c45a089a5bdf4144c28573718b0c4f8b05472a0af208ca919fcf8
new_disjoint_1212    a7784a1f98da2fbadd70a62bc97fe852393cb410a24e666a6d6c246998f0f579
remainder_after_795  6a1327e6c38bfcab30d334691415ba457e84d45d1dfe53d81df4c02aad868123
```

The audit confirmed both Theorem 5.1 and this disjoint arithmetic.  The
1,227-pair theorem is therefore certified, with a net new contribution of
1,212 pairs after removing the exact 15-pair prior overlap.  Global T3-2
remains uncertified.

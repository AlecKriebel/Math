# Proof-first classwise composition for T3-2

**Working theorem note, 2026-08-12 PDT.**  This note records the analytic
composition required for the final theorem.  It is intentionally not a
certificate of the theorem while the three-dynamic-species single-linkage
lemma and the final hard-family replay are still pending.  Finite computation
enters only in the explicitly identified two-linkage support partition; it is
not used to establish any stochastic estimate.

## 1. Statement and fixed-class reduction

Consider a finite stochastic mass-action reaction network in which every
complex has molecularity at most two and every linkage is weakly reversible.
Fix a closed irreducible population class \(\Gamma\).  Delete every population
coordinate constant on \(\Gamma\), delete every linkage with no enabled source
on \(\Gamma\), and merge projected linkages which share a projected complex.
Assume that the resulting network has at most three dynamic species and at
most two active linkage classes.

The desired conclusion is that the physical CTMC is nonexplosive and positive
recurrent on \(\Gamma\).

The reduction is exact.  If \(X_i\equiv m_i\) on \(\Gamma\), closure of
\(\Gamma\) forces every enabled reaction to have zero \(i\)-increment.  In an
active weakly reversible linkage, an enabled source and a directed return path
make every complex physically reachable with the same residual population.
Hence the \(i\)-coordinate is constant across that whole linkage.  Its
falling-factorial factor is a positive constant and can be absorbed into the
reaction rates.  If two projected linkages share a complex, their union is
strongly connected; keeping parallel labelled channels and adding their
propensities gives exactly the projected CTMC.  Thus projection neither
deletes an enabled physical transition nor changes its rate on \(\Gamma\).

It is therefore enough to prove the theorem for the reduced network.  Zero
active linkages give a singleton class.  One and two active linkages are
treated separately below.

## 2. Nonexplosion

Nonexplosion is common to every branch.  A reaction with a bimolecular source
cannot increase total population because its target also has molecularity at
most two.  Consequently every population-increasing reaction has source
degree zero or one, and the total positive-jump rate is bounded by

\[
                         C(1+|x|_1).                 \tag{2.1}
\]

Reaction vectors are bounded.  Localization at total-population levels and a
Yule comparison show that \(|X_t|_1\) is finite on every bounded time interval.
Inside a fixed population sublevel there are finitely many states and bounded
total rates, so population-preserving quadratic reactions cannot accumulate
infinitely many jumps.  The minimal CTMC is therefore nonexplosive.

## 3. The one-linkage branch

The published single-linkage theorem applies when the support contains a
positive pure multiple of every dynamic species.  Weakly reversible
deficiency-zero supports are also positive recurrent by their normalizable
conditioned product-Poisson stationary laws.  These two facts do not exhaust
the projected one-linkage scope: the support

\[
                         \{0,B,2B,A+B\}              \tag{3.1}
\]

and genuine three-species analogues violate the published stochastic-tier
hypothesis on a single closed class.

For at most two dynamic species, an analytic rank/deficiency argument leaves
only (3.1), up to species exchange.  Its missing-cofactor face has an
all-clock origin-launch episode.  Away from that face the ordinary entropy
generator has a top enabled descending source.  At \((A,B)=(n,0)\), geometric
neutral launches and the fast \(A+B\)-exit give, at an included physical
stopping time \(\tau\),

\[
 \mathbb E_{(n,0)}[V(X_\tau)-V(n,0)+\tau]
       \le-\tfrac12\log n,                            \tag{3.2}
\]

while every competing lower-source reaction is retained with
endpoint-weighted probability \(O(n^{-1})\).  State-dependent sampling of
(3.2) and the pointwise generator region gives finite mean hitting time of a
finite set.

The three-dynamic-species branch requires the corresponding carrier theorem.
The load-bearing structural reduction is that a failed proper tier has a
disabled mixed top complex \(V+I\), with \(I=0\), \(V\to\infty\), and no
enabled pure \(V\) or \(2V\) top source.  A valid completion must prove, for
the entire strongly connected linkage rather than for selected words, the
all-clock stopped carrier/service estimate and its physical duration and
endpoint moments.  This theorem is the remaining input to this section and
will be inserted here only after hostile replay.

## 4. The two-linkage support reduction

After projection and merging, two active linkages have disjoint supports in
the ten binary complexes

\[
 \mathcal C_2=\{0,A,B,C,2A,2B,2C,A+B,A+C,B+C\}.       \tag{4.1}
\]

The classwise support reduction is applied in the following order.

1. A strictly positive common stoichiometric invariant makes the class
   finite.
2. A common invariant positive on the two chart-active coordinates excludes
   escape in that chart.
3. Weakly reversible deficiency-zero pairs have the conditioned
   product-Poisson stationary law.
4. The exact seven-support, signed-service, and residual fast-shell theorems
   handle their displayed supports with physical-time Foster estimates.
5. The exact source/D-tier theorem handles every support pair for which all
   proper tier sequences have an enabled top-D descending source.
6. The affine-feasibility theorem removes a failed descriptor precisely when
   no sequence in the fixed affine class can realize its strict monomial
   inequalities.
7. The remaining 2,511 ordered support pairs are partitioned into disjoint
   analytic branches.  The final union contains the prior exact branches, the
   universal one-active branch, the exact 26, easy 416, rank-two 13,
   stopped-service seven, and hard 333 families.

Steps 1--6 are mathematical reductions.  The finite arrangement code in
Step 7 proves only the set identity

\[
 \mathcal R_{2511}=\mathcal R_{\rm prior}\,\dot\cup\,
 \mathcal R_{1212}\,\dot\cup\,\mathcal R_{26}\,\dot\cup\,
 \mathcal R_{416}\,\dot\cup\,\mathcal R_{13}\,\dot\cup\,
 \mathcal R_{7}\,\dot\cup\,\mathcal R_{333}.        \tag{4.2}
\]

It does not quantify over orientations, paths, or populations and supplies no
drift inequality.  Each set in (4.2) is admitted only after its independent
analytic theorem proves the required arbitrary-orientation, arbitrary-positive-
rate statement.

## 5. Common-potential descriptor composition within one pair

For every two-linkage pair, its analytic branch supplies one proper population
potential, either a corrected factorial fourth power

\[
 G_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\cdot x,
 \qquad W_\ell=G_\ell^4,                             \tag{5.1}
\]

or one of the explicitly stated augmented workload scalars in the rank-two
switch branches.  A correction is fixed for the pair, not selected anew at a
stopping endpoint.

Every divergent population sequence has a subsequence with fixed exact
source tier, deterministic tier, availability pattern, and active-coordinate
set.  An affine-infeasible descriptor cannot occur in \(\Gamma\).  On a
passing descriptor the exact factorial finite-difference expansion yields

\[
                         \mathcal LW(x_n)\to-\infty.  \tag{5.2}
\]

On a failed descriptor the corresponding local theorem gives an all-reaction
physical stopping time \(\tau_x\), includes its causing reaction, retains the
actual endpoint, and proves, outside a finite set,

\[
 \mathbb E_x[W(X_{\tau_x})-W(x)+\eta\tau_x]\le-\delta,
 \qquad \eta,\delta>0.                              \tag{5.3}
\]

The endpoint has a fixed moment of order greater than eight (and the required
physical-duration moment).  A cutoff first crossed during an open excursion
is charged as an auxiliary boundary endpoint.  Only an outer closed return is
an exact chart handoff.  Reclassification costs zero because the endpoint is
evaluated with the identical pair potential.

The hard family uses the all-species reflected lift.  From a fixed reference
\((x^\circ,0)\), update

\[
 D_i^+=(D_i+\zeta_i)^+,
 \qquad H_i=X_i-D_i\le x_i^\circ.                   \tag{5.4}
\]

A divergent one-active bad tube has positive selected debt; otherwise
\(X_i=H_i\le x_i^\circ\).  Structural no-history faces cannot carry such a
reachable mark.  Multi-service episodes may continue after the first debt
reduction; reflection affects only the auxiliary mark and never suppresses a
physical reaction.

The descriptor table is used only after (5.2)--(5.3) are proved.  If the
generator-good and episode-good regions failed to cover the complement of a
finite set, a divergent uncovered sequence would have a fixed descriptor
subsequence, contradicting its analytic branch.  This compactness argument
turns the sequencewise estimates into uniform \(\eta,\delta\) on the fixed
class.

## 6. Random-time Foster gluing

Let \(K\) be the resulting finite target in the physical or reflected marked
class.  On the generator-good region run until \(K\) or an episode-good state;
stopped Dynkin applied to (5.2) pays both the potential change and physical
time.  At an episode-good state run (5.3).  Concatenating these pieces at
actual endpoints gives stopping epochs \(S_m\) for which

\[
 \delta\,\mathbb E(m\wedge N_K)
 +\eta\,\mathbb E S_{m\wedge N_K}
 \le W(x)+\delta.                                   \tag{6.1}
\]

Nonexplosion rules out infinitely many positive-length physical episodes in
finite time.  Letting \(m\to\infty\) gives

\[
                         \mathbb E_xT_K<\infty.       \tag{6.2}
\]

In the reflected construction, the reachable marked target is finite because
\(0\le D_i\le X_i\); its physical projection is finite.  Starting from that
finite target, take one ordinary physical jump and apply (6.2) to the finitely
many possible successors.  An absorbing singleton is already recurrent;
otherwise the finite trace has finite mean positive return.  Its cycle
occupation measure is a finite invariant measure, and irreducibility promotes
it to the unique stationary probability on \(\Gamma\).  Thus every state of
\(\Gamma\) is positive recurrent.

## 7. Remaining publication gates

This composition becomes a theorem only when all of the following are pinned
and independently replayed on the exact bytes cited by the final manuscript:

1. the three-dynamic-species single-linkage carrier theorem;
2. the integrated hard one-active 1,104 theorem;
3. the hard-333 pair composition, including correction compatibility;
4. the exact disjoint global union and all earlier support reductions; and
5. the final manuscript's render, bibliography, theorem cross-references, and
   reproducible read-only verification package.

Until then, no global certification flag is justified.

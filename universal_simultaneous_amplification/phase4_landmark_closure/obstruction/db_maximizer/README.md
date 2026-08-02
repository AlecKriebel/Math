# dB maximization and cross-rule sum investigation

## Closed result: the dB maximizer conjecture fails through `r=9/5`

Let `G` be the seven-vertex weighted windmill with center `0`, blades
`(1,2),(3,4),(5,6)`, equal center attachments on each blade of weights

    (100, 10, 1),

and internal blade weights

    (600, 1200, 1800).

Then the exact dB chain gives

\[
 \rho_{\rm dB}(G,3/2)=0.3175490238143979\ldots
 >\frac{1458}{4655}
 =\rho_{\rm dB}(K_7,3/2).
\]

`verify_r_three_halves_counterexample.py` independently constructs the full
126-transient-state chain and the 52-transient-state lumped chain, proves
their transitions agree orbit by orbit, solves both over the rationals, and
checks the exact positive excess.

A second exact example raises the fitness to `7/4`.  It is the nine-vertex
four-blade windmill with

    outer    = (1, 40, 2400, 200000),
    internal = (9000000, 3800000, 2000000, 920000).

It satisfies

\[
 \rho_{\rm dB}(G,7/4)=0.387510078397605232\ldots
 >\frac{6588344}{17097795}
 =\rho_{\rm dB}(K_9,7/4).
\]

`verify_r_seven_fourths_counterexample.py` checks every one of the 512
labelled transition rows against the 162-state orbit chain and solves its 160
transient equations exactly.

A five-blade example reaches `r=9/5`.  On eleven vertices, take

    outer    = (1, 6, 120, 3500, 60000),
    internal = (9000000, 2500000, 880000, 410000, 190000).

Then

\[
 \rho_{\rm dB}(G,9/5)=0.410344367875481897\ldots
 >\frac{1937102445}{4780900817}
 =\rho_{\rm dB}(K_{11},9/5).
\]

`verify_r_nine_fifths_counterexample.py` uses exact FLINT rationals to check
all 2048 labelled transition rows and solve the 484 transient orbit
equations.

## Exact cross-rule diagnostic

At `r=3/2`, the complete graph maximizes
`rho_Bd+rho_dB` among all positive weighted triangles, strictly except at
equal weights.  The comparison numerator has the exact manifestly
nonnegative form

\[
 2\sum_{(i,j,k)}q_{ijk}
 \sum_{(x,y,z)\in\operatorname{Perm}(a,b,c)}
 x^iy^jz^k(x-y)^2,
 \qquad q_{ijk}>0,
\]

with 24 displayed rational coefficients in
`verify_triangle_sum_r_three_halves.py`.  That verifier derives both
six-state chains and checks the decomposition symbolically.

## Exact `r=2` obstruction for a singular family

Let a unit-weight `K_c` core, `c>=3`, be joined weakly to any fixed number of
disjoint satellite cliques `K_(m_j)`, with arbitrary fixed sizes `m_j>=2`.
Satellite `j` may have an arbitrary positive internal weight `a_j` and an
arbitrary positive attachment scale `b_j`; all its core edges have weight
`epsilon*b_j`.  If `n=c+sum_j m_j`, then

\[
 \limsup_{\epsilon\downarrow0}\rho_{\rm dB}(G_\epsilon,2)
 \le {n-1\over2n}<\rho_{\rm dB}(K_n,2).
\]

The proof in `R2_CORE_PAIR_OBSTRUCTION.md` reduces the rare component changes
to an exact scale tradeoff.  For arbitrary clique sizes, the two directional
rare-event odds have product `16*T_c*T_(m_j)`, where `T_k=2^(k-2)`.  The pair
case is certified by a coefficient-positive polynomial; only three small
size pairs remain, and their exact quadratics have negative discriminants.
This is a broad family theorem, not a universal dB maximizer result.

An apparent positive `c=60`, `q=3` extreme-weight instance was a floating
point artifact: a 608-transient-state exact solve gives excess
`-3.763244026503474e-10`.  The theorem and this exact audit are checked by
`verify_r2_core_pair_obstruction.py`.

## Conditional reduction for arbitrary satellite modules

`R2_ARBITRARY_MODULE_REDUCTION.md` proves that the same suppression theorem
holds for arbitrary fixed weak satellite modules if every module `H` obeys
two explicit stationary invariants.  With vertexwise dB singleton fixation
values `alpha_v` at fitness two and `beta_v` at fitness one half, internal
weighted degree `delta_v`, and

    B = sum_v alpha_v,
    C = sum_v alpha_v/delta_v,
    D = sum_v beta_v/delta_v,

the invariants are

\[
 B\le {|H|\over2},\qquad
 (2B-|H|+1)C\le BD
 \quad\hbox{when }2B-|H|+1>0.
\]

The reduction and its continuous scalar endpoint argument are **PROVED**.
The two module invariants are **OPEN**.  `verify_r2_module_invariants.py`
checks them exactly on 250 rational small graphs; this finite audit is not a
proof.

## Conjectural complementary-level diagnostic

`DUAL_LEVEL_DIAGNOSTIC.md` derives the exact forward-recovery transform.  For
stationary dB-dual level masses `pi_k`, the inequality

\[
 k\pi_k\le(n-k)(r-1)^{2k-n}\pi_{n-k},\qquad k>n/2,
\]

survives every exact test in `verify_dual_level_windmills.py`: all three
certified dB-amplifying windmills at their original fitness and at `r=2`, and
the 66-vertex extreme clique-core instance at `r=2`.  The verifier recovers
the dual masses independently from exact forward orbit values by a triangular
binomial transform.  This is an **EXACT COMPUTATION OF EXAMPLES**, not a proof
of the displayed conjecture.  At `r=2` the conjecture would imply the first
open module invariant `B<=|H|/2`, but not the second degree-weighted one.
The same verifier also checks four open occupied/hole variants with degree and
reciprocal-degree markers on all six windmill cases by exact labelled Möbius
inversion.

## Status of the universal questions

- **PROVED:** `K_n` is not a universal dB maximizer for thresholds
  `r>=3/2`, `r>=7/4`, or `r>=9/5`.
- **OPEN:** whether `K_n` is a universal dB maximizer for every `r>=2`.
- **PROVED FOR A BROAD SINGULAR FAMILY:** weakly attached heterogeneous clique
  satellites around a fixed clique core are dB-suppressing at `r=2` once the
  coupling is sufficiently small.
- **PROVED CONDITIONAL REDUCTION:** the same conclusion holds for arbitrary
  fixed modules subject to the two explicitly stated open module invariants.
- **OPEN DIAGNOSTICS:** the module invariants and complementary-level dual
  inequality have extensive exact finite tests but no universal proof.
- **OPEN:** whether `K_n` universally maximizes `rho_Bd+rho_dB` at
  `r>=3/2`, or even just at `r=3/2` for arbitrary `n`.
- **NUMERICALLY OBSERVED:** no sum counterexample in the finite and lumped
  searches recorded in `RESEARCH_LOG.md`.
- **PROVED FAILED ROUTE:** averaging a graph with a vertex-permuted copy can
  decrease the sum, so direct symmetrization monotonicity is false.

All numerical optimization here is discovery only.  Exact claims are backed
by absorbing-chain or polynomial certificates.

## Programs

- `search_db.py`: cancellation-safe full-subset Bd, dB, and sum search.
- `random_sum_search.py`: broad random sum reconnaissance.
- `search_gadget_sum.py`: separated star-of-gadgets limit search.
- `search_two_class_sum.py`: exact two-count lumping for dense equitable
  two-class graphs.
- `search_windmill_db.py`: exact blade-count dB/Bd evaluation and numerical
  optimization for heterogeneous windmills.
- `search_clique_windmill_db.py`: numerical exact-count search with larger
  clique blades.
- `search_oriented_windmill_db.py`: numerical exact-state search with
  asymmetric two-vertex attachments.
- `search_core_windmill_db.py`: numerical clique-core and pair-satellite
  search.
- `search_block_db.py`: numerical exact-count search over undirected
  equitable block graphs.
- `search_metaclique_db.py`: numerical exact rare-event macro search for a
  network of weakly coupled clique modules with no distinguished core.
- `verify_r_three_halves_counterexample.py`: exact dB counterexample.
- `verify_r_seven_fourths_counterexample.py`: stronger exact dB
  counterexample.
- `verify_r_nine_fifths_counterexample.py`: exact dB counterexample at the
  largest certified fitness in this folder.
- `verify_triangle_sum_r_three_halves.py`: exact triangle sum certificate.
- `verify_r2_core_pair_obstruction.py`: exact polynomial certificate and
  exact audit of the closest numerical false positive at `r=2`.
- `verify_r2_module_invariants.py`: exact finite audit of two open module
  invariants; passing tests are diagnostic only.
- `verify_dual_level_windmills.py`: exact forward-orbit recovery and finite
  tests of the open complementary-level dual inequality.

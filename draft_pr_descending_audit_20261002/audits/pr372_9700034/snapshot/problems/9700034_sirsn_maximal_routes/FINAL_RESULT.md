# SIRSN maximal route integrability: final partial results

**9700034 / AMR-096-0034: proposed original unsolved, 5/5.**
All five substantive author turns are frozen for independent review. The
ordinary SIRSN axioms have not been shown here to imply finite expected
maximum route length, and no genuine SIRSN counterexample has been built.
The partial results below must retain their exact hypotheses. Historical
novelty is unverified.

## Source and target

Aldous's 2012 Open Problem 34 becomes Open Problem 8 in the published 2014
paper, §8.4.3 p.38, with the same request: for independent uniform U_i in the
unit disc, under which additional assumptions, if any, is
E sup_i len R(0,U_i) finite? The route process and endpoints are independent.
The sampled supremum is countable. Prescribed routes are compatible but need
not minimize Euclidean length or satisfy a route-length triangle inequality.
The finite-dimensional measurability setup must not be replaced silently by
a jointly measurable continuum routing map. SOURCE_SCOPE.md and
FINAL_SOURCE_MAP.md record these distinctions and the completed prior gate.

## Five-turn results

1. **Poisson-road model (credited corollary).** Kahn's common travel-time
   diameter and speed-record method give E[M^q]<infinity for every
   q<gamma−1, uniformly over countably many destinations in the unit ball.
   In the plane, every gamma>2 gives the desired first moment. The argument
   uses one common event, rather than a union bound over infinitely many
   endpoints. The independent-increment estimate is unconditional; travel-
   time conditioning is not treated as independent. Kahn's construction
   and main estimates, and the binary hierarchy's known bounded stretch,
   are credited prior results.
2. **FDD increment criterion.** If E|F(u)−F(v)|^p≤C|u−v|^(alpha p) on a fixed
   square, with alpha p>2, dyadic chaining gives a quantitative L^p bound
   for the sampled maximum. The proof works in a countable extension of the
   source FDDs. In particular, an additional route-length triangle inequality
   and a p-th unit-route moment with p>2 suffice. A translated log-log scalar
   field shows the critical L² increment bound alone can fail even with all
   one-point moments. That field is not a SIRSN.
3. **Sampled tail visibility.** For the asymptotic exceedance frequency Q(t),
   the exact maximal tail is P(Q(t)>0), while the marginal tail is E Q(t).
   Explicit deterministic/random lower positive-mass conditions and inverse-
   frequency moments imply integrability. Conversely, the two-route bound
   P(M>t)≥a(t)²/b(t) gives a failure criterion if its integral diverges.
   A scalar mixture with all marginal moments has a finite maximum almost
   surely but infinite mean maximum; it has no claimed SIRSN realization.
4. **Unconditional geometric localization.** The major-road crossing set on
   an outer circle is finite almost surely. Compatibility then makes the
   exterior union a finite collection of finite-length arcs. Hence the whole
   sampled bounded-endpoint family has a finite random confinement radius.
   No integrable exterior bound follows. For annular destinations, the
   entire fixed-root union within radius eta has expected length at most
   3*pi*p(1)*eta. The bounded middle also has finite expected length. Disc
   and annulus integrability are equivalent; only destination-neighborhood
   maxima and the lengths of the finitely many exterior arcs remain.
5. **Mixtures and a genuine family obstruction.** Countable-mixture closure
   makes universal finiteness equivalent to a uniform linear estimate
   H≤C(Delta+p). Actual models with unbounded H/(Delta+p) would yield a valid
   SIRSN counterexample by the explicit mixture weights. Randomly rotated
   affine distortions of any one fixed bounded-stretch SIRSN cannot provide
   that family: transverse route variation forces Delta to grow with the
   same anisotropy as the maximal upper bound. No required unbounded-ratio
   family has been established.

## Exact remaining gap

The packet supplies sufficient conditions and eliminates some failure
mechanisms. It does not prove the needed endpoint visibility, joint increment
control, terminal maximal estimate or exterior first moment from the ordinary
axioms. Almost-sure finiteness of a finite random exterior union is distinct
from its integrability. The valid mixture reduction is not an existence
proof for its unbounded-ratio inputs. The affine no-go constant depends on
the fixed base law and does not prove the universal estimate.

No result for the neighboring traffic or spanning-length problems is counted
again as a new discovery. No scalar obstruction is an original counterexample.
The source's open-ended invitation to state extra assumptions is answered
partially; the possible need for such assumptions remains unresolved.

## Evidence and reproduction

The five checkers have 151,582 + 183,315 + 51,476 + 104,312 + 12,734 =
**503,419 exact finite assertions**. They check algebra, finite compatible
paths, exchangeable laws, projections and mixture weights. They are not
SIRSN simulations or formal verification of the continuum arguments.

Run `python verify_packet.py`; standard Python suffices. An optional
`--source-dir` verifies the four separately held primary-source files
(three PDFs and the maintained HTML page). Raw sources, images and imported
records are excluded from the public packet. All historical proof bytes and
manifests are preserved. The final author manifest binds every public file
except itself. Independent review is pending; no sixth author search follows.

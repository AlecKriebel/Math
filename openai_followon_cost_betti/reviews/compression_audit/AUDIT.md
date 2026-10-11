# Independent audit: compression and deployment

Audit timestamp: 2026-10-06 21:31 PDT (2026-10-07 04:31 UTC).

Reviewer scope: the complete foundational compression and deployment proofs
in family 259, plus the group/action definitions and height upper bound. This
is an automated mathematical audit, not conventional human refereeing or
formal verification. The rank, planar, finite-model transfer, and positive
Bernoulli gap arguments are outside this review's certification scope.

## Exact input and verdict

Read-only source checkout: `/Users/alec/Desktop/math`, commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
The three reviewed source files were clean relative to that commit when
checked. All cited line numbers below refer to those exact files under
`preprints/A-group-without-fixed-price-October-5-2026/build/`.

| Input | SHA-256 |
| --- | --- |
| `compression.tex` | `e50593230e86100c675a8021a1ca3d4f0a1993882815595ba3baaa20c8b70572` |
| `deployment.tex` | `cfcc17cbdc07eae6198351f9ef331c59411e081b6ac91b270f515ef68a800dce` |
| `group-actions.tex` | `7d24f27417d52e5944c8d28bc80cb1b60d3c8fbe1696c58de4c678c605e672b3` |

**Verdict within this scope:** no substantive defect was found in the
compression lemma, the finite-stage deployment proposition, or the height
action upper bound. Their proofs can be reconstructed without accepting the
paper's claimed fixed-price conclusion. These findings do **not** verify
the still separate pivotal assertion `delta_X > 0`.

Strongest audited foundational implication: if `Gamma = A *_J B` is finitely
generated, `J` is infinite, and the action is essentially free p.m.p. on a
standard probability space, then

`Cost(R_Gamma) >= 1 + inf{C(E): E in R_A, R_J vee E = R_A}`.

The proof also symmetrically yields the stronger lower bound with the sum
of the two relative infima, by applying the final normal-form argument to
both factors at each finite stage. That observation is not needed for the
requested follow-on and is not a novelty claim.

Checkpoint estimates: foundational subtask mathematical resolution 100%;
subtask evidence package 100%. These estimates describe only this limited
review, not the root project's mathematical or publication completion.

## Compression: independent reconstruction and attacks

Exact statement (`compression.tex:120–135`): on a finite-measure standard
Borel space with a countable p.m.p. Borel ambient equivalence relation, let
`S subset T subset Q`, with `Q = S vee E` and `C(E) < infinity`.
For every positive error there is `F` inside `Q`, with `Q = T vee F` and
`C(F) <= C(E) - kappa(S) + kappa(T) + error`, where
`kappa(U) = integral 1/|[z]_U| d lambda(z)`.

The following verifies each potentially fragile operation independently.

1. **Borel enumeration and preservation.** Lines 31–42 restrict the ambient
   partial bijections to enumerate each Borel subrelation. A Borel map
   whose graph lies in the ambient relation need not preserve measure if
   it is many-to-one; the source correctly states the preservation claim
   only for partial isomorphisms. Partitioning by the first matching
   ambient index proves that claim. Countable images/saturations and the
   class-size tests are Borel. No uncountable selection is being made.

2. **Finite classes and atoms.** Lines 44–66 choose an order-minimal point
   only from finite classes. The resulting sheets are related by Borel
   partial bijections, so each has equal measure. Thus a transversal has
   measure `integral 1/|class|`. This works on atomic spaces and classes
   of varying finite sizes. An infinite p.m.p. class cannot contain an
   atom of positive measure on a finite-measure space: all class members
   would have the same positive mass. Hence there is no hidden atomic
   obstruction on the infinite-class part.

3. **Exact small complete set.** Lines 79–109 do not seek a Borel
   transversal for infinite classes. A finite partition of the infinite
   part is randomly marked, and the entire uncovered saturation complement
   is added. Every class is met for every marking, including all null
   exceptional classes. For each infinite class, the number of partition
   atoms met tends to infinity, so the expected measure of the uncovered
   part tends to zero. This gives a deterministic marking of small
   measure. The finite part contributes exactly `kappa(T)`. The use of a
   finite random sample does not require a probability measure on any
   uncountable family of Borel choices.

4. **Where contraction takes place.** Lines 139–151 retain all infinite
   `S`-classes and every `S`-class meeting the complete set `M`. Outside
   the resulting `Y`, every `S`-class is finite. For finite retained
   classes, a selected point in `M` gives
   `kappa(S;Y) <= lambda(M)`; infinite retained classes contribute zero.
   The source is not choosing an order-minimal point of an infinite set.

5. **Deleting one edge per excluded class.** Lines 154–196 measure
   distance on the quotient by `S`, with `S`-steps free. A shortest path
   to the `Q`-complete set `Y` exists with finite length. Every excluded
   class chooses one labelled edge leading to strictly smaller distance.
   Borel choice reduces to a least label/direction and a minimum inside
   one finite class. An edge instance cannot be selected in both
   directions, since that would assert both `d(K')=d(K)-1` and
   `d(K)=d(K')-1`. Repeated graphing maps retain separate labels. Thus
   the exact deleted cost is `kappa(S;Z minus Y)`. Directed distances
   also rule out contraction cycles.

6. **The many-to-one map does not create fake savings.** Lines 199–237
   define `f` by finite descending recursion. It is constant on excluded
   `S`-classes and fixes `Y` pointwise; it sends `S`-steps to `S`-steps
   and every deleted edge to a stationary step. The map need not be
   injective. The crucial repair is already present in lines 212–235:
   split each residual domain by two ambient indices, one witnessing
   `f(x)` and one witnessing `f(phi_i(x))`. On each piece the conjugated
   map is a measure-preserving partial bijection of exactly the old
   domain's measure. Overlapping images are counted as separate indexed
   instances. The proof does not equate the measure of the many-to-one
   image with the measure of the old domain.

7. **Recovery of the entire relation.** Lines 242–257 first recover
   `Q|Y` from `S|Y` and the pushed maps, by applying `f` to a finite path.
   Every arbitrary point has a `T`-related representative in `Y` because
   `Y` contains a `T`-complete set. These two end steps recover `Q` on
   all of `Z`. The proof never requires `x T f(x)`, which would generally
   be false. This is an important hidden-assumption attack that fails.

The final accounting at lines 263–269 is then purely additive and uses
the unnormalized measure. When `S=T`, the statement requires no savings.
When `T=Q`, it gives the usual lower bound
`C(E) >= kappa(S)-kappa(Q)`. With `S=id` and infinite `Q`, it gives
`C(E) >= lambda(Z)` (`compression.tex:275–286`). None of these boundary
cases contradicts standard cost.

### Checkable finite boundary artifact

`finite_boundary_check.py` exhaustively reconstructs the actual deletion
and pushforward on equal-weight finite atomic spaces with one through five
points. It enumerates every simple graph and every admissible nested pair
of partitions `S subset T subset Q = S vee E`, then checks:

- selected labelled edges are distinct;
- each deleted edge has equal images under `f`;
- `T vee pushed(E') = Q`;
- the cost identity in atom units is
  `|pushed(E')| = |E| - number(S classes) + number(T classes)`.

Result: **PASS, 329,027 cases**, including two extra cases with loops,
repeated edge instances, and noninjective `f`. The recorded output is
`finite_boundary_results.json`. Run with `python3 finite_boundary_check.py`;
the checked runtime was Python 3.14.6. This computation verifies finite
boundary behavior, not infinite-class/Borel measurability or the full
theorem. The analytic argument above supplies those remaining checks.

## Deployment: exact finite-stage verification

1. **Near-minimal finite graphing** (`deployment.tex:45–68`). Finite
   generation supplies finitely many translations. After splitting a
   near-minimal countable graphing by displacement, a finite initial
   segment misses each fixed translation on a decreasing Borel set of
   measure tending to zero. Adding precisely those missing restrictions
   gives a finite generating graphing within the requested error. There
   is no unjustified assumption that the cost infimum is attained.

2. **Finite unnormalized sheets** (`deployment.tex:70–114`). Each
   translation is written as a finite factor word. Its finitely many
   internal sheets are copies of its original domain. Projection is
   measure-preserving on each individual sheet, not globally. The
   pullback relation is enumerated by sheet-to-sheet maps. A subdivided
   graphing has cost `c + lambda(Z) - 1`, and the join is the full
   pullback relation. These assertions follow by direct finite-path
   reconstruction. The distinction between the original probability
   mass `1` and the enlarged mass `lambda(Z)` is retained throughout.

3. **Monotone relations, nonmonotone edge families**
   (`deployment.tex:119–159`). When factor `i` is processed, putting
   `S_{n+1}=Q_i^n intersect Rbar_J` leaves its `Q_i` relation unchanged
   after compression; the other `Q` grows. Both remain in their factor
   pullbacks and still join to the full relation. Summing the two family
   costs telescopes to `c-1+kappa(S_n)+epsilon`. Each application of
   compression therefore has finite cost. No inclusion among consecutive
   graphing families is asserted or needed.

4. **Exhaustion of `Rbar_J`** (`deployment.tex:167–208`). Every pair in
   a limiting factor relation's intersection with `Rbar_J` enters the
   supplied relation at the next stage of that factor. Thus the two
   intersections are both `S_infinity`. A shortest chain for a
   `Rbar_J` pair alternates factor types. If it has at least two steps,
   any `Rbar_J` step could be recolored and combined with its neighbor,
   shortening the chain. Its projected group word consequently alternates
   outside `J`, while the endpoint displacement belongs to `J`.
   Pointwise freeness and amalgam normal form forbid this. A shortest
   one-step chain lies in the intersection and hence in `S_infinity`.
   The zero-step case is the diagonal. This also handles repeated
   projected vertices: such an adjacent step is automatically in
   `Rbar_J` and cannot survive in a shortest chain of length at least two.

5. **The only limit is numerical** (`deployment.tex:197–208`). Infinitude
   of `J` and freeness imply infinitely many distinct base-sheet points
   in each `Rbar_J`-class. Increasing `S_n`-classes therefore have sizes
   tending to infinity. Dominated convergence on the finite-measure
   enlarged space gives `kappa(S_n) -> 0`. No graphing is obtained by
   taking the limit of the replacement graphings.

6. **Projection at one finite stage** (`deployment.tex:213–252`). Split
   by source and target sheets, so each projected map remains a partial
   bijection of the same domain measure. Supplied edges project to
   `R_J`; all others project to the indicated factor. Once `R_J` is
   supplied to both projected families, their join is `R_Gamma`.
   A shortest projected chain between `A`-related endpoints cannot have
   alternating length at least two outside `J`, because its displacement
   lies in `A`. A single `B`-step between such endpoints lies in `J`.
   Consequently `R_J vee F_A^n = R_A`, precisely the admissibility
   condition in `delta_X`, at every finite stage. The symmetric argument
   also holds for `B`. Taking only the scalar cost limit proves the
   claimed lower bound.

Freeness is essential to this deployment proof. Without it, projected
endpoint relations need not force the chosen displacement product into
`J` or the correct factor. The source explicitly assumes essential
freeness and first restricts to a pointwise-free invariant conull set
(`deployment.tex:10–12,37–40`), so this is an actual checked hypothesis,
not a gap. Ergodicity is not used in either foundational lemma.

## Group/actions and upper bound

The normal-form construction at `group-actions.tex:38–67` gives factor
embeddings and the required reduced-word properties. The free-basis
argument for `J` at lines 69–78 rules out cancellation in the expansion
of a reduced word in `b_i,w`; the embedded `A` shows `Gamma` is infinite.
The displayed 101 generators make `Gamma` finitely generated
(`group-actions.tex:80–83`).

The Bernoulli right action and p.m.p. coordinate permutations are checked
at lines 105–124. For each nonidentity `g`, fixed points lie in the
probability-zero event `x(g)=x(1)`. Countability yields an invariant conull
free set. The homomorphism `chi` is compatible on the amalgamating group,
including `chi(w)=100` (`group-actions.tex:126–157`). Its finite height
extension remains free because its first coordinate is free.

The marker at lines 178–190 includes the entire null collection of
`t`-orbits missing the positive-measure marker. Thus the all-orbit
generation assertion is correct, not merely almost-everywhere. The
commutation path at lines 192–204 supplies every `J` generator everywhere
at cost `1+100p`. Finally, lines 229–250 propagate the initially available
99 consecutive source heights to all remaining heights. The range
`k=0,...,M-100` supplies exactly `99,...,M-1`, including the final
wrap-around endpoint. Consequently the upper bound `1+99/M` holds for
every integer `M>100`.

## Classical source check and attribution boundary

The deployment construction is classical. Gaboriau's original
[2000 paper](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/Cout/Cout.pdf),
§IV.28–IV.32, pp. 67–69, defines the sheet subdivision, its projection,
and its relation on the base sheet. §IV.35 handles bounded-fiber,
finite-measure deployment, and §IV.36–IV.37 develops alternating-color
amalgam arguments in the hyperfinite-amalgam setting. The present source
reconstructs its own relative compression estimate and does not invoke
the hyperfinite-amalgam cost formula for the nonamenable `J` here.

Retrieved source: `sources/gaboriau-2000-cost.pdf`, 433,522 bytes,
SHA-256 `a246ca48536250b18198688d56f0f233db9e0324dbda5a0d339c3294a6b1c19a`.
The accompanying extracted text is a working audit aid. These third-party
working copies should not be included in the final public upload kit
without a redistribution-rights decision.

This audit establishes no historical novelty of the general relative
estimate; it verifies its proof as written. It neither attributes the
fixed-price breakthrough to this follow-on nor certifies the unpublished
positive Bernoulli cost gap by relying on upstream theorem labels.

## Dependencies and exact remaining gap

| Mechanism | Evidence | Status | Exact gap |
| --- | --- | --- | --- |
| Borel finite-class contraction | Complete source proof independently reconstructed; exhaustive finite boundary checks | Audited within scope | No gap found; no formalization reproduced |
| Finite-stage deployment | Exact relation invariants, normal form, finite-stage projection and scalar limit | Audited within scope | Requires free p.m.p. action, infinite `J`, finite generation as stated |
| Height upper bound | Explicit marker path and checked propagation endpoints | Audited within scope | No gap found |
| Positive relative Bernoulli gap | Upstream invokes finite-model/rank/planar mechanisms | Outside this audit | Must independently verify `delta_X >= eta > 0`; foundational lemmas alone cannot yield it |
| Cost–Betti consequence | Classical bridge assigned separately | Outside this audit | Precise inequality/free-action invariance/zero beta_0 still require separate source verification |

No outreach occurred. No source-clone writes, branch changes, Git index
changes, commits, pushes, or release operations occurred in this subtask.

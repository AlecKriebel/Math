# PR239 priority synthesis: adversarial checkpoint review

2026-10-15 UTC. This reviews a research checkpoint. No manuscript exists.
The initial view predates reading the four priority-family reports; the
reviewed current artifacts and source passages are pinned separately.

## Disposition

**The mathematical bridges pass, and the existing literature requires
substantially narrower credit language than “a new general all-scale
mechanism.” Exact scalar-model historical priority remains unresolved.**

I did not authenticate a specific previously published theorem, or a valid
already published theorem-level corollary, which resolves the literal
universal full-law target. This is a scoped finding about the sources and
implications examined, not a guarantee that no such theorem exists. The
unavailable BMP1999/2007 and Conlon–Song1999 originals are specific,
material source holds. Their relevance cannot be dismissed by a missing
search hit, a narrow reading of an inconsistent window description, or a
generic statement that CLTs are weaker.

No mandatory repair to the frozen candidate follows from this synthesis.
The candidate already disclaims novelty. The new audit transfer proves
that its final-segment construction is not necessary for closing its
earlier estimate: an old multiscale method also does so. That reduces the
plausible contribution to an exact model application, quantitative
derivation, and possibly a simpler proof. Priority for those narrower
items is also not certified here.

## Exact target and interpretation

For **each fixed** iid scalar law supported in `(0,1)`, the walk has jumps
`+1,-1` with probabilities `p,1-p`. For every deterministic diverging
equal-interval width `M_N`, every deterministic alignment, and every fixed
`epsilon,K>0`, the target is environmental probability `O(N^(-K))` for a
coarse endpoint L1 discrepancy greater than epsilon. The onset can depend
on the chosen width sequence; law constants need not be uniform near
deterministic arrows. The frozen proof separately covers real common
geometric lengths. No symmetry, uniform ellipticity, or inverse moments
may be silently inserted.

Writing `A(nu)` for that assertion at one law, the literal full-law
extension is `for every nu, A(nu)`. The negation is the existence of a
law for which A fails. A nontrivial earlier law-special A result would be
important context and could refute a stronger informal universal-failure
reading, but would not resolve this literal full-law question. The
deterministic interior law has A trivially and is not a substantive new
resolution. The four inspected families authenticate no nontrivial
law-special exact A result either; inaccessible originals may alter that
assessment.

## Source classifications that survived attempted falsification

| Source/route | What is established | Exact limitation |
|---|---|---|
| BCR2014/2016, Theorem5.1 | Strong coarse error `C M^(-c)+C N^(-c)` with a superpolynomial environment tail; old multiscale closure | Static iid, all-directions uniform ellipticity, dimension at least4 and ballisticity assumptions. The exact directed scalar embedding violates those hypotheses. |
| Peretz2022/2025 | Static low-dimensional invariant-density/local-limit extension and quantitative semi-local comparison | Same all-directions ellipticity mismatch. Its disproved conjecture is a different one. |
| BBDS2024v1/2026v2, Lemma4.1 | The same arbitrary-diverging-width/every-K strength already in a directed one-dimensional dynamic model | Backbone transition field is future dependent, correlated, can have zeros, and has three possible next-layer successors in dimension1. No verified exact scalar iid inclusion. |
| BRAS2005/2006 and RAS2004/2005 | The exact scalar model is included after a parity shear; quenched invariance and replica/Green estimates are real prior ingredients | Inspected statements do not assert the target environmental norm/tail or the quantitative input H. |
| JRS2011/2019 | Exact model inclusion; stationary past density, covariance, particle invariant laws/equilibrium | Column sums and particle equilibrium are different observables from a fixed-start endpoint law. No stated target tail bridge. |
| Recent general-flow, beta and continuum results | Real fluctuation, local-limit or law-special formulas | Inspected stated outputs do not give all microscopic cells with every-K environmental probability at every divergent width. Additional proof cannot be assumed. |
| BMP1999/2007 and Conlon–Song1999 | Highly relevant older leads; BMP's partially accessible survey has a terminal factor and strong quasi-local definition | Complete controlling originals not authenticated in the reviewed cutoff. Hypotheses, region, residual rate and object identification are not excluded. |

The controlling BCR and BBDS theorem statements and models were read
directly in the locally authenticated full primary texts. I independently
retrieved the exact BCRv1, BBDSv1, BRASv2 and JRS-author PDF byte streams
and matched all four hashes. The first availability dates of BCR and
BBDS were independently checked against arXiv histories: 27May2014 and
18October2024, respectively. BBDS's January2026 revision is not the first
appearance of Lemma4.1. The v2 proof clarification should still be cited
when relying on the current result. [BCR history](https://arxiv.org/abs/1405.6819),
[BBDS history](https://arxiv.org/abs/2410.14302).

### BBDS has the full scale/tail strength in its own model

Its deterministic error tends to zero at **every** `M_N->infinity`, and
`exp[-c log^2 N]` is smaller than every fixed `N^(-K)` eventually. If
one conservatively reads its constants only at each fixed M, the
historical family's partition inequality still proves the conclusion:

`L_target <= L_fixed_fine + 2 alpha(split fine cells)`.

Choose a sufficiently large fixed fine width first. Diffusive tightness
and annealed spread make the split-cell mass vanish uniformly in target
alignment as the target width diverges. This avoids an unjustified
M-dependent diagonalization. Thus a slow-scale gap is not an objection
to BBDS's theorem; model inclusion is the actual gap.

The direct BBDS local-kernel rule is uniform on nonempty subsets of the
three successors, and off the backbone is uniform on all three. At any
percolation parameter below1 there is positive probability of a closed
current site, hence all three successors have positive annealed
one-step probability; at parameter1 the kernel is uniform on all three.
An injective per-layer spatial change cannot turn this into two
successors. A noninjective projection or skeleton would require a new
proof of the resulting quenched Markov law and iid scalar environment.
No theorem application is supplied by simply asserting such a map.

### Exact scalar inclusion in BRAS/JRS is successful

`Y_s=(X_s+s)/2` and `r_(s,y)=p_(s,2y-s)` give iid kernels on `{0,1}`.
The index map is bijective on the reachable parity sites; both annealed
jumps have positive probability, so span one holds. Their stochastic
noise condition holds because `E[p(1-p)]>0`. This remains valid for
merely elliptic continuous laws and deterministic interior laws. It
preserves quenched path probabilities exactly. Excluding JRS/RAP by
parity or span would therefore be wrong; the recent lane's resealed
correction is the controlling current assessment.

Original real equal intervals transform to equal real intervals of half
the length. Odd integer counts can alternate by one after the shear;
this is deterministic geometry to check in a cell theorem, not a model
containment obstruction. Source reading: BRAS's model and Lemma4.1,
and JRS's assumptions(1.3)–(1.5), Theorem1.1 and Proposition3.1.
[BRAS dated primary](https://arxiv.org/pdf/math/0507226v2),
[JRS primary](https://www.math.utah.edu/~firas/Papers/walkers.pdf).

## New transfer derivations: independently checked result

`ANALYTIC_TRANSFER_REVIEW.md` provides the full independent bookkeeping.
It checks the actual Freedman denominator at a shrinking threshold, the
high-moment constants when the order grows, sign-test entropy, boundary
expectations, the old-cell replacement, finite-cone coloring, and the
terminal stopping rule. The result is

\[
\mathbb P\{L_{N,M}>CM^{-7/320}+CN^{-1/128}\}
\le C\exp[-c(\log N)^2]
\]

at sufficiently large integer widths and times, for each fixed law. The
derived H uses `gamma=5/16`, `beta=9/32`, `eta=1/64`, `b=1/128`.
The iteration uses `rho=7/8`, with same-parity smoothing exponent `1/7`.
For small segment times its weighted bad-cell concentration has power
`N^(63/256)`. In particular its failure probability remains a function
of N rather than deteriorating to a tail in M. The desired all-scale
quantifiers follow without any lower growth rate for M.

The audit's old-method transfer is therefore a complete present proof
route, not a restatement of an unsupported equivalent. The **historical
inference** remains blocked at a dated scalar quantitative comparison or
a genuinely general published theorem accepting the needed elementary
inputs. BRAS's cumulative Green estimate plus first hitting gives the
conditional occupation bound; ordered expansion gives its Kac moments.
The rest of H is now explicitly derived. A proof assembled now from
old tools does not authenticate an old publication of that application.
Calling H “new” merely because no match was found would be equally
unjustified.

I identified a small generic-exponent exposition point: the bridge proof
caps `b_1` at `1/8`, so its directly stated sufficient exponent should
also expose that cap. The clarification is now made. I checked the
complete diff, the old 10-entry seal preserved byte for byte, and the
new 23-entry seal. The numerical rate above is unaffected.
`FINAL_RESEAL_CHECK.json` records the completed verification.

## Quasi-local positive implication and its genuine residual gap

The new quasi-local stationary-factor argument passes independently.
Uniform cylinder oscillation on a finite alphabet forces essential
boundedness. A fixed cylinder approximation radius depending only on
epsilon produces finite-range dependent bounded terminal factors.
Weighted bounded differences yields an `exp[-c_epsilon sqrt(N)]` tail,
because the sum of squared coordinate effects is `O(N^(-1/2))`.
The expected coarse norm vanishes at every divergent width. It is
incorrect to insist that this part requires a growing approximation
radius or a specified rate of oscillation decay.

That positive argument concerns the stationary factor only. To transfer
a local limit `mu_N=b_N Phi+r_N`, the coarse or total residual still
needs every-K environmental probability control (or a sufficient
deterministic uniform error). An a.s. or L2 o(1) does not give it.
The BMP survey's normalized and unnormalized window descriptions do
not agree, and the broad normalized reading contains the diffusive
bulk. Thus a narrow-window exclusion of BMP is not justified.

The unbounded-density caution also passes. For a fixed two-atom
uniformly elliptic scalar law, positive finite-cone inward-funnel events
make the JRS finite-past density martingale arbitrarily large. Its L2
limit cannot be essentially bounded. A literally uniform finite-state
quasi-local Phi is bounded and cannot automatically be identified with
that density. This does not prove that BMP is false, or that BMP uses
the same object and hypotheses. It makes the original definitions and
identification more necessary, not less.

## Remaining actionable work versus unavoidable search limits

The following are concrete unresolved checks, rather than an expectation
of infinite literature search:

1. Authenticate BMP1999's complete theorem and proof, and the complete
   relevant BMP2007 survey section. Determine the actual model/law
   assumptions, the normalized spatial region, quantifier uniformity,
   local-limit residual mode/rate, and meaning of quasi-concentration.
   If a uniform residual is available over the bulk, complete the
   positive quasi-local bridge and classify its law coverage.
2. Authenticate Conlon–Song1999's controlling theorem/proof, rather than
   relying on its title or later descriptions. Check exact environment
   restrictions, any small-disorder restriction, averaging/local-limit
   object, environmental tail, and the full-law versus law-special
   distinction. Its separate archival lane should be read when ready.
3. Compare any obtained older quantitative scalar estimate with H.
   An earlier genuine H, or a stronger sufficient residual theorem,
   combined with the established closure could settle earlier theorem
   coverage. If none occurs in those originals, record their exact
   exclusion and move on; do not replace it with a global novelty claim.

These missing originals remain material for a definitive priority
disposition or a novelty-focused manuscript narrative. They do not
invalidate the separately checked candidate mathematics, and they do
not prevent an explicitly qualified research checkpoint from recording
what is proved and what is still being checked. Parent directions
govern any actual publication; this reviewer performed none.

Even complete resolution of these source forks would not prove global
novelty. Bounded searches cannot exclude every unindexed thesis,
non-English paper, unnoticed corollary or unpublished proof. That is a
permanent evidentiary limit, unlike the named originals currently being
pursued. No person was contacted and no outreach was prepared.

## Credit and wording if a manuscript is later prepared

No manuscript text is being reviewed or created here. Before a paper
could make a reviewable priority assertion, its author should:

- Credit BCR's 2014 Theorem5.1 and the BBDS2021/2023 bad-box method;
  identify BBDS2024 Lemma4.1 as an existing same-strength one-dimensional
  dynamic-environment result. Cite the current revision too. Do not
  call the general all-scale bootstrap a new mechanism or say all
  previous one-dimensional results stop at polynomial widths.
- State the exact scalar iid theorem and explain the model differences.
  Describe the one-final-segment proof as a proof in this setting;
  priority for that particular simplification has not been established.
- Credit the BRAS replica/Green-function input and JRS density picture
  with successful exact shear inclusion. Do not retain the superseded
  span/parity exclusion. Same-parity gradients are essential in the
  original coordinate.
- Distinguish the printed conjecture's mathematical negation from
  historical claims such as “first resolution,” “remained open,” or
  “previous methods cannot reach this scale.” Those historical claims
  are not cleared by this audit.
- Preserve the specific unresolved BMP/Conlon source questions until
  answered. Do not present a missing original or a search log as
  evidence that an earlier theorem is absent.

A currently supportable research-note statement is that the exact
full-law positive theorem has a checked proof, its general ingredients
and all-scale methodology have established precedents, and no earlier
complete scalar-model theorem has yet been authenticated in this audit.
That statement asserts no invented guarantee of novelty.

## Evidence and scope of completion

All four current family manifests passed independent byte/hash checks;
the recent lane's read-only verifier also passed its 90 private evidence
pins, 18 search receipts, 67 queries and preserved historical seal.
My separate exact controls passed 13,328 assertions covering path shear,
the arbitrary-partition inequality, finite-cone coloring, the weighted
convolution bound, inward-funnel identities, parity negative controls
and the rational exponent margins. Their finite scope is explicit;
analytic deductions establish the limiting statements.

The authored manifest excludes all full third-party sources and raw
provider outputs. Only this assigned folder was written. No Git,
index, ref, provider, other-chat or external-person mutation was made.
This synthesis is complete at **100% of its assigned checkpoint
review**, including the final repair and reseal check;
historical priority and overall research discovery completion are not
being assigned 100%.

## Sanitation-only reseal after completion

At 2026-10-15 05:02 UTC I independently checked the local-limit lane's
sanitation revision. Its original 28-entry authored set and manifest are
preserved privately and match the preceding recorded seal. The only
authored payload changes are removal of the query from the single
challenge URL in `BMP_FAILED_ROUTES.json[0].error` and an appended log
entry. All other values in that JSON and every scientific artifact are
byte-identical. The manifest adds sanitation metadata and updates its
timestamp and the two changed file pins. The current local manifest still
has 28 entries; its SHA256 is
`23523ea977f25bbb02f4b8add1f6502317f570d5bf52b0e8f9f00d10b0443259`.

I preserved this synthesis's preceding complete public-safe seal byte for
byte under `revision_history/completed_seal_20261015T0452Z/`, including its
13 authored artifacts, manifest and checksum. Current input pins and
actual controls were refreshed, retaining **13,328** exact assertions.
`SANITATION_ONLY_REVIEW.json` records the independent comparison, and the
offline verifier repeats it without printing or copying the removed query.
No source was acquired and no scientific finding or priority verdict changed.

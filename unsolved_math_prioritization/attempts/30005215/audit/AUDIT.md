# Independent adversarial audit: asymmetric black-box operator norms

Problem ID **30005215**, code **OWR-11101919-002**, rank **562**. Reviewed
2026-10-04 UTC.

## Verdict

**PASS for the explicitly stated finite-dimensional, exact-oracle theorem.**
No blocking mathematical defect was found in the frozen packet's compact-plane
algorithm or its uniform-cap convergence proof. The recommended queue outcome
is **`already_solved`, `1/5`**, crediting Bresch, Lorenz, Schneppe, and Winkler,
without a novelty claim.

This verdict is deliberately narrower than a certification of every formula or
proof in the cited papers. Two claims in the inspected mismatch preprint fail,
as the packet already discloses. The packet gives an independent proof of an
appropriately completed compact-plane algorithm; that proof does not rely on
those claims. The result is almost-sure convergence of norm estimates, with
constant-vector storage. It is not a deterministic finite-time norm certificate,
a floating-point stability theorem, an infinite-dimensional theorem, or a proof
for every stochastic-gradient step-size schedule suggested in the original
report. Those distinctions are already explicit and need no blocking edit.

## 1. Frozen evidence and review scope

The reviewed `FROZEN_MANIFEST.json` has SHA-256

    ff6821bf7d014912220011b4e24ea9faff96e9e9f53d68c1293154c166d2d660

All eight listed public files match their recorded byte counts and SHA-256
hashes. The three source PDFs match the public source manifest. The source
identities, dates, and version numbers were independently checked against the
publisher and arXiv pages. The original contribution and the relevant theorem
and algorithm passages were read. Printed OWR p.2251 and mismatch p.12 were
also visually inspected.

The frozen public files were not changed. All new review artifacts are in this
separate audit directory. No remote publication or repository mutation was
performed by this review. The archived `independent_review: pending` field is
part of the preserved pre-review snapshot; this document records the completed
review against its exact hash.

## 2. Does the theorem answer the actual question?

The OWR contribution motivates norm computation through optimization step-size
conditions. Its numerical question supplies evaluations of A, but no A-adjoint,
and separately asks for the norm of A−V given A and V-adjoint. It rules out
large sketches because too many stored vectors are unavailable. It discusses a
monotone stochastic ascent idea and asks for a full convergence argument. The
next page supplies the bilinear characterization used in this packet. These
points were checked in the actual contribution, rather than inferred from a
catalogue paraphrase. [Original report](https://ems.press/journals/owr/articles/11101919)

The report begins in Hilbert-space optimization, without a separate universal
infinite-dimensional algorithmic specification. Both later papers explicitly
formulate the numerical oracle problem in finite-dimensional real Hilbert
spaces. The packet transparently adopts that formulation and does not silently
claim the more general setting. Its fixed-vector-memory and incremental-value
requirements match the papers' model.

The source's step-size motivation does not turn a lower estimate into a safe
upper bound. In particular, using a lower estimate in a reciprocal step-size
bound can permit an unsafe step. The packet warns about this. Neither the
original question nor the packet supplies a deterministic stopping certificate,
precision model, or dimension-independent complexity target. It would be
incorrect to advertise those as established outcomes.

## 3. Oracle legality, work, and memory

For u in the output space and v in the input space, the available identity is

    b(u,v) = <u, Av> − <Vᵀu, v> = <u, (A−V)v>.

This uses exactly the two allowed black boxes. No evaluation of Aᵀ, V, B=A−V,
or Bᵀ is hidden in the update. B and an optimal singular pair occur only in the
analysis. With U=[u,w] and Q=[v,x], all entries of C=UᵀBQ are computable from
Av, Ax, Vᵀu, and Vᵀw. The update's cached images remain correct by linearity.

After initialization, an iteration requires one new A call if d>1 and one new
Vᵀ call if m>1. Over N iterations the exact counts are

    A calls:   1 + N·1_(d>1)
    Vᵀ calls:  1 + N·1_(m>1).

For a dimension-one side, the corresponding tangent query is omitted. The
single-operator specialization uses one initial A evaluation and at most one
new A evaluation per iteration. Besides oracle work, each iteration has
O(d+m) vector arithmetic and constant-size spectral algebra. Its storage is a
constant number of input/output vectors plus an at-most-2-by-2 matrix:
O(d+m)=O(max(d,m)). It neither assembles the operator nor retains a growing
history or sketch.

The test fixture stores dense matrices to supply and independently check the
oracles. Those matrices are not inspected by the tested estimator. That is an
appropriate test harness, not an illicit query in the proposed method.

## 4. Compact maximization and exceptional cases

Because U and Q have orthonormal columns,

    max pᵀCq = ||C||₂

for unit coefficient vectors p,q, and the corresponding Up,Qq are feasible
unit vectors in the sampled planes. The old pair remains feasible; changing
its initial sign makes the starting value nonnegative. Hence, in exact
arithmetic,

    0 ≤ s_k ≤ s_(k+1) ≤ ||B||₂.

The compact domain is important. A maximizer can occur at a plane direction
whose tangent-chart slope is infinite. A denominator formula can fail there;
the SVD update does not. This also avoids division by a projected determinant
or cross coefficient.

The stated tie rule is measurable. For the at-most-2-by-2 positive semidefinite
matrix H=CᵀC, its top spectral projector is Borel measurable: on a simple-eigenvalue
stratum it is obtained from the eigenvalues and H, while on the repeated
stratum the top eigenspace is the full coefficient space. Selecting the first
coordinate with a nonzero projected component and normalizing gives a Borel
unit eigenvector. For positive norm, p=Cq/||C|| has unit length; at C=0 the
fixed first-coordinate choices are valid. There is no unprovided random tie
selection.

The following cases are therefore covered analytically:

- B=0: every value is zero and every compact maximization exists.
- Rank one: projected 2-by-2 determinants may vanish identically; the SVD
  maximum still exists.
- Repeated maximal singular values: neither uniqueness nor a spectral gap is
  used. Only the value is claimed to converge.
- Nonglobal stationary or null starting vectors: the uniform success bound
  below applies to these states too.
- m=1 or d=1: that side is already its complete ambient line; its approximation
  probability is one. For a scalar operator the first compact update gives the
  exact absolute value; initialization already has that value after sign choice.
- A zero-dimensional side: the stipulated zero return is valid under the usual
  zero-operator norm convention; the positive-dimensional construction is not
  invoked.

## 5. Uniform caps, adaptive iterates, and convergence

Fix a target unit vector t and an arbitrary current unit vector a. Write

    t = αa + βz,   β≥0,   z in a-perpendicular when β>0.

For a unit tangent sample X, the candidate t′=αa+βX has unit length, belongs to
the sampled plane, and satisfies ||t′−t||=β||X−z||. When β=0 the target is
already in the plane. Thus a radius-δ tangent cap supplies a feasible target
approximation with probability bounded below independently of the current
state and the target. This includes targets arbitrarily close to either pole;
there is no worsening factor 1/β.

For n=2 the tangent sphere is S⁰ and a cap of radius δ<1 has mass 1/2. Both
choices actually generate the same full plane, so this lower bound is merely
conservative. For n=1 the packet correctly defines the success probability to
be one. In higher finite dimension an open tangent cap has strictly positive
surface measure. For clarity, if θ=2 asin(δ/2), then for n≥3 its mass can be
written as

    p_n(δ) = (1/2) I_(sin²θ)((n−2)/2, 1/2).

The proof needs only positivity. These constants deteriorate with dimension;
no dimension-independent practical rate follows.

Now fix a maximizing singular pair (r,t) of the fixed matrix B and put
M=||B||₂>0. Compactness supplies such a pair even with repeated singular values.
Conditional on the full history, the two freshly sampled tangent directions
are independent, with their correct current-state uniform laws. Therefore both
planes approximate their respective fixed targets to δ with conditional
probability at least

    p = p_m(δ) p_d(δ) > 0.

On this favorable event their feasible pair has bilinear value at least
M(1−2δ). The chosen SVD maximizer need not itself fall inside the target caps;
its value is at least that feasible value. This objective comparison is the
correct argument and avoids an unsupported assertion about the selected
vectors' locations.

With δ=ε/4 and E_k={s_k<M(1−ε)}, monotonicity gives nested failure events and

    P(E_(k+1) | history through k) ≤ (1−p) 1_(E_k).

The factor is 1−p_m p_d. Conditional independence of the fresh directions does
not imply independence of the iterates, and none is required. Taking
expectations yields P(E_N)≤(1−p)^N. Continuity from above shows eventual
attainment of each prescribed relative threshold with probability one; a
countable intersection over ε=1/j gives s_k→M almost surely. M=0 is separate
and immediate.

This is a complete global-value convergence argument. It neither stops at
“a monotone bounded sequence has a limit” nor relies on unproved avoidance of
all nonglobal stationary points. For each fixed ε and dimension it even gives
a conservative tail bound on the number of iterations. That bound is
probabilistic, and it supplies no deterministic observable test proving exact
convergence on a particular run. The algorithm itself requires no knowledge
of M, the target pair, or these cap probabilities.

The one-oracle Gram-matrix specialization has the same argument with one
cap: ||At′||≥||A||(1−δ). It uses no unavailable adjoint.

## 6. Prior work, the two cautions, and attribution

The first cited paper explicitly treats the forward-only finite-dimensional
norm problem; its Theorem 2.19 states almost-sure norm convergence. The
second explicitly treats the A/Vᵀ model and states the corresponding result
in Theorem 2.26. Their dates and authors match the packet. These are direct
prior matches, not keyword-only references. [Forward-only paper, v3](https://arxiv.org/abs/2410.08297v3),
[mismatch paper, v2](https://arxiv.org/abs/2503.21361v2).

The mismatch v2 cautions are real:

1. Proposition 2.11 asserts nonzero projected determinant under a non-singular-
   pair hypothesis. For B=rsᵀ, however, C=(Uᵀr)(sᵀQ) has rank at most one for
   every sampled plane pair. Its determinant vanishes identically. The explicit
   rational example with B=diag(1,0,0) and u=v=(3/5,4/5,0) is not a singular
   pair; its projected entries are 9/25, −12/25, −12/25, 16/25. Thus the example
   obeys the relevant exclusion and invalidates the claimed nonvanishing.
2. In the Theorem 2.26 proof, the complement of simultaneous success is bounded
   by a product of marginal failures. A complement of a product event is a
   union, not an intersection. Independent success probabilities p and q
   supply a failure probability 1−pq, not (1−p)(1−q). Optimized update
   coordinates also need not be independent merely because the direction
   samples are independent. [Mismatch v2, pp.12, 19–21](https://arxiv.org/pdf/2503.21361v2)

Neither defect disproves the desired existence theorem. Nor may a reviewer
silently certify the original printed formulas in all degenerate cases. The
packet's compact maximization removes the first dependency; the direct
conditional feasible-value bound removes the second. Credit to the earlier
random-search methods and their stated resolution is appropriate, while the
present robust formulation and self-contained justification must remain
visible. The packet already does this and explicitly makes no novelty claim.
No unseen publisher revision is certified by this audit.

## 7. Reproduction and additional checks

The frozen verifier was replayed with its given seeds. Its output is
**byte-for-byte identical** to `checks.json`:

- 600 exact rational identities, comprising 300 oracle identities and 300
  rank-one determinant identities, plus the explicit rational example;
- 600 floating-point geometric identities;
- 11 numerical matrix cases, each with 600 iterations, including all advertised
  shapes and degeneracies, with the recorded oracle counts.

The zero-mismatch floating-point result is about 6.47×10⁻¹⁵ rather than exact
zero. It passes a declared roundoff tolerance. This confirms that the numerical
run is a smoke test, not an implementation-level proof of exact lower bounds.
The manuscript makes that distinction correctly.

The independently written `adversarial_checks.py` additionally passes:

- the exact rank-one source counterexample, including the non-singular-initial-
  pair hypothesis;
- eight compact-update boundary cases: zero, nonglobal stationary, null
  stationary, repeated top singular value, negative scalar, one output,
  one input, and rank one;
- 400 plane-identity boundary cases, including both poles, near-poles, and
  orthogonal targets in dimensions 2, 3, 8, and 31;
- an exact event-algebra counterexample to the product-of-failures bound.

These finite checks validate algebra, selected edge cases, and reproducibility.
The analytic argument above establishes convergence. No amount of finite
sampling would substitute for that argument.

## 8. Publication recommendation and limits

No blocking correction is requested. Preserve the finite-dimensional/exact-
oracle scope, lower-estimate warning, source-proof cautions, prior-author
credit, and no-novelty statement. The suggested `already_solved`, `1/5`
classification is supported on that basis, rather than by unquestioning
acceptance of the preprint's problematic proof steps.

This review does not independently certify every historical repository search
in `SOURCE_GATE.md`, future performance, floating-point stability, singular-
vector convergence, or unseen publication revisions. Those are not needed for
the stated theorem. Downloaded source documents, extracted text, catalogue
records, and unrelated material are excluded from the audit deliverables.

## Audit files

- `AUDIT.md`: this mathematical and source-matching review
- `integrity_checks.json`: frozen-file and source-PDF integrity results
- `replayed_checks.json`: unchanged verifier's independent replay
- `adversarial_checks.py`: additional reproducible finite checks
- `adversarial_results.json`: their output
- `VERDICT.json`: concise machine-readable conclusion
- `AUDIT_MANIFEST.json`: hashes of the audit deliverables, excluding itself

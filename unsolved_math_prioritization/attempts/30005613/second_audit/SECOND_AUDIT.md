# Second adversarial review of the quasiconical pure point construction

Problem 30005613, OWR-14297736-021, rank 800. Reviewed 5 October 2026.

## Verdict

PASS for the full existential theorem in the frozen PROOF.md. No unresolved
mathematical gap was found in the finite-window argument, preservation of
multiple spectral clusters, common Hilbert space construction, infinite
exhaustion, fixed-rank limits, or eigenbasis completeness. No correction to
the frozen proof is required.

The accepted conclusion is that, for every integer d >= 2, some connected
open quasiconical tower of expanding cubes with positive windows tending
to zero has a Dirichlet Laplacian with a complete orthonormal eigenbasis,
spectrum and essential spectrum both [0,infinity), and no absolutely
continuous or singular continuous spectral subspace. Zero is not an
eigenvalue. Both cube widths and window widths are chosen inductively.

This is an adversarial mathematical AI review. It is not a formal proof
certificate, human peer review, historical novelty determination, or
editorial acceptance. The scope excludes prescribed arbitrary cube widths,
Neumann conditions, smooth boundaries, and positive-length connecting
passages. These exclusions already appear in the candidate.

## Reviewed objects and independence

The original proof was read in full before the first audit was consulted.
The second review then checked the earlier analytic reconstruction against
the proof and the relevant already available source material. Neither
frozen input nor its local extracted files was changed.

- Author archive: QUASICONICAL_30005613_AUTHOR_SAFE_FREEZE.zip, 16,490 bytes,
  SHA-256 2d15c0f1f7b094c92bafb6d2fed6d3b212c597adf9043c9f49c737a6f082e09e.
- Original PROOF.md: 14,044 bytes,
  SHA-256 5d1bab0b62ac5f78c69b0d82babd0b79fa4944097470fa760fdb3c485e362a20.
- First audit archive: QUASICONICAL_30005613_INDEPENDENT_AUDIT_SAFE_FREEZE.zip,
  45,053 bytes,
  SHA-256 64bf89900a083fbc41176efd9766fde3a64397a5850207ce8e190eebbcdae6ea.
- First AUDIT.md: 13,677 bytes,
  SHA-256 7bc157b9fa10242967cfa0910fea00ce69cd9c03a2e086431c3a6d0cbcb5e043.
- First ANALYTIC_CHECKS.md: 12,092 bytes,
  SHA-256 968921d47a78d862ea7cfa4479bb5f3713df03653a8bafc779ab8598ebb83e5e.

All eight author archive entries and all seventeen first-audit archive
entries matched their extracted local files. Both archive manifests,
complete member sets, and CRC checks passed. The embedded author snapshot
in the first audit was byte-identical to the original eight-entry archive.

This review used the existing mathematical candidate and local sources.
It did not initiate another research approach, a literature search, a
repository-state search, or any remote write. It makes no fresh claim about
current manuscript status, priority, or repository publication status.

## The finite-window limit

PROOF.md Sections 2 and 3, especially lines 41-83, survive the following
independent reconstruction. Fix one finite old stage and the proposed next
cube. The old windows stay fixed. Write D0 for the disconnected union and
D_delta for the result of opening only the new window around p.

The two adjacent cubes occupy opposite sides of their contact plane.
Because delta < a_n < a_{n+1}, every point of the new window cube off that
plane already belongs to one of the cube interiors. Consequently
D_delta differs from D0 only by a relatively open piece of that plane.
This is a null change for L2 but need not be a null change for H01.
The argument correctly keeps those two facts separate.

Put all form domains in H01(B), by zero extension, for one bounded box B
containing this finite geometry. The spaces V_delta = H01(D_delta)
decrease as delta decreases, and V0 is contained in each of them. Their
intersection is V0. One way to see the last assertion is the
quasicontinuous characterization of H01: along a countable decreasing
sequence delta_m -> 0, a member of every V_delta_m vanishes quasi-everywhere
outside their intersection. The intersection of the underlying sets is
D0 union {p}. A single point has zero H1 capacity when d >= 2, so it cannot
relax this zero-boundary condition. This argument uses countable unions of
capacity-zero exceptional sets and does not require a regular slit boundary.

The dimension-two endpoint is important. For 0 < r < 1, a cutoff equal to
zero on the disk of radius r^2, equal to one outside the disk of radius r,
and equal to log(rho/r^2)/log(1/r) in between satisfies

    integral |gradient eta_r|^2 = 2*pi/log(1/r) -> 0,
    integral |1-eta_r|^2 <= pi*r^2 -> 0.

For d >= 3, the usual cutoff changing over radii r to 2r has gradient
energy O(r^(d-2)) and L2 error O(r^d). Thus the claimed removable point
condition holds in every claimed dimension. A rescaled linear cutoff in
dimension two would not prove it. No dimension-one extension is justified.

The same conclusion can be formulated without quasicontinuity. Multiplying
a weak H1 limit by a cutoff avoiding p puts it in V0, because eventually
all added windows lie where the cutoff is zero. Bounded Sobolev truncation,
the capacity cutoffs above, and closedness of V0 remove the cutoff. This
supplies the Mosco lower condition; V0 subset V_delta supplies the recovery
condition. The first audit's ANALYTIC_CHECKS.md Sections 1 and 2 carry out
this alternative correctly.

Norm convergence, rather than merely strong convergence, follows because
this fixed finite stage sits in a bounded box. If it failed, choose
delta_m -> 0 and unit-bounded f_m with the resolvent differences bounded
away from zero. Passing to a subsequence gives f_m weakly convergent to f.
The solutions u_m = (A_D_delta_m+1)^(-1)f_m are bounded in H01(B), hence
have a subsequence convergent strongly in L2 and weakly in H1. The preceding
lower condition places its limit in V0. Testing against V0 identifies that
limit as (A_D0+1)^(-1)f. Compactness of the latter resolvent also makes its
values on f_m converge strongly to that same limit, a contradiction.

This proof treats all sufficiently small positive delta, including
nonmonotone sequences, and arbitrary fixed earlier apertures. It verifies
the exact finite-window norm-resolvent input the candidate needs.

## Multiplicity and finite constraints

PROOF.md Sections 2-4 use full eigenspaces, not distinguished eigenvectors.
Once the old stage is fixed, its protected spectral set S_n is finite and
positive. For a next width in the bounded interval (a_n+1,a_n+2), the cube
eigenvalue formula bounds all positive integer multi-indices that could
resonate with any lambda in S_n. Only finitely many widths are excluded.
There is no circular dependence: the old spectrum is fixed first, the
nonresonant new width is fixed second, and the aperture is chosen last.

Nonresonance makes an old protected eigenspace exactly the corresponding
eigenspace of the disconnected enlarged domain, extended by zero. Because
this domain is bounded, that eigenvalue is isolated with finite
multiplicity. Under t -> 1/(1+t), its resolvent eigenvalue is isolated and
nonzero. Small contours can therefore be chosen away from the rest of the
compact resolvent spectrum, including zero. The resolvent identity and
Neumann inversion on those contours give norm-convergent Riesz projections.

An old repeated eigenvalue may split. Its whole cluster still has the old
rank and contains complete eigenspaces of the new stage. Distinct old
clusters use disjoint intervals, so they cannot collide across the chosen
interval boundaries. Since each smaller protected projection selects a
subset of the same family of complete clusters, nesting persists.

At each step there are finitely many protected projections. Thus one
positive aperture can meet every required norm bound, as well as the
positive geometric upper bound. Its size need not be computable, and the
spectral gaps need not have a uniform lower bound. A sufficiently high new
finite spectral cutoff includes all transported clusters and approximates
the finite current test set. Future transport need not preserve its
low-energy-cutoff form. All these distinctions are explicit in the proof.

For completeness, if orthogonal projections P,Q have norm distance below
one, Q restricted to range(P) is injective, and P restricted to range(Q) is
injective. When one rank is finite these two facts imply equal finite ranks.
This applies both to finite-stage transport and the eventual norm limits.

## Geometry and the common Hilbert space

The cubes have disjoint interiors and successive closures meet along the
intended face. The new window cube intersects both adjacent interiors, so
each finite stage is open and connected. Their increasing union is open
and connected. The cube half-widths increase by more than one, so the union
contains balls of arbitrarily large radius.

Outside the cube interiors the union contains only countably many pieces
of contact hyperplanes. They have zero d-dimensional volume. Therefore
the final L2 space really is the Hilbert direct sum of the cube L2 spaces.
There is no additional L2 component located on the windows. Each cube sine
basis is fixed when that cube is chosen and remains fixed afterward.

Every earlier finite-stage operator or projection can be extended by zero
on future cube summands without altering its norm or finite rank. This
common Hilbert space may be identified after the entire geometry has been
chosen; the earlier estimates remain valid under its canonical embeddings.
The cube sine functions are used only as L2 test vectors. The proof does
not assume they are eigenvectors of the connected final Laplacian.

## Infinite exhaustion uses strong convergence

PROOF.md Section 5 correctly uses a different convergence statement from
the finite-window argument. Set V = H01(O), with form inner product
b(u,v) = integral (gradient u dot conjugate(gradient v) + u conjugate(v)).
The zero-extended V_n = H01(O_n) are closed increasing subspaces of V.
Their union is dense because a compact subset of an increasing open cover
lies in one finite member, and compactly supported smooth functions define
H01(O).

For each f in H, R_n f is the b-orthogonal projection of Rf onto V_n.
Consequently R_n f -> Rf in the form norm and in H, with norm(R_n) <= 1.
Here R_n is a bounded self-adjoint zero-extended finite-stage resolvent.
It has a kernel on future cubes and is not itself the resolvent of a
densely defined self-adjoint operator on the whole final H. The proof
never requires that false identification.

Indeed, norm convergence of the infinite exhaustion is impossible here.
For a fixed n, use normalized smooth cutoffs supported in much later large
cubes, with norm(Au_j) -> 0. Then R_n u_j = 0 and
Ru_j-u_j = -R A u_j -> 0. Thus norm(R-R_n) >= 1; since both operators are
positive contractions their self-adjoint difference has norm at most one.
So norm(R-R_n) = 1 for each n. This reinforces why only strong convergence
can be used at this step, and the candidate does exactly that.

## Fixed-rank limits yield genuine eigenvectors

For each fixed birth index k, the transport estimates imply

    norm(P_m^k-P_n^k) <= sum from j=n to m-1 of 2^(-j-2),
    norm(P^k-P_n^k) <= 2^(-n-1),                    n >= k.

Norm continuity of adjoints and products makes P^k an orthogonal projection.
The rank comparison above gives its original finite rank. Taking limits
of P_n^k P_n^(k+1) = P_n^k preserves nesting. This would fail for strong
projection convergence alone, but the proof has norm convergence.

For each fixed f and k, both commutation limits are justified by

    norm(R_n P_n^k f-R P^k f)
      <= norm(P_n^k-P^k) norm(f) + norm((R_n-R)P^k f),

    norm(P_n^k R_n f-P^k R f)
      <= norm(P_n^k-P^k) norm(R_n f) + norm(P^k(R_n-R)f).

Both right sides tend to zero, so P^k commutes with R. No unbounded
operator commutator or norm convergence of R_n is used. Its range is
finite-dimensional and reducing for the positive injective resolvent R.
The restricted operator has strictly positive eigenvalues mu. If
Rv = mu*v there, then v = mu^(-1)Rv lies in dom(A) and
Av = (mu^(-1)-1)v. Every vector in this range is therefore in H_pp(A).

No uniform positive lower bound on mu across all k is needed. The
finite-dimensional assertion for each fixed k excludes an individual
protected space disappearing to infinite energy.

## The completeness diagonal closes the continuous-spectrum gap

This is the decisive check. Fix any cube-basis vector f_(j,l). It belongs
to F_n for every n >= max(j,l), not merely at its first appearance. Its
birth-stage approximation at each such n satisfies

    norm((I-P_n^n)f_(j,l)) < 2^(-n).

Apply the uniform tail formula to the entire trajectory born at that n:

    norm(P^n-P_n^n) <= 2^(-n-1).

Therefore

    norm((I-P^n)f_(j,l)) < 3*2^(-n-1) -> 0.

This diagonal use of k=n is legitimate. For each n the trajectory is
already defined for all future stages, and its tail bound is explicit
and independent of k. It is not an exchange of a nonuniform pointwise
limit with a moving index. Reapproximating the same test vector at later
births is essential: its error and its entire later perturbation tail
both tend to zero.

Each P^n f_(j,l) is in the closed span of actual eigenvectors of A. Hence
that closed span contains every cube-basis vector and equals H. This
eliminates both continuous spectral subspaces, including a possible
singular-continuous orthogonal complement. No trace-class theorem is
being asked to eliminate singular-continuous spectrum, and the existence
of dense point spectrum alone is not used as a substitute for completeness.

Equivalently P^k -> I strongly. The finite-dimensional orthogonal
differences of successive nested ranges reduce R; diagonalizing on them
gives a complete orthonormal eigenbasis of A. The limiting P^k need not be
full spectral projections of A, and the argument does not require them to
be. Commutation and finite-dimensionality are sufficient.

## Spectrum as a set and the endpoint

The scaled, compactly supported plane waves in PROOF.md Section 8 lie in
dom(A), even though the boundary is irregular. Their residual bound is
the direct product-rule estimate

    norm((A-lambda)u_n)
      <= r_n^(-2) norm(Delta chi)
         + 2*sqrt(lambda)*r_n^(-1) norm(gradient chi) -> 0.

Their supports lie in distinct cubes, so the unit vectors are orthogonal
and weakly zero. Weyl's criterion gives every lambda >= 0 in essential
spectrum. Nonnegativity gives the converse. Completeness then identifies
the spectral set with the closure of the eigenvalues. If Au=0, the form
identity makes its weak gradient zero; connectedness makes u constant,
and infinite volume rules out a nonzero L2 constant. All claimed spectral
conclusions follow without confusing spectral type with a discrete
spectral set or asserting uncountably many eigenvalues.

## Source and reproducibility boundaries

The already available accepted author version of Krejcirik and Lotoreichik,
Quasi-conical domains with embedded eigenvalues, was reinspected at
Section 2.2, Propositions 2.2 and 2.3, and the beginning of Section 3.
Those passages supply the bounded finite-domain convergence and explicitly
leave the later cube centers free. Public references are
https://arxiv.org/abs/2205.08172v2 and
https://doi.org/10.1112/blms.13113.
The local PDF is 194,167 bytes, SHA-256
32081b2bf77ed26dd3ed2d05538f0a6e6b836159f1db9628d5778d47352d90ac.
No source text or PDF is included in this report package.

The first independent checker was replayed with the original author
directory and author archive, without optional corpus or source inputs.
It passed 2,923 exact finite and integrity assertions. Its embedded replay
of the author's checker passed 4,187 assertions and reproduced the frozen
author output byte-for-byte. The 2,923 count includes the optional author
archive checks; it is therefore different from the earlier 2,911 portable
count without that archive. These are software diagnostics and integrity
checks, not computer proofs of the infinite-dimensional theorem.

The separate second-review verifier checks the supplied frozen objects,
their manifests, nesting of the author snapshot, and the geometric error
tail arithmetic. Its package mode checks this report package's manifest.
The analytic verdict rests on the arguments above, not on assertion counts.

The package contains only this authored review, acceptance and verification
metadata, a reproduction utility, and a manifest. It includes no source
copies, raw datasets, private material, or changed original proof. There
are no required mathematical repairs and no unresolved targeted gaps.

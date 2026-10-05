# Independent adversarial audit of the quasi-conical pure point construction

Problem 30005613 / OWR-14297736-021, queue rank 800.
Audit date: 5 October 2026.

## Verdict

**PASS for the full existential theorem as stated in the frozen PROOF.md.**
No mathematical correction is required and no unresolved logical gap was
identified. This is an independent adversarial AI audit, not a proof-assistant
certificate, human peer review, or a historical-priority determination.

The accepted statement is: for every integer d≥2, there exists a connected
open quasi-conical tower of expanding cubes, joined through positive windows
whose widths tend to zero, such that its Dirichlet Laplacian has a complete
orthonormal eigenbasis and spectrum [0,∞). Both absolutely continuous and
singular continuous spectral subspaces vanish. All eigenvalues are positive,
their closure is [0,∞), and the whole spectral set is essential.

Cube widths and apertures are both free inductive parameters. The proof
does not establish the same result for every already prescribed tower,
smooth boundaries, positive-length passages, Neumann conditions, or bounded
domains. These limitations are already explicit in the candidate and do
not narrow the existential question addressed here.

## Frozen object and scope of review

The author ZIP is 16,490 bytes, SHA-256
2d15c0f1f7b094c92bafb6d2fed6d3b212c597adf9043c9f49c737a6f082e09e.
Its manifest is SHA-256
4ae99f0866dc70b2a60fd88707bb20acf5be845be4c7af4d635ac3b62b9349ff.
The proof is 14,044 bytes, SHA-256
5d1bab0b62ac5f78c69b0d82babd0b79fa4944097470fa760fdb3c485e362a20.

All seven manifest-listed files and the manifest itself matched the ZIP
byte-for-byte. The audit package preserves those eight files in author/.
The frozen original was not edited. Every proof section was checked, with
particular attention to multiplicity, the finite/infinite quantifier order,
the dimension-two capacity issue, and completeness of the eigenvectors.
ANALYTIC_CHECKS.md records an independent reconstruction of the crucial
arguments, including a direct proof of the finite-window convergence.

## Section by section mathematical review

### Sections 1 and 2: operator, geometry, and finite-window theorem

The form definition on H₀¹(O) is appropriate for arbitrary open sets with
slits. Bounded finite stages have compact resolvent and strictly positive
eigenvalues by zero extension into a fixed bounded box; no Lipschitz boundary
hypothesis is needed. Adjacent cubes touch at the intended common face,
and a window cube of half-width δ<a_n lies inside their interiors except
on that face. The L² spaces before and after opening the window are
canonically identical, while their form domains differ.

The source dependency is correctly scoped to the finite, bounded stage.
As δ tends to zero, the only persistent new boundary point is the interface
center. In d=2 a naive linearly rescaled cutoff would have nonvanishing
gradient energy, but a logarithmic cutoff has energy 2π/log(1/r)→0. In
d≥3 the usual shrinking cutoff has energy O(r^(d-2)). Thus a point is
removable in this H¹ capacity calculation in every claimed dimension.

The audit's direct Mosco argument uses cutoffs away from the interface
center, bounded Sobolev truncation, and weak closedness of H₀¹(D0). A
bounded-box compactness contradiction then upgrades convergence to the
operator norm of the resolvents. It keeps all earlier windows fixed and
does not infer form equality from measure-zero changes. The imported
finite-window fact is valid for exactly the geometry used.

The passage from norm-resolvent convergence to isolated spectral-cluster
projections is also valid. The resolvent eigenvalues are nonzero and
isolated, so fixed contours avoid both the other eigenvalues and zero.
Resolvent identities give uniformly convergent contour integrals. The
norm-distance-less-than-one criterion supplies equality of ranks.

### Section 3: avoiding all current resonances

For each fixed λ in the finite protected set, and a in a bounded candidate
interval, the cube eigenvalue formula bounds every positive integer
multi-index that could resonate with λ. Only finitely many widths are
excluded. Choosing the next width in (a_n+1,a_n+2) is therefore possible.

Crucially, the old finite-stage operator has already been fixed before this
choice. Its protected eigenvalues do not depend on the new width. The new
width is fixed before its aperture is chosen. There is no circular choice
of the eigenvalue set and the geometry, and no generic simplicity claim.
Avoiding a finite set of exact resonances requires no uniform gap estimate.

### Section 4: preserving all the induction invariants

Each protected projection is a sum of complete eigenspace projections.
At the next stage, an old eigenvalue's whole cluster is transported, even
if the eigenvalue splits. Every smaller protected projection is a subset
of the same family of disjoint clusters. This preserves both full spectral
subspace status and nesting.

Only finitely many projections and clusters are constrained at any one
stage. The aperture can simultaneously satisfy all their norm bounds and
its positive geometric upper bound. Rank stabilization follows from the
same estimates. A new finite spectral cutoff contains all old protected
clusters and approximates the finite current test set, by the spectral
theorem for the bounded-stage compact resolvent.

Nothing requires preserving a preferred eigenvector in a multiple
eigenspace. Nothing requires the transported old projection to remain
a low-energy cutoff. These two distinctions remove the main finite-stage
obstructions. They were checked explicitly rather than inferred from
one-eigenfunction perturbation theory.

### Section 5: final domain and exhaustion

The union of the finite stages is open and connected. The unbounded cube
widths give arbitrarily large balls. The countably many interface windows
are d-dimensional null sets, so the cube L² bases form a complete
orthonormal system for the final Hilbert space.

The form spaces V_n=H₀¹(O_n) increase inside V=H₀¹(O) after zero extension.
They are closed in the form norm. Their union is dense because any compact
support in the increasing open exhaustion lies in a finite stage. The
variational solution R_n f is the form-orthogonal projection of Rf onto
V_n, which gives strong convergence R_n→R on the common final H.

The extended R_n have zero kernels on future cubes and are not themselves
resolvents on all of H in the usual densely defined sense. The proof never
needs that false assertion. It correctly proves convergence directly and
uses only bounded operator identities. It also never assumes operator
norm convergence of this infinite exhaustion.

### Section 6: fixed-rank limits and genuine eigenvectors

For each fixed birth index k, the summable errors make P_n^k converge in
operator norm. The tail sum is exactly 2^(-n-1). The limit is an
orthogonal projection with the same finite rank. Norm limits preserve
nesting between any two adjacent birth indices.

The commutation limit is valid: a strongly convergent uniformly bounded
sequence R_n can be multiplied by a norm-convergent sequence P_n^k on
either side, and both products converge strongly. Hence the limiting
projection commutes with the actual limiting resolvent R. No unbounded
operator is moved through a limit, and no convergence uniform over all
birth indices is asserted.

On each finite-dimensional reducing range, R is a positive injective
matrix. Its eigenvalues are strictly positive. For an eigenvector with
Rv=μv, v=μ^(-1)Rv lies in dom A and satisfies Av=(μ^(-1)-1)v. Thus every
protected limiting range is spanned by genuine eigenvectors. In particular,
its finite rank cannot escape to infinite energy: that would force a
nonzero kernel vector for R.

### Section 7: the decisive completeness estimate

Every fixed cube-basis vector f_(j,l) belongs to every test set F_n from
n=max(j,l) onward. At each such birth index the approximation error is
less than 2^(-n), and all future transport contributes at most 2^(-n-1).
Therefore its distance from the limiting pure point subspace is less
than 3·2^(-n-1) for arbitrarily large n, and is zero.

The use of k=n in this estimate is legitimate: the tail bound is valid
for every trajectory beginning at its own birth. The proof is not
silently interchanging a merely pointwise convergence with an unbounded
index. The explicit tail bound supplies what is needed at that diagonal.

Since the tests form a basis, the pure point subspace is all of H. This
eliminates the otherwise uncontrolled orthogonal complement and excludes
both continuous spectral types. Merely obtaining dense eigenvalues would
not do so. The nested finite differences additionally yield a complete
orthonormal eigenbasis.

### Sections 8 and 9: support, endpoint, and limitations

Scaled compactly supported plane waves in disjoint enlarging cubes have
unit norm and residual O(r_n^(-2)+|ξ|r_n^(-1)). They belong to the
Dirichlet operator domain without requiring smoothness of the boundary.
They are weakly zero, so Weyl's criterion puts every λ≥0 in the essential
spectrum. Nonnegativity gives σ(A)=σ_ess(A)=[0,∞).

For a complete eigenbasis the spectral set is the closure of the
eigenvalues. The zero-energy form identity, connectedness, and infinite
volume exclude a zero eigenfunction. Pure point spectral type is not
being confused with a discrete spectral set or with every real λ being
an eigenvalue.

The construction is qualitative. It supplies no numerical apertures,
spectral-gap modulus, decay rate for individual eigenfunctions, or
boundary-smoothing theorem. These are unnecessary for the accepted claim.

## Adversarial failure modes explicitly checked

- Null geometric changes do not imply equal Dirichlet form domains. The
  proof uses capacity and convergence instead.
- Dimension two needs logarithmic cutoffs. Their energy tends to zero.
- Exact new-cube resonances can destroy localization of a selected old
  eigendirection. The finite forbidden-width argument avoids them.
- A repeated eigenvalue can have unstable individual eigenvectors. Whole
  spectral clusters preserve rank and provide the required continuity.
- Pure point finite approximants alone do not guarantee a pure point
  limit. The norm-convergent protected subspaces and dense birth schedule
  supply the missing information.
- Strong convergence of projections alone can lose rank. The candidate
  has operator norm convergence at every fixed birth index.
- Summable errors alone do not ensure completeness. The candidate makes
  the later birth error and its whole future tail tend to zero on a fixed
  complete test system.
- Trace-class invariance controls the absolutely continuous part, not the
  singular continuous part. It is not used for the final conclusion.

## Reproduction and provenance

The author's exact checker reproduces its frozen output byte-for-byte:
4,187 assertions. The independently authored checker passes 2,944 exact
finite and integrity assertions with all optional inputs. Its portable
mode passes 2,911. These counts are separate; they are not counts of
infinite-dimensional proof obligations discharged by software.

The independent checker includes a different nonresonance enumeration,
two-dimensional birth blocks with splitting multiplicities and multiple
rational rotations, geometric contact checks, exact error tails, and an
explicit unstable rank-one eigendirection example. Its remaining checks
verify the unchanged author files, archive, complete corpus hashes,
statement and review hashes, and source PDF hashes. It does not simulate
the Dirichlet PDE or compute admissible windows.

Full supplied corpora were read for the target identity, not just extracted
records. The review hash was independently reconstructed using the
repository's documented pair of problem and matched report. The target
has no report at its problem-code key, so the matched report is empty.
All three full-corpus hashes match the author metadata.

SOURCE_CHECKS.md gives the primary-source and fresh bounded repository
checks. The 2026 survey's open-problem status makes historical-priority
language inappropriate. No later primary resolution was located by the
bounded searches, which do not prove literature completeness.

## Corrections and publication boundary

Required mathematical corrections: none. ANALYTIC_CHECKS.md is a
supporting exposition, not a repair on which a changed theorem depends.

One provenance caveat deserves emphasis: the default-branch code search
returned no hit even though direct inspection finds the target in QUEUE.md.
Its negative result must not be described as exhaustive. The direct
attempt-directory, actual attempts-tree, and bounded PR/branch checks are
the appropriate evidence for the limited statement that no matching actual
prior mathematical attempt was located. This caveat does not affect the proof.

The original two substantive approaches out of a five-approach budget
remain two. This review does not claim that the previously queued remote
state has already been updated. No remote write, PR creation, merge,
release, DOI registration, or external outreach was performed.

The safe package contains authored mathematics and audits, checker code,
public citations, and verification metadata only. It excludes source PDFs,
article excerpts, screenshots, raw dataset records, and private coordination
material. The accepted result is suitable to present as a fully reviewed
existential proof candidate, with its AI-review and scope qualifications
retained for further expert scrutiny.

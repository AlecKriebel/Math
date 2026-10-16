# Root mathematical reconstruction for PR #765

Checked 16 October 2026 UTC against immutable head
021518f6f65a86658f72e0b31bfa0814bf1aa25d, problem 30005613,
OWR-14297736-021. This is verification of the complete saved candidate
within its original 2/5 substantive-attempt budget, not a new proof search.

The root initial position was saved before historical favorable reports.
The complete author proof, complete selected source record and empty prior
report, both historical mathematical audits, the historical analytic
reconstruction, and the two new independent family reconstructions were
subsequently read. Software checks are finite diagnostics and integrity
checks; they do not formally certify the PDE theorem.

## Exact claim and source scope

For each integer d>=2 there exists one connected open quasi-conical tower
of expanding cubes, joined through positive shrinking zero-thickness
windows, whose form-defined Dirichlet Laplacian A has a complete
orthonormal eigenbasis. Its spectrum and essential spectrum are [0,infinity),
its positive eigenvalues are dense there, zero is not an eigenvalue, and
both continuous spectral subspaces vanish. Both cube half-widths and
apertures are selected inductively. The candidate supplies no arbitrary
preassigned-tower, smooth-boundary, Neumann, positive-length-passage or
effective-aperture theorem.

The official OWR contribution, printed2077-2078, poses this existential
question. KL Section3 explicitly leaves later centers unfixed and selects
them during induction. Its Section5 and the dated September2026 survey's
OpenProblem1 ask whether the singular continuous part can also be removed.
These primary sources support the stated parameter freedom. A dated open
question does not establish current priority; that is a separate gate.

## Geometry and the finite-window analytic input

Let a_1=x_1=1, choose a_(n+1) in (a_n+1,a_n+2), and set
x_(n+1)=x_n+a_n+a_(n+1). At p=(x_n+a_n)e_1, a connector cube of half-width
delta<a_n lies in the two adjacent cube interiors except for its middle
face. Thus the newly added set is exactly an open patch of that face.
The union remains open because the whole connector cube is included, and
is connected because the connector overlaps both components. Its change
in d-dimensional measure is zero; its change in H_0^1 boundary conditions
is not zero. The common L2 identification is justified by this explicit
geometry, not by a general equal-closure assertion.

Fix a finite old tower with all its windows unchanged, fix the next cube,
and contain the resulting domains D_delta in one bounded box B. Zero
extension embeds their closed form spaces V_delta into H_0^1(B).
The spaces decrease as delta decreases. Their intersection is V_0:
for bounded u in every V_delta multiply smooth approximants by a smooth
cutoff vanishing near p; once delta is sufficiently small the products
are supported compactly in D_0. In d>=3 the cutoff gradient energy is
O(r^(d-2)); in d=2 use inner radius r^2, outer radius r and a smooth
logarithmic profile. Its energy is C/log(1/r) and its L2 error tends to
zero. The products converge to bounded u in H1. Apply this argument to
bounded real and imaginary Sobolev truncations to treat arbitrary u.
Closedness gives the claimed intersection without requiring slit-boundary
regularity or writing H_0^1 of a nonopen set.

For any delta_j->0, a weak H1 limit of u_j in V_delta_j belongs eventually
to each fixed V_s and therefore to the intersection V_0. The constant
recovery sequence for each v in V_0 supplies the other Mosco condition.
Resolvent solutions of unit-bounded inputs have a uniformly bounded
H_0^1(B) norm. If their difference from R_0=(A_D0+1)^(-1) did not converge
in operator norm to zero, choose weakly convergent unit inputs f_j and
use Rellich compactness to extract strongly convergent outputs. Testing
against V_0 identifies their limit as R_0 f. Compactness of R_0 also gives
R_0 f_j->R_0 f, a contradiction. Thus R_delta->R_0 in operator norm.

This directly proves the needed input and agrees with KL Props2.2-2.3
and its successive interconnection argument. It is a finite bounded-stage
statement, with old windows fixed. In d=1 it fails: every positive window
joins adjacent intervals into a single interval. The dimension restriction
and logarithmic d=2 argument are essential.

## Nonresonance, multiplicities, and finite constraints

Once the old finite operator is fixed, its protected spectral set S is
finite and positive. A new cube resonance requires
pi^2 sum(m_i^2)/(4a^2)=lambda, with lambda in S and a in a bounded open
interval. This bounds every positive integer m_i, leaving finitely many
forbidden widths. An admissible width exists before any new aperture is
chosen. There is no circular or infinite spectral-avoidance condition.

Each protected old eigenvalue then has exactly its old eigenspace in the
disconnected enlarged domain. Isolate all protected eigenvalues by
disjoint intervals. Norm convergence of the bounded resolvents gives
norm convergence of their Riesz projections about isolated nonzero
resolvent eigenvalues. Projections at distance below one have equal rank
by injectivity of either projection on the other's range. Transporting
complete clusters preserves multiplicity and nesting even when a cluster
splits; transporting an arbitrary selected eigenvector would fail.

There are finitely many protected projections at each stage, so one
positive aperture meets every requested norm bound and the geometric
upper bounds. A sufficiently high finite spectral cutoff at the new
bounded stage contains all transported clusters and approximates every
current finite probe. After birth a protected projection need not remain
a low-energy cutoff. No uniform gap, simple spectrum, aperture modulus,
or bound on all future birth ranks is needed.

## The actual limiting resolvent and finite-rank limits

The growing connected open tower O contains arbitrarily large balls.
Except for countably many null interface patches its L2 space is the
direct sum of cube L2 spaces. Fix each cube sine basis when that cube is
chosen; their union is an orthonormal basis of final H. These are L2
probes, not claimed eigenvectors or operator-domain vectors of final A.

The zero-extended V_n=H_0^1(O_n) form increasing closed subspaces of
V=H_0^1(O), dense in its form norm. Indeed each compact support in the
increasing open cover lies in one finite stage. For f in H, the partial
solution R_n f is the form-orthogonal projection of Rf onto V_n, with
R=(A+1)^(-1). Hence R_n->R strongly and ||R_n||<=1. Partial extensions
have kernels on unused future cubes; they are not asserted to be genuine
full-H resolvents. Operator-norm convergence of this exhaustion is not
used and would be false.

For each fixed birth k, ||P_(n+1)^k-P_n^k||<2^(-n-2) gives a norm limit
P^k with tail bound ||P^k-P_n^k||<=2^(-n-1). Products and adjoints are
norm continuous; the limit is an orthogonal projection. Distance below
one preserves its original finite rank. Nesting passes to the limits.

The identities R_n P_n^k=P_n^k R_n pass strongly to RP^k=P^kR: combine
strong convergence of the uniformly bounded R_n with norm convergence
of P_n^k on each fixed vector. Each finite-dimensional range reduces the
actual injective positive R. Its eigenvalues mu are positive; if
Rv=mu v, then v=mu^(-1)Rv lies in dom(A) and Av=(mu^(-1)-1)v. Thus every
limiting range lies in H_pp(A). Injectivity prevents a nonzero protected
space from escaping to infinite energy.

## Completeness is the decisive spectral-type step

Use F_n={f_(j,l):j,l<=n}, birth error eta_n=2^(-n), and the tail bound
above. Every fixed basis probe belongs to every sufficiently late F_n,
so ||(I-P^n)f||<2^(-n)+2^(-n-1)->0. The same explicit tail bound is
valid along every trajectory, including the newly born k=n. This is not
an interchange of two uncontrolled limits. Since H_pp(A) is closed and
contains every P^n f, it contains every basis probe and equals H.
Consequently both continuous spectral subspaces vanish. Dense eigenvalues
alone, or trace-class absence of absolutely continuous spectrum, would
not imply this conclusion; direct sums with continuous multiplication
operators provide counterexamples to those weaker arguments.

Diagonalize R on the finite-dimensional orthogonal differences of the
nested limiting ranges to obtain the claimed complete orthonormal
eigenbasis. The limiting projections need only reduce R; they need not
be full spectral projections of A.

## Spectrum and zero

For lambda>=0 choose |xi|^2=lambda and unit chi in C_c^infinity(B_1).
Inside cube n use r_n=a_n/2 and
u_n(x)=r_n^(-d/2)chi((x-c_n)/r_n)exp(i xi dot x).
These belong to the actual operator domain with action -Delta, have unit
norm and disjoint supports, and therefore are weakly null. The product
rule gives residual at most r_n^(-2)||Delta chi|| plus
2 sqrt(lambda) r_n^(-1)||grad chi||, tending to zero. Weyl's criterion
and nonnegativity give spectrum=essential spectrum=[0,infinity).
Completeness makes this the closure of the point eigenvalues. A zero
eigenfunction would have zero weak gradient, hence be constant on the
connected infinite-volume O, and hence vanish in L2. All eigenvalues are
positive; pure point type does not make every spectral point an eigenvalue.

## Artifact integration and source-render correction

Root reproduced all three immutable normal/outer-O/environment2 wrapper
runs with identical outputs and all39 original bytes unchanged. Nine
corrupted in-memory filesystem views were rejected by the actual guard
under optimization2. These diagnostic scopes and unrun optional historical
corpus/queue modes are explicit in root_reproduction/.

Root independently rendered K26 PDF p16 from fresh bytes with SHA256
d9d296eec2dcebc5b5cb7ce97257f4efb0ab3203f1265dc317be05f804899d30.
Both point-spectrum equalities visibly include closure bars. The new
spectral-family report's criticism of an imprecise equality is therefore
incorrect, a presentation/source-reading issue with no effect on the
candidate theorem. A separately preserved addendum has been requested;
the already closed original review must remain untouched. No final root
integration gate is implied until all family manifests and this correction
are closed, read, and verified.

Mathematical reconstruction: no candidate proof repair identified.
Priority, whole-preprint review, human peer review, and publication remain
separate decisions. No external communication occurred.

Final integration addendum 2026-10-16T05:12:33.076331+00:00: both mathematical family manifests and the separate source-reading correction are closed and verified; MATH_GATE.json is PASS. Both bounded priority reviews are also closed and challenged, with no full predecessor or blocking credit issue located. PRIORITY_GATE.json permits only the narrowly credited construction framing and retains exact historical-coverage limits. No candidate proof repairs were required. Whole-preprint reviews remain pending.

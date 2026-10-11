# Root reconstruction: quarter-filled optimal flux, PR376

2026-10-03 UTC. Original head `9a92b6a0bd7cff3a8c11bf66ff9338264ab012d1`.
Audit estimate60%; original unrestricted discovery0%. This is a candidate-informed
reconstruction, not an independently sealed blind rediscovery. Three separate
source-first families preserve their own earlier independence. Their final
artifacts, complete controls and a final integration gate remain to be checked.

## Literal target and normalization

The complete [Lieb1998 HTML](https://web.math.princeton.edu/~aizenman/OpenProblems_MathPhys/9802.OptFlux.html),
including its technical TeX, asks for the lowest-quarter spectral-sum minimum
over arbitrary nearest-neighbor Hermitian hopping phases on a large periodic
square lattice. Uniform pi/2 is a conjectured optimizer. A claim about one small
square, one uniform-flux class, one local basin, or one moment polynomial is not
that comparison. The source does not precisely quantify a thermodynamic claim;
finite and bulk conclusions must be distinguished. The packet's finite graph is
the simple even L-square torus, L>=4, with unit hopping and zero diagonal.
Energies are in units of that hopping magnitude; densities are per vertex.
No spin multiplicity, interaction or chemical-potential term is added to the
literal matrix objective.

Three independently retrieved full source files match the frozen hashes.
Lieb1994's reflected partition-function theorem is at half filling, with its
stated reflection assumptions; its proof does not provide the quarter-filled
sorted sum. Lieb-Loss1992 Lemma2.1 requires agreement of **all circuit** fluxes.
On a torus, plaquettes alone omit two loop holonomies. Its determinant theorem
and SectionVII counterexamples also prevent replacing an energy optimization
by a polynomial or determinant optimization. Source text and actual rendered
pages were read; optional public replay without source inputs checks zero raw
bindings. Fresh source-bound replay is a separate execution.

## Gauge, projection and small-volume global result

There are2N undirected edges and N-1 independent vertex-gauge directions. The
gauge quotient therefore has N+1 dimensions: N plaquette phases with one total
product constraint, and two unrestricted circuit holonomies. Set a spanning
tree's phases to1. Plaquette equations successively determine vertical phases
and horizontal wrap phases, with closure exactly the total-product constraint.
The construction works for continuous phases, not only the checker's finite
residue grids. Twisting either loop at zero plaquette flux changes twisted plane
waves and their eigenvalues, so those parameters cannot be discarded.

Ky Fan's variational identity follows directly from eigenbasis projection
weights: E_q(T)=min_rank-q-P Tr(PT). Compactness allows joint minimization over
P and actual edge phases. For each edge the trace contribution is
2Re(P_yx T_xy), minimized at T_xy=-P_xy/|P_xy| when the entry is nonzero.
Hence the exact Grassmannian objective is -2max_P sum_edges |P_xy|. This
reformulation leaves a substantive nonconvex problem; it does not solve it.

Bipartiteness gives paired singular values +/-s_j of the off-diagonal block.
The fixed second moment gives sum s_j^2=2N. With q=N/4, Cauchy-Schwarz gives
E_q>=-N/sqrt2. Equality requires exactly q singular values sqrt8 and all
others zero, equivalently T^3=8T. The L4 Gaussian-integer hopping matrix has
that identity entrywise and trace T^2=64, giving four eigenvalues each at
plus/minus sqrt8 and eight zeros. Its energy is -8sqrt2 and is globally optimal
over all phases. Zero plaquette flux with both antiperiodic loops has the same
spectrum, so minimizing flux is not unique at this size. This tie does not
refute that quarter flux is also optimal. For even L>=8 the unique straight
three-step displacement reaches a non-neighbor with a unit-modulus T^3 entry;
there T^3=8T is impossible. L6 has a second three-step route and is excluded.

## Local moments, defect and the actual energy floor

For L>=8, six-step closed walks have no noncontractible winding. Their exact
local winding classification has232 empty,144 square and24 rectangular walks
per root. Thus, with S=sum cos(phi_p) and neighboring plaquettes counted once,
Tr T^4=28N+8S and Tr T^6=232N+144S+12sum cos(phi_p+phi_q).
The exact integer enumerator verifies all returning direction words; Gaussian
matrix multiplication independently tests the identities at actual fields.
The finite enumeration gives a complete local combinatorial certificate, and
the no-winding argument extends it to every stated size.

For D=||T^3-8T||_F^2, expanding those moments and completing a square gives
D-44N/3=(48/N)(S+N/6)^2 +6sum(c_p+c_q-2S/N)^2
+6sum(s_p-s_q)^2. All terms are nonnegative. Uniform fluxes compatible with
the total-product condition can approximate arccos(-1/6), proving only
thermodynamic defect sharpness. The independent global family further observes
that finite equality is impossible: equality forces all sines equal and every
adjacent cosine sum=-1/3. Equal sines give equal or opposite cosines; the
nonzero required sum forces both cosines=-1/6, and connectedness forces a
uniform phase. Compatibility makes its exponential an Nth root of unity,
whereas twice its cosine=-1/3 would be a rational noninteger algebraic integer.
The family's written derivation and controls will be checked separately before
promotion; this does not identify the energy minimizer.

Write r=sqrt8 and delta=qr-sum_(j<=q)s_j. The exact distance identity is
sum_(j<=q)(s_j-r)^2+sum_(j>q)s_j^2=2r delta. All s_j lie in[0,4]. For
f(s)=s(s^2-8), |f(s)|<=4(4+r)|s-r| and |f(s)|<=8s on that interval.
Apply the first estimate only to the top q values and the second to the rest.
Then D<=4r[4(4+r)]^2 delta, giving the stated positive uniform correction
11(3sqrt2-4)/1536 to -1/sqrt2. The substantial slack in this conversion
explicitly prevents importing the defect optimizer as an energy optimizer.

## Uniform magnetic bands and all holonomies

For L=4n, a four-site Harper fiber has diagonal(A,B,-A,-B), A^2+B^2=4,
and closing phase w. Its directly expanded characteristic polynomial is
E^4-8E^2+4-2cos(4kx)-2cos(4ky). There is exactly one outer-negative
eigenvalue per fiber, and exactly q fibers, with a positive gap to the inner
bands. The actual quarter-filled sum is therefore the full outer-negative band,
with density -1/(4n^2) times the sum of f(cos x+cos y), where here
f(t)=sqrt(4+sqrt(12+2t)). The factor accounts for the fourfold repeated
vertical cosine, not for a physical spin multiplicity.

For every derivative order m>=1, each repeated chain-rule term has sign
(-1)^(m-1): the inner and outer square-root derivative signs combine to
that same sign and their combinatorial coefficients are positive. For generic
c=cos a, the n Chebyshev roots are distinct. Differentiating their g-sum gives
sum g'(x_i)/T_n'(x_i), the divided difference of g' divided by the positive
leading coefficient2^(n-1). The divided-difference mean value gives precisely
the sign of g^(n). Continuity covers the repeated endpoint roots. Thus each
holonomy is globally optimized inside the uniform class at a=b=0 for odd n,
and pi for even n; strictness gives uniqueness of those loop values modulo2pi.
This is an all-n written proof, not an extrapolation from degree20 checks.

At n2 all sampled cosines vanish at the optimizing twists, giving
-(1+sqrt3)/4. Strict concavity and zero average cosine yield the Jensen
benchmark, strict for n>=3. Centered periodic integration cells give mean
coordinate displacement pi/(2n); the derivative bound K gives the full
twist-uniform error K*pi/(4n)=K*pi/L for the band integral. The endpoint
chord and Jensen upper bound on mean band magnitude give the stated continuum
enclosure, with the sign reversed for energy. None of these comparisons ranges
over nonuniform fields.

## Exact L8 Hessian and local scope

At antiperiodic loops, the actual64-dimensional hopping matrix has eigenvalues
-a,-b,b,a, a=1+sqrt3 and b=sqrt3-1, each of multiplicity16. The occupied
cluster gap is2. Internal multiplicity does not obstruct analyticity of its
Riesz projection or the trace sum. The four cubic projector polynomials are
checked at the exact eigenvalues and via the quartic relation. Their nearest
edge entry is -a T_xy/16, so every phase gradient vanishes. The direct Hessian
term is a/8; the off-cluster term has the negative transition denominator and
factor2. Multiplication by13824 yields precisely the weights6,2sqrt3 and
3(sqrt3-1) used in the executable contraction. Indices in that sparse trace
contraction implement Tr(P0 Ke Pj Kf), and taking the real part is required.

The whole128-square real symmetric Hessian, all gauge columns and its
translation invariance are checked. Connectedness gives rank63 for the gauge
differential. Fourier decomposition gives64 actual Hermitian2-square blocks:
at each nonzero frequency, the nonzero Fourier gauge vector supplies a kernel,
so positive trace establishes the other eigenvalue. The zero-frequency block
is kappa I2, kappa=(7sqrt3-9)/144>0. All64 trace certificates were inspected;
their radical endpoints and signed-coefficient lower estimates are exact
integers/rationals. Subtracting2kappa proves the advertised transverse bound.
This establishes65 positive physical directions and63 zero gauge directions.
An analytic local transverse slice and Taylor's theorem give strict local
minimality modulo gauge. Distant configurations and other sizes are untouched.

## Canonical bulk limit and phase separation

A single changed edge has eigenvalues plus/minus the hopping increment's
magnitude, so |Tr(P Delta)| is at most that magnitude for every projection.
The fixed-rank variational principle then bounds energy changes by the sum
over changed edges, with factor1. Removing2L wrap edges changes total energy
by at most2L. To upper-tile an even large open square, put quarter-rank
minimizing projections in every complete even l-box and a diagonal coordinate
projection on the leftover vertices. The leftover area is divisible by4.
Joining edges have zero trace against that block projection and the leftover
projection's hopping energy is zero. There is consequently **no upper joining
penalty**. The limsup is bounded by every fixed-box density; the sequence's
infimum bounds its liminf. This proves the all-even-square canonical limit and
its infimum formula, then the torus limit by the wrapping estimate.

Decoupled spectral sums minimize over **all** allocations r_j of the total
particle count. Equal block density cannot be used for a lower bound. The
lower convex envelope over every rank0..l^2 has a minimizing mixture on at
most two ranks. At the integer quarter rank its weights are rational, so a
square array with side a multiple of their denominator realizes exactly both
the proportions and total rank. The block trial proves the convexified upper
bound. Cutting a large torus into open l-boxes removes exactly2L^2/l edges;
the all-allocation variational identity and convexity give the lower bound
C_l(q_l)/l^2-2/l. The two sides supply rigorous certificates but are not
claimed equal at finite l.

The verified remaining interval is the coarse phase-independent energy floor
<=e_opt<=e_*, where e_* is the uniform band integral. No proof of
e_opt>=e_* and no certified better extensive competitor is present. Historical
author states and result text remain frozen; the current wrapper explicitly
qualifies the completed scoped review and independent SymPy dependency.
All five proofs and all ten Python source files, including the support module,
have been fully read.
Complete direct-object, manifest, ledger and full-stream reproduction are
separate artifacts. The outcome under review is **unsolved,5/5**, with no
paper, DOI, Zenodo record, tracker row or release.

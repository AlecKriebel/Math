# Independent pair, boundary, cutoff and projection subaudit

Final reviewed package: **package_v4**, frozen 2026-10-07T04:51:33.594395Z.
Audit completed 2026-10-07 UTC. Completion estimate: **100% of this assigned
subaudit**, with no estimate of global-theorem completion implied.

**Verdict: PASS within the stated scope; no blocking mathematical defect found.**
The pointwise field kernels, signed source–receiver identity, species factors,
positive energy, initial-entry term, collision-label exclusion, radial-tip
removal, differentiated dyadic cutoffs and moving receiver projection survive
the independent checks below. This is not a verdict on the complete global
theorem, the downstream occupation/dyadic selection sums, the local/continuation
proof, attribution, publication readiness, or any Lean certificate.

No earlier reviewer verdict was consulted. No candidate or upstream source was
edited, and no Git operation or external communication was performed. Exact
source hashes and final v4 binding are in `SOURCE_SCOPE.json`.

## Exact source binding

The analytic candidate was initially read from immutable package_v2. Before
finalizing, the exact package_v3 `main.tex` diff and hashes were checked. Its
only textual changes are the original Glassey–Strauss continuation attribution
and corresponding bibliography entry, outside the present core scope. The
pair, transfer and uniform-chain supplements and both pair certificate scripts
are byte-identical between v2 and v3.

The exact v3-to-v4 delta was subsequently inspected: it adds only
`\begingroup\small\raggedright`, `\setlength{\itemsep}{3pt}`, and the
closing `\endgroup` around the bibliography. It changes no statement, equation,
attribution content, or proof. All five analytic supplements and both pair
certificate scripts are byte-identical between v3 and v4. The actual pinned
upstream section files were rehashed and still match their pinned manifest.

The final v4 main source SHA256 is
`9d72d239677c1066ba22ffbea8ff36f26251a2eae532921bd5e8e12b5f9fdb8c`.
The unchanged pair supplement SHA256 is
`2e2cc01799947bee5bd4ad3e67e4674101e6514e6bfef3b42bfe4da4b08153b4`.
The actual upstream `retarded.tex` SHA256 is
`eedf365c0be2cefacecc93c2825b4991ccad1d32826d83aa24eb4b63ccf37be2`;
`cancellation.tex` SHA256 is
`6b615a3b4ba0fbb6d04ea2e88b441dabdd51f6b33fc976b23407413fc9ae162a`.
These match the pinned-source manifest for commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

Candidate references below mean
`reviews/package_v4/source-and-verification/`; upstream references mean the
actual files under
`sources/upstream_pinned/preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026/build/sections/`.
Line numbers below are verified against the frozen files. All pair-related main
line numbers remain the same in v4.

## Findings and file/line evidence

| Claim | Candidate evidence | Actual upstream evidence | Independent outcome |
|---|---|---|---|
| Number-preserving normalization and signed equations | main.tex:42–60; SUPPLEMENT_PAIR_IDENTITY.md:37–53 | Common normalized velocity law used in retarded.tex:149–153 | Correct Jacobian `m_b^3`; Maxwell source is `e_b f_b`, acceleration is `lambda_b` |
| Positive energy and cone orientation | main.tex:133–160; pair supplement:97–131 | retarded.tex:48–86 | Correct mass-weighted energy and `U−n·S`; charge signs cancel in work, not in positive budgets |
| Retarded phase Jacobian and receiver/source-time conversion | main.tex:180–189; pair supplement:148–152, 205–214 | retarded.tex:124–144, 392–428 | `dz=d dy dv` and `dt/ds=d/D`; no acceleration/mass factor in determinant |
| Electric and magnetic retarded signs | main.tex:198–210; pair supplement:161–185 | retarded.tex:196–279 | Direct potential differentiation gives exactly the displayed electric kernel and `n×kernel` magnetic kernel |
| Full signed branch cancellation | main.tex:215–264; pair supplement:194–287 | cancellation.tex:39–102 | Correct including the transport term, arbitrary independent accelerations and receiver residual sign |
| Source-field and source-cutoff factors | main.tex:358–376, 412–414; pair supplement:310–340 | retarded.tex:342–389; cancellation.tex:207–225 | Source costs carry `|c_ab lambda_b|`; bulk receiver costs carry `|c_ab|` and full `K_a` |
| Selected cutoff cancellation | main.tex:426–432; transfer supplement:121–138 | cancellation.tex:127–169 | Valid sourcewise after common physical multiplier is factored out; no comparison of different kernels |
| Initial-cone entry and radial tip | main.tex:191–196, 433–436; transfer supplement:134–138 | cancellation.tex:308–357; retarded.tex:257–279, 412–428 | Positive source-entry term bounded by datum/horizon; no remaining radial-tip distribution |
| Moving receiver projection | main.tex:420–424; transfer supplement:129–133 | cancellation.tex:256–270; direction.tex:84–123 | Exact derivative retains longitudinal primitive component and has claimed projected receiver size |
| Fixed-time receiver coefficient | main.tex:416–419; pair supplement:409–425 | cancellation.tex:363–375 | Both density and positive cone-flux bounds give the claimed `U`; no additional charge factor |

The two boundary terms must be distinguished: differentiation of the Maxwell
potential domain produces the initial sphere field in retarded.tex:163–172;
integration of the primitive along source time produces the entry term in
cancellation.tex:325–339. The sources retain both, and both have uniform datum
cost. They are not silently identified or omitted.

## Independent derivation of the physical factors

With physical momentum `p=m_a v` and `f_a=m_a^3 F_a(t,x,m_a v)`, the phase
Jacobian gives `F_a dp=f_a dv`. The normalized particle equation has
`V_a'=lambda_a(E+u_a×B)`, `lambda_a=e_a/m_a`. Maxwell potentials have source
coefficient `e_b/(4 pi)`. Therefore the branch force has the overall factor

    c_ab/(4 pi),  c_ab=lambda_a e_b=e_a e_b/m_a.

The source velocity derivative is

    b_b=lambda_b q_b^(-1)(I−u_b tensor u_b)(E+u_b×B).

Before cancellation, acceleration-kernel and source-cutoff terms therefore
have coefficient `c_ab lambda_b=e_a e_b^2/(m_a m_b)`. After the primitive is
differentiated, that source acceleration cancels only in the two bulk
residuals; it remains in cutoff derivatives. The receiver velocity derivative
is `alpha_t=q_X^(-1)(I−alpha tensor alpha)K_a` with the full normalized
acceleration `K_a`, so there is no new `lambda_a` and no division by charge.

For unit masses with charges `+1,−1`, the pair matrix is
`[[1,−1],[−1,1]]`; the source-acceleration coefficient matrix is
`[[1,1],[−1,−1]]`. Neutral source or receiver factors vanish. Different fixed
positive masses only change these exterior coefficients and positive energy
weights. No massless uniformity follows or is claimed.

## Independent retarded-field check

Let `ell=(r d)^(-1)`, with observation point fixed while source time varies.
Then

    r_s=−n·u,
    n_s=−(u−n(n·u))/r,
    d_s=−n_s·u−n·b,
    s_t=1/d,  grad_x s=−n/d,
    grad_x ell|_s=−(n−u)/(r^2 d^2).

Differentiating `−grad_x ell−partial_t(u ell)` produces

    (n−u)/(r^2 q^2 d^3)
      +[(n−u)(n·b)−d b]/(r d^3).

The curl of `u ell` produces its cross product with `n`, with the same sign.
The label-domain indicator has derivatives
`partial_t 1_{t>|x-y0|}=delta(t−|x-y0|)` and
`grad_x 1_{t>|x-y0|}=−n0 delta(t−|x-y0|)`. Thus its electric boundary
factor is `(n0−u0)/(t d0)` and its magnetic factor is `n0×(n0−u0)/(t d0)`.
No source-acceleration factor belongs on this boundary.

The potential electric field has initial time derivative `−j(0)`. Adding the
homogeneous wave with velocity `curl B0` therefore gives the Maxwell initial
velocity `curl B0−j(0)`. The homogeneous waves need not separately be a
vacuum Maxwell solution; retarded.tex:288–289 says this explicitly. There is
no missing initial-current term.

## Independent signed identity and its quantifiers

The direct force-to-source-time conversion is
`(d/D)[E_kernel+alpha×B_kernel]`, with `Qh=h+alpha×(n×h)`.
On the retarded branch,

    t'=d/D,  r'=d/D−1,
    r n'=(d/D)(alpha−n)+n−u=N0.

For `eta=1−alpha·u` and `k=u−eta n/D`, differentiation through source
velocity gives

    −b/(r d)−n(alpha·b)/(r d D)−k(n·b)/(r d^2).

These are precisely the source-acceleration terms in the negative derivative
of `k/(r d)`. For a receiver variation `A`,
`partial_alpha k[A]=n(A·k)/D`; with `alpha'=alpha_t d/D`, its derivative is
cancelled by the positive receiver residual
`n(alpha_t·k)/(r D^2)`. The geometric identities at main.tex:240–246 then
give exactly

    Kbranch=−(k/(r d))'
       +eta/(r^2 D^2)[n/(q_X^2 D)−alpha]
       +n(alpha_t·k)/(r D^2).

This derivation uses arbitrary source derivative `b` and receiver derivative
`alpha_t` separately. It does not substitute equal accelerations or a common
charge-to-mass ratio. Strict timelikeness guarantees nonzero denominators;
the identity excludes `r=0`, whose removal is handled below.

## Integration by parts, entry, collision labels and radial tip

On a fixed compact classical prefix, supported momenta and source/receiver
accelerations are bounded and `d,D` have positive lower bounds. At a time
mesh of spacing `zeta`, a source label that collides with the receiver at
some time lies in a spatial ball of radius `2 zeta` at a mesh point. Volume
preservation and the bounded transported density bound each mesh-point mass
by `C zeta^3`, and the union mass by `C zeta^2`. This proof works for
different species and requires no identical flow. Almost every source label
therefore has strictly positive minimum equal-time separation on the compact
prefix, which implies a labelwise positive lower bound on retarded radius.

The weight vanishes at receiver-interval endpoints. The only nonzero branch
endpoint is source time zero. Integrating `−(k/(r d))'` gives the positive
entry contribution

    f_b0(z) psi(t0) chi Pi(t0) k/(t0 d0).

Parameterizing initial position by `y0=X(t0)−t0 n` has absolute Jacobian
`t0^2 D`. Consequently the boundary density is bounded by `C t0 |psi(t0)|`
because `Dk=Du−eta n` is bounded, `d0` has a datum-dependent lower bound,
the initial velocity support is bounded, and `chi<=1`. Its integrated cost is
`C integral |psi| dt0`; the constant contains the fixed pair coefficient.

The factors from derivatives of the receiver-time weight and matrix are
`psi_s=psi_t d/D`, `Pi_s=Pi_t d/D`. After changing measure back, these give
`psi_t chi Pi f_b k/r` and `psi chi Pi_t f_b k/r`, respectively. This
accounts for both derivative terms in cancellation.tex:285–291.

Bounded cutoff overlap on a fixed prefix gives an integrable majorant
`C_prefix f_b(r^(-2)+r^(-1))`. A radial cutoff supported at `r~gamma`
has an extra derivative at most `C/gamma`; its new error is bounded by
`C_prefix f_b/(gamma r)`. With `dy=r^2 dr dn` its integral is
`O_prefix(gamma)`. Thus there is no cone-tip boundary or point-supported
term. The prefix-dependent constant is used only to justify the limit, not
as a final a priori constant. This distinction is explicit in the sources.

## Cutoff and projection bounds checked independently

In the narrow sector `d~theta^2`, `D~phi^2`, `theta<=16 kappa phi`, write
`k=(u−n)+n(1−eta/D)`. Since
`eta−D=alpha·(n−u)=O(phi theta)`, this gives

    |k|<=C theta/phi,  |P_X k|<=C theta,  |P_X n|<=C phi.

The multiplier on a source-time cutoff derivative in spacetime measure is
`f_b Dk/(r d)`, of size `C f_b phi/(r theta)`. Source logarithmic rates are
`C |lambda_b|p^(-1)(G/theta+theta |B|)`, producing exactly

    C|c_ab lambda_b|[f_b phi G/(r p theta^2)
                            +f_b phi |B|/(r p)].

Geometric rates use `|r'|<=C`, `|n'|<=C theta/r`,
`|d'_n|/d<=C/r`, and `|D'_n|/D<=C theta/(r phi)`. They produce
`C|c_ab|f_b phi/(r^2 theta)`. Receiver logarithmic rate is
`|D'_alpha|/D<=C theta^2|K_a|/(w phi^3)`, producing
`C|c_ab|f_b theta |K_a|/(w r phi^2)`. Projecting each of these primitive
terms adds `phi` because `|P_X k|<=C theta`.

The identity `sum beta_j=1` can be differentiated before restricting to the
branch. For a fixed selected index set, source or geometric derivatives of
the selected sum equal the negative unselected derivatives. At each state
the common multiplier is factored out of this sum, source species by source
species. The derivative is supported only where the two families meet,
giving comparable representative coordinates. Different pair coefficients
are never cancelled. Receiver derivatives remain directly estimated on
selected supports.

For high receiver energy, let `rho=|V_X|~w`, `xi=V_X/rho`,
`P_X=I−xi tensor xi`, with fixed dyad `w`. Direct differentiation gives

    Pi_t=−w/rho^2[(xi·K_a)P_X
          +(P_X K_a) tensor xi+xi tensor(P_X K_a)].

Hence `||Pi_t||<=C |K_a|/w` and
`|Pi_t k|<=C theta |K_a|/(w phi)`. This uses the full norm of `k` and
retains its longitudinal component. A false replacement of `|k|` by
`|P_X k|` here would gain an unjustified extra `phi`; the candidate does not
make that replacement.

To check the receiver residual more explicitly,

    alpha_t=P_X K_a/q_X+xi(xi·K_a)/q_X^3.

Together with `|P_X k|<=C theta`, `|k|<=C theta/phi` and
`phi>=c/w`, this gives `|alpha_t·k|<=C theta|K_a|/w`. Therefore the
unprojected receiver residual has the displayed size
`C f_b theta |K_a|/(w r phi^2)`, and its projection gains `phi` from
`P_X n`. For bounded receiver energy, `phi` is bounded below and the direct
norm bound suffices. No projector is used at zero momentum; the direction
argument uses high-energy ranges, where its denominator is bounded away
from zero.

At fixed receiver time the receiver kernel integrates to

    C|c_ab|/w min[h^2(p theta)^3,
                              (p theta h phi^2)^(-1)].

The first bound uses density `C p^3 theta^2`, cone-direction cap area
`C phi^2`, and the radial integration of `r^(-1)`. The second divides the
kernel by the positive cone-particle energy density `q d f_b`; the ratio
is `C/(w p theta h phi^2)`, and the cone budget is `H0/m_b`. These constants
are exterior, fixed species/data constants. Smallness of charge is neither
used nor inferred. Validity of the downstream selected-bin inequality is a
separate audit obligation.

## Computation and exact limitation

Both distributed scripts were run successfully:
`verify_pair_identity.py` gives zero generic polynomial residuals and
`exact_kernel_certificate.py` gives zero polynomial residuals plus 292 exact
rational assembled checks. Their universal polynomial scope is local
kinematic algebra, not the global PDE theorem.

The independent `independent_pair_check.py` in this folder imports neither
candidate certificate. It differentiates the retarded scalar/vector
potentials, converts the direct Lorentz kernel to branch measure, and
independently differentiates the full primitive. All **2,028 exact rational
cases passed**, including four off-axis/axis rational unit directions,
zero velocities, almost-null aligned/opposite velocities, independent
positive/negative accelerations, very small/large radii, opposite charges,
unequal positive masses, extreme fixed mass ratios, and zero charges.
The result and script hash are in `independent_pair_check_result.json`.
These are falsifiable spot-checks supporting, but not replacing, the
universal analytic derivation above.

The strongest scoped conclusion is that the advertised pair/boundary
mechanism introduces no unsupported equivalence to the one-species theorem
and no new sign, mass, boundary or moving-projection obstruction. It supplies
the pointwise and integration-by-parts inputs assumed by the uniform chain.
Whether that chain's occupation bounds, scalar dyadic sums, coefficient
selection, bootstrap closure and continuation establish the advertised
global theorem must be decided by the other independent audit routes.

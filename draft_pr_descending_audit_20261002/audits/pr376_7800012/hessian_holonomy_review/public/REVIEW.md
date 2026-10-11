# PR376: independent holonomy and full-phase Hessian review

**Scoped PASS. No mandatory mathematical repair found in the uniform-flux holonomy theorem (TURN_3) or the exact 8x8 local theorem (TURN_4).** The source's unrestricted quarter-filled optimal-flux question remains unresolved. A uniform-class global optimum and an 8x8 local optimum do not supply the missing comparison against arbitrary nonuniform phases.

This report audits the frozen attempt 7800012 supplied for original PR head `9a92b6a0bd7cff3a8c11bf66ff9338264ab012d1`. It binds the bytes actually replayed through executable/source hashes and the author manifests, rather than assuming an unrelated working checkout equals that head. No Git, remote, candidate, or publication mutations were performed. No external person was contacted.

## Independence and receipts

The literal [1998 problem page](https://web.math.princeton.edu/~aizenman/OpenProblems_MathPhys/9802.OptFlux.html), [Lieb 1994](https://arxiv.org/pdf/cond-mat/9410025), and [Lieb-Loss 1992](https://arxiv.org/pdf/cond-mat/9209031) were accessed first. The complete original HTML was downloaded; both complete primary PDFs were extracted and their pertinent theorem/gauge pages visually inspected. Raw inputs, extracts, renders and the author copy are ignored. The source bytes match the packet's three source hashes exactly.

`independent_pre_candidate_seal.md`, SHA256 `54173ecdfb2220c027ac24d46f2876de3a081e21bccb22d9ece66ea5c917cb27`, was fixed before any candidate/root/sibling or prior-verdict access. It independently derived the torus cycle count, occupied-cluster derivative formula, 4x4 uniform-holonomy polynomial and controls. The seal's typed time label was approximate and incorrect; its authoritative filesystem timestamp is **2026-10-03 05:44:16.868600 UTC**, recorded in the research log. Candidate reading started afterward. The separate verdict seal was written before the prior review was opened; its SHA256 is `53f329675cce42ce99a75f0ab9a5c6f9747e16f8e2aacde6332ad333b0f11d73` and filesystem timestamp is 2026-10-03 05:51:55.457450 UTC.

Every executable source was read, including the complete Hessian construction, five author checkers, replay wrapper, Gaussian-matrix module and, after verdict sealing, prior independent checker and review wrapper. All five standard-library author outputs reproduce byte-for-byte: **102,005 assertions**, per-turn counts `[22885,2773,105,45409,30833]`; **157 manifest bindings** and **three primary source files** verified. The entire 64-mode author certificate also reproduces exactly. The independent program imports no candidate code and adds **8,662 exact SymPy assertions**, full symbolic 2x2 Fourier blocks and a full 128x128 Hessian output. A separate standard-library program adds 19 topology/holonomy controls. After sealing, all 64 independently computed Fourier traces were compared exactly to the frozen certificate (130 comparisons); the prior review wrapper then reproduced its 984 controls.

The independent interpreter was invoked by its existing absolute path `/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python`, without resolving it, installing anything or changing that runtime. It supplies Python 3.14.6 and SymPy 1.14.0. The author replay uses standard-library Python only.

Three development failures in the independent symbolic checker are preserved with their script hashes. They were comparisons before expanding a matrix polynomial, before rationalizing a radical denominator, and before denesting the independently computed square root in the loop curvature. Explicit exact normalization repaired the checker; these failures did not require modifying candidate formulas. Final runs have exit status zero and empty stderr.

## 1. Torus coordinates and boundary assumptions

For a connected simple square torus with L>=3, there are N=L^2 vertices and 2N oriented positive-direction edges. A vertex phase chi changes edge phases by `chi_head-chi_tail` and conjugates the hopping matrix diagonally. The kernel of this incidence map consists of constants, so its rank is N-1. The edge-phase quotient has dimension N+1. Plaquette curl has rank N-1: the only face relation is the sum of oriented boundaries. Two independent noncontractible loops complete the coordinates. The exact topology controls verify incidence rank, curl rank, `curl*incidence=0`, and the N+1 rank after adjoining both loops for L=3,4,6,8. The written spanning-tree argument establishes the general statement.

Consequently, the original page's local-plaquette shorthand is incomplete on a finite torus. Equal plaquette fluxes and equal two loop products imply gauge equivalence: remove the phase difference on a spanning tree, then use the face cycles and two homology cycles to remove every chord. Plaquettes alone do not suffice. The independent zero-plaquette 4x4 controls give fourth spectral moments 640,576,512 for zero, one, and two antiperiodic loops. This is a checkable finite counterexample to that auxiliary shorthand, not to quarter-flux optimality.

Total plaquette product is one. Uniform pi/2 therefore requires N divisible by four. The simple-edge model excludes length two: on the 2x2 torus positive-direction instructions revisit the same unordered edges and leave only four distinct edges, not eight. The candidate avoids that issue by using even L>=4. Its quarter-flux fiber theorem further requires L divisible by four; the 8x8 Hessian claim has precisely that size. The L=6 case is not silently included in TURN_3.

## 2. Complete uniform-pi/2 holonomy theorem

Let L=4n. In the gauge with horizontal hopping `exp(i a/L)` and vertical hopping `i^x exp(i b/L)`, Fourier decomposition produces four-site Harper fibers with vertical diagonal `(A,B,-A,-B)` and one formal closing edge w, where A=2cos(k_y), B=-2sin(k_y), w=exp(4ik_x). The independent formal determinant over Laurent polynomials gives

`det(lambda I-H)=lambda^4-8lambda^2+4-z^4-z^(-4)-w-w^(-1)`,

where z=exp(ik_y). Thus, for `t=cos(4k_x)+cos(4k_y)`, eigenvalues are the four signed roots of `lambda^2=4 +/- sqrt(12+2t)`. The outer negative band is isolated uniformly: its magnitude is at least `sqrt(4+2sqrt2)` and every inner magnitude is at most `sqrt(4-2sqrt2)`. There are exactly N/4 fibers, one occupied eigenvalue in each. Degeneracies within bands and the possible middle-band touching cause no occupied-cluster ambiguity.

Define `f(t)=sqrt(4+sqrt(12+2t))`. Repeated chain/product rules express each derivative of f as a positive-integer-weighted sum of products `g^(k)(h(t))*product h^(m_i)(t)`, with `sum m_i=m`. Both square-root derivatives have sign `(-1)^(order-1)`, so each term has sign `(-1)^(m-1)`. This proves that sign for every m>=1 throughout t>-6, with strict nonzero magnitude. The independent derivative samples through order eight supplement this proof; they do not prove its all-degree quantifier.

The band sampling is

`E/N=-(1/(4n^2))*sum_(j,k=0)^(n-1) f(cos((2pi j+a)/n)+cos((2pi k+b)/n))`.

For fixed d in [-1,1], the n nodes of the first sum are the roots of `T_n(x)-c`, c=cos(a). For -1<c<1 these roots are distinct. Implicit differentiation and the divided-difference formula give

`d/dc sum g(x_i)=sum g'(x_i)/T_n'(x_i)=g'[x_1,...,x_n]/2^(n-1)`.

The mean-value theorem makes its sign equal to that of `g^(n)`, since the remaining factorial is positive. Continuity of the multiset of roots handles both repeated-root endpoints. For n=1 the same formula reduces to g'. Taking `g(x)=f(x+d)` proves strict monotonicity in c for every fixed d. The resulting global maxima of the positive band sum have `a=0 mod2pi` for odd n and `a=pi mod2pi` for even n. Applying the same argument to b gives the unique pair of loop values within the positive uniform-flux class. No assumption about a uniform flux optimizer in the unrestricted problem enters this proof.

The 4x4 in-class optimum is -8sqrt2, with loop Hessian `(sqrt2/8)I2`. On 8x8 the optimized uniform energy is `-16(1+sqrt3)`. Incorrectly retaining periodic loops gives

`-4*(2sqrt2+2(1+sqrt3)+sqrt(4+2sqrt2))`,

which is strictly higher by strict Jensen concavity (the sampled t values are 2,0,0,-2 instead of all zero). The auxiliary 70-digit decimal difference is about 0.0901942425552457. The exact concavity proof, not that decimal, rejects the missing-holonomy comparison mutant.

The candidate's continuum density, shifted-cell error `K*pi/L`, and chord/Jensen enclosure follow from `f'(t)=1/(2f(t)sqrt(12+2t))`, whose maximum on [-2,2] is K at -2. The mean absolute displacement of a centered cell is pi/(2n) per coordinate; the two-coordinate Lipschitz bound and energy factor 1/4 give exactly the stated error. These calculations control the uniform class and do not identify the unrestricted bulk optimum.

## 3. Smoothness, exact projectors and Hessian signs

At the 8x8 antiperiodic base, the independently built matrix satisfies `T^4-8T^2+4I=0`. Lagrange interpolation at eigenvalues `-1-sqrt3, 1-sqrt3, -1+sqrt3, 1+sqrt3` independently recovers all four cubic projector polynomials in TURN_4. Each projector has trace16 and the appropriate eigenvalue equation; the four interpolation identities prove orthogonal projectors summing to I. The occupied/unoccupied gap is exactly2.

An isolated rank16 cluster has an analytic Riesz projection and analytic summed energy even though the occupied eigenvalue has multiplicity16. Individual occupied eigenvectors need not be chosen differentiably. An explicit sufficient gap-preserving phase neighborhood is `max |h_e|<1/4`: the hopping difference has operator norm at most `4 max |h_e|<1`, so the original gap2 persists by eigenvalue perturbation bounds. At an occupied/unoccupied gap closure one cannot simply reuse this smooth Hessian; `diag(u,-u)` with one occupied state has energy `-|u|`, an elementary cusp control.

For an oriented edge e=(u,v), `K_e[u,v]=i T[u,v]` with Hermitian reverse. Its second phase derivative is minus that edge's hopping matrix. Exact projector entries at every edge give `P_0[u,v]=-(1+sqrt3)T[u,v]/16`. Therefore every gradient component vanishes and the direct Hessian term is `(1+sqrt3)/8` on each edge diagonal.

Differentiating the isolated projector in occupied/unoccupied blocks gives

`H_ef=((1+sqrt3)/8)delta_ef -2 sum_(j=1)^3 Re Tr(P_0 K_e P_j K_f)/(lambda_j+1+sqrt3)`.

Each denominator in the subtracted term is positive. Equivalently, the second-variation sum uses negative denominators `lambda_occ-lambda_unocc`. Reversing this sign or dropping the direct term violates exact gauge invariance; both mutants are rejected by the independent full `H*G` control. With projector numerators scaled by48 and H by13824, the transition weights are exactly `6, 2sqrt3, 3(sqrt3-1)`. All orientation, factor-two and scale conventions agree with the executable candidate.

## 4. Completeness of the 128-direction certificate

The independent implementation derives projectors with SymPy and evaluates sparse contractions for the two edge orientations. It separately constructs diagonal gauge conjugacies for one-step x and y translations, verifies them on every matrix entry, and thus proves the phase-energy Hessian is translation invariant in the seam gauge. It constructs the full 128x128 Hessian from those rows, verifies symmetry and exact annihilation of all vertex-gauge columns, and obtains incidence rank63.

It then computes all 64 actual Hermitian 2x2 Fourier blocks, rather than testing selected phase vectors or using only author trace values. At each nonzero frequency the gauge vector `(exp(2pi i kx/8)-1, exp(2pi i ky/8)-1)` is nonzero; exact block determinant zero and positive trace imply one zero and one positive eigenvalue. At zero frequency the block is

`kappa I2, kappa=(7sqrt3-9)/144 > 0`.

Every trace is at least 2kappa; the independent code verifies this with rational radical interval bounds (or exact zero difference). The roots sqrt2,sqrt3,sqrt6 are enclosed by adjacent 15-digit rationals whose squared inequalities are checked with integers. Complexification does not change the rank/inertia of the real symmetric Hessian, so the full real inertia is **65 positive, 0 negative, 63 zero**. There are no additional physical null directions. The minimum positive eigenvalue is kappa.

The distributed loop directions have one orientation's 64 phases equal to 1/8, the other zero. They have Euclidean norm one. Direct differentiation of the n=2 uniform energy gives both curvatures kappa, agreeing exactly with the full zero-frequency block. This independently checks both holonomies and the normalization against a separate energy formula.

Since gauge additions are an exact linear action on phase coordinates, a local Euclidean transverse slice has dimension65. Analyticity, stationarity and the positive transverse Hessian imply a strict local minimum there by Taylor's theorem. Gauge invariance extends that statement to every sufficiently small phase perturbation modulo gauge. It proves neither global 8x8 minimality nor local minimality at other sizes.

## Disposition and exact remaining gap

The scoped results survive attempts to falsify loop completeness, band occupation, cluster smoothness, projector normalization, Hessian transition signs, omitted direct terms, hidden physical nullspace and finite-size extrapolation. The prior review, read only after the independent verdict was sealed, agrees on these families; its verdict was not used to build this report.

No mandatory repair is identified in TURN_3/4. Preserve the packet's explicit size restrictions and original **unsolved** disposition. The strongest verified family result is the complete all-holonomy optimizer inside the uniform-pi/2 class for L=4n, plus the exact 8x8 strict local phase minimum modulo gauge. The remaining central gap is a lower-energy competitor or global lower bound against every nonuniform phase configuration at the intended finite or thermodynamic scale. No current argument closes that gap.

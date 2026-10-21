# Independent kernel/static-dynamic consistency adversary

Frozen PR214 head: `36d5ef15098163e74bf14c2e696f560ce592affd`. Target: 30005244 / OWR-11101924-008. Author budget shown by the parent: 2/5; this work is verification, with no new author attempt, repair, tracker mutation, provider mutation, Git mutation, or publication. Only the assigned family directory was written.

**Result: PASS for the kernel and consistency claims of CANDIDATE.md, conditional on its explicit geometric hypothesis (G), fixed complex frequency, and bounded measurable support. No counterexample or material gap was found in this family.** This does not decide source scope, the separate pathological-support construction, the abstract spectral argument, novelty, or acceptance of the entire PR.

The exact claim is that the embedded static matrices converge strongly on whole-space L2 to the compressed principal-value static operator, while the actual diagonal-omitting dynamic remainder matrices converge in Hilbert-Schmidt norm to the continuum dynamic remainder. The published static lattice bound supplies a uniform norm and interval. Success means deriving those statements without altering the sampled matrix, silently inserting a self interaction, assuming boundary regularity beyond (G), changing limit order, or invoking boundedness of a nonzero-frequency whole-space lattice operator.

## Independence and chronology

The candidate and full relevant primary texts were read first. The independent mathematical reconstruction was saved at 2026-10-15T07:57:38Z in `INDEPENDENT_RECONSTRUCTION.md`. No inherited `independent_review`, `FINAL_DISPOSITION.md`, or `SOURCE_AUDIT.md` verdict was opened for this family, either before or after that reconstruction. The list of available submitted filenames was inspected later for provenance only. The second author turn and its inherited review were not needed for this narrow family and remain outside this certification. No author program was run, imported, or modified.

## Checkable derivation

### 1. Kernel and distributional shift

The exact radial Hessian calculation gives

    K_k(x)=exp(ikr)/(4 pi r^3)
      [(1-ikr-k^2 r^2)I+(k^2 r^2+3ikr-3)ee^T].

CDN's d=3 normalization has nu_3=4 pi/3, so its (3.41) is exactly `(I-3ee^T)/(4 pi r^3)`. The distributional and principal-value kernels differ by `I delta_0/3`: the difference is supported at zero, homogeneous of degree -3, and cubic symmetry forces a scalar matrix delta; tracing fixes its coefficient. The Fourier multiplier of the principal-value operator is `xi xi^T/|xi|^2-I/3`. Its eigenvalues are exactly `-1/3,-1/3,2/3`, verifying the sign, normalization, and continuum form interval.

The dynamic difference has locally integrable singularity, including for complex k:

    R_k= -k^2 (I+ee^T)/(8 pi r) - i k^3 I/(6 pi) + O(r).

The exact symbolic control additionally obtains the next terms `3k^4 r I/(32 pi)-k^4 r ee^T/(32 pi)`. There is no r^-2 term and no constant ee^T term. For fixed k and finite L this yields `|R_k(x)|_F <= C(k,L)/r` on `0<r<=L`. Since only the bounded support difference set is used, negative imaginary k is admissible. The Hessian of `g_k-g0` is locally integrable and adds no delta distribution.

### 2. Cubic cancellation and static strong convergence

With any finite radial cutoff the lattice sum is exactly zero. Reflections cancel mixed entries, permutations equalize diagonal entries, and termwise trace zero cancels the equal diagonal values. No infinite conditionally convergent sum is rearranged. Translation disappears in `x_m-x_n=h(m-n)`. A cubic self cell also has zero principal-value integral by the same symmetry; it is not being replaced by the distributional self term `I/3`.

The near contributions for compact smooth input, after subtracting the center value, are both bounded by `C ||grad phi||_infinity delta`. The lattice estimate is

    h^3 sum_{0<|hj|<=R} |hj|^-2 <= C R.

For completeness, unit cubes around points in an integer annulus `j<=|n|<j+1` lie in an annulus whose radii differ by a fixed constant; comparison of its volume gives at most `C(j+1)^2` points. Summing the resulting bound proves the estimate, including the empty-sum case `R<h`. On bounded center sets and fixed cutoff, far sums have compact integration support and uniform smoothness, so ordinary Riemann sums converge uniformly. Sending h to zero before the cutoff radius handles the singularity without exchanging limits.

A local argument alone would not establish strong convergence on whole space. Here the omitted step is actually present and correct: the sampled input has uniformly bounded discrete L1 norm, and outside a ball containing twice its support both the discrete and continuum outputs are bounded by `C(1+|x|)^-3`. Their squared tails have integral `O(R^-3)`. Thus the dense-set convergence is in global L2, and the static lattice bound extends it to every L2 input. This argument proves strong convergence, with no static operator-norm claim.

The isometry uses the weighted sequence norm `h^3 sum |u_m|^2`; multiplication by this scalar weight changes neither the matrix nor its operator norm. With `J_h*` equal to cell averages, `J_h T J_h*` has the claimed action on cellwise constants, and its uniform norm is at most the fixed lattice norm.

### 3. Geometric masks

The actual hypothesis is volume consistency `(G)`. It implies strong multiplication-operator convergence because

    ||(M_h-M)u||_2^2=integral_{O_h triangle O}|u|^2 -> 0.

The right-hand side tends to zero for each L2 u by absolute continuity of the integral. This step does not assume an unknown eigenfunction has point values or regularity. Products of uniformly bounded strongly convergent operators therefore give static compressed convergence. Bounded O automatically puts O_h in a fixed box for all sufficiently small meshes. Empty or null supports cause no defect; the common-space extra zero eigenvalue is inside the lattice interval. The familiar boundary-null case does imply (G) for arbitrary translations by the vanishing measure of shrinking boundary neighborhoods.

### 4. Actual dynamic matrices and Hilbert-Schmidt convergence

The two-variable constant kernel on `Q_m x Q_n` integrates against a constant cell input with a factor `h^3`. Its output is exactly `sum_{n!=m} h^3 R_k(x_m-x_n)u_n`, and its same-cell block is zero. It therefore represents the actual matrix difference, with no cell-average replacement. Its Hilbert-Schmidt norm squared is `h^6 sum_{m!=n}|R_k(x_m-x_n)|_F^2`, consistently with the Frobenius norm of that weighted matrix.

Near the diagonal, center differences have length below `delta+sqrt(3)h`, so

    integral_{|x-y|<delta}|c_h|_F^2
      <= C h^6 #I_h sum_{0<|hj|<delta+sqrt(3)h}|hj|^-2
      <= C'(delta+h).

This correctly includes the count of occupied cells: `h^3 #I_h=|O_h|` is bounded. The continuum counterpart is at most `C delta`, since `r^-2` is locally integrable in dimension 3. In particular diagonal omission does not retain positive HS mass in the limit.

Away from a fixed diagonal neighborhood and for small h, center differences stay uniformly away from zero; the remainder is bounded and uniformly continuous there. Same-cell pairs cannot lie in that complement for sufficiently small h. The mask product differences are supported in

    ((O_h triangle O) x B) union (B x (O_h triangle O)),

which has vanishing volume in the common box. Hence the far kernels converge in L2. Taking h->0 and then delta->0 proves the asserted Hilbert-Schmidt convergence for arbitrary measurable supports satisfying (G). There is no hidden smooth boundary hypothesis.

### 5. Published static input suffices

The full source dependency is CDN (1.19), (1.21), Theorem 1.6, Sections 2.1-2.2, matrix extension Section 2.4/Lemma 2.7, and (3.38)-(3.49)/Proposition 3.15. Its conditions hold entrywise for the degree-two polynomial

    p_ij(x)=(delta_ij |x|^2-3x_i x_j)/(4 pi).

Each entry has zero spherical average. The Ewald decomposition expresses its lattice symbol as a rapidly summable Fourier part and a Gaussian-decaying Poisson part. The bounded homogeneous continuum symbol supplies the only potentially discontinuous Poisson term; it is still bounded. The omitted coefficient at zero is exactly zero because `p(0)=0`. This proves a bounded lattice convolution with precisely the zero diagonal and the desired off-diagonal entries. Realness, evenness, and matrix symmetry make it selfadjoint. The small-wavevector symbol limit gives inclusion of the continuum interval in the lattice numerical-range closure.

Only this boundedness, selfadjointness, and interval containment are needed. Compression to any finite occupied set inherits the form bound, even if geometric assumptions in a source statement about finite-section exhaustions or an instability converse require separate care. In particular the candidate does not need the source's stronger “if and only if” instability assertion. Arbitrary positive h is allowed because static homogeneity makes the entries independent of h; there is no reliance on h being reciprocal to an integer.

## Independent controls and their limits

Run `controls.py` with the parent's supplied Python environment and an output path within this directory. No author code is used. `CONTROL_RESULTS.json` records package versions and results.

- Exact SymPy radial identities and normalization passed. The integer numerator shell identities passed on all 427 nonempty squared-radius shells through 512, without rounded radicals. An exact rational h/translation check passed. The general symmetry proof above establishes all shells; finite checking is corroboration only.
- For `phi(y)=y_1^2 exp(-|y|^2)e1`, angular integration gives `(D phi)(0)=-2e1/15`. Independent finite lattice sums at h=1/2,1/4,1/8,1/16 have first-component errors approximately `9.70e-3, 3.06e-3, 8.06e-4, 2.04e-4`. The Gaussian sum is truncated to a radius-6 coordinate box, so these floating-point observations are illustration only.
- For unit-cube nested center grids, HS differences between the actual dynamic kernels at n and 2n cells per side decrease from about `0.3853` to `0.2212` for k=1.7 and `0.3218` to `0.1624` for k=1.2-0.8i as n runs 2,4,6,8. The fine-kernel squared mass in omitted coarse same-cell blocks decreases proportionally to the mesh scale. At k=0 every value is exactly zero. These computations compare actual embedded finite kernels and do not by themselves prove convergence to the continuum kernel.

## Source inspection and limits

`SOURCE_READ_MAP.json` pins both primary PDFs and their text extractions, identifies all read passages, and records which page images were checked. OWR printed pp.2580-2582/PDF pp.70-72 confirms the negative Hessian, factor 4 pi, h^3 weight, omitted diagonal, and `A_k-I/3` comparison. CDN PDF/printed pp.28-30 confirms (3.38)-(3.49); pp.14-15 and 17 confirm the exact Ewald/cancellation/matrix inputs. Source texts and rendered pages are private/ignored and are not in the safe authored manifest.

This is a bounded mathematical verification, not a formal proof certificate. It does not certify the exact numerical endpoints of the lattice interval; no such endpoint values are needed. It does not cover mesh-dependent frequencies or frequencies tending to infinity, unbounded supports, noncubic or anisotropic grids, or supports violating (G). The latter remain a distinct scope question. No broader priority audit was undertaken.

Assigned family completion estimate: **100%**. Strongest verified result: all kernel, normalization, static strong consistency, geometric-mask, and dynamic Hilbert-Schmidt convergence steps needed by the candidate are valid under its stated hypotheses. Remaining gap in this family: none found.

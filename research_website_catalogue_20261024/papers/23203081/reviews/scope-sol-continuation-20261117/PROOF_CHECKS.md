# Row 189 continuation: analytic proof and interface checks

This is a verification of the actual native and imported arguments, informed by the now-authorized packaged audits. It is not blind to those opinions. The frozen original-only reconstruction remains unchanged in the sibling INITIAL lane. Mathematical conclusions here are based on calculations below and exact primary interfaces, not on favorable author review statements.

## Central imported theorem: actual pinned proof body

I acquired every manuscript/build file listed in the native upstream inventory at OpenAI commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. All 13 acquired preprint objects, including the PDF, match their recorded SHA-256 values. I read main.tex and every included analytic section, the slab figure source and bibliography. The relevant dependency chain is reduction → moment coordinates → adjoint identities → density → tensor estimate → homogeneous variance → slab/all-body limits. The unrelated later measure/B-conjecture corollary was read but is not an interface needed for this note. No equality classification of logarithmic Brunn–Minkowski is assumed.

### Slab reduction

For widths h_i(t)=h_i(0)exp(t ell_i), the differentiated potential has first and second derivatives sum b_i psi_i and sum b_i² psi_i, b_i=-q ell_i. Thus (log Z)''=Var(dot V)-E(ddot V), with the correct sign. Gaussian domination covers both derivatives. At even q→infinity the integrand tends to the Gaussian indicator off finitely many bounding hyperplanes; epsilon→0 then recovers volume. Spanning normals ensure finite volume before taking nested dense direction sets. Continuity of finite measure from above gives the exact Wulff intersection for arbitrary positive continuous even support bounds. The separate interval computation covers dimension one; the follow-on uses n>=2.

### Moment construction

The truncated target is the ball B_R with density exp(-V)/Z_R. Berman–Berndtsson Theorem 1.1 supplies its smooth moment potential because the target contains zero, the weight is positive smooth, and evenness gives zero barycenter. Uniqueness after translating the minimum gives an even potential. Klartag's hypotheses apply to each ball, and the cap is 4/epsilon independently of R.

I checked the uniform coercivity rather than assuming a lower Hessian cap: supporting planes and E[z·grad(phi_R)]=n give phi_R(y)-phi_R(0)>=c|y|-n. The upper Hessian cap gives a quadratic upper bound. Normalization bounds phi_R(0) in both directions, hence a common integrable exponential majorant. The moment equation and cap give a positive determinant lower bound on each compact set, hence local eigenvalue lower bounds. The right side of the log equation is locally uniformly Lipschitz. A concave spectral extension of log gives the required uniformly elliptic equation; a priori interior estimates apply to already smooth truncations. Local smooth convergence and the common tail preserve mass and pushforward. Dense gradient image is strengthened to surjectivity by finitely many supporting slopes making each tilted potential coercive. No global lower Hessian bound is inserted.

### Adjoints and density

The source adjoint is partial*_k=x_k-partial_zk. Its row transformation gives delta_mu(tau)=x and A=x·grad-tau:D². Direct expansion of delta_mu(tau D²f tau) agrees with grad_z((A-1)f), so D_zW is symmetric and u=A(A-1)f. Double adjunction gives both first- and second-derivative pairings. Compact support in x remains compact in z because the inverse moment map is continuous.

For a centered even range annihilator g, weighted transposition produces A(A-1)g=0 in distributions. Its principal symbol is (xi·tau xi)², locally elliptic. The cutoff product expansion has coefficients 4,-12,-8. The resulting estimates control both Ag in L² and local gradient energy, using only tau's global upper bound. Splitting g=(g-Ag)+Ag gives a harmonic constant and an eigenvalue-one part. For the latter, eta_r v tends to v in graph norm; the compact Hessian identity forces its Hessian to vanish locally. Thus the obstruction is affine, and evenness plus centering remove it. I checked the negative terms, the cutoff annulus bounds and the graph limit; no assumed spectral improvement or global lower bound is used.

### Tensor estimate

The vector identity is E u²=E WᵀHW+E tr((D_xW)²). The second term is a matrix-square trace and is not replaced by a squared matrix norm. Twice differentiating the moment equation yields the displayed weighted-divergence formula for tau H tau-tau, with the negative cubic contraction. Integration by parts compares the two energy expressions.

A constant dual transformation at a fixed point normalizes tau to I; all derivative indices pair with opposite tensor variance, so the scalar contractions are invariant. No moving frame is differentiated. With S fully symmetric and J_ijk=h_ia C_ajk, the three remaining contractions give

    2||S||² + 4<S,J> + ||J||² + <J,J^(12)>.

Since J is symmetric in its last two slots, ||Sym J||²=(||J||²+2<J,J^(12)>)/3. Expanding squares gives exactly

    2||S+Sym J||² + (1/6)||J-J^(12)||².

The additional R term is nonnegative because R is symmetric. No positivity of the test Hessian h is required. This is a general algebra check; finite program agreement is corroboration only.

### Homogeneous variance

For each degree-q summand, H_i x=(q-1)grad psi_i and m_i=E tr(tau H_i)=q E psi_i. Polynomial cutoff errors vanish under Gaussian tails and the tau cap. The Hilbert–Schmidt inequality gives d_i²<=m_i E tr(MBH_iB); the H_i-semidefinite form gives E WᵀH_iW>=(q-1)d_i²/m_i. Adding and using the tensor energy yields sum d_i²/E psi_i<=E u². The denominators are positive because the density is positive and each normal is nonzero. Density extends the bound to every centered even L² test; scalar Cauchy–Schwarz yields the variance bound. The auxiliary Gaussian energies dropped in this step are nonnegative. This closes the central analytic chain, rather than transferring it to an unproved equivalent inequality.

## Exact primary interfaces

The linked sources were actually acquired; acquisition hashes and text are retained locally. I checked the stated hypotheses and the relevant proof passages, rather than relying on the author audits' conclusions. This does not claim to reprove every established theorem in those sources.

| Interface | Actual primary check and application |
|---|---|
| Compact moment solution | [Berman–Berndtsson, Theorem 1.1, journal p.651](https://numdam.org/item/10.5802/afst.1386.pdf): positive smooth weight on a convex target containing zero, zero weighted barycenter, gradient diffeomorphism and source-translation uniqueness. The normalized ball target meets these hypotheses. PDF page 4 personally viewed. |
| Uniform moment Hessian cap | [Klartag v1, Proposition 3.1 and Remark 3.5](https://arxiv.org/pdf/1309.2767v1): bounded smooth positively curved target; smooth convex density potential and bounded derivatives for each target; Hessian at least epsilon I. I read the finite-difference maximum argument and checked epsilon|u|²<=delta psi<=2t|u|, giving the cap 4/epsilon. PDF page 12 personally viewed. |
| Nonlinear interior estimate | [Wang's journal article, Corollary 2.3, pp.942–943](https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1806604056548241409-1806604056548241409-2398ebf5172d5f2f7f2c3b729bc59588.pdf): concave uniformly elliptic F on real Sym(n), C² solution, Hölder right side. It is not restricted to complex or even real dimensions. Both theorem/proof pages personally viewed. The newly served PDF differs from the old audit hash; see provenance limitations below. |
| Linear bootstrap | [Fernández-Real–Ros-Oton v1, Theorem 2.20 and Corollary 2.21, pp.46–47](https://arxiv.org/pdf/2301.01564v1): local a priori estimates for uniformly elliptic coefficients/right sides of the stated Hölder regularity. The truncation solutions are already smooth, so the a priori solution-class assumption is satisfied before passage to the limit. |
| Distribution smoothing | [Dyatlov's currently served notes, November 15, 2026, Theorem 15.2](https://math.mit.edu/~dyatlov/18.155/155-notes.pdf): an elliptic smooth-coefficient differential operator preserves singular support. I read the statement and parametrix-based proof passage. This supplies the local fourth-order smoothing interface. This is a newly identified current version, not the September 28 Theorem 14.2 cited by the manuscript. |
| Symmetric weak existence | [BBCY v2, Theorem 1.7 and Proposition 7.3](https://arxiv.org/pdf/1710.04401v2): -n<p<1, positive bounded density, full-dimensional convex body, prescribed Lp measure and closed-group invariance. I read Section 7, including the limiting multiplier/scaling and invariant variations/Haar averaging. G={I,-I} fixes the optimizing center and preserves the construction. The theorem's direct origin-interior statement is restricted to p<=2-n; the native proof correctly obtains interiority from symmetry instead. PDF page 4 personally viewed. |
| Global regularity ingredient | [BBC, Theorem 1.1(i) and Section 4 proof](https://www.renyi.hu/~carlos/lp-chou-wang-smoothness-jga.pdf): positive bounded density and p<1. Origin interior makes N(K,0)={0}, so the exceptional boundary set is empty. Boundary C¹ then supplies strict convexity of affine support charts. The proof uses support-cone geometry and localization; a bare local determinant bound is not substituted. PDF page 3 personally viewed. |
| Support smoothness | [Chou–Wang, author version, Proposition 1.2 and its proof](https://maths-people.anu.edu.au/~wang/publications/3-p-Minkowski.pdf): strictly convex support charts away from {h=0}, the generalized surface-measure equation, and smooth positive data give the required support regularity. This is the acknowledged 2005 author copy, not a byte-identical claim about the 2006 journal PDF. PDF page 9 personally viewed. |
| Classical nonsmooth interfaces | [BLYZ, Section 2 and Lemma 3.2](https://math.nyu.edu/~yangd/papers/LBMI.pdf): surface-measure weak continuity, almost-everywhere unique normals, Wulff contact, volume/cone-volume normalizations and uniform Wulff first variation. Ordinary BM equality gives positive homothety; differentiating its concave root-volume functional supplies the first-Minkowski equality case used by the native note. |
| Smooth transfer attribution | [He–Liu v1, Theorem 4 and complete Section 3 proof](https://arxiv.org/pdf/2510.21530v1): the conditional smooth target is explicit. Their convention uses sphere dimension n. The native local path avoids their global-path regularity assertion; positive-p arithmetic in that external proof is not needed by the native general-body route. |

## Follow-on deductions rechecked after primary reading

The unchanged INITIAL proof reconstruction contains the complete local calculations. I rechecked them against the now-read inputs:

1. Contact h_W=a only almost everywhere is sufficient in both mixed-volume sandwich bounds. Uniform quotient convergence and surface-measure weak continuity give the Wulff derivative for either sign. The log derivative produces integral log(h_L/h_K) dnu_K >= (1/n)log(V(L)/V(K)).
2. Strict Jensen for p>0 yields only S_K-almost-everywhere ratio constancy at equality. Classical first-Minkowski equality then recovers homothetic translates; symmetry removes translation. Identical unnormalized Lp measures give mixed volumes V(L) and V(K); n-p>0 forces equal volumes and scale. Atomic measures remain permitted.
3. At p=0, equal data fix V=M/n. The scale-invariant functional makes both candidate supports global minimizers. A local geometric support path retains positive curvature by openness, and constant weighted log integral plus LBM forces constant volume. Even variations yield the same PDE on a one-sided interval. Differentiating gives 0=-tr((Q^-1 A)²)-(n+1)w²+2h Q^-1(dw,dw). At both extrema, the gradient vanishes and similarity to a symmetric matrix makes the trace nonnegative. Both extrema are zero. No imported LBM equality class is used.
4. Existence follows from the exact invariant theorem, with full dimension and symmetry putting zero in the interior. BBC then supplies boundary C¹ and strict affine support charts, before Chou–Wang gives support regularity. Convexity gives Q>=0; the positive determinant gives Q>0. In ambient dimension two, the distributional ODE h''+h=f h^(p-1) directly bootstraps. This avoids a false density-only strict-convexity inference.

Scaling remains c^(n-p). The three masses are S_(K,0)=h dS, cone volume=h dS/n, and probability=h dS/(nV). Each signed box atom is respectively V/2, V/(2n), and 1/(2n). Distinct equal-volume boxes falsify arbitrary-measure uniqueness at p=0, while lying outside smooth positive-data hypotheses. Positive min h, full dimension, origin symmetry, p range and admissible support/curvature class are indispensable. I found no hidden boundary exception at n=2 or at the smooth p=0 endpoint.

## Limits and adversarial outcome

No substantive scientific defect was identified in the checked analytic chain. The complete pinned upstream analytic proof was read and checked, not merely its headline statement, a formal model, finite certificates, or author verdicts. General imported mathematical results remain attributed inputs, as in an ordinary mathematical proof. I did not kernel-build Lean, extract theorem axioms, run a comparator, or validate the full Lean development. The native note explicitly disclaims those achievements, and they are not premises of the analytic route.

The exact old Wang PDF was not reacquired: the server returned 163339 bytes instead of 163779 and a different hash. Extraction produced graphics-state diagnostics while exiting zero; relevant theorem/proof pages rendered legibly and were personally inspected. This fresh journal source supports the same real elliptic interface, but the old audit byte-level evidence is not reproduced. Dyatlov's live URL now serves November 15 notes with different numbering; the exact historical September version was not obtained or silently relabeled. Neither provenance distinction was concealed or treated as a scientific correction to the native proof.

No exhaustive novelty or priority certification was performed. The author expressly credits established reductions and disclaims first public announcement. Packaged prior-review assertions and their historical hashes remain evidence of what the author recorded, not mathematical premises or certificates for the final ZIP. No broader result, narrowed promotional replacement, extra experiment, or follow-up program is proposed.

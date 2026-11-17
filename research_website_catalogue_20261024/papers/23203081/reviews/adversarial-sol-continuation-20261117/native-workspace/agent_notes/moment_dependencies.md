# Independent audit: moment coordinates, external regularity and tensor estimate

Audit time: 2026-10-06 PDT (2026-10-07T04:13Z onward). Independent subagent: `moment_dependencies`.

Scope: `moment.tex`, `tensor.tex`, and associated identities needed in upstream family 091, tested against primary sources. Original follow-on target: smooth even log/Lp-Minkowski existence and uniqueness for ambient n >= 2, p in [0,1), plus arbitrary-body uniqueness for 0 < p < 1. This report does not certify the complete upstream theorem, follow-on proof, novelty, formalization, or publication package.

Checkpoint estimates for this delegated audit: mathematical verification 100%; publication-package review 0%. These are task accounting, not evidence or overall-project estimates.

## Verdict

No material defect was found in the moment-coordinate construction, cited dependency assumptions, or tensor estimate at pinned upstream commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The exact external statements fit the truncations; the upper Hessian cap is 4/epsilon; Wang's cited corollary is actually a general real uniformly elliptic theorem despite the title of his paper; the coordinate sum of squares is correct in every dimension.

The strongest verified result within this audit: smooth even V on R^n with D²V >= epsilon I admits a smooth even probability potential phi with 0 < D²phi <= (4/epsilon)I, gradient a global smooth diffeomorphism, and pushforward to Z^{-1}e^{-V}dx. The associated tensor energy lower bound also survives the direct contraction audit below. No assertion of complete formal verification is made.

I read the exact external statements and relevant local arguments. I did not rebuild Lean or reconstruct every proof in the external literature. The source clone remained read-only; no external individual was contacted.

## Source versions and primary evidence

| Upstream file | SHA-256 |
|---|---|
| build/moment.tex | 7e145c98d83124dcd250cad6b530c7e457a672249d76cab7ab7ba9e297049755 |
| build/tensor.tex | a4ff83463ed8aac5409de660da013161c12144cf8b431626c3ed2363112bd798 |
| build/identities.tex | 3726a4ff74c31c15f33f60f53ef2e6cf23ab1a38758e01886e8fb78c520c762c |

Also read project AGENTS.md, upstream references.bib and lean/docs/091.md. Primary-source URLs, byte sizes and hashes are recorded in `moment_dependencies_sources/download_manifest.json`. Full third-party PDFs/texts are research evidence only; exclude them from public uploads and commits unless redistribution rights are separately verified. The Numdam PDF bears restrictive copying language.

### Berman–Berndtsson2013, Theorem 1.1, journal p. 651

Primary source: https://numdam.org/item/10.5802/afst.1386.pdf; DOI 10.5802/afst.1386.

The theorem uses a convex body P containing zero in its interior and positive smooth g. It supplies a smooth convex phi satisfying g(grad phi)det D²phi=e^{-phi}, with gradient diffeomorphic from R^n onto int P, exactly when g(p)dp has barycenter zero. Uniqueness is up to source translations.

Apply P=closure B_R and g=e^{-V}/Z_R, with Z_R=integral over B_R. This g is globally smooth and pointwise positive, and bounded above/below on the compact target. Evenness ensures the barycenter condition. The equation becomes det D²phi_R=Z_R exp(V(grad phi_R)-phi_R). Change of variables shows integral e^{-phi_R}=1. The theorem's displayed equation uses the ordinary determinant, without a hidden n! factor. Translating the unique preimage of zero to zero fixes the minimum. Reflection and uniqueness force evenness. The fixed equation leaves no independent additive constant.

### Klartag1309.2767v1, Proposition 3.1 and Remark 3.5, pp. 9–13

Primary source: https://arxiv.org/pdf/1309.2767v1.

Hypotheses: bounded convex target, smooth convex rho with value and all derivatives bounded on it, centered probability density e^{-rho}; additionally smooth boundary with positive Gauss curvature and D²rho >= epsilon_0 I. The proof and remark give D²psi <= (4/epsilon_0)I for the source moment potential, independent of target radius.

Application uses B_R and rho_R=V+log Z_R. All derivatives are bounded for each R by smoothness on R^n; these bounds need not be uniform in R. D²rho_R=D²V >= epsilon I, giving exactly 4/epsilon. Klartag's psi is upstream phi_R, not its Legendre dual. Independently checking his maximum-principle scale: epsilon_0|u|² <= central difference <= 2t|u| gives central difference <= 4t²/epsilon_0. The arXiv history checked on the audit date lists only v1; no later version was substituted.

### Yu Wang2012, Corollary 2.3, journal pp. 942–943

DOI 10.4310/MRL.2012.v19.n4.a16. Actual 8-page journal PDF retrieved at current publisher endpoint:
https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1806604056548241409-1806604056548241409-2398ebf5172d5f2f7f2c3b729bc59588.pdf

The old URL returned 403. The shorter 2011 arXiv note lacks this exact corollary and was not treated as interchangeable.

Corollary 2.3 applies to every concave uniformly elliptic F on real Sym(n), f in C^alpha, and C² solution F(D²u)=f. It gives interior C^{2,beta} for some beta in (0,alpha), with constants depending only on n, ellipticity, alpha, |F(0)|, norm f and norm u. No complex Hessian or even real ambient dimension is required. The upstream alpha labels an output exponent; it need not equal the input Hölder exponent.

### Fernández-Real–Ros-Oton2301.01564v1, Theorem 2.20 / Corollary 2.21

Primary source: https://arxiv.org/pdf/2301.01564v1, printed pp. 46–47.

These are interior Schauder C^{2,alpha} and higher-order estimates for uniformly elliptic nondivergence equations with C^{k,alpha} principal coefficients and right sides. They are a priori statements. This is appropriate because each truncated phi_R is already smooth; the proof does not secretly apply them to an unproved weak-solution regularity class.

## Independent whole-space passage check

1. Evenness and uniform convexity imply V(x)>=V(0)+epsilon|x|²/2, hence finite positive Z. For fixed R, gradient image B_R gives |grad phi_R|<=R, and supporting planes with slopes ±(R/2)e_i supply linear coercivity. Thus the density has exponential tails. The normalized convex function g_R=phi_R-phi_R(0) satisfies 0<=g_R<=R|z|, so its expectation is finite.

2. Cutoff integration of div(z e^{-phi_R}) is justified by that tail and bounded gradient, yielding E(z·grad phi_R)=n. Supporting planes at z and -z give
   g_R(y)>=g_R(z)+|grad phi_R(z)·y|-grad phi_R(z)·z.
   Integration gives g_R(y)>=integral |x·y|dmu_R - n. The density on B_1 has uniform lower bound e^{-max_{B_1}V}/Z. Rotational invariance of B_1 yields c|y|-n<=g_R(y).

3. The Hessian cap C=4/epsilon gives g_R(y)<=C|y|²/2. Probability normalization implies e^{m_R}=integral e^{-g_R}, where m_R=phi_R(0). Gaussian lower and exponential upper integrals bound m_R uniformly. This produces a common integrable exponential majorant for the actual densities e^{-phi_R}.

4. On each fixed ball, phi_R and its gradient are uniformly bounded. The equation and Z_2<=Z_R<=Z give a uniform positive lower determinant bound. Every Hessian eigenvalue is at most C, so its smallest is at least det/C^{n-1}. Thus locally delta I<=D²phi_R<=CI, uniformly in R. The logarithmic right sides are uniformly Lipschitz because their gradient is D²phi_R grad V(grad phi_R)-grad phi_R, with V evaluated on a fixed compact set.

5. Extend scalar log from a neighborhood of [delta,C] to smooth concave s on R with positive upper/lower derivative bounds, by continuing its decreasing positive derivative to constant positive tails. Then F(Q)=tr s(Q) is concave, uniformly elliptic on all real symmetric matrices, smooth even at repeated eigenvalues, and equals log det on these Hessians. Its constants are fixed for the local ball, independent of R. Wang Corollary 2.3 applies after fixed rescaling; the Lipschitz right sides give uniform C^alpha norms for any fixed alpha<1.

6. Differentiating with w=partial_k phi_R gives
   (D²phi_R)^{-1}:D²w = grad V(grad phi_R)·grad w - w.
   Principal coefficients and right side are uniformly C^beta on smaller balls, and the coefficients are uniformly elliptic. The cited Schauder estimates give uniform C^{3,beta} bounds for phi_R; iteration supplies all derivative bounds. A diagonal smooth subsequence retains the locally positive lower bound and global upper cap.

7. Dominated convergence proves probability normalization and pushforward against bounded continuous tests. Positive Hessian yields local invertibility and strict gradient monotonicity, hence injectivity. Pushforward to an everywhere positive density implies dense image. For any x_0, choose finitely many image points close to x_0±e_i; their convex hull contains a ball about x_0. Their supporting planes make phi(z)-x_0·z coercive, so it attains a minimum at grad phi=x_0. This proves surjectivity, not just density. Local inverses combine to a smooth global inverse. Compact target supports have compact inverse images under the continuous inverse.

No global uniform positive lower Hessian bound is used or claimed. The whole-space limit does not require derivative bounds on V uniform across target truncation radii. No unsupported boundary condition at infinity is inserted.

## Independent tensor audit

Definitions in target coordinates: h=D²_x f, P=tau h, B=tau h tau, tau=D²_z phi, M=tau^{-1}. Negative weighted divergence is delta_mu, and source adjoint is partial*_k=x_k-partial_{z_k}.

Direct expansion verifies W=grad_z[((A-1)f)(grad phi)] with A=x·grad_x-tau:D²_x. Thus D_z W really is symmetric; D_x W need not be. The commutator [partial_l,partial*_k]=tau_kl gives D_z W=B+R with R symmetric, making tr(MRMR)=||M^{1/2}RM^{1/2}||² nonnegative. Prematurely substituting a Hilbert–Schmidt norm for tr((D_x W)²) would be incorrect, but the manuscript does not do so.

Twice differentiating the moment equation independently yields
(tau H tau-tau)_{ij}=(partial_d-x_d)(M_{dk}C_{ijk})-tr(MC_i MC_j),
where C=D³_z phi and H=D²_xV. The cancellation uses partial_d M_{dk}=-c_b M_{bk} and M(x+c)=grad_xV. The sign agrees with negative weighted divergence.

For Q=h tau h, integration by parts leaves a nonnegative R term and three contractions. They are invariant under a constant dual coordinate change z=Tz', x'=T^T x. The potentials transform as phi'=phi∘T-log|det T|, V'=V∘T^{-T}, and Z'=|det T|Z, preserving the moment equation and probabilities. Derivative indices are covariant, h and H have contravariant indices, and P has one of each. Taking T=tau^{-1/2} at the chosen point gives tau=I. All derivatives are computed with T constant; no moving-frame derivatives were omitted.

In that frame set S_{ijk}=f_{ijk}, J_{ijk}=h_{ia}C_{ajk}. S is fully symmetric and J symmetric in its last two indices. Direct contractions are:

- cross term = 2||S||²+2<S,J>;
- derivative of Q = 2<S,J>+<J,J^{(12)}>;
- cubic term = ||J||².

Full symmetrization is Sym J=(J_{ijk}+J_{jik}+J_{kij})/3. Relabeling indices gives ||Sym J||²=(||J||²+2<J,J^{(12)}>)/3 and <S,Sym J>=<S,J>. Thus their total is
2||S+Sym J||²+(1/6)||J-J^{(12)}||²>=0.
This is a general all-dimensional algebra proof with no positivity assumption on h. The weighted vector-field identity E(delta_mu W)²=EW^THW+E tr((D_xW)²), with precisely the matrix square, completes the tensor lower bound.

Supplement: `moment_dependencies_tensor_check.py` checks six contraction identities using exact rational arithmetic, including indefinite h, in 250 deterministic cases in dimensions 1–5. It passed. This is a finite-dimensional regression/falsification check, not a replacement for the all-dimensional proof. It uses only Python 3's standard library.

## Remaining project gap

This narrow route is not blocked. Overall resolution still requires the rest of the upstream proof, endpoint transfer, arbitrary-body equality proof, priority and attribution, complete package reviews, publication, DOI and tracker verification. A favorable verdict here supplies no certification of those tasks.

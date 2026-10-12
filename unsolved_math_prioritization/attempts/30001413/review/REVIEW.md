# Independent review: hinged-plate positivity partial (30001413)

**Verdict: PASS_SCOPED_LINEAR_REGULARITY_AND_NEAR_NAVIER_RESULTS.** No mandatory correction. Preserve **unsolved, 2/5 approaches** for the broad optimal-domain question.

Reviewed `PARTIAL_SOURCE_AUDIT.md`, SHA256 `e0a92b317f81e5d5aba96fa5e4ebfcc958c65ab3668cb050fa575327ca3ef60f`. The reviewer used gpt-6-astra at xhigh. This is independent AI mathematical/source review, not human peer review or a priority certification.

## 1. The actual operator and source quantifiers

I read the original Parini–Stylianou OWR contribution on printed pp.335–336 and visually checked the theorem and concluding domain question. Its functional is the stated Kirchhoff–Love energy on H²(Omega) intersect H¹_0(Omega), with L² loads and mathematical parameter interval −1<sigma<1. The smaller physical interval ends at 1/2. The curvature sign is nonnegative on convex boundary pieces and the derivative is outward normal.

The natural weak equation has the boundary bilinear term

    −(1−sigma) integral_boundary kappa u_n phi_n.

This is not ordinary Navier data except at sigma=1 or where the curvature contribution vanishes. The artifact keeps the actual variational operator; it does not invoke a second-order factorization as a substitute on rough or nonconvex domains.

The original theorem includes positivity for every nonzero nonnegative L² load and a distance-to-boundary estimate. Its final question asks whether the domain assumptions are optimal. The submitted results establish credited sufficient improvements and retain the unresolved optimality distinctions. In particular, its direct C¹,¹ proposition asserts positivity and superharmonicity, without silently claiming an independently proved sharp quantitative boundary estimate.

## 2. Published coverage of the regularity improvement

I checked the full published Romani 2017 article, especially Theorem 4.7, Proposition 4.9 and Remark 4.10. Theorem 4.7 gives the determinant boundary identity for every H² function with zero boundary trace on a bounded planar C¹,¹ domain. Convexity is not needed for that identity. The proof uses H² approximation by C¹,¹ zero-trace functions and continuity of both sides.

Remark 4.10 explicitly discusses forcing independent of u and says that the **linear** Kirchhoff–Love positivity result extends to bounded convex C¹,¹ domains. Thus the attribution is supported by a specific linear statement, rather than an inference from a semilinear abstract. The independent linear argument below also verifies the all-load scope.

The Antunes–Gazzola 2013 C² result corroborates the source status. The later Romani result on nonconvex limaçons concerns nonlinear ground states with a threshold; it is not an all-load linear inverse theorem. The submitted text correctly excludes that substitution and the separate stressed-plate operator.

## 3. Direct linear variational proof

In normalized Hessian coordinates (p,q,sqrt(2)r), the quadratic form has matrix

    [1 sigma 0; sigma 1 0; 0 0 1−sigma].

Its eigenvalues are 1+sigma and1−sigma, the latter repeated. For −1<sigma<1 it is bounded below by (1−|sigma|) times the squared Frobenius norm of the Hessian. Poincare and integration by parts control the lower derivatives on H² intersect H¹_0. Consequently the form is coercive, the load is continuous, and the energy is strictly convex. Existence and uniqueness hold for every L² load.

Polarization of the credited determinant identity gives exactly the displayed weak curvature problem, with the correct factor 1−sigma. No pointwise trace of Delta u for a general H² function is needed.

For f≥0, solve −Delta w=|Delta u| with zero Dirichlet trace. C¹,¹ L² regularity gives w in H² intersect H¹_0. The equations

    −Delta(w−u)=|Delta u|+Delta u≥0,
    −Delta(w+u)=|Delta u|−Delta u≥0

and the weak second-order maximum principle imply w≥u and w≥−u.

The normal-trace signs used next are valid at this regularity. One can justify them in local C¹,¹ graph coordinates: flatten the boundary, use zero trace to write the inward difference quotient as the average of the inward derivative, and use the H¹ trace continuity of the gradient to obtain convergence in L² on the boundary. Nonnegative quotients have nonnegative limits. The zero tangential trace then identifies the resulting sign with the outward normal derivative. Thus a nonnegative H² zero-trace function has outward normal trace≤0 almost everywhere. Applied to w±u, this gives w_n≤±u_n, hence w_n≤−|u_n| and w_n²≥u_n².

The Laplacian norms of w and u coincide. Convexity of the domain gives kappa≥0 almost everywhere, and 1−sigma>0. Therefore both terms in the submitted energy difference are nonpositive. Since u is the unique minimizer, w=u. It follows that u≥0 and −Delta u≥0. For a nonzero load, the weak equation rules out u=0; the strong second-order maximum principle gives strict interior positivity.

Only non-strict comparisons are necessary. In general the auxiliary function could equal |u| without equaling u; the submitted argument does not rely on an overstrong strict alternative or on |u| belonging to H². Its use of strict convexity closes the comparison correctly.

## 4. Stadium and the separately quantified nonconvex conclusion

The stadium is bounded, convex and connected. Its straight and circular pieces have matching tangent directions and a Lipschitz tangent field, so its boundary is C¹,¹. At the specified join, its graph has matching first derivative 0 but second derivatives 0 and −1 on the two sides. It is not C². The same stadium therefore satisfies the credited positivity conclusion for every −1<sigma<1 and every nonnegative L² load while lying outside the original C²,¹ class.

I read Gazzola–Sweers 2008 Definitions 2.1–2.2, Theorems 2.3 and 4.1 and the relevant proof/application discussion, and visually checked Theorem 4.1 on printed p.407. It concerns the same H² intersect H¹_0 weak form and continuous, possibly signed alpha on any fixed bounded C² domain. The constants delta_c<0<delta_1 depend on the domain, and the positivity assertion holds for all nonzero nonnegative L² loads when alpha lies strictly between them. The case delta_c=−infinity is allowed.

For a fixed C² planar domain, signed curvature is continuous and bounded. With K=||kappa||_infinity and the submitted eta and epsilon,

    |(1−sigma)kappa| < eta

throughout 1−epsilon<sigma<1. This places alpha=(1−sigma)kappa strictly inside the theorem's window. The same epsilon works for all loads: it depends on the domain and theorem constants, not on f. The determinant identity identifies this solution with the unique minimizer of the original energy.

On the annulus 1<|x|<2, the outward-normal curvature is 1/2 on the outer component and −1 on the inner component. The domain is connected, smooth and nonconvex. The theorem therefore gives genuine positivity for the curvature-dependent problem at some sigma values strictly below1, not only at the Navier endpoint. It does not give superharmonicity on that annulus; indeed the cited theorem separately notes the obstruction when alpha is negative somewhere. The artifact makes no such nonconvex superharmonicity claim.

The near-1 interval is domain-dependent and may lie entirely above the physical interval. No annular threshold has been computed. No positivity conclusion for every sigma in (−1,1), for an arbitrary prescribed sigma, or for every rough nonconvex domain follows.

## 5. Checks and verdict limits

All **3,242** submitted controls reproduce with a byte-identical receipt. The independent checker uses a matrix/Sylvester coercivity test, a determinant divergence identity, radial annular boundary integrals with both curvature signs, non-strict normal-trace factorization and rational coefficient-window checks. All **917** independent exact assertions pass; the receipt is `independent_results.json`. Reproduce with `python independent_checks.py`; reproduce the submitted receipt with `cd author_replay && python verify.py`. SymPy is used for the exact algebra.

The tests do not establish an unknown Green-function sign or compute delta_c and delta_1. The universal statements rest on the variational argument and the precise credited theorems checked above. No substantive gap was found in the partial claims. The optimal geometric characterization, minimal regularity, and a sigma-uniform nonconvex replacement remain unproved by this package.

## Primary sources

- [Original OWR8/2010](https://ems.press/content/serial-article-files/46265), pp.335–336
- [Romani 2017, published Analysis & PDE article](https://msp.org/apde/2017/10-4/apde-v10-n4-p06-s.pdf), Theorem 4.7, Proposition 4.9 and Remark 4.10
- [Gazzola–Sweers 2008, full published paper](https://gazzola.faculty.polimi.it/hinged.pdf), Definition 2.1, Theorems 2.3 and 4.1
- [Antunes–Gazzola 2013](https://www.numdam.org/item/10.1051/cocv/2012014.pdf), Theorem 2.1 and Corollary 2.2
- [Romani later semilinear results](https://arxiv.org/abs/2304.14945v3), checked for scope only

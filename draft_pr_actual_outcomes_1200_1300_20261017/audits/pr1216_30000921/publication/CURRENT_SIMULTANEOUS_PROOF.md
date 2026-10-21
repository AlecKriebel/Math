# Simultaneous polynomial failures: elementary proof

This is a current added argument, distinct from the original fixed-polynomial construction. It is an attributed historical negative-answer note: older Gaussian hypercyclicity theorems already imply its existence conclusion, even for frequently hypercyclic functions. No new first solution, first existence theorem, or current-openness claim is made. AI tools were used extensively; this is unrefereed, without external human peer review or formal proof-assistant certification.

Let H(C) have the compact-open topology and let D be differentiation. There is a dense set B of functions f in HC(D) such that, for every nonconstant complex polynomial p,

    |(pf)^(n)(0)| -> infinity.

The same f works for all p; the threshold in n may depend on p. The assertion concerns pointwise multiplication p(z)f(z), not P(f) or p(D)f.

Put ell_n=(n+1)^(-1/2), u_n=log(n+e), and

    X_M={f in H(C): ell_n <= |f^(n)(0)| <= u_n for n>=M}.

Each X_M is a nonempty closed subset of the complete metrizable space H(C), hence complete in a compatible relative metric. The baseline series sum ell_n z^n/n! is entire. Since u_n<=n+1, all series with these eventual jet bounds converge normally on every disk, and their bounded tails tend to zero uniformly over X_M after a fixed finite prefix.

## Relative density of hypercyclic functions

Fix a Gaussian-rational polynomial q(z)=sum_(k=0)^d beta_k z^k/k!, an integer radius R>=1 and s>=1. The relative hitting set U(q,R,s)=union_(N>=0){f in X_M: ||D^N f-q||_R<1/s} is open by continuity of differentiation.

To prove density, fix g in X_M and a compact-open neighborhood, represented by ||f-g||_r<epsilon. Choose L>=M so that 2 sum_(n>L) u_n r^n/n!<epsilon. For sufficiently large N>L, retain the jets of g through L, use baseline ell_n after L, and replace the block N,...,N+d with gamma_k chosen by radial clipping of beta_k outward to modulus ell_(N+k), retaining beta_k when it is already outside that disk. At beta_k=0 choose the positive boundary point. Then

    |gamma_k-beta_k|<=ell_(N+k),
    ell_(N+k)<=|gamma_k|<=max(1,|beta_k|).

As u_n tends to infinity, the finite block also satisfies its upper bound when N is sufficiently large. The resulting F_N lies in X_M and stays in the neighborhood because all its changed jets lie beyond L and both tails are bounded by u_n. All retained low jets vanish under D^N. Every normalized jet of D^N F_N-q has modulus at most ell_N: on the target block by clipping, and afterward by the decreasing baseline. Therefore

    ||D^N F_N-q||_R <= ell_N exp(R) -> 0.

Thus U(q,R,s) is relatively dense. Baire inside X_M, applied to the countable triples of Gaussian-rational q and integer R,s, proves HC(D) intersect X_M is dense in X_M. No assertion that X_M is invariant under D is used.

## Escape for all nonconstant polynomials

For a_n=f^(n)(0), f in X_M, and p(z)=sum_(j=0)^d c_j z^j, c_d nonzero, d>=1, Leibniz gives for n>=M+d

    (pf)^(n)(0)=sum_(j=0)^d c_j (n)_j a_(n-j).

The top-degree contribution has modulus at least |c_d|(n)_d /sqrt(n-d+1), of order n^(d-1/2). The sum of all lower contributions has modulus at most C_p n^(d-1)log(n+e), C_p=sum_(j<d)|c_j|. Its ratio to the leading lower bound tends to zero. Reverse triangle gives divergence to infinity. This includes d=1 and arbitrary complex phases. The bounds on f were fixed before p; there is no intersection indexed by uncountably many polynomials and no uniformity in p is claimed.

Evaluation at zero is continuous and onto C. A scalar sequence with escaping tail cannot be dense: choose a small disk avoiding its finitely many initial values inside a disk avoided by its tail. Hence pf is not HC(D).

## Ambient density and category

Given any entire target g on a disk, first approximate it by a polynomial P. For M>deg P sufficiently large, P+sum_(n>=M)ell_n z^n/n! lies in X_M and is arbitrarily close to P. Relative density then gives a nearby member of HC(D) intersect X_M. Thus B=union_M(HC(D) intersect X_M) is dense in H(C).

Each X_M is closed with empty ambient interior, since all polynomials lie outside X_M and polynomials are dense. Thus this B is meagre; this is compatible with Costakis's2008 residual family on which all nonzero polynomial products are hypercyclic. Nonzero constant multiplication preserves HC(D) by scaling each orbit; zero and every nonconstant polynomial do not preserve the entire class. Universal polynomial preservers are exactly the nonzero constants.

## Prior implication and attribution

Nikula arXiv1209.6209v1 Theorem1 (repository submission2012-09-27, theorem PDF pp2–3) states that IID full-complex-support jets satisfying a weak tail condition give an almost surely entire frequently D-hypercyclic series. Standard circular complex Gaussian jets qualify. Their small-ball and large-tail probabilities imply by Borel–Cantelli that eventually (n+1)^(-3/4)<=|a_n|<=log(n+e). The same leading-degree argument gives all-polynomial escape, and polynomial additions give a dense family. Thus the simultaneous negative answer already follows as an elementary corollary of an older theorem, even with frequent hypercyclicity. We do not claim that the exact multiplier corollary was explicitly printed there, nor identify the first explicit disproof. Further earlier general Gaussian-measure routes are recorded in the priority audit.

Radially clipping Gaussian jets to the exact X_M annuli changes a bounded sequence of jets by c_n->0 (upper violations are only finite). The entire correction h has ||D^n h||_R<=exp(R) sup_(k>=n)|c_k|->0, which preserves frequent hypercyclicity. The clipped product law has full support in X_M by coordinate support and uniform factorial tails. Hence even density of frequently hypercyclic functions in each X_M follows from the older theorem plus elementary estimates. This exact-annulus observation is also not claimed as new. The self-contained Baire argument above provides an alternative proof without invoking random hypercyclicity.

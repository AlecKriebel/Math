# Independent priority and mechanism review: PR 466 / problem 30000999

Audit target: frozen `release/PROOF.md` and `release/SOURCE_GATE.md`, read only after writing `INITIAL_HYPOTHESIS.md` and opening the independent search ledger. No older audit, peer verdict, repository history, queue, or chat was consulted. This report separates mathematical correctness from priority.

## Decision

The frozen proof establishes its full stated strengthened theorem: for each fixed ambient integer n >= 3, each fixed real 1 <= p < infinity, and each fixed 0 < a < 1, the displayed even smooth densities in [1-a,1+a] have an inverse W_p ratio tending to infinity. The sufficient lower rate k^((n-2)/(2p)) is correct. The circle-even isometry is correct. I found no central mathematical gap in this mechanism.

The original unrestricted question is a direct classical parity/nullspace consequence. The official source does print the question, but its negative answer already follows from the defining equators, without any high-frequency argument. It should not be promoted as a novel resolution of a substantive previously open unrestricted inverse problem. The stronger even statement must be evaluated on its own merits; lack of an exact prior printing does not restore the original question's novelty or open status.

The exact all-real-finite-p, fixed-amplitude localization statement was not located in this bounded public search. That is an unresolved priority gap, not a novelty finding. In addition, the p=1 and p=2 even conclusions already follow directly from classical spectrum plus standard transport facts, with stronger rates than the note records for p=2.

## Original primary source and implication

Benjamin K. Stephens, “Measuring the Geodesic Radon Transform with Mass Transport,” *Calculus of Variations*, Oberwolfach Report 31/2008, workshop 6-12 July 2008, printed pp. 1762-1764; DOI [10.4171/OWR/2008/31](https://doi.org/10.4171/OWR/2008/31). Independently retrieved [official report](https://ems.press/content/serial-article-files/46174), SHA-256 `15854a33755fcaae9620944f730823932f48c32f6a56b9ce057c0b1b5862e54f`; printed p. 1763 was locally rendered and visually inspected. It defines normalized equator averages, their measure dual, intrinsic spherical W_p, and p in [1,infinity). Its final paragraph asks for a uniform reverse contraction factor. The passage's measure class is all probability measures, with no evenness or support restriction. The workshop and report volume are from 2008, while the [official EMS metadata](https://ems.press/journals/owr/articles/2042) records publication on 30 June 2009 (and submission on 6 July 2008). A blanket inference that a 2009 label is erroneous is therefore unsupported; the dates describe different stages of the same source.

Own deduction directly from that definition: E(u)=E(-u), so R delta_u=R delta_-u, whereas W_p(delta_u,delta_-u)=pi. No uniform inverse modulus vanishing at zero can hold. The same parity mechanism gives smooth positive distinct densities 1+a x_1 and 1-a x_1 with identical images. Thus restricting merely to smooth positive measures does not repair the original formulation.

This conclusion does not assert anything about Stephens's intended unstated repair, what workshop participants knew, or an exact historical publication announcing a negative answer. None is needed for the mathematical implication just checked.

## Independently checked mechanism

Put alpha=(n-2)/2>0. For even k=2m, use H_k=Re(x_1+i x_2)^k and r=(x_1^2+x_2^2)^(1/2). Its Euclidean Laplacian vanishes because the polynomial is holomorphic in the first two coordinates. Restriction to the sphere gives -Delta_S H_k=L_k H_k, L_k=k(k+n-2). Plane rotation by pi/k changes the sign, proving zero mean. Even k gives antipodal evenness. The Euclidean gradient norm is k r^(k-1), and projection to the tangent space can only decrease it; hence H_k/k is 1-Lipschitz for the intrinsic metric.

For a uniform vector X on a d-dimensional unit sphere, the polynomial moment identity

    E[(v dot X)^(2m)] = (2m-1)!! / product_{j=0}^{m-1}(d+2j) * (v dot v)^m

is obtained for real v by rotational invariance and one-coordinate moments, then extends to complex v as a polynomial identity. The dot product remains bilinear. With w=e_1+i e_2 and v=(I-u u^T)w, one has v dot v=-(w dot u)^2. Setting d=n-1 and taking real parts gives

    F H_(2m) = lambda_(2m) H_(2m),
    lambda_(2m)=(-1)^m product_{j=0}^{m-1}(2j+1)/(n-1+2j).

There is no zero even eigenvalue. Its modulus equals Gamma(alpha+1/2) Gamma(m+1/2)/(sqrt(pi) Gamma(m+alpha+1/2)) and is asymptotic to a positive constant times k^(-alpha).

Gaussian spherical coordinates give r^2 ~ Beta(1,alpha). Consequently

    M(q)=int r^q d sigma=Gamma(alpha+1) Gamma(q/2+1)/Gamma(q/2+alpha+1), q>=0.
    int H_k^2 d sigma=M(2k)/2.
    ||grad_S H_k||_p<=k M(p(k-1))^(1/p).

The conditional angular factor has mean cos^2(k theta)=1/2. These formulas apply to real p; no integer-order extension or analytic continuation in p is being assumed.

The density rho_k=1+a H_k has integral one and fixed bounds 1-a<=rho_k<=1+a. Self-adjointness follows from symmetry of the orthogonal-pair probability measure, so R(rho_k sigma)=(1+b_k H_k)sigma with b_k=a lambda_k. The input lower bound is the elementary Lipschitz-test inequality together with W_p>=W_1:

    W_p(rho_k sigma,sigma)>=a M(2k)/(2k).

For the output, take eta_t=1+t b_k H_k and v_t=b_k grad_S H_k/(L_k eta_t). The density remains at least 1-a, and

    partial_t eta_t+div_S(eta_t v_t)=b_k H_k+(b_k/L_k)Delta_S H_k=0.

For each k this is a globally smooth vector field on the compact sphere. The smooth flow pushes sigma to eta_t sigma, and its endpoint map supplies a coupling. Length bounds, convexity of z^p for p>=1, and the flow change of variables give

    W_p((1+b_k H_k)sigma,sigma)
      <=a|lambda_k| (1-a)^(-(p-1)/p) M(p(k-1))^(1/p)/(k+n-2).

No optimality of the flow, uniform derivative bound, Sobolev equivalence, or linearization theorem is needed. The image differs from sigma because b_k and H_k are nonzero, ensuring a positive denominator. Dividing the two bounds gives exactly

    ratio >= (k+n-2)/(2k) * (1-a)^((p-1)/p)
             * M(2k)/(|lambda_k| M(p(k-1))^(1/p)).

The moment and spectrum exponents cancel as (-alpha)-(-alpha)-(-alpha/p)=alpha/p. Its asymptotic multiplicative constant is positive for each fixed n,p,a. This proves the advertised divergence, including p=1, nonintegral p, and arbitrarily large finite p.

## Primary prior context and what it actually implies

1. Michael Quellmalz, “The Funk-Radon transform for hyperplane sections through a common point,” *Analysis and Mathematical Physics* 10, article 38, published 11 August 2020; [DOI 10.1007/s13324-020-00383-2](https://doi.org/10.1007/s13324-020-00383-2). The publisher's full text was read. Theorem 4.1's proof identifies the classical odd nullspace; Proposition 6.1 gives the even Sobolev isomorphism with smoothing degree (d-2)/2 and expressly attributes it to Strichartz, Lemma 4.3. Its ambient d equals this note's n. This is spectral context, not an exact prior W_p theorem.

2. Robert S. Strichartz, “L^p estimates for Radon transforms in Euclidean and non-Euclidean spaces,” *Duke Mathematical Journal* 48(4), 699-727 (1981); [DOI 10.1215/S0012-7094-81-04839-0](https://doi.org/10.1215/S0012-7094-81-04839-0). Quellmalz's primary paper attributes the precise Sobolev statement to Lemma 4.3. The 1981 full text was not successfully retrieved through the DOI/Project Euclid attempts; its exact lemma page is therefore not independently attested here. Attribution should be phrased accordingly.

3. T. N. Bailey, M. G. Eastwood, A. R. Gover, L. J. Mason, “Complex analysis and the Funk transform,” *Journal of the Korean Mathematical Society* 40(4), 577-593, July 2003; [DOI 10.4134/JKMS.2003.40.4.577](https://doi.org/10.4134/JKMS.2003.40.4.577). Its authored paper's p. 577 states the smooth odd-nullspace characterization and credits Funk (1913). The paper text was available in an indexed PDF copy; date and bibliographic metadata were independently checked in [Oxford's institutional record](https://ora.ox.ac.uk/objects/uuid%3Ae87019f5-5d16-4252-9dce-bafd6756fb72). This independently documents that the relevant nullspace fact predates the 2008 question. It concerns S^2; the direct antipodal argument above covers every defined ambient n.

4. Remi Peyre, “Comparison between W_2 distance and H-dot^{-1} norm, and localisation of Wasserstein distance,” *ESAIM: COCV* 24(4), 1489-1501 (2018); [DOI 10.1051/cocv/2017050](https://doi.org/10.1051/cocv/2017050); [author preprint](https://arxiv.org/pdf/1104.4631), first submitted 24 April 2011. The retrieved manuscript's Theorem 1/Corollary 3 are on pp. 2-3, and Theorem 5 is on p. 4. They compare intrinsic W_2 with a negative homogeneous norm on connected Riemannian manifolds; the lower comparison requires nonnegative Ricci curvature and upper density bounds. The sphere satisfies this curvature assumption. The theorem numbering just given is the manuscript's, not independently checked publisher numbering.

5. D. A. Edwards, “On the Kantorovich-Rubinstein theorem,” *Expositiones Mathematicae* 29(4), 387-398 (2011); [DOI 10.1016/j.exmath.2011.06.005](https://doi.org/10.1016/j.exmath.2011.06.005). The publisher's Section 1, equation (1.3), states the compact-metric W_1 duality. It identifies the transport distance with a norm of the signed difference, so scalar multiplication of that difference multiplies W_1 exactly. The result is explicitly classical.

6. Philip Greengard, Jeremy Hoskins, Nicholas Marshall, Amit Singer, “On a linearization of quadratic Wasserstein distance,” [arXiv:2201.13386](https://arxiv.org/abs/2201.13386), submitted 31 January 2022, v2 1 March 2022. Retrieved pp. 1-3 and Section 3.5. It supplies quadratic local-linearization context on bounded convex Euclidean domains and cites classical antecedents. It does not establish the full intrinsic spherical, fixed-amplitude, all-p statement and is not used as such.

7. Vincent Divol, “Measure estimation on manifolds: an optimal transport approach,” [arXiv:2102.07595](https://arxiv.org/abs/2102.07595), first submitted 15 February 2021. The current retrieved manuscript has Proposition 2.8 on p. 5, negative-norm definition (2.2) on p. 4, and the flow argument in Appendix B, pp. 25-26. It provides a related general-p flow construction, but defines Wasserstein by ambient chord distance and prints a p^(-1/p) factor. I did not import that factor or transfer its metric convention to the present intrinsic problem. The frozen proof's own coupling calculation avoids those issues entirely.

## Stronger classical special-order consequences (own deductions)

For p=1, let N(H)=sup_{Lip(phi)<=1} int phi H d sigma. Compact-metric Kantorovich-Rubinstein duality gives

    W_1((1+a H_k)sigma,sigma)=a N(H_k),
    W_1((1+a lambda_k H_k)sigma,sigma)=a |lambda_k| N(H_k).

Thus the ratio is exactly |lambda_k|^(-1), of order k^alpha. No harmonic localization is required for this deduction.

For p=2, -Delta_S H_k=L_k H_k implies the homogeneous negative norm at sigma is ||H_k||_2/sqrt(L_k), by integration by parts and Cauchy-Schwarz, with equality testing phi=H_k. Applying Peyre's upper and lower comparisons, while accounting for normalized versus unnormalized volume, gives at least

    W_2((1+a H_k)sigma,sigma) / W_2((1+a lambda_k H_k)sigma,sigma)
      >=(1/2) sqrt((1-a)/(1+a)) |lambda_k|^(-1).

All constants are independent of k. This proves order k^alpha divergence for p=2 from published tools, stronger than the frozen note's sufficient k^(alpha/2) lower rate. These are deductions from classical results, not assertions that the exact displayed theorem was printed in those papers.

For other p, a general intrinsic W_p tangent-norm theorem would plausibly yield another short route, but no such theorem with every required hypothesis and uniformity was verified in this audit. That route is not used to claim prior coverage, and is not needed to validate the note.

## Boundaries, limits, and unresolved gaps

- For n=2, E(u) has two points. With J the pi/2 rotation, R mu=(J_#mu+(-J)_#mu)/2. On even measures this reduces to J_#mu. Rotation is a metric isometry, and pushing any coupling forward, then using J inverse, proves equality of W_p distances, including p=infinity. No injectivity loss remains on the even circle.
- The Beta(1,alpha) law was used only for alpha>0. At n=2, r=1 identically and |lambda_(2m)|=1; the asserted divergence cannot be extended there.
- The vector fields and densities are smooth for each k; derivative norms need not be uniformly bounded. The theorem does not decide fixed regularity, finite-bandwidth, support, or inverse-modulus variants.
- No p=infinity even-density divergence follows by taking a limit in this proof. The order of limits in k and p matters.
- The report gives a sufficient lower bound for a true transport ratio. It does not establish optimal growth. Numerical checks here evaluate only the proved lower-bound expression.
- Searches were public and bounded; no full citation-network review, unpublished-source survey, or external contact occurred. The full-strength priority question remains unresolved, while the original unrestricted negative answer is already definitive.

## Checkable artifacts and recommended wording

`check_mechanism.py` and `MECHANISM_CHECKS.json` independently check 319 exact product/gamma cases, 35 rate cases including p=1.1,1.5,pi,100, and 12 asymptotic constants. All passed. Finite checks supplement the algebra and do not prove limits or novelty.

Safe description: “An explicit quantitative counterexample on smooth even positive densities, built from classical Funk eigenvalues and a smooth transport flow; historical novelty of this strengthened all-finite-p statement is unverified. The original all-probability formulation is ruled out immediately by classical antipodal noninjectivity.”

No exact-printing absence, adjunct result, or currently queued catalogue row should be used to support an original-problem first-resolution claim. The frozen source gate largely acknowledges this distinction; promoting a claim of novel discovery would require evidence beyond it.

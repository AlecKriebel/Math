# Continuous finite energy elasticity gaps with precise scope

## Review status of this edition

This AI-assisted mathematical exposition and independent internal AI source/proof audit are unrefereed. Bounded acceptance here does not mean external human peer review, journal acceptance of these authored documents, or formal proof-assistant certification. The AKM result is prior published work; no novelty is claimed. Deep cited existence, finite-distortion, change-of-variables and topological dependencies remain external. No author was contacted.

## Conclusion

Almi, Krömer and Molchanova supply a genuine later result relevant to Ball's Problem 4: a Lavrentiev gap for a homogeneous polyconvex elastic energy, continuous orientation-preserving finite-energy maps, partial Dirichlet data and the Ciarlet–Nečas constraint. The accepted formulation here uses the paper's two-component reference configuration and the strictly subcritical exponent ranges. It is a literature attribution and bounded source audit, with no novelty claim and no independent reconstruction of the deep finite-distortion or existence theorems.

The printed two-dimensional Theorem 3.2 also claims its upper endpoint. The endpoint logarithmic competitor has infinite inverse-Jacobian energy as printed. That endpoint is therefore attributed accurately but excluded from this audit's accepted corollary. The three-dimensional Theorem 4.1 is strictly subcritical and does not use the defective endpoint construction.

## Common definitions

Let d be 2 or 3, let |F| be the Frobenius norm, and put

W(F) = |F|^p + gamma (det F)^(-q) if det F > 0, and W(F) = +infinity otherwise,

gamma = p d^(p/2 - 1)/q.

For the reference set Omega_s and boundary portion Gamma_s described below, define

E_s(y) = integral over Omega_s of [W(gradient y) - W(I)] dx,

Y_s = { y in W^{1,p}(Omega_s; R^d): det gradient y > 0 almost everywhere, y = y_0 on Gamma_s, and integral det gradient y <= |y(Omega_s)| }.

The last inequality is the Ciarlet–Nečas condition (CN). It enforces almost-everywhere injectivity in this regime, not injectivity at every point. The same CN and boundary conditions occur on both sides of each comparison. Traces on the boundary are interpreted through the continuous Sobolev representative. Normalization subtracts the same constant W(I)|Omega_s| from every competitor and has no effect on the existence of a gap.

W is independent of position; smooth on positive-determinant matrices; frame-indifferent; isotropic; polyconvex; minimized at rotations; and divergent as the determinant tends to zero from above. Here “homogeneous” describes the material's independence of x, not positive homogeneity in F. Its p-growth forces W^{1,p} regularity and, because p>d, continuity. These conclusions concern the specified energy and admissible class, not arbitrary polyconvex elastic densities.

## Two dimensions

Let S_1 = (-1,1) x (-s,s), Q(x_1,x_2)=(-x_2,x_1), xi=(4,0), S_2=xi+Q S_1, and Omega_s=S_1 union S_2. For 0<s<1 the closures are disjoint.

Gamma_s consists of the two end edges {−1,1} x (−s,s) of S_1 and the two end edges (4−s,4+s) x {−1,1} of S_2. Set y_0(x)=x on the first component and y_0(x)=x−xi on the second, restricted to these edges. The freely translated whole-component map y_0 is not itself CN-admissible: its images overlap in the central square. It is a convenient extension of the prescribed trace, not a finite-energy admissible minimizer.

Published Theorem 3.2 states: for every p>2 and 1<q<=p/(p−2), there is s_bar>0 such that for every 0<s<=s_bar,

min over Y_s E_s < inf over Y_s intersect W^{1,infinity} E_s.

Accepted portion in this audit: p>2 and 1<q<p/(p−2). The source's upper-bound construction gives min E_s=o(s), whereas its Lipschitz lower bound gives inf E_s>=m s for a fixed m>0 and small s. A Lipschitz competitor also gives inf E_s<=M s, so the gap is not caused by an empty regular comparison class.

At q=p/(p−2), the source's theorem statement remains a published claim, but its exhibited logarithmic competitor does not have finite energy. This audit does not accept that endpoint and does not claim the theorem is false. See ENDPOINT_AND_PROOF_NOTES.md.

## Three dimensions

Let S_1 = (-1,1) x (-1,1) x (-s,s), Q(x_1,x_2,x_3)=(x_1,−x_3,x_2), xi=(0,4,0), S_2=xi+Q S_1, and Omega_s=S_1 union S_2. Again these are two disjoint reference components, each with Lipschitz boundary.

Gamma_s is the union of the four end faces

[-1,1] x {−1,1} x [-s,s], and [-1,1] x [4−s,4+s] x {−1,1}.

The trace is y_0(x)=x on the first component and y_0(x)=x−xi on the second. The rest of the boundary is free; no image-container condition appears in Y_s.

Theorem 4.1 states: for every 3<p<4 and every 2<q<p/(p−2), there is s_bar>0 such that for every 0<s<=s_bar,

inf over Y_s E_s < inf over Y_s intersect W^{1,infinity} E_s.

Proposition 4.2 proves the Sobolev infimum is o(s), and Proposition 4.3 bounds the Lipschitz infimum between m s and M s with 0<m<M independent of s. Theorem 2.3 also supplies attainment of the left infimum, because the constructed finite-energy competitor makes Y_s nonempty and the infimum finite. This min-versus-inf refinement is a corollary of the paper's existence theorem, not a stronger independent existence result.

The exponent restrictions are substantive. The low-energy squeeze requires q<p/(p−2). The Lipschitz finite-distortion argument requires q>d−1, which is q>2 in three dimensions. Their simultaneous feasibility gives p<4. The paper does not establish this example for every p>3, for q=2, for q=p/(p−2) in three dimensions, or for p=4.

## Explicit bounded corollary

For d=3, choose p=7/2 and q=11/5. On the two-component configuration above, for all sufficiently small s there is a strict finite gap between the CN-admissible W^{1,7/2} minimum and the corresponding Lipschitz infimum. Every finite-energy admissible deformation is continuous; W is homogeneous in the material sense, isotropic and polyconvex; and the prescribed data are confined to a proper boundary portion.

Indeed, 3<7/2<4 and 2<11/5<7/3=p/(p−2). The claim follows from Theorems 4.1 and 2.3 with no limiting endpoint. For the elementary integrability check in Proposition 4.2, alpha=18/25 and beta=29/40 satisfy alpha<beta<1, p(alpha−1)>−1, p(beta−1)>−1, and q(1−alpha−beta)>−1. This numerical choice checks the source interface; it is not an independent proof of the theorem.

## Boundary of the conclusion

The low-energy maps collapse entire internal reference cross-sections: to a point in d=2, and to a line in d=3. Those reference sets have zero d-dimensional measure. Thus continuity, positive Jacobian almost everywhere and CN coexist with noninjectivity on the exceptional sets. The paper explicitly warns about the physical interpretation of this deep self-contact.

The result cannot be silently restated with globally injective homeomorphisms, their strong or weak Sobolev closure, a connected reference domain, or only the unconstrained positive-Jacobian class. In particular, without CN the translated map y_0 has normalized energy zero and is Lipschitz, so this construction supplies no gap in that enlarged class.

Remark 3.1 suggests adding a connecting component, but does not perform the required energy and admissibility analysis. Keeping the old prescribed end edges can turn part of Gamma_s into an internal constraint. A connected, boundary-only mixed-Dirichlet formulation therefore requires an additional argument. Its completion is outside this audit.

## Primary references

- J. M. Ball, Some open problems in elasticity, 2002, author-hosted 44-page manuscript, Sections 2.1–2.3, especially PDF pages 2–4 and 8–9. https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf
- S. Almi, S. Krömer and A. Molchanova, A new example for the Lavrentiev phenomenon in Nonlinear Elasticity, arXiv:2309.08288v2, revised 8 November 2023. https://arxiv.org/abs/2309.08288v2
- Published version: A new example for the Lavrentiev phenomenon in nonlinear elasticity, ZAMP 75, article 2 (2024), published online 8 December 2023. https://doi.org/10.1007/s00033-023-02132-4

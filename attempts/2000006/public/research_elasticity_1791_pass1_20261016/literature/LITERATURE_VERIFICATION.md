# E-6322: primary-source theorem and literature verification

Checked 16 October 2026. Target: every full-class global minimizer for the fixed three-dimensional density

\[
W(F)=a|F|^6+b|\operatorname{cof}F|^3+c(\det F)^2+d(\det F)^{-2},\qquad a,b,c,d>0,
\]

with the prescribed smooth diffeomorphic full trace, must satisfy \(\operatorname*{ess\,inf}_\Omega\det Dy>0\).

## Result

No theorem or counterexample establishing this exact assertion was verified in this bounded literature investigation. This is a search result, not a proof of novelty or an exhaustive declaration of the 2026 state of the literature. Several consequences are already established by existing theory and must not be claimed as new:

1. Existence of full-class global minimizers.
2. Continuity of every finite-energy competitor on the closure.
3. Almost-everywhere injectivity and the change-of-variables formula, using the full homeomorphic boundary data.
4. Appropriate inner and outer variational identities once the stress-growth hypotheses are verified.

None is the required uniform Jacobian estimate. In particular, “global invertibility” in several relevant papers denotes an almost-everywhere property, not everywhere injectivity or a lower Jacobian bound.

## 1. Existence: the exact law passes the known hypotheses

Source: J. M. Ball, *Some Open Problems in Elasticity* (2002), author manuscript, Theorem 2.1, p.4; admissible class on p.4; determinant barrier on p.3. The provided 44-page manuscript was inspected directly. Public source:

https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf

The theorem assumes the standing elasticity hypotheses, a nonempty trace class, polyconvexity, and a lower bound by a positive multiple of \(|F|^2+|\operatorname{cof}F|^{3/2}\), up to an additive constant. It yields a global minimizer in the full finite-energy \(W^{1,1}\) class; injectivity is not built into that class.

Application to E-6322: put \(h(J)=cJ^2+dJ^{-2}\) for \(J>0\) and \(+\infty\) otherwise. Then \(h''(J)=2c+6dJ^{-4}>0\), and
\(P(F,C,J)=a|F|^6+b|C|^3+h(J)\) is convex and lower semicontinuous in its independent variables. The positive-power terms dominate the theorem's required growth. The given extension \(G\) has bounded gradient and a positive minimum determinant on compact \(\bar\Omega\), so it is a finite-energy competitor. The resulting minimizer is in \(W^{1,6}\). This is a direct theorem application, not a new positivity result.

The same argument can be seen directly: a minimizing sequence is bounded in \(W^{1,6}\); its cofactors and determinants are weakly continuous in \(L^3\) and \(L^2\), respectively; convex lower semicontinuity in the minors preserves finite energy and the barrier; the trace is weakly closed. Positivity almost everywhere follows from finite energy, not from an essential lower bound.

## 2. Almost-everywhere invertibility already holds for every competitor

Source: Stefan Krömer, *Global invertibility for orientation-preserving Sobolev maps via invertibility on or near the boundary*, arXiv:1912.11086v2 (9 January 2020; manuscript dated 10 January), Theorem 6.1, pp.26–27. Primary manuscript:

https://arxiv.org/pdf/1912.11086v2

Theorem 6.1 assumes a bounded Lipschitz domain, \(p>d\), positive determinant almost everywhere, continuity on the closure, and topological degree at most one. It provides a change-of-variables formula, a unique preimage for almost every target point, and connected interior fibers. It generalizes Ball's 1981 Theorem 1, as identified in the subsection immediately preceding its statement. Krömer's original theorem and proof were inspected; Ball's original 1981 full text was not successfully retrieved in this pass.

Our application: \(p=6>3\) gives closure continuity. Trace equality implies equality of the continuous boundary representatives. For \(z\notin G(\partial\Omega)\),

\[
\deg(y;\Omega;z)=\deg(G;\Omega;z)=
\begin{cases}1&z\in G(\Omega),\\0&z\notin G(\bar\Omega).\end{cases}
\]

Thus the theorem's degree hypothesis is automatic. In particular, this works when \(\Omega\) has holes: it uses the supplied diffeomorphic extension and Theorem 6.1 directly. Do **not** substitute Corollary 6.5, whose boundary-only route assumes that \(\mathbb R^d\setminus\partial\Omega\) has exactly two connected components. No extra injectivity constraint need be imposed on E-6322 competitors to obtain this almost-everywhere conclusion.

This observation is a baseline strengthening, not a regularity theorem. It does not rule out exceptional collapsed fibers, establish an everywhere inverse, or give a quantitative Jacobian estimate.

## 3. Current primary corroboration: the terminology matters

Sabrina Traver, *Global invertibility of Sobolev mappings with prescribed homeomorphic boundary values*, arXiv:2507.07206v2, 22 May 2026; related publisher DOI 10.1007/s00526-026-03370-w. Theorem 1.2, pp.2–3; Corollary 1.3, p.3; definition (1.1), p.2:

https://arxiv.org/pdf/2507.07206v2
https://arxiv.org/abs/2507.07206

For bounded Lipschitz source and target domains, a \(W^{1,n}\) map with positive Jacobian almost everywhere and prescribed \(W^{1,n}\) homeomorphic full trace has a continuous monotone surjective extension to the closures, and is injective off a null set. The paper's “global invertibility” means unique preimages almost everywhere; it explicitly allows squeezing. The E-6322 class satisfies these hypotheses with target \(G(\Omega)\). No derivative lower bound is asserted. The p>n predecessor is credited to Ball. The manuscript's theorem statement and definition were inspected, rather than inferring everywhere injectivity from its title.

Carlos Mora-Corral and David Mur-Callizo, *Invertibility of Sobolev maps through approximate invertibility at the boundary and tangential polyconvexity*, arXiv:2503.01795v1 (3 March 2025), Theorems 4.1 and 4.3; related DOI 10.1051/cocv/2025028:

https://arxiv.org/html/2503.01795v1

The main injectivity theorem is again explicitly **almost everywhere**. Theorem 4.3 requires its no-cavitation/divergence-identity class up to the boundary, approximate boundary invertibility, and the two-connected-components topological assumption. Its existence application includes a boundary energy. These statements add no uniform Jacobian estimate for E-6322. The abstract's shorter word “injective” must be read against the theorem.

## 4. Finite-distortion theorems do not follow from the energy bound

Krömer's same manuscript, §6.2, pp.29–31, defines

\[
K_O=|Dy|^3/J,\qquad K_I=|\operatorname{cof}Dy|^3/J^2,\quad J=\det Dy.
\]

Theorem 6.8 (p.30) assumes either \(K_O\in L^{2q}_{\mathrm{loc}}\), \(q>1\), or \(K_O\in L^2_{\mathrm{loc}}\) together with \(K_I\in L^q_{\mathrm{loc}}\), \(q>1\). It obtains a homeomorphism. Theorem 6.10 (p.31) instead assumes \(K_I\in L^1_{\mathrm{loc}}\), yielding a homeomorphism on a specified reduced domain; it does not automatically identify that domain with all of \(\Omega\).

Our algebraic comparison, not an assertion imported from the source: E-6322's known integrals give only

\[
\int K_O\le (\int|Dy|^6)^{1/2}(\int J^{-2})^{1/2},
\qquad
\int K_I^{1/2}\le(\int|\operatorname{cof}Dy|^3)^{1/2}(\int J^{-2})^{1/2}.
\]

Thus the readily available bounds are \(K_O\in L^1\) and \(K_I^{1/2}\in L^1\). Neither verifies the displayed hypotheses. Stronger integrability would require a new argument using minimality or another established result; it cannot be silently read off the separate summands. Even proving homeomorphism would still be weaker than E-6322's determinant estimate.

## 5. Positive-Jacobian regularity results require additional hypotheses

P. Bauman, D. Phillips and N. C. Owen, *Maximal smoothness of solutions to certain Euler–Lagrange equations from nonlinear elasticity*, Proc. Roy. Soc. Edinburgh A 119 (1991), 241–263:

https://doi.org/10.1017/S0308210500014815

The publisher synopsis, rechecked this pass, starts from a \(C^{1,\beta}\) stationary state for its regularity/positive-Jacobian conclusion. The original full article remains unavailable in this inspection, so no exact theorem number, full structural hypothesis match, or global boundary conclusion is claimed. Ball's supplied manuscript, p.11, likewise describes this as a conditional theorem for already \(C^{1,\beta}\) energy-momentum solutions. Neither source licenses assuming this regularity for E-6322 minimizers.

P. Bauman, N. C. Owen and D. Phillips, *Maximum principles and a priori estimates for a class of problems from nonlinear elasticity*, Ann. Inst. H. Poincaré ANL 8 (1991), 119–157:

https://www.numdam.org/article/AIHPC_1991__8_2_119_0.pdf

The full PDF text was inspected: §1, pp.120–124; §3, pp.129ff., in particular Theorems 3.2, 3.3 and 3.6; and Theorem 4.2 (p.141, PDF p.24, visually checked). This is a two-dimensional neo-Hookean-type model. Its maximum principles assume classical equilibrium solutions, and its global controls are expressed through derivative quantities on the boundary. Theorem 4.2 bounds the reciprocal Jacobian only on compact interior subsets and requires the displayed integral of \( |Du|^{12+16/s} \), where \(s\) is its barrier exponent. Smoothness of a prescribed trace does not give an a priori bound for the unknown normal derivative. The paper therefore does not prove the arbitrary Sobolev-minimizer, three-dimensional, whole-domain assertion here.

K. Zhang, *Energy minimizers in nonlinear elastostatics and the implicit function theorem*, Arch. Rat. Mech. Anal. 114 (1991), 95–117:

https://doi.org/10.1007/BF00375399

The original full theorem was not retrieved. Ball's inspected source p.7 and the recovered Bevan–Yan introduction pp.193–194 identify the relevant near-affine/small-boundary-perturbation conclusion. This remains a known-case exclusion, not a verified unconditional applicability claim for this exact energy. No unseen theorem's exponent range is asserted.

## 6. Derivatives of minors cannot be removed from positivity theorems

B. Benešová, M. Kružík and A. Schlömerkemper, *A note on locking materials and gradient polyconvexity*, arXiv:1706.04055v5 (2018), directly inspected recovered source:

https://arxiv.org/pdf/1706.04055v5

Definition 5.1 and Remark 5.2 (p.18) distinguish formal convexity in derivative variables from the coercivity actually used. Proposition 5.1 (p.21) requires cofactor **Sobolev** control through a term \(|\nabla\operatorname{cof}Dy|^q\); its positivity clause requires \(q>3\) and \(s>6q/(q-3)\). Proposition 5.4 (p.26) also controls \(\nabla J\) in \(L^r\); its positivity clause requires \(r>3\), \(s>3r/(r-3)\). The mechanism is Hölder continuity of a minor together with inverse-determinant integrability.

E-6322 has no derivatives of minors and has only \(s=2\). Neither positivity clause applies. The fact that some gradient-polyconvex deformations need not belong to \(W^{2,1}\) does not make these first-gradient energy theorems. Likewise, explicitly imposing a hard lower-determinant constraint proves a different problem.

## 7. Singular-minimizer and special-model titles do not settle this target

The previously recovered Bevan–Yan (2008), *Minimizers with topological singularities in two dimensional elasticity*, DOI 10.1051/cocv:2007043, is two-dimensional, uses double-cover boundary data, and proves minimality in a proper subclass (pp.192–194; its full-class question remains explicitly posed on p.204). The previously recovered Bevan–Kabisch arXiv:1608.00160v1 studies twist/shear classes and distinct barrier models (pp.1–4). Its positive-measure zero-Jacobian examples use the nonnegative-Jacobian constraint without a blow-up barrier; its shear boundary singularity example uses mixed boundary conditions and assumes a positive lower Jacobian bound. The source passages identified in the formulation gate were rechecked against the local texts. Primary links: https://doi.org/10.1051/cocv:2007043 and https://arxiv.org/pdf/1608.00160v1 . Neither supplies full-class minimality for the exact three-dimensional density with admissible diffeomorphic data.

A recent additional check: André Guerra and Riccardo Tione, *A singular minimizer of a smooth strongly polyconvex functional in two dimensions*, arXiv:2609.32404v1 (26 September 2026), Theorem 1.2:

https://arxiv.org/html/2609.32404v1

The theorem constructs a unique singular Lipschitz minimizer from a two-dimensional disk into \(\mathbb R^6\) for a specially designed, everywhere smooth, strongly polyconvex integrand on \(\mathbb R^{6\times2}\) with bounded second derivative. This refutes an unrestricted inference from strong polyconvexity to full smoothness. It neither studies the square 3×3 determinant barrier nor uses E-6322's density. Nonsmoothness alone would not refute a positive essential lower bound on a determinant even in matching dimensions.

## 8. Current-status and novelty discipline

Neff et al., *Rate-Form Equilibrium for an Isotropic Cauchy-Elastic Formulation. Part I: Modeling*, J. Nonlinear Science 36, article 8 (2026), online 24 November 2025, §1.1.1–1.1.2, was inspected in publisher full text:

https://link.springer.com/article/10.1007/s00332-025-10214-y

Its context section still distinguishes direct-method existence from lower Jacobian control and weak equilibrium, and describes implicit-function conclusions near a known smooth equilibrium. This is contemporary evidence that the general difficulty persists, not an exact-tuple theorem or a certification that no E-6322 result exists.

Ball Problem 6 is broader than E-6322: it requests adequate constitutive growth assumptions and allows a suitably selected local-minimum branch as well as global minimizers. A proof of this frozen target would establish a concrete sufficient-condition branch; a counterexample would reject only the frozen benchmark. None of the reviewed literature licenses interpreting one as a full answer to every part of Ball's programme.

## Verification limits

- Inspected exact statements and relevant proof mechanisms, not independent full proofs of every cited paper.
- Ball (2002), Benešová–Kružík–Schlömerkemper (2018), Bevan–Yan and Bevan–Kabisch were available in recovered local source text; Krömer, Traver, Mora-Corral–Mur-Callizo, Guerra–Tione and the two-dimensional maximum-principles paper were inspected through primary online full texts. Krömer, Traver, Mora-Corral–Mur-Callizo, and the maximum-principles article were additionally retrieved as local PDFs; selected theorem pages were visually inspected.
- The original Ball (1981), Bauman–Phillips–Owen maximal-smoothness paper, and Zhang (1991) were not retrieved in full. Primary substitutes and the exact resulting limits are stated above.
- Search results were used to find sources, not as substitutes for verified theorem hypotheses. No external publication or account mutation was performed.

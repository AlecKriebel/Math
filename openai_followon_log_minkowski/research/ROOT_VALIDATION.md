# Lead's independent proof checks

Recorded 2026-10-06 21:19 PDT. This is distinct from agent reports and from the unavailable formal rebuild.

Read all needed upstream TeX sections: introduction, reduction, moment, identities, density, tensor, variance; inspected exact actual Lean endpoint definitions/declaration and pinned hash inventory. Truncated-ball moment assumptions and source cap are explicitly recorded in two independent primary-source audits. Root checked local ellipticity from determinant/cap, the spectral log extension and smooth limit, gradient surjectivity by tilted coercivity, affine-only density obstruction, sign of the vector Bochner trace, constant dual coordinate normalization, tensor symmetrization coefficients and homogeneity factors. No material unsupported claim was found in the needed manual proof. Broader measure-theoretic upstream applications are not dependencies and are not certified here.

Independently rederived the nonsmooth Wulff first variation. Boundary normal uniqueness makes h_W=a S_W-a.e. The classical mixed-volume inequalities in both orders sandwich the root-volume difference with integrals of b-a. Uniform variation and weak measure convergence identify the derivative for t of either sign. Thus no assumption that geometric interpolation is a support function is smuggled into the nonsmooth case.

Independently checked equality: exp(px) is strictly convex for p>0; equality in the final product bound forces equality in BOTH steps, hence h_L/h_K=c S_K-a.e. Classical V1 sees exactly that a.e. set, so its equality case gives homothetic translates. Symmetric bounded bodies cannot have two centers. Equal prescribed measures give Vp(K,L)=V(L) in both orders, then equal volume as n-p>0 and finally equality of bodies.

Independently derived endpoint identity in main.tex: q=h exp(tw), A=Q(hw), Q(hw²)=2wA-w²Q+2h dw⊗dw. First derivative is tr(Q^-1 A)=-w; since tr I=n-1 the second derivative is

    0=-tr((Q^-1A)^2)-(n+1)w²+2h Q^-1(dw,dw).

Q^-1A is similar to a symmetric matrix. At both extrema of w the last term is zero, giving w=0, hence uniqueness. The only interpolation regularity used is Q(q_t)>0 on a small interval about0, by compactness and continuity. This removes the global-Wulff-regularity step from He–Liu. Smooth f-prescribed minimizers have volume M/n; local Euler–Lagrange multiplier is exactly1, no hidden normalization. n=2 retains matrix dimension1 and coefficient3.

Existence root checked primary BBCY Thm1.7/Prop7.3 and CW Prop1.2 text. Smooth f has finite positive bounds. G={±I} is closed and invariance is exactly evenness. A full-dimensional symmetric body contains a ball about0, making support positive. This makes the two weak measure conventions equivalent globally. CW's positive-support local strict convexity plus regularity gives support C2α and Ck+2,α; equation's positive determinant upgrades semidefinite Q to positive definite. The circle can be checked directly from distributional h''+h=f h^(p-1).

Box constants checked: each facet area V/(2a_i), S0 atom a_i times area=V/2, cone volume V/(2n). An agent-report factor-two typo was corrected globally before package review. Density scales c^(n-p), not c^(n-1-p). No claim extends to nonsymmetric bodies or arbitrary singular p=0 measures.

The source statement of actual formal declaration agrees with all-body log-BM. The dependency build was stopped under disk pressure, before theorem compilation, so no kernel axiom set or independent formal certificate is asserted. The theorem chain is justified by the manually audited mathematical proof, not a Lean catalogue entry. The supplemental finite exact arithmetic checks are falsification evidence only.

Priority root read independent primary audit and searched the inaccessible Stancu2022 article independently. Earlier Stancu2018 announcement is credited. Established reductions and source-authorship are preserved. No first-public-result claim or abstract-only theorem reliance is used.

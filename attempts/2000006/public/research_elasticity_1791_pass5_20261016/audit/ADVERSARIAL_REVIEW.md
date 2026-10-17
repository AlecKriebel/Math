# E-6322: fifth and final independent adversarial review

16 October 2026. Final mathematical disposition: **UNSOLVED 5/5**.

The final artifacts are accepted as rigorous partial progress with the qualifications below. No full-class minimizing counterexample or unconditional whole-domain determinant bound has survived review. This is an acceptance of the stated auxiliary results, not acceptance of the benchmark assertion. There is no sixth research pass and no novelty or priority claim.

## 1. Frozen statement and audit controls

The complete target was reread. Its SHA-256 remains

`66006f5870581093313e1906c245c009c6738a2845b5fa674da03eb934baf8f9`.

The energy in three dimensions is

\[
W(F)=a|F|^6+b|\operatorname{cof}F|^3+cJ^2+dJ^{-2},\qquad J=\det F>0,
\]

and is infinite otherwise. All four coefficients are arbitrary positive finite numbers. The domain is any bounded connected smooth domain; its entire boundary has the trace of an orientation-preserving smooth diffeomorphism defined near the closure. There is no ball, symmetry, smallness, homeomorphism, smooth-approximation, or restricted-comparison assumption. Every finite-energy map in the stated full Sobolev class is a competitor. The desired individual-minimizer lower bound includes every boundary collar.

All four prior audit manifests were recursively checked against their recorded file bytes and hashes. Their 85 bound entries were unchanged. The final manifest records the prior manifest chain and every final authored lane file. Private source documents are not included in the final artifact list.

The reviewer read the frozen final reports, independently checked their analytical arguments, reran the exact and positivity scripts in temporary mirrors, and made the separate algebraic/control checks in `verify_audit.py`. Running a symbolic test does not certify a Sobolev chain rule, full-class minimality, compactness, or an unproved regularity hypothesis. Those steps were reviewed as proofs.

Two scope-wording corrections were requested and incorporated before final hashes: an expensive finite comparison at the genuine identity minimizer was separated from a different nonstationary oscillatory sequence. No mathematical statement was strengthened by these corrections.

## 2. Coupled endpoint moment: accepted

Reviewed `positivity/COUPLED_ENDPOINT_MOMENT.md` and its exact certificate.

Let y be a full-class minimizer and v a same-trace W^{1,6} map. Write F=Dy, A=Dv, J=det F, j=det A, M1=cof F:A and M2=cof A:F. Under the explicit signs j,M1,M2>=0, the determinant of the actual compatible segment y_t=(1-t)y+tv is

\[
J_t=(1-t)^3J+t(1-t)^2M_1+t^2(1-t)M_2+t^3j\ge(1-t)^3J.
\]

Thus every t<1 is admitted, including when the endpoint has infinite barrier energy. This is not a substitution of unrelated pointwise matrices.

For 0<t<=1/2 the barrier secants have the integrable upper bound

\[
\frac{J_t^{-2}-J^{-2}}t\le126J^{-2},
\]

because ((1-t)^{-6}-1)/t equals the sum of (1-t)^{-k}, k=1,...,6. Their pointwise limit is 6J^{-2}-2M1 J^{-3}. Reverse Fatou, rather than an unjustified monotonicity assertion, is the correct limiting argument. The positive-density derivative is integrable because |DH(F)|<=C|F|^5 and both endpoint gradients lie in L^6. If the mixed moment were infinite, the upper limit of the total energy secants would be negative infinity, contradicting minimality. Consequently

\[
M_1J^{-3}\in L^1,\qquad
2d\int M_1J^{-3}\le\int DH(F):(A-F)+6d\int J^{-2}.
\]

The report correctly claims an inequality, not exchange of the full integral derivative with its pointwise limit. It also correctly avoids importing convexity of H along arbitrary matrix segments. The bound C_H=6a+2b+2c/9 follows from |cof F|<=|F|^2/sqrt(3), |J|<=|F|^3/(3sqrt(3)), and |D(cof)(F)[R]|<=2|F||R|. Young's inequality gives the stated [H(A)+11H(F)]/(6a) bound.

For rank(A-F)<=1, M1=2J+j and M2=J+2j. The new inequality recovers the previous source coefficient 2 after cancellation. Full-rank compact Hessian perturbations of identity with positive-definite gradients show that the new allowed segment class really is larger.

The radial diagnostic y=r^{1/2}log(e/r)^kappa x, 1/6<kappa<=1/2, has positive principal stretches s,s,sq. Its identity endpoint obeys all mixed signs, while M1 J^{-3} is comparable to s^{-7}; the radial integral is proportional to integral r^{-3/2}log(e/r)^{-7kappa}dr and diverges. This supplies a legitimate negative infinite right energy derivative and excludes the map from minimization. It does not contradict the earlier impossibility of uniformly positive single-fixed-direction repairs for that map: the new path changes several components. The map was already nonminimal by affine uniqueness.

**Unresolved premise:** an arbitrary minimizer is not known to admit a useful same-trace endpoint with the mixed signs and quantitative lower bounds. Taking v=y gives only the baseline moment; taking the prescribed smooth extension need not satisfy either mixed sign.

## 3. Whole-boundary non-Dini modulus criterion: accepted

Reviewed `positivity/NON_DINI_MODULUS_CRITERION.md`. This is an additional-hypothesis theorem, not an inferred modulus for all minimizers.

The safe material identity is div(pI+Q(Dy))=0, with p=3dJ^{-2} initially only in L^1 and Q a degree-six positive-energy tensor. Assume Dy has a continuous representative on the compact closure, with uniform modulus omega. The global gradient bound implies the modulus of Q(Dy) is at most C omega.

The already audited negative-norm estimate starts with an L^1 pressure, so there is no circular L^2 assumption. On ordinary balls and the uniform smooth-boundary caps, subtract a constant Q and obtain

\[
\left(\fint_{U_r}|p-p_{U_r}|^2\right)^{1/2}\le C\omega(cr).
\]

The scaled cap geometry and bounded volume ratios give bounded successive mean differences. Telescoping only to radius r yields

\[
p_{U_r}\le C_0+C_1\int_r^R\omega(t)\frac{dt}{t}.
\]

Fixed geometric changes of the upper scale affect C0; fixed scale factors in omega are absorbed by changing variables and an additive constant. No pressure boundary trace and no convergent Dini integral have been assumed.

If the continuous J vanishes at any interior or boundary point, then J<=C omega(r) throughout its small ball or cap. Since J>0 a.e., this gives p_{U_r}>=c omega(r)^{-2}. A zero therefore forces

\[
\omega(r)^2\left(1+\int_r^R\omega(t)\frac{dt}{t}\right)\ge c_*>0
\]

at every sufficiently small scale. The stated liminf-zero condition contradicts this. If omega is zero on a sufficiently small interval, J would instead vanish on a set of positive volume immediately. Compactness after exclusion of all zeros gives the claimed positive minimum.

For omega(r)<=C log(eR/r)^{-alpha}, the product is bounded by a constant times L^{1-3alpha} for alpha<1, L^{-2}log L for alpha=1, or L^{-2alpha} for alpha>1. Thus alpha>1/3 suffices, including non-Dini exponents. This has been independently checked at the boundary as well as in the interior.

The exact lane's endpoint example is correctly **nonconstitutive**. With L=log(e/r), p=L^{2/3}, and

\[
q=r^{-2}\int_0^r\frac23s\,\log(e/s)^{-1/3}ds,\qquad Q=q\,n\otimes n,
\]

one has q'+2q/r=-p', q~(1/3)L^{-1/3}, and div(pI+Q)=0 distributionally. The possible puncture contribution vanishes since its boundary flux is O(r^2 L^{2/3}). All finite pressure moments exist, yet p is unbounded. The tensor Q and formal J=p^{-1/2} have the critical logarithmic modulus. The uniform modulus bound follows from |Q|<=C L^{-1/3} near zero and |DQ|<=C/(rL^{1/3}) away from it. No deformation realizing this Q(Dy) is supplied. It limits the abstract pressure argument, not the benchmark itself.

## 4. Compensated inverse repair: accepted with its existence quantifiers

Reviewed both reports in `variations/`.

For the actual inverse v, write H=Dv, K=det H and V(H)=X(H)+dK^3. A rank-one-connected endpoint, relative bounds on H, cof H and K, and a proved inverse-class mechanism make the t<1 segment legitimate and integrably differentiable. Natural-exponent Sobolev regularity alone is not used as that mechanism. The exact differentiated inequality is

\[
3d\int K^2(K-K_e)\le R,\qquad R=\int DX(H):(H_e-H).
\]

The determinant mass is conserved even when the endpoint itself is inadmissible: use any admitted t in (0,1), integral K_t=integral K, and affine interpolation of K_t. If the transferred donor and recipient masses both equal m>0, donor K>=lambda and recipient K<=kappa, then

\[
3d(\lambda^2-\kappa^2)m\le R.
\]

The weighted-moment version is accepted and important: a measurable high-level set need not have any open subset suitable for a smooth repair. The report explicitly controls donor/recipient moment leakage rather than presuming such a subset.

A repair for every positive-measure sufficiently high level, with one fixed kappa and one fixed cost bound R<=C0 m, would force K<=sqrt(kappa^2+C0/(3d)). These constants may depend on the individual minimizer, exactly as the target permits. The relative domination constant M may vary with the level; it is only needed to justify each individual differentiation. The fixed recipient threshold kappa=2|Omega|/|D| supplies a positive-measure low-K region by the known mass integral, but does not supply compatible transport to it.

For the actual construction, take a compact smooth h>=-1 with zero integral on every source x1-fiber, set f(x)=integral h(s,x')ds, and phi_t(x)=x+t e1 f(x). The determinant is 1+t h>=1-t; each fiber is increasing and fixes its endpoints. Thus phi_t is a genuine smooth diffeomorphism for t<1, y composed with phi_t^{-1} is an admitted primal comparison, and its inverse is phi_t composed with v. This directly establishes the natural-exponent comparison class and avoids an illicit W^{1,9/4} assertion for f composed with v.

The exact cofactor formula was checked independently. For A_t=I+t e1 tensor Df and k_t=1+t h,

\[
\operatorname{cof}(F A_t^{-1})
=k_t^{-1}[\operatorname{cof}F+t(\operatorname{cof}F\,Df)\otimes e_1].
\]

The resulting positive first cost is R=integral E_+:D(e1 f), where E_+=H I-F^T DH and |E_+|<8H. Transported mass in inverse coordinates cancels the primal Jacobian, giving exactly the stated source donor/recipient integrals.

The two oscillatory controls have different meanings. At the actual identity minimizer, bounded determinant density can accompany a chosen finite comparison cost of order N^6, although its signed first derivative is exactly zero. For the separate sequence y_N=Id+(delta/N)w_N e1, total baseline energy is uniformly bounded, but the chosen signed positive first cost is at least cN-C. The shear identity

\[
(E_+(I+s e_1\otimes e_2))_{12}
=-[6a(3+s^2)^2+3b\sqrt{3+s^2}]s
\]

and the O(N^{-1}) gradient error give that conclusion directly. This sequence is nonstationary: its barrier first variation stays bounded. It is neither an optimal-repair lower bound nor a level-aligned minimizer counterexample.

**Remaining step:** finite-energy compatibility and uniform signed cost per unit mass must be constructed simultaneously for a minimizer's high levels. The criterion restates a consequence of safe material stationarity; it is not an independent new equilibrium equation.

## 5. Degenerate weighted tangents: accepted conditional exclusions

Reviewed all three frozen reports in `counterexample/`.

### 5.1 Whole-density normalization and full variation passage

Suppose the explicitly stated weighted rescalings converge strongly in W^{1,infinity} on an interior annulus to U_i=r^{alpha_i}phi_i, with ordered positive weights, m=alpha1, s=sum alpha_i>3, and nontrivial limiting determinant. Set L_r=diag(r^{alpha_i-m}). Then

\[
r^{2(s-3)}W(\operatorname{diag}(r^{\alpha_i-1})P)
=r^{2(s+3m-6)}H(L_rP)+d(\det P)^{-2}.
\]

On each compact positive-J_U patch, the approximating physical gradients lie in a compact subset of GL^+ for every fixed sufficiently small radius. Compact componentwise variations with amplitudes r^{alpha_i} are legitimate for both parameter signs. The permissible interval may depend on the radius. Strong gradient convergence permits weak stress passage without differentiating its error. This supplies all three limit Euler equations, rather than only an accidentally retained row.

The same positive patch forces m>1/2 and s<9/2 through the strain and barrier masses on shrinking annuli. Equality is excluded by absolute continuity of the original energy integral. These are necessary scaling restrictions, not replacements for stationarity.

### 5.2 Superbalanced and balanced profiles

If s+3m>6 and the angular profile is C^1, all three limiting equations are those of the pure determinant barrier on positive patches. In local U target coordinates they state that every derivative of J_U(U^{-1}(X))^{-3} is zero. Hence J_U is locally constant, contradicting J_U(tz)=t^{s-3}J_U(z) along a short positive radial segment. Angular zeros elsewhere and the absence of a regular target-axis preimage do not matter.

If s+3m=6 and the angular profile is C^2, write H0(P)=H(Pi P), with Pi the projection onto rows of minimum weight. The limit density is H0(P)+d(det P)^{-2}, and H0 is C^2 on all matrices. On the positive set, the full Euler equation gives

\[
\nabla J_U^{-2}=(3d)^{-1}(DU)^T\operatorname{div}DH_0(DU).
\]

The right side is bounded on each compact annular path without requiring J_U bounded away from zero. A path starting in the positive set cannot reach its first zero in finite length. Connectedness therefore makes J_U positive everywhere on the annulus and hence gives a positive angular minimum.

At least one row, including row 3, is absent from H0: all three minimal weights would force m=1 and s=3, excluded by the assumptions. The third equation is therefore pure barrier. With everywhere positive angular Jacobian, U has an isolated zero at the origin: a nonzero zero would make DU(z)z=diag(alpha_i)U(z)=0. The local degree is positive because sufficiently small regular target values have finitely many positive-Jacobian preimages. It follows that a small nonzero third-axis value has a regular preimage. Its radial curve maps to a vertical target segment, along which the third pure-barrier equation makes J constant, again contradicting its positive homogeneity degree.

The C^2 hypothesis in the balanced continuation step is retained. No bounded second derivatives are inferred from strong W^{1,infinity} convergence of the actual rescalings.

### 5.3 Subcritical profile with a simple minimum and dense positive set

If s+3m<6, alpha2>m, the profile is C^2, and {J_U>0} is dense, strain normalization gives scalar 6-harmonicity of U1 on every positive patch. The scalar residual is continuous, so density extends the equation across the determinant-zero set. This density premise cannot be omitted.

Writing U1=r^m phi, the spherical identity is

\[
\int (m^2\phi^2+|\nabla_S\phi|^2)^2|\nabla_S\phi|^2
=m(5m-3)\int(m^2\phi^2+|\nabla_S\phi|^2)^2\phi^2.
\]

For 1/2<m<3/5 it forces phi=0. At m=3/5 it makes phi1 constant. The correct critical argument is Stokes, not an unsupported degree assertion for a degenerate profile:

\[
\int_{S^2}j=cm\int_{S^2}d\phi_2\wedge d\phi_3=0,
\]

contradicting continuous j>=0 nontrivial. For 3/5<m<1, the puncture flux error is O(r^{5m-3}), so scalar 6-harmonicity extends weakly across zero. The scalar gradient regularity theorem then contradicts a nonzero homogeneous degree m<1 function. The external input is used only for that scalar limit; it is not an elasticity regularity theorem. The original scalar corollary was verified in pass 3: [Uhlenbeck (1977)](https://doi.org/10.1007/BF02392316), printed p.222, with its parameter p=4.

Thus among the assumed strong C^2-profile weighted tangents with s>3 and nontrivial nonnegative determinant, the residual cases are subcritical profiles with repeated minimum weight or an open angular zero-determinant region. An identically zero leading determinant remains unexcluded in every scaling range. Weaker or nonexistent tangents, non-power degeneration and boundary degeneration remain outside this classification.

### 5.4 Explicit critical-axis family

For y_perp=r^{m-1}x_perp and y3=z rho^2 r^{beta-3}+z r^{beta+delta-1}, the exact determinant and its angular integral were independently checked. Under m>1/2, beta>2m, gamma=2m+beta-3>0, delta>0 and 2gamma+delta<3, the map is admitted and has essential determinant infimum zero. Its full trace is the global smooth diffeomorphism G(x1,x2,z)=(x1,x2,z(1+rho^2)).

The leading angular zeros are the poles, where the image axis is critical. Nevertheless the third positive stress is smaller than the barrier stress by the positive radial exponent 4gamma. The limiting third equation requires J_U to be constant on non-axis fibers. At fixed transverse target radius q,

\[
J_U=q^2[(\beta-2m)r^{\beta-3}-(\beta-3m)q^2r^{\beta-2m-3}].
\]

The two distinct powers can have constant sum on an interval only if (beta-2m)(beta-3)=0 and (beta-3m)(beta-2m-3)=0. The hypotheses force beta=3, m=1, then gamma=2, which violates finite barrier energy. Thus every admitted family member is nonstationary. Failure of the limiting equation gives actual compact strict descent on sufficiently small physical annuli. The subcritical example (m,beta,delta)=(3/5,2,1/4) shows this rejection is not redundant with the balanced/superbalanced theorem.

No existence of these tangents for arbitrary minimizers, no complete singularity classification, and no boundary tangent theorem is claimed.

## 6. Universal graph repair and primary-source hypotheses: accepted

The matrix classification in `literature/UNIVERSAL_GRAPH_REPAIR_OBSTRUCTION.md` was proved independently. For fixed real 3-by-3 A,B,

\[
\det(A+BH)>0\ \text{for every }H\in GL^+(3)
\]

holds exactly when A=0, det B>0 or B=0, det A>0. If B is invertible and A nonzero, choose an orientation-preserving H sending a nonzero u to -B^{-1}Au; the output has a kernel. If B has rank one or two, use orientation-preserving singular-vector coordinates and complete any independent top row frame to a positive H. The fixed bottom rows of A must be independent; choosing the top frame with the opposite output orientation and scaling it gives a negative leading determinant coefficient. Rank-zero B is immediate.

For a C^1 graph map, the two classified branches are disjoint relatively open sets. Connectedness of D times Omega and the strong full-product collar Phi(z,x)=x select the A=0 branch everywhere, hence independence of z and then the identity map. This theorem quantifies over every incoming positive matrix. It does not prohibit a graph tailored to one particular inverse gradient or transformations with only an actual-graph collar. Fixed material diffeomorphisms only compare determinants by bounded positive factors; this says nothing about families with deteriorating distortion constants.

The final primary-source screen was independently checked in parsed primary text: [Henao–Mora-Corral–Oliva, Global invertibility of Sobolev maps](https://repositorio.uam.es/bitstream/handle/10486/700604/global_henao_ACV_2021_ps.pdf?isAllowed=y&sequence=1), author version 7 May 2019, Props. 7.3–7.4, printed pp.16–17. Both retain p>=n-1. Proposition 7.3 uses q>=p/(p-1); Proposition 7.4 changes the cofactor threshold but adds the stated extension and boundary hypotheses. In dimension three, inverse p=9/5 misses the common p>=2 requirement. A high cofactor exponent alone does not repair it. The metadata accurately discloses failed local retrieval and unavailable screenshots; no local PDF hash or visual inspection is asserted.

The exact inverse class and its energy-bounded closure were already established through primal W^{1,6} compactness and the full transported Piola identity. They do not imply arbitrary natural-exponent additions preserve the class. Nor would such an addition theorem by itself create finite-energy repairs: V is singular even on bounded matrix sets approaching zero determinant.

## 7. Final tests and acceptance limits

The final exact lane has 51 checks. Its temporary reproductions of the four sealed earlier exact scripts give 150 additional checks and 14 quadrature comparisons, for 201 exact checks in total. All twelve recorded earlier exact file hashes match and all earlier output bytes reproduce. The final positivity script has 28 successful checks. The reviewer independently reproduced both final outputs byte-for-byte in temporary locations, preserving the frozen inputs.

`AUDIT_CHECKS.json` records the reviewer's 57 additional algebraic and integrity controls. `REPRODUCTION_CHECKS.json` records the separate execution results. The independently reviewed `exact/BARRIER_DOMINATED_TANGENT_ADDENDUM.md` records the final superbalanced argument without altering the 201 exact-check total. `AUDIT_MANIFEST.json` binds the target, every final authored lane file, the prior audit manifest chain, and the present reports and scripts. Test counts are supplemental verification counts; they are not independent proofs of the benchmark or a measure of mathematical completeness.

The accepted end state is:

- genuine full-class comparison and weighted-moment theorems;
- a precise actual inverse class and substantial finite-energy comparison mechanisms;
- conditional whole-boundary positivity criteria;
- narrower, correctly quantified interior profile exclusions;
- explicit finite-energy diagnostic maps, method obstructions, and source-hypothesis checks;
- **no unconditional E-6322 resolution and no compliant minimizing counterexample**.

The final report `FINAL_ACCEPTANCE_REPORT.md` states the overall five-pass outcome. No frozen assumption has been silently strengthened, and Ball's broader adequate-growth program is not identified with this fixed benchmark.

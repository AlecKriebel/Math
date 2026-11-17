# Independent original-only adversarial record

UTC checkpoint: 2026-11-17T06:13:28Z. Reviewer lane: adversarial-sol. Row 189; Zenodo record 23203081. Best-guess completion toward this lane's initial scientific assessment: 65%; toward an unconditional independently checked theorem: 35%. This record is written before reading any packaged mathematical reviews, audit conclusions, certificates, upstream mathematical bodies, other families, or root scientific findings. Only the complete controlling `main.tex`, all five native PDF pages as text and personally viewed fresh page images, native record API metadata, and source custody metadata have informed it. No scientific program has been executed.

## Exact targets and conditions

Target A: for each integer ambient dimension n >= 2, each real 0 <= p < 1, and each strictly positive even smooth f on the unit sphere, there exists exactly one positive even smooth support function h with Q(h)=Hess_s h+hI positive definite and h^(1-p) det Q(h)=f. No volume normalization is imposed. The determinant is of an (n-1)-square matrix.

Target B: for 0 < p < 1, arbitrary full-dimensional origin-symmetric compact convex K,L with identical finite measures h_K^(1-p) dS_K=h_L^(1-p) dS_L are equal. No density or curvature hypothesis appears here. Target B expressly excludes p=0.

The essential external analytic assumption U is the global origin-symmetric logarithmic Brunn-Minkowski (LBM) inequality for the Wulff intersection of h_K^(1-t)h_L^t, all t in [0,1], including nonsmooth bodies. The manuscript asserts U is proved in a pinned OpenAI release. I have not checked that release; at this checkpoint all deductions using U are conditional. Existence, symmetry preservation, and regularity are separate external assumptions E and R, with theorem numbers supplied by the original paper but not independently checked here. Ordinary Minkowski first inequality with its equality case and weak continuity of surface-area measure are further classical input C.

Falsification success would be an explicit in-scope counterexample, an incorrect displayed identity/inequality, a missing hypothesis essential to the deduction, or an external input that fails to imply the assertion assigned to it. A conditional reconstruction is not an unconditional verification of U, E, or R.

## Independent reconstruction and adversarial checks

1. **Wulff first variation.** Positive continuous a implies W[a] has interior and is bounded. At each regular boundary point, an active half-space exists by compactness of the sphere. Its normal must equal the unique normal at that point, so h_W[a]=a almost everywhere for the surface-area measure. This is sufficient even if the defining a is not a support function. For A=W[a], C=W[b], Minkowski first inequality and h_C<=b give

   V(C)^(1/n)-V(A)^(1/n) <= integral(b-a)dS_A/[n V(A)^((n-1)/n)].

   Interchanging A,C gives the displayed lower bound using S_C. The signs in the manuscript survive this independent derivation. If (a_t-h_K)/t converges uniformly to g, then a_t/h_K -> 1 uniformly because min h_K>0. Thus (1-epsilon)K subset W[a_t] subset (1+epsilon)K. Weak continuity of S_W[a_t], uniform convergence of the quotient, and bounded total surface measure yield the same limit in both bounds. Negative t reverses bounds but preserves the common limit. Hence V'(0)=integral g dS_K. No density approximation is needed.

2. **Differentiation of U.** At t=0, the logarithmic path has g=h_K log(h_L/h_K), bounded and continuous because both supports have positive minima. Right differentiation of U gives integral log(h_L/h_K) dnu_K >= (1/n)log(V(L)/V(K)), where nu_K=h_K dS_K/(nV(K)). Factors n and V(K) agree with direct differentiation of log V. This uses only U's inequality and no equality classification.

3. **Equality with singular S_K.** Jensen applied to exp(p log r), p>0, with r=h_L/h_K, yields V_p(K,L)/V(K) >= (V(L)/V(K))^(p/n). If equality holds, both intervening nonnegative gaps vanish, so r=c S_K-almost everywhere and c=(V(L)/V(K))^(1/n). This does NOT by itself give support equality on the sphere. Instead integral h_L dS_K/n=cV(K), exactly the ordinary Minkowski equality value. Input C gives L=cK+x. Two origin symmetry centers of a bounded body cannot differ, so x=0. This correctly avoids the singular-support trap. A facet-supported measure is not a counterexample to this step.

4. **Equal-measure volume comparison.** If the shared measure is mu, then V_p(K,L)=integral h_L^p dmu/n=V(L). Writing a=V(K), b=V(L) gives b >= a^(1-p/n)b^(p/n), hence b>=a for n-p>0. Reversing K,L gives a>=b. Positive volumes make all divisions legitimate. Equality plus item 3 yields K=L. This checks Target B conditionally on U and C. The exponent does vanish at p=n, where scaling preserves the measure; that excluded value cannot be silently included.

5. **Endpoint path and stationary equation.** For p=0, integral f=nV, so both smooth solutions have the same positive volume v=M/n. The logarithmic inequality makes F(L)=M^(-1)integral f log h_L -(1/n)log V(L) globally minimized at either solution. Their F values and logarithmic integrals coincide. For w=log(h_1/h_0), q_t=h_0 exp(tw), C^2 dependence and compactness make Q(q_t)>0 for all sufficiently small |t|. Therefore q_t is actually a smooth support function locally; global Wulff smoothness is not being assumed. The f-weighted logarithmic integral is constant in t. U gives V(q_t)>=v for small t>=0, and minimality of F gives V(q_t)<=v. Thus q_t stays a minimizer with volume v. All small smooth even variations remain admissible. Vanishing first variation yields f/q_t=det Q(q_t), since the integrand is even and all even tests are allowed. This argument cannot be copied to nonsmooth supports because local Q-positivity is essential.

6. **Independent second derivative.** Put Q=Q(h_0), A=Q(h_0 w). The product rule gives

   Q(h_0 w^2)=2wA-w^2Q+2h_0 grad w tensor grad w.

   The first derivative of log(q_t det Q(q_t)) is w+tr(Q^(-1)A)=0. The second derivative has zero contribution from log q_t, so

   0=tr(Q^(-1)Q(h_0 w^2))-tr((Q^(-1)A)^2)
    =-(n+1)w^2+2h_0 Q^(-1)(grad w,grad w)-tr((Q^(-1)A)^2).

   The coefficient is n+1 because the tangent trace has dimension n-1. Q^(-1)A is similar to the symmetric matrix Q^(-1/2)AQ^(-1/2); therefore the trace of its square is nonnegative despite Q^(-1)A not generally being symmetric. At a maximum and a minimum of w the gradient vanishes, forcing each extremal value to be zero. One-sided validity in t suffices because q_t and these derivatives are smooth at zero. No differentiation of a nonsmooth path occurs. I found no algebraic or logical contradiction in this endpoint deduction under U and the smooth hypotheses.

7. **Regularity interface.** The paper's actual argument is not a smooth-density limiting proof of uniqueness: it imports symmetric existence and then regularizes a positive support. A necessary internal geometric bridge is valid: if the boundary of K is C^1, equality H((u+v)/2)=(H(u)+H(v))/2 for its homogeneous support H entails that a common support point has normals u and v; C^1 forces u and v to be positive proportional. Distinct points on an affine hyperplane avoiding zero cannot be positive proportional. Thus the restriction of H to that hyperplane is strictly convex. This checks that elementary bridge, not the hypotheses or conclusion of the cited analytic regularity theorem. The unverified interfaces are exactly BBCY Theorem 1.7/Proposition 7.3 for symmetric full-dimensional measure solutions; BBC Theorem 1.1(i) for C^1 boundary with no segment when 0 is interior; and CW Proposition 1.2 / BBC Theorem 1.1(iv) for C^(2,alpha) support and bootstrapping with RHS f h^(p-1). Once C^2 regularity and the positive determinant are available, Q>=0 implies Q>0 pointwise, and compactness gives uniform ellipticity for further smooth bootstrapping. These citations may contain dimension, normalization, or symmetry qualifications and must be checked after the initial gate.

## Boundary counterexample attempts

- **Boxes at p=0:** each facet at +/-e_i has area V/(2a_i), multiplied by h=a_i gives L0 atom V/2. Equal-product boxes with a_1=s,a_2=s^(-1), other a_i=1 share the measure yet differ for s!=1. Their cone-volume atoms are V/(2n), total V. This is an actual counterexample to an extension of B to p=0, already explicitly excluded by the paper. It does not have smooth positive spherical density and therefore does not contradict A.
- **Smooth approximation of boxes:** distinct equal-measure singular limits do not provide distinct smooth equal-data solutions. Data in separately smoothed sequences can differ. No uniqueness-under-limit principle is asserted or supplied; attempting to transfer smooth uniqueness to arbitrary L0 data would be invalid.
- **Ellipsoid attempt:** for h(u)=(u^T A u)^(1/2), A positive definite, the standard direct support-curvature formula gives h detQ=det(A) h^(-n). Changing unimodular axes changes this density. Thus same-volume noncongruent ellipsoids are not an immediate p=0 counterexample. This is a hand diagnostic, not an imported proof or executed computation.
- **Scaling:** h -> ch multiplies h^(1-p)detQ by c^(n-p). For n>=2 and p<1 this exponent is positive, so no nontrivial dilation preserves fixed f or the fixed measure. At p=0 the integral also fixes volume. No residual normalization ambiguity remains.
- **Translation and evenness:** positive even support means K=-K and 0 is interior. Translations generally destroy evenness, and two symmetry centers would force a nonzero period of a bounded set. The ordinary Minkowski equality translation is therefore eliminated legitimately.
- **Degenerate bodies:** lower-dimensional bodies, zero volume, vanishing support, and origin on the boundary are outside both stated classes. The divisions by V and log h require exactly this exclusion. No claim of extension to these cases should be inferred.
- **n=2:** the tangent matrix is 1 by 1 and the endpoint coefficient is 3. The scalar distributional relation is h''+h=f h^(p-1); with positive h it bootstraps locally. The trace-square argument still works. n=1 is excluded; no reduction to it is needed.
- **p limits:** p->0 loses Jensen strictness uniformly and does not prove nonsmooth endpoint rigidity. p=1 is not claimed, and p=n is not claimed. Smooth positive f is bounded away from zero on the compact sphere; no claim covers sign-changing, merely nonnegative, atomic, or noneven f.

## Strongest independently checked statement and remaining gap

The manuscript's explicit deductions reconstruct Target B and the uniqueness portion of Target A conditionally on U and C; I have found no original-text counterexample or internal defect in those deductions. The local smooth endpoint mechanism and nonsmooth equality treatment survive the above adversarial checks. This is an initial, fallible mathematical assessment, not acceptance of an unconditional theorem.

The central unresolved dependency is U itself. Repeating that it was audited, citing a release, finite tensor tests, or identifying a Lean declaration cannot establish it. The external E/R theorem statements are also unverified. Novelty and priority assertions are documentary claims not checked here. The native Description accurately labels the results as consequences and disclaims formal verification of the follow-on theorem; this does not discharge U. Next work, only after an explicit root RESUME, must authenticate and read the actual primary mathematical input bodies before any unconditional scientific promotion. No outreach is prepared or requested; no extended repair is attempted.

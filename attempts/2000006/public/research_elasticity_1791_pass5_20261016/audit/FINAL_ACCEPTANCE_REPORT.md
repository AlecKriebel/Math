# Final acceptance report: E-6322

16 October 2026. Five authorized mathematical passes completed.

## Verdict

**UNSOLVED 5/5.** The investigation proves neither the frozen universal lower-Jacobian assertion nor a counterexample consisting of an actual full-class global minimizer. The accepted deliverables are rigorous auxiliary results, conditional theorems, comparison mechanisms, counterexample-route exclusions, and verified limits of proposed methods. No sixth pass is included.

This is the result of the investigation, not a claim of exhaustive literature coverage or novelty of its auxiliary results.

## The exact unresolved assertion

For arbitrary positive finite a,b,c,d, let

\[
W(F)=a|F|^6+b|\operatorname{cof}F|^3+c(\det F)^2+d(\det F)^{-2}
\]

when det F>0 and W(F)=infinity otherwise. Let Omega be any bounded connected smooth domain in R^3, with the entire trace of a smooth orientation-preserving diffeomorphism defined near its closure. Minimize over every finite-energy W^{1,6} map with that trace, without imposing injectivity or higher regularity.

What remains unproved is that **every global minimizer has some individual epsilon>0 with det Dy>=epsilon almost everywhere on all of Omega**, including arbitrarily thin boundary regions. No common epsilon across minimizers or data is required. A permitted nonaffine-trace minimizer with essential determinant infimum zero has not been constructed either.

## Main accepted conclusions

### 1. The baseline and inverse are genuine

Existence follows from the standard polyconvex direct method with the finite-energy smooth datum. Full degree-one boundary data give almost-everywhere invertibility and area change even when the domain has holes. The actual Sobolev inverse, rather than merely a formal matrix field, satisfies

\[
Dv\in L^{9/5},\qquad \operatorname{cof}Dv\in L^{9/4},\qquad
K=\det Dv\in L^3,
\]

with full trace G^{-1}. The exact inverse density is

\[
V(H)=a|\operatorname{cof}H|^6/K^5+b|H|^3/K^2+c/K+dK^3.
\]

These conclusions do not assert everywhere injectivity. An admitted finite-energy map with a collapsed segment demonstrates why that extra conclusion cannot follow just from the energy and trace assumptions.

An intrinsic full-boundary transported Piola identity characterizes the actual inverse-image class and recovers the primal weak derivative and trace. Energy-bounded closure is proved by returning to primal W^{1,6} compactness. Compact W^{1,9/4} inverse additions and certain natural-exponent graph transformations preserve the exact class when their resulting energy is finite. No general finite-energy amplitude interval or unrestricted W^{1,9/5} addition theorem follows.

### 2. Safe variations produce actual comparison information

Inner and outer diffeomorphism variations have integrably controlled stresses. Ordinary unrestricted Piola stationarity is not automatically justified. Coupled primal/inverse variations are dual forms of the same safe identities; an additional independent equation or unconditional higher-integrability gain was not obtained.

Same-trace rank-one-connected endpoints with nonnegative determinant give a weighted inverse-cube moment. The final multicomponent extension uses nonnegative endpoint determinant and both mixed determinants. It provides a genuine finite-energy segment and

\[
2d\int (\operatorname{cof}Dy:Dv)(\det Dy)^{-3}
\le\int DH(Dy):(Dv-Dy)+6d\int(\det Dy)^{-2}.
\]

Its needed mixed moment is finite. No arbitrary-minimizer construction supplying favorable mixed signs and a quantitative lower bound has been proved.

Interior and boundary-collar barrier estimates, quantitative componentwise coercivity, and a boundary-preserving reference truncation are valid. Their source terms and finite safe-level ceiling remain; none has been converted into an arbitrary high-level reverse-Hölder estimate.

### 3. Whole-boundary positivity is proved under explicit extra regularity

The material equation is a pressure identity with p=3d(det Dy)^{-2}. An L^{6q} gradient estimate transfers to an L^q inverse-square determinant estimate. A Dini modulus for the positive constitutive tensor gives bounded pressure. A continuous gradient with modulus omega also suffices under

\[
\liminf_{r\downarrow0}\omega(r)^2
\left(1+\int_r^R\omega(t)\frac{dt}{t}\right)=0.
\]

In particular a uniform logarithmic gradient modulus of exponent greater than 1/3 excludes both interior and boundary zeros. These are global conditional results, not regularity conclusions for arbitrary minimizers. The needed gradient estimate or modulus remains unproved.

### 4. Several singularity routes have been excluded with their hypotheses retained

Exact C^2-angular weighted cores with positive component weights and positive determinant degree cannot minimize under the stated finite-energy hypotheses. Strong weighted annular tangents with positive angular determinant are excluded under the stated C^1-profile hypotheses. The final pass also excludes nontrivial nonnegative-Jacobian superbalanced C^1 profiles, balanced C^2 profiles, and subcritical C^2 profiles with a simple lowest weight and dense positive-determinant set. A repaired critical-axis family with allowed nonaffine smooth trace is nonstationary by a local fiber-pressure calculation.

No tangent existence theorem has been established. Identically rank-deficient limiting determinants, remaining subcritical degenerate profiles, weaker or nonexistent power tangents, and boundary-only degeneration remain outside these exclusions. All explicitly degenerating admitted maps remain diagnostic nonminimizers, rather than counterexamples to E-6322.

### 5. A precise sufficient repair estimate remains missing

A legitimate compensated inverse rank-one repair transferring determinant mass m from K>=lambda to K<=kappa must satisfy

\[
3d(\lambda^2-\kappa^2)m\le R,
\]

where R is its signed positive-energy first cost. If every positive-measure high level admitted such a repair with m>0 and R<=C0 m for fixed kappa,C0, then K would be bounded and the benchmark would follow. Smooth triangular material maps give actual finite-energy compensated comparisons, but the required level alignment and uniform cost have not been proved.

The source-energy and transverse-cost examples show why arbitrary prescribed repairs cannot simply be assigned that bound. They do not rule out better minimizer-specific repairs. The universal graph classification likewise rules out only a matrix-universal repair recipe; it does not rule out a map-tailored construction.

## Scope relative to Ball's original question

[Ball's Some Open Problems in Elasticity (2002)](https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf), Problem 6 and equation (2.19), asks for adequate growth assumptions in a broader first-gradient program. It does not prescribe this benchmark's exponent tuple or one local-minimality topology.

A proof of E-6322 would provide one specific sufficient-condition branch. One compliant counterexample would refute that branch, while leaving other exponents and other growth laws open. This investigation supplies neither outcome. Conditional smooth-solution, planar, small-data, constrained-class, or interior results are not relabeled as a resolution of the original program or the fixed benchmark.

## Verification and final acceptance

The final audit accepts all frozen final lane reports with the qualifications in `ADVERSARIAL_REVIEW.md`. All four prior audit manifest chains remain intact, with 85 bound entries verified unchanged. The exact lane reproduced 201 exact checks across five passes and 14 quadrature comparisons; the final positivity lane passed 28 checks. The reviewer reran both final scripts in temporary mirrors and obtained byte-identical outputs, then passed 57 additional algebraic and integrity controls.

The manifest records exact bytes and SHA-256 hashes for the final authored reports, tests, controls, frozen target, and prior audit manifests. No copied primary-source document or private source material is included in that manifest's authored deliverable set. Test success verifies the specified auxiliary computations; it does not bridge the still-missing analytic theorem.

**Final status: rigorous partial progress accepted; E-6322 UNSOLVED 5/5.**

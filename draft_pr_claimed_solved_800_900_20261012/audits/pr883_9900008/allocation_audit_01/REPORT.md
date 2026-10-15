# Independent adversarial allocation-family audit of PR 883 / 9900008

## Verdict and precise scope

**PASS for the mathematical claim as scoped in the frozen proof and the original problem. No identified mathematical gap remains in this bounded audit.**

There exists a nonzero, locally finite, diffuse random measure on R², with a constant accompanying random element, whose joint law is invariant under every measurable, pointwise-covariant, preserving allocation that is a function of the original observed pair, and which is not mass-stationary. The invariant-direction periodic example in the frozen proof establishes this. The argument genuinely covers all such allocations, including allocations that are not globally injective or surjective. Its universal step is analytic; finite diagnostics are supplementary.

This verdict concerns the unrestricted, background-free question in Thorisson's Problem 4.1 and the corresponding 2009 Problem 7.5. It does not concern a premise allowing an independent stationary background, a premise requiring invariance under all preserving Markov kernels, or a variant excluding invariant directions. Explicit controls below show that the candidate actually fails the first two stronger premises. No result about one-dimensional, free-action, full-support, or positive-density variants is inferred. No novelty, priority, exhaustive literature clearance, human peer review, or formal proof-assistant certification is asserted.

The immutable audit target is head `af25d26e21945a1a132aace5e600485152777070`. The supplied original-source manifest has SHA-256 `53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab`; its 26 originals total 211,771 bytes. The audited `author/PROOF.md` has SHA-256 `d700c5af20ff7a0dcafcabfeb2b78a35dcd740169318aafb8af2ab4eaba86331`. All were independently hashed against the externally supplied pins. No candidate file, shared index, Git ref, PR, record, or external communication was modified. The author status remains claimed_solved at turn 1/5; this is an audit, not another central proof-search turn.

## Independence and primary definitions

Before reading the authored proof, README, addenda, or previous audits, I read Thorisson's original section 4, printed pp. 5–6, and the 2009 paper's sections 2–3, Definition 6.1, Remark 6.2, and section 7. `INDEPENDENT_RECONSTRUCTION.md` records the resulting stabilizer/quotient mechanism and falsification plan. I subsequently read the complete authored proof, author and current README, both credit addenda, and the entire inherited author checker. I did not execute the inherited checker. Earlier audit conclusions were not used as mathematical premises.

The source uses the shift convention theta_t eta(B)=eta(B+t). A measurable displacement pi of the original state generates

    tau_omega(s)=s+pi(theta_s omega).

Equivalently, the allocation satisfies the pointwise identity

    tau_(theta_t omega)(s-t)=tau_omega(s)-t

for every state and both translations. Taking s=t recovers the displacement representation from the covariance identity. Thus no regularity, bijectivity, or invertibility assumption is implicit in that representation. Preservation is the equality of Borel measures tau_*xi=xi, and the tested invariance is the law of the shifted *joint pair*, not that pushforward equality alone.

For mass-stationarity, a relatively compact C of positive Haar measure and Haar-null boundary is placed around the origin by an independent uniform U in C. Conditional on the state and U, V is chosen according to the normalized restriction of xi to C-U. The required joint identity is

    (theta_V omega,U+V) =_d (omega,U).

The 2009 definition permits a general sigma-finite state-space measure, and does not assume that the law to be tested is itself stationary. This candidate uses a probability law. Neither full support nor absolute continuity with respect to planar Lebesgue measure is required. “Diffuse” means no atoms.

The relevant primary sources are [Thorisson's problem list](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf) and [Last–Thorisson (2009)](https://arxiv.org/abs/0906.2062), especially Example 3.4, Definition 6.1, Remark 6.2, Example 7.1 and Problem 7.5. The source allocation identities hold pointwise, not merely modulo an unspecified spatial-null equivalence relation. A version with only such an equivalence relation would need a separate definition at the root and is not silently covered by this verdict.

## Complete measurable model

Let lambda be Lebesgue measure on R and put

    nu = sum_(n in Z) delta_n + 2 sum_(n in Z) delta_(n+1/2),
    mu = lambda tensor nu.

The horizontal coordinate is the lambda coordinate. Let T=R/Z, use its Borel sigma-algebra, and define

    theta_(a,b) u = u+b mod 1,
    mu_u = theta_(0,u) mu,
    xi(u)=mu_u,
    Q=delta_0.

Take X constant with trivial action. The two families of supporting lines of mu_u have heights n-u and n+1/2-u, and densities 1 and 2, respectively.

Each mu_u is a locally finite Radon measure: a compact rectangle meets only finitely many lines and each intersected line has finite horizontal length. Every singleton has zero mass. The measure is nonzero and the origin lies in the support under Q. The action is jointly Borel and satisfies xi(theta_t u)=theta_t xi(u).

The state is exactly the observed measure, rather than an enlarged ambient space. To check this carefully, for a continuous compactly supported test function phi, the expression integral phi dmu_u is a locally finite sum of continuous translated line integrals, uniformly with only finitely many contributing integer indices as u ranges over a compact phase interval. Thus u -> mu_u is continuous in the vague topology. It is injective: equality of the measures must identify the density-1 line family, hence identify u modulo 1. Compactness of T and the Hausdorff vague topology make this map an embedding. Its inverse on its image is Borel and sigma(xi)=B(T). No independent coordinates or randomness have been hidden in the state.

If a formulation insists that a displacement be defined on the full canonical space of Radon measures, there is also a Borel extension. The orbit K={mu_u:u in T} is compact, hence closed, and invariant under translations. Define a displacement on K through the inverse phase map and put it equal to zero on K's complement. The induced allocation is the identity off this orbit, because the complement is translation invariant. Thus any globally preserving allocation on the displayed orbit extends to one on the full canonical space. Conversely, any full-space allocation restricts to this orbit. This removes a possible domain-of-definition objection without changing the test class relevant to Q.

The exact translation stabilizer of every orbit state is R x Z. Horizontal translations do nothing; vertical integer translations preserve both line families. A half-integer vertical translation exchanges densities and is not a symmetry. These symmetries are allowed in the original problem and are the mechanism of the example.

## Universal allocation classification by test functions

Fix an arbitrary measurable pointwise-covariant allocation of this state. Write

    pi(0)=(a0,b0),    pi(1/2)=(a1,b1).

At u=0, covariance forces, for every real x and every integer n,

    tau_0(x,n)=(x+a0,n+b0),
    tau_0(x,n+1/2)=(x+a1,n+1/2+b1).

This follows directly by evaluating theta_(x,n)0=0 and theta_(x,n+1/2)0=1/2. It does not posit that a measurable map of a line has to be a translation: the full horizontal stabilizer and the unit vertical period force it. Arbitrary measurable distortions, partitions, rescalings, or separate translations of individual members of one periodic family would violate this covariance identity on the observed state. The only permitted horizontal motions on the two support families are the two arbitrary translations a0 and a1.

For every nonnegative Borel test function f on R², Tonelli's theorem and translation invariance of lambda give

    integral f(tau_0(s)) mu(ds)
      = sum_n integral_R f(x+a0,n+b0) dx
        + 2 sum_n integral_R f(x+a1,n+1/2+b1) dx
      = sum_n integral_R f(z,n+b0) dz
        + 2 sum_n integral_R f(z,n+1/2+b1) dz.

This is the full Borel pushforward identity, including infinite integrals; it is not a finite-window approximation. Hence

    (tau_0)_*mu
      = lambda tensor [sum_n delta_(n+b0)
                       +2 sum_n delta_(n+1/2+b1)].

Preservation at the single Q-supported state therefore implies equality of the bracketed measure with nu. To obtain a finite quotient identity, first restrict the vertical measure to [0,1), and only then map that interval to T. Each period has exactly one line from each output family. With [r] denoting a residue modulo 1, the resulting finite identity is

    delta_[b0] + 2 delta_[1/2+b1] = delta_0 + 2 delta_(1/2).       (A)

Pushing the entire infinite measure directly to T would give infinite atoms; that invalid maneuver is unnecessary and is not the argument in the frozen proof.

All cases in (A) can be settled without assuming a bijection. Positivity first excludes either output residue lying outside {0,1/2}. If the two residues coincide, the target receives weight 3, impossible at either supported residue. If the residues are exchanged, the target at 0 receives weight 2 instead of 1. The only remaining assignment is

    [b0]=0,    [1/2+b1]=1/2,

which is precisely b0,b1 in Z. Two density-1 lines cannot merge to make a density-2 target: their images are at heights n+b0, so distinct integers n give distinct target lines. There is just one density-1 family per forced period. Rational weights 1 and 2 suffice; an irrationality assumption is unnecessary in this periodic model.

The calculation gives the following complete classification on this orbit. A Borel pi induces a preserving allocation if and only if the vertical components of pi(0) and pi(1/2) are integers. Their horizontal components are arbitrary. Values of pi on T minus {0,1/2} are arbitrary Borel values. Necessity follows from preservation at u=0. For sufficiency at an arbitrary u, the source lines are n-u and n+1/2-u, and their images have those same respective heights plus b0 and b1. Integer b0,b1 permute each family and the horizontal translations preserve lambda. This establishes preservation at every state.

It follows that for every preserving allocation,

    theta_(tau_0(0)) 0 = b0 mod 1 = 0.

Both X and xi are therefore fixed at the rooted state, so the required joint distributional invariance holds. The statement is valid whether preservation is demanded everywhere or only Q-almost surely, because Q=delta_0 and necessity already used only that one state. Since sigma(xi)=B(T), allowing measurable dependence on the whole pair does not enlarge the available information beyond this phase space, and the older xi-measurable subclass is also covered.

This addresses the zero-mass root objection. Although {0} has mu-mass zero, assigning its image differently changes pi(0), and therefore changes the images of the entire horizontal line through zero and all its integer-period translates. Positive-mass line segments constrain that image. The root is not a freely mutable spatial-null exceptional point in the source's pointwise-covariant class.

## Direct mass-stationarity failure and consistency check

Take C=[0,1)². It has Haar measure 1, compact closure, and Haar-null boundary. For every U in this box, the vertical interval [-U2,1-U2) contains one density-1 line, at height 0, and one density-2 line, at height 1/2 or -1/2. Half-open endpoints cause no ambiguity even at U2=0 or 1/2. The horizontal interval has length 1. Thus

    mu(C-U)=3,
    P(V2=0 | U)=1/3,
    P(V2 in {-1/2,1/2} | U)=2/3.

The measurable evaluation H(eta)=eta([0,1) x {0}) equals 1 at the original measure. At the shifted measure theta_V mu it is the density of the sampled line, hence equals 2 with probability 2/3. The event {H=2} consequently has probabilities 0 and 2/3 before and after the specified mass choice. Even the state marginal fails to be invariant, so the full defining joint identity fails. No Palm-lift theorem or uniqueness claim is needed for this conclusion.

As an independent consistency check, uniform phase on T is stationary for this flow. For the unit square B and nonnegative Borel f on T, the Campbell expression is

    integral_T integral_B f(theta_t u) mu_u(dt) du
      = f(0)+2f(1/2).

The intensity is 3, so the associated normalized Palm law is (delta_0+2delta_(1/2))/3. This agrees with the direct mass sampling. Difference from this particular Palm law alone would not prove the needed failure; the previous paragraph proves it directly.

## Adversarial controls and exact class boundaries

**Admissible positive controls.** Identity, every fixed horizontal translation, and every fixed integer vertical translation are preserving. More generally the complete classification permits independent arbitrary a0,a1 and independent integer b0,b1. It also permits highly noninjective and nonsurjective global allocations, which illustrates that injectivity was not tacitly imposed. Using representatives r in [0,1), set

    pi(r)=(0,0) if r=0 or 1/2;
    pi(r)=(0,-r) otherwise.

This is Borel. On every state's supporting lines the allocation is the identity, and so it preserves xi everywhere. At state 0 it maps both (0,1/3) and (0,1/4) to (0,0). Its entire image at that state lies on integer or half-integer horizontal lines, so it is not surjective onto R² either. The lost off-support locations have zero source mass. The origin itself remains constrained because its entire translation orbit inside the density-1 family carries positive mass.

**A mass-preserving map that is excluded by covariance.** At the fixed state mu define a Borel map by

    (x,n)     -> (x/2,n+1/2),
    (x,n+1/2) -> (2x,n),

and leave off-support points fixed. It preserves mu: compressing a density-1 line by the horizontal factor 1/2 gives density 2, while expanding a density-2 line by factor 2 gives density 1. It changes the rooted type. It is therefore a genuine continuous-mass transport, but fails the source covariance. The state is fixed by horizontal translation t=(1,0), whereas at s=0 the two sides of tau(s-t)=tau(s)-t are (-1/2,1/2) and (-1,1/2). This is why atomlessness by itself does not supply an admissible splitting allocation. Arbitrary measure-preserving geometric maps form a larger class than the original problem's allocations.

**A root-changing allocation after adding a stationary independent background.** Let r be uniform on T, independently of the original state, and use the enlarged flow

    theta_(a,b)(u,r)=(u+b,r+a) mod 1.

The background alone is stationary; it can be represented by the jointly measurable stationary field Y_s={r+s1}. For representatives u,r in [0,1), define

    pi_bg(u,r)=(-r/2,1/2),             if u=0;
    pi_bg(u,r)=(r,-1/2),              if u=1/2 and r<1/2;
    pi_bg(u,r)=(0,0),                 otherwise.

Generate the allocation by the source displacement formula on this enlarged state. It is globally Borel and pointwise covariant by construction. Fix a state (u,r) and a horizontal cell [k-r,k+1-r). Write v=x-(k-r). A light line's whole cell, 0<=v<1, is compressed onto the first half of the neighboring heavy line by v -> v/2. The first half of the heavy cell, 0<=v<1/2, is expanded back onto the whole light cell by v -> 2v. The second half of the heavy cell is fixed. The respective received densities are 1/(1/2)=2, 2/2=1, and 2. Thus each complete target light cell has density 1 and each complete heavy cell has density 2. Off-support points are fixed. This proves preservation for all phases by countable cell decomposition, not merely on a sampled grid.

Under delta_0 tensor Haar, pi_bg has vertical component 1/2 for every r. Consequently the original measure marginal changes from mu_0 to mu_(1/2) with probability one. The candidate therefore fails the background-extended allocation premise, exactly as the established theorem would require. This is not an original-pair counterallocation: its horizontal slicing coordinate r is absent from that pair. It provides a falsifiable class distinction instead of a generic warning about extra randomness.

**An explicit preserving Markov kernel.** On the two support types, use the stochastic matrix

    P = [[0,1], [1/2,1/2]].

In spatial terms, from a light line send to the neighboring heavy line at vertical displacement +1/2. From a heavy line send half to the light line at displacement -1/2 and half to itself. Keep the horizontal coordinate fixed; off support use the identity kernel. The observed phase identifies the types, so the kernel is pointwise covariant and Borel. The balance calculation is

    (1,2) P = (1,2).

It preserves mu, but from a light root its shift is to a heavy root with probability one. Hence the candidate is not invariant under all preserving Markov kernels. The deterministic quotient calculation is not being misapplied to kernels; the neighboring general Markov-characterization problem is not resolved here.

**Boundary checks.** Equalizing the two densities permits a swap in the finite mass equation and also gives the measure an additional half-period symmetry, invalidating this particular two-type witness. Allowing an additional density-1 source family permits two light sources to feed a density-2 target. The independent checker exposes both changes. The frozen proof uses exactly two periodic families and positive unequal densities, so these are genuine hypothesis tests rather than counterexamples to its argument. Removing the continuous invariant direction or adjoining background information changes the rigidity mechanism and calls for a separate theorem. This example is singular relative to planar Haar measure and is not a strictly positive density example.

## Primary cross-checks, computation and remaining gap

I independently read [Last–Thorisson's 2015 manuscript](https://arxiv.org/abs/1405.7566), section 6's theorem and proof, section 7's definitions, example and Theorem 7 proof, and section 8 Proposition 1 and Theorem 8. Proposition 1 is precisely the established Lebesgue-product mechanism preserving and reflecting mass-stationarity; it is appropriately credited in the current addendum. Its product-box argument is consistent: the extra coordinate is independently uniform in the translated interval, and after the mass choice its new position is independently uniform in the original interval. That leaves the original-coordinate joint identity equivalent. The central verdict here does not require this proposition because both allocation invariance and mass-stationarity failure were verified directly. Theorem 7's independent-background requirement is essential and agrees with the explicit control above. The positive-density Theorem 6 has further line-integrability and infinite-half-line-integral assumptions; the present singular example does not meet even its density premise.

The 2023 [transportation manuscript](https://arxiv.org/abs/2112.13053), section 8, already uses horizontal Lebesgue lines over a canonical vertical Poisson process as a diffuse allocation obstruction without external randomness. The 2024 [factor-point-process manuscript](https://arxiv.org/abs/2303.05137), introductory Theorems 1.1–1.2 and definitions, makes the no-invariant-direction boundary explicit. These are direct known overlaps and scope context, not evidence of a novelty claim or substitutes for the proof above. I did not investigate the unrelated PR mentioned in the historical metadata.

`check_allocations.py` is an independent read-only standard-library harness. It authenticates the original manifest's external pin, all 26 original file hashes and their membership/total size, and all five primary PDF hashes. It runs no inherited program and writes no fixtures. Ordinary and optimized Python both exited successfully, with actual timestamps, interpreter commands, script hashes, stdout and stderr in `RECEIPT_NORMAL.json` and `RECEIPT_OPTIMIZED.json`. Each run checks:

* the nine quotient assignment categories, including collisions and off-support residues;
* 16,807 rational instances of the full allocation covariance identity and 147 exact product-rectangle identities;
* the admissible noninjective/nonsurjective control and the excluded density-swap control;
* 46,656 exact background-covariance instances and 506 exact affine-cell interval identities;
* equal-weight and extra-family assumption controls, the Markov balance matrix, and the mass-sampling discrepancy.

These are exact rational diagnostics and sign/implementation controls. They are not a finite enumeration offered in place of the universal proof. The test-function argument, finite per-period measure identity, measurable-state construction, explicit counterclass controls, and direct mass-sampling event supply the checkable mathematical artifacts.

**Strongest verified result:** the entire source-scoped counterexample theorem stated at the top, with the full classification of preserving allocations on its phase orbit. **Exact remaining mathematical gap:** none identified. **Unverified broader claims:** none are needed; novelty, priority, general stronger-premise theorems, and whole-program completion are not certified by this bounded audit. Completion of the assigned allocation family is 100%.

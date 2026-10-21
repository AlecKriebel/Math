# A checkable classical product specialization and its exact scope

This is the priority reviewer's deduction, not a claim that Zelik explicitly called his examples a counterexample to Eden's conjecture. It identifies which part of the unrestricted imported question is already elementary in the classical product framework. It does not replace the mathematically verified entire-R5 construction in PR111.

## Primary source actually read

Sergey Zelik, *A remark on a uniform Lyapunov dimension of cascade systems*, author-hosted preprint, https://sergey-zelik.co.uk/publications/dlyap.pdf. The author publication list links this exact body: https://sergey-zelik.co.uk/publications/publications.htm. Retrieved 2026-10-06; 217864 bytes; SHA256 `0e7eaa6b186887bf138a8ce0fdd3cdbce0164c9956aaf308e14cd16782029141`.

Read the introduction, Section 1, and Examples 3.1–3.3, printed pp. 10–12. The framework is a continuously differentiable cascade map on a compact invariant set in a product phase space. Example 3.1 treats decoupled products and merged component exponents; Example 3.2 treats torus translations with zero external exponents. Example 3.3 explicitly uses a global attractor attracting all bounded subsets of the chosen product phase space. Smooth linear maps meet the continuity and uniform differentiability hypotheses without a regularity gap.

The associated published paper is *On the Lyapunov dimension of cascade systems*, CPAA 7(4) (2008), 971–985, DOI https://doi.org/10.3934/cpaa.2008.7.971. Publisher metadata gives received June 2007, revised November 2007, online April 2008. The author PDF is undated and has a different title and numbering. The publisher PDF was not retrieved: the historical PDF URL in publisher HTML returned 404. Search-index text points to published Examples 4.1–4.3 on pp. 980–981, but this audit does not authenticate those printed pages as a downloaded publisher body. All detailed source references below are to the author PDF actually read. The older intrinsic manifold dimension convention is independently explicit in Gelfert (2003), printed pp. 553–555, https://ems.press/content/serial-article-files/35401.

## Explicit finite-dimensional specialization

Let T2 = R2/Z2 and give M = R × T2 the flat product metric. Consider

    x' = -x,
    theta1' = 1,
    theta2' = sqrt(2).

Its flow is

    phi_t(x, theta) = (exp(-t)x, theta + t(1,sqrt(2)) mod Z2).

This is a real-analytic, complete autonomous flow on the smooth three-dimensional manifold M. The time-one map has the decoupled form of Zelik's Example 3.1 with internal map x -> exp(-1)x and external translation of Example 3.2. The tangent derivative of the external translation is the identity. No inference from arbitrary matrix cocycles to derivatives of an autonomous flow is needed here.

### Dissipativity and global attractor

K = [-1,1] × T2 is compact and positively invariant. Every bounded subset E of M satisfies |x| <= R for some finite R. Its image enters K after any time greater than max(0,log R). Thus the flow is dissipative in the bounded-set/compact-absorbing-set sense; it is also strictly contracting in intrinsic three-dimensional volume, since its divergence is -1.

A = {0} × T2 is compact and fully invariant. With the product metric,

    sup_(x,theta) in E dist(phi_t(x,theta), A) <= exp(-t) R -> 0.

It therefore attracts every bounded subset of the full phase M. It is the minimal closed global attractor: any closed set C attracting all bounded sets must attract the bounded set A itself. Since phi_t(A) = A for all t, this forces dist(a,C)=0 for every a in A and hence A is contained in C. This is minimality as a global attractor. In addition, each continuous-time orbit in A is dense in A: there is no nonzero integer pair (m,n) satisfying m+n sqrt(2)=0, so the irrational linear flow has no proper orbit-closure subtorus. Thus A is also a minimal invariant set. Discrete time-one minimality is neither needed nor asserted.

### Absence of equilibrium and periodic competitors

There is no equilibrium in M, because the angular velocity (1,sqrt(2)) never vanishes. If a trajectory had a positive period T, its angular coordinates would require T=m and sqrt(2)T=n for integers m,n. Since T>0, m>0, contradicting irrationality of sqrt(2). This includes x=0; a nonzero x cannot be periodic because exp(-T)x != x. Consequently there are no equilibrium or periodic trajectories anywhere in M, including A.

### Intrinsic local and uniform dimensions

In the flat product tangent spaces, Dphi_t is diag(exp(-t),1,1), with singular values (1,1,exp(-t)) for t>0. Thus every trajectory has ordered intrinsic Lyapunov spectrum (0,0,-1). Under the Kaplan–Yorke convention using the last nonnegative partial sum, j=2 and

    d_KY = 2 + (0+0)/1 = 2.

Every point of A attains the supremum 2. The fixed-global-j convention also gives j=2 and dimension 2. Finite-time singular-value dimension is exactly 2 for every t>0. Uniform exterior-growth dimension is also 2, since omega_d(Dphi_t)=1 for 0<=d<=2 and exp(-(d-2)t) for 2<d<=3. Hence there is no convention mismatch among these quantities in this specialization. All maximizers are aperiodic and there are no equilibrium/periodic candidates.

## Mapping to the imported target

The authenticated target is AMR-048-0006 / source 4900006, not source 491: a smooth dissipative dynamical system with a global attractor is asked to have a local-Lyapunov-dimension maximizer at an equilibrium or an unstable periodic orbit. No Euclidean-only, chaos, genericity, transitivity, or existence-of-competitors assumption is stated. Under the ordinary smooth-manifold/intrinsic-tangent interpretation, the preceding classical specialization satisfies every explicit hypothesis and makes the proposed conclusion false. This demonstrates that a first resolution of that unrestricted wording is not a defensible novelty claim. It does not establish the intended quantifiers of Eden's unread original thesis or refute any additional historical hypothesis that is absent from the imported wording.

## Mapping to Parker–Goluskin's ambient convention

Parker–Goluskin, arXiv:2510.14870v2 (21 January 2026), actual body SHA256 `c8e53fbd26bd51b270deb81cf318161cb14f260ab827a0996d401fee899c6e7c`, printed pp. 2, 5–7, https://arxiv.org/pdf/2510.14870v2, explicitly allows a lower-dimensional manifold embedded in Rn as phase space on p. 2, but defines tangent evolution through the full n-by-n ambient Jacobian on p. 5. Its Definition 2.3 chooses one global j over the given forward-invariant set. The intrinsic three-exponent calculation above cannot be silently substituted into that ambient convention.

Embed M as B = R × S1 × S1 in R × C × C = R5 via z_i = exp(2 pi i theta_i). Choose the explicit smooth ambient extension

    F(x,z1,z2) = (-x, 2 pi i z1, 2 pi i sqrt(2) z2).

On B this is exactly the preceding flow. B is forward invariant, and all positive trajectories starting in B are bounded. A_B = {0} × S1 × S1 is the compact minimal global attractor for the phase B: its ambient Euclidean distance from phi_t(x,z1,z2) equals exp(-t)|x|. It has no equilibria or periodic trajectories, by the same integer-period argument.

The full ambient derivative has one exp(-t) multiplier and two planar rotation blocks. Its singular values are (1,1,1,1,exp(-t)); its ordered ambient spectrum is (0,0,0,0,-1). Thus Definition 2.3 has global j=4 and dimension 4 at every point of A_B. Intrinsic dimension 2 and this ambient dimension 4 are different valid computations for different tangent conventions. Normal radial directions supply the two additional zero exponents of this extension.

This embedded example fits the phase-space scope explicitly allowed by Parker–Goluskin. It is global relative to B, exactly as the product literature uses its chosen phase. The chosen linear extension does NOT have a compact global attractor on all R5: arbitrary |z1| and |z2| are conserved, giving invariant tori at arbitrarily large radii. No compact set can attract every such invariant set. Changing the off-manifold extension can change the normal spectrum; the extension has been fixed explicitly to avoid that ambiguity.

## What is and is not prior here

The familiar quasiperiodic product mechanism, plus this routine checkable specialization, already supplies a negative answer to the literal manifold-permitting assertion and to its embedded-manifold formulation with the explicit ambient extension above. Zelik is a source for the classical framework, not an authenticated publication of this exact three-variable example under an Eden-counterexample label. The author PDF's undated status and the unavailable publisher body should remain visible in the bibliography audit.

It does not supply PR111's stronger theorem for a real-analytic field on all R5 with a compact global attractor for that entire phase, strict volume contraction everywhere, actual equilibrium/periodic competitors all having lower dimensions, a unique maximizing saddle-torus locus, and the exact maximum 203/50 under two separately stated asymptotic conventions. Those differences are mathematically checkable added content. Their existence does not, by itself, establish a substantial new resolution of a historically meaningful open conjecture. A future publication would need to frame any remaining contribution as an explicit Euclidean construction and exact certificate, credit the classical product mechanism, and avoid claiming first disproof of the unrestricted imported sentence or of the historical Eden conjecture.

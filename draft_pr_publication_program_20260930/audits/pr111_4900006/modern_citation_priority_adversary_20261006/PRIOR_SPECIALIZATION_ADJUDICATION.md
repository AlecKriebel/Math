# Adjudication of the prior quasiperiodic obstruction

Date: 2026-10-06. This is a check of the consequence of existing product/torus theory, not a new search for a central proof. It is independent of the newly commissioned priority reports. The mathematical proof of PR111 is separately authenticated by the root gate.

## Exact phase space and flow

Consider the standard product flow on the manifold

    Ω = R × S¹ × S¹,
    Φ_t(w,θ1,θ2) = (e^(−t)w, θ1+t, θ2+√2 t),

where angles are modulo 2π. Its generator is (−w,1,√2). This is the decaying internal equation with independent quasiperiodic external dynamics. The author version of Zelik's cascade paper supplies the direct-sum mechanism, torus dynamics and global-attractor phase-space framework: introductory pp1–3 and Examples3.1–3.3 on pp10–12. The specialization and the following elementary checks are our deductions from that framework; the source does not call this an Eden counterexample. The official publication is CPAA7(4):971–985 (2008), DOI10.3934/cpaa.2008.7.971. The retrieved author version has a different title/numbering from the journal version; the exact journal PDF was unavailable at three publisher URL variants. Do not silently treat author and journal pagination as identical.

The set A={0}×S¹×S¹ is compact and invariant. For any bounded E⊂Ω,

    sup_(x∈E) dist(Φ_t(x),A) ≤ e^(−t) sup_(x∈E)|w(x)| → 0.

Thus it is a genuine global attractor relative to the specified phase space. It attracts all bounded subsets, not merely one chosen orbit. Its invariance also proves minimality: if a closed set attracts the bounded set A, the invariance Φ_t(A)=A forces containment of A.

There are no equilibria because the angular velocities never vanish. There are no periodic orbits: a period T>0 would require T=2πm and √2 T=2πn for integers m,n, which contradicts irrationality. All trajectories in A are quasiperiodic. No chaos, genericity or transitivity of the entire noncompact phase space is asserted.

## Two tangent conventions, explicitly separated

The intrinsic derivative on TΩ has singular values 1,1,e^(−t), hence spectrum (0,0,−1). The usual nonnegative-partial-sum Kaplan–Yorke value is 2 everywhere on A. Equilibrium/periodic attainment is impossible because neither orbit type exists.

To check the ambient convention used in Parker–Goluskin, embed Ω in R⁵=C²×R by |z1|=|z2|=1 and use the real-analytic ambient extension

    z1'=i z1, z2'=i√2 z2, w'=−w.

Its full ambient derivative is block diagonal with two orthogonal rotations and e^(−t). Its ambient singular values are 1,1,1,1,e^(−t), with spectrum (0,0,0,0,−1). In Definition2.3 of Parker–Goluskin, j=4 and D4=4 everywhere, for B=A or B=Ω. The finite-time nonnegative-partial-sum expression is also exactly4 at every t>0. This proves failure of their unrestricted attainment assertion under their own ambient derivative convention. It would be wrong to substitute the intrinsic value2 into that ambient formula.

The extension has divergence−1 on R⁵, but it does **not** have a compact global attractor attracting all bounded subsets of R⁵: ambient radii are conserved. Its compact global attractor is relative to Ω. This distinction is essential. It is admissible to the literal manifold-inclusive modern scope: Parker–Goluskin v2 p2 permits embedded lower-dimensional phase spaces, Section2.1 p5 treats forward-invariant B, and Definition2.3 p7 imposes no requirement that equilibria or periodic orbits exist. A claim that additionally requires the phase space to be all Rⁿ would exclude this elementary obstruction and needs a separate audit.

## What does and does not follow about priority?

The product mechanism is explicitly prior. The exact unrestricted manifold-inclusive maximizer assertion is already contradicted by its elementary specialization. This is mathematically sufficient prior-theory evidence against promoting that broad assertion as a novel longstanding resolution. It is **not** evidence that Zelik explicitly announced a disproof of Eden's historical conjecture, nor that every stronger Euclidean/nonvacuous formulation was previously answered.

PR111's accepted v2 construction supplies a stronger theorem: a complete real-analytic vector field on all R⁵, a compact global attractor for the full phase space, one actual equilibrium and four actual periodic circles, strict ambient volume contraction, and an aperiodic torus whose local dimension strictly exceeds every equilibrium/periodic value under two separately computed conventions. Those features do not follow simply by replacing the contracting equation in the torus product; global radial behavior and competing orbit values must be designed and verified. No identical prior theorem was found in this bounded modern search. Its originality and research value remain unestablished; stronger explicitness alone cannot turn an already elementary broad negative answer into a new resolution of the historical or generic problem.

No Git/PR/publication action is authorized by this adjudication.

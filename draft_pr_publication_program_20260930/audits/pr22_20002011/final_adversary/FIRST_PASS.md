# Independent first pass — before earlier mathematical audit evidence

This first pass read the two governing AGENTS.md files, queue README and the two queue rows, the current written proof and source-scope/status documents, both complete source records, and the full pinned upstream prior reports for numeric records 20002011 and 20002052. The pinned reports are untrusted historical inputs. The current README reports previous passes, but their proofs, results, scripts and historical independent_review have not been inspected. A short source-only AIM excerpt was initially read from the root source cache, then the original AIM PDF was independently downloaded and its complete relevant pp. 16–18 and 27–28 read. No root/family derivation, previous independent review, author verification script, Branson proof, or their computation receipts has yet been inspected.

## Exact acceptance claim and boundaries

The target is AIM 2003 Conjecture 1, p. 17, identically reprinted as Problem 30, p. 28. For a universal natural density S on closed oriented even-dimensional Riemannian manifolds, conformal invariance of its integral is asserted to imply S=aQ+L+G. Here L is pointwise conformally invariant as a density; Q is a critical Branson Q-density with self-adjoint critical GJMS conformal linearization; G is a conformal gradient of the integral of a smooth natural local density F at every metric and in every smooth conformal direction. The source distinguishes a two-metric primitive from a single-metric local primitive. It adds no formal-self-adjointness hypothesis on S. The surrounding invariant-theory text includes polynomial curvature contractions of critical weight, so an example in that narrower class is sufficient. The all-dimensional implication is falsified by a single allowed dimension and metric; a universal counterexample in every dimension is unnecessary.

Acceptance must independently establish the universal variational implication, compute the actual density variation including volume and connection, realize an admissible closed smooth example, convert pointwise skew to an integrated witness, and verify published priority from Branson's full relevant proof. It must reproduce each saved script receipt and challenge metadata, exact hashes, original budget and duplicate/source provenance. A published refutation supports already_solved/exclusion for this literal target; it does not solve an independently formulated self-adjoint/generalized-Q conjecture or support a new paper/DOI. Whether the package satisfies those source/provenance conditions is still unverified at this checkpoint.

## Independent variational derivation

Fix g and write g_u=e^(2u)g. If H is a gradient, dF(u)[v]=∫vH_(g_u). Mixed derivatives in fixed function directions v,w commute, so ∫v D_gH(w)=∫w D_gH(v). This uses the variation of the density, not of its scalar coefficient alone. Smooth local metric-jet dependence suffices for the two derivatives. The conformal factor directions commute because they add in the affine space of factors. A pointwise invariant L has D_gL=0. Q has D_gQ=P_g with P_g formally self-adjoint. Therefore every asserted S=aQ+L+G has symmetric density linearization, independent of how a decomposition might be chosen. Adding a different pointwise invariant or a conformal gradient cannot remove a nonzero skew part.

Conformal invariance of ∫S merely gives ∫D_gS(w)=0 for all w; equivalently D_gS*1=0. It is not the stronger identity D_gS=D_gS*. The second variation of ∫S being zero is immaterial: the proposed primitive has ∫wS as its first variation, whereas ∫S is a different functional.

## Independent universal conformal computation

Use Δ=∇^i∇_i, J=R/(2(n−1)), P=(Ric−Jg)/(n−2), B=|P|². Differentiating the connection gives δΓ^k_ij=δ^k_i w_j+δ^k_j w_i−g_ij w^k. Hence δP_ij=−∇_i∇_j w and δB=−4wB−2P^ij∇_i∇_j w. The inverse metrics in B supply its −4wB term. For a varying scalar b, δ(Δb)=−2wΔb+(n−2)⟨dw,db⟩+Δδb, including the trace of δΓ. Volume contributes δdV=nw dV.

For S=ΔB dV, the complete scalar coefficient of its density variation is

  A_n w=(n−6)wΔB+(n−10)⟨dw,dB⟩−4BΔw−2Δ(P^ij∇_i∇_j w).

At n=6 this is A w=−4 div(B∇w)−2ΔT w with T w=P^ij∇_i∇_j w. The first term and Δ are formally self-adjoint. Two successive integrations by parts give T*h=∇_j∇_i(P^ij h); no derivative-order exchange is assumed. Thus A−A*=−2(ΔT−T*Δ). Expanding T* gives T h+2⟨dJ,dh⟩+(ΔJ)h, using contracted Bianchi ∇_iP^ij=∇^jJ. Retaining the first-order and zeroth-order adjoint terms is essential.

Under a constant scaling e^(2c)g, P_ij stays fixed, B scales e^(−4c), Δ scales e^(−2c), and dV scales e^(6c). Thus S has exactly critical density weight zero, scalar weight −6, and physical scalar dimension length^(−6). It is parity-even polynomial and diffeomorphism-natural. ∫S=0 on every closed six-manifold by Stokes, independently of conformal variation. The general n formula must not silently be declared critical for n≠6.

## Independent closed geometric realization

On a flat oriented T^6 choose a coordinate ball, a smooth bump χ equal to 1 on a smaller ball, and extend f=χx1x2x3 by zero. The metric e^(2f)g0 is globally smooth and positive definite. Set w=f (or a separate smooth extension of the same local cubic). At p=0, f=df=Hess f=0, so Γ(p)=0, ∂Γ(p)=0, P(p)=0, and ∇_kP_ij(p)=−f_ijk(p). The cubic is harmonic, and the exact trace formula J=−e^(−2f)(Δ0 f+2|df|²) has order at least four near p. Thus dJ(p)=0.

At p, w=dw=Hess w=0. The product rule for ΔT w leaves only 2∇P·∇Hess w, equal to −2∑_ijk f_ijk²=−12. The six permutations of (1,2,3) each give 1. In T*Δw, the three types of terms contain respectively P(p), dJ(p), or Δw(p); all vanish. Therefore (A−A*)w(p)=24. A itself gives 24 and A* gives 0 at this jet; the fourth-order principal terms agree and the obstruction is lower-order.

The function K=(A−A*)w is smooth and positive on some smaller ball. A nonnegative smooth nonzero v supported there gives

  ∫v A w dV−∫w A v dV=∫vK dV>0.

All integrations by parts are on the closed torus. The cutoff outside this neighborhood neither changes its jets nor produces boundary terms. This supplies a genuine integrated obstruction to any claimed decomposition. Changing the sign convention of Δ changes the witness sign but cannot make it zero.

The Ricci comparison is consistent: Ric=4P+Jg, tr P=J, so |Ric|²=16|P|²+14J² in n=6. Varying ∫J³dV gives −3∫wΔJ² dV. Thus ΔJ²dV is a conformal gradient, with no skew contribution, and the Ricci-norm divergence has the same obstruction multiplied by 16.

## Attempts to falsify and first-pass status

Potential failures tested by the deductions above: confusing scalar/density symmetry; omitting volume; imposing flatness on the deformed metric; using unconstrained curvature jets; losing trace or connection terms; inferring a global integral witness from a point value without support; choosing an example of the wrong weight; treating arbitrary zero-integral divergences as gradients; transferring the repaired hypothesis to the literal statement; claiming all dimensions from a six-dimensional formula. None defeats this candidate's universal proof.

Novel independent computation controls planned after this seal: a finite Fourier/Laurent-polynomial closed periodic witness with a nonzero exact integrated pairing (not only local point jets), nonlinear mutation checks on omitted trace/volume/adjoint terms, and anisotropic/scaled cubic controls. These finite controls supplement the proof; no successful computation will substitute for its universal quantifiers.

First-pass verdict: the mathematical obstruction in SOURCE_STATUS.md sections 3–4 is sound under the stated closed smooth Riemannian assumptions. The literal AIM duplicate identity is supported by the complete primary statement. Published-prior classification, all receipts, full package/history integrity and repaired-target boundary remain to be checked. Acceptance-audit completion estimate: 25%.

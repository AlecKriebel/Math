# KSZZ adversarial check: DGP24 semistability scope

Checkpoint: 2026-10-07 05:40 UTC (2026-10-06 22:40 PDT). Completion estimate: 100% of this scoped citation-and-slope audit; this is not an estimate for the whole KSZZ audit.

## Claim tested

For a K-semistable complex Q-Fano variety X and a smooth projective birational model p:W→X, the ordinary cotangent bundle Ω_W is slope semistable for H=p*L, where −K_X≡(n−1)L. A surjective morphism q:W→Y to a smooth d-fold then yields μ_H(q*Ω_Y)≤μ_H(Ω_W).

Success criterion: find an unfulfilled scope condition, a counterexample, or a failed sheaf/slope implication. Outcome: none found in this step.

## Primary-source evidence

[Druel–Guenancia–Păun, published PDF](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.612.pdf), DOI 10.5802/crmath.612, pp.93–118 (2024): Definition 1 uses klt singularities and ample Q-Cartier −K_X. On p.97, Assumption A asks for twisted KE metrics with every sufficiently small positive γ; Remark 4 identifies it with K-semistability. Notation 5 sets up a resolution and permits discrepancies a_i>−1. On p.100, equation (18) bounds the slope of every rank-r tangent subsheaf by [1+γ(n/r−1)]μ(T_W), measured against p*c₁(X). The following paragraph takes γ→0 and obtains semistability of T_W. Theorem 6(i), p.101, then states tangent-sheaf semistability on X. Actual KE existence is imposed only for the later polystability argument.

I also checked the [author-hosted LTW uniform-YTD paper](https://sites.math.rutgers.edu/~cl1412/papers/LTW20.pdf). Its Theorem 1.1 concerns uniformly K-stable log Fano pairs with arbitrary klt singularities; Corollary 1.2 imposes discrete automorphisms for the untwisted KE equivalence. This paper alone does not state the exact smooth-twist formulation of DGP Remark 4. That deeper analytic implication was not independently reconstructed here; DGP explicitly states it and proves the semistability implication under it.

## Independent algebraic checks

**Dualization does not require H ample.** Let E=T_W and define deg_H(F)=c₁(F)·H^(n−1). Suppose E is semistable. For a saturated subsheaf F⊂E* of rank d<n, the dual map E→F* is surjective in codimension one. If Q is its image and K its kernel, deg_H(Q)=−deg_H(F) and deg_H(Q)=deg_H(E)−deg_H(K). Semistability bounds deg_H(K)≤(n−d)μ_H(E), so −deg_H(F)≥dμ_H(E), and μ_H(F)≤μ_H(E*) follows. A nonsaturated F has degree at most its saturation because the degree of every effective divisor is nonnegative for nef H. Full-rank subsheaves satisfy the inequality by the same effective-divisor argument. Thus E* is semistable for this nef degree function.

**Additional blowups do not introduce a slope obstruction.** For any smooth projective birational model of normal X, outside a subset of X of codimension at least two the model and X agree. A subsheaf of the tangent bundle restricts there to a subsheaf of T_X. Extend and saturate it in the reflexive sheaf T_X. Its determinant degree on X equals the determinant degree on the model against p*A^(n−1), by the projection formula: all modifications supported on p-exceptional divisors have zero such degree. The rank is unchanged. Hence semistability of T_X against ample A=−K_X gives tangent semistability on any such model against p*A, even if one worries about the auxiliary resolution choice in the analytic setup. This also handles the resolved graph chosen in KSZZ.

**The differential map is an injection of sheaves.** For q:W→Y surjective with W,Y smooth over C, the field extension C(Y)⊂C(W) is separable; the generic differential has rank d. The kernel of q*Ω_Y→Ω_W is therefore torsion. Its source is locally free, so its kernel is zero. The map may fail to be a subbundle on the critical locus, but the subsheaf inequality is enough; saturation can only strengthen the required inequality.

**The displayed slope is correct.** Since K_W=p*K_X+Σa_iE_i and E_i·H^(n−1)=0,

    μ_H(Ω_W) = K_W·H^(n−1)/n = −3(n−1)/n,

using Hⁿ=Lⁿ=3. The source bundle has rank d and c₁(q*Ω_Y)=q*K_Y, so KSZZ obtains

    q*K_Y·H^(n−1)/d ≤ −3(n−1)/n.

For d<n, this leads to the claimed strict negativity after adding (d−1)q*L_Y, using q*L_Y≤H and nef H. The argument loses strict negativity at d=n, exactly as the manuscript states; it is not a valid route for that boundary case.

## Falsification status and exact remaining gap

The proposed objection that DGP24 covers only KE/K-polystable varieties fails. The cited paragraph is explicitly the K-semistable part of the proof, and its polarization is already the nef pullback anticanonical class. Dualization, graph-resolution choice, determinant degree, and q-pullback injection pass independent checks. No crepant resolution, nonpositive discrepancy, smoothability, or discrete-automorphism requirement enters these algebraic steps.

This audit does not independently reprove the analytic twisted-KE existence theorem behind Remark 4, nor certify the later vanishing/Koszul portion of KSZZ Lemma 3.5. No external communication or git mutation was performed; reviewed artifacts were untouched.

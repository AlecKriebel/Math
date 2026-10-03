# Turn 3/5: a finite-cohomological-dimension obstruction

## Attempt

The product construction failed because its geometric dimension is fixed. Test whether this is a general obstruction, and whether finite generation or a compact character sphere can turn it into a universal impossibility proof.

## 1. Algebraic lemma

Let H have integral cohomological dimension at most d<∞. If H is FP_d, then H is FP_∞.

For d=0, the trivial ZH-module Z is already projective and finitely generated. For d≥1, choose the beginning of a projective resolution supplied by FP_d:

P_d→P_{d−1}→⋯→P_0→Z→0,

with every P_i finitely generated. Put S_d=ker(P_{d−1}→P_{d−2}), with P_{−1}=Z when d=1. The surjection P_d→S_d makes S_d finitely generated. Since pd_{ZH}(Z)≤d, dimension shifting gives Ext^1_{ZH}(S_d,A)=Ext^{d+1}_{ZH}(Z,A)=0 for every ZH-module A. Hence S_d is projective. Truncating at S_d gives a finite-length projective resolution with all terms finitely generated. Append zero modules in higher degrees to obtain FP_∞.

In particular, if H is F_n with n≥max(2,d), then H is finitely presented, is FP_d, and is FP_∞. The standard equivalence F_m ⇔ F_2 plus FP_m for m≥2 now gives H of type F_∞. This last step is essential: FP_∞ alone would not imply F_∞ for a group that is not finitely presented.

## 2. Exclude all finite virtual cohomological dimension

Suppose G has a torsion-free finite-index subgroup L with cd_Z(L)=d<∞. Assume K_n=ker(f_n:G_n→Z) is F_n for some n≥max(2,d). Intersect both groups with L and set

J=G_n∩L,    K=K_n∩L.

Then K has finite index in K_n, so K is F_n. Restricting a projective ZL-resolution to ZK preserves projectivity, because ZL is free over ZK on a coset transversal. Thus cd_Z(K)≤cd_Z(L)=d. The lemma implies K is F_∞. Finite-index invariance then gives K_n F_∞, contradicting failure of F_{n+1}.

Therefore no group of finite virtual cohomological dimension can solve KOU-21.119. More precisely, no exact finite fiber length n≥max(2,d) occurs in this class. The low-dimensional bound is deliberately conservative; no extra use of the Stallings–Swan theorem is needed.

Consequences include finite-rank right-angled Artin groups, finite-rank right-angled Coxeter groups (after passing to their torsion-free finite-index subgroups), and groups with finite-dimensional classifying spaces. The Schesler–Zaremsky RACG examples therefore cannot solve the simultaneous question with a fixed finite defining complex, irrespective of how far into finite-index subgroups one passes. Increasing the defining complex can produce many separate examples, but changes G.

## 3. Why this does not prove universal nonexistence

Type F_∞ does not imply finite cohomological dimension. Thompson's group F is a familiar counterexample: it is F_∞ and contains free abelian subgroups of arbitrarily large rank. The desired G is permitted to have infinite-dimensional classifying spaces, and it is not required to have a torsion-free finite-index subgroup. Thus the dimension argument narrows the search but leaves a substantial class untouched.

One might instead argue that a finitely generated group has a finite-dimensional character sphere, so the descending BNSR sequence Σ^1⊇Σ^2⊇⋯ should stabilize. That inference is invalid. There are strictly decreasing sequences of open, antipodally symmetric subsets even of a circle, with a rational direction in each successive difference. For example, in homogeneous coordinates [x:y] with x≠0, let U_n consist of directions with |y/x|<1/n. Every U_n is open and antipodally symmetric. The rational slopes 2/(2n+1) lie in U_n but outside U_{n+1}. The existence of this toy sequence does not realize it as group invariants; it only disproves the topological stabilization argument.

For an F_∞ group H and a nonzero integral character χ, the BNSR criterion says ker χ is F_n exactly when both [χ] and [−χ] belong to Σ^n(H). Therefore the problem requires rational antipodal directions that leave the symmetric BNSR filtration at every degree, possibly in varying finite-index subgroups. Mere finite dimension of H^1 or openness of Σ^n supplies no bound.

## Outcome and exact gap

The finite-dimensional geometric route is blocked by a proved obstruction. Any solution must lie outside the class of finite virtual cohomological dimension. A universal no-go argument would require an additional uniform stabilization theorem for virtual BNSR invariants, which has not been established. The next attempt examines Thompson's group F, an explicit F_∞ group of infinite cohomological dimension with subgroups of every finite finiteness length.

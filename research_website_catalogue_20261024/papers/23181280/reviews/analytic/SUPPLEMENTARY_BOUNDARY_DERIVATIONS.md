# Supplementary exact boundary derivations

These checks were developed after the independent early mechanism was sealed. They support secondary statements and boundaries of the actual paper; they are not a replacement reduction or a claim of a new contribution.

## Symmetric root tables give an ordinary edge-additive objective

If for each root r and each edge e={u,v} the two costs coincide, write their common value as d_r(e). Every rooted orientation of every tree uses e exactly once. Consequently

`F(T) = sum_{e in T} sum_{r in V} d_r(e)`.

This is the ordinary minimum spanning-tree objective with edge weight sum_r d_r(e). The hard construction crucially has asymmetric clause-root costs; its t-root's symmetric table is only a structural forcing device. The theorem does not assert hardness of symmetric root tables. The independent script checks this identity on all 384 trees of its eight-vertex fixture.

## Integral common edge variables determine one tree and unique orientations

Consider the classical joint system in outward notation: z_r(u,v)>=0; z_r(u,v)+z_r(v,u)=x_{uv} for each root and edge; root indegree zero; all other indegrees one. Summing indegrees for any root gives sum_e x_e=N-1. For a nonempty vertex set S, select r in S. Summing indegrees over S yields

`sum_{e inside S} x_e + sum_{arcs entering S} z_r = |S|-1`,

so sum_{e inside S} x_e<=|S|-1. Also x>=0 follows from the pair sums. For integral x these inequalities imply x_e is zero or one (take two-endpoint sets), no selected cycle exists (apply the inequality to its vertices), and N-1 selected edges form a spanning tree. N=1 is the empty case. On that tree, indegree zero fixes all root-adjacent edges outward; at each subsequent vertex its one incoming parent arc leaves all other incoming arcs zero and fixes their reverses outward. Induction determines the unique rooted orientation. Thus the manuscript's interpretation of integral feasible common-edge data is sound.

## The full joint lift can nevertheless have a cheaper fractional point

Use the four-clause unsatisfiable formula

`(x1 or x2) and (x1 or not x2) and (not x1 or x2) and (not x1 or not x2)`.

Each of the four assignments falsifies one of these clauses, so the formula is unsatisfiable. Its reduction instance has N=8, K=10 and 13 graph edges. The independent exact matrix-tree determinant gives 384 spanning trees; exhaustive evaluation gives integer minimum 11. This finite minimum also follows from the reduction's universal no-instance lower bound and an explicit structured tree with only one false selected literal.

Take common edge variables x_tf=1 and x_e=1/2 on every other graph edge. Their sum is 7=N-1. For each root independently form a convex average of genuine structured-tree orientations with these same edge marginals:

* For t, f and both variable roots, average all four assignments and all 16 clause selections uniformly. Every hub attachment and every clause attachment then has marginal one half.
* For clause root q_j, select either of that clause's two variables with probability one half. Make that selected literal true and the other literal false. Average independently over both attachment choices of each of the other three clause leaves. Both variable assignments are balanced and every clause attachment has marginal one half, so the common x is unchanged. At root q_j the selected literal is always true, hence this entire root vector has cost zero.

Every averaged root vector is nonnegative, has zero root indegree, unit other indegrees, and the prescribed pair sums x. Thus combining these different root averages with the common x is feasible for the classical lift. The t-root cost is K=10 and all other root costs are zero; the fractional objective is 10, strictly below the integer minimum 11.

`EXACT_JOINT_LIFT_WITNESS.json` gives every rational x and z entry in a declared order. The independent script verifies every equality, inequality, objective, and the exact tree census. The witness confirms the distinction between an integral projection and integrality of the entire joint lift under objectives involving all root variables. It does not rely on an LP solver, floating-point tolerances, or a P-versus-NP assumption.

## Orientation transposition is substantive

For the one-positive-literal formula, attach its variable to the false hub. The structured tree's outward root costs are (3,0,0,1), total 4, above K=3. If one simply reverses the orientations without transposing the table, the root costs become (3,0,0,0), yielding a false yes-instance at cost 3. Reversing both the orientation convention and every table entry restores the original costs identically. This independent control confirms why the paper includes an explicit table transpose.

The first attempted orientation control used a true-literal tree, for which both directions happened to have zero clause cost. That nondiscriminating test was replaced by the false-literal tree above; no manuscript claim or source was changed.

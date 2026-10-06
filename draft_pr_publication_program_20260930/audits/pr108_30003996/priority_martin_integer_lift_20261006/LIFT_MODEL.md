# Exact joint integer lift audit

This is an independent check of the existing candidate and formulation lineage. It supplies no new central hardness route and no priority claim.

Let G=(V,E) be a connected simple undirected graph, n=|V|, and A its two arc directions. The following outward convention is the system stated in Friesen's 2019 dissertation, printed p8 Proposition 2, equations (2.4)-(2.7):

    z_r(u,v)+z_r(v,u)=x_{uv}       for every root r and edge {u,v}
    sum_u z_r(u,v)=1              for every v != r
    sum_u z_r(u,r)=0
    z>=0.

No cardinality equation is needed here: summing indegrees gives sum_e x_e=n-1. The inward convention in Fernandez et al., EJOR260 (2017), manuscript p7 (2a)-(2f), transposes z and uses outdegree at most1 at nonroots plus cardinality n-1. Cardinality makes those inequalities equalities. CCZ's February2010 survey, pp25-26, provides the same inward equalities. These sections supply the projected spanning-tree system. Their relevance here is exact integer model identity. Terminology such as the OWA paper's integrality property must not be read as a proof that the whole joint lift is integral for arbitrary objectives.

## Integer points and objectives

Choose any nonempty S subset V and r in S. Common-edge equality and the indegree constraints imply

    x(E(S)) = z_r(A(S)) <= sum_(v in S) z_r(delta_in(v)) = |S|-1.

For S of size2 this yields x_e<=1. An integer feasible x is therefore a 0/1 acyclic support with n-1 edges, hence one spanning tree. Conversely every spanning tree supplies feasible z by rooting it outward at every r. For a fixed tree x, its z fiber is unique even without imposing integrality on z: the root has indegree0, each neighbor must take its one incident tree arc outward from the root, and induction along the tree determines all arcs. Thus imposing integrality on x alone or jointly on x and z gives exactly the same common-tree integer realizations. Disconnected cycles cannot survive all-root constraints.

The literal source objective is exactly

    F(T)=sum_(r,a) c_r(a) z_r(a).

There are n roots and 2n|E| explicitly supplied arc costs. Every feasible integer point has n(n-1) selected z entries. Inward and outward models are equivalent by transposing every supplied cost. Any additional linear edge objective sum_e alpha_e x_e can be absorbed at one chosen root r0 by adding alpha_e to both c_r0 arc directions. Conversely any all-root table is a joint z objective directly. This is an exact bijection with no graph enlargement and no change of root count; dense encoding costs O(n|E|L) bits for L-bit rational/integer entries. Uniform addition of M to all costs adds Mn(n-1) to every integer objective and threshold. For bounded signed integer data choose M at least the largest negative magnitude; its bit length is polynomial. None of this converts arbitrary lifted objectives into projected edge objectives.

## Full-lift fractional obstruction

Use the candidate on the unsatisfiable four-clause formula

    (x or y), (x or not y), (not x or y), (not x or not y).

Its graph has hubs t,f, variables x,y, four clause vertices, and13 edges. Set B=2 and K=10. Take x_tf=1 and x_e=1/2 for every other edge. For a clause whose signs are (s1,s2), its own root's z is the average of these two outward oriented trees:

- Variable assignment (s1,1-s2), every clause attached to x.
- Variable assignment (1-s1,s2), every clause attached to y.

Every root gets its own pair of trees, sharing the displayed edge marginals. For nonclause roots use signs (1,1) in the same recipe. This satisfies every full-lift equation exactly. The symmetric t-root contribution is10, and each clause root's contribution is0 because its selected literal is true in both trees used for that root. The distributions at different roots disagree on the common underlying assignment; the linear constraints only equate their edge marginals.

Every actual common tree has objective at least11. The candidate threshold lemma forces any tree of objective at most10 to have tf, exactly four clause leaves and exactly one hub per variable; the four clauses admit no satisfying assignment. Trees of cost11 exist. Exact enumeration in `validate_lift.py` checks this without relying on satisfiability software or floating arithmetic, and saves the complete rational witness in `LIFT_VALIDATION.json`. The fractional minimum is10: all lift points satisfy x(delta(q_j))>=1, x_tf<=1 and sum_e x_e=7, so the t contribution p+2q=7-h+q is at least10.

Hence this full polyhedron is not the convex hull of its integer points. Projected spanning-tree integrality and a feasible integral lift of every tree cannot justify polynomial solution of arbitrary joint lifted integer objectives. This finite counterexample audits that inference; it is not an earlier published hardness theorem.

## Existing proof's B=2 restriction

For any candidate tree, q>=m and p+q+h=n+m+1. For any B>1 the existing structural identity is

    p+Bq = Bm+n+(1-h)+(B-1)(q-m).

B=2 therefore forces h=1,q=m under exactly the same nonnegative threshold argument. All remaining literal costs are0/1. The existing proof thus supports the elementary restriction to {0,1,2}, threshold2m+n, without new gadgets, root counts or proof budget. Uniform positive shift gives costs{1,2,3} and threshold2m+n+N(N-1). This refinement alone does not establish substantive novelty over a prior general theorem or a prior bounded-cost result.

## Adjacent fundamental-cut objective

For a demand edge {s,t}, deleting a selected tree edge {a,b} separates its endpoints precisely when the two roots give that tree edge opposite directions. Consequently its cut-membership indicator equals |z_s(a,b)-z_t(a,b)| for either fixed endpoint ordering. Summing weighted demands over all tree edges gives total tree distance. The natural expression is an absolute difference, and Bunke et al.'s actual published ILPs add cut-membership/shore variables and coupling. No reduction to an arbitrary linear objective on the unchanged Martin coordinates was established in this audit. This is a transfer gap, not a proof that every possible alternative representation or reduction is impossible.

The eight-vertex diagnostic can pad every two-literal clause by repeating a literal if an exactly-three-literal 3CNF convention is required; its simple graph and cost table remain the same. The N=1 boundary has no edge or arc variable, unique trivial tree and cost0; N=2 follows from the same equations. Root-independent symmetric costs reduce to ordinary edge-cost MST, so hard instances depend on the candidate's supplied root/direction asymmetry.

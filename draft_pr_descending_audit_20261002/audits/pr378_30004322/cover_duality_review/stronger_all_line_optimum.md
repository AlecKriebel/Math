# Post-exposure strengthening of the Turn 5 component LP result

This deduction was made only after the independent cover/duality proof and code were sealed, and after reading the frozen candidate. It is candidate-derived analysis, not an independently discovered construction. No historical novelty is claimed. The frozen candidate correctly restricts its optimality claim to arrangement components; the theorem below does not repair an error in that stated claim.

## Statement

For the Turn 5 subarrangement in the 5q-th Fermat arrangement, retaining exactly residues R={0,2,3} modulo 5 in each pencil, the exact fractional cover optimum using **all projective lines** is

    tau_all(Z_q) = 11/3 if q=1;
                   4q if q>=2.

The component-only optimum is 4q for every q>=1, as in the candidate. The Seshadri constant remains 1/(4q+1). In particular unrestricted optimality is strictly different at q=1 and agrees thereafter.

A further exact geometric conclusion is that the maximum number of singular points on a line outside the retained arrangement is q+1. Deleted Fermat lines attain it. For q>=2 they are precisely the auxiliary lines attaining that maximum, because every other class has at most two singular points and q+1>=3. At q=1 other two-point auxiliary lines also attain it.

## Complete all-line classification needed by the dual

Use the exact all-line classification proved before candidate exposure in independent_proof.md, applied to the full n=5q grid. Every projective line belongs to one of the following classes:

1. A retained Fermat component: it has 3q+1 singular points if its residue is 0, and 4q+1 otherwise.
2. A deleted Fermat component: residue 1 or 4. It contains exactly q surviving grid points, all double points, plus its coordinate vertex. For residue 1, the other two residues must both be 2; for residue 4 they must both be 3. Each equation has q lifts after one remaining index is fixed. Thus its point count is q+1, and its load under the candidate dual is q/(2q)=1/2.
3. A coordinate axis: it contains exactly two vertices, with zero candidate dual load.
4. A line with one coefficient zero, fixing a coordinate ratio outside the nth roots: it contains no grid point and at most one vertex, with zero dual load.
5. A line with three nonzero coefficients: it contains no coordinate vertex and at most two points of the full roots-of-unity grid, by the exact circle equation derived independently. Passing to the subfamily cannot increase its grid count.

This is a classification of all projective lines, not a finite experiment or a list of selected auxiliary lines.

For an explicitly algebraic version of the at-most-two-grid-point step, a line ax+by+cz=0 with abc nonzero gives au+bv+c=0 at (u:v:1), where u and v are roots of unity. As their conjugates equal their inverses, eliminating v and its conjugate gives the polynomial equation

    a conjugate(c) u^2 + (|a|^2+|c|^2-|b|^2)u + conjugate(a)c = 0.

Its leading coefficient is nonzero. There are at most two u values, and each uniquely determines v. Thus the classification can be checked purely by this exact degree-two equation; a picture or numerical root computation is unnecessary.

## q>=2

The candidate primal has cost 4q. Its point dual assigns 1/q to 000 grid points, 1/(2q) to double grid points, and zero to 023 grid points and vertices. Retained component loads are exactly 1; class 2 loads are 1/2; classes 3 and 4 have load zero. A class 5 line has load at most 2/q<=1. Thus the dual is globally feasible for every q>=2 and has total 4q. Weak duality proves tau_all=4q. This reasoning is independent of any assumption that the component maximum equals the all-line maximum.

## q=1: a concrete dual failure and exact replacement

There is one 000 point H=(1:1:1), six double grid points D, six 023 grid points T, and three vertices. The candidate component dual gives H weight 1 and every point of D weight 1/2. For each P in D, the joining line HP has load 3/2. It is neither a retained nor a deleted Fermat component: the double-point triple has residues 221 or 334, none zero, while H has indices 000. A Fermat component joining them would require one equal index. Therefore HP has three nonzero coefficients and exactly the two grid points H,P. These six lines are distinct, since a repeated joining line would contain H and two different double grid points, contradicting the at-most-two-grid-point classification.

An unrestricted primal certificate puts weights

    1/9 on each of the three residue-0 components;
    4/9 on each of the six residue-2/3 components;
    1/9 on each of the six lines HP, P in D.

At H coverage is 3/9+6/9=1. At a double grid point it is 2(4/9)+1/9=1. At a 023 grid point it is 1/9+2(4/9)=1. At a vertex it is likewise 1/9+2(4/9)=1, because each pencil retains one line of each residue. The added lines contain no vertex or other grid point. The total weight is 3/9+24/9+6/9=11/3.

For a matching global dual, assign H weight 2/3, every D point 1/3, every T point 1/6, and every vertex zero. A residue-0 component contains H, two T points, and its vertex, for load 2/3+2/6=1. A residue-2/3 component contains two D points, two T points, and its vertex, for load 2/3+1/3=1. A deleted component has load 1/3. Axes and non-root-ratio lines have load zero. For the remaining lines, there are at most two grid points. If one is H, the other contributes at most 1/3; otherwise their sum is at most 2/3. There is only one H, so the invalid bound 2(2/3) never occurs. This dual is globally feasible and its total is

    2/3 + 6(1/3) + 6(1/6) = 11/3.

Weak duality proves the exact unrestricted optimum 11/3. Its cover also raises the lower bound for curves outside these fifteen support lines from 1/4 to 3/11, though the Seshadri minimum remains attained by the original six five-point lines with ratio 1/5. No assertion that the nonlinear lower bound is attained is made.

## Exact controls and remaining gap

exact_subfamily_check.py reconstructs actual projective coordinates and every arrangement pair intersection over Q(zeta_(5q)) for q=1,2,3. It enumerates every distinct point-pair line, verifies the above all-line classification, checks every primal and dual constraint, and saves full stdout. The all-q theorem is the analytic proof above; these finite exact checks do not establish universality by sampling.

This strengthening resolves the specific component-versus-all-line LP gap for the candidate family. It does not resolve the unrestricted arrangement conjecture or certify novelty. An adversarial reviewer should verify the all-line classification and exceptional q=1 repair before this extension is promoted; the frozen candidate itself does not need an amendment for its component-scoped claim.

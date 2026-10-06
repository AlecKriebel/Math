# Persistence refutes the literal city-ODE collapse conjecture

Problem 9700026 / AMR-096-0026. Authored mathematical correction, 6 October 2026.

## Scope and conclusion

The literal alpha-greater-than-one clause of Conjecture 32(a) in David Aldous's 25 April 2007 technical notes is false for its displayed associated dynamical system. We prove persistence for every positive initial state whenever beta > 2 alpha, including alpha > 1. Thus this is not merely an exceptional symmetric equilibrium.

This does not settle collapse when beta < 2 alpha, convergence or uniqueness of a positive limit, or the stochastic model with new cities. It is not a claimed refutation of the different parameter-restricted 2012 paper. No claim of literature novelty is made.

## Exact system

Let D=[0,1]^2, let n>=2, and fix distinct positions x_i in the interior of D. Let alpha,beta>0 and z be a positive probability vector. Put

S_i(z)={y in D: z_i^alpha |y-x_i|^(-beta) >= z_j^alpha |y-x_j|^(-beta) for all j},

A_i(z)=area(S_i(z)), and z_i'(t)=A_i(z(t))-z_i(t).

These are the fixed-position equations in [1], section 6.4, printed page 40. Null sets at sites and tied boundaries do not affect areas. We use precisely the displayed time variable and right-hand side.

Write q=alpha/beta and p=2q. For positive weights, membership is equivalent, away from the finitely many sites, to

|y-x_i| <= (z_i/z_j)^q |y-x_j| for every j.

Consequently the vector field depends on alpha,beta only through q. For example (alpha,beta)=(2,8) and (1/2,2) give the identical vector field, without a time change.

## Existence and positive simplex invariance

For each positive weight vector, a pairwise tie is a circle or a line: its equation is a nonzero polynomial

|y-x_i|^2 - (z_i/z_j)^(2q)|y-x_j|^2 = 0.

It is nonzero because x_i and x_j are distinct. Such a set has two-dimensional measure zero. Outside the finite union of these sets, the winning site is unchanged by sufficiently small perturbations of the positive weights. Dominated convergence therefore gives continuity of every A_i on the positive orthant. Also sum_i A_i=1 and 0<=A_i<=1.

Peano's theorem supplies a local C^1 solution in that orthant. Along any such solution, writing s=sum_i z_i gives s'=1-s, so s(0)=1 implies s(t)=1. Since z_i'>=-z_i, integrating (e^t z_i)' >=0 gives z_i(t)>=e^(-t)z_i(0)>0 on every finite time interval. Hence the solution cannot meet the boundary in finite time. On any finite interval its values stay in a compact subset of the positive simplex and its derivative is bounded, so it extends to all t>=0. The following estimates hold for every such solution; uniqueness is not needed to invalidate the conjecture.

## Geometric area bound

For each i choose h_i>0 such that the square x_i+[-h_i,h_i]^2 is contained in D and

8 h_i^2 <= |x_i-x_j|^2 for every j!=i.

Such choices exist because the sites are distinct and interior. For z in the positive simplex consider the smaller square

Q_i(z)=x_i+[-h_i z_i^q,h_i z_i^q]^2.

It lies in D since z_i<=1. If y belongs to this square, then

|y-x_i| <= sqrt(2) h_i z_i^q,

|y-x_j| >= |x_i-x_j|-|y-x_i| >= 2 sqrt(2)h_i-sqrt(2)h_i z_i^q >= sqrt(2)h_i.

It follows that |y-x_i| <= z_i^q |y-x_j| <= (z_i/z_j)^q |y-x_j|, using z_j<=1. Thus Q_i(z) is contained in S_i(z), up to irrelevant site conventions, and

A_i(z) >= 4h_i^2 z_i^(2q) = K_i z_i^p, where K_i=4h_i^2>0.

This estimate requires neither symmetry nor stationarity nor a chosen basin of attraction.

## Quantitative persistence in the actual ODE time

Assume beta>2alpha, so 0<p<1. The area bound gives

z_i' >= K_i z_i^p-z_i.

Set u_i=z_i^(1-p), which is differentiable by positivity. Then

u_i' >= (1-p)(K_i-u_i).

The integrating-factor inequality yields, for every t>=0,

z_i(t) >= [K_i+(z_i(0)^(1-p)-K_i) exp(-(1-p)t)]^(1/(1-p)).

The bracket is a positive convex combination of K_i and z_i(0)^(1-p). Therefore

z_i(t) >= min{z_i(0), K_i^(1/(1-p))}>0,

liminf_(t->infinity) z_i(t) >= K_i^(1/(1-p))>0.

For any i, choose j!=i. The simplex identity and the positive bound for z_j prevent z_i from tending to 1. This disproves the alpha>1 collapse clause throughout the nonempty parameter region alpha>1, beta>2alpha.

## Exact rational instance

Take alpha=2, beta=8, n=3, and

x_1=(1/5,1/4), x_2=(3/4,1/3), x_3=(2/5,4/5),

z(0)=(1/6,1/3,1/2), h_1=h_2=h_3=1/16.

The geometric inequalities are strict. Here p=1/2, K_i=1/64 and K_i^(1/(1-p))=1/4096. The displayed initial weights all exceed this threshold. Hence for every t>=0 and every i,

1/4096 <= z_i(t) <= 1-2/4096 = 2047/2048.

In particular no coordinate tends to 1. The certificate and checker establish the rational inequalities exactly. The theorem, rather than finite sampling, proves the entire trajectory assertion.

## General-position qualification

The source gives no formal definition of its general-position phrase. The theorem applies to every configuration of finitely many distinct interior sites and every positive initial vector, not just the rational illustration. Strict separation and interiority persist under perturbations. Thus counterexamples contain an open set of positions, initial conditions, and parameter pairs alpha>1, beta>2alpha; ordinary genericity exclusions cannot eliminate them. The theorem also allows any n>=2, so it is not tied to a special number of sites.

## References

[1] David J. Aldous, technical notes linked from “A Spatial Model of City Growth and Formation,” dated 25 April 2007, section 6.4 and Conjecture 32, printed p.40. https://www.stat.berkeley.edu/~aldous/Research/OP/cities-notes.pdf

[2] David Aldous and Bowen Huang, “A Spatial Model of City Growth and Formation,” arXiv:1209.5120v1 (2012). https://arxiv.org/abs/1209.5120

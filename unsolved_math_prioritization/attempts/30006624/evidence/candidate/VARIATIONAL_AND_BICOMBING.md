# Approaches 2 and 3: descent and metric compatibility

## Approach 2: constructive modularization

Status: proved below by a direct descent argument. This is a reduction lemma, not a solution of the nonuniform local-to-global conjecture.

## Definitions

For a metric space (X,d), let

I_eta(a,b) = {z : d(a,z)+d(z,b) <= d(a,b)+eta}.

Call X almost modular if, for every triple a,b,c and every eta>0, the three sets I_eta(a,b), I_eta(b,c), and I_eta(c,a) have a common point. Call X modular if the same holds for eta=0.

## Lemma

Every complete almost modular metric space is modular. No connectedness, length-space hypothesis, local medianity, or uniqueness assumption is needed.

### Proof

Fix target points a,b,c. Put

P = d(a,b)+d(b,c)+d(c,a),
F(x) = d(a,x)+d(b,x)+d(c,x),
f(x) = F(x)-P/2 >= 0.

The three nonnegative pair defects

e_ab(x)=d(a,x)+d(b,x)-d(a,b),
e_bc(x)=d(b,x)+d(c,x)-d(b,c),
e_ca(x)=d(c,x)+d(a,x)-d(c,a)

sum to 2f(x). Therefore f(x)=0 exactly when x is a median of the target triple.

Given x with f(x)>0, relabel the target points if necessary so that e_ab(x) is largest. Let s=e_ab(x)/2. Then

f(x)/3 <= s <= f(x).

Set eta=s/10, and use almost modularity to choose y in the eta-median set of (a,b,x). Write r=d(x,y). The three approximate-interval inequalities give

s-eta/2 <= r <= s+eta.

Indeed, for the lower bound, add the triangle inequalities d(a,x)<=d(a,y)+r and d(b,x)<=d(b,y)+r, then use d(a,y)+d(b,y)<=d(a,b)+eta. For the upper bound, add d(a,y)+r<=d(a,x)+eta and d(b,y)+r<=d(b,x)+eta, then use d(a,b)<=d(a,y)+d(b,y).

Also, the latter two approximate-interval inequalities and the ordinary triangle inequality for c give

F(y) <= F(x)-r+2eta.

Consequently, writing Delta=f(x)-f(y),

Delta >= r-2eta >= (19/20)s-(1/5)s = (3/4)s >= f(x)/4.

Thus f(y)<=3f(x)/4. Moreover r>=(19/20)s implies 2eta=s/5 <= (4/19)r, so

Delta >= (15/19)r,
r <= (19/15)(f(x)-f(y)).

Iterate this step, stopping immediately if f reaches zero. Otherwise obtain a sequence x_n with

f(x_n) <= (3/4)^n f(x_0)

and, for all N>M,

sum_{n=M}^{N-1} d(x_n,x_{n+1})
 <= (19/15)(f(x_M)-f(x_N))
 <= (19/15)f(x_M).

This proves that x_n is Cauchy. Completeness gives a limit m. Continuity of the distance functions gives f(m)=0. All three nonnegative pair defects therefore vanish, so m belongs to I(a,b) intersect I(b,c) intersect I(c,a). This proves modularity.

The construction also gives d(x_0,m)<=(19/15)f(x_0), for at least one median m of the fixed target triple.

## Consequence for the assigned conjecture

Together with Bowditch's Proposition 9.1, this proves:

A complete connected locally median metric space that is almost modular is median.

Thus, for the complete simply connected locally median path-metric problem, it suffices to prove global approximate median existence. Once that is established, one does not additionally need a uniform quantitative approximate-median uniqueness estimate.

## Exact remaining gap

The premise of almost modularity is global. The descent step asks for an approximate median of (a,b,x), whose two target points a,b may be arbitrarily far from x. The local hypothesis provides no such point directly. Merely substituting short initial pieces of approximate paths from x toward a,b,c gives a local stationarity condition, not the necessary global defect decrease. Therefore this lemma removes the final approximate-to-exact conversion problem but does not remove the nonuniform continuation problem in constructing approximate medians.

## Approach 3: auxiliary CAT(0) metrics and bicombings

### Proposition 3.1: a uniform bilipschitz CAT(0) metric supplies USC

Let d and rho be two metrics on X with constants 0<a<=b<infinity satisfying

a*d <= rho <= b*d.

Assume (X,rho) is CAT(0). For any continuous rectifiable paths alpha,beta:[0,1]->X having the same endpoints, there is an endpoint-fixed homotopy H between them satisfying

Length_d(H_s) <= (b/a)*max{Length_d(alpha),Length_d(beta)}

for every s in [0,1].

Proof. Define H(t,s) to be the point of parameter s on the unique rho-geodesic from alpha(t) to beta(t). CAT(0) convexity gives, for all t,u,

rho(H(t,s),H(u,s)) <= (1-s)*rho(alpha(t),alpha(u)) + s*rho(beta(t),beta(u)).

Summing over arbitrary partitions and taking the supremum bounds each slice's rho-length by the convex combination of the two rho-lengths. The metric inequalities compare path lengths with the same constants a,b, giving the stated bound. Continuity is the usual continuous dependence of CAT(0) geodesics on their endpoints, also immediate from the displayed convexity inequality together with continuity in s. Endpoints remain fixed because the geodesic from a point to itself is constant.

In particular, given epsilon>0, choosing delta=(a/b)*epsilon ensures that any two paths of d-length less than delta with common endpoints are homotopic through paths of d-length less than epsilon. This is USC. Under the target's remaining hypotheses, Bowditch's Proposition 9.4 then proves medianity. No claim is made that the target hypotheses construct rho.

### Why a canonical local construction has not solved the target

Bowditch's finite-rank CAT(0) metrization for established complete connected median spaces is compatible with restriction to closed convex subspaces. That result is a useful input but not a gluing theorem for arbitrary ambient-good neighborhoods.

First, a good metric ball need not be median-closed. In l1^3 the three points (1,1,0), (1,0,1), (0,1,1) have norm 2 and lie in the open radius-5/2 ball, whereas their median (1,1,1) has norm 3. In infinite-dimensional l1, any neighborhood of zero contains points epsilon*e_i for every i and some epsilon>0. Its interval-convex hull contains epsilon*(e_1+...+e_n) for every n: inductively, the next such point lies in the interval between the preceding sum and epsilon*e_(n+1). This hull is unbounded. Thus small bounded ambient-convex neighborhoods cannot be assumed in general.

Second, agreement of median operations on an overlap is not enough for canonical auxiliary metric agreement. The diagonal D={(t,t):t in R} in the l1 plane is closed, complete, connected and closed under medians. Its induced metric is 2|s-t|, a rank-one line metric, whose canonical CAT(0) metric is unchanged. The plane's canonical CAT(0) metric is Euclidean and restricts to sqrt(2)|s-t| on D. These metrics differ. D is not interval-convex in the plane: the interval between (0,0) and (1,1) is the entire unit square. This is exactly the hypothesis missing from the tempting restriction step.

Even if compatible local metrics were supplied, their distortion constants and completion behavior would still need control to produce the global uniformly bilipschitz CAT(0) metric required by Proposition 3.1. A locally varying finite rank is not a global rank bound. An unbounded-rank metric change can change completeness.

A possible finite-rank refinement would try to prove that the local convex hull of a small ball stays within a bounded multiple of that ball, then patch canonical metrics on convex charts. The localization, overlap, and completeness assertions have not been certified in this packet and are not used. The original question has no finite-rank assumption in any event.

### Status

This family establishes a rigorous sufficient auxiliary condition and two exact obstructions to an automatic implementation. The missing construction of a global controlled bicombing or compatible auxiliary metric remains explicit. The variational family has a different missing premise: global approximate medians. Neither premise is inferred from pointwise local medianity.

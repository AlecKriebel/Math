# A certified partial result for directed linear k-cut

Problem 30003993 / OWR-16633-010.

The partial theorem is accepted by the accompanying [mathematical audit](MATHEMATICAL_AUDIT.md). This AI-assisted manuscript and audit are unrefereed; acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. The original question remains open.

## Status

The original uniform-constant-versus-unbounded question is **not resolved** by the theorem below. We prove a family of finite simple directed graphs with unit edge costs whose original path-distance LP integrality gaps have lower limit at least 3. This strengthens the source-reported lower bound tending to 2, but is a bounded lower bound. No priority claim is made. All mathematical arguments below are self-contained.

## The original LP and the theorem

For a directed graph G with distinct terminals s_0,...,s_{k-1}, let OPT(G) be the minimum number of edges whose deletion destroys every s_i-to-s_j directed path with i<j. The distance relaxation minimizes sum_e x_e over x_e>=0, subject to sum_{e in P} x_e>=1 for every such path P.

**Theorem.** For every integer k>=2, put

C_k = sum_{l=1}^k (k-l+1) floor(k/l), and M_k=C_k+1.

There is an explicitly constructible finite simple directed graph G_k, with k ordered terminals and unit edge costs, satisfying

OPT(G_k)=C_k-k^2,
LP(G_k)<=C_k/3.

Consequently, whenever C_k>k^2,

OPT(G_k)/LP(G_k) >= 3(1-k^2/C_k),

and these lower bounds tend to 3 as k tends to infinity. The construction has polynomially many vertices and edges in k. In particular, any universal integrality-gap bound, if one exists, must be at least 3.

The displayed LP bound need not be the exact LP optimum. No equality claim for that optimum is used.

## 1. An auxiliary interval-vertex construction

Let T={0,...,k-1}. For every nonempty integer interval I=[a,b] contained in T, introduce a deletable vertex v_I of integer weight

c_I=floor(k/(b-a+1)).

Introduce undeletable ordered terminals s_0,...,s_{k-1}. Put in the following directed arcs:

- v_I -> v_J, for distinct intervals I,J, whenever b(I)>=a(J);
- s_i -> v_I whenever i>=b(I);
- v_I -> s_j whenever a(I)>=j.

Only interval vertices may be deleted in this auxiliary model. Its use is temporary: Section 4 gives a finite unit-edge-cost graph, with no undeletable edges or weighted objective.

A path starting at s_i and ending at s_j, with no internal terminal, has the form s_i,v_{I_1},...,v_{I_m},s_j. If m=1, the inequalities i>=b(I_1)>=a(I_1)>=j imply i>=j. If m=2, the arc between the interval vertices implies i>=b(I_1)>=a(I_2)>=j. Thus a forward path (i<j) with no internal terminal uses at least three interval vertices.

A forward path with internal terminals also contains a forward subpath between consecutive terminal visits: a sequence of terminal indices with larger last index than first index has an increasing consecutive pair. That subpath uses at least three interval vertices. Therefore assigning length 1/3 to each interval vertex is feasible for the node-distance relaxation. This is a direct path-length argument, not an appeal to an approximation theorem.

## 2. Exact characterization of feasible retained interval families

For a retained interval family F, form its undirected intersection graph: I and J are adjacent exactly when I intersect J is nonempty. Two distinct interval vertices have arcs in both directions exactly in this case, since b(I)>=a(J) and b(J)>=a(I).

Every connected component of this intersection graph is strongly connected in the directed interval graph. Different intersection components have disjoint interval unions, hence have an unambiguous left-to-right order. An arc between different components can only go from the component on the right to the component on the left. Thus the strongly connected components are exactly the intersection components.

For an intersection component A, define

alpha(A)=max_{I in A} a(I), beta(A)=min_{I in A} b(I).

**Claim.** F is a feasible retained family if and only if alpha(A)<=beta(A) for every intersection component A; equivalently, every component has a common point.

Necessity: If beta(A)<alpha(A), choose I,J in A with b(I)=beta(A) and a(J)=alpha(A). There is a directed interval path from v_I to v_J within A. Together with s_beta -> v_I and v_J -> s_alpha this is a forbidden forward terminal path.

Sufficiency: A terminal-free subpath entering component A from s_i requires i>=b(I)>=alpha(A) for its first interval I. If it exits the same component to s_j, then j<=a(J)<=alpha(A), so j<=i. If it moves to another component, that component is strictly to the left, and its entire interval union lies to the left of A; it still cannot exit at a terminal index larger than i. Hence no terminal-free forward subpath exists. Decomposing any path at internal terminal visits proves that no forward terminal path exists at all.

This characterizes every possible interval-vertex deletion set, not a restricted class of label-based solutions.

## 3. Exact auxiliary integer optimum

The total interval weight is C_k, because there are k-l+1 intervals of length l.

Let A be one feasible retained component, let [L,R] be the union of its intervals, and let n=R-L+1. Its common intersection contains an integer p. For each length l, at most l integer intervals of that length contain p. Every interval in A is contained in [L,R], so l<=n. Therefore

sum_{I in A} c_I <= sum_{l=1}^n l floor(k/l) <= k n.

Different components have disjoint interval unions. Their n values sum to at most k. Hence every feasible retained family has weight at most k^2.

This bound is attained by retaining all k singleton intervals [i,i]. They are pairwise disjoint components, each of weight k. The minimum deleted weight is therefore exactly C_k-k^2.

For convergence, use floor(k/l)>=k/l-1 to obtain

C_k >= k((k+1)H_k-k)-k(k+1)/2,

where H_k=sum_{l=1}^k 1/l. In particular C_k/k^2 tends to infinity, so k^2/C_k tends to zero.

## 4. Exact conversion to the original unit-edge-cost model

First split every interval vertex v_I into I^- and I^+, with a directed central edge I^- -> I^+ of integer cost c_I. Replace each auxiliary arc into v_I by an arc into I^-, and each arc out of v_I by an arc out of I^+. Give every noncentral arc integer cost M_k=C_k+1. Terminals are left unchanged. These are ordinary finite costs, not infinity.

Now replace every edge e=(u,v) of integer cost w_e by w_e internally vertex-disjoint directed paths u -> z_{e,r} -> v, for r=1,...,w_e. Every edge in the resulting graph has cost one. All auxiliary z vertices are private to their paths. The resulting directed graph is simple, even though the description uses parallel route bundles.

**Integral lower bound for all cuts.** There is a feasible cut of size C_k-k^2 obtained by breaking every route of every nonsingleton central bundle. Thus a minimum cut has size at most C_k, strictly less than M_k. Such a cut cannot break all M_k routes of any noncentral bundle. All original noncentral connections therefore remain traversable. If the c_I routes of a central bundle are not all broken, that central connection also remains traversable. The fully broken central bundles consequently define a feasible interval-vertex deletion set. Breaking the bundle for I costs at least c_I distinct deleted edges. Section 3 now gives a lower bound C_k-k^2 on every minimum edge cut. Together with the exhibited upper bound this proves exact equality.

This argument allows cuts anywhere, including both legs of any bundle. It never assumes that a cut respects the gadget structure in advance.

**Feasible original edge-distance LP vector.** Put length 1/3 on the first edge of each path in each central bundle, and length zero on every other edge. Its cost is C_k/3. Any forward terminal path projects to a directed walk in the split auxiliary graph, hence to a forward terminal walk in the interval construction. Between some consecutive terminal visits its index increases, and the argument in Section 1 proves that this segment traverses at least three interval vertices. Each traversal uses a central route and contributes 1/3. Thus every forbidden path has length at least one.

No weighted-to-unweighted approximation assumption is needed: both the exact integral equality and the fractional feasibility have been proved directly for G_k.

## 5. Size and explicit generation

There are k(k+1)/2 intervals, hence O(k^2) central edges and O(k^4) noncentral edges before route replacement. C_k<=k^2 H_k=O(k^2 log k), and each noncentral bundle has C_k+1 routes. The resulting graph therefore has O(k^6 log k) vertices and edges. Its terminals remain distinct and retain their original order.

The accompanying audit records historical supplementary exact checks and explicit graph generation. The proof is valid for every integer k independently of those finite checks, and requires no omitted program, generated certificate or raw output. This proof-only edition excludes those computational artifacts.

## 6. What remains open

The lower bound tends to the finite constant 3. It neither proves an absolute upper bound nor produces a family with gaps tending to infinity. The original question therefore remains unresolved.

## Source credit

The precise source target is Chandra Chekuri's contribution, “Open Problem: Approximation and Integrality Gap for Linear k-Cut,” Oberwolfach Report 50/2018, printed p. 3013. The later paper by Kristof Berczi, Karthekeyan Chandrasekaran, Tamas Kiraly, and Vivek Madan, “A tight sqrt(2)-approximation for linear 3-cut,” Mathematical Programming 184 (2020), 411–443, provides context and the previously reported general-k bounds. The interval construction and proofs in this note were independently developed; novelty has not been established. No copied source document is included in this packet.

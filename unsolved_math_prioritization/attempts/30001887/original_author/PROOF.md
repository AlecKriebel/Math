# Multiple-cover thresholds: five approaches and exact barriers

Problem identifier: 30001887 / OWR-11136-013. Date: 2026-10-05.

## Verdict and formulation

**Unsolved in this investigation.** No complete proof, counterexample, or prior resolution of the unrestricted question was established. The results below are elementary conditional results, special cases, and negative controls; no novelty claim is made.

The primary OWR report, printed pp. 2512–2514, defines m_k(P) using all coverings of the **whole plane by translates of one fixed planar set P**. It asks whether m_2(P)<infinity implies m_3(P)<infinity, and whether the thresholds of a cover-decomposable P grow linearly in k. The constant in O(k) may depend on P. The definition does not impose convexity, boundedness, openness, or local finiteness. We use indexed families, so different indices may represent equal translates. The distinctions below remain essential even if repeated copies are prohibited.

Write C=(P+t_i)_{i in I}. Its incidence edge at x is E_x={i:x in P+t_i}. A decomposition into k covers is exactly a coloring c:I->{1,...,k} for which every E_x contains every color. Point-finite means each E_x is finite. Locally finite means every compact planar set meets finitely many members; local finiteness implies point-finiteness, but these terms are not interchangeable in general.

The website's exact extracted problem record could not be inspected: the named public page returned HTTP 403 and the web reader could not access it. The assignment's descriptor and the primary report match the subject, but exact website-to-source equivalence is not certified. The raw AI corpus record was unavailable. This dossier investigates the recovered primary-source question, without inventing missing record wording.

## Approach 1. Balanced binary splitting

### Retained theorem 1

Let H=(V,E) be a hypergraph with finite edges. Suppose that for every W subset V there is a partition W=W_0 disjoint-union W_1 satisfying

| |e intersection W_0| - |e intersection W_1| | <= D

for every e in E, where D is a fixed nonnegative integer. Let k>=2 and q=2^ceil(log_2 k). If every edge has size at least

M=q+(q-1)D,

then H has a polychromatic k-coloring.

**Proof.** Apply the assumed partition recursively to every current vertex class, through r=log_2 q levels. After j levels, each edge meets each current class in at least

|e|/2^j-D(1-2^(-j))

vertices. For j=0 this is equality. If a parent class meets e in a vertices, each child meets it in at least (a-D)/2; substitution proves the next step. At j=r the displayed bound is at least 1 by the hypothesis on |e|. Thus the q terminal classes all meet every edge. Merge terminal classes by any surjection from q labels to k labels. Each resulting class still meets every edge. This proves the theorem. In particular M<2k(D+1), so a uniform hereditary discrepancy bound is sufficient for a linear threshold. QED.

For a point-finite whole-plane covering, apply this to its incidence hypergraph. If this hypothesis holds uniformly with D=D(P) for all such coverings, the result is a linear upper bound for the **point-finite** version of the problem. This statement does not cover incidence edges of infinite size.

### Why ordinary two-cover splitting is insufficient

Take n indexed copies of P=R^2. One red copy and n-1 blue copies form a valid two-cover decomposition. Its red depth is exactly one, however large n is. Thus the mere output specification “both colors cover” provides no increasing lower bound on the depth in either color. This is a counterexample to the proposed recursive inference, not to the desired existence theorem: these same n copies can plainly be split evenly.

**Exact obstacle.** No hereditary discrepancy bound, balanced splitting rule, or preservation of infinite depth has been deduced from m_2(P)<infinity. The theorem above assumes the missing quantitative property rather than proving it.

## Approach 2. Remove shallow subcovers

### Retained theorem 2

Let X be a target set and C an indexed family of subsets. Suppose every subfamily covering X has a subcover H whose depth at every x in X is at most s, for a fixed positive integer s. If C covers X at least 1+s(k-1) times, then it partitions into k covers of X.

**Proof.** Choose such a subcover H_1 and remove it. The remaining depth is at least 1+s(k-2). Repeat. Before the j-th removal, for 1<=j<=k-1, every depth is at least 1+s(k-j), so the current family is still a cover and the assumption applies. After k-1 removals the remainder has depth at least one. Use H_1,...,H_{k-1} as the first k-1 color classes and the entire remainder as the final class. Each is a cover and the classes partition C. Infinite point degrees cause no difficulty here: removing at most s members at a point preserves their infinitude. QED.

### Retained finite-interval case

Every finite cover of X subset R by bounded closed intervals has a subcover of depth at most two, even when X is infinite.

**Proof.** Choose an inclusion-minimal subcover H; it exists because the starting family is finite. Suppose three members share a point p. Among these three, choose A with smallest left endpoint and B with largest right endpoint. If A=B, that interval contains the other two, contradicting minimality. Otherwise their common point p makes A union B an interval spanning both extreme endpoints. The third interval is contained in A union B, so removing it preserves coverage of X, again a contradiction. Thus no point belongs to three members of H. QED.

Consequently, every finite (2k-1)-fold interval covering of any X splits into k covers. This also applies to parallel strips above such one-dimensional finite families. It is a genuine special case, not an unrestricted planar conclusion.

### Ordered-translate improvement, with its hypothesis retained

For P=[0,1] x R, every **point-finite** k-fold whole-plane covering by translates decomposes into k covers. To see this, project the translates to their left endpoints a_i. Every compact interval of endpoints is contained in finitely many intervals of the form [x-1,x], and each such interval contains only finitely many endpoints by point-finiteness. Hence the endpoint multiset is locally finite. Whole-line coverage forces the endpoints to be unbounded in both directions. They can therefore be ordered, including repeated endpoints, as a doubly infinite sequence indexed by Z. Give the i-th endpoint color i modulo k. At any x, the indices of intervals covering x form a finite consecutive block. If its size is at least k, it contains all residue classes. Thus each color covers the whole plane.

This restricted threshold is exactly k: k-1 copies of the integer-translate strip covering have depth k-1 at every noninteger x and cannot be split into k covers. If distinct translates are required, replace repeated lattice copies by k-1 different small shifts of the lattice; a point off all their boundaries still has depth k-1.

**Exact obstacle.** A uniform shallow-subcover bound has not been proved for arbitrary P with finite m_2(P). Minimality alone gives it for intervals because of their order, not for general planar sets. The ordered-strip proof explicitly requires point-finiteness; it is not a silent reduction of the original unrestricted covering class.

## Approach 3. Random colors and the number of incidence constraints

### Retained theorem 3

Let a finite hypergraph have at most N edges, all of size at least M. If

N k ((k-1)/k)^M < 1,

then it admits a polychromatic k-coloring.

**Proof.** Color each vertex independently and uniformly from k colors. For a fixed edge e and fixed color a, the probability that a is missing from e is ((k-1)/k)^|e|, at most ((k-1)/k)^M. There are at most Nk such bad events. The union bound shows that the probability of at least one bad event is below one. A coloring with no bad event exists. QED.

For example M>k log(Nk) is sufficient, since 1-1/k<=exp(-1/k). The result also handles finitely many possibly infinite incidence edges: first choose M vertices from each edge, and color the finite union of those witnesses by the finite theorem. Extending the coloring arbitrarily preserves the witnesses.

A finite geometric family may have many points but only finitely many different incidence signatures. The theorem applies with N equal to the number of signatures being constrained. It need not constrain shallow signatures when the task is to cover only a prescribed heavy region.

### Why the parameter cannot simply be erased

For each s>=2, the complete s-uniform hypergraph on 2s-1 vertices is not 2-colorable: one color class in any two-coloring has at least s vertices and contains an edge. It has binomial(2s-1,s) incidence constraints. Thus large edge size alone gives no uniform coloring theorem for arbitrary hypergraphs. A local-dependency improvement would likewise require a uniform dependency bound; none follows from the original hypothesis in this investigation.

**Exact obstacle.** N is not bounded in terms of P and m_2(P) by this argument, and the term log N cannot be discarded. These finite-instance bounds therefore do not give the required shape-dependent threshold valid for all covers.

## Approach 4. Extremal obstructions and exact planar realization

### Retained theorem 4A: the nonhereditary hub obstruction

For each s>=2, take V_0 of size 2s-1, all s-subsets of V_0, and a new vertex h. Let H_s have edges {h} union A over all s-subsets A of V_0. Then H_s is (s+1)-uniform and 2-colorable, but has no polychromatic 3-coloring.

**Proof.** Color h red and V_0 blue for the two-coloring. Suppose there is a polychromatic three-coloring and call the color of h color 1. Every s-subset A must contain both colors 2 and 3. Recolor any color-1 vertices in V_0 with color 2; every s-subset still contains colors 2 and 3. This is a proper two-coloring of the complete s-uniform hypergraph on 2s-1 vertices, which is impossible by the pigeonhole argument above. QED.

Deleting h produces precisely that non-2-colorable trace. The family of these examples is therefore not evidence for the hereditary conjecture or the fixed-P whole-plane question.

### Retained theorem 4B: arbitrary finite incidence patterns in shapes with m_k=1

Every finite hypergraph H with n>=1 vertices and q>=1 edges can be represented as incidences of q planar witness points with n translates of an **open** planar set P for which m_k(P)=1 for every finite k.

**Construction.** Number vertices i=0,...,n-1 and edges e=0,...,q-1. Set Q=n+1, t_i=(i,0), and x_e=(Q(e+1),0). For each incidence i in e, place an open disk of radius 1/4 centered at x_e-t_i. Let D be the union of these finitely many disks. Put R=Q(q+1)+n and define

P=D union {(u,v):u>R}.

**Incidence proof.** The numbers Q(e+1)-i for all pairs (e,i) are distinct integers. Indeed equality for two pairs would give Q(e-f)=i-j, whose right side has absolute value less than Q. Thus e=f and i=j. Their mutual distance is at least one. Consequently x_e-t_i lies in D exactly when i is incident with e. Every x_e-t_i is at most Qq and hence strictly less than R, so the added half-plane introduces no witness incidences. Therefore x_e belongs to P+t_i exactly when i belongs to e.

**Whole-plane proof.** All disk centers have first coordinate at least Q-(n-1)=2. Hence P is contained in {u>0} and contains {u>R}. For any indexed family (P+t_i) covering the whole plane, the first coordinates a_i of the translation vectors must be unbounded below. Otherwise their common lower bound would leave a left half-plane uncovered. Choose distinct members with a_{i_j} strictly decreasing to minus infinity. Split this sequence cyclically into k subsequences. Each subsequence has first coordinates tending to minus infinity; its translated right half-planes alone cover every point of R^2. Assign all remaining members arbitrarily to one color. This partitions the original covering into k covers. Every 1-fold covering therefore decomposes, and the minimum positive threshold is m_k(P)=1. QED.

The far-half-plane device already appears in the 2013 preprint of Pach, Pálvölgyi, and Tóth, Section 2.3 (see SOURCES.md). The explicit finite-incidence construction here is supplied as a proved control, not as a novelty claim.

This is a particularly strong negative control: even an arbitrarily deep, finite, non-2-colorable witness configuration can occur for a shape whose every whole-plane cover splits into arbitrarily many covers. The finite configuration does not cover the whole plane. Extending it to a whole-plane cover can destroy the obstruction.

The constructed P is unbounded and, when D is nonempty, disconnected and nonconvex. It is not an example for a bounded or convex subclass. It has no point-finite whole-plane covering, because the decreasing sequence supplies infinitely many covering half-planes at every point. This is consistent with the original source's unrestricted definition.

**Exact obstacle.** A genuine negative solution needs one fixed P with a proof of finite whole-plane m_2(P), and, for every proposed threshold M, an M-fold whole-plane cover by its translates that has no three-cover decomposition. Neither finite hub examples nor the coding construction meet those quantifiers. The construction proves why an unchecked finite-to-global transfer would be false.

## Approach 5. Finite types and compactness

### Retained theorem 5A: finitely many allowed sets

This elementary bound is already stated in the 2013 survey, Section 6; a complete proof is included here.

Let F={S_1,...,S_r} be a finite family on any nonempty target X, and let C be a multiset of its members. If every point has depth at least r(k-1)+1, then C decomposes into k covers.

**Proof.** For each type S_j occurring at least k times, put one of its copies into each color class, and assign any additional copies arbitrarily. Types occurring fewer than k times can also be assigned arbitrarily. If a point x were contained only in types occurring fewer than k times, its total depth would be at most r(k-1), contrary to assumption. Thus some type containing x contributes all colors at x. QED.

The proof remains valid with infinitely many copies of a type: select k of them and distribute the others. If at most t different types contain any one point, replace r by t.

### Retained theorem 5B: the legitimate point-finite compactness step

Fix P, M, and k. Suppose every finite family of translates of P can be colored with k colors so that every point covered by at least M members sees all colors. Then every point-finite M-fold whole-plane covering by translates of P decomposes into k covers.

**Proof.** For a covering indexed by I, consider the product space {1,...,k}^I with discrete finite factors; it is compact. For each x, require that all k colors occur on E_x. Since E_x is finite, this condition defines a closed cylinder subset C_x. For finitely many points x_1,...,x_l, the union J of their incidence edges is finite. By the assumed finite-family coloring theorem, the translates with indices J can be colored so that every x_j sees all colors, since its full incidence edge is contained in J and has size at least M. Extend this coloring arbitrarily to I. Thus the C_x have the finite intersection property. Compactness supplies a coloring in their total intersection. QED.

This argument does not require that the finite subfamily cover the whole plane. That is exactly why its premise is stronger than a statement only about whole-plane coverings. In particular, if P is bounded, no finite family of its translates covers the plane at all; the original premise does not give a nonvacuous finite-family coloring theorem directly.

### The infinite-edge closure warning

For vertices N, let the incidence edges be all infinite tails. Color the first n vertices red and then alternate red and blue forever. Each such coloring is polychromatic on every tail. The sequence of colorings converges coordinatewise to the all-red coloring, which is not polychromatic on any tail. Hence the set of colorings satisfying an infinite-edge polychromatic condition need not be closed. The closed-cylinder proof above cannot be used unchanged without point-finiteness. This observation is an obstruction to that proof, not a counterexample to colorability of the tail family.

**Exact obstacle.** The finite-type threshold grows with r or t, and neither is bounded for all translate covers. Compactness does not create a uniform threshold and does not turn whole-plane m_2(P) into a finite-family hereditary hypothesis. A separate geometric reduction or infinite-cover argument is missing.

## What would finish the original problem

A positive proof must derive a uniform k-cover threshold from whole-plane m_2(P) for every fixed allowed P, including non-point-finite families, without substituting total-cover decomposability. A negative proof must construct the single fixed shape and all-threshold whole-plane witnesses described in Approach 4. None of the five approaches supplies this final step. The checked calculations below validate finite controls and arithmetic only; the written arguments carry the universal statements actually retained.

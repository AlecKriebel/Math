# Proof 02  Structure of mass two affine circuits

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Statement

For a finite set S of distinct integer vectors, augment each point x to the column (1,x). Assume every primitive integer affine circuit has positive coefficient mass two. Equivalently each circuit is either an arithmetic progression with coefficients (1,-2,1), or a parallelogram with coefficients (1,1,-1,-1).

**Classification.** The affine matroid decomposes as a direct sum of components, each of which is one of the following, up to rational affine equivalence on its affine span:

1. A singleton.
2. A centered cross-polytope together with its center: {c, c+u_i, c-u_i : 1<=i<=n}, where u_1,...,u_n are linearly independent and n>=1.
3. A center-free cross-polytope {c+u_i,c-u_i : 1<=i<=n}, with independent u_i and n>=2.
4. A two-layer simplex {a_i,a_i+v : 1<=i<=n}, where v, a_2-a_1,...,a_n-a_1 are linearly independent and n>=2.

Types 3 and 4 agree for n=2 (a parallelogram); the list is not intended to be disjoint. Different components have direct-sum augmented linear spans; equivalently S is their affine join. Conversely, all such joins satisfy the circuit condition. Rational affine equivalence, rather than a unimodular lattice equivalence, is intended; centers in type 3 can be half-integral.

## 1. Planar lemma

**Lemma.** An admissible configuration of affine dimension at most two has at most five points. If it has five, it is {c,c+u,c-u,c+v,c-v}, with u,v independent. In particular every arithmetic-progression triple in a five-point admissible planar set has the same midpoint.

A line contains at most three points: for four ordered collinear points x_1<x_2<x_3<x_4, both triples (x_1,x_2,x_3) and (x_1,x_2,x_4) would have to be arithmetic progressions, forcing x_3=x_4.

First suppose a planar set contains an AP triple. Normalize four of its points to O=0, U=u, R=-u, V=v, with u,v independent. Any additional point W has a fundamental affine circuit over the basis {O,U,V}. Its permitted barycentric forms are the three midpoints, six extrapolations, and three parallelogram completions:

U/2, V/2, (U+V)/2, -U, -V, 2U, 2U-V, 2V, 2V-U, U-V, V-U, U+V.

The point -U is already present. Of the eleven other candidates, only -V is admissible. Here is an exact certificate for every excluded candidate. The listed vector is the primitive affine relation on the ordered columns (O,U,V,R,W); its nonzero support is a circuit, directly checked using independence of U,V. K is its positive mass.

| W | Relation on (O,U,V,R,W) | K |
| --- | --- | --- |
| U/2 | (0,3,0,1,-4) | 4 |
| V/2 | (0,1,2,1,-4) | 4 |
| (U+V)/2 | (-2,0,-1,1,2) | 3 |
| 2U | (-3,0,0,2,1) | 3 |
| 2U-V | (-4,0,1,2,1) | 4 |
| 2V | (0,1,-4,1,2) | 4 |
| 2V-U | (-2,0,2,1,-1) | 3 |
| U-V | (0,3,-2,1,-2) | 4 |
| V-U | (0,-1,2,1,-2) | 3 |
| U+V | (0,-1,-2,1,2) | 3 |

Thus an AP-containing planar set is contained in {0,±u,±v}.

If a planar admissible set contains no AP triple, choose an affine basis {0,u,v}. Every other point must be one of u+v, u-v, v-u. Any two such points force an AP triple: u+v and u-v have midpoint u; u+v and v-u have midpoint v; u-v and v-u have midpoint 0. Hence there is at most one extra point, and the set has at most four points. This proves the lemma.

## 2. Components containing an AP circuit

Let T be an AP triple with midpoint c.

Two distinct AP triples that meet can share only one point, since sharing two puts their four-point union on one line. If their union is not collinear, it is a five-point planar admissible configuration, so the planar lemma says their shared point is the midpoint of both.

Let Q be a parallelogram circuit meeting T.

- They cannot meet in three points, since a circuit contains no dependent proper subset.
- If they meet in two points, their five-point union lies in the plane of Q. By the planar lemma it is a centered cross with center c. Consequently Q comprises its four outer points: the common points are the endpoints of T, and the other diagonal of Q is another AP through c.
- They cannot meet in exactly one point. Their union has six points and augmented rank at most 2+3-1=4. Rank at most three would place six points in a plane, which the planar lemma excludes. In rank four, the affine relation space has dimension two and is spanned by the relations of T and Q. Eliminate the coefficient of the unique common point. All other five coefficients are nonzero. This five-support relation is a circuit: any relation supported there must lie in the one-dimensional subspace of the two-dimensional relation space that vanishes at the common point, and hence has that same full support. But admissible circuits have support at most four. Contradiction.

Now start with T and expand through all circuits connected to it. Every newly encountered AP triple has midpoint c. Every newly encountered parallelogram avoids c and comprises two endpoint pairs about c: indeed if it contains any existing endpoint x, its intersection with the existing triple {c,x,2c-x} must consist of the two endpoints, by the preceding local analysis. Its other two points form another pair about c. Thus the entire component has the form {c,c±u_1,...,c±u_n}.

The directions u_i are linearly independent. If not, choose a minimally linearly dependent subset. No two directions are proportional, by the three-point limit on lines. Reverse signs of selected u_i so the primitive dependence has all coefficients positive: sum_i a_i v_i=0, with a_i positive integers and at least three terms. Then

sum_i a_i(c+v_i) - (sum_i a_i)c=0

is an affine circuit: a proper subset of the v_i is linearly independent, and the sole relation among all of them has nonzero coefficient sum, so the endpoints alone are affinely independent. Its primitive positive mass is sum_i a_i>=3, a contradiction. This proves type 2.

## 3. The AP-free case is binary

Let A be a rational full-row-rank representation by augmented columns of an AP-free admissible configuration; choose independent rows if necessary. All primitive circuits now have coefficients in {0,±1} and support four.

Fix a column basis B. Every fundamental circuit expresses a nonbasis column in B-coordinates with entries 0,±1. For two bases related by a single exchange, the determinant ratio is one of the nonzero fundamental-circuit coordinates, hence has absolute value one. The basis-exchange graph is connected (extend their common independent subset and exchange an element outside it), so every nonzero maximal minor of A has the same absolute value as det B.

Normalize D=B^{-1}A, with its basis columns the identity. Every maximal minor of D is 0 or ±1. Every nonzero square minor of D extends to a maximal minor by adjoining the identity columns for rows outside that minor. There is no repeated column in this extension: if an identity column for an outside row had already occurred, the original minor would have had a zero column. Hence every square minor is 0 or ±1, so D is totally unimodular.

Reduction modulo two has exactly the same independent column subsets. A real-independent subset extends to a real basis, whose determinant is ±1 and stays nonzero modulo two. Conversely, a real-dependent column subset has all appropriate minors zero, hence remains dependent modulo two. Thus the matroid is binary.

We use the elementary binary-cycle fact: the symmetric difference of two circuits is a disjoint union of circuits. For completeness, their incidence vectors add to a kernel vector over F_2. Its nonempty support contains a circuit; remove that circuit by adding its incidence vector and iterate. Because every circuit here has size four, two distinct circuits cannot intersect in one point (their symmetric difference would have size six, which is not a positive multiple of four), or in three points (difference size two). If they intersect, they therefore meet in exactly two points, and their symmetric difference is itself a four-circuit.

## 4. Pair blocks and exclusion of the seven-element exception

A pair block is a set partitioned into disjoint two-element pairs P_1,...,P_n such that every P_i union P_j is a circuit.

Any two intersecting circuits initialize a three-pair block: take their intersection and their two differences. A component with only one circuit is already a two-pair block.

We first exclude the following pattern: three pairs P_i={a_i,b_i}, all three pair-unions circuits, and a further circuit C={a_1,a_2,a_3,x}, where x is outside those six points.

On the six pair elements, the only possible circuits are the three pair-unions. To see this, any other four-circuit has intersection of even size with each pair-union. If its pair-intersection sizes are m_1,m_2,m_3, then m_i+m_j is even for each i,j, so all m_i have the same parity. All odd would sum to three, not four; all even gives a pair-union. Consequently these six columns have rank four: {a_1,b_1,a_2,a_3} is independent and spans them.

Their signed real circuit equations can be reoriented, by independently multiplying columns by -1, to have

a_1+b_1=a_2+b_2=a_3+b_3=w.

Here is the justification for compatibility of the signs. The relations on P_1 union P_2 and P_1 union P_3 span the two-dimensional relation space on the six columns. A relation on P_2 union P_3 must cancel both coefficients on P_1, so those two coefficient pairs are proportional. Since all nonzero coefficients are ±1, rescale one whole relation by -1 if needed and reorient each pair's columns to obtain the displayed equations. The vectors w,a_1,a_2,a_3 are independent, because they span the six-column rank-four space.

The C relation, after reorientation, reads

x=epsilon_1 a_1+epsilon_2 a_2+epsilon_3 a_3, each epsilon_i in {±1}.

For every i!=j, binary symmetric difference of C with P_i union P_j is the circuit consisting of x,b_i,b_j,a_k, where {i,j,k}={1,2,3}. Thus it also expresses x as a signed ±1 combination of b_i,b_j,a_k. Substitute b_l=w-a_l and compare coefficients in the independent basis {w,a_1,a_2,a_3}. The w coefficient vanishes only if epsilon_i+epsilon_j=0. This is required for all three pairs i,j, which is impossible for three nonzero signs. The pattern is excluded. This is a direct exclusion of the Fano-dual tetrad pattern, without using any excluded-minor theorem.

Now let a pair block of size n>=3 be given, and let C be any circuit that meets it. If C equals an existing pair-union, there is nothing to prove. Otherwise write m_i=|C intersection P_i|. Each m_i+m_j is even, so the m_i all have the same parity.

If all are odd, n<=4. Choose any three pairs. C selects one element from each; its fourth element is outside those chosen six, giving exactly the excluded seven-element pattern.

If all are even, C either consists of two existing pairs, is disjoint from the block, or consists of one existing pair and a new pair Q. In the last case symmetric difference with each old pair-union shows Q union P_i is a circuit for every i, so the block extends by Q.

Because a matroid component is connected by chains of intersecting circuits, repeatedly extending the pair block exhausts the component. There are no additional circuits inside an exhausted block: the same parity argument says every circuit is a pair-union, with its all-odd alternative already excluded. Hence a block of n pairs has rank n+1, since one full pair and one element of each remaining pair form a basis.

## 5. Affine orientation of an AP-free pair block

Write the augmented columns in its pairs as A_i,B_i. For n>=3, the compatibility argument on each three-pair restriction in section 4 shows that the pair relations can be chosen as

s_i A_i+t_i B_i=W for every i, with s_i,t_i in {±1},

for one common nonzero vector W. More explicitly, fix pair 1; the relation on pair 1 with pair i has a coefficient pair on pair 1. Any two such coefficient pairs are proportional because the three-pair relation space contains the circuit on their other two pairs. They are proportional by a sign, so choose that sign consistently and obtain W. For n=2, its sole circuit directly gives such equations.

Let h be the original first-coordinate functional, so h(A_i)=h(B_i)=1. Then h(W)=s_i+t_i belongs to {-2,0,2}, independently of i.

- If h(W) is nonzero, reverse the sign of W and all equations if needed so h(W)=2. Necessarily s_i=t_i=1 for every i. Thus A_i+B_i=W, and the actual points are c±u_i, with c=W/2 in the affine hyperplane h=1. The augmented block rank is n+1; its augmented span is generated by W and its n direction vectors (0,u_i), so the u_i are linearly independent. This is type 3.
- If h(W)=0, each pair has opposite signs. Swap its two labels if necessary so A_i-B_i=W for every i. In affine coordinates all pairs have a common difference v. The augmented span is generated by one point A_1, the n-1 differences A_i-A_1, and W. Its rank n+1 forces those n affine directions to be independent. This is type 4.

Thus mixed sum-type and difference-type pairs are impossible: their common W would have incompatible first coordinates.

## 6. Components and the converse

For any represented matroid, the spans of distinct components form a direct sum. To prove this without a connectivity theorem, decompose any dependence as a sum of circuit dependences: its support contains a minimally dependent subset; subtract a multiple of that circuit dependence to cancel one nonzero coordinate, adding no new support, and repeat. Every circuit lies in a single component. Therefore the full relation space is the direct sum of the component relation spaces. Rank-nullity gives rank(A)=sum_C rank(A_C), which is exactly the direct-sum assertion for their column spans.

In augmented affine coordinates, this direct-sum condition says precisely that the original configuration is an affine join of its components. Its circuits are exactly the circuits of those components.

For a centered cross with center, independence of the directions gives relation equations lambda_{i,+}=lambda_{i,-}=t_i and lambda_c=-2 sum_i t_i. Minimal supports are exactly one endpoint pair with center (AP), or two endpoint pairs without center (parallelogram). For a center-free cross the equations are lambda_{i,+}=lambda_{i,-}=t_i with sum_i t_i=0, and minimal supports are two pairs with opposite t's. For a two-layer simplex, independence of v and the base differences gives lambda_{i,0}+lambda_{i,1}=0 for each i, together with sum_i lambda_{i,1}=0; again minimal supports are two pairs, each with primitive coefficients ±1. Singletons have no circuits. Hence every listed affine join has exactly the permitted circuits.

## 7. Sharp cardinality consequence

Let r=dim(aff S)+1 be the augmented rank and let k be the number of components. A singleton has size 2r_C-1=1; a centered cross with center has size 2r_C-1; and each AP-free nontrivial block has size 2r_C-2. Therefore

|S| <= 2r-k <= 2r-1.

If S is nonempty and r>=2, equality |S|=2r-1 occurs precisely for a single centered cross-polytope with its center. For r=1 the singleton is the equality case. This is a bound on the number of frequencies, not on the number of distinct integer coordinates in a surrounding box.

For an infinite configuration contained in Z^d, taking an arbitrary finite subset of 2d+2 points contradicts the bound |S|<=2(d+1)-1. Thus every infinite integer-frequency configuration fails the mass-two condition on some finite subset. Combined with the previously proved necessary condition, it fails the fixed-p real strict majorant property for every 2<p<4.

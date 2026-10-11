# Repaired proof of the prior vertex critical edge resilience results

This is an independently written verification of the argument in Ema Skottová and Raphael Steiner, *Critical edge sets in vertex-critical graphs*, arXiv:2508.08703v1. It preserves their construction, statements, and constants while making the local corrections in AUDIT.md explicit. It is not a new solution to the remaining k=4 family.

## 1 Definitions and the exact target

A (k,r)-graph is a finite simple graph G with chi(G)=k, chi(G-v)=k-1 for every vertex v, and chi(G-R)=k whenever R is an edge set of size at most r. It is enough to establish chi(G-v)<=k-1 for every v and chi(G-R)>=k for every such R. Taking R empty gives the lower bound for G; adding a new color to any vertex-deletion coloring gives chi(G)<=k. Also chi(G-v)>=chi(G)-1, so the vertex-deletion equalities follow.

For a graph with a proper k-coloring, the condition on R is equivalent to saying that every assignment of k-1 colors has at least r+1 monochromatic edges. Remove all its monochromatic edges to obtain one direction; a proper coloring after deletion gives the other. This equivalence also explains why the Chan graph with exact three-color defect 2 establishes precisely the single-edge case.

## 2 The circulant construction and parameters

Take integers k>=5, r>=1, m>18r+2, and q>=24r+12 with q divisible by 4. Write

    p = (k-1)m             for odd k,
    p = 2(k-1)m            for even k,
    N = qp+1,
    F = {0,2,...,2m-2}.

The vertices are indexed by Z/N. Adjacency means that their cyclic distance is in D=D1 union D2 union D3, where

    D1 = {1,3,...,2m-1}.

For odd k, D3 is empty and D2 is the union of [2m,(k-3)m+1]+ap over 0<=a<q/2. For even k, D2 is the union of [2m,(k-4)m+2]+ap over that range, and D3 is the union of [(k+2)m-1,(2k-4)m+1]+ap.

All displayed distances are positive and at most floor(N/2). For D2 or D3 their largest possible value is at most qp/2-2m+1; D1 is much shorter. The graph is therefore finite and simple. Cyclic shifts and reversal of the indices preserve it. In particular it is vertex-transitive. The distance 1 edges form a spanning cycle.

The proof below verifies Theorem 4.1, namely that this graph is a (k,r)-graph. It uses no external construction or coloring theorem.

## 3 Vertex deletion colorings and the wraparound check

By cyclic symmetry it suffices to color vertices 1,...,qp. Repeat a p-periodic pattern. For odd k each color c has one start

    t_c=(c-1)m+1 if c is odd,
    t_c=(c-2)m+2 if c is even,

and occurs at the residues t_c+F. For even k the two starts of c are

    {(c-1)m+1,(c+k-3)m+2} if c is odd,
    {(c-2)m+2,(c+k-2)m+1} if c is even.

These rules partition the first p positions. Equivalently, divide them into rows of 2m positions. Row a alternates colors 2a+1 and 2a+2, with color labels reduced modulo k-1 in the even case. There are (k-1)/2 rows for odd k and k-1 rows for even k. This proves that every position has exactly one color without assuming a result of Jensen.

For odd k, the difference of two same-color positions has the form bp+f'-f, with f,f' in F and -(q-1)<=b<=q-1. It is even, so cannot be a D1 distance in the forward direction. Its residue modulo p is outside [2m,p-2m+1], excluding D2. In the reverse direction its cyclic distance has residue 1-f'+f. This also avoids the D2 interval: its representative lies either below 2m or above p-2m+1. If the reverse distance is relevant, it is at least p-2m+3=(k-3)m+3>2m-1, which excludes D1. Thus the coloring is proper.

For even k, same-color differences have residues in

    A = {0,(k-2)m+1,km-1}+F-F  modulo p.

The residues contributed by 0 are even values within distance 2m-2 of 0. The other two sets are odd values in [(k-4)m+3,km-1] and [(k-2)m+1,(k+2)m-3], respectively. A cyclic distance of a same-color pair has residue in A union (1-A). This union is contained in

    [0,2m-1]
    union [(k-4)m+3,(k+2)m-2]
    union [p-2m+2,p-1].

These intervals avoid the D2 and D3 residue intervals. A forward difference in D1 is impossible: the short residues of A are even. A reverse D1 distance is also impossible: writing both positions as a start plus f plus a period multiple gives the lower bound

    N-(j-i) >= p+1-(km-1)-(2m-2) = (k-4)m+4 > 2m.

This checks the extra wraparound offset 1 from N=qp+1, which cannot be ignored in a circulant coloring argument. The displayed B0 expansion in Appendix A needs correction, but the residue computation above gives exactly the required exclusion. Hence every vertex deletion is (k-1)-colorable.

## 4 Local balance and periodicity on an unaffected interval

Suppose, for a contradiction, that G'=G-R has a proper (k-1)-coloring phi with |R|<=r. A vertex is unaffected when none of its incident edges was removed. Consider an interval S of 3p consecutive unaffected vertices. By a cyclic shift label it 1,...,3p. Put H_i={v_i,...,v_(i+p-1)}.

Every H_i contained in S has exactly p/(k-1) vertices of each color. Here are the full balance arguments.

For odd k, the corrected sets

    V_j={v_(i+2ma+epsilon+2(j-1)):
         0<=a<=(k-3)/2, epsilon in {0,1}},  1<=j<=m,

partition H_i. Their pairwise distances are 1, 2m-1, or an element of [2m,(k-3)m+1]. Each is consequently a clique of k-1 unaffected vertices, containing each color once. There are m cliques.

For even k, fix a color and its first occurrence j in H_i. All its occurrences there lie in the translate by j of

    [0,2m-1] union [(k-4)m,(k+2)m-1]
    union [(2k-4)m,(2k-2)m-1].

This larger candidate set U consists of five blocks of 2m integers. It can be placed entirely in S. If the forward translate starting at the first occurrence does not fit, that occurrence is greater than 2p+1; taking the last occurrence and the backward version then does fit and still contains all occurrences of this color in H_i.

Partition U into m ten-element sets by pairing the two entries 2l and 2l+1 in each of the five blocks. Each induced ten-vertex graph contains C5[K2], the graph obtained by replacing each vertex of a five-cycle by a two-vertex clique and joining neighboring cliques completely. Indeed the differences between the successive block starts around the five-cycle are 2m, (k-4)m, or (2k-4)m; each required difference plus -1,0,1 belongs to D, as does the distance 1 inside a pair. For k=6 the boundary value 2m-1 comes from D1. An independent set in C5[K2] uses at most one vertex from each two-vertex clique and at most two cliques, so has size at most 2. Hence the chosen color occurs at most 2m times in H_i. Summing over k-1 colors and |H_i|=2m(k-1) forces equality for every color.

The two adjacent windows H_i and H_(i+1) differ only by removing v_i and adding v_(i+p). Their equal color counts imply phi(v_i)=phi(v_(i+p)). Thus phi is p-periodic on S. Extend its pattern to all integer indices as an expected coloring psi. Every p consecutive indices contain m occurrences of each expected color for odd k and 2m for even k.

We will repeatedly use the following lifting fact. If two integer residues differ, up to sign modulo p, by a distance in D, their expected colors differ. Reduce that distance to its representative d in D intersect [1,p-1], choose one representative in [p+1,2p], and the other at distance d on either side. Both are in S and are joined by an unaffected edge. This proves the fact, including for negative indices in the expected pattern.

## 5 Blocks and parity change points in the ordinary cases

For odd k>=7, fix color c and an occurrence j in [1,p]. The p-window starting at j+2m has m occurrences of c. The D2 edges from j force them into

    j+[p-2m+2,p+2m-1],

which has 4m-2 entries. Within this interval any two same-color indices differ by an even number at most 2m-2: a short odd difference is in D1, and a difference from 2m through 4m-3 is in D2 since k>=7. There are m occurrences, so they fill a block t+F exactly. Periodicity gives one such block per color modulo p.

For even k>=10, the 2m occurrences of c in the window starting at j+2m lie in the two absolute intervals

    j+[(k-4)m+3,(k+2)m-2],
    j+[(2k-4)m+2,2km-1].

Each has fewer than 6m positions. Because (k-4)m>=6m, two same-color indices in either interval must differ by an even number at most 2m-2. Each interval therefore has at most m occurrences, and balance forces exactly m in each. Each is a full block t+F. This is the corrected translated-interval argument in Claim 4.7.

A parity change point is an integer i with psi(i) different from psi(i-2). From these block descriptions, two distinct change points of the same parity are separated by at least 2m. Every 2m step changes expected color, by the lifting fact and 2m in D2. There is consequently a change within every m successive steps of size 2. The separation and existence statements together force change points to be exactly

    {t_even,t_odd}+2mZ,

where t_even is even and t_odd is odd. This proves Claim 4.6 for odd k>=7 and even k>=10.

## 6 Exceptional even cases without circular dependence

For k=6 or k=8, Appendix B supplies the missing proof of the same change-point assertion. The following records all of its logical steps, including the two local corrections.

Work with residues modulo p. The ring R_i consists of the k-1 residue classes congruent to i modulo 2m, and Q_i=R_i union R_(i+1). The lifting fact from Section 4 is Subclaim B.1.

1. If class i has color c, its only possible other companions of color c in Q_i are i+(k-2)m, i+(k-2)m+1, i+km, and i+km+1, modulo p. The excluded offsets lie in D1, D2, or D3. The four candidates are pairwise adjacent in the residue sense because their differences are 1, 2m-1, 2m, or 2m+1. If a color occurs only in the second ring, apply this restriction based at one of those occurrences; the two same-ring candidates differ by 2m, so again at most one is possible. Thus every color occurs at most twice in Q_i, and the total of 2(k-1) classes forces exactly twice.

2. Every class i has color in {psi(i-2),psi(i+2m-2)}. If not, balance on Q_(i-2) and Q_(i-1) puts its color c on some x in R_(i-2). Let y be the unique other class of color c in Q_(i-2). Forbidden distances and the assumed unequal colors restrict

       i = x+2+{(k-2)m,km} mod p,
       y = x+{(k-2)m,(k-2)m+1,km,km+1} mod p.

   Therefore i-y is one of -2m+1, -2m+2, 1, 2, 2m+1, 2m+2 modulo p. The second and fourth possibilities contradict the assumed unequal colors. The others are forbidden distances up to sign: crucially -2m+1=-(2m-1), rather than the false positive congruence printed on p. 22. This proves Subclaim B.3.

3. A whole ring consists either of change points or of non-change points. Otherwise successive classes x and x+2m somewhere around the ring have opposite statuses, with x a change point and x+2m not one. Step 2 then gives psi(x)=psi(x+2m-2)=psi(x+2m), contradicting distance 2m. This is B.4.

4. Every ring has each color exactly once. Suppose i and j in one ring share a color c. Step 1 allows, after swapping, j=i+(k-2)m modulo p. Inductively assume psi(i+2l-2)=psi(j+2l-2)=c. The class j+2l-2m is at forbidden difference (k-4)m+2 from i+2l-2, so its color is not c. Step 2 at this class forces it to be a non-change point. Step 3 then makes the entire corresponding ring non-changing, including i+2l and j+2l. Both therefore retain c. Induction yields psi(i+2m)=psi(i), contradicting distance 2m. This proves B.5.

5. For x=0 or 1, enumerate change points t_1<...<t_s in x+{2,4,...,2m}. There is at least one, since psi(x) differs from psi(x+2m). Set t_0=x. At a change point t, Step 2 gives psi(t)=psi(t+2m-2); at all other positions the color equals its predecessor at distance 2. Correcting the non-change interval to end at t_i-2 gives, for every integer a,

       psi(t_i+2ma)=psi(t_(i-1)+2m(a+1)).

   This remains true if successive change points are two apart, when the intermediate chain is empty. Iteration gives psi(t_i)=psi(x+2mi). The k-1 distinct colors on R_x from Step 4 imply that psi(t_i)=psi(x+2mj) exactly when i=j modulo k-1. There is no change after t_s up to x+2m, so psi(t_s)=psi(x+2m), and s=1 modulo k-1.

   If s>1 then s>=k. The color psi(x+1) occurs on some class x+2mj in R_x, with 1<=j<=k-1. As j<=s, the formula gives psi(t_j)=psi(x+1). But t_j-(x+1) is an odd integer from 1 to 2m-1, contradicting D1. Hence s=1 for each parity. Combined with Step 3, this proves the desired change-point assertion for k=6,8.

No use of Claim 4.8 occurs in this argument. To close its later dependency explicitly, the change-point assertion partitions each parity into runs of exactly m equally colored entries, each of form t+F. Balance gives 2m entries of each color per period for even k. Hence every expected color has exactly two disjoint runs modulo p, including k=6,8. This supplies the missing two-block bridge.

## 7 Every nearby vertex has only two color options

For 1<=i<=(N-1)/2, Claim 4.8 asserts

    phi(v_i) belongs to {psi(i),psi(i-1)}.

It is automatic for i<=3p. Otherwise choose i_0 in [p+1,2p] congruent to i modulo p.

For odd k, the k-1 unaffected vertices with indices i_0-d and i_0-1-d, for d=0,2m,...,(k-3)m, form a clique in S. All except the two at i_0 and i_0-1 are neighbors of v_i through D2, since their forward differences from i_0 are in [2m,(k-3)m+1] and i-i_0 is a permitted positive period multiple. Thus every color except those two is excluded. This proof covers k=5 without needing block structure.

For even k, D2 and D3 edges show that v_i is adjacent to every vertex in S whose offset from i_0 lies in

    [-(k-4)m-2,-2m] union [2m-1,(k-4)m+1].

Consider a color absent from all these neighbors in the p-window starting at i_0-(k-4)m-2. Its 2m occurrences are in two full blocks t_1+F and t_2+F. This conclusion uses Section 5 for k>=10 and the bridge in Section 6 for k=6,8. The blocks do not wrap across this window's boundary because its first two positions are forbidden for the color. Their starting points lie in

    T1=i_0+[-2m+1,0],
    T2=i_0+[(k-4)m+2,km-1].

The start separation is at least 4m. If their difference is even, the change-point assertion makes it a positive multiple of 2m, and distance 2m itself is forbidden. If the difference is odd and less than 4m, the second start is at odd distance at most 2m+1 from the end of the first block, again forbidden. Neither T1 nor T2 has span 4m, so one start lies in each. The start in T1 must be its unique even or odd change-point representative. These are the starts of the blocks containing i_0 and i_0-1. Thus the missing color is psi(i_0) or psi(i_0-1), as required.

The period-shift indices used for D2 and D3 lie in their allowed ranges because 3p<i<=(N-1)/2. All tested neighbors lie in S, so none of these particular edges was removed.

## 8 Parity forcing under a deletion budget

In any interval of 2m positions under consideration, if a color occurs more than 2r times, all its occurrences have the same parity. Otherwise one parity has at least r+1 occurrences of that color. Every vertex of the other parity in this interval is adjacent to all of them in G, through odd distances less than 2m. At most r edges were removed globally, so that vertex still has a neighbor of the color in G'. It cannot itself have that color. This proves Claim 4.9. It is a statement about the actual coloring phi, not just the expected pattern.

## 9 Propagating the unaffected pattern

Let L=(N-1)/4. The goal is to extend periodicity to any interval S' of at most L positions containing S. One can first treat a one-sided extension: split a general S' at S and treat its two sides separately, reversing indices if needed. Two vertices on opposite outer sides cannot be p apart because S has length at least 3p. Shrink the unaffected core to 3p positions if necessary and extend the one-sided target to length L. Thus it suffices to treat S=[1,3p] and S'=[1,L]. Every extra index used below is less than N/2 since L+p<N/2.

Suppose i+1 is the first position in S' whose actual color differs from expectation. Then i>=3p and the two-option result gives

    phi(v_i)=phi(v_(i+1))=psi(i)=c.

### The case k at least 6

Assume i even, the other parity being identical. Let t_0 be the even change point in [i-2m+1,i], and t_1 the first odd change point after t_0. The interval W=[t_0,t_0+2m-1] contains i and i+1. Its even expected colors are all c; its odd expected colors are c_1 before t_1 and c_2 from t_1 onward, with c_1 different from c_2 and both different from c. By the two-option assertion, the positions [t_0+1,t_1-1] use only c,c_1 and [t_1,t_0+2m-1] use only c,c_2. These intervals have total length 2m-1, so one contains m consecutive positions.

Because i and i+1 both have color c with opposite parities, Section 8 bounds the total number of c-colored positions in W by 2r. At least m-2r positions of that m-interval therefore share the other color. The inequalities m-2r>m/2+1 and m-2r>2r follow from m>18r+2. They force both parities of that other color and more than 2r occurrences in W, contradicting Section 8 applied to W. The smaller m-interval is used only for the counting, not as an incorrectly sized input to Claim 4.9.

### The case k equal to 5

Here p=4m. Expected colors have fixed parities: if x<y in [1,4m] have opposite parities, one of the positive odd differences y-x and x+4m-y is less than 2m. Use the unaffected representatives x,y,x+4m and D1 to deduce distinct colors. Periodicity extends this to all positions. Since each color occurs m times per 4m-window, exactly two colors have each parity.

Set

    SL=[i-2m+2,i+1],   SR=[i-1,i+2m-2].

Both have length 2m and contain i,i+1; hence both have at most 2r actual occurrences of c. The union has length 4m-3, so has at least m-3 expected occurrences of c. All positions of SL except i+1 have their expected colors, while i+1 has the extra actual color c. Therefore SL has at most 2r-1 expected occurrences of c. Counting the union and adding the expected occurrence at i in the overlap shows that SR contains a set Sc of at least m-2r-1 expected occurrences of c.

Assume i even. All Sc positions are even. At most 2r-1 of them have actual color c because i+1 is another c-colored position of SR outside Sc. Put c_1=phi(v_(i-1))=psi(i-1), an odd expected color, and let c_2 be the other odd expected color. At most 2r-1 Sc positions can have actual color c_1; otherwise they and i-1 violate Section 8. By the two-option result, every remaining Sc position has color c_2. There are at least m-6r+1 of them, and each has an immediately preceding expected c_2 position in SR.

Among SR positions, at least 2(m-2r-1)-1 have c as one of their two expected options. The subtraction by 1 handles the possible right endpoint. At least 2(m-6r+1) have c_2 as an option, with no right-endpoint loss because expected c_2 positions are odd and SR ends even. Their intersection has size at least 2m-16r-1. All its actual colors are c or c_2, and at most 2r are c. Thus at least 2m-18r-1 positions of SR have color c_2. The parameter hypothesis makes this number greater than m+1 and greater than 2r. Both parities occur, contradicting Section 8.

In both cases no first deviation exists. Thus phi is periodic on S', proving Lemma 4.3 with its exceptional-case dependence closed.

## 10 Global contradiction and Theorem 4.1

There are at most 2r affected vertices. Any interval of L=qp/4 vertices is split by its a<=2r affected vertices into at most a+1 unaffected intervals. Its largest such interval has size at least

    (L-2r)/(2r+1) = [q/(8r+4)]p - 2r/(2r+1) > 3p-1.

Its integral size is at least 3p. Lemma 4.3 therefore gives p-periodicity on every interval of L consecutive vertices. Choose any unaffected vertex and cyclically label it v_0. The adjacent vertex v_(N-1) is still joined to it in G'. Each pair v_((a-1)p),v_(ap), for 1<=a<=q, fits in an interval of L consecutive vertices since p+1<=L. Hence

    phi(v_0)=phi(v_p)=...=phi(v_(qp))=phi(v_(N-1)).

This contradicts their surviving edge. Thus G-R has no (k-1)-coloring for every |R|<=r. Together with Section 3, this proves Theorem 4.1 for every k>=5, with no computational assumption and no imported theorem of Jensen.

## 11 Quantitative progression orders

Set m=18r+3 and A=8(k-1)m. Given n>=A(6r+3)+1 with n=1 modulo A, write n-1=Ax with x>=6r+3. If k is odd take q=8x; if k is even take q=4x. Then q is a multiple of 4, q>=24r+12, and qp+1=n. This proves Theorem 1.3 directly from Theorem 4.1. Taking x=6r+3 gives n=Theta_k(r^2) and the square-root subsequence lower bound.

## 12 Gluing without weakening resilience

Let H be a k-critical graph on h vertices with t edges u_iw_i, where critical here means both vertex- and edge-critical. For each edge take a disjoint (k,r)-graph G_i of order n_i, a vertex v_i, and a proper (k-1)-coloring of G_i-v_i. Partition its neighbors into A_i of color 1 and B_i of the other colors. Delete all edges of H, delete v_i from each gadget, and add the edges u_i A_i and w_i B_i. The new graph has h+sum_(i=1)^t(n_i-1) vertices and is simple.

In a purported (k-1)-coloring after deleting at most r new-graph edges, some original edge u_iw_i of H has equal endpoint colors. Identify their common color at v_i and retain the gadget colors. This yields a coloring of G_i after deleting at most the same r edges, transferring removed attachment edges one for one to their original incident edges. It contradicts resilience of G_i.

For vertex-criticality, a gadget can be colored with any two distinct prescribed colors at its terminals: in its chosen coloring use color 2 at u_i and 1 at w_i and then permute colors. If a vertex of H is deleted, color H minus that vertex and extend separately through all gadgets; at a missing terminal choose any distinct auxiliary color and then discard the terminal. If a vertex inside gadget j is deleted, color H-u_jw_j with k-1 colors. Its two endpoints have the same color, since otherwise it would color H. Use a vertex-deletion coloring of G_j with v_j assigned this common color and extend all other gadgets using their distinct terminal colors. This is the corrected index range i in [1,t] except j. The new graph is consequently a (k,r)-graph. This proves Lemma 2.1 in full.

## 13 Sparse critical scaffolds and all large orders

For completeness, the elementary critical-graph facts used by Lemma 2.2 can be closed without importing the cited textbook theorem.

An odd wheel on an even number n>=4 of vertices is 4-critical: its odd rim forces three rim colors and the hub a fourth; removing a rim vertex or edge leaves a path, and removing the hub or a spoke has a three-coloring. Its edge count is 2(n-1). For odd n>=7, take the Hajós join of a wheel of order n-3 and K4: delete an edge u_iv_i in each, identify u_1,u_2, and add v_1v_2. Its order is n and its size is 2(n-4)+5<2n.

The Hajós join of two k-critical graphs is k-critical. In a hypothetical (k-1)-coloring, each edge-deleted input must have equal colors on its deleted-edge endpoints, forcing v_1 and v_2 equal despite their new edge. For deletion of an internal edge f in one input, color that input minus f; its original selected edge remains, so its terminals have distinct colors. Color the other input minus its selected edge, with equal terminal colors, and match the identified vertex. The new edge is then proper. If the new edge is deleted, use equal-terminal colorings on both inputs. For a vertex deletion in one input use its critical coloring and the same terminal matching; if a selected endpoint is removed, the now-absent new edge causes no obstruction. If the identified vertex is deleted, color both input punctures and permute colors to distinguish v_1,v_2. These constructions also give the upper chromatic bound. This proves both edge and vertex criticality.

Adding a universal vertex raises chromatic number by one and preserves criticality. For a deleted new edge to old vertex v, color the old graph minus v with k-1 colors and give v and the universal vertex one common new color. Other edge and vertex deletions follow directly from criticality of the old graph. Iterating k-4 times from a 4-critical graph of order h-(k-4) constructs a k-critical graph of every order h>=k+3 with at most (k-2)h edges. This is Lemma 2.2 with its elementary dependencies proved.

Now fix k,r and A=8(k-1)(18r+3). For

    n >= A[2(k-2)A(6r+3)+2],

write n=Ax+h with A<=h<2A. We have h>=k+3. Choose the preceding k-critical scaffold H of order h and t<=(k-2)h edges. Then

    x > n/A-2 >= 2(k-2)A(6r+3) > (k-2)h(6r+3) >= t(6r+3).

Thus x is a sum of t integers x_i>=6r+3. Each n_i=Ax_i+1 is an allowed order from Section 11. The gluing operation gives total order h+sum(n_i-1)=h+Ax=n, proving Theorem 2.3 and therefore Theorem 1.2. For fixed k the threshold is Theta_k(r^3), while the progression minimum is Theta_k(r^2). These are the precise quantifier upgrades needed; merely constructing large-k graphs for a fixed r would not suffice.

## 14 Separate upper bound and its explicit external input

Conlon and Fox, *Bounds for graph regularity and removal lemmas*, Lemma 8.1 on printed p. 56, states an equitable partition into at most 2^(epsilon^(-C)) parts and, for each part X, a partition of all vertices into O(1/epsilon) sets Y such that (X,Y) is epsilon-regular. Their convention requires one alpha with alpha<d(A,B)<alpha+epsilon for all sufficiently large subpairs; it agrees with Skottová-Steiner's convention. The source's p. 57 expressly omits the proof. That theorem is the sole substantial external input to the upper bound, and is not independently reproved here.

Choose epsilon=(log n)^(-1/C), sufficiently small compared with 1/(2(k-1)). The number of parts is at most n^(log 2)<n, so a largest equitable part X has at least two vertices. For each v in X, color G-v with k-1 colors and permute colors so color 1 occupies at least (|X|-1)/(k-1)>=epsilon|X| vertices of X. Choose v uniformly from X. For each paired set Y, count its color-1 neighbors of v.

If d(X,Y)<=epsilon, their expected count is at most epsilon|Y| by averaging degrees. Otherwise the regularity interval has alpha>0. For any puncture coloring, if at least epsilon|Y| vertices of Y had color 1, those vertices and the at least epsilon|X| color-1 vertices in X would have positive density by regularity. They actually have density zero in a proper coloring, even when X and Y overlap, since the removed vertex is in neither color class. Hence each such Y has fewer than epsilon|Y| color-1 vertices. Its contribution is again at most epsilon|Y|. Sum over the partition of all vertices to get expected count at most epsilon n.

For some v, deleting those at most epsilon n incident edges permits extension of its puncture coloring by color 1 at v. This gives a critical edge set of size at most n/(log n)^(1/C). The implication is valid. It establishes no lower-bound existence result and is not used in Sections 2-13.

## 15 Supplementary necessary conditions at k equal to 4

Proposition 5.1 can also be accepted after making its empty-W case explicit. For a nontrivial vertex partition X,Y, both induced graphs are three-colorable by vertex-criticality. Randomly permuting the three colors on one side leaves expected monochromatic crossing-edge count e(X,Y)/3. Every full coloring has at least r+1 monochromatic edges, so e(X,Y)>=3r+3. In particular minimum degree is at least 3r+3.

For the maximum degree bound, suppose a vertex v has at most 2r+1 nonneighbors W. If W is empty, pick w!=v and color G-w with three colors. The color assigned to universal v appears nowhere else, so restoring w with that color creates only one monochromatic edge, a contradiction. Thus W is nonempty. For each w in W, in a three-coloring of G-w, v's color can appear among neighbors of w only inside W. At least r+1 neighbors of w must have that color, or restoring w and removing at most r edges would contradict resilience. They form an independent set of size r+1 in N(w) intersect W.

An endpoint of a longest path in G[W] has all its W-neighbors on the rest of that path. But a path on at most |W|-1<=2r vertices has independence number at most r; extra edges cannot increase it. Contradiction. Thus maximum degree is at most |V(G)|-(2r+3). Combining the minimum and maximum degree inequalities gives |V(G)|>=5r+6. This is a necessary condition, not a construction for the residual family.

## 16 Closure summary

- Theorem 4.1 depends on the vertex-deletion argument of Appendix A and Lemma 4.3; both are closed above by explicit arguments.
- Lemma 4.3 depends on local balance, the ordinary block argument, Appendix B for k=6,8, the newly explicit consequence of those change points, two color options, and the parity-budget contradiction. There is no cycle in that dependency graph.
- Theorem 1.3 follows by integer parameter substitution.
- Theorems 2.3 and 1.2 additionally use the gluing lemma and elementary sparse critical scaffolds, whose dependencies are proved above.
- Jensen's construction provides historical motivation and the shape of a coloring, but no theorem of Jensen is an unproved premise of this lower-bound proof.
- The upper bound alone imports Conlon-Fox Lemma 8.1. Its exact statement and source are verified; its omitted proof is outside this audit's closure claim.
- The Chan computation is independent of every step of this conventional proof. Combining the accepted scopes gives all r at k>=5 and r=1 at k=4, with no inference about the remaining k=4, r>=2 family.

## Attribution and review boundary

The existence construction and quantitative results proved above are those of Ema Skottová and Raphael Steiner, *Critical edge sets in vertex-critical graphs*, arXiv:2508.08703v1 (12 August 2025): https://arxiv.org/abs/2508.08703v1. Sections 2–13 give the full repaired conventional lower-bound proof, including both appendices, the exceptional k=6,8 bridge, gluing, and the all-large-orders step. The correctness-relevant printed repairs are recorded individually in AUDIT.md. The theorem statements and thresholds are unchanged.

Section 14 separately uses David Conlon and Jacob Fox, *Bounds for graph regularity and removal lemmas*, Lemma 8.1, printed pp. 56–57: https://www.its.caltech.edu/~dconlon/RegRem.pdf. That source omits the lemma's proof; this edition verifies the downstream upper-bound argument and does not re-prove the external lemma. The lower-bound proof has no such dependency.

The finite graph due to Alex Chan is separate and is neither a premise nor a repair of the conventional proof. Its historical exact-computation acceptance and the reproduction limits of this prose edition are in AUDIT.md and ACCEPTANCE.md. This AI-assisted edition is unrefereed; internal AI audit acceptance does not mean external human peer review or formal proof-assistant certification. No novelty, priority, exhaustive current-literature status, or resolution of the residual k=4,r>=2 family is claimed.

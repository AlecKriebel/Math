# A direct all-assignment certificate for the four-ray drawings of K(3,n) and K(4,n)

## 1. Result and scope

For every integer n >= 3, the explicitly specified nice drawings below of K(3,n) and K(4,n) satisfy Székely's universal set-system crossing criterion. Their crossing counts are respectively

    q(n) = floor(n/2) floor((n-1)/2),
    2 q(n).

The proof treats every simultaneous assignment of the sets A_e. It does not infer the criterion from an ordinary-crossing or pair-crossing lower bound. The essential argument is a parity identity on each K(3,3), followed by a triangle-free graph bound. Computation is unnecessary.

This is a family-specific theoretical verification, with unbounded positive crossing counts. It is not a classification of all graphs or a solution for all K(m,n). The bare existential question already has known affirmative nonplanar examples: the established independent-odd values for K(5) and K(3,3), combined with nice one-crossing drawings and Székely's criterion, give such certificates. Pelsmajer, Schaefer and Štefankovič record these values and credit Székely's earlier work; see Section 9. No novelty or priority is claimed. Section 9 separates the established criterion and related classical mechanism from the direct proof given here.

## 2. Exact objects and inequality

Let X and Y be the two vertex classes of K(m,n), where m is 3 or 4 and n >= 3. Let P be the set of unordered pairs {e,f} of vertex-disjoint edges. Each pair in P has two different endpoints in X and two different endpoints in Y. Conversely, a choice of two X-vertices and two Y-vertices admits exactly two unordered independent edge pairs. Thus

    |P| = 2 binom(m,2) binom(n,2).

In particular, |P| is 6 binom(n,2) for m=3, and 12 binom(n,2) for m=4. All counts below count these unordered edge pairs once, not ordered edge pairs or pairs of vertices.

For the drawing D specified in Section 3, put c(e,f)=1 if e and f cross, and put c(e,f)=0 otherwise.

For each edge e, choose an arbitrary set A_e contained in V(K(m,n)) minus the endpoints of e. There is no compatibility requirement among the A_e. For every {e,f} in P, set

    p(e,f) = (|e intersect A_f| + |f intersect A_e|) mod 2,
    b(e,f) = c(e,f) xor p(e,f).

Here an edge in a set intersection means its two-element endpoint set. The symbol xor denotes addition modulo 2, whose result is represented by the integer 0 or 1. Let

    wt(b) = sum over {e,f} in P of b(e,f).

We prove, for every simultaneous assignment A,

    wt(b) >= wt(c).

For complete clarity, write N_ij for the number of pairs with c=i and p=j. Then

    wt(b) = N_10 + N_01,
    wt(c) = N_10 + N_11.

Consequently this is exactly the requested inequality N_11 <= N_01, including all crossing and noncrossing independent edge pairs.

## 3. An explicit nice drawing, without a perturbation convention

Write

    a = floor(m/2),       a' = ceil(m/2),
    h = floor(n/2),       h' = ceil(n/2).

Place the X-vertices at

    (-i,0),  1 <= i <= a,
    ( i,0),  1 <= i <= a',

and the Y-vertices at

    (0,-j),  1 <= j <= h,
    (0, j),  1 <= j <= h'.

Draw every edge as the straight segment joining its endpoints. In this section, positive distance along a signed axis ray is the absolute value of the nonzero coordinate.

### 3.1 Which independent pairs cross

The interior of an edge lies in the open quadrant determined by its two endpoint rays. Interiors belonging to different quadrants are disjoint. Thus an independent crossing can occur only when both X-endpoints are on the same ray and both Y-endpoints are on the same ray.

For such four vertices, reflect the quadrant to the first quadrant and write their coordinates as

    (u,0), (U,0), (0,v), (0,V), with 0 < u < U and 0 < v < V.

Exactly one of the two independent matchings crosses: the segments (u,0)--(0,V) and (U,0)--(0,v). Their supporting lines intersect at

    x = u U (V-v)/(U V-u v),
    y = v V (U-u)/(U V-u v).

Both coordinates are positive, and x<u and y<v; hence the point is in both segment interiors. The two lines are distinct, so their intersection is transverse.

The other matching consists of (u,0)--(0,v) and (U,0)--(0,V), which are disjoint. Indeed every point (x,y) on the former segment satisfies x/u+y/v=1 and x,y >= 0, and therefore x/U+y/V < 1, whereas every point on the latter segment satisfies x/U+y/V=1.

This explicitly identifies every crossing pair: choose two X-vertices on one ray and two Y-vertices on one ray, then match the nearer X-vertex to the farther Y-vertex and vice versa.

### 3.2 Niceness, including absence of triple crossings

All vertices are distinct. Every edge is a simple segment, and its interior lies off the two axes, so it contains no other vertex. Two adjacent edges have distinct supporting lines: their other endpoints are distinct points of the other coordinate axis. They therefore meet only at their common endpoint. Two nonadjacent edges have distinct supporting lines, since one supporting line has a unique intercept on each axis. Hence any pair crosses at most once, and any interior intersection is proper and transverse.

There are no triple interior intersections. If three edges had a common interior point, they would all lie in the same open quadrant. Two of those edges could not share an X-endpoint, because adjacent edges have no common interior point. Thus the quadrant would require at least three distinct X-vertices on its boundary ray. For m=3 or m=4 each X-ray has at most two vertices, a contradiction.

The drawing is therefore nice exactly as required. Its integer coordinates need no generic perturbation, and the same argument works for every n in the asserted range.

### 3.3 Exact total crossing count

Section 3.1 gives

    wt(c) = [binom(a,2)+binom(a',2)]
            [binom(h,2)+binom(h',2)].

The first factor is 1 for m=3 and 2 for m=4. The second factor is q(n): if n=2k it is k(k-1), and if n=2k+1 it is k^2. Thus the exact counts are q(n) and 2q(n), respectively. No two crossing pairs share a crossing point by Section 3.2, so these are also the ordinary numbers of crossing points.

## 4. The all-assignment K(3,3) parity identity

Let H be an induced K(3,3) whose X-part is any three X-vertices of the constructed graph and whose Y-part is any three Y-vertices. For m=3 the X-part is all of X; for m=4 every choice of three X-vertices occupies one X-ray with two vertices and the other with one.

If r of the three Y-vertices lie on the positive Y-ray, Section 3.1 gives exactly

    binom(r,2) + binom(3-r,2)

crossings in H. This is 3 for r=0 or r=3, and 1 for r=1 or r=2. In all cases,

    sum over {e,f} in P(H) of c(e,f) = 1 mod 2.        (1)

Now define independent Boolean variables z_e(v)=1 if v belongs to A_e and z_e(v)=0 otherwise, for all allowed edge-vertex incidences. In arithmetic modulo 2,

    p(e,f) = sum over v in f of z_e(v)
             + sum over u in e of z_f(u).

Consider the coefficient of a fixed variable z_e(v) in

    sum over {e,f} in P(H) of p(e,f).

It is zero if e is not an edge of H or v is not a vertex of H. Otherwise v is a nonendpoint vertex of H. An independent partner f must contain v and join v to a vertex of the opposite part different from the corresponding endpoint of e. There are exactly two such choices in K(3,3). The coefficient is consequently 2, hence zero modulo 2. This holds for every variable, so

    sum over {e,f} in P(H) of p(e,f) = 0 mod 2.        (2)

This calculation includes every allowed incidence variable. It is an identity in all of them simultaneously, not a test of isolated switches under an assumption that their effects do not interact.

Combining (1) and (2) yields

    sum over {e,f} in P(H) of b(e,f) = 1 mod 2.        (3)

In particular, at least one independent edge pair of H has b=1. No topological parity theorem or independent-odd crossing result is assumed in obtaining (3): the baseline parity is counted in the specified drawing, and invariance under all A assignments is proved by the displayed linear identity.

## 5. From local parity to the K(3,n) bound

First take m=3. Fix an arbitrary complete assignment A, and its resulting vector b.

For each unordered pair {y,z} of distinct Y-vertices, let w_yz be the number of independent edge pairs with Y-endpoint set {y,z} for which b=1. There are exactly six eligible independent edge pairs: three choices of their two X-endpoints and two matchings for each choice. Thus w_yz is an integer between 0 and 6, and

    wt(b) = sum over {y,z} in binom(Y,2) of w_yz.     (4)

For any three vertices y,z,t in Y, the independent pairs of the corresponding K(3,3) partition by their Y-endpoint sets. Equation (3) says

    w_yz + w_yt + w_zt = 1 mod 2.

In particular, at least one of these three weights is positive.

Let S be the simple graph on Y whose edges are the pairs of positive weight. Its complement F is triangle-free. Since every positive weight is at least 1,

    wt(b) >= |E(S)| = binom(n,2) - |E(F)|.           (5)

For completeness, the triangle-free bound used here has a short elementary proof. Let F be any triangle-free graph on n vertices, with f edges and vertex degrees d_v. For any edge uv its endpoint neighborhoods are disjoint, since a common neighbor would make a triangle. Hence d_u+d_v <= n. Summing over the edges gives

    sum_v d_v^2 <= n f.

The elementary square-sum inequality gives

    (2f)^2 = (sum_v d_v)^2 <= n sum_v d_v^2 <= n^2 f.

If f=0 the desired bound is immediate; otherwise divide by f to obtain f <= n^2/4. Since f is integral,

    |E(F)| <= floor(n^2/4).

Combining this with (5),

    wt(b) >= binom(n,2) - floor(n^2/4)
          = floor(n/2) floor((n-1)/2)
          = q(n)
          = wt(c).

The middle identity follows by separately substituting n=2k and n=2k+1. This proves the exact universal criterion for K(3,n).

## 6. The K(4,n) bound and its exact multiplicity

Now take m=4 and again fix any complete assignment A on K(4,n).

For each of the four triples T contained in X, restrict to H_T=K(T,Y). For an edge e of H_T, replace its set A_e by A_e intersect V(H_T). For two edges of H_T this does not change p(e,f), since all their endpoints lie in H_T. It does not change c(e,f) either. Therefore the corresponding switched bit vector is precisely the restriction of b.

The restricted drawing has two X-vertices on one ray and one on the other, so the proof in Sections 4--5 applies unchanged. Consequently

    wt(b restricted to P(H_T)) >= q(n)

for each of the four choices of T.

Every independent edge pair in K(4,n) has exactly two X-endpoints. Exactly two of the four triples T contain both endpoints: choose the third vertex from the other two X-vertices. Each bit b(e,f) is therefore counted exactly twice in the sum of these four restricted weights. It follows that

    2 wt(b) = sum over T in binom(X,3) of
                    wt(b restricted to P(H_T))
            >= 4 q(n).

Thus

    wt(b) >= 2 q(n) = wt(c).

The assignment A was arbitrary. This proves the exact universal criterion for K(4,n), with no independence assumption between the four restrictions.

## 7. Equivalent short algebraic check on the triangle-free step

The main proof is complete. The following optional observation provides a second, purely algebraic form of the key estimate.

For K(3,n), let r_yz = w_yz mod 2. Every triangle has r-sum 1. Fix a vertex y_0. Set t_y0=0 and, for each y != y_0, set t_y=1+r_y0,y, with arithmetic modulo 2. The triangle equation then gives, for every distinct y,z,

    r_yz = 1 + t_y + t_z mod 2.

For pairs involving y_0 this follows directly from the definition; for other pairs it follows by using the triangle {y_0,y,z}. Hence r_yz=1 exactly when t_y=t_z. If the two label classes have sizes s and n-s, then

    wt(b) = sum w_yz >= sum r_yz
          = binom(s,2)+binom(n-s,2)
          >= q(n).

To see the final minimum, whenever s >= (n-s)+2, moving one vertex from the larger class to the smaller reduces the sum by s-(n-s)-1 > 0. Thus the minimum occurs at the balanced sizes floor(n/2), ceil(n/2), giving q(n). This also shows directly why a balanced two-class construction attains the bound.

## 8. Consequences and limitations

For both specified drawings and every simultaneous assignment A_e,

    #{independent pairs with c=1 and p=1}
       <= #{independent pairs with c=0 and p=1}.

They have positive crossing count for every n>=3. By Székely's Theorem 1, the drawings are independent-odd-crossing optimal, and because they are nice they are also ordinary-crossing optimal. Thus the respective independent-odd and ordinary crossing numbers equal q(n) and 2q(n).

The logical order is important: the direct all-assignment inequality was established first; the crossing-number consequences follow from the published criterion. An ordinary-crossing formula or pair-crossing formula was not substituted for the all-assignment statement.

This verification covers only the constructed drawings of K(3,n) and K(4,n), n>=3, and copies obtained by graph relabeling or plane isometries. It does not assert the criterion for arbitrary drawings of these graphs, or establish the all-K(m,n) Zarankiewicz conjecture.

## 9. Attribution and literature boundary

- László A. Székely, *An Optimality Criterion for the Crossing Number*, Ars Mathematica Contemporanea 1 (2008), 32--37, Theorem 1 on printed p.33. The theorem is the source for the exact universal criterion and its equivalence with independent-odd optimality; the structured-drawing motivation appears on printed p.34. DOI: https://doi.org/10.26493/1855-3974.43.506 . Publisher: https://amc-journal.eu/index.php/amc/article/view/43 . Full paper: https://amc-journal.eu/index.php/amc/article/download/43/30 . Definitions, the statement, and the motivation were inspected in the retained six-page publisher paper.
- Michael J. Pelsmajer, Marcus Schaefer and Daniel Štefankovič, *Removing Even Crossings*, Journal of Combinatorial Theory, Series B 97 (2007), 489--500, DOI https://doi.org/10.1016/j.jctb.2006.08.001 . Their author manuscript, dated 4 October 2006, states the strong Hanani--Tutte theorem as Theorem 1.2 and records iocr(K(5))=iocr(K(3,3))=1 in Remark 1, crediting Székely's earlier algebraic treatment: https://ovid.cs.depaul.edu/documents/tutte.pdf , PDF pp.3--4. Those passages were inspected. They establish prior nonplanar positive instances; this report does not present the bare existence answer as new.
- The four-ray complete-bipartite construction is the classical Zarankiewicz construction, specialized here to m=3,4 with completely explicit coordinates. No claim is made to have invented it or the crossing counts.
- A closely related classical K(3,n) pair-crossing argument is presented as Lemma 1 in David Eppstein, *The Effect of Planarization on Width*, Journal of Graph Algorithms and Applications 22(3) (2018), 461--481, Lemma 1 on printed pp.466--468, DOI https://doi.org/10.7155/jgaa.00468 , publisher PDF https://jgaa.info/index.php/jgaa/article/download/paper468/2483/2290 . The source uses induction on K(3,n) and K(3,3) restrictions and presents the four-ray construction. The statement and this proof were inspected. That result concerns pair crossings and is not used as an independent-odd theorem here. The direct modulo-2 coefficient argument in Section 4 supplies the exact all-A statement needed in this proof. The literature credits Zarankiewicz and Kleitman for the underlying construction and lower-bound mechanism; no novelty claim is made for this exposition or adaptation.
- The triangle-free edge bound in Section 5 is Mantel's theorem; its complete elementary proof is included rather than treated as an unproved input.

No unpublished ordinary-crossing claim for general complete bipartite graphs is used. Broader classification, priority, and the current status of unrestricted complete-bipartite independent-odd crossing questions are outside this result.

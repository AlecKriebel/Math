# A polynomial versus superpolynomial separation for vertex-distribution-free graph testing

## Status and scope

This is an authored negative answer to the complexity comparison in OWR-16931-012 / problem 30004127, accepted as complete by the accompanying [mathematical audit](MATHEMATICAL_AUDIT.md). This AI-assisted manuscript and audit are unrefereed; acceptance is not external human peer review, journal acceptance or proof-assistant certification. The construction, distance calculation, ordinary-model upper bound, and two-sided oracle lower bound are proved below. No computational experiment or undistributed dataset is needed for the argument. No novelty or priority claim is made.

The separation holds for a fixed property which is hereditary, extendable, and also closed under edge deletion. Thus even a polynomial relation between the two complexities fails. It does not claim a separation for every single forbidden-subgraph property.

## 1. Models and theorem

Graphs are finite, undirected and simple. Write

  dist_D(G,P) = min_{F in P, V(F)=V(G)} sum_{xy in E(G) symmetric-difference E(F)} D(x)D(y),

where each unordered pair occurs once and D is a probability distribution on V(G). Being epsilon-far means distance at least epsilon. In the standard model D is uniform, so the denominator is |V(G)|^2, not the number of unordered pairs. An algorithm must accept members and reject epsilon-far inputs with probability at least 2/3. Its input need not include the number of vertices. It may sample independently from D and ask adjacency queries. We count sample calls and adjacency calls separately.

A canonical tester samples a prescribed number of vertices independently, examines all pairs of distinct sampled labels, and accepts exactly when the graph induced by the distinct labels belongs to P. The number of sample calls is its vertex-sample complexity; the adjacency cost is at most the binomial coefficient of this number and 2. In particular, an induced graph is never formed by treating repeated occurrences of one label as different vertices.

Let C_3 be the property of being 3-colorable. Let A_3 consist of graphs from which deletion of at most one vertex leaves a 3-colorable graph. Define the single, fixed property

  P = { G : G is K_4-free and G belongs to A_3 }.

Here K_4-free means no ordinary (equivalently induced) four-vertex clique.

**Theorem 1.** The following statements hold.

1. P is hereditary and extendable. It is also closed under edge deletion.
2. In the standard model P has a one-sided canonical tester, valid on every finite graph without knowing its size, using

     O(epsilon^(-6) log(1/epsilon)) vertex samples

   and at most O(epsilon^(-12) log^2(1/epsilon)) adjacency queries as epsilon tends to zero.
3. There is an explicit sequence epsilon_d tending to zero such that every unrestricted VDF tester for P, including a two-sided adaptive tester, has worst-case total sample-plus-adjacency cost at least

     exp(c (log(1/epsilon_d))^2)

   for some absolute c>0 and all sufficiently large d. More precisely, a tester with at most s samples and e adjacency queries on these instances must obey the endpoint-exposure lower bound in Section 7. A tester whose queries are restricted to sampled labels needs exp(c log^2(1/epsilon_d)) vertex samples even if all adjacencies between those labels are free.

Consequently, the VDF complexity cannot be bounded by any fixed polynomial in the classical complexity and 1/epsilon, even allowing a fixed constant rescaling of epsilon in the classical bound. The ordinary upper bound is polynomial for all small epsilon, while the VDF lower bound is superpolynomial along epsilon_d. This gives a quantified meaning much weaker than 'same' that already fails.

The lower bound holds with positive rational weights only. Thus no irrational-weight approximation or same-epsilon transfer is used. It remains valid when the tester is additionally told the input size, the distinguished heavy vertex and the entire weight vector.

### Elementary structural facts

The property C_3 is contained in P: a 3-colorable graph has no K_4, and no vertex need be removed. Induced subgraphs of a graph in A_3 are in A_3, using the old exceptional vertex if it remains and no exceptional vertex otherwise. Clique-freeness is hereditary. This proves heredity of P. Adding an isolated vertex preserves both conditions, so P is extendable. Deleting edges also preserves both conditions.

## 2. A self-contained polynomial 3-colorability sampling lemma

The following deliberately conservative bound suffices. The branching-list method is a version of the standard colorability-testing argument of Goldreich–Goldwasser–Ron and Alon–Krivelevich. A complete argument is included to avoid relying on an asymptotic input-size qualification in a cited theorem. Better known sample bounds are not needed.

**Lemma 2.** Fix 0<epsilon<=1/8 and set

  h = floor(6/epsilon) + 1,
  l = ceil((2/epsilon) log(12 * 3^h)),
  r = h*l.

If an n-vertex graph G is epsilon-far from C_3 under the uniform distribution, r independent uniform samples induce a non-3-colorable graph with probability at least 11/12. The statement holds for every n and with replacement.

**Proof.** Consider any proper partial coloring phi:S->{1,2,3}. For v outside S let L(v) be the colors not used on its neighbors in S. Let U be the outside vertices with empty lists. For v outside S union U define

  delta(v) = min_{i in L(v)} |{ u outside S union U : uv is an edge and i is in L(u) }|.

Color S by phi, color U arbitrarily, and color every remaining v by a minimizing color in the definition of delta(v). There are no monochromatic edges within S, or from S to the vertices with nonempty lists. Edges incident with U number at most n|U|. The other monochromatic edges number at most sum_v delta(v): each monochromatic neighbor of v is among the neighbors counted for v's chosen color. Deleting all monochromatic edges produces a 3-colorable graph. Hence

  epsilon*n^2 <= n|U| + sum_v delta(v).

Let W be the vertices outside S union U with delta(v)>=epsilon*n/2. Since delta(v)<=n always, the right-hand side is at most

  n(|U|+|W|) + epsilon*n^2/2.

It follows that |U union W|>=epsilon*n/2.

For a proper partial coloring, use the potential Phi=sum_{v outside S}|L(v)|. Initially Phi=3n. If v is in W and it is colored with any feasible color, adding v to S decreases Phi by at least epsilon*n/2: that color disappears from at least delta(v) other nonempty lists. The removal of v's own list only helps. If a vertex of U is added, no feasible color is possible.

Partition the r samples into h independent blocks of l samples. Construct a tree of proper partial colorings, initially containing the empty coloring. At a node at depth j, use block j+1 and take its first vertex in the corresponding U union W. If it is in U, the node has no feasible children. Otherwise create one child for each of its at most three feasible colors. If the block misses U union W, call this node a failure. Conditional on all earlier blocks, any existing node has probability at most

  (1-epsilon/2)^l <= exp(-epsilon*l/2) <= 1/(12*3^h)

of failure. There are fewer than 3^h possible nodes at depths 0,...,h-1. Conditional union bounds, or equivalently a sum over the fixed ternary-tree addresses, show that with probability at least 11/12 no node fails. This does not require independence of nodes using the same block.

On this event, a feasible branch cannot survive h levels: every feasible step decreases Phi by at least epsilon*n/2, whereas h>6/epsilon and Phi starts at 3n and stays nonnegative. Thus every branch closes. If the graph induced by all sampled labels had a proper 3-coloring, following its colors at the chosen vertices would give a surviving feasible branch. A chosen vertex is outside its path's S, so repetitions elsewhere in the sample cause no problem. This contradiction proves the lemma. □

## 3. A polynomial classical tester for P

Keep r from Lemma 2 and set

  N = 12*r^2,
  M = ceil(N*log(3*N)).

Sample M vertices uniformly and independently; accept exactly when their induced graph belongs to P. This is a well-defined finite computation, although no polynomial running-time claim is made. Its adjacency cost is at most M(M-1)/2. Its completeness is one-sided by heredity.

Suppose G is epsilon-far from P. Because C_3 is a subset of P, G is also epsilon-far from C_3.

If n>=N, divide the first 2r sample calls into two r-blocks. Each block spans a non-3-colorable graph with probability at least 11/12. The probability that their underlying vertex sets intersect is at most r^2/n<=1/12, by a union bound on cross-block pairs. With probability at least 1-1/12-1/12-1/12=3/4, both blocks are non-3-colorable and their vertex sets are disjoint. Their union cannot become 3-colorable by deleting one vertex: a deletion affects at most one of the two witnesses. Consequently the whole sampled induced graph is outside A_3 and outside P.

If n<N, the probability that at least one vertex remains unseen after M draws is at most

  n*(1-1/n)^M <= n*exp(-M/n) <= N*exp(-M/N) <= 1/3.

For n=1 the same conclusion follows directly. On seeing every vertex the tester rejects, since G is outside P. There is no need for the algorithm to know which size case holds. The formula M is at least 2r. As h=O(epsilon^-1), l=O(epsilon^-2), r=O(epsilon^-3), we have M=O(epsilon^-6 log(1/epsilon)), proving Theorem 1(2).

For epsilon>1/8 one may use the tester with parameter 1/8: an epsilon-far input is also 1/8-far. This extends the algorithm to all relevant positive parameters. The empty graph has the property and needs no special rejection behavior.

## 4. An exact heavy-apex distance identity

For a graph H on n>=1 vertices, let J(H) be obtained by adjoining a vertex a adjacent to every vertex of H. Set

  D(a)=1/2, and D(v)=1/(2n) for v in V(H).

**Lemma 3.** If H is 3-colorable, then

  dist_D(J(H),P) = (1/4) dist_uniform(H, triangle-free).

**Proof.** For the upper bound, delete a smallest set of tail edges making H triangle-free. The resulting tail remains 3-colorable. Its join with a is K_4-free, because a K_4 containing a would correspond to a tail triangle, and a K_4 wholly in the tail is impossible in a 3-colorable graph. Deleting a leaves a 3-colorable graph, so the repair is in P. A changed tail edge has D-weight 1/(4n^2), exactly one quarter of its uniform tail weight.

For the lower bound, let F be any graph in P on the same vertex set, and let S be the tail vertices whose edge to a was deleted. Write delta_a=|S|/(4n) for the cost of these root-edge changes and delta_t for the cost of tail changes. The root was originally adjacent to every tail vertex, so no root-edge additions are possible. Because F is K_4-free, F restricted to V(H)\S is triangle-free: a triangle there together with a would be a K_4.

Produce a triangle-free graph on V(H) by using F on V(H)\S and making S independent of every vertex. Relative to H, its changed tail edges outside S number at most 4n^2*delta_t. Deleting all original edges incident with S costs at most n|S| additional changes. Thus

  dist_uniform(H,triangle-free) <= 4*delta_t + |S|/n
                                    = 4*(delta_t+delta_a).

Minimize over F. This gives the other inequality and proves the identity. □

In particular, triangle-free 3-partite H yields J(H) in P. The distance identity uses the complete permitted edit distance, including additions; the lower bound did not assume repairs use deletions only.

## 5. Explicit tripartite hosts with only edge-disjoint triangles

This section supplies all combinatorial details rather than treating a Ruzsa–Szemerédi graph as computational input. The sphere construction is credited to Behrend; the arithmetic progression-to-triangle construction is the standard Ruzsa–Szemerédi method.

Fix an integer d>=4, and put

  B=2^d,  m=(2B)^d=2^{d(d+1)},
  K=floor(2^{d^2-2d}/d).

There is a set A contained in {1,...,m} of size exactly K such that a+b=2c with a,b,c in A implies a=b=c. To prove this, consider vectors x in {0,...,B-1}^d. Their squared Euclidean norms take at most d(B-1)^2+1<=dB^2 values. One sphere therefore contains at least

  B^d/(dB^2) = 2^{d^2-2d}/d

such vectors. Encode a vector as 1+sum_{i=0}^{d-1} x_i(2B)^i and take any K encodings from that sphere. All encodings lie in {1,...,m}. In an equation a+b=2c the added 1 cancels. Each digit sum is at most 2B-2, so no carries occur in base 2B, and the corresponding vectors obey x+y=2z. Equal squared norms then give

  ||x-y||^2 = 2||x||^2+2||y||^2-4||z||^2 = 0.

Thus x=y=z, proving the assertion.

Build a tripartite graph R with disjoint parts

  X={x_X:1<=x<=m},
  Y={y_Y:1<=y<=2m},
  Z={z_Z:1<=z<=3m}.

For each pair (x,a) in {1,...,m} times A, insert the three edges of the triangle

  (x_X, (x+a)_Y, (x+2a)_Z).

There are n=6m vertices and T=mK designated triangles. No edge belongs to two designated triangles: any one of the three edge types determines x and a uniquely. Every triangle is designated. Indeed, its XY edge gives y-x=a in A, its YZ edge gives z-y=b in A, and its XZ edge gives z-x=2c with c in A. Thus a+b=2c, so a=b=c and its vertices form the designated triangle for (x,a).

We have proved: R is 3-partite, its only triangles are precisely T pairwise edge-disjoint designated triangles, and it has no other edges.

## 6. Matched local distributions

Independently at each of the T designated triangles, choose a pattern of retained edges in a fixed ordering of its three edges.

- GOOD: choose uniformly from 000, 011, 101, 110.
- BAD: choose uniformly from 111, 100, 010, 001.

These choices are unambiguous because designated triangles have disjoint edge sets. Edges outside R remain absent. For each triangle, restriction to any specified zero, one, or two edges has the same distribution in GOOD and BAD: every assignment on those coordinates is equally likely. Choices for different triangles are independent.

A GOOD tail H has no triangle, because no designated triangle is retained in full and R has no other triangles. Therefore every J(H) from GOOD belongs to P.

For a BAD tail, let Z_0 be the number of designated triangles whose pattern is 111. Then Z_0 is binomial with T trials and success probability 1/4. These are all the triangles of H and they are edge-disjoint. Consequently exactly Z_0 edge deletions suffice and are necessary to make H triangle-free. By Lemma 3,

  dist_D(J(H),P) = Z_0/(4n^2).

A standard exponential-moment calculation, included below, gives

  Pr[Z_0<T/8] <= exp(-T/32).

Set

  epsilon_d = T/(32n^2) = K/(1152m).

At least a 1-exp(-T/32) fraction of BAD inputs are epsilon_d-far from P.

For completeness, if Z is binomial with mean mu, Markov's inequality applied to exp(-lambda Z) gives

  Pr[Z<=mu/2] <= exp(lambda*mu/2) * (1-p+p*exp(-lambda))^T
               <= exp(mu*(lambda/2+exp(-lambda)-1)).

With lambda=log 2, the bracket is (log 2-1)/2<=-1/8, because log 2<=3/4 (for example integrate 1/x on [1,2], or use exp(3/4)>2). Here mu=T/4, yielding exp(-T/32). The event Z<T/8 is contained in the event used in this bound.

## 7. Adaptive oracle lower bound

### The strengthened access model

Give the tester n and identify the apex label a for free. Give it the entire distribution D: mass 1/2 at a and mass 1/(2n) at each tail label. The tail labels are a known set of n distinct names. Apply a uniformly random secret bijection between these names and the vertices of the fixed host R, independently of the GOOD/BAD pattern bits. The tester may query any two names adaptively, not merely previously sampled names. It may use its own randomness. Oracle calls are bounded in the worst case.

These gifts can only help a tester. Lower bounds in this strengthened model therefore apply to the original unknown-distribution, possibly size-oblivious model on this family of inputs.

Whenever a tail label is first mentioned in a sample or adjacency query, call it exposed. If an algorithm uses s sample calls and e adjacency calls, it exposes at most

  k=s+2e

tail labels. We further help it by revealing the entire induced graph on exposed labels immediately, at no adjacency cost. We do not reveal their secret host identities. Root adjacencies are deterministic and contain no GOOD/BAD information.

### Exposure lemma

**Lemma 4.** For any such adaptive tester, the total variation distance between its complete GOOD and BAD transcripts is at most

  min(1, T*(k)_3/(n)_3)

when k<=n, where (x)_3=x(x-1)(x-2). With k>=n the trivial bound 1 suffices. In particular, for n>=6, it is at most 2T*k^3/n^3 whenever this latter bound is less than 1, and the same inequality trivially holds otherwise.

**Proof.** Generate the secret bijection lazily. Conditional on all host images of exposed labels, every unused name is assigned uniformly among remaining host vertices, independently of previous pattern observations. The pattern choices do not concern the unexposed permutation. Thus whenever the tester first names a new label, even when this choice depends on its transcript, its host image is uniform among the as-yet-unassigned host vertices. The sampling oracle can be realized by first choosing whether to return the root and, otherwise, choosing a uniformly random tail name; this procedure depends on no pattern bits.

Use the same algorithm coins, oracle sample-name choices, and fresh permutation images in two worlds. At each designated host triangle, reveal its pattern only on demand. Until all three of its host vertices have been exposed, at most two of its three edge coordinates can have been revealed. GOOD and BAD have identical joint distributions on those coordinates; conditional distributions for the next coordinate likewise agree as long as at most two coordinates in total are exposed. Couple these observations identically. Different triangle patterns are independent, so the construction applies simultaneously. All non-host edges are zero in both worlds.

The two transcripts therefore remain identical until the exposed host set contains a designated triangle. Stop the coupling on this event; after that it may be completed arbitrarily with correct marginals. Pad the ordered list of fresh host images to k entries if needed. For k<=n, this padded list is a uniform ordered sample without replacement. One way to verify the last assertion is to condition additionally on every already exposed host image: the next unused image has probability 1/(n-j) at each remaining vertex, whatever the preceding transcript or adaptive choice of a new name. Padding uses this same rule.

For each fixed designated triangle, the probability that all three vertices are in the first k images is (k)_3/(n)_3. A union bound over T triangles gives the stated coupling failure bound, which bounds total variation. For n>=6, (n)_3>=n^3/2, and (k)_3<=k^3. If k>=n, then 2T*k^3/n^3>=1 since T>=1, so the final coarse inequality is still valid. □

### Quantitative contradiction

Assume a tester has error at most 1/3. Its rejection probability on GOOD is at most 1/3. On unconditional BAD it is at least

  (2/3)*(1-p), where p=exp(-T/32),

because each epsilon_d-far instance must be rejected with probability at least 2/3; no guarantee is required on the remaining BAD instances. Thus the rejection-probability difference is at least

  1/3-(2/3)*p.

For our d>=4, T>=32 log 4, so p<=1/4 and this difference is at least 1/6. Lemma 4 gives

  2T*(s+2e)^3/n^3 >= 1/6,

and hence the promised endpoint-exposure inequality

  s+2e >= (n^3/(12T))^(1/3).                         (1)

If Q bounds s+e, then s+2e<=2Q, and

  Q >= (n^3/(96T))^(1/3)
    = (216m^2/(96K))^(1/3)
    >= m^(1/3),                                    (2)

using K<=m. The same conclusion holds for a single bound Q on the total number of oracle operations even when the split between s and e varies by execution: at most 2Q labels are exposed, and Lemma 4 applies directly with k=2Q.

If all queries are restricted to sampled labels, even arbitrarily many free induced adjacency queries reveal at most s tail labels. The stronger version of the same reasoning gives s>=(n^3/(12T))^(1/3), in particular s>=m^(1/3). This separately establishes the claimed vertex-sample lower bound, without identifying sample count with edge-query count.

Finally, since d>=4 and floor(x)>=x/2 for x>=1,

  1/(2304*d*2^(3d)) <= epsilon_d <= 1/(1152*d*2^(3d)).

Therefore epsilon_d tends to zero, log(1/epsilon_d)=Theta(d), and

  m^(1/3)=2^{d(d+1)/3}=exp(Theta(d^2)).

Equations (1) and (2) yield the asserted exp(c log^2(1/epsilon_d)) lower bounds. Comparing with Section 3 proves Theorem 1. □

## 8. What the construction does and does not use

The obstruction is a vertex of weight 1/2, whose single-vertex exceptional role is negligible for uniform large graphs but is expensive to erase in the weighted graph. Classical sampling can detect two disjoint 3-coloring violations, or collect a small input completely. Weighted sampling cannot remove the heavy vertex's force on triangle structure in its neighborhood.

The property here is fixed across every d and epsilon. Only the inputs and their positive rational distributions vary. The proof applies to two-sided adaptive testers, not just a canonical one-sided tester. The standard upper bound also handles small inputs and does not receive the number of vertices. The lower bound even supplies that number and the distribution. No proximity promises about the intermediate BAD inputs that are not far are used.

A direct finite witness shows why Proposition 5.7 does not cover P. Let W be the six-vertex wheel formed by a universal vertex and a 5-cycle. It is K_4-free and deleting its center leaves a 3-colorable graph, so W is in P. Blow every vertex up to two vertices. If any one of the six classes has an internal edge, that edge together with one vertex from each of two adjacent neighbor classes gives a K_4: every vertex of W lies in a triangle. Otherwise all six classes are independent. After deleting any one vertex, each class is still nonempty, so the remaining graph contains an induced W and is not 3-colorable. Thus every such blowup is outside P. A blowup-avoidable property would allow a blowup of a member with no forbidden induced copy at all, since a transversal forbidden copy would project to a forbidden copy in the member. Therefore P is not blowup-avoidable. This explains the boundary without using the separation theorem to establish it.

## 9. Credits and primary references

- L. Gishboliner and A. Shapira, “Testing Graphs against an Unknown Distribution,” arXiv:1905.09903v5 (28 September 2021), especially the model in Section 1, Problem 5.6, Proposition 5.7, and footnotes 23–24. https://arxiv.org/abs/1905.09903v5
- L. Gishboliner, joint work with A. Shapira, contribution to Oberwolfach Report 19/2019, “Combinatorics, Probability and Computing,” Problem 5, publisher PDF p.27. https://ems.press/content/serial-article-files/46798
- O. Goldreich, “Testing Graphs in Vertex-Distribution-Free Models,” author manuscript, especially Proposition 2.2 on sampled-vertex access and Theorem 2.3 on converting two-sided VDF testing to one-sided testing. These results are contextual; the lower bound here proves its own adaptive-access statement and does not invoke that conversion. https://www.wisdom.weizmann.ac.il/~oded/R3/vdf.pdf
- N. Alon and M. Krivelevich, “Testing k-colorability,” SIAM Journal on Discrete Mathematics 15 (2002), 211–227; Theorem 3 and Section 4. Their polynomial colorability sampling theorem and the earlier Goldreich–Goldwasser–Ron branching method motivate Lemma 2; our conservative all-size proof is included above. https://doi.org/10.1137/S0895480199358655 ; inspected author manuscript: https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/AlonKrivelevich.pdf
- F. A. Behrend, “On Sets of Integers Which Contain No Three Terms in Arithmetical Progression,” PNAS 32 (1946), 331–332. The sphere-and-digits construction in Section 5 is this classical method with explicit parameters. https://doi.org/10.1073/pnas.32.12.331 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC1078964/
- I. Z. Ruzsa and E. Szemerédi, “Triple systems with no six points carrying three triangles,” Colloquia Mathematica Societatis János Bolyai 18 (1978), 939–945. The arithmetic triangle construction is credited to this standard method and proved in full here. Bibliographic publisher-volume record: https://www.bolyai.hu/files/kotetek_18_1978.pdf . The original seven-page article was not recovered or relied upon as a black box.

The model question and prior testability/classification results belong to the cited authors. This manuscript makes no assertion that its separation is absent from all prior or recent literature. Bibliographic and retrieval metadata are recorded separately; mathematical correctness does not follow from those metadata.

# Turn 2: a constructive hairy-path test for the unknown-tree mixture

**Partial result; original transition unresolved after author turn 2.** This makes the source's credited hairy-path mechanism quantitative using classical weighted Prüfer enumeration. No novelty claim. The unknown-shape model is exactly the one in `SOURCE_GATE.md` and `TURN_1.md`.

## 1. A sufficient mean-degree criterion

For fixed c>0, define

    g(c)=(c+1)log(1+1/c)−1−log c.                  (1)

If g(c)>0 and

    k/(log n)² → infinity,  k≤n,                  (2)

then an explicit, possibly inefficient test strongly distinguishes the unknown uniform labelled k-tree mixture from G(n,c/n).

The test looks for a simple path of a prescribed length of order log n with unusually many edges leaving its vertex set. Its proof uses the actual random planted Cayley tree, not a bounded-degree substitute or a template revealed to the detector.

The derivative g'(c)=log(1+1/c)−2/c is negative. The endpoint limits show a unique positive zero c_h. Exact rational logarithm bounds give

    4/3 < c_h < 7/5.                              (3)

Thus the theorem includes, for example, mean degree c=4/3. The condition (1) and rational bracket (3), rather than a decimal root approximation, define the rigorous criterion.

This does **not** prove detection at a fixed constant multiple of (log n)², and does not settle the source's separate O(log n) question. Condition (2) is deliberate. It still gives a polylogarithmic size, for example k=ceil((log n)³), throughout c<c_h.

## 2. Distance between two fixed vertices of a uniform Cayley tree

Let T be uniform among labelled trees on [k]. Select two distinct fixed labels U,V, say 1 and 2, and let D be their distance. For 1≤d≤k−1,

    Pr(D=d)=(k−2)_(d−1) (d+1)/k^d.                (4)

There are (k−2)_(d−1) possible ordered intermediate labels. The probability of containing the resulting d-edge path is (d+1)/k^d by the classical forest-extension count proved in Turn 1. In a tree that path, if present, is the unique U-to-V path, so the events are disjoint. This proves (4).

In particular,

    Pr(D≤ell)≤ell(ell+3)/(2k).                     (5)

The product in (4) also gives a Gaussian upper tail. For d≥1,

    Pr(D=d)≤[(d+1)/k]
      exp(−[d(d+1)/2−1]/k).                       (6)

Consequently, for ell=O(log n) under (2),

    Pr(ell+1≤D≤k^(2/3))→1.                        (7)

For the upper tail, summing the bound for d≥floor(k^(2/3)) gives at most O(k exp(−Omega(k^(1/3)))). These elementary bounds avoid assuming an unproved concentration of the tree height at a deterministic multiple of sqrt(k).

## 3. Exact boundary law for a prefix of that path

Condition on the full U-to-V path, of length d≤k−2, including its ordered labels. Let S contain its first s vertices, where 1≤s≤d; thus S is a strict prefix. The tree edges leaving S have the exact distribution

    B_T(S) = 1 + Ber(s/(d+1)) + Bin(k−d−2,s/k),    (8)

with independent Bernoulli and binomial terms on the right.

To prove (8), contract the full d+1 vertex path to a single component of weight d+1; the other k−d−1 vertices have weight one. Conditional on containing that path, the component tree has the weighted Cayley distribution. Its Prüfer letters are independent, with component-selection probabilities equal to their weights divided by k. Hence the degree of the contracted path component is

    1+Bin(k−d−2,(d+1)/k).

For each incident component-tree edge, its endpoint on the original path is independent and uniform among the d+1 path vertices. Thinning to the s prefix vertices changes the distribution of off-path attachments to

    Ber(s/(d+1))+Bin(k−d−2,s/k).

There is also exactly one original path edge leaving the strict prefix. This proves (8). Edges are not confused with induced-component sizes; the attachment counts refer to the actual boundary edges of S. If d=k−1 there are no off-path vertices and the boundary is exactly one; that exceptional case is excluded by (7) for the asymptotic argument.

Set s=ell+1 and use the first ell edges of the U-to-V path. Uniformly for d in the event (7), the binomial term in (8) has mean

    (ell+1)[1−(d+2)/k]=(1−o(1))ell.

For every fixed epsilon>0, a binomial lower-tail bound therefore gives

    Pr(B_T(S)<(1−epsilon)ell | full path)≤exp(−Omega(ell)). (9)

Together with (7), this proves that a uniform Cayley tree of size satisfying (2) contains a path of length ell with at least (1−epsilon)ell tree edges leaving its vertex set, with probability tending to one. The selected path is only an existence witness in the proof; the detector is not supplied with its labels or the tree.

## 4. The test and its null error

Assume g(c)>0. Choose a fixed delta>0 small enough that delta<min(1,c)/2 and, writing y=c+1−delta,

    I_c(y):=y log(y/c)−y+c > log c.                (10)

Choose a constant K>1/[I_c(y)−log c], and put ell=ceil(K log n). The test rejects the null if there exists a simple ell-edge path with vertex set S such that

    number of graph edges from S to [n] minus S ≥ y ell. (11)

Threshold rounding is immaterial; one may use a ceiling. The test is a finite enumeration and no polynomial running time is asserted.

Under the null, the expected number of ordered ell-edge paths is at most n c^ell. For a fixed ordered path, conditional on its internal path edges being present, its boundary count is an independent binomial

    Bin((ell+1)(n−ell−1), c/n).

Its mean is c ell+O(1). The standard exponential binomial bound at (11) gives probability at most

    exp(−ell I_c(y)+O(1)).

A union bound therefore gives null rejection probability at most

    exp(log n−ell[I_c(y)−log c]+O(1))=o(1).        (12)

This bound counts all simple paths, including those with additional internal graph edges. It does not assume the graph has no such chords.

## 5. Alternative error with all background edges accounted for

Under Q, use the planted-tree prefix supplied by Sections 2–3. With high probability it has B=B_T(S)≥(1−delta/3)ell. Conditional on the tree and the selected S, the observed graph's boundary count is exactly

    B + Bin((ell+1)(n−ell−1)−B, c/n).              (13)

The remaining boundary edges are independent because the selection used only T, not the background graph. Since B≤k−1≤n−1, the binomial mean is at least

    c(ell+1)(1−(ell+1)/n)−c ≥ c ell−o(1).

It is also at most c(ell+1). A lower-tail bound shows it is at least (c−delta/3)ell with probability 1−o(1), uniformly over the good selected paths. Together with B this is larger than y ell for all sufficiently large n, including rounding. Thus (11) holds with high probability under Q.

Equations (12) and (13) prove strong detection under (1)–(2). The construction is annealed over the unknown random tree and its embedding, exactly as required. The proof does not condition on a detector knowing the tree shape.

## 6. An explicit rational constant and a monotone critical parameter

The strict inequality g(4/3)>0 can be certified without floating-point logarithms. For x>1, use

    log x = 2 sum_(j≥0) u^(2j+1)/(2j+1), u=(x−1)/(x+1),

and bound the tail after m terms by

    0<tail≤2u^(2m+1)/[(2m+1)(1−u²)].

For x=7/4 and x=4/3, a few rational terms certify (7/3)log(7/4)−1−log(4/3)>0. The same method certifies g(7/5)<0. The checker records exact rational intervals. It also checks one explicit test choice at c=4/3: delta=1/100 and K=100 satisfy (10) and the strict inequality K[I_c(c+1−delta)−log c]>1.

There is a simple monotonicity in background density. For p_1<p_2, independently add each absent edge with probability

    r=(p_2−p_1)/(1−p_1).

This maps G(n,p_1) to G(n,p_2). It also maps the unknown planted-tree alternative at p_1 to the alternative at p_2, since planted edges remain forced and all other edges acquire probability p_2. This is a stochastic channel independent of the hidden tree. Hence total variation cannot increase with c, and a test at a larger fixed c transfers to a smaller one by this channel.

Define C_poly as the supremum of fixed c>0 for which some fixed polynomial in log n size admits strong detection in the unknown-tree model. The set is downward closed. The present positive result and Turn 1 give the rigorous bracket

    c_h ≤ C_poly ≤ e,                              (14)

and no polylogarithmic size is detectable at c=e. Equation (14) does not decide whether the supremum equals either endpoint or lies strictly between them, nor whether its endpoint is attained.

## 7. What this changes, and what remains

This turn supplies an actual detector under a quantitative sufficient mean-degree criterion, with a complete random-tree conditioning argument. It uses and credits the hairy-path idea explicitly announced in the original OWR source. Its k≫log² n size condition is weaker than the source's fixed-constant upper-bound formulation, and it is not an O(log n) result. There is no claim of historical priority for the criterion or its optimization.

The remaining interval between c_h and e, the optimal low-c unknown-tree size, and the true critical transition are still unresolved. Richer local statistics on long planted-tree paths, or a truncated-likelihood analysis, may improve the bracket. The present argument does not turn the second-moment boundary e into a proven detection transition, and does not infer detection from moment divergence.

# A two-dimensional complex with PL embedding dimension 3 and linear embedding dimension 5

**Problem:** 30000439 / OWR-1194-009.
**Status:** Accepted exact resolution, published unrefereed preprint v1.0, DOI10.5281/zenodo.23088066. Three independent math/source families, two deep bounded priority audits and two sequential fresh full preprint/package reviews completed after runtime documentation repair. No human peer review, formal proof certification or categorical first priority claimed.
**Date:** 30 September 2026. **Model:** gpt-6-astra, xhigh. **Substantive response:** 1/5.

## 1. Claim and terminology

For a finite simplicial complex $K$, let $e_{\rm PL}(K)$ be the least Euclidean dimension admitting a piecewise-linear embedding of its underlying polyhedron. Let $e_{\rm lin}(K)$ be the least dimension admitting an embedding affine on every original simplex, without subdivision.

**Theorem.** There exists a finite two-dimensional simplicial complex $K$ such that

$$\boxed{e_{\rm PL}(K)=3,\qquad e_{\rm lin}(K)=5.}$$

Thus the two minimum dimensions can differ by more than one. This is precisely the existential question in Brehm's contribution to [Oberwolfach Report 12/2006, pp. 701–702](https://ems.press/content/serial-article-files/46044), including its highlighted two-dimensional case.

The construction is probabilistic. It does not provide a small facet list. An explicit finite parameter choice below makes the positive-probability argument quantitative, without generating or searching a large complex.

## 2. Established ingredients

We use the following three classical/recent ingredients, with their contribution boundaries explicit.

1. **Affine van Kampen–Flores.** Every seven points in $\mathbb R^4$ in general position contain two disjoint triples whose convex hulls meet. This follows from the nonembeddability of the two-skeleton of the six-simplex in $\mathbb R^4$, or from the affine van Kampen–Flores theorem. See also the balanced-Radon-pair discussion in Newman, [*Linear embeddings of random complexes*](https://arxiv.org/pdf/2212.09576), Section 4, especially Corollary 10.
2. **Order-type bound.** For $n$ labeled points in general position in $\mathbb R^4$, there are at most $n^{20n}$ relevant order types. The order type determines which disjoint triples have intersecting convex hulls. See Goodman–Pollack's enumeration theorem, restated as Theorem 11 and Lemma 12 in the same Newman paper.
3. **PL inflation.** Every linear 4-uniform hypergraph generates a simplicial complex PL embeddable in $\mathbb R^3$. Here “linear hypergraph” means that two distinct hyperedges intersect in at most one vertex. This is the $d=3$ case of Lee–Nevo, [*On colorings of hypergraphs embeddable in $\mathbb R^d$*, Lemma 3.1](https://arxiv.org/pdf/2307.14195), [published version](https://doi.org/10.1007/s00454-026-00856-4).

We also use the standard Janson lower-tail bound. If $Z$ counts subsets present in an independent Bernoulli sample, $\mu=\mathbb EZ$, and $\Delta$ sums $\mathbb E[I_aI_b]$ over **ordered distinct** dependent pairs of indicators, then

$$\mathbb P(Z=0)\le \exp\!\left(-\frac{\mu^2}{2(\mu+\Delta)}\right). \tag{1}$$

Equivalently one can include diagonal pairs in the denominator. See Frieze–Karoński, [*Introduction to Random Graphs*](https://www.math.cmu.edu/~af1p/BOOK.pdf), Section 34.6, Theorem 34.13, equation (34.36) in the current author-hosted version; Newman also states and uses this inequality in Theorem 14. Our Bernoulli variables are whole triangles, so indicators are independent unless they share a triangle, even if their triangles share individual vertices or edges.

The new candidate step is the deletion-robust combination of these ingredients. Newman's published random-complex separation alone concerns PL and linear embeddings in the same even ambient dimension; it does not by itself supply the gap of two asserted here.

## 3. Many forbidden pairs in every placement

Let $\mathcal T=\binom{[n]}3$ and $M=|\mathcal T|$. Fix a general-position labeled placement $\pi:[n]\to\mathbb R^4$. Let $\mathcal W_\pi$ be the family of unordered pairs $\{\sigma,\tau\}$ of disjoint triples whose convex hulls intersect in this placement.

Every seven-element vertex set contains at least one such pair. Each pair uses six vertices and is contained in exactly $n-6$ seven-element sets. Double counting therefore gives

$$
|\mathcal W_\pi|\ge \frac{\binom n7}{n-6}
=\frac17\binom n6. \tag{2}
$$

Every triangle belongs to at most $M$ pairs in $\mathcal W_\pi$.

Let $m=n^{5/4}$, taking $n$ to be a fourth power, and let $F\subseteq\mathcal T$ be any set with $|F|\le m$. Remove from $\mathcal W_\pi$ all pairs incident with $F$, leaving $\mathcal W_{\pi,F}$. Uniformly in both $\pi$ and $F$,

$$
|\mathcal W_{\pi,F}|
\ge\frac17\binom n6-mM.
$$

For $n\ge12$, $\binom n6\ge(n/2)^6/720$ and $M\le n^3/6$. Thus, provided $n^{7/4}\ge107520$,

$$
|\mathcal W_{\pi,F}|\ge c n^6,
\qquad c:=\frac1{645120}. \tag{3}
$$

Indeed, the first term is at least $n^6/322560$, and the removed term is at most $n^{17/4}/6\le n^6/645120$.

## 4. A random family remains nonembeddable after every small deletion

Select every triangle in $\mathcal T$ independently with probability

$$p=n^{-3/2},$$

and denote the selected family by $\mathcal H$. For fixed $\pi,F$, let $Z_{\pi,F}$ count those pairs in $\mathcal W_{\pi,F}$ for which both triangles lie in $\mathcal H$.

Its mean satisfies

$$\mu_{\pi,F}=|\mathcal W_{\pi,F}|p^2\ge c n^3. \tag{4}$$

Two distinct indicators can be dependent only if the corresponding pairs share a triangle. There are at most $M^3$ ordered pairs of this kind: choose their common triangle and the other two triangles. Their joint expectation is $p^3$. Also $|\mathcal W_{\pi,F}|\le M^2/2$. Consequently

$$
\mu_{\pi,F}+\Delta_{\pi,F}
\le \frac{M^2p^2}{2}+M^3p^3
\le\frac{n^3}{72}+\frac{n^{9/2}}{216}
\le n^{9/2}. \tag{5}
$$

Equations (1), (4), and (5) give the uniform estimate

$$
\mathbb P(Z_{\pi,F}=0)
\le\exp(-a n^{3/2}),
\qquad a:=c^2/2. \tag{6}
$$

There are at most $n^{20n}$ relevant placements, and at most

$$\sum_{j=0}^{m}\binom Mj\le(m+1)M^m\le(m+1)n^{3m}$$

deletion sets of size at most $m$. The union bound yields

$$
\mathbb P\bigl(\exists\pi,F:\ Z_{\pi,F}=0\bigr)
\le (m+1)n^{20n+3m}\exp(-a n^{3/2})=o(1), \tag{7}
$$

because $n^{5/4}\log n=o(n^{3/2})$. Therefore, with probability tending to one, **every** deletion of at most $m$ triangles leaves a family that cannot be linearly embedded in $\mathbb R^4$.

Here (7) genuinely quantifies over deletion sets chosen after seeing the random sample. We do not assume that the eventual cleaning operation is independent of $\mathcal H$.

### Why generic placements suffice

If a finite complex has a linear embedding, sufficiently small perturbations of its vertex positions still give an embedding. One way to see this is to use all pairs of disjoint nonempty faces: their convex hulls are compact and disjoint, so their distances have a positive minimum over the finitely many pairs. Small perturbations preserve these disjointness relations. These relations also ensure injectivity on the whole complex: if two barycentric representations have the same image, cancel their common vertex coefficients; unless they represent the same point, this produces intersecting convex hulls of disjoint faces. In particular all simplices stay nondegenerate. An arbitrarily small generic perturbation is consequently possible.

Thus a putative nongeneric linear embedding would produce one of the generic placements forbidden in (7).

## 5. Cleaning makes the hypergraph linear

Let $B$ be the number of unordered pairs of selected distinct triangles sharing an edge. Such a pair is specified by its common edge and two distinct additional vertices. Hence

$$
\mathbb EB=\binom n2\binom{n-2}2p^2\le n/4.
$$

Markov's inequality gives

$$\mathbb P(B>m)\le\frac{n}{4m}=\frac1{4n^{1/4}}=o(1). \tag{8}$$

When $B\le m$, choose one triangle from each offending pair and delete the union of all chosen triangles. The resulting deletion set $F$ has size at most $B\le m$ and meets every offending pair. Therefore $\mathcal H'=\mathcal H\setminus F$ is a linear 3-uniform hypergraph.

At the same time, (7) guarantees that the complex $K$ generated by $\mathcal H'$ cannot be linearly embedded in $\mathbb R^4$.

We can also ensure that $K$ is nonplanar. The number $T=|\mathcal H|$ is binomial with mean

$$\lambda=Mp\sim n^{3/2}/6,$$

and variance at most $\lambda$. Chebyshev's inequality gives $\mathbb P(T<\lambda/2)\le4/\lambda=o(1)$. Since $m=o(\lambda)$, for sufficiently large $n$ one has

$$|\mathcal H'|\ge T-m>n. \tag{9}$$

Distinct retained triangles share no edge, so the one-skeleton of $K$ has exactly $3|\mathcal H'|>3n$ edges and at most $n$ vertices. It is not planar, by the planar graph edge bound. In particular $K$ has no PL embedding in $\mathbb R^2$.

The high-probability events (7)–(9) have a common realization. Fix one such realization and its cleaned family from now on.

## 6. The two exact embedding dimensions

The cleaned triangle family is linear: distinct facets meet in at most one vertex. The self-contained [first-subdivision lemma](PL_SUBDIVISION_LEMMA.md) gives a linear embedding of its abstract first barycentric subdivision in $\mathbb R^3$, hence $e_{\rm PL}(K)\le3$. This also directly satisfies the original OWR derived-complex convention. It independently verifies the special case supplied by Lee–Nevo's Lemma 3.1 after adjoining one private apex to each triangle; no novelty for this auxiliary lemma is asserted. The supplement handles original vertex labels, all face intersections, angular separation at shared vertices, isolated vertices and cyclic incidence graphs.

By the nonplanarity established in (9), $e_{\rm PL}(K)\ge3$. Hence

$$e_{\rm PL}(K)=3.$$

Equation (7) gives $e_{\rm lin}(K)\ge5$. Conversely, every finite two-dimensional complex embeds linearly in $\mathbb R^5$: place its vertices on the five-dimensional moment curve. Any six vertices are affinely independent, so any two triangles meet precisely in their common face. Therefore

$$e_{\rm lin}(K)=5,$$

which proves the theorem.

## 7. An explicit finite choice and a small exact certificate

One may take

$$n=2^{256},\qquad p=2^{-384},\qquad m=2^{320}.$$

This is only an existence parameter; no sample of this size is generated.

Since $645120<2^{20}$, one has $a>2^{-41}$ and $a n^{3/2}>2^{343}$. Using $\log n<256$,

$$
\log\bigl((m+1)n^{20n+3m}\bigr)
<770m+5120n<2^{331}.
$$

The failure probability in (7) is thus below $\exp(-2^{342})<1/8$. The bound in (8) is $2^{-66}$. Finally $\lambda\ge n^{3/2}/24>2^{379}$, so Chebyshev's failure probability is below $2^{-377}$; also $\lambda/2-m>n$. The sum of these three failure bounds is less than one, proving existence for this explicit $n$.

`check_bounds.py` verifies the displayed rational/integer inequalities using the standard library. It does not enumerate complexes, simulate the construction, or certify the imported geometric and probability theorems.

## 8. Scope and attribution

This proof concerns finite abstract simplicial complexes and their original triangulations. It does not claim the same separation for a manifold, a fixed small vertex count, or a prescribed embedding. The retained triangles meet at most at vertices, and the complex is typically not a manifold.

The affine van Kampen–Flores obstruction, order-type counting, Janson inequality, random nonembedding method, and PL inflation lemma are imported and credited. The candidate contribution is the robust cleaning argument that combines linear-hypergraph PL embeddability in dimension three with a uniform obstruction to linear embeddability in dimension four. Two independent full primary-source priority families found no subsuming result in their bounded corpus; global priority is not proved. The relevant Lee–Nevo lemma was already public in July2023. Three independent mathematical/source families pass this chain. The current [priority assessment](PRIORITY_ASSESSMENT.md) records known ingredients and access limits; fresh publication-package reviews remain required before acceptance/publication. The earlier exact-hash review remains historical and is not transferred to modified files.

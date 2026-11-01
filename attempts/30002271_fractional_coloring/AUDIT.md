# Prior-resolution audit: averaged local fractional coloring

Problem ID **30002271**, OWR-12330-013 (row 1910). Disposition: **already_solved1**. This is an original exposition and verification of a previously published affirmative example, not a new mathematical result.

## Target and attribution

For a nonempty finite simple graph, put N[u]={u}∪N(u), ω_v=ω(G[N[v]]), γ(v)=(d(v)+1+ω_v)/2, and A(G)=max_u (Σ_{v∈N[u]}γ(v))/(d(u)+1). The exact target asks whether **there exists** such a graph with χ_f(G)>A(G). No ceiling is applied, and no maximum over subgraphs is present.

Andrew D. King, joint work with Katherine Edwards, *Getting to the point of Reed’s Conjecture: How local can you go?*, in *Graph Theory*, Oberwolfach Report 02/2013, pp.103–105, poses this question on p.104 and supplies the affirmative construction on p.105. Credit belongs to that prior source. See [official report](https://ems.press/journals/owr/articles/12330), DOI 10.4171/OWR/2013/02, and [official PDF](https://ems.press/content/serial-article-files/46434).

Katherine Edwards and Andrew D. King, [*A superlocal version of Reed’s Conjecture*, arXiv:1208.5188v2](https://arxiv.org/abs/1208.5188v2), §6, p.15, repeats the calculation and explicitly gives k>4. Its unrounded parameter is denoted γ′ℓ. These source facts identify prior resolution; the arguments below independently verify the mathematics. No claim is made about which publication first discovered the construction.

## Construction and fractional chromatic number

Fix an integer k≥2. Take a core C={c_0,…,c_{k−1}} inducing K_k. For each c_i add k distinct leaves, each adjacent only to c_i. There are k(k+1) vertices and k(k−1)/2+k² edges.

Every fractional coloring has total weight at least k: an independent set contains at most one core vertex, so summing the coverage requirements over C gives that lower bound. Conversely color c_i with color i, and all its leaves with color i+1 modulo k. This is a proper k-coloring because k≥2. Its color classes, each assigned weight one, form a feasible fractional coloring. Consequently χ_f(G_k)=χ(G_k)=k. This does not rely on a numerical LP approximation or on a perfect-graph theorem.

## Local quantities and both vertex types

A core vertex has degree 2k−1. Its closed neighborhood consists of all k core vertices and its own k leaves. The largest clique there has size k: a clique using a leaf has size at most two, and k≥2. Therefore γ(c_i)=((2k−1)+1+k)/2=3k/2.

A leaf has degree one and its closed neighborhood is an edge, so γ(leaf)=(1+1+2)/2=2. The two types of neighborhood average must both be checked because the target uses a maximum over all vertices.

For a core vertex, the average is [k(3k/2)+k·2]/(2k)=3k/4+1. For a leaf it is [(3k/2)+2]/2=3k/4+1. Thus A(G_k)=3k/4+1 and χ_f(G_k)−A(G_k)=(k−4)/4.

It follows that every integer k≥5 yields a strict example. The smallest member of this particular family that works is k=5: 30 vertices, 35 edges, χ_f=5, A=19/4, and gap 1/4. This is not a claim of minimum order among all counterexamples. For k=4 there is equality, while k=2,3 do not work. The k=1 construction is K₂, whose fractional chromatic number and neighborhood average are both 2; extending χ_f=k or γ(core)=3k/2 to that exceptional case is incorrect. The empty k=0 construction is excluded by the nonempty target and undefined maximum.

## Scope safeguards

1. **Maximal-clique averages are different.** For k≥2 the maximal cliques are the core and each pendant edge. The core average is 3k/2, while a pendant edge average is 3k/4+1. Their maximum is 3k/2≥k. This family does not contradict the intended maximal-clique upper bound. The distinct OWR Conjecture 7 has a printed direction inconsistent with its intended bound; Edwards–King Conjecture 4 supplies the upper-bound direction. No resolution of that conjecture is claimed.
2. **An outer maximum over subgraphs is different.** In the induced core H=K_k, recomputed degrees are k−1, local clique numbers are k, and all γ_H(v)=k. Hence the outer-subgraph maximum is at least k=χ_f(G_k); this example cannot refute that variant. Reusing degrees from the ambient graph when evaluating H would be a different statement.
3. **Vertex-specific fractional demands are different.** Demand bounds of the form f(v)≤2/(d(v)+1+ω_v)=1/γ(v) do not assert the neighborhood-average inequality above. No conclusion about a universal local-demand conjecture follows from this audit.
4. Changing closed to open neighborhoods, rounding γ, restricting the maximum to selected vertices, or changing the number of attached leaves changes the target or the calculation.

## Reproducible verification and limits

Run `python check_exact.py` from this directory. The checker builds graphs from adjacency lists for each k=1,…,12. It uses generic pivoted Bron–Kerbosch enumeration for maximal cliques of the graph and its complement, computes every local clique number and neighborhood average with exact rational arithmetic, checks a proper-coloring primal certificate and nonnegative fractional-coloring dual certificate against all maximal independent sets, and verifies the strict threshold and maximal-clique variant. Nonnegative dual weights make checking maximal independent sets sufficient for all independent sets. Results are in EXACT_CHECKS.json. Normal and Python optimized-mode runs produced byte-identical output; explicit exceptions, not removable assertions, enforce checks.

These finite checks corroborate but do not replace the all-k proof. The accompanying independent review checks boundary cases, quantifiers, and nearby variants. Source text/PDFs, datasets, private coordination, and unrelated records are not included. No repository publication or queue edit is part of this audit. No exhaustive literature or present-status claim is made for distinct conjectures.

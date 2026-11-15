# A fixed birational map without a prime-field cycle-distribution limit

Alec Kriebel · [ORCID](https://orcid.org/0009-0001-9320-500X) · Version 1.1 · 21 October 2026

Unrefereed preprint; version 1.1. Developed with extensive AI assistance; no external human or journal peer review, journal acceptance or formal proof-assistant certification is claimed.

[Zenodo DOI](https://doi.org/10.5281/zenodo.23539734)

## Original abstract

For the fixed birational map L(u,v)=(u,(u^2+1)v), reduction at every prime p≡3(mod 4) permutes all of F_p^2. Its point-weighted distribution of periods divided by p has no limit. At every fixed 1/2≤ x<1, the distribution function is 1-φ(p-1)/(p-1)+o(1), with limsup 1 and liminf at most 23/24. Moreover, neither these distribution-function values nor the period measures converge on any further prime subset of positive upper relative density. The latter statement uses the classical continuous empirical law for φ(p-1)/(p-1). A supplementary proposition treats all odd primes on the invariant regular domain, and under uniform-point deletion or arbitrary exceptional-period completion. These conventions cannot restore convergence on any positive-upper-density prime selection. The contribution is a precisely delimited application to the broad existence assertion in the 2004 Oberwolfach problem on finite-field maps. The triangular family, primitive-value estimates, totient mean and scalar distribution law are established ingredients; no new arithmetic theorem or historical firstness is claimed.

## The idea in plain English

A finite field has only finitely many points, so a permutation eventually repeats every point. One can record the number of steps in each point’s cycle, divide that period by the prime, and ask whether the distribution settles as the prime grows.

This paper studies one fixed map, L(u,v)=(u,(u²+1)v). For primes congruent to 3 modulo 4 it permutes the whole affine plane. Its period distribution keeps changing, even after restricting to any further collection of these primes with positive upper relative density.

The obstruction comes from the classical arithmetic quantity φ(p−1)/(p−1), the proportion of generators of a cyclic group of order p−1. An exact fiber count connects that quantity to the point-period distribution. A separate result shows that changing only the exceptional fibers at other odd primes cannot remove the obstruction under the stated uniform-point conventions.

## The precise result

Set L(u,v)=(u,(u²+1)v), with rational inverse L⁻¹(u,v)=(u,v/(u²+1)). It is a fixed infinite-order birational map over Q with invariant u and genus-zero generic invariant fibers. Put S={p prime : p≡3 (mod 4)}. For every p in S the reduction permutes all of F_p². If T_p(z) is a point’s least positive period, define μ_p=(1/p²)Σ_{z∈F_p²}δ_{T_p(z)/p} and D_p(x)=μ_p([0,x]). These are uniform point weights and normalization by p.

Theorem 1(i). Put θ_p=φ(p−1)/(p−1). For each fixed x∈[1/2,1), eventually as p tends to infinity in S, |D_p(x)−(1−θ_p)|≤1/p+64p^(−1/4). In particular D_p(x)=1−θ_p+o(1). The exact fiber identity is D_p(x)=1−(p−1)P_p/p² once p(1−x)>1, where P_p counts u for which u²+1 has multiplicative order p−1.

Theorem 1(ii). For every such fixed x, limsup_{p→∞, p∈S}D_p(x)=1 and liminf_{p→∞, p∈S}D_p(x)≤23/24.

Theorem 1(iii). For every A⊆S satisfying limsup_{X→∞} #{p≤X:p∈A}/#{p≤X:p∈S}>0, D_p(x) does not converge along A for any fixed x∈[1/2,1). The probability measures μ_p do not converge weakly along A either. Since S has density 1/2 among the primes, the stated relative-density condition also gives positive upper density among all primes.

Proposition 4. For every odd prime p, set N=p−1, θ_p=φ(N)/N, r_p=#{u∈F_p:u²+1=0}∈{0,2}, and Ω_p={(u,v)∈F_p²:u²+1≠0}. Its size is p(p−r_p), and L permutes Ω_p. Here P_p counts nonzero primitive multipliers u²+1. Uniformly through all odd primes, |P_p/p−θ_p|≤r_pθ_p/p+θ_p(2^ω(N)−1)/√p≤2/p+64p^(−1/4)=o(1), where ω(N) is the number of distinct prime divisors of N.

Give every point of Ω_p equal weight 1/[p(p−r_p)] and divide its least period by p to obtain μ_p^reg. For fixed x∈[1/2,1) with p(1−x)>1, D_p^reg(x)=1−(p−1)P_p/[p(p−r_p)]=1−θ_p+o(1). With the globally bounded continuous ramp h(t)=max{0,min{1,2t−1}} on [0,∞), ∫h dμ_p^reg=(1−2/p)(p−1)P_p/[p(p−r_p)]=θ_p+o(1).

The same asymptotics hold under every following convention: retain all regular points, delete any subset of the exceptional fibers, give every remaining exceptional point an arbitrary finite nonnegative assigned period, and renormalize uniform point weights. This includes deleting all exceptional fibers, deleting only their nonperiodic points, and completing all p² affine points. Assigned periods can exceed p; the completed probability measures live on [0,∞).

Under every one of these conventions, the CDF at each fixed x∈[1/2,1) and the period measures fail to converge along every prime set of positive upper density relative to all primes. Only exceptional points vary: their retained mass is at most r_p/p≤2/p, so every [0,1]-valued statistic changes by at most 2/p. The explicit limsup/liminf in Theorem 1 remains the full-affine class-3 statement.

## Why the result holds

The first coordinate is fixed. On each regular vertical fiber, the map multiplies the second coordinate by u²+1. The zero section has period one; every nonzero point has the multiplier’s multiplicative order. Every proper divisor of p−1 lies below p/2, so at the stated fixed thresholds only primitive multiplier fibers are excluded.

A classical primitive-element character indicator and quadratic character-sum estimate compare the number of primitive fibers with pθ_p. Classical shifted-prime arithmetic then supplies incompatible subsequences and the displayed limsup/liminf bound.

The stronger statement about every positive-upper-density selection uses the established atomless empirical law of θ_p. A convergent selection of positive upper density would force an atom at its limit. The ramp h extracts θ_p+o(1) as a bounded continuous moment, so the same obstruction rules out weak convergence. The infinite-prime conclusions follow from this proof and its explicit classical inputs; finite checks in the package are supplementary.

## Scope and limitations

The inverse is rational, not a complex polynomial inverse, and the invariant fibers have genus zero. The result addresses the broad birational existence assertion written in the 2004 Oberwolfach problem. It does not settle narrower genus-one or polynomial-automorphism questions, or the source’s separate prime-averaged statistic normalized by p².

All CDF conclusions use a fixed x∈[1/2,1). The exact identity requires p(1−x)>1; it is not uniform for moving x approaching 1. Uniform point weights cannot be replaced by equal cycle weights. No prohibition on convergent arbitrary zero-density prime selections is claimed.

At primes congruent to 1 modulo 4, L is not a full-affine permutation. Proposition 4 retains every regular point and its uniform weight, and changes only exceptional points under the stated deletion/assignment conventions. It does not cover deleting regular points, general reweighting, negative assigned periods or stability of unbounded moments.

The triangular map family, primitive-value character method, shifted-prime totient mean and scalar empirical law are established work. The contribution is the precisely delimited application and its proof for this map and statistic. A bounded primary-source comparison does not certify a new map family, new arithmetic theorem, historical firstness, exhaustive novelty or current worldwide openness.

A specific historical limit remains: Roberts’s 2011 reference 9 cites N. Neumärker, J. A. G. Roberts, C.-M. Viallet and F. Vivaldi, The dynamics of reversible birational maps over finite fields, UNSW Preprint (2011). Its body and version relationships remain unrecovered. Its unseen contents cannot establish either prior coverage or absence of this exact application. An authenticated earlier statement would require reconciliation of the historical description.

## Prior work

[F. Vivaldi, joint work with J. A. G. Roberts, Maps over finite fields: integrability and reversibility, OWR 54/2004, pp.2944–2945](https://doi.org/10.4171/OWR/2004/54). The broad birational existence assertion and point-weighted T/p statistic. The later genus-one heuristic and Conjecture 2 use different scope.

[A. Ostafe and I. E. Shparlinski, On the degree growth in some polynomial dynamical systems and nonlinear pseudorandom number generators, arXiv:0902.3884v3 (2009), §2.1](https://arxiv.org/abs/0902.3884v3). The older triangular polynomial family contains the displayed map after exchanging coordinates.

[A. R. Booker, S. D. Cohen, N. Sutherland and T. Trudgian, Primitive values of quadratic polynomials in a finite field, arXiv:1803.01435v2 (2018), §2](https://arxiv.org/abs/1803.01435v2). Classical primitive-value character framework, equations (5)–(6) and Lemma 1.

[L. Menici and C. Pehlivan, Average r-rank Artin conjecture, Acta Arithmetica 174(3) (2016), 255–276](https://doi.org/10.4064/aa8258-4-2016). The unconditional shifted-prime mean, with r=m=1 in Lemma 2. This is not the fixed-base primitive-root conjecture.

[J.-M. Deshouillers and M. Hassani, A note on the distribution function of φ(p−1)/(p−1), J. Aust. Math. Soc.93 (2012), 77–83; online 16 January 2013](https://doi.org/10.1017/S1446788712000250). The continuous shifted-prime scalar empirical law, associated with Kátai; Proposition 2.1 and its m=2 application.

[S. Aivazidis and E. Sofos, On the distribution of the density of maximal order elements in general linear groups, arXiv:1308.5701v2 (2014)](https://arxiv.org/abs/1308.5701v2). The n=1 mean and continuous law in Theorems 1.1(i) and 1.3(i), including the prime/prime-power relation in §6. Standard Dirichlet, prime number theorem and Siegel–Walfisz inputs are explicitly used.

[J. A. G. Roberts, Order and symmetry in birational difference equations and their signatures over finite phase spaces, Vigo proceedings (2011), pp.213–221](https://www.dma.uvigo.es/~eliz/pdf/Roberts.pdf). Printed p.220, reference 9, authenticates the unresolved four-author 2011 preprint citation. The cited preprint body remains unrecovered.

## Paper and supporting materials

Read the complete eight-page published preprint in the on-page PDF reader.

[Open complete PDF](fixed-birational-cycle-nonlimit.pdf) · [Download complete PDF](fixed-birational-cycle-nonlimit.pdf) · [Zenodo original PDF](https://zenodo.org/records/23539734/files/fixed-birational-cycle-nonlimit.pdf)

[Download complete original ZIP](fixed-birational-cycle-nonlimit-verification.zip) · [Zenodo original ZIP](https://zenodo.org/records/23539734/files/fixed-birational-cycle-nonlimit-verification.zip) · [Download BibTeX](citation.bib)

## Edition and rights

The manuscript and Zenodo’s declared publication date are 21 October 2026, version 1.1. Zenodo created and updated this record on that date UTC. The native versions response contains one record; the label 1.1 alone does not authenticate an earlier deposited edition or establish historical priority.

Authored text and code: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Third-party cited works retain their own rights.

## AI use and review status

AI systems were used extensively in research, mathematical model and proof development, computation, literature investigation, writing and internal adversarial verification. This is an unrefereed preprint. Internal AI reviews are not independent human or journal peer review; no journal acceptance or formal proof-assistant certification is claimed. The named author is responsible for the claims, materials and citations.

## Collaboration

Substantive collaboration on independent verification, a meaningful mathematical extension, or development of a journal submission is welcome. Authorship and responsibilities would be discussed by mutual agreement and would reflect actual research and writing contributions.

## Citation

Alec Kriebel. A fixed birational map without a prime-field cycle-distribution limit. Version 1.1, 21 October 2026. Unrefereed preprint. [doi:10.5281/zenodo.23539734](https://doi.org/10.5281/zenodo.23539734).

```bibtex
@misc{Kriebel2026BirationalCycleNonlimit,
  author = {Kriebel, Alec},
  title = {A fixed birational map without a prime-field cycle-distribution limit},
  year = {2026},
  month = oct,
  day = {21},
  version = {1.1},
  doi = {10.5281/zenodo.23539734},
  url = {https://doi.org/10.5281/zenodo.23539734},
  note = {Unrefereed preprint, version 1.1, dated 21 October 2026. Developed with extensive AI assistance.}
}
```

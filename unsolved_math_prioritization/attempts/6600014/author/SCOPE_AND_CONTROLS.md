# Scope controls and complete elementary checks

These checks guard against changing the mathematical question. They are not attempted counterexamples to its now-resolved planar statement, and carry no novelty claim.

## 1. Arbitrary Delone sets and repetitivity

Rectifiability is the existence of a bi-Lipschitz bijection to the standard lattice. An ambient rectification necessarily restricts to such a bijection. Therefore a nonrectifiable Delone set cannot be an input to Navas's question.

Nonrectifiable planar Delone sets exist even with repetitivity, as proved by María Isabel Cortez and Andrés Navas, *Some examples of repetitive, nonrectifiable Delone sets*, Geometry & Topology 20 (2016), 1909–1939, DOI [10.2140/gt.2016.20.1909](https://doi.org/10.2140/gt.2016.20.1909). This is an external literature control; no reconstruction of their counterexamples is claimed here.

Repetitivity means that each finite-radius patch recurs, up to translation, inside every sufficiently large ball. Linear repetitivity requires the necessary ball radius to be bounded linearly in the patch radius (in the usual large-radius formulation). Navas's earlier 2016 note proves ambient rectification for linearly repetitive Delone sets in every dimension, and also explains the Burago–Kleiner sufficient condition. That earlier theorem is a genuine special case, not by itself the full original answer. See [DOI 10.1016/j.crma.2016.08.010](https://doi.org/10.1016/j.crma.2016.08.010), published pages 976–977.

## 2. Bounded displacement cannot be inserted

Let D=2Z². It is Delone, and A(x)=x/2 is a 2-bi-Lipschitz ambient map carrying D onto Z². Nevertheless no bijection φ:D→Z² has uniformly bounded displacement in these fixed coordinates.

**Proof.** Suppose |φ(d)−d|≤M for every d. Every lattice point z∈Z²∩[−n,n]² then has its preimage in 2Z²∩[−n−M,n+M]². Thus

    (2n+1)² ≤ (2 floor((n+M)/2)+1)² ≤ (n+M+1)².

Choose an integer n>M. The last inequality is impossible since 2n+1>n+M+1. ∎

This does not contradict Navas's use of bounded displacement **after** a suitable ambient change of coordinates. It rules out assuming that the original given set must already have a bounded-displacement bijection to the fixed Z².

## 3. Homogeneity or origin fixing cannot be inserted

Let a=(1/2,0) and D=Z²+a. Translation A(x)=x−a is an ambient isometry satisfying A(D)=Z². However no injective ambient map F with F(0)=0 can satisfy F(D)=Z²: the unique preimage of 0 under F would be 0, which is not in D.

In particular a positively homogeneous injective map, satisfying F(tx)=tF(x) for all t>0, cannot work for this D. Substituting x=0 and t=2 gives F(0)=0. This is an exact obstruction to an added homogeneity requirement, not to ambient rectification.

## 4. A specified equivariance cannot be inserted

Suppose the extra demand were F(x+z)=F(x)+z for all z∈Z² and x∈R². For D=2Z², such a map would obey

    F(D)=F(0)+2Z².

If this equalled Z², then 0∈F(D) would force F(0)∈2Z², hence F(D)=2Z², which omits (1,0). Contradiction. Yet the dilation from §2 gives an ambient rectification. This only rules out the particular unit-translation equivariance just specified; it does not rule out conjugating actions or other meanings of equivariance.

## 5. A prescribed-map theorem is dimension-sensitive

Define f:Z→Z by f(0)=1, f(1)=0, and f(n)=n otherwise. This is a 2-bi-Lipschitz bijection. To prove the upper inequality, if neither point is swapped its distance is unchanged; if both are swapped the distance remains 1; if exactly one is swapped, the distance changes by at most 1, and the original integer distance is at least 1. Since f=f⁻¹, the same upper estimate implies the lower inequality.

There is no continuous injective extension H:R→R. Indeed H(−1)=−1, H(0)=1, and H(1)=0. The intermediate value theorem makes 1/2 occur at a point in (−1,0) and also at a point in (0,1), contrary to injectivity. Thus replacing the planar prescribed-map theorem by an all-dimensional assertion including dimension one is false.

This is different from the one-dimensional **existence-of-some-map** question. Every Delone D⊂R can be enumerated increasingly as (x_n) indexed by Z; separation r and covering radius R give r≤x_(n+1)−x_n≤2R. Define A linearly between successive x_n with A(x_n)=n. Its positive slopes lie between 1/(2R) and 1/r. Splitting any interval at the finitely many x_n it crosses proves the same global upper and lower slope bounds. The map tends to both ends of R and is onto, so it is bi-Lipschitz and A(D)=Z.

Consequently an introductory phrase in the 2016 collection asserting nonrectifiable Delone sets in “any dimension” must not be read literally to include dimension one. The actual target problem is unambiguously planar.

## 6. Computation is auxiliary

`verify.py` checks the adjacent-swap inequalities on 820 integer pairs, 101 exact counting contradictions for bounded-displacement bounds M=0,...,100, a finite translation/inverse identity sample, and the arithmetic slack in the published constant. These finite checks supplement the complete general arguments above. They neither prove the extension theorem nor establish a universal theorem by sampling.

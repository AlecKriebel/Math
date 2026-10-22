# Kleiner's Problem 61: a marked-realization obstruction

**Problem:** 6200061 / AMR-061-0061, rank 810.  
**Outcome:** partial result; the general equality and existential attainment conjectures are not proved or disproved here.  
**Credit:** the problem is Bruce Kleiner's, recorded by Misha Kapovich. The distinction between Ahlfors-regular and equivariant conformal dimension is explicitly discussed by Hume, Mackay and Tessera. The arguments below are an authored elementary exposition and obstruction; no priority or novelty claim is made.

## 1. Scope and quantifiers

Write A(G) for the infimum of Hausdorff dimensions of Ahlfors-regular metrics in the quasisymmetric gauge of the boundary of a non-elementary hyperbolic group G. Write E(G) for the corresponding infimum over visual metrics on boundaries of proper geodesic hyperbolic spaces with a geometric G-action. Here geometric means isometric, proper and cocompact. This is the usual setting of the cited visual-boundary results; we do not exploit the source's abbreviated phrase “metric spaces” to allow pathological non-geodesic spaces.

Problem 61 asks whether A(G)=E(G). Its additional attainment question is understood as follows: if A(G) is attained within the Ahlfors-regular conformal gauge, does some geometric model have a visual metric of dimension A(G)? This is existential. It does not assert that every minimizing metric, with its given marking of the group action, is a visual metric.

Standard boundary theory gives A(G) <= E(G): a geometric action identifies its visual boundary quasisymmetrically with the group boundary, and a visual metric is Ahlfors regular. See Coornaert [C93] and Hume–Mackay–Tessera [HMT20, Definitions 12.4–12.5]. The missing implication is an upper bound E(G) <= A(G).

## 2. Visual metrics force each group element to be bilipschitz

**Lemma 1.** Let X be a proper geodesic hyperbolic space and let rho be a visual metric based at o, with parameter epsilon > 0 and comparison constant C >= 1:

C^(-1) exp(-epsilon (xi|eta)_o) <= rho(xi,eta) <= C exp(-epsilon (xi|eta)_o).

Every isometry g of X induces a bilipschitz map of (boundary X,rho).

**Proof.** The Gromov product changes by at most d(o,p) when its basepoint changes from o to p. This follows directly from the triangle inequality in the finite-point formula and passes to the boundary definition. Isometry invariance gives (g xi|g eta)_o=(xi|eta)_(g^(-1)o). Thus

C^(-2) exp(-epsilon d(o,g^(-1)o)) rho(xi,eta)
 <= rho(g xi,g eta)
 <= C^2 exp(epsilon d(o,g^(-1)o)) rho(xi,eta).

If another boundary-product convention introduces a bounded hyperbolicity error, it is absorbed in C. The constant may depend on g, which is enough here. QED.

**Corollary.** If a marked boundary metric d is equivariantly bilipschitz to a visual boundary metric, every group element acts bilipschitz on d. A non-Lipschitz element obstructs even this weakened marked realization.

## 3. An optimal Ahlfors-regular metric that fails marked realization

**Theorem 2.** For every closed orientable hyperbolic surface group Gamma, there is a metric d on its marked boundary such that:

1. d is quasisymmetrically equivalent to a standard visual metric;
2. d is Ahlfors 1-regular and attains A(Gamma)=1;
3. d is not equivariantly bilipschitz to any visual metric on the boundary of an isometric Gamma-action on a proper geodesic hyperbolic space.

This is an obstruction to an unnecessarily strong realization strategy, not a counterexample to Problem 61.

**Proof.** Realize Gamma as a cocompact torsion-free Fuchsian group acting on the upper half-plane. Its boundary is the extended real line R union {infinity}. Choose a nonidentity element. After conjugating the action and, if needed, replacing the element by its inverse, it has the form

g(x)=a x+b, where a>1 and b=a-1>0.

Indeed its two fixed points can be placed at -1 and infinity; its multiplier or that of its inverse is greater than one.

Use the chordal metric

q(x,y)=|x-y| / (sqrt(1+x^2) sqrt(1+y^2)),
q(x,infinity)=1/sqrt(1+x^2).

It is a standard visual metric of the hyperbolic plane. Define h(x)=x|x| and h(infinity)=infinity, and pull q back:

d(x,y)=q(h(x),h(y)).

This is a genuine metric, since h is a homeomorphism.

### Quasisymmetry, including the point at infinity

For finite x,y,

(1/2)|x-y|(|x|+|y|) <= |h(x)-h(y)| <= |x-y|(|x|+|y|).

For equal signs this is equality without the factor 1/2; for opposite signs it is the inequality between u^2+v^2 and (u+v)^2. If |x-y| <= t|x-z|, then

|x|+|y| <= 2|x|+t|x-z| <= (2+t)(|x|+|z|).

Consequently h is quasisymmetric on R with control 2t(2+t). Near infinity use the coordinate u=1/x. The coordinate expression of h is again u|u|, because 1/h(1/u)=u|u|. Away from 0 and infinity h is locally bilipschitz. In each of these local coordinates, q is bilipschitz equivalent to Euclidean distance.

For completeness, local quasisymmetry here gives global quasisymmetry on the compact circle. Choose a finite collection of these coordinate neighborhoods and a positive Lebesgue radius r for that cover. Triples with both comparison distances below r use one of finitely many local distortion functions. For triples with the denominator distance at least r and numerator at most t times that distance, uniform continuity bounds the image numerator by omega(t diam), while compactness and injectivity bound the image denominator below by a positive number m(r). This bound tends to zero with t. For any fixed t>1 the same argument uses denominator cutoff r/t. An increasing homeomorphism dominating these bounds is a global quasisymmetry control. Thus the identity from q to d is quasisymmetric, because its distances in the target equal those of h into q.

### Dimension and regularity

The map h is an isometry from (boundary Gamma,d) onto the chordal circle. Pulling back its arclength measure gives an Ahlfors 1-regular measure for d. Its Hausdorff dimension is 1. The topological dimension of a circle is 1 and is a lower bound for its Hausdorff dimension in any compatible metric; q itself gives the matching upper bound. Therefore A(Gamma)=1 and d attains it.

### Failure of Lipschitz continuity of a group element

For 0<t<=1, all numbers 0,t,b,b+at are nonnegative. Hence

d(0,t)=t^2/sqrt(1+t^4),

d(g0,gt)=(2ab t+a^2 t^2) /
 [sqrt(1+b^4) sqrt(1+(b+at)^4)].

Let R(t)=d(g0,gt)/d(0,t). Since t<=1,

R(t) >= [2ab / (sqrt(1+b^4) sqrt(1+(a+b)^4))] / t.

The bracket is strictly positive. Thus R(t) tends to infinity as t tends to zero, so g is not Lipschitz on d. Lemma 1 and its corollary rule out the claimed equivariant bilipschitz realization. QED.

**The marking matters.** Abstractly, (boundary Gamma,d) is isometric to a round circle and can certainly be a visual boundary. One can also conjugate the action by h. Neither observation supplies a bilipschitz *equivariant* identification for the original marked Gamma-action. Conversely, the original Fuchsian action already supplies some optimal visual metric q, so the existential conjecture holds for this group.

## 4. Exact certificate for a model calculation

For the illustrative affine map g(x)=2x+1, the squared ratio is exactly

R(t)^2 = 8(1+t)^2(1+t^4) / [t^2 (1+(1+2t)^4)].

This illustration is not an assertion that an arbitrary chosen surface contains an element with multiplier 2. The general proof above works for its actual multiplier a>1.

For 0<t<=1, t^2 R(t)^2 >= 4/41 follows after clearing positive denominators from

P(t)=82(1+t)^2(1+t^4) - (1+(1+2t)^4) >= 0.

In ascending monomial order its coefficients are

(80,156,58,-32,66,164,82).

Its degree-six Bernstein coefficients on [0,1] are

(80,106,2038/15,168,1026/5,282,574).

All are positive. Since the Bernstein basis polynomials are nonnegative on [0,1], this is an exact finite algebraic certificate of the inequality for the entire interval, not an inference from sample points. The included verifier independently expands the expression, converts its coefficients, and checks the certificate using rational arithmetic. Separately, it evaluates 80 dyadic samples as regression checks; those samples prove no general theorem.

## 5. An additive-defect lemma and the exact remaining obstruction

**Lemma 3.** Suppose d0 is a metric on a group G and there is a finite constant K such that

|d0(hx,hy)-d0(x,y)| <= K for all h,x,y in G.

Then D(x,y)=sup_h d0(hx,hy) is a finite left-invariant metric with d0<=D<=d0+K.

**Proof.** The bounds follow from the identity element and the hypothesis. Symmetry and the triangle inequality hold for every summand; taking a supremum preserves the needed triangle upper bound. Positivity follows from D>=d0. Left invariance follows by reindexing h -> hk. QED.

A bounded change in a metric changes each finite-point Gromov product by at most 3K/2. Thus whenever the relevant boundary definitions and visual structures apply, the corresponding exponential products are comparable by a fixed multiplicative constant. This explains why *uniform additive* equivariance would be useful.

We do not claim that every quasisymmetric filling supplies such a metric d0, nor that Lemma 3 alone gives a proper geodesic model with a geometric action. Both would require additional hypotheses or constructions. An arbitrary quasi-isometric conjugacy supplies multiplicative and additive coarse bounds, not the uniform additive hypothesis written above. Theorem 2 shows that a universal procedure preserving every supplied optimal marked boundary metric up to bilipschitz equivalence cannot work.

To resolve the original equality it would suffice, for every eta>0, to construct a genuine geometric model with visual dimension at most A(G)+eta. It may be necessary to replace a chosen near-minimizing gauge metric by a different metric of nearly the same dimension. To resolve the stronger attainment clause, the error must disappear when A(G) is attained. No such general construction is established here.

## 6. Standard positive controls and a rescaling pitfall

For the free group F_r, r>=2, the (2r)-regular Cayley tree has visual ultrametric rho_epsilon(xi,eta)=exp(-epsilon n), where n is common-prefix length. Every epsilon>0 is allowed. Each length-n cylinder, n>=1, has uniform boundary measure

mu(C_n)=1/[2r(2r-1)^(n-1)].

With Q=log(2r-1)/epsilon, its diameter to the Q power is (2r-1)^(-n); the ratio is the constant (2r-1)/(2r). Comparing arbitrary radii with consecutive cylinder radii proves Ahlfors Q-regularity. Letting epsilon grow gives A(F_r)=E(F_r)=0. Zero is not attained by an Ahlfors-regular metric on this infinite compact boundary: a finite 0-regular measure would assign a uniformly positive mass to every singleton by continuity from above, impossible for an infinite set. This is a standard example, not a new resolution.

For a group acting geometrically on real hyperbolic n-space, n>=2, the round boundary gives visual dimension n-1 and topological dimension gives the reverse lower bound. Thus A=E=n-1, attained. This includes the surface groups in Theorem 2.

Uniformly rescaling a geometric model does not by itself reduce the optimized visual dimension. If distances are multiplied by c>0, the growth exponent changes from v to v/c and the parameter describing the *same* visual metric changes from epsilon to epsilon/c. The dimension quotient v/epsilon is unchanged. Holding epsilon fixed while varying c assumes its admissibility anew and is not a general shortcut.

## References and status

Full public-source metadata and inspection scope are in SOURCES.json; no source PDFs or copied extracts are included.

- [K07] Misha Kapovich, Problems on Boundaries of Groups and Kleinian Groups, dated October 24, 2007; workshop collection from 2005; Problem 61, printed/PDF page 17. https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf
- [C93] Michel Coornaert, Mesures de Patterson-Sullivan sur le bord d'un espace hyperbolique au sens de Gromov, Pacific Journal of Mathematics 159 (1993), 241–270. https://doi.org/10.2140/pjm.1993.159.241
- [BS00] Mario Bonk and Oded Schramm, Embeddings of Gromov hyperbolic spaces, Geometric and Functional Analysis 10 (2000), 266–306. https://doi.org/10.1007/s000390050009
- [HMT20] David Hume, John M. Mackay and Romain Tessera, Poincare profiles of groups and spaces, Revista Matematica Iberoamericana 36 (2020), 1835–1886. Definitions 12.4–12.5 and the following discussion explicitly identify Kleiner's Problem 61. https://doi.org/10.4171/rmi/1184
- [HMT22] Same authors, Poincare profiles of Lie groups and a coarse geometric dichotomy, Geometric and Functional Analysis (2022). Section 5.3 distinguishes the two dimensions while improving profile bounds without the equivariance hypothesis. This bypass does not prove their equality. https://doi.org/10.1007/s00039-022-00617-4
- [HM25] David Hume and John M. Mackay, Connecting conformal dimension and Poincare profiles, arXiv:2511.10469 (2025 preprint), Questions 1.4–1.5 and Theorems 1.6–1.7. This concerns a profile critical exponent, not E(G). https://arxiv.org/abs/2511.10469

A targeted literature search through October 5, 2026 found no full resolution. This is a bounded search result, not a proof that none exists. The supplied catalog's earlier triage conflates the equality and attainment questions and invokes asymptotic dimension without an identified relevant theorem; neither is accepted here as proof or status authority.

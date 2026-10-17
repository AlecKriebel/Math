# Authored deduction from classical separated-condenser theory

This is an independently assembled mathematical implication, not a claim that any cited paper prints Hayman–Lingham Problem 7.58 or its resolution. It records a concrete prior-theorem mechanism for the zero-length branch. The original submitted proof is not modified by this note. Independent adversarial checking of this new assembly remains appropriate.

## Imported results and exact scope

Bagby's fundamental theorem identifies the transfinite logarithmic-energy modulus of a planar condenser with its conformal modulus. In its normalization, for disjoint nonempty compact plates A,B in the sphere, with connected complementary domain R,

    cap(R) = 2π / inf I(μ−ν),

where μ,ν range over probability measures on A,B and I is logarithmic energy. The zero or infinite endpoint interpretations are reciprocal. The definitions and fundamental theorem were inspected in the official IUMJ scan, especially printed pp.315–318 and323. The scan says1967; the publisher catalog/DOI labels the item1968. Both predate the target edition. [Official paper](https://www.iumj.indiana.edu/IUMJ/FTDLOAD/1968/17/17017/pdf).

Kallunki–Shanmugalingam Theorem1.1 concerns disjoint nonempty COMPACT subsets of a domain in a proper, ϕ-convex metric space with doubling measure and a (1,p)-Poincaré inequality, 1<p<∞. It identifies all-rectifiable-curve p-modulus with locally Lipschitz capacity. Euclidean R², Lebesgue area, Ω=R² and p=2 satisfy the assumptions. Definitions and theorem were inspected on printed pp.455–457. [Official paper](https://www.acadsci.fi/mathematica/Vol26/kallunki.pdf).

For the compact real plates used below, these results give the needed one-sided bridge

    M₂Γ(A,B;R²) ≥ cap(sphere\(A∪B)).

Here is a check of the bridge at infinity, rather than an unsupported application to touching plates. By Kallunki–Shanmugalingam, take bounded locally Lipschitz separating test functions with energy approaching the modulus, truncating to[0,1]. Make each function constant outside a large disk with a logarithmic radial cutoff. The cutoff energy tends to0; its gradient error is bounded by that energy, and the original gradient's tail tends to0. The altered function is a legitimate continuous ACL test function for Bagby's capacity, including near infinity, and retains both compact plate values. Hence Bagby's infimum does not exceed the modulus. Since A∪B is a bounded real set, its spherical complement is connected.

No result is applied directly with B=R\E.

## Zero-length implication

Let E⊂[0,1] be compact with one-dimensional Lebesgue measure0. Assume there is a probability measure μ on E with finite logarithmic energy. We show

    M₂Γ(E,R\E;R²) = ∞.

Take 0<ε<1/4 and let φε be the uniform probability density on[−ε,ε]. Put νε=μ*φε. This is an absolutely continuous probability measure supported on[−ε,1+ε], so νε(E)=0.

Use k(t)=log(4/|t|), which is nonnegative on the supports under consideration. Adding log4 does not change the energy of a signed measure of total mass0. For S uniform on[−ε,ε], or the difference of two independent such variables, its density is at most1/(2ε), and |S|≤2ε. For t≠0 the averaged kernel E[k(t+S)] tends to k(t). It is bounded by k(t)+C uniformly in ε: if |t|≥4ε, use |t+S|≥|t|/2; otherwise split off log(4/ε) and bound the positive integral of log(ε/|t+S|) by

    (2ε)⁻¹ ∫_{−ε}^{ε} log(ε/|r|) dr = 1.

Since |t|<4ε, log(4/ε)≤k(t)+log4. Finite energy makes μ nonatomic, so the diagonal has μ×μ measure0. Dominated convergence therefore gives

    I(μ,νε)→I(μ),  I(νε)→I(μ),
    I(μ−νε)→0.

For fixed ε let

    K_j = supp(νε) ∩ {x: dist(x,E)≥1/j},
    m_j = νε(K_j),  ν_{ε,j} = νε|K_j / m_j.

Discard indices with m_j=0. The compact sets K_j lie in the REAL complement F and increase to full νε measure, so m_j→1. The nonnegative kernel k and monotone convergence show that both self and mutual energies of these restrictions converge. Normalization then gives

    I(μ−ν_{ε,j})→I(μ−νε).

For any δ>0, first choose ε and then j so that I(μ−ν_{ε,j})<δ. This is a finite signed energy of separated compact plates E,K_j. Bagby's theorem and the bridge above yield

    M₂Γ(E,F) ≥ M₂Γ(E,K_j) ≥ 2π / I(μ−ν_{ε,j}) > 2π/δ.

Thus the modulus is infinite. The compact restriction is essential: it avoids replacing a separated-plate theorem by an unproved touching-plate assertion.

## Relation to the entire target, and boundary of the priority inference

Positive outer conformal capacity supplies a finite-log-energy probability on E by the classical condenser/logarithmic-capacity correspondence. One way to verify this bridge using Bagby's framework is to use R=B(0,2)\E with its exterior disk plate, move a point of R to infinity by a Möbius map, and apply finite transfinite modulus to get a finite-energy charge. The two transformed plates are separated compact sets, so finite signed energy forces each positive component's self-energy finite. Pullback to E changes the logarithmic kernel by bounded terms. The outer modulus is at most Bagby's Dirichlet capacity: every E-to-circle curve has a last-E/first-circle subcurve inside R, on which a smooth separating test function changes by1. Hence positive outer modulus forces positive capacity and finite transfinite modulus.

For a general compact E, the submitted proof first derives |E|=0 from a hypothetical finite E-to-F admissible density using an actual separating Sobolev potential and critical trace rigidity. The rigidity and trace theorems are classical; the pointwise-potential passage must still be checked with the actual plates. Combining that passage with the deduction above is an alternative assembly of the full result. This note does not independently certify that a single earlier theorem already states the ENTIRE target, and does not date the assembly as a published prior resolution.

The global/local rectifiability convention does not create a hidden gap in the implication above. Proving infinity for the globally rectifiable subfamily already forces infinity for the larger locally rectifiable endpoint family. If equivalence of the two outer moduli is needed, add an arbitrarily small multiple of w(z)=(1+|z|²)⁻¹ to any globally-rectifiable admissible density. This w is in L²(R²), is bounded below on each continuous curve's compact image, and gives infinite cost to every curve of infinite total length.

The appropriate priority consequence is positive overlap and a concrete classical corollary mechanism, not firstness, current openness, or a novelty certificate.

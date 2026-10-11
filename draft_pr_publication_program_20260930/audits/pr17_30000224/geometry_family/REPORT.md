# Independent geometric adversarial report: PR 17 / 30000224

Frozen head: `dae2b77074945443e1b91c92f641ff9feff12235`. Independent first pass began 2026-10-01 15:45 UTC. This report concerns Propositions 4.1 and 5.1 and the geometric linkage assertion in the frozen `PARTIAL_RESULTS.md`. No old review, review summary, sibling report, or root conclusion was consulted before the first-pass findings were sent to the parent.

## Verdict and exact scope

**Accept the two geometric obstructions as correct restricted results.** No fatal gap or counterexample was found. Proposition 4.1 excludes arbitrary, possibly nonhomogeneous, Cohen–Macaulay thickenings that contain `q=wz-xy`. Proposition 5.1 excludes homogeneous Cohen–Macaulay thickenings of generic multiplicity two; its multiplicity-one argument actually applies without homogeneity. Neither proposition resolves the original arbitrary-ideal question.

The original source really permits arbitrary ideals: [Singh–Walther, Question 3.6](https://arxiv.org/pdf/math/0701524), PDF page 8. This report verifies deductions, not novelty or the present global open-problem status.

| Claim / mechanism | Evidence and status | Exact boundary |
|---|---|---|
| Field extension preserves the hypotheses | Finite-type CM base change; explicit monomial injection for the toric prime; power sandwich for the radical | Generic length is preserved, so a length-two assumption survives extension |
| `q in b` forces `b` homogeneous | All-prime depth analysis; torsion-free S2 implies reflexive; height-one reconstruction forces a symbolic power | Requires the actual equation `q`, rather than merely a power of `q`, to vanish |
| `q in b` is impossible | Cartier divisor `rC` of type `(r,3r)`; nonzero deficiency of dimension `2r-1` | No restriction on homogeneity of the proposed `b` |
| A homogeneous length-two thickening is impossible | Primary contraction; torsion-free nilpotent line bundle; conormal `O(-7)^2`; at least 11 quadratic sections versus 10 ambient quadrics | Arithmetical CM and the quadratic restriction map use homogeneity |
| Skew-line/quartic linkage | New exact Groebner intersection and colon computations | Linkage itself does not preserve set-theoretic CMness |
| Homogenization cannot be assumed to preserve CM | Explicit flat same-radical family, with a CM general fiber and a non-CM special fiber | This is a counterexample to a general preservation step, not a counterexample to the Macaulay-curve obstruction |

## 1. Field and embedded-component checks

Put `A=K[s^4,s^3t,st^3,t^4]`. For any extension `K'/K`, its monomial basis remains linearly independent inside `K'[s,t]`. Flat base change of `0 -> a -> R -> A -> 0` therefore identifies `R'/aR'` with the same semigroup algebra over `K'`, which is a domain. Thus the toric prime remains prime, rather than merely becoming a reduced ideal with several components.

Because `R` is Noetherian and `sqrt(b)=a`, there is an integer `N` with `a^N subset b subset a`. After extension this yields `(aR')^N subset bR' subset aR'`; primeness of `aR'` proves radical equality. The CM property of a finite-type algebra is preserved under arbitrary field extension; a precise local formulation is [Stacks, Tag 045P](https://stacks.math.columbia.edu/tag/045P).

If generic length is assumed to be one or two, it remains so after extension. The map `R_a -> R'_(aR')` is flat, local, and has residue field `Frac(A')`. Tensoring a composition series of the finite-length localized quotient replaces every residue-field factor with one residue-field factor. This addresses the extra hypothesis needed in Proposition 5.1.

In fact the displayed geometric arguments already work over `K`: the quadric is split, the curve is explicitly `P^1_K`, and its line bundles are `O(e)`. Algebraic closure is harmless but unnecessary.

With the standard definition of a Cohen–Macaulay ring, every local ring of `R/b` is CM. If an associated prime were embedded, localization there would have depth zero and positive dimension, a contradiction. Since `a` is its only minimal prime, `Ass(R/b)={a}`, and `b` is `a`-primary. In particular,

`b = b R_a intersect R`.

This contraction excludes isolated or lower-dimensional components at the vertex and elsewhere. It is essential both for globalizing the generic length-two inclusion and for the unrestricted length-one exclusion.

## 2. Geometry of the reduced curve

On the Segre quadric write `(w,x,y,z)=(ac,ad,bc,bd)`. The curve has equation

`bc^3-ad^3=0`,

of bidegree `(1,3)`, and is the graph `([s^3:t^3],[s:t])`. Projection to the second factor is an inverse isomorphism to `P^1`. Consequently it is smooth and is a Cartier divisor of type `(1,3)`. The convention matters: `O_Q(u,v)|C` has degree `3u+v`, whereas `O_C(1)` has degree four. This also independently gives `N_(C/Q)=O(6)` and `N_(Q/P^3)|C=O(8)`.

The independent polynomial probe reconstructs the toric ideal

`a=(wz-xy, x^3-w^2y, wy^2-x^2z, y^3-xz^2)`.

This is not inferred from a finite range of degrees. Its exact Buchberger certificate gives a Groebner basis with minimal leading monomials `wz,w^2y,wy^2,xz^2`. Inclusion-exclusion gives the Hilbert series

`(1+2T+2T^2-T^3)/(1-T)^2`.

The image semigroup algebra has the same series: degree zero has dimension one, degree one dimension four, and every degree `d>=2` has dimension `4d+1`. Completeness in degree two is exact exponent enumeration; induction adds exponents zero and four to a full interval. A surjection between the two graded rings with equal Hilbert series is an isomorphism. Thus the finite Groebner certificate proves equality in every degree.

## 3. Proposition 4.1: arbitrary ideals containing the quadric

Assume `q in b`, and set `S=R/(q)`, `P=a/(q)`, `J=b/(q)`. The gradient of `q` is `(z,-y,-x,w)`, so the three-dimensional hypersurface `S` is regular away from its vertex. It is CM, satisfies S2, and is regular in codimension one; therefore it is normal. `P` has height one.

Here is the precise all-prime depth step omitted from the compressed exposition. Let `p` contain `P`, and put `h=ht_S(p)`. Since `S` is a finite-type hypersurface domain, it is excellent and catenary. Its dimension formula gives

`dim (S/J)_p = dim (S/P)_p = h-1`.

The quotient is CM by hypothesis, so its depth is `h-1`, while `depth S_p=h`. The local exact sequence `0 -> J_p -> S_p -> (S/J)_p -> 0` and the depth lemma give `depth J_p=h`. This includes `p=P` (`h=1`, quotient Artinian), height-two primes on the support, and all height-three primes, including the vertex. If `p` does not contain `P`, then `J_p=S_p` because the radical of `J` is `P`. Thus `J` is MCM everywhere, and in particular S2.

As a nonzero ideal in the normal domain, `J` is finite, torsion-free, and rank one. The exact equivalence between these conditions plus S2 and reflexivity, including reconstruction as a height-one intersection, is [Stacks, Tag 0AVB](https://stacks.math.columbia.edu/tag/0AVB). At `P`, the local ring is a DVR and `J_P=P^r S_P` for an integer `r>=1`. At every other height-one prime, `J` localizes to the full ring. Consequently

`J = S intersect P^r S_P = P^(r)`.

There is no residual ideal supported only at the vertex: such a correction would contradict the reflexive intersection equality.

The symbolic power is graded. One may prove this without assuming `J` graded: every scaling automorphism preserves `P`, its ordinary powers, its localization, and hence `P^(r)`. For a finite sum of homogeneous components of distinct degrees `d_i`, apply scalings `2^j`, for `0<=j<n`. The matrix `((2^d_i)^j)` is Vandermonde with distinct entries in characteristic zero, and inverting it shows every homogeneous component belongs to the ideal. The homogeneous preimage in `R` is exactly `b`.

The Cartier-divisor interpretation can also be checked on charts instead of assumed from reflexivity of a sheaf. On `S_w`, eliminate `z=xy/w` and put `F=x^3-w^2y`. The two other cubics become `-(y/w)F` and `-(y^2/w^2)F`, so `P_w=(F)`. Since

`S_w = K[w,w^-1,x,F]`,

`(F^r)` is `P_w`-primary and the localization of `P^(r)` is exactly `(F^r)`. The symmetric chart with `z` inverted gives the other end. These two charts cover `C` in projective space; away from `C` the ideal sheaf is the unit ideal. Thus the projective scheme really is the Cartier divisor `D=rC`, and its ideal on `Q` is `O_Q(-r,-3r)`. No embedded projective point is hidden in this step.

The quadric inclusion gives

`0 -> O_(P^3)(k-2) -> I_D(k) -> O_Q(k-r,k-3r) -> 0`.

Since both intermediate line-bundle cohomology groups on `P^3` vanish, at `k=r` the deficiency is exactly

`H^1(I_D(r)) = H^1(O_Q(0,-2r))`, with dimension `2r-1`.

There is an independent Cech explanation: for `O_(P^1)(n)`, first cohomology consists of Laurent exponents `n<j<0`. For `n=-2r` this is the interval `-2r+1,...,-1`. Tensoring with the single global section of `O(0)` gives precisely `2r-1` independent classes for every `r>=1`. This is a universal count; the probe's values `r=1,...,20` are checks only.

A homogeneous two-dimensional CM coordinate ring has `H^0_m=H^1_m=0`. The first vanishing makes its defining ideal saturated. The second gives surjectivity from each graded piece to the corresponding global sections and hence zero curve deficiency. The computed positive deficiency contradicts that CM consequence. Therefore Proposition 4.1 is valid even when `b` was initially nonhomogeneous.

## 4. Proposition 5.1: the homogeneous double obstruction

Generic multiplicity one is excluded without homogeneity: the localized length-one quotient forces `bR_a=aR_a`, and primary contraction gives `b=a`. The original reduced ring is not CM; equivalently its degree-one missing normalization monomial gives `H^1_m(A)=K(-1)`.

For generic multiplicity two, the maximal ideal of the localized Artinian quotient has square zero. Thus `a^2 R_a subset bR_a`. Primary contraction gives `a^2 subset b` globally. Homogeneity is now used to form the projective curve `Y=Proj(R/b)` with its embedded reduced curve `C` and coherent nilpotent ideal

`L=I_C/I_Y subset O_Y`.

The inclusion `a^2 subset b` makes `L` an `O_C`-module. At the generic point it is rank one: it is the unique one-dimensional nilpotent ideal in a local Artinian length-two algebra. It is torsion-free. Indeed a nonzero torsion subsheaf on the smooth integral curve would have finite support, and at a support point would give a nonzero finite-length submodule of `O_(Y,p)`. Such a submodule has a nonzero socle. This contradicts depth one of the local CM curve ring. A finite torsion-free rank-one module over a DVR is free, so `L` is a line bundle `O_(P^1)(e)`. This argument rules out embedded point modifications, rather than silently assuming a ribbon presentation.

The natural conormal surjection exists because `I_C^2 subset I_Y`:

`I_C/I_C^2 ->> L`.

The Euler-sequence identification with the Jacobian kernel is correct. Pullback of the Euler sequence on `P^3` has middle term `O(-4)^4`, while the Euler sequence on `P^1` has middle term `O(-1)^2`. Differentiating the degree-four parametrization gives the map between these middle terms. Contracting with `(s,t)` gives four times the parametrization, so the rightmost scalar map is invertible in characteristic zero. The kernel of the full Jacobian is therefore precisely the conormal kernel of `f^*Omega_(P^3) -> Omega_(P^1)`.

The new probe differentiates the parametrization and solves rational coefficient systems from scratch. The kernel dimensions for coefficient degrees `0,1,2,3` are `0,0,0,2`. Its two reconstructed cubic columns have no common rank-drop point: an exact univariate gcd of their minors on `t!=0` is constant, and one minor is nonzero at `t=0`. They furnish a global isomorphism from `O(-7)^2` to the conormal bundle. The endpoint Jacobian minors also certify surjectivity of the Jacobian. Hence

`N_C^* = O(-7)^2`.

As an additional geometric check, the differential of the quadric expressed in the displayed frozen cubic frame has coefficients `(t/2,s/2)`. Its two entries have no common zero, giving

`0 -> O(-8) -> O(-7)^2 -> O(-6) -> 0`.

This extension cannot split because `Hom(O(-6),O(-7)^2)=0`. It agrees with the expected normal sequence on a `(1,3)` curve and with the classical rational-quartic statement on printed page 463 of [Eisenbud–Van de Ven](https://eisenbud.github.io/papers/pdfs/1981-001.pdf). The explicit calculation, rather than that complex-geometry citation, supplies the field-uniform proof.

A surjection `O(-7)^2 -> O(e)` requires `e>=-7`: if `e<-7`, every map is zero because its coefficients would be sections of `O(e+7)` of negative degree. Twist `0 -> L -> O_Y -> O_C -> 0` by two. Since `O_C(2)=O(8)` and `e+8>=1`, the left term has vanishing first cohomology, so

`h^0(O_Y(2))=(e+9)+9=e+18>=11`.

The arithmetically CM coordinate ring has `H^1_m=0`, forcing the map `R_2 -> H^0(O_Y(2))` to be onto, with source of dimension ten. This contradiction proves Proposition 5.1. Local CM alone would not supply that surjectivity: the use of homogeneous arithmetic CM at this exact point must be retained.

## 5. An exact boundary test for homogenization

Consider `B=K[x,y,z]/(x^2,xy+z)`. Eliminate `z=-xy` to get `B=K[x,y]/(x^2)`, a one-dimensional CM ring with radical `(x,z)` in the original polynomial ring. Its highest-total-degree initial ideal is

`(x^2,xy,xz,z^2)`.

The extra generators follow from `x(xy+z)-y x^2=xz` and `z(xy+z)-y(xz)=z^2`; the exact degree-compatible Groebner certificate proves that they generate the complete initial ideal. The class of `x` survives but is killed by all three variables, so the special quotient has depth zero. Its radical is still `(x,z)`.

Explicitly, the full homogenized family is

`(x^2,xy+z tau,xz,z^2) subset K[x,y,z,tau]`.

Its Groebner basis has monic leading monomials `x^2,xy,xz,z^2`, independent of `tau`, so its standard monomials give a free `K[tau]`-basis. It is flat. The nonzero fibers are CM and the zero fiber is not, despite having the same radical throughout. Adjoining another free variable gives the same phenomenon in dimension two. Therefore even a flat same-radical degeneration supplies no general reduction from a nonhomogeneous CM thickening to a homogeneous CM thickening. This is an exact falsification of that tempting extra step.

## 6. Exact linkage statement and source caution

Let `I=(w,x) intersect (y,z)` and `g=wy^2-x^2z`. The new elimination/colon calculations prove

`I intersect a = (q,g)`,

`(q,g):wy = a`, and `a I subset (q,g)` with `wy notin a`.

Since `wy in I`, the last two statements give `(q,g):I=a`. The reverse colon is `I` as well. The certified intersection expresses `(q,g)` as `(w,x) intersect (y,z) intersect a`. The quartic prime is not contained in either line prime: `y^3-xz^2` is outside `(w,x)` and `x^3-w^2y` is outside `(y,z)`. Colon of a prime ideal by an ideal not contained in it returns that prime, whereas `a:a=R`. Taking the intersection therefore gives `(q,g):a=I`. Finally, `q` is prime and `g` is nonzero modulo `q`, so they are a regular sequence. Thus both directions of complete-intersection linkage are justified directly.

The Segre computation is exactly `g=ab(bc^3-ad^3)`. This agrees with the selected linkage in [Boix–Eghbali, Remark 5.7](https://arxiv.org/pdf/1806.04405), PDF page 18. It supplies no unconditional thickening theorem. In particular, the later phrase in their Remark 5.10 that the displayed quartic quotient is not reduced conflicts with its explicit toric prime; that phrase is not used here or in the geometric obstructions.

## Reproducibility, strongest result, and remaining gap

`python3 independent_probes.py` requires only the Python standard library. It passes 99 exact assertions and writes `probe_results.json`; no frozen verifier is imported. The artifact includes reconstructed syzygies, Groebner generators, Hilbert-series data, Cech counts, colon/intersection evidence, and the degeneration certificate. The syzygy and cohomology ranges are finite checks. The global frame, ideal/Hilbert-series certificate, and proofs above supply the universal deductions.

The strongest result independently verified in this family is:

* Any proposed CM ideal with radical `a` is `a`-primary and has generic multiplicity at least two, whether homogeneous or not.
* No such ideal can contain the actual reduced quadric equation `q`.
* If it is homogeneous, its generic multiplicity is at least three.

The binomial exclusion is outside this family's principal verification scope. Together with that independently audited algebraic claim, the remaining class is non-binomial `a`-primary ideals for which `q` is nonzero and nilpotent in the quotient. A nonhomogeneous member can still have generic multiplicity two; a homogeneous member must have multiplicity at least three. No construction or exclusion of those classes has been proved. A route relying on CM-preserving homogenization is blocked by the explicit preservation counterexample; a route relying only on linkage transfers the central difficulty to unsupported hypotheses.

Recommended exposition hardening is limited to spelling out the local dimension formula in Proposition 4.1 and retaining the precise arithmetic/homogeneous boundary in Proposition 5.1. These are explanations of sound steps, not repairs of a false result. No novelty claim, unrestricted solution, release, DOI deposit, tracker change, or external outreach is warranted by this validation.

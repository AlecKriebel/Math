# Independent review: existence of disjoint-hypercyclic tuples

**Problem:** 30000567.  
**Verdict:** **PASS_COMPLETE_CREDITED_KNOWN_EXISTENCE_RESULT**.  
**Recommended status:** `already_solved`, `0/5` new approaches.  
**Mandatory corrections:** none.

The reviewed snapshot is `KNOWN_RESULT.md`, SHA-256 `04a12c724f2c57717465e856f58c79012b921e8b800cf3e8f8abc388f14503db`. This is a separate AI source/proof audit, not human peer review or a new discovery claim.

## 1. Original quantifiers and theorem match

I read the complete Bès contribution in [OWR 37/2006](https://ems.press/content/serial-article-files/46067), printed pp. 2235–2238, and inspected rendered Definition 1 and Problem 10. The definition requires one vector whose simultaneous co-orbit is dense in the **full finite product**. Both the vector and iteration index are shared by all coordinates. The problem asks whether every separable infinite-dimensional Banach space supports such a pair or larger finite tuple.

The next definition concerns disjoint transitivity/mixing, and the last paragraph discusses hypercyclic subspaces, but neither is imposed by Problem 10. In particular, the original problem does not require commuting operators or a dense set of common starting vectors. The candidate accurately avoids importing these stronger requirements. Each component of the constructed tuple is individually hypercyclic by projection, as Definition 1 also requests.

I read the complete [Shkarin author manuscript, arXiv:1209.1212v1](https://arxiv.org/abs/1209.1212v1), including its scalar-field convention, Theorem D, Proposition 1.3 and the reduction lemmas. The convention explicitly permits both real and complex scalars. Theorem D states the result on every separable infinite-dimensional **Fréchet** space for each prescribed positive finite tuple size. Its Definition 1.1 is exactly the same-time, same-vector, full-product definition above. Restricting to Banach spaces and taking any finite size at least two answers the original problem completely. No separable-dual condition belongs here; that condition appears in the distinct dual-hypercyclic Theorem S.

The manuscript was deposited in 2012, but its primary arXiv journal reference gives J. Math. Anal. Appl. 367 (2010), 713–715. I checked the cached publisher-deposited Crossref record: DOI `10.1016/j.jmaa.2010.01.005`, volume 367, issue 2, pages 713–715, publication year 2010. Thus the package correctly distinguishes deposit and publication dates. The final publisher-typeset PDF was not recovered. The actual mathematical verification uses the complete primary author manuscript; it is not represented as a page-by-page comparison against that inaccessible typeset version.

Shkarin expressly credits earlier existence constructions by Bès–Martin–Peris and Salas. The candidate preserves that attribution and does not claim that this campaign, or necessarily Shkarin's short proof, first discovered the existence theorem.

## 2. The required input is justified and not weakened

Proposition 1.3 supplies a single operator whose every prescribed finite direct sum is hypercyclic. Mere hypercyclicity of an arbitrary operator would not suffice, and the candidate never makes that inference.

For the Banach target I also inspected the full published [Grivaux paper](https://jot.theta.ro/jot/archive/2005-054-001/2005-054-001-010.pdf), its real/complex standing convention, and Theorem 2.6 with proof on printed pp. 152–153. It supplies a mixing operator in the infinite-dimensional setting used here. The theorem's abbreviated wording is not a license to claim hypercyclicity in finite dimensions; the package retains the original infinite-dimensional hypothesis throughout.

Here is the precise topological passage needed after the credited mixing input. For nonempty basic product-open sets `U=∏U_i` and `V=∏V_i` in `X^m`, mixing supplies an integer `N_i` for each coordinate. For all `n≥max_i N_i`, independently choose `z_i∈U_i` with `T^n z_i∈V_i`. This proves mixing, hence transitivity, of `T^⊕m`. The maximum exists because the tuple is finite.

Let `(V_j)` be a countable basis of the separable metric space `X^m`. Each set `⋃_(n≥0)(T^⊕m)^(-n)(V_j)` is open and dense by continuity and transitivity. Their intersection is nonempty by completeness and Baire's theorem. A vector in the intersection has a dense orbit. This is the complete logical step from mixing to the required product-hypercyclic vector; no coordinatewise choices of different orbit times are substituted for it.

The stronger Fréchet claim is itself the explicitly credited Shkarin theorem and Proposition 1.3. The candidate does not pretend to rebuild Bonet–Peris's general existence construction from finite-dimensional matrix tests.

## 3. Transporter and orbit identities

For linearly independent nonzero `u,v`, continuous linear functionals `f,g` with the four specified coordinate values exist by Hahn–Banach on their finite-dimensional span. In the complex case these are complex-linear functionals; no conjugate-linear inner product is being substituted. Define

`N z=(g(z)−f(z))(u−v)`.

Then `(g−f)(u−v)=−2`, giving `N²=−2N`. Consequently `S=I+N` satisfies `S²=I`; direct evaluation gives `Su=v` and `Sv=u`. Every term is bounded in a Banach space, and the inverse is the same bounded map. In the locally convex Fréchet setting the same finite-rank map and its inverse are continuous. The proportional-vector case uses `λI`, with `λ≠0`, and is handled separately.

No Schauder basis, infinite-dimensional complemented subspace, or reflexivity assumption is hidden in this construction. The finite-dimensional coordinate functionals are all that is required.

Now take a hypercyclic vector `(u₁,…,u_m)` for `T^⊕m`. Each coordinate is nonzero: otherwise the corresponding projection of its orbit is the singleton zero rather than dense in `X`. For a fixed nonzero `x`, choose the transporter in the correct direction, `S_i u_i=x`, and set `R_i=S_i T S_i^(-1)`. Repeated multiplication cancels adjacent inverse factors and yields

`R_i^n x=S_i T^n u_i`

for **the same** integer `n` in every coordinate, including `n=0`. The product map `∏S_i` is a homeomorphism, so it sends the dense product orbit to the asserted diagonal-start co-orbit. This is a full proof of the transport step, without any commutativity requirement between the different `R_i`.

Although every nonzero `x` can be chosen when constructing the operators, those operators depend on that choice. This does not assert that a fixed tuple has a dense set or subspace of disjoint-hypercyclic starting vectors. The candidate's exclusions are correct.

## 4. Exact controls and their limits

All **32,184 submitted assertions** pass on replay, and the output receipt is byte-identical to the original. The mathematical artifact, verifier and receipt hashes agree with the frozen package.

The separate standard-library checker uses an independent basis-conjugation construction: it forms a swap as `P W P^(-1)` and compares it with the rank-one formula. Its **3,650 assertions** pass, covering 150 independent vector pairs, including 50 pairs over the exact Gaussian-rational field `Q(i)`. It checks inverses, fixed complementary coordinates, similarity powers, scalar transporters, and thirteen simultaneous four-coordinate complex orbit identities.

These finite-dimensional maps are expressly **not hypercyclic examples**. Their role is to test the algebraic signs, inverses, scalar conventions, and common-time identities. Infinite-dimensional density follows from the credited mixing/direct-sum existence theorem and the Baire/homeomorphism arguments above.

## 5. Final disposition

The full existential target of OWR Problem 10 has a known affirmative answer, valid over both scalar fields and even for separable infinite-dimensional Fréchet spaces. The artifact's exact source match, dependency attribution, short proof, and publication-date qualification all pass. Keep `already_solved 0/5`; retain the inaccessible final-typeset-PDF caveat and the absence of a novelty claim. No mandatory correction to the frozen snapshot is needed.

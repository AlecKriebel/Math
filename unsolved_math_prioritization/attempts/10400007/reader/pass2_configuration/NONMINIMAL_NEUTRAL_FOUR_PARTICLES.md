# The first nonminimal neutral charge sector

PASS2, 14 October 2026. Use `M=S³\K`, `k=Q(u)`, and the ordered rank-one coefficient system `A_w` from PASS1, now with

`w=(1,1,−1,−1)`.

This is not covered by the minimal-neutral theorem: it has proper neutral subsets. We compute the resulting groups and their natural collision filtration. The computation concerns these groups, not every operation that could enrich them.

## Result

For every smooth/tame oriented knot,

`dim H₄(F₄(M);A_w)=2`,
`dim H₅(F₄(M);A_w)=4`,
`dim H₆(F₄(M);A_w)=8`,
`dim H₇(F₄(M);A_w)=6`,

and every other ordinary homology group is zero.

Borel–Moore groups have dimensions `6,8,4,2` in degrees `5,6,7,8`, respectively, and are zero elsewhere. The collision filtration is natural under oriented knot-pair diffeomorphisms. No canonical splitting of its two contributions in ordinary degree six is asserted.

## Proof

Let `X=M⁴`, let `D` be the union of its six collision diagonals, and let `A=L₁⊠L₁⊠L₋₁⊠L₋₁` on `X`. The ambient compact-support cohomology is zero.

As in PASS1, an intersection of collision diagonals is indexed by a graph on the four particle labels. Its connected components are the blocks of the corresponding partition. A restricted coefficient product is compact-support acyclic if any block charge is nonzero. The surviving cases are exactly:

1. A connected graph, whose intersection is the full diagonal `M` with trivial coefficients.
2. The disconnected graph with edges `{13,24}`.
3. The disconnected graph with edges `{14,23}`.

The two disconnected graphs each give a copy of `M²` with trivial coefficients. They occur in Čech degree `p=1`, because they have two edges. There are no other fully neutral proper partitions: singletons have nonzero charge, and a three-element subset cannot have charge zero.

The full-diagonal summands form the connected-graph relative cochain complex used in PASS1. Its cohomology has dimension six in Čech degree `p=2`. Since `H_c^*(M;k)` has dimension one in degrees two and three, these contribute

`E₂^(2,2)=k⁶`, `E₂^(2,3)=k⁶`.

For each neutral pair partition,

`H_c^*(M²;k) ≅ H_c^*(M;k)⊗H_c^*(M;k)`,

with dimensions `1,2,1` in degrees `4,5,6`. The two partitions therefore contribute

`E₂^(1,4)=k²`, `E₂^(1,5)=k⁴`, `E₂^(1,6)=k²`.

There is no omitted first-page differential from one of these terms to a full-diagonal term: restrictions preserve the compact-support cohomological degree `q`, whereas the pair-product terms have `q≥4` and the diagonal terms have `q≤3`.

All other second-page entries are zero. A higher cohomological Čech differential changes `(p,q)` by `(r,1−r)` with `r≥2`, so none can connect the two surviving columns `p=1,2`. The spectral sequence collapses. It gives compact-support cohomology of `D` of dimensions

- six in total degree four;
- eight in total degree five;
- four in total degree six;
- two in total degree seven.

Open/closed localization shifts these degrees up by one to obtain `H_c^*(F₄(M);A_w)`. Oriented duality in dimension twelve then gives the stated ordinary Betti numbers. The dual charge vector is obtained by swapping the positive and negative labels, so ordinary dual-coefficient homology has the same dimensions; ordinary/Borel–Moore duality gives the stated Borel–Moore degrees.

## Naturality and the extension caveat

The finite diagonal arrangement is defined directly from the complement, and a diffeomorphism acts diagonally on it. The coefficient restriction to every partition is given by block charge addition. These facts induce natural maps on the Čech resolution and its filtration.

Two filtration pieces contribute in total degree five for `D`, hence in ordinary homology degree six for `F₄(M)`: dimensions six from the full diagonal and two from pair partitions. A collapse computes the associated graded and total vector-space dimension, but does not supply a canonical chosen direct-sum decomposition. We do not use such a splitting.

The two degree-four homology directions arise from pairwise collision-sphere products associated with the two neutral matchings. Higher enriched linking, products or extension information might be knot sensitive; the calculation does not discard them. The companion report constructs and computes one genuine secondary linking operation at the Laurent-coefficient level, the Blanchfield form.

## Reproducible check

`check_enriched_pairing.py` enumerates all edge subsets of the six-edge complete graph, assigns the surviving coefficient cohomology, builds the signed Čech differentials, checks their squares, and computes exact rational ranks. It verifies the displayed second page and Betti numbers. The proof above establishes why those matrices and the collapse compute the claimed groups.

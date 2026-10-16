# Independent full review: complexity and rational tiling cohomology, 6600013

**PASS for all five scoped results, with the additive roof-parameterization clarification. Original arbitrary higher-dimensional question remains unsolved, 5/5 author turns.** No mandatory mathematical change to the frozen results is required. This is an AI-assisted audit, not external peer review or novelty certification.

The reviewed 44-file author packet is bound by FINAL_FROZEN_MANIFEST.json SHA-256 6051cac8bee10f0bdfa2bdadcb782ee3782855964cd2e10ee1a1fb0023c6f056 and commit fdda349c0bf35776bdfe5e8001b95f42df9b7057, repository folder unsolved_math_prioritization/attempts/6600013. Every remote Git blob and local byte length was checked. No author file was modified.

## Exact source and credited correction

The original Julien Problem2.5.1, arXiv1604.06280 page8, was visually checked together with its surrounding discussion. It asks whether O(n^d) translational patch complexity of an aperiodic repetitive d-dimensional tiling implies finite total rational cohomology rank. The rational-versus-integral distinction is explicit: the quoted Thue–Morse integral group is not finitely generated, but has finite rational rank. That is not a rational counterexample. The preceding finite-rank/high-complexity examples disprove the converse direction, not this implication.

Primary sources: https://arxiv.org/pdf/1604.06280 ; Julien's available v1 https://arxiv.org/pdf/0804.0145 ; Koivusalo–Walton's published *Cut and project sets with polytopal window I: Complexity*, ETDS41(2021)1431–1463; and Julien's2017 paper https://www.numdam.org/item/10.5802/aif.3091.pdf . All four frozen PDFs were hash-verified. The one-dimensional Rauzy proof is Theorem5.10/Proposition5.16 in the downloaded v1, while the original problem cites published Proposition6.7. This numbering discrepancy is recorded, not conflated.

Koivusalo–Walton's introduction, canonical Example4.3 and Section8 were read. Their quasicanonical condition repairs the acceptance-domain/hyperplane-cut topological identification; almost-canonical alone is insufficient. Canonical schemes satisfy the stronger condition. The author packet correctly avoids invoking an unrestricted almost-canonical cohomology equivalence. Julien2017 Section2 confirms finite prototiles, translational FLC, repetitivity and no nonzero translational period. Singular cohomology, rotational hulls and partially periodic examples are outside the audited target.

## Turn 1: cofinal rank control and the product theorem

The centered Rauzy graph maps retain the interval coordinate and the correct boundary identifications, giving the usual suspension inverse limit. Connected graph ranks are p(n+1)-p(n)+1. The argument only needs infinitely many small ranks, and correctly proves the direct-limit bound without asserting injectivity. Conversely independent limit classes remain independent at every sufficiently late stage.

The liminf slope argument respects integer increments, including integer values of the liminf. Minimal aperiodicity supplies Morse–Hedlund's n+1 floor. Cartesian-product word complexity is exactly the product of factor complexities; independent coordinate translations give the full product hull, repetitivity and absence of nonzero periods. Čech Künneth is justified at finite graph products and then through filtered direct limits, avoiding a local-contractibility assumption on the hull itself.

The factor inequality 1+r<=3max(1,r-1) and eventual complexity slopes give total rank at most3^d times the specified box-complexity liminf coefficient. The coefficient is not claimed unchanged under arbitrary radius conventions. The two Sturmian classes are independent over Q because invariant-measure integration gives1 and an irrational frequency; this proves sharpness for the stated product subclass.

## Turn 2: a genuine approximant obstruction

The rectangular pattern complexes are finite CW complexes even when boundary identifications are not regular. Prefix/suffix attaching maps yield the stated alternating cell count. Centered cropping gives the suspension inverse limit; this is not an assertion that all raw cellular classes survive.

The Thue–Morse alignment argument is valid: double letters locate substitution parity, and the excluded length-five alternating factors remove the ambiguity at the stated lengths. The exact even/odd recurrences, small initial values and two cofinal increment patterns imply the Euler values2n+6 and-2n. The two-block recoding is invertible, and the integral shear has determinant1, so the system is genuinely fully aperiodic, repetitive and FLC. Its rectangular complexity is p_TM(n+m)(m+1), while its suspension is homeomorphic to the product hull. Thus its limiting rational cohomology is finite despite unbounded stage Betti numbers. This is a valid obstruction to a raw approximant-rank argument, not a source counterexample.

## Turn 3: persistence and the collared stationary model

For each fixed finite-dimensional source space, increasing kernels stabilize; the canonical image in the direct limit has dimension equal to the infimum of later composite ranks. The supremum over source stages is therefore correct, with the quantifier 'for every i there exists j' retained. The cochain image formula rank[B_j,FZ_i]-rank(B_j) is valid after the chain identities are checked.

All ten shared-pair gluings of the six Thue–Morse collar edges coincide with the legal four-letter language. The stated vertex and edge substitution maps respect boundaries. Unique pair recognition and growing collared borders determine complete legal neighborhoods, supplying the inverse-limit identification. The three cycle columns and their substitution matrix were independently reconstructed. Rank(J)=rank(J²)=2 and the nonzero eigenvalues2,-1 produce rational H¹ rank2; integral inversion of2 is not claimed. The transposed cohomology map and the product rank polynomial1+4t+4t² are correct. Exact cropping ranks verify the death of two transient degree-two dimensions without extrapolating a uniform stabilization delay from finite data.

## Turn 4: actual covers, topology and metric conventions

The finite-stage cover theorem uses actual covers pulled back from a specified finite graph-product level. Collapsing spanning trees and lifting homotopy equivalences bound the total number of cells by D product(1+M_i). Independent cofinal choices of factor word lengths are legitimate. Finite-state transport must be local and flat on every square; these hypotheses give a genuine cover, including higher product-cell compatibility. They do not justify arbitrary finite-to-one factor maps.

The two-sided complexity estimate assumes the full D-sheet extension, as stated. Its liminf consequence only shifts the integer argument by a fixed amount. It does not require regular variation. The coefficient bound follows from the factorwise liminf inequality.

For tau(a)=aab,tau(b)=ab, b marks supertile endpoints and preceding a-runs distinguish the two blocks. Primitivity, irrational frequency and the block-length estimate establish minimality, aperiodicity and linear complexity. Properness gives growing borders. The displayed free-group inverse verifies that its two-loop substitution map is a homotopy equivalence.

The variable-length substitution requires a metric convention when identifying that stationary graph model with the unit-roof symbolic suspension. The additive TOPOLOGICAL_CLARIFICATION.md supplies it explicitly: PF lengths ((1+sqrt5)/2,1), expansion(3+sqrt5)/2, and the tilewise roof-change homeomorphism. This is not a translation-time-preserving conjugacy. It lifts compatibly to every decorated cover because the symbolic crossing cocycle is unchanged. Thus the cohomology/connectedness computations and unit-box complexity statements are all justified without an unstated constant expansion on unit tiles.

The cyclic cover monodromy is surjective, and its pullbacks remain surjective because the substitution induces a free-group automorphism. Lifted maps are homotopy equivalences. Connectedness of the inverse-limit cover, together with the constant-cardinality/clopen minimal-component argument over a minimal base, proves the finite extension is minimal. Its periods project to base periods and hence vanish. Fourier decomposition has one trivial character contribution(1,4,4), and each nontrivial character contributes one H² dimension, giving(1,4,q+3). Rational ranks equal complex ranks by scalar extension. The growing q-dependent complexity constants are retained.

## Turn 5: infinite cohomology without an admissible finite generator

The2-adic additive cocycles commute with finite-level reduction. Basic cylinder sets prove minimality of the inverse-limit action; base freeness proves its freeness. Suspension commutes with the tower via the common fractional square coordinate, with compatible boundary identifications.

The q-to-2q maps are genuine two-sheeted covers. Summing over cell lifts is a cochain transfer and its composition with pullback is twice the identity; over Q pullback is injective. This passes through the substitution models and Čech continuity. Unbounded finite ranks q+3 therefore give countably infinite H², with degree-one rank4 and no higher cohomology.

The topological obstruction is equally explicit: two points over one base configuration with a small nonzero2-adic fiber difference keep that difference under every lattice translation. The action is nonexpansive. Every finite-alphabet subshift is expansive, so the specified action is not conjugate to one. Compactness forces every continuous finite-valued observation to factor through one finite fiber level and one finite base window; its whole orbit code loses the remaining fiber tail. Its low-complexity factor image does not become a generator. No arbitrary factor-map cohomology assertion is made. The full-state decoration fails FLC, and the canonical finite-level complexity constants diverge. No different source-admissible realization is constructed or universally ruled out.

## Reproduction and disposition

All5,367 author assertions replay byte-exactly, all173 historical/final bindings and four primary PDF hashes verify, and all44 remote raw blobs match. The separate checker passes22,728 exact controls: independently assembled cyclic cover cochains and Betti numbers through covering degree24, pullback/transfer identities, the collared Thue–Morse map and cycle basis, proper-substitution inverse words and monodromy surjectivity, and product-rank bookkeeping. Infinite topology and admissibility were audited analytically; finite matrices do not replace those arguments.

Recommended disposition: original unsolved5/5, with all scoped results and this additive parameterization clarification retained. No new author search, full original proof or admissible infinite-rank counterexample is claimed.

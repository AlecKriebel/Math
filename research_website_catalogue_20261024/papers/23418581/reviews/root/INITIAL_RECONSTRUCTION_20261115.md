# Root paper-first reconstruction — 23418581

The complete four-page published PDF, all279 controlling TeX lines, and all four fresh root page rasters have been personally read before current peer reports/verdicts, archived review bodies, supplied programmes/results or foreign primary bodies. The manuscript itself reports historical checks and attribution; those statements are target claims, not independently reproduced evidence. General representation-theory background predates this intake. The comparison gate stays closed until this reconstruction and its authority are frozen.

## Exact target and success conditions

Let p be any odd prime, k algebraically closed of characteristic p, r=2p−1, and λ=(r−1,1). The whole original claim is that, in the printed convention Y^λ=F I_N(λ) at stable N≥r, the Young module is simple of dimension r−1, while its polynomial injective hull I_n(λ) is nonprojective for every n≥2. The manuscript also claims that this refutes the unrestricted first proposal of Miyachi's printed2009 Conjecture7 and its stronger Λ-family criterion. No conclusion about characteristic-zero/nontrivial-root-of-unity variants or new classification is claimed. A success requires the full all-prime/all-rank proof, actual conventions and all load-bearing structural inputs, not just the p3 computation.

## Family1: elementary symmetric-group simplicity

Here r≡−1 modp, so p does not divide r. The coordinate-sum map splits the natural permutation module V=k^r as its constant line and A={sum coordinates=0}. A constant vector in A must vanish because r is invertible. For a nonzero submodule of A, use a nonzero vector with two unequal coordinates: subtracting its transposition produces a nonzero multiple of e_i−e_j. Coordinate permutations generate every difference and hence all A. This proves A is simple of dimension r−1 without a classification theorem. This part is independent of any Schur-module label identification.

## Family2: exact label through symmetric powers and polarization

At stable N≥r, set H=Sym^(r−1)(k^N)⊗k^N. Subject to the cited injective/weight-multiplicity theorem, any simple label whose relevant weight is (r−1,1,0,...) must dominate λ; only (r) and λ do so. The λ weight in L_N(λ) is the unique highest-weight line. The other relevant weight has multiplicity one in L_N(r): its highest vector x_1^r lies in the socle of Sym^r, and the coefficient of t in (x_1+t x_2)^r is r x_1^(r−1)x_2≠0. The ambient weight space has dimension one. Thus H=I_N(r)⊕I_N(λ), conditional on the exact cited multiplicity convention.

Costandard reciprocity makes I_N(r)=∇_N(r)=Sym^r at the maximal partition. Multiplication m:H→Sym^r splits through the equivariant polarization δ(f)=sum_i(∂f/∂x_i)⊗x_i, with mδ=r id. Krull–Schmidt cancellation gives ker m≅I_N(λ). On multilinear weight spaces, H is the r-dimensional permutation representation on the distinguished tensor variable, and m is coordinate sum to the trivial line. Exactness of the stable Schur functor then identifies F I_N(λ)=A. Critical checks remain the actual F I Young convention, the tensor-symmetric-power injectivity/multiplicity theorem, and the costandard reciprocity orientation. A sign/conjugation or convention mismatch cannot be dismissed using a familiar Young-module name.

## Family3: direct rational GL2 local structure

Use the algebraic diagonal torus: distinct monomial characters remain distinct in characteristic p; this is not a statement about distinct characters of the finite diagonal group. Any rational GL2 submodule splits into weight components. Over infinite k, the coefficients of a unipotent translate belong to the submodule by Vandermonde extraction.

From x^(m−i)y^i, the coefficient of t^i in y→y+t x is x^m. For m=2p−1, the expansion (1+t)^m=(1+t^p)(1+t)^(p−1) has every coefficient nonzero modulo p. Starting from x^m, the opposite unipotent therefore produces all monomials. Sym^(2p−1) is simple.

For B=Sym^(2p−3), the image W of E^(1)⊗Sym^(p−3) under x^(1)⊗f→x^p f and y^(1)⊗f→y^p f consists exactly of indices0..p−3 and p..2p−3. The ranges are disjoint, so the map is injective and dimW=2p−4. Frobenius multiplication is equivariant. The binomial expansion with base-p digits(1,p−3), together with extraction to x^(2p−3), shows W is generated from any nonzero weight vector, hence simple of highest weight(2p−3,0).

B/W has only the two weights represented by indices p−2,p−1; the two opposite unipotents connect them by coefficient p−1≠0. Therefore it is simple, with dominant highest weight(p−1,p−2) and dimension2. A torus-stable complement would have to be exactly those two monomial weight lines. But y→y+t x applied to index p−2 has coefficient x^(2p−3) at t^(p−2), outside that span. The extension is nonsplit. Since its two simple factors are nonisomorphic, its socle is W and its top is B/W.

This proof covers p3 too: B=Sym^3, W=span(x^3,y^3) is the Frobenius-twisted natural module, and the quotient is det⊗E. Equal dimensions do not identify their algebraic highest weights. The p2 case is outside the proof: W would have no displayed basis and the nonsplitting argument would not supply the claimed obstruction.

## Family4: injective obstruction and all permitted ranks

Only (r) strictly dominates λ. Because ∇_2(r) is simple and has a different highest label, its multiplicity of L_2(λ) is zero. The precise reciprocity formula would then give I_2(λ)=∇_2(λ)=det⊗B. Its socle is L_2(2p−2,1), top L_2(p,p−1); the labels differ even for p3. Contravariant duality fixes simple labels and interchanges socle/top, so I_2(λ) is not contravariantly self-dual.

The implication 'indecomposable polynomial injective projective ⇒ contravariantly self-dual indecomposable tilting' is load-bearing and must be checked in the actual Schur-algebra source; it is not assumed for every algebra with a duality. Subject to this input, I_2(λ) is nonprojective.

If I_N(λ) were projective for some N≥2, its corresponding tilting highest label μ must dominate λ because L_N(λ) is a composition factor. Hence μ is (r) or λ, both with at most two parts. The exact labelled rank-truncation theorems for I and T would yield I_2(λ)=T_2(μ), contradicting the rank-two obstruction and the injective-tilting⇒projective statement. This is a labelled argument; arbitrary idempotent truncation need not preserve projectives. An alternative route worth checking as an independent verification is whether the specific rank idempotent commutes with contravariant duality, taking a hypothesized self-dual I_N(λ) to the explicitly non-self-dual I_2(λ). No unsupported alternative is promoted into a substitute proof.

## Family5: printed formulation, boundaries and attribution

Simplicity of Y implies simplicity of its top. Thus all-rank nonprojectivity refutes the first proposal only if the actual printed statement quantifies over the q1/positive-characteristic setting and existential n≥lengthλ in the stated convention. The subsequent characteristic-zero subsection must be read in context; no inference is made from the manuscript's asserted placement alone. Likewise the Λ-family corollary needs the actual sufficient membership⇒projectivity interface and quantifiers, not a completeness theorem.

The scope is algebraically closed k, odd p, n≥2, ordinary polynomial Schur categories, stable Schur functor only at N≥r and q1. No finite-group-GL2 inference, row-regular⇒p-restricted substitution, arbitrary-projective truncation, numerical-only universal proof, firstness, worldwide-open or characteristic-zero claim is accepted. Classical augmentation, rank-two structure, symmetric-power injection and truncation deserve their existing credit.

## Falsifiable checks and remaining gaps at initial seal

Before final disposition, read actual Miyachi OWR printed944–947, especially945–946 and the following subsection; actual De Visscher–Donkin dated12Jan2005 reciprocity/projective-injective/labelled truncation and symmetric-tensor multiplicity statements; actual Cox–Parker stable conventions; and the claimed Erdmann–Law local structure interface as needed for exact credit. Check field/rank/degree/partition and duality conventions rather than replacing them by source titles. Distinguish accepted manuscripts from final publisher bodies.

Inspect every native support programme and its saved expected/actual outputs after this initial. The presealed independent adversarial lane owns any meaningful supplied exact replay; root will read its exact full streams/code and perform only safe custody comparisons. The manuscript-reported p3/p5 coefficients and S(2,5) 56basis/3136products/dimP6 versus dimI4 are currently unverified source reports. Root has run no scientific programme or own numerical control and has read no external/current peer findings. Exact original source/edition/rights/archive custody and all peer proof gaps remain to be checked. Follow-up defaults to none.

Initial result: the elementary reconstruction is coherent conditional on these precise classical interfaces, with no counterexample yet found. This is not a scientific PASS or publication authority. Estimated bounded root review completion:35%.

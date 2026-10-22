**Integrated reader status.** Full historical audit of the conditional bridge. The CR dependency, and only that dependency, is replaced by the accepted [192-class proof](../proofs/CLASS_GENERATION.md). Original retrieval-failure statements remain accurate; they are no longer a blocker to the integrated theorem. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# Independent audit of the natural-group Bray generation bridge

Date: 13 October 2026. This audit reviews the natural-group generation reduction.

## Verdict

**ACCEPTED as a complete mathematical reduction under the explicitly stated class-random generation input CR(Sp, Ω).** The new orthogonal half-mass refinement, conditioning, exact derived-group target, product obstruction, probability estimate, and confidence amplification all pass independent review. No substantive mathematical correction was required.

**The original-source gate remains open.** A full 2013 survey coauthored by the authors of the 2011 generation theorem was retrieved and inspected, including visual inspection of its Theorem 2.53 on printed p.77. It supports the stated classical-group generation input. The original Praeger–Seress 2011 full article and its exact ambient-group conventions were not retrieved. In particular, Ω is not expressly listed in the inspected survey statement, and its generalized-Fitting terminology for larger classical groups is imprecise. The audit does not convert this documentary qualification into an unconditional certification of the original theorem's exact Ω scope.

The accepted deduction is therefore:

> If CR holds for the natural quasisimple Sp and Ω factors, the accepted marginal constructions, with the orthogonal refinement below, give the asserted O(log n) sampling bound for containing C_G(t)'' in natural Sp and O/SO/Ω, and O(log n (1+log(1/δ))) samples give confidence at least 1−δ.

This is stronger than accepting a heuristic projection argument, and weaker than certifying an unqualified all-classical result in all representations and dimensions. The numerical marginal thresholds are explicit; the full generation threshold includes the uncomputed published dimension constant d₀.

The reviewed author's artifact is `GENERATION_BRIDGE.md` in the corresponding author packet. Its accepted original identity and reader-copy identity are recorded in the [artifact manifest](../metadata/AUTHORED_ARTIFACTS.json). The statements below are an independent check, not a reproduction of a source document.

## 1. Precisely what input is used

Fix α=1/4 and β=3/4. The required CR input asserts absolute positive integers c,d₀ such that, for every odd q, every natural J=Sp(U) or Ω(U) of dimension e≥d₀, and every prescribed sequence of c J-conjugacy classes of involutions having fixed dimension r with αe<r<βe, independent uniform elements in these classes generate a subgroup containing J with probability at least 1−q^(−e).

The choice 1/4,3/4 is important. The actual 2013 printed balance definition has strict inequalities at both endpoints. Text extraction misread the lower inequality. Every strong involution in the audited closed interval [e/3,2e/3] meets both strict inequalities with room to spare. Likewise the printed dimension condition is strict; increasing d₀ beyond its stated integer cutoff is legitimate.

The theorem must apply to every prescribed class sequence. A result only for uniformly random involutions, a single conjugacy class, or an average over classes would not suffice. The inspected restatement explicitly gives the prescribed-sequence and mutual-independence hypotheses. It is not merely a generation assertion from an abstract.

The survey's Table 2.1 lists symplectic and special orthogonal groups for a different pre-involution theorem, Theorem 2.31 and Corollary 2.32. That table is expressly local to those results. It neither proves nor disproves Ω inclusion in Theorem 2.53. The original definitions remain the exact outstanding check.

Restricting CR to perfect Sp and Ω avoids the known scalar issue in the survey's informal generalized-Fitting example: ordinarily F*(GL) also contains central scalars, and in suitable full orthogonal groups a scalar factor can lie outside Ω. An arbitrary list of Ω-involutions cannot generate such an extra factor. No conclusion about a larger group's full generalized Fitting subgroup is used here.

## 2. Independent check of the orthogonal Ω refinement

In the accepted orthogonal construction, f=f_*f₀ is squarefree, the distinguished factor has degree k divisible by d≥4, and deg f₀=a−k≥a/6>8. Thus there are s≥2 distinct primary factors. Each factor has exactly two trace-form square classes. Changing the coefficient by a nonsquare changes the base-field discriminant by a nonsquare, since χ_q(Norm x)=χ_(q^j)(x).

For a fixed f, exactly 2^(s−1) sign assignments have the required discriminant of A. Prescribing the distinguished primary space U_* to have square discriminant leaves exactly 2^(s−2), because the remaining s−1 signs can supply either total parity equally often. Every corresponding K-orbit has the same centralizer order 2^s. Therefore the count of K is halved exactly, not just approximately and not by an independence assumption.

Neither det K nor det(I+K) changes when the trace-form class changes: both are fixed by f. The embedding count of F with F*F=K depends only on the total induced-form discriminant and the fixed dimensions, which remain unchanged. This validates the same one-half factor in the graph probability mass, including a=b and different eigenspace discriminants.

The involution z is negative precisely on U_* and F(U_*), and positive on the other blocks. Their dimensions are k. The two restricted forms have discriminants related by det(K|U_*), already a square in the distinguished-factor construction. They therefore both have square discriminant. Since k is even, their determinant signs are positive. With Q=β/2, the spinor norm of the negative-space involution is 2^(−k)disc(β|U_*); the factor 2^(−k) is a square. Both restrictions lie in Ω.

The accepted original bound counted an actual subset of successful outputs, with mass greater than 1/(5,000,000 log n). Halving that counted subset proves the new bound greater than 1/(10,000,000 log n) for each separately chosen factor while requiring both restrictions to lie in Ω. This does not assert that every successful Bray output lies in Ω×Ω, or that its spinor norms are independent of balance.

## 3. Class invariance and selection bias

For C=C_G(t), replacing uniform g by gc, c∈C, sends z=inv(tt^g) to z^c. Thus the output law is C-conjugation invariant. Its atom at the identity causes no issue because a strong selected restriction is nontrivial.

In the symplectic case the exact centralizer is Sp(A)×Sp(B), even if dim A=dim B. Commutation with t preserves the two distinct eigenspaces; interchanging them is not centralizing t.

For orthogonal groups, let D=O(A)×O(B). C is D or the kernel of the total determinant or of total determinant and spinor norm. An involution z commuting with t has four nondegenerate joint eigenspaces. One has dimension at least n/4≥3. Its reflection subgroup, embedded in C_D(z), realizes determinant/spinor pairs (−1,+1) and (−1,−1), because a quadratic space of dimension at least three over an odd finite field contains a hyperbolic plane and represents both square classes. These pairs generate D/C. Hence D=C C_D(z), and z^D=z^C.

Consequently conditioning on the pair of full component isometry classes makes the pair uniform on the Cartesian product of those classes. In particular the two coordinates are then independent. Admissibility and strength on either factor are class properties, so conditioning on them does not disturb this conclusion.

A strong involution in Ω(U) has a centralizer in O(U) whose reflections similarly map onto O(U)/Ω(U). Its O-class is thus a single Ω-class. Therefore selected strong components meet CR's exact Ω-class requirement. No blanket assertion that arbitrary O-conjugacy classes remain intact in Ω is made.

## 4. The exact target C_G(t)''

At the large dimensions in question, let L_U=Sp(U) or Ω(U). Taylor's Theorems 8.7–8.8 and 11.45–11.48 give perfectness and nonabelian simplicity modulo center, with explicit low-dimensional exceptions far below the working cutoffs. The spinor characterization is supplied by Theorem 11.51.

Put L=L_A×L_B. This product lies in C, including when G=Ω(V), because the factors extended by the identity have determinant and spinor norm one. D/L, and therefore C/L, is abelian. Hence C'≤L; perfectness gives L=L'≤C'. Thus C'=C''=C^∞=L. In Sp one even has C=L.

This equality is established for the current natural large-dimensional setting. It is not imported from a source that used a last-derived target, and no equality is claimed for small exceptional groups, projective centralizers, or similitude centralizers.

## 5. Subdirect products and central covers

Suppose a subgroup K≤D projects onto groups containing L_A and L_B. Then K'≤L and its two projections are L_A and L_B, because the factor quotients are abelian and the L_U are perfect. Let S_U=L_U/Z(L_U). Goursat's elementary simple-factor argument says the image of K' in S_A×S_B is either the whole product or one graph of an isomorphism S_A→S_B.

If it is the whole product, K'Z=L with Z=Z(L_A)×Z(L_B). Since Z is central and L is perfect, L=(K'Z)'=K''≤K'. This proves containment upstairs. Surjectivity only modulo centers has not been mistaken for an automatic lift.

Otherwise there is one fixed graph Δ_φ. If H₁=⟨K,z⟩ still fails to contain L, its derived image is also a graph and contains Δ_φ. Two isomorphism graphs between these simple groups have the same order, so the larger graph equals Δ_φ. Since z normalizes H₁', it must normalize that already fixed graph. Its component automorphisms satisfy a_B(z_B)=φ a_A(z_A)φ^(−1).

This is the correct way to avoid an automorphism union bound. The graph is fixed by previously exposed data. One does not assume that K itself is diagonal, that an isomorphism of simple quotients lifts to the quasisimple factors, or that dimension alone distinguishes abstract simple groups.

## 6. Why the extra sample has at most two bad lifts

If h∈D_U induces the identity on S_U, write hxh^(−1)=x f(x), f(x)∈Z(L_U). Centrality makes f a homomorphism L_U→Z(L_U). Perfectness implies f=1. Hence h centralizes L_U as matrices.

The scalar-centralizer check in the candidate is valid and elementary. In Sp, the image of a transvection minus the identity is its center line, and all lines occur, so a commuting linear map preserves every line and is scalar. In Ω, the common fixed space of all Siegel transformations with fixed singular center line ⟨u⟩ is precisely ⟨u⟩. Thus a commuting linear map fixes every singular line. A Witt basis with at least two hyperbolic pairs forces one scalar on the hyperbolic summand. For an anisotropic vector w, the independent singular vectors e₁+w−Q(w)f₁ and e₁−w−Q(w)f₁ have sum in that summand, so their eigenvalues equal the same scalar and subtraction gives the same scalar on w. Finally an isometry scalar satisfies c²=1. The kernel has at most two elements.

Expose K, the two component classes of the independent extra sample, and its A component. At most two values of the B component can induce the required automorphism. Its conditional distribution is uniform in its B class, so failure is at most 2/|z_B^(D_B)|. This is valid without simultaneous strength and without identifying the relative negative dimensions.

The class-size estimates are correct. In dimension e with strong negative dimension s, the exponent in both order quotients is s(e−s)≥2e²/9. The symplectic product correction is at least 7/8. The orthogonal correction is at least (7/6)/(8/3)²=21/128. The resulting bad probabilities are at most (16/7)q^(−2e²/9) and (256/21)q^(−2e²/9), both strictly below 13q^(−2e²/9). The possible central lift multiplicity has already been charged in the numerator two.

## 7. Probability bookkeeping and amplification

Partition samples into 2c+1 independent blocks, c for A, c for B, and one extra B block. A block of length

L=ceil(κ^(−1)log n log((2c+1)/η))

fails to contain its target event with probability at most exp(−κL/log n)≤η/(2c+1). The union bound gives collection probability at least 1−η. This uses separate marginals only. It avoids the erroneous inference that one block simultaneously supplies both marginal events with failure ≤one marginal failure probability.

Conditioning all blocks to succeed preserves independence, because the event factors over disjoint blocks. The first successful output in a block has exactly the single-trial law conditioned on the target event. This follows by conditioning its first-success index, then averaging; earlier failures have no effect on the current independent draw.

Conditioning on each selected component class now yields the independent class-random sequence required by CR. The two projection failures cost at most q^(−a)+q^(−b). The extra block remains independent of K under all this block conditioning. Adding the graph-escape failure gives

P(H≥C_G(t)'')≥1−η−q^(−a)−q^(−b)−13q^(−2b²/9).

With η=1/20 and the minimum factor dimensions 16384 in Sp or 32768 in O, the remaining error is less than 1/20, uniformly q≥3. The base success exceeds 0.9. Independent batches fail simultaneously with probability at most 10^(−r), where r=ceil(log(1/δ)/log 10). Retaining every output suffices; no algorithmic test identifying a successful batch is needed.

This establishes O(log n) samples at fixed confidence, and O(log n (1+log(1/δ))) for variable confidence. It does not claim that a fixed unspecified constant times log n already gives failure o(1), or that this is total bit complexity. Computing exact orders and obtaining independent uniform group samples remain computational operations with their own costs.

No extension to merely pointwise-nearly-uniform sampling is included. Such a law is not in general conjugacy invariant; directly reusing the class-uniformity argument would be invalid. A separate mixture/coupling argument could address it, but is not needed for the current theorem.

## 8. Independent finite controls

The [stage certificate](../certificates/GENERATION_BRIDGE_STAGE.json) records an exact-arithmetic reconstruction using explicit exceptions and elementary group operations. It was run normally and under -O and -OO. These are safeguards, not a substitute for the proof:

- Enumerated all 120 matrices of SL(2,5), checked its derived subgroup has order 120, its center has order two, and the projective group has order 60.
- Computed all conjugation actions on the 60-element quotient; every fiber has exactly two matrices.
- Constructed the 240-element proper subdirect subgroup {(x,±x)} of SL(2,5)². Its projections are both full, but it is not a graph upstairs; modulo centers it is a single graph. This directly controls the central-cover pitfall.
- Adding (I,u) with u a standard noncentral unipotent to generators of that subgroup produces all 14,400 elements of SL(2,5)².
- In a 30-element order-four class, a specified projective conjugation action has exactly two lifts, attaining the two-over-class-size safeguard.
- Exhaustively enumerated a four-trial rational-probability first-success model with two possible selected classes; the selected law is precisely the success-conditioned one and uniform within its two-element class.
- Exhaustively checked the orthogonal primary square-class half-count for s=2 through 8, both total discriminants, and both distinguished discriminants.

## 9. Retrieval and publication boundary

The 2013 survey was retrieved from an author-profile PDF link publicly supplied in its ResearchGate page metadata. It has 49 PDF pages, 493,076 bytes, SHA-256 `177111138e707c1beecdb19176e82802bd43eb2a6ab25cd5bcf3a200ca13ba92`. PDF page 43 is printed p.77 and was rendered and visually inspected. Printed pp.75–77, the nearby definitions, Table 2.1's separate scope, and bibliography were read.

The exact original legacy URL supplied by Crossref redirects to the journal homepage, not the article. The current article HTML request returned empty HTTP 202. The publisher abstract, UWA metadata, author bibliography, and OpenAlex locations were checked; none yielded original full text. OpenAlex reports no known repository full-text location, which is evidence about that service's records, not proof that no accessible copy exists.

The original article remains a concrete next documentary task: inspect Theorem 1.1 together with its definition/list of ambient groups and its convention for the generated normal subgroup, verifying the exact natural Ω specialization or a sufficient class-preserving supergroup specialization. The present proof should not be described as having completed that check.

Source PDFs, extracted text, HTML response bodies, and renders are private inspection evidence. They are not authored mathematical work and must not be included in any public proof packet. Public citations and verified hashes and sizes are listed in the source metadata. Integrity hashes certify bytes, not mathematical truth.

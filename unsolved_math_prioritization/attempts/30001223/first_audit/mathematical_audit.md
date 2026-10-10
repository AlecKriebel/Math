# Independent adversarial audit: Simple Tops of Young Modules

## Verdict

**ACCEPTED: counterexample to the unrestricted positive-characteristic bridge in Miyachi's Conjecture 7.**

Over an algebraically closed field of characteristic 3, with q=1, r=5 and lambda=(4,1), the Young module is simple of dimension 4, while the polynomial injective I_n(4,1) is not projective for every n >= 2. The author's family, for each odd prime p with r=2p-1 and lambda=(2p-2,1), also passes the mathematical audit.

No repair to the frozen author's mathematical argument is required. The convention supplement below supplies an additional direct identification with the source's Schur-functor definition. This is an independent audit, not external peer review or evidence of novelty.

The verdict does **not** refute the separate De Visscher-Donkin classification of projective-injective polynomial modules. Nor does this q=1 positive-characteristic example settle a reformulation restricted to characteristic zero at a nontrivial root of unity.

## Frozen target and source scope

The inspected author archive is exactly 12,753 bytes, SHA-256 e82e3a8349c00e74199090c3463918f5a83b915d85003438fa030adabf797978. It was preserved unchanged. Its verifier is 5,729 bytes, SHA-256 0474f5230da11233e3182bb533de1d949d07b43581c7ec6cbaa65a97286f2ea6. These bytes match the author's receipt. The receipt's assertion about a pin preceding the first historical execution cannot independently establish that chronology; the current independent replay verified the immutable archive before executing it.

All three supplied corpora were hashed in full. The unique full target record, rank 824, ID 30001223, problem number OWR-3400-007, was reviewed, including its statement, background, dated literature assessment and associated report. The associated report is the empty object. Both the statement hash and the serialization-based review hash match the catalog and frozen source metadata. No corpus contents or copied source documents are packaged here.

Miyachi's printed pages 944-947 were read. Pages 945-946 define Y^lambda=F I(lambda), state the existential rank bound n >= length(lambda), and distinguish the index-set statement as stronger. The catalog's description of the latter as an equivalent formulation should therefore not be treated as an established equivalence. Conjecture 7 has no local characteristic-zero restriction. That qualification occurs later, in the separate rational-category construction for simple Specht modules. The source's unit parameter permits q=1. De Visscher-Donkin explicitly treats that classical positive-characteristic specialization and gives quantum characteristic p, not the multiplicative order 1 of q.

The algebraically closed field used in the counterexample meets the general field setup. No omitted finite-field hypothesis, n >= r condition, or restriction to p-restricted partitions excludes the example. Stable rank n >= r is needed for the source's Schur functor, and is used only there. The existential polynomial-module assertion ranges down to n=2.

## Convention audit: a direct identification

Let p be an odd prime, r=2p-1, N >= r, E=k^N, and alpha=(r-1,1,0,...,0). In the source's conventions the module H=Sym^(r-1)(E) tensor E is polynomial injective. Multiplication m:H -> Sym^r(E) has the natural polarization section (1/r) delta, since m delta=r id and p does not divide r.

To identify its kernel without relabeling a Specht module, use the symmetric-power injective decomposition in De Visscher-Donkin, printed page 12: the multiplicity of I_N(mu) in H is the alpha-weight multiplicity of L_N(mu). Such a mu must dominate alpha, so it is either (r) or (r-1,1). The latter multiplicity is 1. The former is also 1: its alpha-weight space is contained in the one-dimensional alpha-weight space of Sym^r(E), and is nonzero because the unipotent expansion of x_1^r has coefficient r x_1^(r-1)x_2. Here the highest vector x_1^r lies in the simple socle L_N(r).

Thus H is I_N(r) direct sum I_N(r-1,1), and I_N(r)=Sym^r(E), since (r) is maximal. The split multiplication kernel is therefore isomorphic to I_N(r-1,1), by Krull-Schmidt cancellation.

The stable-rank Schur functor takes the weight (1,...,1,0,...,0) subspace. In H its basis consists of r vectors: the second tensor factor is x_j and the first is the product of all other x_i, for 1 <= j <= r. Permutations permute this basis. Multiplication maps every basis vector to the same monomial x_1...x_r. Hence F I_N(r-1,1) is exactly the augmentation kernel in k^r. There is no conjugation, sign twist, or exchange of costandard and Weyl labels in this calculation.

This kernel is simple: if a nonzero invariant subspace contains v, then v is not constant, because the constant line meets augmentation trivially when p does not divide r. For unequal coordinates v_i and v_j, subtracting the transposed vector produces a nonzero multiple of e_i-e_j. Its conjugates span augmentation. This proves simplicity over k, without enumerating finite-field vectors.

The partition (2p-2,1) is p-regular but not p-restricted: the first difference is 2p-3 >= p. Confusing these conditions would give an incorrect projectivity claim. The proof makes no such inference.

## Rank-two calculation

Set B=Sym^(2p-3)(k^2), with basis v_i=x^(2p-3-i)y^i. The subspace W with indices 0 <= i <= p-3 or p <= i <= 2p-3 is invariant: it is the image of multiplication E^(F) tensor Sym^(p-3)(E) -> B. The two monomial ranges are disjoint, so its dimension is 2p-4.

Every nonzero rational GL_2-submodule contains a monomial, by the algebraic torus weight decomposition. Translating y to y+tx and extracting coefficients reaches x^(2p-3). Translating x to x+ty reaches exactly the displayed monomials, since modulo p,

(1+t)^(2p-3)=(1+t^p)(1+t)^(p-3).

All coefficients in the second factor are nonzero. Consequently W is simple, with highest weight (2p-3,0). Coefficient extraction is legitimate over the infinite field k by Vandermonde interpolation.

The quotient has weights (p-1,p-2) and (p-2,p-1), joined in both directions by unipotent coefficients p-1. It is simple of dimension 2. A complement would have to be precisely the sum of the two corresponding weight lines in B. Translation of v_(p-2) produces a nonzero x^(2p-3) coefficient, so this sum is not invariant. The extension is nonsplit. Its simple socle and head have different highest weights, including at p=3 when both have dimension 2.

Twisting by determinant gives nabla_2(2p-2,1) with socle L_2(2p-2,1) and head L_2(p,p-1).

Separately Sym^(2p-1)(E) is simple: any monomial reaches the highest monomial, whose translates reach every monomial because

(1+t)^(2p-1)=(1+t^p)(1+t)^(p-1)

has no zero coefficient modulo p. Among **all** partitions of r dominating (r-1,1), only (r) is strictly larger; partitions with a third nonzero part cannot dominate it. The injective costandard-filtration reciprocity therefore supplies no extra section, giving

I_2(2p-2,1) is isomorphic to det tensor Sym^(2p-3)(E).

The equality concerns the genuine polynomial injective hull, not only a submodule or a representation of GL_2(F_p). Contravariant duality fixes simple labels and exchanges head and socle. The different labels above show that this injective is not self-dual. De Visscher-Donkin's projective-injective self-duality result then proves it is not projective.

For p=3, the costandard decomposition rows in order (5),(4,1),(3,2) are (1,0,0), (0,1,1), (0,0,1). Reciprocity gives projective and injective dimensions 6,4,6. The top of I_2(4,1) is L_2(3,2), whose projective cover has dimension 6, giving a second nonprojectivity check.

## The all-rank quantifier

Assume I_N(lambda) were projective for some N >= 2. The source proves that a projective polynomial injective is an indecomposable tilting T_N(mu). Its highest weight mu dominates every composition label, hence dominates lambda. Thus mu is (r) or (r-1,1), in either case a label with at most two parts.

De Visscher-Donkin's rank truncation from N to 2 explicitly sends I_N(lambda) to I_2(lambda) and T_N(mu) to T_2(mu) for these labels. Therefore I_2(lambda) would be an injective tilting, and hence projective, contradicting the rank-two calculation. This excludes every integer N >= 2, including all stable ranks.

The argument uses the stated injective and tilting truncation theorems with their label hypotheses. It does not infer generic preservation of projectivity, heads, or socles under an idempotent functor. The self-duality implication is the polynomial highest-weight result, not a claim about arbitrary finite-dimensional algebras.

Since membership in the proposed De Visscher-Donkin index set supplies a projective injective, no rank's set can contain this lambda. The stronger bridge is therefore also false. This conclusion needs only the sufficient construction, not the conjectured completeness of that classification.

## Independent computational support and limits

The independent checker uses repeated polynomial convolution, rather than the author's binomial coefficient construction, and incremental elimination, rather than the author's Gaussian-elimination implementation. It reproduces coefficient span ranks 36 and 12, simple constituent ranks 4 and 4, section-equation ranks 4 and 5, and endomorphism dimension 1.

The adjacent-transposition matrices of S_5 on augmentation generate an algebra of dimension 16 over F_3. Its scalar extension remains the full endomorphism algebra, so this finite algebra test also establishes absolute simplicity in the concrete case. A p-divides-r control at p=r=3 instead gives algebra dimension 3 below the full dimension 4. Binomial-support checks through the odd primes up to 31 agree with the family, but are not the proof for every prime.

The frozen author's 34 baseline, optimized, relocated, source/proof/data/result mutation, cache, missing/extra inventory, schema, directory, symlink and FIFO controls all passed. Both coherently repinned wrong-case and false-result data were rejected. The audit package's own 28 baseline, optimized, relocation and mutation controls also passed. Independent code passed normal and optimized execution. No assertion statement is used as an acceptance condition.

A manifest does not provide an independent authenticity guarantee against coordinated rewriting of the manifest and all code. The external archive SHA-256 is the trust anchor. These checks are not a sandbox guarantee against concurrent filesystem replacement or a malicious Python runtime. The finite calculations supplement the mathematical argument; they cannot establish the all-rank statement by enumeration.

## Literature and source inspection

A bounded current search on 6 October 2026 did not establish an earlier published resolution of this exact bridge. That is a search limit, not a novelty finding. The author's declared unpublished/proposed status is retained; this audit changes the internal mathematical verdict, not the historical literature status.

Primary references:

- Hyohe Miyachi, "Dipper's hypothesis and self-injective endomorphism rings," contribution in Representations of Finite Groups, Oberwolfach Reports 6 (2009), report 17. Definition and theorem on printed p. 945; Conjecture 7 on p. 946. https://ems.press/content/serial-article-files/46217 ; https://doi.org/10.4171/OWR/2009/17
- Maud De Visscher and Stephen Donkin, "On projective and injective polynomial modules," manuscript dated 12 January 2005; published in Mathematische Zeitschrift 251 (2005), 333-358. Definitions and reciprocity, printed pp. 6-7; symmetric powers and truncation, pp. 8-9; projective-injective duality and tiltings, pp. 10-11; symmetric-power injective decomposition, p. 12. https://openaccess.city.ac.uk/id/eprint/969/ ; author-hosted manuscript https://www.staff.city.ac.uk/maud.devisscher.1/Publications/prinjjan12.pdf

The source text and source images were inspected privately and are excluded from this audit archive. Public hashes, byte counts, URLs, page locators and verification outcomes are recorded separately.

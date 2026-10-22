# Independent audit: reduced powers on loop spaces

Problem 11100062 / AMR-110-0062. Audit date: 6 October 2026.

## Decision

**Accept the submitted packet as a correct, carefully scoped collection of partial results and diagnostic examples. The original fixed-space question remains unresolved by this work.** No mathematical correction patch is required. This is not acceptance of a full solution, a fixed-space counterexample, a novelty claim, or an exhaustive assertion about the current literature.

The reviewed author archive has 13,840 bytes and SHA-256 `5de2a4ab509186a5fdc6929079c3b710b7760afc7d271a1884a1a6158e5fb4dd`. Its manifest SHA-256 is `ab545498f9f4bd670fb277b86ba689c2d0110cacbe8f173728197bab2c16daff`. All six author files are preserved byte-for-byte under `author/` in this audit packet. This report and the acceptance record are additive; the historical author status saying that review was pending has not been silently rewritten.

## 1. Target and source authentication

The target fixes one simply connected finite CW complex X before varying the odd prime. It asks for one prime threshold, depending on X, that kills every positive reduced power in every degree of H*(ΩX; F_p). P^0 and the Bockstein are outside the claim. A prime-dependent collection of spaces cannot refute it, and a bound that depends on the input degree does not prove it.

The complete catalogue, problem collection and research-report collection were independently parsed. Each of the first two contains one target record. The exact statement hash and the default-serialization hash of the complete problem/report pair match their catalogue pins. This was a comparison with the full supplied collections, not merely with the selected record. The selected pair also agrees with the complete pair. Public hash/size evidence is recorded separately; corpus contents are excluded.

The complete third substantive entry of [Hovey's primary page](https://www-users.cse.umn.edu/~tlawson/hovey/unstable.html), after stripping markup and normalizing whitespace, agrees exactly with the complete statement including the attribution paragraph. The primary page was also independently opened on the web. Neither its historical wording nor the catalogue classification is treated as a current theorem-status certificate.

## 2. Proposition 3.1: homology generators

**Accepted, including the strict threshold 2p.** Let the direct linear dual of P^t be P_*^t; no antipode-conjugated action is being substituted. For z in H_q(Z; F_p), its image pairs with a cohomology class of degree

    k = q − 2t(p−1).

If k is negative there is no target. Otherwise the instability axiom makes P^t vanish on degree k when 2t > k. Thus a nonzero image requires

    q = k + 2t(p−1) >= 2t + 2t(p−1) = 2pt.

Consequently every positive P_*^t kills a generator of degree q < 2p. The index is 2pt, not 2t(p−1); this distinction is essential near the boundary. The unit is also killed because all positive operations vanish on H^0.

The propagation to products is valid, but it is not obtained by mistakenly identifying the Pontryagin product with the product dual to the diagonal. Let μ: Z×Z → Z be the H-space multiplication. Then xy = μ_*(x×y), naturality commutes μ_* with P_*^t, and the external Cartan identity gives

    P_*^t(xy) = Σ_(i+j=t) (P_*^i x)(P_*^j y).

The operations have even degree, so no additional sign changes the formula. On a word in the generators, a positive total index forces a positive index on some factor. Induction kills every such term. Relations among generators do not invalidate this argument: words span the algebra and the operation is linear. Homotopy associativity suffices for associativity on homology. No commutativity, primitivity, freeness, or integral torsion-freeness is required.

Degreewise finite type supplies the nondegenerate pairing used to conclude that all P^t vanish on cohomology. The hypothesis is satisfied for each loop space used in the packet. The argument also shows that the practical input is a family of homology generators killed by positive powers; the degree bound is a convenient sufficient condition for that input.

## 3. Corollary 3.2, its endpoint, products and retracts

**Accepted.** For connected Y and field coefficients, the natural Bott–Samelson tensor-algebra description gives the Pontryagin algebra on reduced H_*(Y). The generators have degree at most dim(Y), with no extra suspension shift. This yields the claimed strict inequality dim(Y) < 2p. The natural inclusion of Y by the James unit identifies the tensor-length-one classes, so it is injective in homology and induces a surjection in cohomology.

The threshold cannot be relaxed to dim(Y) <= 2p as a dimension-only statement. For Y = CP^p, a degree-two class x satisfies P^1x = x^p ≠ 0. A lift a along the James-unit pullback exists; naturality detects P^1a by its nonzero restriction. This checks both the real dimension 2p and the exact equality boundary. Each such Y depends on p, which is expressly acknowledged.

For a homotopy retract with i: Z → W and r: W → Z satisfying r i ≃ id, the map r* is injective. If P^t vanishes on W, then r*(P^t a) = P^t(r*a) = 0 forces P^t a = 0. An H-space retraction is unnecessary. The mod-p statement also passes through a p-local equivalence in the stated nilpotent finite-type setting. Finite products are handled by the field Künneth isomorphism and Cartan. No unsupported infinite-product argument is used in these corollaries.

The tensor-algebra input was checked in the cited [Büscher–Hebestreit–Röndigs–Stelzer paper](https://msp.org/agt/2013/13-1/agt-v13-n1-p05-s.pdf), proof of Proposition 4.3, printed page 143. The original Bott–Samelson proof was not independently reconstructed.

## 4. Corollary 4.1: moment-angle complexes

**Accepted with the stated no-ghost-vertices convention.** The versioned [Stanton–Vylegzhanin preprint](https://arxiv.org/abs/2506.15573v3), dated 14 January 2026, was independently checked in its current record, HTML and the supplied hash-verified PDF. Proposition 4.19 gives algebra generators of H_*(ΩDJ(K); k) in degrees strictly below 2m for every field. Its proof obtains the total-degree ceiling 2m−1 from squarefree multidegrees. The paper's standing convention excludes ghost vertices.

Apply Proposition 3.1 to ΩDJ(K). Since 2m−1 < 2p for every odd p >= m, equality p=m is permitted. There is no need to import the stronger prime exclusions used in the source's separate geometric decomposition theorem. The explicit splitting in Theorem 6.4 makes ΩZ_K a space-level retract of ΩDJ(K), so the reduced-power result transfers without requiring that splitting to preserve Pontryagin multiplication.

The finite-type condition is harmless: DJ(K), with finitely many coordinates, is simply connected and of finite type, and so is its loop homology in each degree. Z_K is a finite complex. The case of a simplex is contractible on the moment-angle side and creates no exception. With zero vertices both spaces are points, making the assertion vacuous.

A source-level typographical issue does not affect this use: the preprint's general unlooped fibration display in Theorem 6.4 has an extra loop symbol in its base, whereas the immediately following loop splitting and its DJ(K) specialization are the correct statements. The author packet uses only the explicit splitting. Independently, it follows from the standard fibration Z_K → DJ(K) → (CP^∞)^m: the loop map to (S^1)^m has a space section formed by multiplying the coordinate circle inclusions in ΩDJ(K). This identifies the loop space, as a space, with its fiber times the torus. The no-ghost-vertices assumption ensures the coordinate inclusions are available.

No Bockstein conclusion is licensed by this proof. No general finite-complex generation theorem is inferred from this special commutative-algebra input. The external Backelin–Roos result underlying Proposition 4.19 remains a cited theorem rather than an independently reproved one.

## 5. Proposition 5.1: Eilenberg–Moore degree window

**Accepted; filtration extensions do not invalidate this particular argument.** Put w = d−r−1 >= 0. The relevant filtration is increasing in bar length:

    0 = F_(−1) ⊆ F_0 ⊆ F_1 ⊆ … ⊆ H*(ΩX; F_p).

Each F_s is stable under the Steenrod action. This is the actual filtration of the abutment, not merely an action on an early page. The cited [Menichi paper](https://arxiv.org/abs/math/0101221), page 2, explicitly states the Steenrod-module filtration and strong convergence; the page was independently visually inspected as well as read in extracted text. Its reduced bar support produces total degrees between rs and (d−1)s at length s. The shift subtracts one for every bar factor.

Two support consequences require distinct arguments:

1. In degree q > (d−1)s, every graded piece of length 0 through s vanishes. Inducting from F_(−1)=0 gives F_s^q = 0. This step handles possible lower-filtration extensions rather than disregarding them.
2. At input degree n, all graded pieces of length greater than floor(n/r) vanish. Since r >= 1, strong convergence and degreewise boundedness make the increasing filtration exhaustive and eventually constant in that degree. Thus H^n = F_floor(n/r)^n.

For a in degree n and s=floor(n/r), P^t a belongs to F_s in degree n+2t(p−1). It therefore vanishes when that degree exceeds (d−1)s. Writing n=rs+u, 0<=u<r, gives the exact identity

    (d−1)s − n = (d−r−1)s − u = ws − u.

For 0<n<=N, this is at most w floor(N/r); every t>=1 is covered by the displayed sufficient bound on 2(p−1). H^0 is handled by instability. If n<r, positive cohomology is already zero; no division-by-zero or length-zero exception is concealed. The assumptions d>=r+1 and r>=1 are used explicitly. When d=r+1, w=0 and the bound applies uniformly for every odd prime.

A filtration-preserving operation cannot raise the increasing length index here, because it maps F_s into F_s. It may lower that index. Therefore triviality on the associated graded alone would not suffice. The accepted proof is stronger: it eliminates every possible filtered target in the relevant total degree. There is no assumption of spectral-sequence collapse, and no unproved lifting of a graded zero to an actual zero.

**Endpoint check.** The packet's own example X=Σ²CP^p, with r=N=3 and d=2p+2, satisfies

    2(p−1) = (d−r−1) floor(N/r),

yet P^1 is nonzero on degree three. Hence changing the strict greater-than sign to greater-than-or-equal-to would be false. This is an additional audit observation, not a new approach to the unresolved global question.

When w>0, the sufficient prime bound grows with N. The deduction for every fixed finite degree window cannot be exchanged with a claim of one bound for all degrees. This quantifier limitation is accurately stated by the author.

## 6. Proposition 6.1: cup powers versus reduced powers

**Accepted.** CP^p is simply connected, with its first positive cell in degree two and its top cell in degree 2p. Two reduced suspensions give X_p=Σ²CP^p with first positive cell in degree four and top cell in degree 2p+2; it is 3-connected. For odd p>=3,

    2p+2 <= 3p.

The Anick cup-power theorem, in the precise form restated on page 1 of Menichi's paper, therefore applies with r=3 and kills positive-degree pth cup powers in H*(ΩX_p; F_p).

Set Y_p=ΣCP^p. Suspension isomorphisms are isomorphisms of modules over stable cohomology operations, so P^1(σx)=σ(P^1x)=σ(x^p), a nonzero class of degree 2p+1. The degree is 3+2(p−1), as required. This computation does not identify σ(x^p) with the pth cup power of σx: the latter is zero, and confusing them would invalidate the example.

The James unit Y_p → ΩΣY_p induces a cohomology surjection in degree three by its tensor-length-one homology injection. A lift of σx exists, and naturality detects its nonzero reduced power. No transgression is assumed to be injective or to produce arbitrary lifts. Stability is used only across ordinary reduced suspension; the lift is supplied by Bott–Samelson.

This disproves the proposed general upgrade from cup-power vanishing to vanishing of all reduced powers, even within the stated connectivity-dimension range. It does not refute Hovey's fixed-X assertion. In fact, fixing the index p of this example and then varying a new prime ℓ gives vanishing for sufficiently large ℓ by the suspension corollary, consistently with all statements in the packet.

## 7. Remaining gap and literature scope

The large-prime decomposition statement used for rationally elliptic finite X was checked in Anick's 1992 Theorem 6 and Stanton's discussion. Finite-dimensional rational homotopy is a substantive hypothesis; finite-dimensional X alone is insufficient. This review relies on those precise published restatements and does not claim direct proof verification of the inaccessible original 1986 paper.

The [Anick torsion construction](https://msp.org/pjm/1986/123-2/pjm-v123-n2-p01-s.pdf) was independently checked on printed pages 257–260. It rules out blanket eventual integral loop-homology torsion-freeness for finite simply connected complexes. It supplies no nonzero reduced power and is correctly used only to block a route, not to answer the original question.

The five-approach ledger records the expected partial disposition: a valid special-class result, a bounded-degree theorem, a genuine diagnostic family, and the unresolved uniformity gap. An Adams–Hilton chain algebra having finitely many generators is not a homology-generation theorem. Rational localization does not automatically control all integral primes in all loop degrees.

Current-source checks were deliberately bounded. The Southampton repository's indexed metadata independently confirms the August 2025 thesis. Direct record/PDF requests in this review returned 403; its complete PDF was not read, and the author's reported indexed Conjecture 1.3 excerpt was not independently recovered. This is a provenance limitation, not evidence that the reported excerpt is false. It is not used as proof of global openness. The original packet already identifies the thesis as limited, older status evidence.

A further [April 2026 paper by Stanton and Vylegzhanin](https://arxiv.org/abs/2604.25344), on colimit descriptions of polyhedral-product loop homology, was located during this review. Its abstract, introduction and occurrence of the Steenrod discussion were inspected in the current HTML. It directs that discussion back to the earlier paper; no general solution was identified in the inspected material. The full 29-page paper was not proof-audited. Accordingly, the January 2026 source is the current inspected version of the cited generator theorem, not a claim that it is the latest work in the whole subject.

The author's bounded repository-search account was inspected, but a fresh repository-wide search was not independently repeated in this audit. No priority conclusion depends on it. The only accepted global status is that the present investigation does not resolve the original question.

## 8. Integrity, negative controls and release safety

The author archive contains exactly six regular UTF-8 Markdown/JSON files. There is no code, notebook, executable checker, binary payload, PDF, raw source text, dataset record, or private coordination file. Every manifest byte count and SHA-256 was checked, and ZIP CRC checks passed. All seven downloaded-public-source hashes and sizes match the supplied metadata.

A separate private, standard-library-only integrity helper was run with `python -I -S`, with `python -I -S -O`, and in relocated copies under both modes with hostile local shadow modules. All four outputs were identical. The helper does not import or execute any archive content and uses explicit exceptions rather than assertions for validation. It is not included in the release.

Each mode rejected twelve malformed controls: outer-size/hash modification, truncation, duplicate member, unexpected code member, parent traversal, absolute path, symlink entry, changed authored content, missing member, incorrect manifest length, a forged full-solution flag with a refreshed member hash, and duplicate JSON keys with a refreshed member hash. The symbolic degree identity also received 86,688 finite integer sanity checks. These tests establish byte integrity and limited arithmetic consistency; they do not certify topological theorems computationally.

All mathematical proofs were reviewed as proofs. No correction was needed, so there is no fabricated patch or correction replay. The original author freeze remains unchanged. The acceptance record explicitly retains unresolved status, five of five approaches, no fixed-space counterexample, no novelty claim, and no publication performed by this review.

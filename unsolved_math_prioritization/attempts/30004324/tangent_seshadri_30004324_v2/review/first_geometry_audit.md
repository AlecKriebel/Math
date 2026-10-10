# Independent adversarial audit: tangent-Seshadri candidate 30004324

Audit date: 2026-10-05. This report concerns the exact frozen author candidate identified below. It is an AI-assisted mathematical audit, not external peer review, formal proof verification, or a historical priority certificate.

## Verdicts

- **Mathematical proof: PASS.** This first independent audit found no essential mathematical gap in the five-lemma argument. The arbitrary fixed point and arbitrary characteristic are retained. The new bridge to Picard number one and Fano is justified below, including the compressed coarse-space step.
- **Original integrity verifier: REVISE_REQUIRED.** A reproducible extra-file bypass exists: an unexpected nested file named `MANIFEST.json` is ignored. This does not change any mathematical conclusion and was not present in the actual frozen archive. A strict replacement and independent negative controls accompany this report.
- **Actual author freeze: PASS.** All 13 archive files match the author directory byte for byte, including the manifest; all supplied external hashes match. No source PDF, extracted source text, or dataset is in that archive.
- **Publication posture:** independently checked candidate, awaiting further specialist scrutiny. This audit does not turn a manuscript into an accepted resolution. The unrestricted statement is still presented as a conjecture in the independently retrieved 2025 toric paper.

If a single packet-readiness label is required before repair of the original verifier, use **REVISE_REQUIRED (integrity tooling only)**, not mathematical failure or a partial proof. No proof-level revision is required by this audit. The explanatory insertions in Sections 4 and 5 are recommended for a self-contained exposition.

## 1. Exact binding and target

Author archive: `TANGENT_SESHADRI_30004324_AUTHOR_SAFE_FREEZE.zip`.

- Bytes: 19,163
- SHA-256: `6483242536c534a84072815ae4c3aa9de57fd2769386eb2e5e1ad85041cc6a01`
- Root author manifest SHA-256: `4869e62250a25e64fc6e4096ea56842a7b23400789f3ba00c14ba81c2c8cd8f7`
- `candidate_proof.md`: 10,612 bytes; SHA-256 `eb96aab30ab17aca553ef83102145c5dd51b2c36895be2b2a028f5090b9aedc1`
- `audit_questions.md`: 1,969 bytes; SHA-256 `eea2e20cc94286d6e29286da48e10832c53e3bf25e1bffc0922b401bc56bc2d7`

Both the proof and audit questions were read completely before forming a verdict. The author freeze was not edited.

The target is: for a smooth integral projective n-fold X over an algebraically closed field k, positivity of the Fulger–Murayama relative tangent-bundle Seshadri constant at one closed point x implies X is isomorphic to P^n. No Fano, nef-tangent, characteristic-zero, or general-point hypothesis is added.

The exact target was independently recovered from the OWR contribution, printed page 3289, and the research paper, Conjecture 4.9. The 2019 arXiv numbering is 5.9. The [primary OWR report](https://publications.mfo.de/bitstream/handle/mfo/3816/OWR_2019_53.pdf?isAllowed=y&sequence=1) and [published-layout manuscript](https://par.nsf.gov/servlets/purl/10198624) were freshly downloaded and inspected. Version numbering must not be mixed.

## 2. Dependency audit

The essential imported results have the following scopes.

1. **Normalized-curve slope formula.** FM21 Example 3.20 and Corollary 3.21 apply to a coherent sheaf on a projective scheme over an algebraically closed field. No global nefness is assumed. Positive characteristic uses normalized Frobenius minimal slope. Its specialization to split bundles on P^1 is exact.
2. **Rational curve through the specified point.** FM21 Corollary 4.6 assumes smoothness, projectivity, and positivity at some closed point over an algebraically closed field. Its proof explicitly produces a rational curve through that point, rather than merely through a general point.
3. **Fano conclusion.** FM21 Proposition 4.8(1) assumes smooth projective Fano X and the same positivity at some point; it has no characteristic restriction. The characteristic-zero general-point clause is a distinct alternative (2) and is not used. The proof of (1) invokes Mori's characterization, not Conjecture 4.9. These three FM dependencies were checked directly in the [research manuscript](https://par.nsf.gov/servlets/purl/10198624), pages 9–10 and 16–17.
4. **Stable maps.** [Abramovich–Oort](https://arxiv.org/pdf/math/9808074), Theorem 2.8 and Section 2.5, provide the proper finite-presentation Artin stack of fixed degree stable maps into a projective finite-presentation target, with finite stabilizers and projective coarse moduli scheme. Set the base to Spec k, genus to zero, number of marks to one, and use the embedding defined by A. The entire stack need not be Deligne–Mumford in characteristic p.
5. **Coarse restriction.** [Conrad, Theorem 1.1 and Section 2](https://math.stanford.edu/~conrad/papers/coarsespace.pdf), supply the finite-inertia coarse-space facts used below: properness and compatibility with flat base change, in particular restriction to an open coarse subspace. [Stacks, Proposition 94.13.3](https://stacks.math.columbia.edu/tag/03YR) identifies an algebraic stack with trivial inertia as an algebraic space. No arbitrary non-flat coarse-space base change is assumed.
6. **Deformations.** For a fixed smooth proper source curve and smooth target, H^1 of the pulled-back tangent bundle, with the prescribed points subtracted, is an obstruction space. Its vanishing gives smoothness of the appropriate Hom/evaluation morphism. This applies in every characteristic. The cohomological evaluation calculation is also explicitly used in [Gounelas, Proposition 4.7](https://ems.press/content/serial-article-files/26314?nt=1), printed page 299. The audit gives the exact pointed calculation in Section 5.
7. **Descent.** Proper flat finite-presentation morphism, geometrically connected P^1 fibers, and an invertible sheaf of fiber degree zero give a rank-one pushforward and an isomorphic adjunction pullback. The H^0=1, H^1=0 calculation proves this by cohomology and base change. Alternatively, the candidate's reduced base meets [Stacks, Lemma 37.33.2](https://stacks.math.columbia.edu/tag/0BEZ), with universal pushforward of the structure sheaf supplied by [Lemma 53.20.12](https://stacks.math.columbia.edu/tag/0GKA).
8. **Ampleness.** Ampleness of Cartier divisors on a projective variety is numerical, in arbitrary characteristic. Equivalently, apply the Nakai–Moishezon criterion to the positive rational multiple of A obtained in Section 7. The any-characteristic scope is also explicit in [Fujino–Miyamoto, Theorem 1.3](https://www.math.kyoto-u.ac.jp/~fujino/Nakai-Moishezon3.pdf). This is not a nef-plus-positive-on-some-curves shortcut.

The audit accepts published theorems as mathematical inputs after checking their statements and hypotheses. It does not claim to have newly proved all the foundational theorems behind those inputs, or to have independently inspected the complete Kollár monograph. The exact Fano statement needed here is independently stated and proved in FM21, which suffices as the cited dependency.

## 3. Lemmas 1–2: positivity and all pointed boundaries

### 3.1 Splitting and normalization

Let C be an integral rational curve through x, and f:P^1→X its normalization map. Write f*TX as the sum of O(a_i). The curve formula gives min(a_i) ≥ mult_x(C)·epsilon(TX;x)>0. Consequently every a_i≥1, hence f is very free. Frobenius multiplies every splitting degree by p^e, so dividing the minimum by p^e gives the same minimum. There is no substitution of the characteristic-zero slope criterion on an arbitrary curve.

Because f is birational onto C, it is an isomorphism over a nonempty smooth open subset of C. Its differential is therefore generically nonzero even in characteristic p. A nonzero map O(2)→f*TX requires some a_i≥2. Thus -KX·C≥n+1. The argument needs only its weaker positive-degree consequence later.

The differential conclusion is deliberately restricted to normalization maps. A purely inseparable multiple cover can have zero differential; this does not contradict the proof and is separately excluded by the degree argument.

### 3.2 Absolute minimality

Choose very ample A. The existence input makes the set of positive integers A·C, for rational images through x, nonempty. Its minimum d exists. This minimum is over **all** such images, not just one irreducible family and not just very free maps chosen in advance.

Consider a one-pointed degree-d stable map evaluated at x. The arithmetic-genus-zero nodal source has a tree dual graph and P^1 components. If the mark is on a contracted component, every contracted component in the connected contracted cluster containing it maps to x. A first nonconstant component reached from that cluster has image containing x: the attaching node maps to x. A nonconstant image of P^1 is rational by Lüroth's theorem, also in positive characteristic.

For this distinguished component, write the total field-extension degree onto its image as e≥1, including any inseparable degree, and the image's A-degree as c≥d. All other active components have strictly positive A-degree contributions. Thus

    d = e c + (sum of other positive contributions) ≥ e c ≥ c ≥ d.

Equality forces e=1, c=d, and no other nonconstant components. This also disposes of multiple covers with the same image, and multiple active components whose images coincide.

With exactly one active vertex, every connected contracted subtree meets it at exactly one edge. A subtree of t>0 contracted vertices and m≤1 marks has 2(t−1)+1+m≤2t special-point incidences. Stability would require at least 3t. This is impossible. Therefore no contracted component remains, and the source is smooth irreducible P^1 with birational map.

**Geometric-field qualification.** Minimality initially refers to k-curves. A lower-degree rational image over an algebraically closed extension K would give a K-point of the finite-type degree-c Hom scheme with 0 mapped to x, for c<d. A nonempty finite-type scheme over algebraically closed k has a k-point. Its image is a rational curve through x of degree at most c, contradicting d. Thus extending geometric residue fields does not defeat the argument. Equivalently, it is enough to rule out every closed point of a putative finite-type boundary.

### 3.3 Genuine negative examples checked

A contracted component carrying two marks and one attaching node is stable. A contracted component carrying one mark and joining two active components is also stable. Neither is a counterexample: the former belongs to a two-pointed compactification; the latter requires extra positive degree. The proof only eliminates boundaries in the one-pointed degree-d evaluation fiber. It never says that the two-pointed stable-map space has smooth domains everywhere.

**Verdict for Lemmas 1–2: PASS.** No contracted-mark escape, inseparable-cover escape, or omitted lower-degree-family escape remains.

## 4. Lemma 3: full scheme/projectivity justification

This is the most compressed sentence in the candidate and deserves expansion. The following supplies a complete route rather than assuming coarse spaces commute with taking a closed fiber.

Let M be the proper Artin stack of genus-zero, one-pointed A-degree-d stable maps to X, and q:M→S its projective coarse moduli scheme. Evaluation ev:M→X factors through a map of algebraic spaces S→X by the coarse universal property. Set M_x=ev^{-1}(x). It is proper and nonempty.

At every geometric point of M_x the map f is birational from P^1. An ordinary automorphism preserving f acts identically on the dense open where f is an isomorphism, so is the identity. An infinitesimal automorphism is a vector field on P^1 vanishing at the mark, killed by df. Since df is generically injective and a vector field cannot be nonzero only on a finite set, this vector field is zero. The finite stabilizer group scheme therefore has a single geometric point and zero tangent space. A nontrivial finite local group scheme would have a nonzero cotangent space at the identity by Nakayama; hence the stabilizer is the trivial group scheme. Counting only automorphism k-points would not have sufficed.

The stack M has finite inertia I→M. The locus W where this inertia is the identity is open. One way to see this is to use the identity section to split the finite pushforward algebra as O_M plus the kernel of augmentation. The latter is coherent, and its support is closed; outside its support the inertia is exactly the identity. All of M_x lies in W. This argument also excludes hidden infinitesimal inertia over a nonreduced base.

The coarse map q is a proper universal homeomorphism on the underlying stack topology, so W is the inverse image of an open V⊂S. By flat base change for coarse moduli along the open immersion V→S, W→V is a coarse morphism. But W has trivial inertia, hence is already an algebraic space. The universal property makes W→V an isomorphism.

Now M_x is a closed substack of W and therefore a closed subscheme of V. In particular it is a scheme. Its composite immersion into the projective scheme S is proper: M_x is proper over k and S is separated over k. A proper immersion is a closed immersion. Thus M_x is projective. This uses only open/flat coarse restriction; the possibly invalid closed-fiber coarse base change is unnecessary.

Take the reduced irreducible component H containing the chosen point. It is integral projective. Restrict the universal stable curve to obtain U→H, with its actual marking section σ and evaluation e. The universal curve is projective and flat of finite presentation. Every geometric fiber has just been shown to be smooth P^1, so the morphism is smooth. U is an integral projective variety: smoothness gives reducedness over the reduced base, and flatness plus geometrically integral fibers gives irreducibility.

Degrees of pullbacks of line bundles from X are locally constant in this flat proper family, since degree is determined by the Euler characteristic on its genus-zero fibers. They are constant on connected H. The marking satisfies e∘σ=x as a morphism, not just on a dense set.

**Verdict for Lemma 3: PASS.** The scheme and projectivity claims are correct. The explicit paragraph above is an expository strengthening, not an additional geometric assumption or unresolved essential lemma.

## 5. Lemma 4: deformation on the correct component

Put E=f*TX. For distinct source points 0 and infinity, with f(0)=x,

    H^1(P^1,E(-0-infinity)) = direct sum H^1(P^1,O(a_i-2)) = 0,
    H^1(P^1,E(-0)) = direct sum H^1(P^1,O(a_i-1)) = 0.

The second equality makes Hom(P^1,X;0↦x) smooth at f. The exact sequence

    0 → E(-0-infinity) → E(-0) → E|infinity → 0

makes the evaluation differential H^0(E(-0))→E|infinity surjective. Deformation theory, or the smooth-source/smooth-target differential criterion, makes evaluation at infinity smooth at f. No generic-smoothness theorem is invoked.

The group Aut(P^1,0) is a smooth two-dimensional group in all characteristics. Its action here has trivial scheme-theoretic stabilizer. Smooth pointed P^1 families with a section are locally trivial for this purpose, so quotienting gives the smooth-source locus of the pointed stable-map stack. Hence the pointed Hom scheme maps smoothly to M_x near f. Smoothness of the Hom scheme implies smoothness of M_x at [f,0], so that point lies on a unique local irreducible component. The nearby Hom maps therefore land in the chosen H, not an unidentified component.

Evaluation at infinity lifts those maps to points of the ordinary universal curve U. Its image in X contains a nonempty open subset, because the Hom evaluation is smooth at f and hence open near f. Properness of U makes e(U) closed. Since X is irreducible, a closed subset containing a nonempty open subset is all of X. Therefore e is surjective.

At the marking section the evaluation is constant; smoothness there is neither asserted nor needed. Nor is the universal curve confused with the open space of pairs of distinct markings. One can identify it with a stabilized two-marked construction, but the resulting ghost at collision does not change the one-pointed source family used here.

For a dimension check, if b=-KX·C then dim H=b−2 locally at f, and dim U=b−1. The bound b≥n+1 is consistent with surjective evaluation. The proof does not secretly assume dim H=n−1 or that e is generically finite; neither is needed.

**Verdict for Lemma 4: PASS.** The fixed point may be special. Positive characteristic causes no separability gap because smooth evaluation is proved directly at the very free map.

## 6. Lemma 5: numerical Picard reduction

Let D be any Cartier divisor on X. Write b=D·C for a fiber image. Since all fiber maps are birational, this is the degree of e*O_X(D) on a fiber and is constant on H. Set

    L = O_X(dD) tensor A^(-b).

The restriction of e*L to any fiber has degree db−bd=0. A degree-zero line bundle on P^1 is trivial. Cohomology and base change apply because π:U→H is proper and flat and e*L is invertible, hence flat over H. On every fiber the cohomology dimensions are h^0=1 and h^1=0. Consequently B=π_*(e*L) is a line bundle and the adjunction π*B→e*L is an isomorphism, as can also be checked on every fiber followed by Nakayama.

Pulling back along σ gives

    B = σ*π*B = σ*e*L = (constant map to x)*L,

which is the trivial line bundle tensored with the one-dimensional vector space L_x. Thus e*L is actually trivial, stronger than numerical triviality.

To test L against an arbitrary integral curve Γ⊂X, take an integral component Z of e^{-1}(Γ) dominating Γ. Such a component exists because e is proper surjective. A sufficiently general sequence of ample hyperplane cuts yields a complete curve in Z with at least one integral component Γ' dominating Γ. More explicitly, the generic fiber has dimension dim Z−1, and that many hyperplane cuts have positive finite degree on it; hence a horizontal curve component survives. No smoothness or separability of Γ'→Γ is required. After normalization the map has finite positive total degree q, possibly divisible by the characteristic. The projection formula gives

    0 = deg(e*L|Γ') = q·deg(L|Γ).

These are ordinary integers, not elements of k, so characteristic p does not turn q into zero in the equation. Therefore L·Γ=0 for every Γ. It follows that d[D]=b[A] in N^1(X)_R. Since A has nonzero numerical class and n≥1, the Picard number is exactly one.

This is the required bridge from a covering family to numerical generation. It does not infer Picard rank one merely from coverage, rational connectedness, or the presence of one very free curve. The contracted global section and the proper P^1 family are indispensable.

**Verdict for Lemma 5: PASS.** The line-bundle descent and numerical descent both hold in the precise setup used.

## 7. Fano reduction and final cited theorem

Use D=-KX. Its degree on the normalization of C is the sum of the positive a_i, so b>0. Lemma 5 gives -KX numerically equivalent to (b/d)A. For any positive-dimensional integral subvariety Z of dimension r, the top intersection is therefore

    (-KX)^r·Z = (b/d)^r A^r·Z > 0.

Nakai–Moishezon makes -KX ample; equivalently one may use numerical invariance of ampleness directly. Smoothness ensures KX is Cartier. The proof has now established the missing Fano hypothesis rather than assumed it. Applying the established FM21 Proposition 4.8(1) gives X≅P^n. Clause (2), with its general-point and characteristic-zero restrictions, is unused.

For n=1, deg TX=2−2g independently gives the same result. If dimension zero is admitted, an integral smooth projective zero-fold over an algebraically closed field is a point.

**Verdict: PASS.** The conclusion follows from the candidate's unchanged hypotheses and the checked dependencies.

## 8. Countermodel search and scope checks

- **Products:** a ruling in P^a×P^b has a trivial tangent quotient of positive rank, so cannot satisfy the positivity hypothesis. They do not refute the Picard reduction.
- **Very free curves alone:** the (1,1) curves in P^1×P^1 have ample pulled-back tangent bundle. They are not absolute minimal-degree rational curves through x for O(1,1); rulings have smaller degree. Their compactified family acquires reducible members. This refutes two tempting weakened versions of the argument, but neither is the candidate's statement.
- **Blow-ups of projective space:** on the exceptional locus the normal quotient has negative degree. Outside it, a strict transform of a line meeting the center has anticanonical degree at most n, contrary to the necessary n+1 bound. These familiar higher-Picard-rank spaces fail the starting hypothesis.
- **Inseparable maps:** a p-fold Frobenius cover has zero differential but mapping degree p>1, so is excluded by the minimum-degree equality. Birational normalization maps remain generically separable onto their image.
- **Singular targets:** the candidate requires smooth X. The singular toric counterexample in [Chang's paper](https://arxiv.org/pdf/2211.17172v2) concerns a different hypothesis and does not invalidate this proof.
- **Two-marked ghosts:** real, accepted by controls, and irrelevant to the claimed boundary-free one-marked evaluation fiber.
- **Coarse moduli in characteristic p:** arbitrary closed base change is not used in the supplied complete justification.
- **General-point substitutions:** none. Every evaluation and minimum is anchored at the given x.

No countermodel satisfying the exact hypotheses and contradicting an essential step was found. This negative finding is an audit result, not an exhaustive classification claim independent of the proof.

## 9. Computational and integrity checks

The frozen author's 909,136 numerical/graph assertions and ten integrity controls were rerun successfully. Their significance is limited to the identities and finite cases they implement.

A separately written checker enumerates labeled trees by edge subsets rather than the author's Prüfer construction. It checks 50,069 one-mark/one-active configurations across 1,442 trees, the minimum-degree bookkeeping, 3,905 positive splitting cases, and 6,525 blow-up numeric cases. It has 85,247 bounded mathematical-control assertions, including genuine negative controls. Every one passes.

None of these finite calculations proves stable-map properness, descent, deformation smoothness, numerical ampleness, the Fano characterization, or the conjecture. The mathematical verdict rests on Sections 2–7.

The new strict manifest verifier rejects 14 independent mutations and accepts the clean fixture. In particular it rejects an extra nested `MANIFEST.json`, which the original verifier incorrectly accepts. The actual frozen author archive separately passes this stricter verifier. See `STRICT_INTEGRITY_FINDING.md` for the exact issue and correction.

## 10. Recommended next review

A fresh specialist should first read the candidate independently and attempt to break absolute pointed minimality, characteristic-p stabilizers, the correct-component deformation argument, and the global contracted-section descent. The fully expanded proof above should then be compared with that independent assessment. The 2025 source's continued conjectural framing warrants unusually careful scrutiny; it is not by itself a mathematical objection.

No source text, source PDFs, raw datasets, or private coordination records are included in this audit packet. Bibliographic information, public URLs, hashes, byte counts, inspection history, original analysis, and reproducible controls are included.

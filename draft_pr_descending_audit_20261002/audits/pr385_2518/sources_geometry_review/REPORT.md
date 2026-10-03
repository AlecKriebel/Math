# Independent primary-source and Turn 4-5 audit of PR 385

Frozen head: `fd4a71f2f7e08ece5f0d34d9d0df3fb6f460d8bf`.

**Scoped finding: PASS.** The primary problem reconstruction and the universal Turn 4-5 proofs are valid on the audited assumptions. No mathematical repair is requested. This is a verification of partial results; the original question remains **unsolved, 5/5 author turns**, and no historical novelty or solution paper is certified. This report does not assess readiness to merge; the parent audit's PR 386-before-385 order remains applicable.

## Inputs, source order, and independent evidence

Work began with independently fetched primary PDFs, before candidate conclusions and historical review. I read and visually inspected the complete Kourovka printed/physical p.177, the article pp.18 and 53, and Nikolov-Segal printed p.172 (physical p.2). I additionally read the article conventions, pp.27-28 (the discrete comparison), p.30 (the automorphism epimorphism) and p.52 (the neighboring problem), plus the candidate Turn 1-3 dependencies and complete Turn 4-5 mathematics. Only after reconstructing these claims and designing independent controls did I read the historical review and final wrapper.

All 45 frozen files match the external snapshot manifest's byte lengths and SHA-256 hashes. This check includes the target queue snapshot without changing it. `frozen_hash_receipt.json` records every binding. The snapshot manifest itself, the frozen source manifests, the privately copied code, the outputs, and the source downloads are bound in the audit receipts.

Four independent primary PDF downloads reproduce the historical PDF bytes exactly:

| Primary PDF | Bytes | SHA-256 |
| --- | ---: | --- |
| October 2026 Kourovka full edition | 1,881,857 | `31baec1b36ec3a956e787355eccfffa2e89df5b1fe31b22a3123377d8103baab` |
| October 2026 updates | 510,255 | `82068f0185495805184c806b296db3481764828f36f6e956ef0c41215e426195` |
| Barnea et al. v3 | 607,670 | `46bde3892cce8a7a6ea908ce21aca199cd5c3c6795510ae456c373b50859f15c` |
| Nikolov-Segal 2007 | 1,293,579 | `53f155d07e92ae243bdae722f3d535dedcd66bfd1a3dacbdd654e3ea577a344a` |

Source URLs, retrieval times and HTTP evidence are in `source_fetch_receipts.json`. The current text extraction matches the historical updates text, but not every other historical extraction. Those differences do not undermine byte-identical PDFs; extraction depends on tooling and fonts. Historical page PNG bytes were not reconstructed or certified. New renderings supplied visual source checks, not a claim of historical screenshot identity. `historical_source_comparison.json` makes these distinctions explicit.

## Exact original target and topology

For every prime p and every finite-rank free pro-p F with rank d>=2, the problem asks for a finite open-subgroup family U containing F for which

    {K <= F : K <= U_i, and alpha(K)=K for all alpha in Aut(U_i), all i} = {1}.

This is the same target on Kourovka p.177, Problem 21.9, and [Barnea et al. v3](https://arxiv.org/pdf/2507.04120v3), p.53, Question 4. The Kourovka entry is unannotated and the October update contains no standalone 21.9 entry. I have not treated the absence of a later verified solution as a novelty proof.

The quantified K is not restricted to closed subgroups. The ambient profinite convention uses continuous automorphisms. [Nikolov-Segal](https://annals.math.princeton.edu/wp-content/uploads/annals-v165-n1-p05.pdf), Theorem 1.1, applies because F and each open U_i are topologically finitely generated. An abstract automorphism pulls open finite-index subgroups back to finite-index subgroups, which are open by strong completeness. It is therefore continuous, as is its inverse. Hence the abstract and continuous automorphism groups coincide here.

For a common characteristic K, every U_i is closed and every ambient automorphism is a homeomorphism. Thus closure(K) stays inside all U_i and remains characteristic in each. K=1 exactly when closure(K)=1. This proves equivalence of the all-K and closed-K versions without asserting K itself is closed. Since F belongs to the family, K and its closure are normal in F.

The article's Observation 6.10 is a discrete-free-group result for certain ranks. Its p.28 expressly leaves the free-pro-p analogue unknown. Its Proposition 12.2 concerns invariance under finitely many individual automorphisms, which does not replace invariance under every automorphism of each finite open-domain family. Neither neighboring result supplies the requested family.

### Harmless source typo

The article p.16 prints the Schreier formula with rank(F) where rank(F)-1 is required. The parent pointed out this typo; I independently confirmed the displayed source formula. The candidate uses the correct formula, `1+[F:U](d-1)`. In the index-p case its explicit basis has one generator x_1^p and p(d-1) conjugate generators, independently giving `1+p(d-1)`. More generally a connected m-sheeted covering of a rank-d rose has md edges and m vertices, so its free rank is md-m+1. The candidate's rank calculation must be justified by these facts, not by blindly copying the misprinted formula. No candidate repair follows.

## Turn 4: universal normal-containment proof

The external input is exactly article Theorem 3.11 on p.18, credited there to Lubotzky's Theorem 3.2 and Ribes-Zalesskii's Theorem 9.1.19. It applies to a **closed, topologically finitely generated** subgroup H of finite-rank free pro-p F, producing an open V in which H is a free pro-p factor. The theorem is credited, not reproved.

If H also has infinite index, write V=H*B. B is nontrivial: otherwise H=V would be open. It is a finitely generated free pro-p group, because it is a free factor and quotient of finite-rank V. A nontrivial such B has a quotient C_p. Choose b mapping to a generator.

Suppose a nontrivial subgroup N normal in F lies inside H. Pick a!=1 in N. Normality in V puts bab^-1 in H. The free-factor retraction r:V->H kills B, fixes H, and satisfies r(bab^-1)=a. Because bab^-1 already lies in H, this implies bab^-1=a as actual elements of V.

Residual finiteness of the pro-p H gives a continuous finite p-group quotient P with nonidentity image a_bar. Map H to the coordinate-zero lamp of P wr C_p and B to its cyclic shift. The free-pro-p product's universal property extends these continuous maps to V. The two elements a and bab^-1 map to the same nonidentity lamp on distinct coordinates, so are unequal. This contradicts the retraction consequence. The proof does not invoke an abstract free-product normal form, and never requires N to be closed or finitely generated.

For the pair {F,U} with [F:U]=p, the independently checked Turn 1 lattice mechanism confines any common characteristic K to U'. Consequently closure(K) is a nonopen normal subgroup. The normal-containment theorem proves exactly that a nontrivial survivor has infinitely generated closure and cannot be confined to any closed finitely generated infinite-index container. It also excludes finite abstract generation of K, because the closure of finitely many abstract generators is topologically finitely generated.

The finite-normal-generation comparison is correct. The closed normal closure of the finitely many basis commutators is F': after imposing those relations the basis images commute, and the free-pro-p abelianization is Z_p^d. F' is nontrivial (finite noncommuting Heisenberg generators witness this), infinite-index, and therefore not topologically finitely generated. It is not asserted to be common characteristic in U, and Turn 3's explicit commutator prevents that interpretation. Finite normal generation or a finite quotient presentation does not activate Hall's finitely generated-container hypothesis.

Boundary audit: H=1 only permits N=1; if H is open the theorem's infinite-index hypothesis fails and nontrivial normal cores can be contained in H; if N is not normal then conjugation need not remain in H; nonclosed H is outside Hall's hypothesis. The proof retains all these distinctions, including p=2.

## Turn 5: exact comparison proofs

### Scalar lattices

The Turn 1 coordinate-extraction lemma is valid for arbitrary additive subgroups in rank at least two. Invariance under all p-adic transvections extracts arbitrary multiples of each coordinate; coordinate permutations produce a Z_p ideal I with M=I^d. A nonzero ideal contains an element of minimal finite valuation, hence is p^a Z_p. Thus a common characteristic nonzero K in A=Z_p^d and in each open U_i satisfies K=p^a A=p^{b_i}U_i. Comparing lattices gives U_i=p^{a-b_i}A, with a-b_i>=0. Conversely finitely many scalar lattices share the nonzero power lattice at their largest exponent. The rank-one assertion is separately justified: all open subgroups are powers, so the smallest member of any finite family supplies a common characteristic subgroup. No rank-two lemma is silently applied in rank one.

For the original nonabelian free-pro-p F, this comparison governs an abelianized image of K only; vanishing of that image does not imply K=1.

### P-adic Heisenberg group, every prime and every open family

The UT_3(Z_p) coordinate multiplication, inverse and commutator formulas are correct. The inverse limit of UT_3(Z/p^e) is pro-p. The two elementary unipotents generate topologically: their commutator supplies the central direction, and x^a y^b z^{c-ab} supplies any triple by continuous p-adic powering. This works at p=2 as well as odd primes. The group has nilpotency class two and cannot be a nonabelian free pro-p group.

An arbitrary open U contains a congruence subgroup, hence deep elements on both noncentral axes. Commuting with them forces p^e a=p^e b=0; torsion-freeness of Z_p forces a=b=0. Therefore Z(U)=U intersect Z(G). The intersection is open in the procyclic center and equals p^{k(U)}Z. For finitely many U_i, k=max k(U_i) is finite. The nonzero subgroup p^k Z is a power subgroup of every center and is characteristic in every U_i. The proof uses no normality or coordinate-form assumption on U_i. Finiteness is material: an infinite descending congruence family can have trivial intersection.

### Finite quotient and exact nonlifting

Modulo p, the displayed subgroup a=0 is elementary abelian of rank two. Its only characteristic subgroups are itself and 1. The coordinate map theta(a,b,c)=(b,a,ab-c) is an involutory automorphism and moves that subgroup to b=0, excluding itself as a common characteristic subgroup. The argument is valid for p=2, where the displayed subgroup is C_2^2 inside a group isomorphic to D_8; it makes no assertion that every maximal subgroup is elementary abelian.

Upstairs the preimage a in pZ_p has center equal to the whole central Z_p and therefore a nontrivial common characteristic subgroup. The downstairs local coordinate swap exchanging b and c moves the image of that center. It cannot be induced by an upstairs automorphism descending to the specified quotient, because every upstairs automorphism preserves the center. This is the claimed nonlifting obstruction. It does not contradict the separately proved lifting for the specific Frattini quotients of a free pro-p group in Turn 2.

## Replays and new falsification controls

I copied the two author programs after reading them into a private audit subfolder and ran them using the standard library under Python `-B`. The Turn 4 output has 614 assertions and the Turn 5 output 51,455 assertions. Both stdout files are **byte-identical** to the frozen receipts. `author_copy_bindings.json` binds the private code to the snapshot; `EXECUTION_RECEIPTS.json` records interpreter, arguments, timestamps, exit codes, imports, and code/stdout/stderr hashes.

`independent_controls.py` imports only `collections`, `itertools`, and `json`, with no author or historical-review imports. Its 10,071 passing assertions use materially different representations and hypotheses:

- Generic 3x3 matrix multiplication and geometric-series inversion test theta at p-power precision and at primes 7 and 11, beyond the author's finite-prime scan.
- Complete multiplication-table automorphism enumeration at p=2 obtains 8 automorphisms of UT_3(F_2), 6 of the displayed C_2^2, and directly enumerates the unique common characteristic subgroup 1.
- Deep nonnormal open-subgroup shadows H_s have a,b divisible by p^s and c divisible by p^{2s}. Their finite centers have additional torsion directions absent from the image of the p-adic center. For example modulo 8 with s=1 the center has order 8, whereas the image of the p-adic center has order 2. These extra directions retreat to higher valuation as precision grows. This checks the exact limiting trap and confirms why finite-center substitution is invalid.
- Nonabelian D_8 lamps implemented as permutations in a wreath product with top C_4 separate lamp conjugates; single-lamp containment fails normality. The trivial-complement boundary is explicitly retained.
- Exhaustive additive subgroup enumeration over (Z/8)^2, (Z/9)^2, F_2^3 and F_3^3 independently yields only scalar GL-invariant subgroups. The finite nonscalar subgroup has different invariant factors at higher precision, so these controls deliberately make no unjustified inverse-limit classification claim.

These finite checks supplement the written universal proofs. They cannot certify the pro-p Hall theorem computationally or eliminate every possible common core in an infinite free pro-p group.

## Strongest verified result and exact missing step

For an index-p pair {F,U}, every common characteristic K lies in U'; a nontrivial K must have infinitely generated closure and cannot be contained in any closed finitely generated infinite-index subgroup. The comparison classifications and the explicit failure of arbitrary finite-quotient automorphism lifting are valid for their stated groups.

The original missing step is unchanged: prove that **some finite open-domain family including F** has trivial maximal common characteristic core, or prove that **every** such finite family has a nontrivial core. For the cyclic core-descent construction, a positive answer requires the exact order of quantifiers

    for every Frattini depth k, there is a descent stage t with V_t <= Phi^k(F).

Strict index growth, exclusion of finitely generated survivors, fixed finite precisions and comparison groups do not establish this cofinality. Promoting any of those to a solution would transfer the central difficulty to an unsupported equivalent claim. The audit does not reopen that route or add a sixth research turn.

Audit completion estimate: 100% of this assigned source/Turn 4-5 scope. Original discovery completion is not certified; the frozen author's subjective 20% remains a heuristic rather than a proof metric.

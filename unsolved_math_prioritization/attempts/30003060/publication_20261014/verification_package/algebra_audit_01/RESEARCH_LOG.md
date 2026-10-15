# Independent algebra audit: PR 826 / problem 30003060

Scope: frozen head `286cc67c0727b4decfd4f261a0591cd8823ebce9`; mathematical validation only. No Git, queue, frozen-source, or unrelated-effort mutation. No external communication. The parent supplied the confirmed exact `claimed_solved` gate. Internal reviewer independence is relative to the author and old reviewers; this is an AI audit, not human, novelty, or formal certification.

## 2026-10-15 04:14 UTC — intake checkpoint (10% complete)

Read candidate `source/author/PROOF.md`; have not opened any previous reviewer conclusions or implementations. Independently reconstructing the two-term chain complex and cap action, then implementing an exact matrix check from chain tensors and a separate orbit/period count. Candidate formula looks plausible, but its interpretation of the left cap and the repeated-word distinction remain explicit falsification targets.

Exact proposed claim: for a finite alphabet and its free tensor algebra over any field of characteristic p>0, higher Koszul homology with coefficients in the algebra and differential from the fundamental degree-one cocycle has, in each positive total weight n, one degree-zero and one degree-one class for each cyclic orbit whose number of *distinct words* is divisible by p. All higher degrees vanish; weight zero is k in degree zero. In characteristic zero the positive-weight higher groups vanish. Rank two supplies a counterexample to the unrestricted-field forward implication from Koszulness to positive-degree higher vanishing. No characteristic-zero converse is claimed.

Independent reconstruction before old reviews: R=0 forces every W_j with j>=2 to vanish; in total weight n>0 the degree-one basis is (length n-1 word, last letter), and the degree-zero basis consists of length n words. The commutator differential should be the difference between concatenating at the right and at the left. Their quotient is therefore a cyclic coinvariant quotient. The cap action needs a primary-definition check to fix which concatenation and sign is used; either concatenation gives the same class in degree-zero homology. No incoming degree-two terms exist in either homology stage.

Planned controls: rank zero and one; total weight zero; characteristic zero, two, and odd primes; repeated words of length divisible by p but orbit size prime to p; primitive length-p words; deliberately wrong length-for-orbit and sum-instead-of-difference models. Finite tests supplement the proof and cannot establish the infinite statement.

## 2026-10-15 04:16 UTC — algebra/computation checkpoint (75% complete)

Independently retrieved exact primary source arXiv:1512.00183v3. Its equation (2.3) confirms b(a tensor v)=av-va. Equations (4.1)-(4.2) give left cap va and right cap -av at degree one. Since b(z)=0, the aggregate products av and va agree already as chains in degree zero, so candidate delta=[av] is correct. Section 5.2 explicitly permits every characteristic for the fundamental cocycle; its cycle-evaluation formula also agrees directly with the candidate.

Fresh standard-library implementation `exact_chain_check.py` completed successfully: 234 exact matrix/independent necklace-period comparisons over Q and F_2,F_3,F_5,F_7,F_11; primitive length-p witnesses for 14 primes through 43; 10 falsification controls. No prior author/reviewer implementation or conclusions have been read. The matrix route computes the induced cap rank as rank([b,cap(ker b)])-rank(b), without assuming the orbit formula. The second route counts necklace representatives and minimal periods.

The repeated-word controls confirm that rank-one x^p has orbit size one and no higher class, despite p dividing its total weight. At length six, (xy)^3 has orbit size two while (xxy)^2 has size three; the exceptional characteristics differ accordingly. Characteristic-two behavior is valid because no argument divides by two. There is no unresolved central mathematical gap so far. Remaining work is the full checkable writeup, source/candidate binding, a final audit of the checker and limitations, and the decision.

An initial receipt-generation helper used an unresolved relative Path('.') and failed before writing a receipt. It was corrected to resolve the working directory; no frozen input or other effort was touched.

## 2026-10-15 04:18 UTC — final checkpoint (100% of assigned algebra audit complete)

Decision: **CLEAR** for the exact stated counterexample and full cyclic-orbit formula. The detailed independent reconstruction is in `MATHEMATICAL_AUDIT.md`; the fresh checker, exact output, and primary/candidate binding are `exact_chain_check.py`, `RESULTS.json`, and `SOURCE_RECEIPTS.json`. After adding explicit cap-boundary fillers, the complete checker was rerun successfully; result counts and checker digest were independently rechecked. The candidate's SHA-256 matches the frozen-source manifest.

Strongest verified result: free rank-two A over every positive-characteristic field is Koszul yet HK^hi_1(A) is nonzero. For finite-rank free A and each positive total weight n, both degree-zero and degree-one higher homology have one basis class per distinct cyclic orbit whose cardinality is divisible by the characteristic; all higher homological degrees vanish, and weight zero is k only in degree zero. Sign conventions, both homology stages, fields of characteristic two and odd primes, repeated words, rank zero/rank one, and both notions of weight are accounted for in the proof.

Exact remaining gap relative to the mathematical claim: none identified. Exact limitations relative to the overall source problem: this audit does not establish historical unrestricted-field intent, novelty, formal certification, or human review. The characteristic-zero converse remains unresolved by this calculation, so completion of the *original research question under a characteristic-zero restriction* is not asserted. No external individual was contacted and no Git, queue, frozen-source, or other-effort file was mutated. No previous reviewer conclusion or implementation was read.

## 2026-10-15 04:20 UTC — acceptance-interface hardening (85% of revised audit complete)

Parent independently identified a mandatory verification-interface issue: the fresh checker used Python assert statements, which optimization mode removes. The algebra and existing normal-mode results remain correct, but an optimized invocation could skip acceptance checks. Before changing current files, preserved `exact_chain_check.py`, `DECISION.json`, and `RESULTS.json` byte for byte under `historical_v1/`, with a historical README and digest/size manifest.

Revised scope: replace every acceptance assertion with an explicit fail-closed check; run normal and optimized modes to distinct output paths; compare all semantic results ignoring timestamps/checker digest; and deliberately corrupt an expected dimension to prove both modes reject. No mathematics or tested parameter range changes are authorized or needed. The previous 100% checkpoint described the original assigned mathematical audit; the interface hardening now reopens completion until both replay receipts are recorded.

## 2026-10-15 04:21 UTC — hardened replay checkpoint (100% of revised audit complete)

Replaced every acceptance assertion in current `exact_chain_check.py` with explicit `need` checks that raise `VerificationFailure` and preserve useful diagnostics under Python optimization. Added explicit final coverage checks and a test-only deliberately incorrect expectation switch. AST inspection confirms zero assertion statements remain. No mathematical calculation, test range, or independence claim changed.

`replay_verification.py` verified byte-exact preservation of all three historical artifacts and ran both modes to distinct paths. Normal and optimized replays both returned 0, each executing **2,110 explicit checks** across the same 234 comparisons, 14 prime witnesses and 10 negative controls. Every semantic result agrees after ignoring only timestamp/checker-digest fields. All historical mathematical arrays and values remain unchanged. Current `RESULTS.json` equals the normal replay byte for byte.

The explicit rejection control changed the expected higher_h1 at (r,n,char)=(2,2,2) from 1 to 2. Both modes returned 1 with the intended `Matrix/necklace mismatch` diagnostic and wrote no acceptance artifact. The complete positive/negative replay receipts, interpreter metadata, output digests and comparison outcomes are in `REPLAY_RECEIPTS.json`. The report and current decision now identify the hardened interface and updated artifact hashes. Decision remains **CLEAR** for the mathematics; the mandatory interface repair is completed. No Git, frozen source, other effort or external individual was touched.

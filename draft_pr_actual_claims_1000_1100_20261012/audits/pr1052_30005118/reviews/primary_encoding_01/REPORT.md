# Independent primary-source and complexity-interface audit

**Verdict: ACCEPT the submitted mathematical scope at head `b7e55279707ce2c720304ca98111088d7d037371`. No required correction to its normalization, cyclic transfer, or two NP-completeness claims was found.** The conclusion is a deterministic polynomial-time decision classification for two explicit encodings of ordinary same-group self-sums with unbounded input n. It gives polynomial-time recognition iff P=NP, not an unconditional impossibility. The integer hardness construction remains AFWS's external established theorem; this review reconstructs its relevant integer mechanisms and the composed cyclic consequence without claiming an independent proof of the entire bibliography or every result in the paper.

All eight submitted originals were frozen immediately and matched SUBMITTED_PINS and local head Git bytes exactly. The whole head tree and its target subtree were saved. This review wrote only in its assigned directory, changed no Git index, called no PR/publication service, used no other agent, and contacted no individual. The independent mathematical derivation and then the primary findings were frozen before reading prior ACCEPT labels, SOURCE_LEDGER, or INDEPENDENT_AUDIT. Their timestamp/hash records are in `frozen/`.

## Primary target and controlling source

The original is Marcelo Campos's Problem 15, attributed to Alon and Granville, OWR 22/2022 printed p1228, PDF p64. Both the input B and unknown A are subsets of the same `Z/nZ`, and the equality is `B=A+A`. There is no prime-modulus restriction in this problem and no input encoding or definition of efficient. Ordinary all-pair notation on Campos's printed p1174/PDF p10 permits repeated summands. Both complete pages were visually inspected. [Official original report](https://publications.mfo.de/bitstream/handle/mfo/3964/OWR_2022_22.pdf?isAllowed=y&sequence=4)

The controlling proof is Abboud–Fischer–Safier–Wallheimer, *Recognizing Sumsets is NP-Complete*, arXiv:2410.18661v2, dated 26 October 2024. Theorem 1.2 is on manuscript p2. Section 5.1 p21 and the final proof p23 explicitly allow the final root to be any subset of Z; the integer interpretation does not depend on the informal finite-universe example in Definition 1.1. The body constructs explicit sets and gives polynomial running time in a polynomial numerical universe. It does not formally define a binary bit-string language. The explicit sparse and dense encoding consequences here are inferences from that construction plus the independently checked transfer. [Pinned version](https://arxiv.org/abs/2410.18661v2), [controlling body](https://arxiv.org/html/2410.18661v2)

The public publisher record confirms SODA 2025, pp4484–4506, DOI `10.1137/1.9781611978322.153`, published online 7 January 2025. Direct shell access returned 403; browser retrieval of the public record succeeded. The full inspected proof is v2, not a separately acquired publisher typeset chapter. A failed fetch provides no evidence that the mathematical theorem is false. [SIAM record](https://epubs.siam.org/doi/10.1137/1.9781611978322.153)

Theorem 1.3 is a separate statement for fixed-characteristic vector groups F_p^d. For d>1 these additive groups have exponent p and are not cyclic of order p^d. This theorem is unnecessary here. The integer chain remains self-sum throughout; unrelated A+B and query/property-testing statements do not supply the claimed result.

## Numerical and logical interface

For q=v+c>=1, the complete p23 chain is:

| Step | Root condition | Numerical output bound | Body locator |
|---|---|---|---|
| SAT gadget | exists A subset U: X subset A+A subset Y | 160q^2 <= 2^8q^2 | Lemma5.3, pp21–23 |
| Masking | exists A' subset U': X'=A'+A' | 2^17(2^8q^2)^2=2^33q^4 | Lemma1.5, pp15–18 |
| Positioning | exists A'' subset Z: X_phi=A''+A'' | 2^24*2^33q^4=2^57q^4 | Lemma1.4, pp8–11; final p23 |

All transformations explicitly run in polynomial time. The p2 O(q^4) universe statement agrees with the calculation. The exponent is visibly 57 on p23; the looser 60 appearing in the ETH argument p26 does not replace it. No final-output zero anchor is assumed: positioning translates the relevant block, and the candidate normalizes its final integer target itself.

I checked the full relevant integer sections (pp8–11, 15–18, 21–23), their forward and reverse mechanisms, and actual parameter arithmetic, in addition to theorem/metadata pages. The detailed reconstruction is preserved in `frozen/PRIMARY_FINDINGS_BEFORE_PRIOR.md`. The main checks were:

- Sidon-separated variable choices forbid both s_i and s_i+1 because their mixed sum is absent. Clause target t_k admits only the literal-complement representations. A satisfying assignment supplies a root of the sandwich instance; conversely every represented clause forces a satisfied literal. Unused variables can be assigned arbitrarily. Range separation and Sidon uniqueness rule out unintended representations.
- The constant integer skeleton is primitive by a separated maximum point. Its three diagonal representation counts are 1 and its central count is 4. The full-interval filler blocks absorb all other sums. In the reverse positioning direction, the primitive support identifies the intended root block and endpoint blocks enforce its containment in U. Endpoint cases omitted from the source's parity shorthand are harmless because a mixed half-stride support would force all offsets to 0, contradicting interior points of a filler interval.
- Masking first forces root extrema 0,N and parity, so A+[0,N] is independent of A. Complementary singleton pairs cover precisely the optional central target Z=Y\\X; required X remains attributable to the unknown root block. Actual occupied coarse supports are separated, and within each layer the stride 4N exceeds pair-interval width 2N. Translating allowed root and target by h and 2h respectively preserves self-sum equality and yields the advertised polynomial nonnegative universe.

Several literal manuscript lines are inaccurate, but direct reconstruction preserves the theorem's bound. These are source presentation issues, not candidate proof defects:

| Locator | Literal issue | Check/repair preserving the needed statement |
|---|---|---|
| p21 Lemma5.1 proof | all-p-point graph need not have size q; its stated range inequality does not follow for every allowed prime; p=2 has diagonal collisions | use the first q graph points with odd p in [q,2q), q=1 fixed and q=2 using p=3; range <=p(2q−1)−1<4q^2 |
| p8 positioning estimate | `(4m+2)n` misses the doubled skeleton support | actual maximum coefficient is 8*(4*5^8)+2=12500002<2^24 |
| p9 positioning support range | initial half-stride range is too narrow | allow indices up to 2max(I), then rescale; final support is still <=max(I) |
| p17 masking arithmetic | inline `512N^2=2^17h` misses h's square | N=16h gives 512N^2=2^17h^2, as formal lemma p15 and final p23 already use |
| pp11,16–18 ancillary lines | membership/union symbol or scale factors are omitted | the equations/construction identify the intended sumset, affine inverse, and [0,N] interval directly |

The first issue has an explicit allowed-prime counterexample: q=6,p=11 gives all-graph maximum 221>144 and 11 rather than 6 points. Taking its first six points gives maximum 113<=144 and retains Sidon uniqueness. Thus a literal all-p-point reading is wrong, while the lemma and the final 2^57 bound are attainable without increasing the constant. `SOURCE_PRESENTATION_CHECKS.json` records these arithmetic checks. This review does not promote the incorrect intermediate displays as exact facts.

## Independently checked candidate proof

For nonempty integer S, any root R is finite by a translation injection into S. Minima satisfy min S=2 min R. An odd minimum is NO. An even minimum t permits the exact root translation R->R−t/2 and target translation B=S−t, including negative t. A normalized root has min 0 and max M/2, where M=max B.

For odd n>2M and 0 in B subset [0,M], suppose cyclic A+A=B. A pair a,c represents 0, so c=−a. Repeated summands put 2a and −2a in B. Their canonical representative sum is a nonnegative multiple of n at most 2M<n, hence both doubles are 0. Oddness implies a=0. Thus 0 in A and A subset B. Its representatives lie in [0,M], and every pair sum lies in [0,2M] below n. Both directions of cyclic equality therefore lift to ordinary integer equality. Integer roots project back. This proves the stronger every-cyclic-root lift claimed by the certificate.

The total map is correct on every branch: empty S has the fixed YES image; odd min S maps to the fixed NO (5,{0,1}); even min S maps to n=max(3,2M+1), B=S−min S. The fixed NO follows from the lemma because a root of {0,1} would need 1 and therefore introduce 2. M=0 gives (3,{0}). For an everywhere nonempty, zero-containing restricted language, replace the empty-source image with (3,{0}), as the submission explicitly permits. All restricted outputs have odd n and every representative b satisfies 2b<n. This proves the stated restriction without falsely treating the unrestricted empty image as zero-containing.

The anchor uses ordinary diagonal sums. `{1}` gives a counterexample to omitting normalization, since it has no integer root but equals `{3}+{3}` modulo 5. The even-order root `{n/2}` of `{0}` invalidates an every-root zero-anchor claim for even n. Neither stronger assertion is made by the candidate.

## Two explicit input models and quantifiers

For sparse input, n and residues are binary. If an integer-source encoding has length L, subtraction of the extrema and formation of 2M+1 require O(L) bits; only |S| residues are emitted. Thus the integer-to-cyclic transformation is polynomial in L even for enormous numerical M. The fresh bounded-universe SAT construction also directly supplies a polynomial sparse reduction, so no formal source input-encoding ambiguity can obstruct sparse hardness.

For dense input, arbitrary sparse integer instances may yield exponentially long vectors. The valid dense reduction composes directly with SAT: M<=2^57q^4 and n<=max(3,2^58q^4+1), so writing n bits is polynomial in the formula's encoded length. Large fixed constants affect practicality, not polynomial-time reducibility. Use the standard explicit 3-CNF encoding: unused variables may be deleted and occurring variables relabeled in polynomial time, making q polynomial in the encoded formula length. Constant exceptional branches and the variable/clause-free satisfiable formula have fixed outputs.

For dense NP membership, the certificate is n bits and O(n^2) modular pair operations suffice. For sparse NP membership, a nonempty root A admits the injection a->a+a0 into B for any a0 in A; hence |A|<=|B| for every positive n. At most |B| binary canonical residues use O(|B|log(n+1)) bits. Computing all pairs, including diagonals, sorting/deduplicating, and comparing exact sets is polynomial bit time. B empty has the empty certificate and cannot have a nonempty root. These membership arguments cover even n and n=1, although hardness uses odd outputs. They also apply to the restricted target language after checking its promises in polynomial time.

NP-hardness plus these verifiers proves NP-completeness in each model. Accordingly each deterministic polynomial-time exact decision algorithm exists iff P=NP. For each individually fixed n there are finitely many targets; that fact neither contradicts nor establishes a uniform polynomial algorithm for unbounded n. No conclusion follows here for restricted summands, unrelated summand sets, prime moduli, succinct circuits, oracle-only input, search/output tasks, randomization, average case, or approximation.

## Falsifiable checks and comparison with prior records

The reproducible checker `independent_checks.py` passed: 502 zero-anchor target checks over odd n<=15, 43690 cyclic root candidates, all 1024 integer targets contained in [-3,6], every total-map exceptional case, the restricted empty-YES substitution, the source skeleton multiplicities, and all 230 two-variable one/two-clause literal-multiset SAT gadgets with all possible allowed-root subsets. Sidon sizes 1 through 100 also passed. These finite checks supplement the universal derivations and do not prove asymptotic hardness by enumeration. `INDEPENDENT_CHECKS.json` is the final completed output; an eager-cache issue in the initial checker was fixed before reliance on this run.

Only after both independent freezes did I read all remaining submitted files. The prior SOURCE_LEDGER and INDEPENDENT_AUDIT identify v2, the proper original page, p23 exponent 57, unrestricted integer root, separate dense/sparse arguments, and their limits correctly. Their raw PDF hashes match the freshly downloaded version-pinned files exactly: OWR `a0622a6a42add0931f7b1d005157fb499122b8934ce0591f7c9cad684cd5f9ea` (655364 bytes), AFWS `89e6d1eb1b539ea58d463ba1b83cc5d71519055de36cc079398bdb918441a808` (616293 bytes). The old unversioned retrieval is therefore authenticated as the same inspected v2, not misidentified merely because its original URL lacked a suffix.

The prior reports expressly describe a theorem-applicability audit rather than independent reproof of every source gadget. This was a real scope limit, disclosed fairly, rather than a false full-source verification claim. The present deeper reconstruction adds the specific source presentation issues above and confirms that they leave the composed result intact. Publisher-only metadata and source proof versions remain clearly separated. The eight-file manifest is internally consistent, including its declared no-self-hash policy. This source-interface review does not independently certify historical editorial-preservation assertions about excluded older artifacts.

The entire inspected v2 body contains no explicit cyclic corollary (full-text search and theorem/conclusion inspection). That is only narrow comparative evidence. The prior bounded negative searches likewise do not certify priority. The submission asserts no original hardness gadget or novelty for the elementary transfer; no exhaustive novelty verdict is made here. A separate priority review may examine wider literature without changing this mathematical acceptance.

## Evidence and remaining boundary

The submitted theorem, all three source equivalences and their numerical chain, complete transfer, certificate-size bound, input quantifiers, edge cases, and decision-only consequence are now checked at this interface. The remaining external dependencies are the established AFWS result, standard 3-SAT NP-completeness, and its routine underlying constructions; I do not claim every citation in the source has been reproved or that the publisher body is byte-identical to v2. There is no unresolved source-interface blocker. This acceptance is scoped mathematics, AI-assisted and unrefereed, and does not include a new priority claim or publication authorization.

Completion of this assigned full primary-source/encoding adversarial audit: **100%**. The freeze documents preserve the independence order, `PIN_VERIFICATION.json` binds originals/head bytes, `SOURCE_FETCH_RECEIPTS.json` records fresh raw-source identities and failures, `VISUAL_INSPECTION_RECEIPT.json` records the exact complete pages inspected, and the final output manifest binds this report and all authored checks. Full third-party bodies and page images remain solely in ignored `sources/raw/`.

## Corrected partial results; general two-set question unresolved

For every 3-permutable set S and every fixed integer C >= 0, only finitely many positive integers n have the whole integer interval [n,2n-C] contained in S. Here 3-permutable requires an omega enumeration avoiding both increasing and decreasing 3-term arithmetic progressions at arbitrary subsequence positions. The complete proof gives the equivalent divergent-deficit conclusion, the P >= k+2 finite-prefix bound for k distinct C3 scales and two fixed anchors, and the stated bounded-additive-dyadic-run and monochromatic-interval exclusions.

For each prescribed nondecreasing unbounded f:N->N, an adaptation of Geneson's construction yields one 3-permutable set with upper natural density at least 2/3 and infinitely many full intervals with positive deficits at most f of their starts. Those deficits still diverge. The proof also gives translation equivalence of the zero-based and positive-integer two-set existence questions. Neither an admissible complement nor a theorem ruling out all two-colorings is supplied. The full two-set target remains unresolved by this work; no novelty, priority or exhaustive worldwide-status claim is made.

## Required corrections applied, full audit preserved

The original candidate is explicitly NOT accepted as written. Acceptance is after two precise domain/scope corrections: Theorem 1 counts positive integer starts, avoiding vacuous negative-start empty intervals; the affine extension uses positive inverse coordinates and separates infinite from finite lattice intersections. CORRECTIONS.md retains the complete explanation and counterexamples. The exact two-hunk CORRECTIONS.patch is preserved byte for byte, 2,030 bytes, SHA-256 fa7fbcfaca2a8e832172cf750bf589194c141334213d56c2305b473fcfc61ac7.

The original proof was 16,461 bytes, SHA-256 8c4d56bb0e21785f4aeb21239518783dcf139afd10839c6514fea6472e0ad0b7. The distributed PROOF.md is exactly the corrected 16,759-byte proof, SHA-256 670b73ed1e4c3a0fd52235a67f6ee9a67140bb8949e923798bb52c73f5e074bd, with no further proof edits. The patch is already applied in this edition and targets the omitted historical authored/PROOF.md, so it should not be applied again to the distributed proof. Original candidate and audit inputs remain unchanged. The complete substantive mathematical audit, acceptance and correction explanation are retained; editorial changes add review/edition framing, remove workflow-only statements and describe omitted finite checks historically.

Kasel's [Structural rigidity in the Erdős–Graham two-set permutation problem](https://raw.githubusercontent.com/Wkasel/erdos197/main/paper/main.pdf), an August 2026 author manuscript, supplies the credited finite C3 lemma (Theorem 22). The proof rederives it completely by mirror propagation and four cases, then uses fixed anchors and finite predecessor counts. [The source repository](https://github.com/Wkasel/erdos197) stated during the recorded audit that it excludes the canonical dyadic candidate and leaves EP-197 unresolved. Its SAT/DRAT results and surrounding conjectures are not dependencies. The correction to Remark 3 is separate from the valid finite lemma.

Jesse Geneson's [Density bounds for permutations avoiding monotone arithmetic progressions, arXiv:2608.12604v1](https://arxiv.org/abs/2608.12604v1), is credited for the Section 3 construction and 2/3 density mechanism. The adapted statement is fully proved through finite binary ordering, cross-stage AP exclusion and the density count. LeSaulnier and Vijay's [On Permutations Avoiding Arithmetic Progressions, pinned PDF arXiv:1004.1740v1](https://arxiv.org/pdf/1004.1740v1) fixes the exact positive-integer arbitrary-subsequence question. Its older 1/2 density conjecture is not used. The differing arXiv abstract-page title is recorded in the metadata.

These AI-assisted authored documents and their independent internal AI audit are unrefereed. “Accepted” means only the corrected partial scope. No external human peer review, journal acceptance or formal proof-assistant certification is claimed. No computational result is a dependency of either infinite proof.

## Source and verification boundaries

The historical independent audit freshly retrieved all three primary PDFs and matched their recorded exact bytes: Kasel, 205,129 bytes, SHA-256 89736e1eec491ae3f249e30efb1d1133fabb4c528757e0ae246cbde818605c8a; Geneson, 266,695 bytes, SHA-256 f71bc1992ae1c11df30db54f7c06416896f95ab816b48110872b615aa7113cd7; LeSaulnier–Vijay, 64,364 bytes, SHA-256 46662dfb1b596a8568617a8ced810d440691c1c705c17e3c77fc48add3499c6e. Exact versions, URLs, inspection coverage and retrieval times are preserved in public metadata. Edition preparation performed no new scholarly-source retrieval or inspection.

Historically recorded independent checks replayed 236,283 primitive steps across 160 finite branches at ten scales and rejected 11 malformed certificates; the candidate's distinct checker rejected 12 malformed controls. Generator reproduction matched all ten certificate files and its manifest. The original audit's 17 packet-integrity controls and normal/-O/-OO comparisons are retained as historical verification metadata. Finite tests support instances and edge cases, while universal claims rest on the written arguments. Programs, certificates and detailed test outputs are omitted; this is not an executable reproduction package.

Exactly eleven authored mathematical prose, correction-patch and public verification/source metadata files are proposed as additions. Copied third-party documents/text/images, code, certificate contents, raw datasets, private sources, private personal data and private coordination material are excluded. QUEUE.md and unrelated paths remain unchanged.

## Exact public-file identities

- `ACCEPTANCE.md`: 5,087 bytes; SHA-256 `c657fe7c94d309c78392a4483fd2e4940b2e78b0e7353ac5913c6db11fdb5ba6`.
- `AUDIT.md`: 16,757 bytes; SHA-256 `f1e95d9fe696d0ccf57bfa0f287be057e92a1cbd4658995ed392fce043812b2f`.
- `CORRECTIONS.md`: 3,107 bytes; SHA-256 `6291feb2fbb6b2386b56ef1891d9f23290f3627b66c390c419713029223123ae`.
- `CORRECTIONS.patch`: 2,030 bytes; SHA-256 `fa7fbcfaca2a8e832172cf750bf589194c141334213d56c2305b473fcfc61ac7`.
- `MANIFEST.json`: 2,220 bytes; SHA-256 `ee25709dc7a728c4a8cf762fca08ac09d2797df96bd24ade75c7f44ff7a49718`.
- `PROOF.md`: 16,759 bytes; SHA-256 `670b73ed1e4c3a0fd52235a67f6ee9a67140bb8949e923798bb52c73f5e074bd`.
- `README.md`: 4,385 bytes; SHA-256 `0f67d2bf9d87039007548871f104051606df698763c5b221ac678015f29d449b`.
- `SOURCE_AUDIT.md`: 3,841 bytes; SHA-256 `5be2df01257abefdd29e8e2b5de2ec2da622d93bd50abfc1fb1feb824f1e668b`.
- `SOURCE_METADATA.json`: 3,394 bytes; SHA-256 `9db9148a65b1299d3bf8db6e1662dc7d0006cedf19366bb5f15dcdacf3146793`.
- `STATUS.md`: 3,747 bytes; SHA-256 `48a312cce05653bd362a4e1b6999ff28754d46a2c02698ae31a77ddb1c03be44`.
- `VALIDATION_SUMMARY.json`: 4,071 bytes; SHA-256 `8bc9a47a87f890cef0eaac436bdee687a504806a1a74ae351dc34dc710f6ec85`.

MANIFEST.json lists all eleven members and hashes the other ten; this body separately pins its digest.


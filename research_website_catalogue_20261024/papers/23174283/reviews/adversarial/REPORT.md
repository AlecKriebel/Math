# Independent adversarial review — Exact chordal separation of spherical Fibonacci points

The full published theorem is supported for its original quantified scope. No counterexample, substantive proof gap or unsupported mathematical dependency was found within its hypotheses. This assessment includes every integer n≥3, the exact value 2/√Fn and the unique unordered minimizing pair {z0,z1}; it is not a finite-n or asymptotic replacement. The proof is self-contained. Worldwide priority and continued openness of the 2012 conjecture in 2026 are not certified.

This is an AI adversarial review, not human peer review or formal proof-assistant certification. It grants no publication, browser, site, native-service, tracker, Git or release authority. Root114's initial independent reading gate remains pending at this packet's preparation; findings are retained locally, and only custody, primary locators and readiness have been sent to root.

## Frozen original and reading independence

Record https://zenodo.org/records/23174283, DOI 10.5281/zenodo.23174283, native version **1.0**, original declared publication date **2026-10-05**. Actual native timestamps are created 2026-10-05T23:41:09.395608+00:00 and updated 2026-10-10T21:33:20.838889+00:00. The source prints October 5, 2026 but does not print a version; the version is a native metadata field.

* SOURCE_READY.json SHA256 `b9f69bfea594378f8cd69a00d214ce14c894fd33e850047a915327432d96ae20`.
* Actual complete 3-page PDF, 61,391 bytes, SHA256 `d708af8be2f035af994bca24166a19c0c8ee1d4ea405ca213fe032ef55e9e8ee`.
* Sole controlling TeX, all 200 lines, 8,651 bytes, SHA256 `56a9eb3d76574d8521589988d6f1024be7653f524a450f9745104cf60a6f8553`.
* Whole native supporting ZIP, 25,341 bytes, SHA256 `0a0094e6044a2b153d400fc34408077d4ce65912c8c1e3f357876381feb91714`: 13 complete safe regular payloads, 51,353 expanded bytes. Original native order is PDF then ZIP; there is no embedded PDF or nested archive.

I personally read the entire actual manuscript PDF, every controlling TeX line and all three fresh full-page rasters before any foreign body, source code, program result, inventory triage, archived review or current peer finding. The substantive exact-claim reconstruction and attacks were sealed at 2026-11-15T00:48:54.800050+00:00 (November 14 local time): INITIAL_SEAL.json SHA256 `527cbe8fb0216c1af6a41ef2dbc2c8cd33ebf34cdbf635e1ac0b7154c8337c2c`, reconstruction SHA256 `575584d7fc5bcc143195439778e80011ca48578f846f059f38a5b43083e03c7b`. These files remain unchanged. No sibling review or root scientific opinion has been read.

After that seal, I read the complete supplied author_verify.py, historical_independent.py, identity_controls.py, proof_controls.py and verify_package.py, the full historical PROOF.md, README, source provenance and manifest. PROOF.md is the older restricted Cassini route and was treated as source history, not an inherited independent opinion. The current TeX's unimodular-basis proof controls the theorem. The archived priority note and expected aggregate scientific-output file were not used as review authority. INPUT_MANIFEST.json binds all 29 source-custody files before reproduction; hashing unread data does not imply reading its contents.

## Exact claim and central proof scrutiny

For n≥3, q=Fn, p=F(n−1), and exactly 0≤k<q, the paper fixes rational longitudes 2πpk/q and unshifted heights 1−2k/q. The unit-sphere coordinates are explicit. The metric is the ambient Euclidean chord. The associated minimum spherical geodesic distance is 2 arcsin(1/√q), obtained by a monotone conversion, not by identifying chord and arc.

DERIVATION.md supplies the full independent argument. The load-bearing arithmetic inequality m|mp−ℓq|≥q/3 is valid for every 1≤m<q and every integer ℓ. Its integer-basis sign argument covers large and negative ℓ, the duplicate initial Fibonacci value, and the terminal h=1 case where F(h−1)=0. The determinant, two error identities and addition identity have recurrence proofs; no nearest-integer rounding premise is smuggled into that lemma.

For distinct latitudes a<b, direct sphere geometry gives D²=2(U−cV), U−2(b−a)=4a(1−b)≥0 and U²−V²=4(b−a)². This yields the two cosine-dependent bounds with the correct positive square root. A centered nonzero Fibonacci residue either has nonpositive cosine, giving D²≥4m/q≥4/q, or positive cosine, giving the **strict** bound D²≥16/(3q)>4/q. Exact pole substitution attains 4/q. Equality in the first branch requires m=1 and a=0 because the actual upper latitude satisfies b<1; this proves the unique-pair claim. Neither preservation of distances by an equal-area map nor an asymptotic limit is assumed.

## Adversarial boundaries and strongest exact false-variant witnesses

The review actively tried small indices, poles, endpoint changes, residue ties, quarter turns, parity, arbitrary coprime slopes and metric substitutions. None produces a failure within the displayed original hypotheses.

* n=2 is a singleton with no unordered pair; it is expressly excluded. The same analytic proof includes q=2,3,5 without requiring a numerical large-n threshold.
* The genuine q=8,p=5,m=2 case has centered |r|=q/4 and cosine exactly zero. Integer branch tests cover it; rounded cosine signs are unnecessary.
* Including both endpoints at q=2 gives squared pair distances 2,2,4, hence two minimizers. This falsifies an endpoint-expanded uniqueness claim. It does not apply to the stated half-open range.
* Midpoint heights at q=2 make the two points antipodal, giving chord 2 instead of √2. The original theorem explicitly excludes that change.
* General coprimality is insufficient: q=12,p=1,i=5,j=6 gives D²=2−√105/6<1/3=4/q, certified by 105>100. This exact witness shows why the Fibonacci arithmetic matters; it is not a counterexample to the published theorem.
* The coordinate-reversed primary convention is isometric after the parity-dependent reflection. Omitting the odd reflection fails already at n=5,q=5,p=3,j=1,k=3, with opposite nonzero longitude sines. The n=3,q=2 case is too degenerate to witness that error.

No defect-repair route, narrowed promotion or further scientific conjecture is proposed.

## Reproducible evidence and its limits

The independent own_exact_controls.py uses only the standard library and never writes files. Its complete final output is own-exact-controls-v2.stdout.json. It checks four literal polynomial identities, 6,746 centered-residue offsets for n=3..18 (max q=2584), complete integer parity/permutation congruences, half-period ties, quarter turns and terminal cases. A distinct direct radical certificate checks **all 42 unordered pairs** at q=2,3,5,8, retaining every H,P and exact radical or integer gap and all equality decisions. There is no decimal trigonometry, floating tolerance, sampled pair selection or reliance on a proof-derived approximate distance certificate in that finite radical check. The universal theorem is established by the written deductions, not inferred from those ranges.

The deposited proof_controls.py was run **once**, with ordinary assertions enabled and flags −E −B: exit 0, no stderr, exact finite result PASS for n=3..22, 46,345 offsets, 185,380 integer lattice-coordinate cases, 17,710 terminal offsets and 20 rational geometry cases. EXECUTION_RECEIPTS.json records the actual command, script hash, UTC times, complete streams and timeout. The longer historical all-pair campaigns and verify_package.py were inspected but not replayed. Existing result counts in the README were not treated as reproduced evidence.

One illustrative label in the first independent control draft incorrectly used q=3 for an odd-reflection witness. Its universal parity congruence checks were already correct, and its 42 radical certificates were unaffected. The final draft uses the actual odd n=5,q=5 example and adds an explicit index guard. The exact first script and first stdout are retained unchanged; EXECUTION_CORRECTION_RECEIPT.json records the one justified independent rerun. This is a correction to this review's diagnostic example, not a defect in the published source. The authoritative final finite output is v2.

## Primary credit and precise remaining limits

PRIMARY_EVIDENCE.md records fresh actual primary PDFs, selected exact pages, byte hashes, transport and visual checks. The original EMS OWR physical p.10/printed p.2438 contains the displayed construction and exact conjecture. The actual final Aistleitner–Brauchart–Dick publisher PDF, Section 5.2 with Equation (7), confirms the coordinate-order convention and its isometric relationship. Zaremba's original scan p.186 and Suryanarayana–Cools–Nuyens Theorem 2.2 independently confirm the classical F(n−2) hyperbolic-cross index with the correct index-versus-degree normalization. Construction, pole upper bound and arithmetic product estimate must retain positive classical credit.

The review supports the new paper's all-pair spherical lower-bound argument as a proof of the precise stated conjecture. It does **not** certify worldwide first priority or whether a later or unpublished resolution already existed. The fate of the cited Brauchart–Dick in-preparation work remains unverified, as do primary editions outside this bounded interface review. This is an honest priority limit already disclosed by the target, not an unsupported premise in the self-contained mathematical proof. A later public description must not upgrade it to certified worldwide openness, firstness, optimal packing, discrepancy bounds, arbitrary-cardinality or irrational-angle results.

VERIFY_READ_ONLY.py closes native asset hashes, every source-file binding, all ZIP payload identities, the unchanged independent initial packet and this owned packet. Its default mode does not execute source programs, make network requests or write files. CLOSURE.json and SEAL.json record final custody. All substantive work and generated evidence are confined to this adversarial lane; prior packets, sources, site, core configuration, spreadsheet, Git state and services were not mutated.

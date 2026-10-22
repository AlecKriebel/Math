# Independent final-reader review: harmonic circle fibrations

Review date: 13 October 2026. Problem 30003375 / OWR-15208-029, queue row 1766.

## Decision

**Accept this exact reader for the adopted existential-metric statement E, as a credited prior-result consequence.** No unresolved assembly, reproducibility, scope, or publication-boundary blocker was found. This is an acceptance of a frozen authored reader, not a new mathematical proof-search pass or a certification of every historical interpretation of the source question.

The accepted normalized statement is: for every closed connected smooth manifold homeomorphic to S¹ × CP³ and either primitive integral first-cohomology class, some unrestricted smooth metric makes the harmonic circle representative a smooth fibration with connected fibres. The same constructed metric works for the two signs. A supplied smooth bundle projection can itself be made harmonic.

The disposition `already_solved` is accepted **only with that express E qualification**, and `prior_result` is the result classification. Browder–Levine supplies smooth fibering; the classical metric-existence mechanism is credited to Calabi as recalled by Katz, with an explicit construction of the necessary bundle case in the proof. There is no new-theorem or historical-priority claim. The original metric quantifier and homotopy-class normalization are not authenticated. Arbitrary-metric assertion U, prescribed-metric question G, and curvature-constrained variants remain outside this result; no assertion about their worldwide open or solved status is made.

## 1. Exact accepted object

The reader consists of 13 regular files, including its manifest, totalling 70,841 bytes. Its manifest lists the other 12 files, totalling 68,620 bytes. It excludes only itself, thereby avoiding a self-hash cycle.

- `MANIFEST.json`: 2,221 bytes; SHA256 `cb6eb161b96b63842e04400727f620f1891a8bddc16c461438f2560398cdb707`.
- External `READER_SEAL.json`: 2,350 bytes; SHA256 `7828b49620826804087d64a2bef041eb4612a4238577171375d9271077b7bfa4`. It enumerates and pins all 13 reader files, including the manifest. Its stage label correctly describes the assembly-stage candidate; this report supplies the subsequent independent acceptance.
- `PROOF.md`: 16,025 bytes; SHA256 `776ef606f87874d2e2c6b83eea5ad98be6995cac863709ca0c316c2cf37db203`.
- `INDEPENDENT_MATHEMATICAL_AUDIT.md`: 14,378 bytes; SHA256 `f1a1bae26a1ab9f8c22f13250fe296c5fdb057ad5c64e8c645f8407146450fc5`.
- `SOURCE_SCOPE_ACCEPTANCE.md`: 12,071 bytes; SHA256 `837d4a6a92181f98d800998266d5c4cadf80c159785fda56b62987fa7b52aaab`.

I independently calculated every file's size and digest against both the manifest and external seal. The proof, its original script and output, the mathematical audit and acceptance, the independent adversarial script and output, and the source-scope acceptance were all compared directly against their accepted originals. All eight were byte-identical. The proof pin in `ACCEPTANCE.json`, the audit, the manifest, and the seal agree. The complete reader was checked again after testing and remained unchanged.

The assembler added only the reader introduction, machine-readable result, reproducibility report, verifier, and integrity metadata. This review neither rewrote accepted mathematical text nor changed the reader's checks.

The three corrections already incorporated into the accepted proof remain present: explicit orientability, the distinction between the induced fundamental-group map and cohomological pullback, and positive fibre dimension in the general metric proposition. Original correction evidence was retained unchanged outside the public reader. It is not included in these public deliverables.

## 2. Mathematical and scope consistency

I read the proof, detailed audit, source-scope acceptance, README, result record, acceptance record, and both check scripts in full, checking that the reader preserves the exact accepted argument and qualifications.

The topological application is correctly separated from the metric construction. The given smooth manifold has dimension seven, fundamental group Z, and degreewise finitely generated higher homotopy groups from CP³. Browder–Levine is applied to that smooth manifold in the chosen class; no smooth structure or metric is transported through a merely topological homeomorphism. Primitivity gives connected fibres. Orientability gives orientation-preserving monodromy. No identification of the fibre as smooth CP³, no trivial monodromy, and no classification of a particular exotic connected sum is required.

The explicit construction remains internally consistent: the negative sign in Moser's vector-field equation gives pullback preservation; the composition is φ composed with the isotopy endpoint, in the correct order; the displayed bundle diffeomorphism preserves the base projection; collared endpoint interpolation supplies smooth seam compatibility; the exponent −2/m fixes volume pointwise; and the orthogonal total metric has Hodge star of dt equal to the descended closed fibre volume form. Harmonic-map uniqueness in a fixed integral class identifies every such representative up to rotation. Negation preserves the same metric and submersion property.

The reader does not turn an example of a nonharmonic prescribed projection into a counterexample to nonsingularity of the actual harmonic representative. It also does not infer sectional-curvature control from conformal normalization or volume preservation. Those important limits are consistent across the proof, audit, README, and result records.

Imported dependencies remain explicit: Browder–Levine, Serre's finite-generation implication, and standard de Rham, Hodge, smooth-flow, and bundle theory. The previous mathematical audit checked the relevant theorem statements and their application but did not rederive the full imported proofs. This final-reader review does not claim a new inspection of original scholarly sources or a formal verification of those dependencies. Calabi attribution remains through Katz; no direct inspection of Calabi's complete chapter is claimed.

## 3. Independent execution and failure tests

Testing used Python 3.12.14 and a frozen copy outside the candidate reader. The normal invocation was `python3 -I -B verify_reader.py`. Its output matched the recorded 1,233-byte `REPRODUCIBILITY_RESULTS.json` exactly, SHA256 `f01a5c1d9dc42f691a6ef7182dcd4151652698153e2ae115dabc7dc7f87b030d`.

Both mathematical scripts ran successfully in the verifier's fresh temporary directory. The author script reproduced 60 seeded exact-rational interpolation cases, with the expected 555-byte output. The adversarial script reproduced the expected 914-byte output. The checks use only the Python standard library and need no source PDFs, dataset, network, or repository state. Static inspection of the actual scripts found no network calls or external-input dependency.

There were 13 independent test cases: one positive reproduction and 12 expected rejections. Every case behaved as expected:

1. Normal isolated, no-bytecode invocation: pass and byte-identical recorded output.
2. `-O`: rejected with the required assertion-enabled-mode diagnostic.
3. `-OO`: rejected with the same diagnostic.
4. Missing `-I`: rejected with the required invocation diagnostic.
5. Same-size alteration of the proof: SHA256 mismatch rejected.
6. Missing listed file: rejected.
7. Unlisted extra file: rejected.
8. Listed proof replaced by a symlink: rejected.
9. Manifest replaced by a symlink: rejected.
10. Duplicate manifest entry: rejected.
11. Altered expected script output with an internally recomputed manifest: execution-output mismatch rejected.
12. Deliberately false assertion in a script with an internally recomputed manifest: failed subprocess rejected.
13. Script that changes its own temporary copied bytes, with an internally recomputed manifest: copied-input mutation rejected.

The last three tests intentionally update local test-copy manifest records to reach the execution checks rather than stop at the initial digest gate. They do not alter the candidate, constitute accepted reader revisions, or override the external accepted hash pins. Exact machine-readable observations are in [INDEPENDENT_READER_CHECK_RESULTS.json](INDEPENDENT_READER_CHECK_RESULTS.json).

Optimized execution is deliberately unsupported, not falsely reported as a passing proof check. The original assertion-based scripts remain unchanged, and the verifier uses explicit runtime requirements so that `-O` and `-OO` cannot bypass its rejection. These finite checks are reproducibility and algebraic sanity evidence. They do not establish global smooth existence, all seam jets, imported topology, or formal theorem correctness.

## 4. Closure, integrity limits, links, and public boundary

The clean-copy reproduction confirms practical closure for the two finite checks in this Python environment. The verifier requires the exact manifest-listed file set, compares byte counts and hashes, executes only copied scripts with their copied expected outputs, rejects unexpected standard error or generated files, checks copied inputs for changes, and verifies the reader again afterward.

This is interpreter and working-directory isolation. It is not an operating-system security sandbox: the subprocesses still have the ambient operating system's capabilities. The reader discloses that limit. Static inspection and accepted-byte identity, rather than an enforced network sandbox, support its no-network-call statement.

The verifier checks internal manifest consistency but does not itself authenticate the externally accepted root hash. A coordinated rewrite of a reader and its manifest could produce a different internally consistent object. Reviewers must retain the externally recorded manifest or seal hash to identify this acceptance. Hashes establish byte identity, not mathematical truth, source authorship, or cryptographic identity of an author.

All seven relative Markdown links in the reader resolve to included regular files. Eleven distinct scholarly HTTPS links were inventoried; they are ordinary public source links, with no private chat, local-machine, or coordination URL. No fresh availability check of those external websites is claimed here. The primary mathematical and source-scope audits remain the evidence for the cited source inspections.

Manual review of every included file, supplemented by a private-path and coordination-token scan, found only authored mathematical exposition, authored audit and acceptance records, finite-check code and small synthetic outputs, public references, and safe integrity metadata. No third-party source documents or source bodies, dataset contents, private paths, private personal data, or private coordination files are included. The short source-question quotation is bounded and attributed; no source PDF is republished.

The reader records one newly documented substantive proof-search pass and an unknown prior lifetime count. Independent audit, source adjudication, reproduction, assembly, and this final-reader review add zero substantive proof-search passes. No remote mutation was performed in this review.

## Final acceptance boundary

The exact pinned reader is suitable for publication as the qualified `already_solved` / `prior_result` account of E. Acceptance is conditional on preserving the explicit adopted scope, prior credit, dependency disclosures, and verification limits. It cannot be restated as a new theorem or an unconditional solution to the full historical Farrell question. Any future byte changes require a new integrity pin and an appropriate review of their impact.

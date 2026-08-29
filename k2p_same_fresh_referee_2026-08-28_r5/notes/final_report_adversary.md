# R5 final-report adversarial audit

Date: 2026-08-29 (America/Los_Angeles)

Audited report:

`reports/FRESH_ADVERSARIAL_REFEREE_REPORT_2026-08-29.md`

Audited report SHA-256 after the corrections below:

`ca5d0caf38521418fc035471a93e088f090b2d6ba8e75b8567df9cfe7860348d`

## Conclusion

**PASS for report accuracy and protocol completeness after correction.** The
scientific recommendation **HOLD** is supported by the evidence and is
internally coherent with the separate status lines:

- mathematics PASS;
- computational evidence PASS;
- reproducibility/document consistency FAIL despite byte-level provenance and
  deterministic reconstruction PASS; and
- human metadata PASS, release HOLD.

The report does not overpromote the document defect into a theorem
counterexample. It correctly reserves REJECT for a defeated theorem or
central finite classification and identifies a concrete reproducibility
blocker that prevents ACCEPT. No current scientific execution gate is silently
omitted. The local-tag/remote-release and inaccessible-literature boundaries
are now explicit.

The report contains the eight required top-level sections in the required
order. Its claim matrix now uses the same C01--C13 meanings as the distributed
`THEOREM_ARTIFACT_CROSSWALK.json`, with C14 added solely for integrated
archive/document/provenance consistency. C01--C13 are PASS; C14 is FAIL for
the bounded semantic-document defect. This agrees with the mathematical note,
the computational note, the final evidence registry, and the machine results.

## Evidence reconciled

I checked the draft against the isolated package, `EVIDENCE_REGISTRY.md`,
`EXECUTION_LEDGER.md`, all three review notes, the independent mathematics and
semantic-anchor results, the quick/full/mutation machine JSON, the relevant
TeX/Python source lines, and the current machine-readable authorities.

The following high-risk values and statements are exact:

- source ZIP: 214,974,312 bytes, 495 files, SHA-256
  `43a620bad862ad14c1b7beb6d605d69354c7da8c534e2882cd7564f7ad4a69db`;
- recursive closure: 408 files, 479,382,316 bytes, root
  `18555e4d365b5ddef786201c80fc358c620b2ac2200b0f2d677b61378e584dbc`;
- submission layer: 86 files, 4,257,433 bytes, root
  `91ca33df02687e98fddd84809c46ba495ca9121c69e644fcd2f6e676d10192c0`;
- combined root:
  `df5a19427a9937c0b9350aed2c9968b7ecbb9d7900013b73889350cbc80f9683`;
- quick 23/23, report SHA-256
  `6dff8c349158986462af8566da548cb2bfb32e4159951af63d9a150d7e850234`;
- full 41/41, report SHA-256
  `2f4fce76613bfe3f985ffdce37171854220e67330144e1705780d656211c4e9e`;
- release mutations 25/25 rejected, report SHA-256
  `c14d30290eab72b07b4ff791550a42e5d71d083a860e93a482908e28c7c2ca38`;
- crosswalk/bundle mutations 37/37, report SHA-256
  `a49415da9daa15079b6e0528027826196e6f5a314728fdbfb8b8314df7447b80`;
- exact-mathematics result SHA-256
  `5cf3cecf911e6464821b6417f3a04313cbd7feb635e5c82b051b7ddcf5842ca6`;
- article and supplement source/PDF hashes, page counts, rebuild times, omission
  failures, and visual findings;
- all raw4, theta2, cycle, restoration, and probe counts and partitions; and
- all key authority paths and hashes in the report's artifact table.

The command runtimes and reported peak-RSS values now match the wrapper JSONs.
The 41 full-layer names/times, duplicated focused checks, and every secondary
command remain expanded in `EXECUTION_LEDGER.md` rather than being silently
collapsed into the report's principal-command table.

## Central finding reproduced

The report's blocking finding is exact and independently reproducible:

- `supplement/supplement.tex:780-781` calls
  `5810ffb1d023e503eaa62d9705c28a85e9c724a6ad8357f49ebe61b2dde675dc`
  the “raw-four terminal registry”;
- `audit_article_sources.py:41-42` maps that label to
  `work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json`;
- that file has schema `k2p-raw4-corrected-terminal-overlay-v2` and 16,974
  corrected strict-sign rows; and
- the actual 934-class registry is
  `work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz`,
  schema `k2p-raw4-terminal-certificate-registry-v1`, SHA-256
  `8d821c2000da5cf2647913cbdb42f8a42dfeb6826b8b76be49d91d78ebaf9998`,
  payload
  `8f41e576ac8551ead8fd75d87c4b8d4aee85f5ba1007c0dcf8aaeb62fbfb1439`.

The review-owned result has SHA-256
`a96b8549a5f77176ba638170c9e549a099c525387a0d3ec6226a69e33cf77de9`,
payload
`7966d7b885e32486f3599df05d544d57961e6a1253c8c066736bcf3a8020aa6a`,
status FAIL, and 37 mismatches. Its 37 count comprises this typed-role
substitution plus stale current-language hash/payload cells in the two current
release narratives and the promotion companion. The reported “17 of 18”
promotion cells is exact: only the theta2 ledger file hash remains current.

All three stale narratives are current `RELEASE_LOCK.json` members and none is
in `HISTORICAL_ARTIFACT_REGISTRY.json`. The report accurately notes that the
promotion companion is not the current submission proof authority while still
being a bound, cited theorem-closure companion. The reseal scope follows from
the changed supplement/static-audit/current-narrative bytes and their lock,
crosswalk, telemetry, manifest, archive, and tag descendants.

## Independence and theorem-strength audit

The report now describes the independence boundary accurately:

- the exact mathematics script imports no submitted classifier, grammar, or
  expected-output data but is representative rather than all-family;
- the broad structural scan does not call the decisive submitted classifier,
  but shares the submitted primitive grammar/serialization conventions;
- no second symbolic engine re-expands every high-degree polynomial body;
- no second all-family orbit implementation independent of the grammar is
  claimed; and
- exhaustive submitted producer/replayer/mutation layers therefore remain
  load-bearing and were freshly run.

The integrated promotion of C04--C09 from the mathematical subreview's
conditional UNVERIFIED status to final PASS is justified by the fresh full
41-layer replay, focused full-family producers/replayers, mutation suites, and
independent structural joins. The report does not claim that hashes alone,
sampled ranks, literal polynomial-body equality, or stored PASS status proves
those layers.

No theorem scope is overstated. The excluded mixed-sign, boundary, singular,
higher-level, merely weak-class identifiability, full-image equality,
numerical-stability, bit-complexity, noisy-data, and finite-sample statements
remain excluded. The weak-class result is presented only as the explicit
sharpness family.

## Corrections made to the draft

I made only factual/protocol corrections; none changes the HOLD or any
scientific layer status.

1. Replaced the draft's custom topical meanings for C01--C13 with the exact
   package-crosswalk meanings. This removes a serious label ambiguity while
   retaining every requested mathematical topic across the aligned rows.
2. Corrected the evidence-class summary to identify C05--C09, rather than only
   the former C08--C09, as the principal exhaustive computational residue.
3. Added explicit disclosure that remote-host visibility and cryptographic
   tag-signature verification were not performed; only the local annotated
   tag object, commit, tree, blobs, and ancestry were checked.
4. Replaced an unsupported broad novelty-search sentence with the exact
   boundary: this review checked the load-bearing attributions and nearby
   submitted references but did not attempt an exhaustive priority search.
5. Replaced fourteen `n/a` peak-memory entries with their recorded wrapper
   values and added the two archive-rebuild runtimes and maximum RSS values.
6. Made mutation coverage explicit for strict-domain alterations,
   rank-sampling substitution, certificate-degree reassignment, stale
   PDF/report/source hashes, and missing TeX/Bib inputs.
7. Tightened C04, C05, and C10 wording to cover the exact crosswalk claims:
   licensed triangle semantics, raw-direction uniqueness/75 exceptional rank
   representatives, and the triangle germ's role in global genericity.

## Residual disclosures, not report defects

- Exact numbering in the inaccessible Englander bioRxiv v4 text remains
  UNVERIFIED, while the imported content and submitted K2P algebra are checked.
- Remote repository availability and tag signature are unverified; local Git
  provenance is verified.
- The report does not claim an exhaustive novelty/priority guarantee.
- A second wholly independent grammar and a second all-high-degree symbolic
  engine were not supplied; this is disclosed and does not masquerade as
  independent evidence.

I found no remaining wrong count, hash, runtime, path, source-line reference,
status, severity, reseal dependency, or theorem-strength statement in the
corrected report.

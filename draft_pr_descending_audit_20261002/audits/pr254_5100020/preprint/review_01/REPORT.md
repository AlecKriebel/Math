# Fresh preprint and verification-package adversarial audit 1

**Verdict: PASS for the exact frozen candidate. Mandatory corrections: none.**

Completed 2026-10-13 UTC. The mathematical theorem, source matching and credits, bounded result framing, five-page rendering, reproducibility archive, and exact submission metadata have no unresolved concern within this audit's assigned scope. The user's requested second fresh sequential reviewer remains a separate workflow step; this report does not publish, merge, stage a deposit, or substitute for that step.

I independently reconstructed the proof and recorded my mathematical conclusion before reading any earlier PR254 mathematical or priority verdict. I then challenged the source/priority/provenance alignment against the primary papers and included reports. I did not edit the manuscript, archive, PR, branch, tracker, or deposit, and did not contact outside individuals or other shard chats. All authored work is in preprint/review_01/.

## Frozen inputs independently confirmed

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| odd_origin_area_product.tex | 16257 | e2f115f1eee7489a9d888b9d1b639ac851e5442402fd453556612c1f39e3e8fd |
| output/pdf/odd_origin_area_product.pdf | 70407 | 687c633a92a61f1962d719be628ef5e119e077846254456f89a088d5fd13f34f |
| odd-origin-area-product-verification.zip | 170660 | 99666e523c0b78c2c8f73b8d42ed993d207a210b50cf12cd908c455cc4ad6d26 |
| metadata.json | 2011 | e468d37d5e5aea602e7572bc22f12c4576c28f74e4554e1568f77c177167b3d7 |
| zenodo-deposit.json | 2236 | f70de8848c1a874a7a582cc39dfffd16141bf067bee9c7337664c54397ec86a0 |

The original historical proof preserved in the ZIP has SHA256 ff2b1d78a1b94997d366d5173243ea95b949d5ae24574471639740b35cf2c16e, matching the original intake. It is intentionally different from the current standalone paper source. The prior audits bind that historical proof, and the present review binds the above current TeX/PDF/ZIP. This distinction is clear in the package README.

## Exact accepted claim and success criteria

For a fixed noncircular ellipse a>b>0 and a strict nested nondegenerate confocal elliptical caustic alpha>beta>0, each primitive family of least odd period N>=3 and admitted coprime winding has constant product of the signed original-side origin-pedal area and signed original-vertex origin-antipedal area. Every consecutive real antipedal intersection is finite. Circles receive a separate direct argument. Signed stars, reversal, repeated traversals and possible zero derived area are interpreted correctly. Hyperbolic/collapsed caustics, unsigned face areas, outer/inner polygon substitutions, and primitive parity manufactured by repeated lists are excluded.

Success requires a universal proof of that exact construction, an exhaustive complex pole analysis, source definitions matching the theorem, reproducible finite controls accurately labelled, consistent title/author/date/license/disclosure, and a self-contained current deposit kit. Neither prior PASS flags nor numerical samples meet the universal-proof requirement.

## Independent mathematical findings

The detailed checkable reconstruction is in INDEPENDENT_DERIVATION.md. All twelve numbered equations are correct, and the universal proof closes without transferring the central difficulty to another unproved invariant.

1. **Canonical domain and stars.** Stachel's Theorem 4.3/(4.9) supplies actual reflected trajectories with v=2K tau/N, delta=2v, a=alpha dn(v)/cn(v), b=beta/cn(v). The parameter k is the caustic eccentricity; numerical libraries use k^2. Strict nesting, confocality and least period follow explicitly. Since gcd(2tau,N)=1, real periods 2K and delta generate ell=2K/N. Every admitted coprime star is included.

2. **Real intersections and the actual polygons.** The chord determinant is 2ab sn(v)cn(v)dn(u)/(1-k^2sn^2(v)sn^2(u)), strictly positive on the real axis. It proves independence of consecutive original radial normals. Solving their named lines gives the stated intersections; expanding adjacent shoelace determinants gives exactly F(P,Q). It is a bilinear meromorphic continuation with no conjugation or division by complex norm. Foot projections use the actual original sidelines, not boundary tangents.

3. **Complete divisor and the dangerous finite endpoint distinction.** D has one double pole per 2K by 2p cell and precisely the two distinct simple zeros p+/-v, with slopes +/-2cd/s. B has simple poles there, a simple zero at p with opposite finite endpoints, and a simple zero at r=K+p with coincident finite endpoints. These exhaust the support. At coincidence the exact polarization identity makes the numerator O(z^2), even for zero complex norm. At opposition the singularity is genuine: H(P(p+v))=alpha^2d^2/(c^2s^2)>0 and the numerator is 2H^2, so its nonzero simple-pole residue is H^2s/(iab c). The manuscript correctly retains this pole.

4. **Incident cancellation, including N=3.** Each F incident to a pole vertex has order at most two, while their sum is exactly G(z)-G(-z). Its even negative Laurent coefficient cancels, leaving at most a simple pole. There is only one pole vertex at the relevant phase modulo 2K and no edge with two pole endpoints. For N=3, the remaining edge is the already-accounted opposite-endpoint term and adds at most a simple pole. At every odd period the midpoint opposition classes reduce to the vertex classes because v=tau ell.

5. **Trace uniqueness and forced zeros.** On X=C/(ell Z+4p Z), S=sum dn has exactly two noncancelled simple poles p,3p, with residues -i,+i. Its evenness, real period and 2p antiperiod force zeros at p+ell/2,3p+ell/2. These exhaust the complete simple zero divisor by total-order equality on the compact torus. Therefore S(w)S(w+ell/2) is constant. Matching residues and eliminating a holomorphic antiperiodic difference gives U=c_*S, including U identically zero. The proof never assumes the desired product.

6. **Credited pedal factor and precise shift.** The side tangent is n(u) dot X=1, n=(-sn(u)/alpha,cn(u)/beta), so its origin foot is Q=n/(n dot n), exactly equation (11). Q vanishes at common Jacobi poles and has possible even double coordinate poles only at dn zeros. The regular-neighbor difference is O(z), reducing the incident area pole to simple. Its area has the same antiperiod and shifted pole classes, hence T=c_p S(u+K). The actual pedal uses u=w+v, and (v+K)/ell=tau+N/2 is a half-integer. This gives the complementary-divisor constant product.

7. **Controls, zeros, units and limits.** The circle stars have radii R cos(theta/2) and R/cos(theta/2); theta in (0,pi) gives finite intersections and product N^2R^4sin^2(theta)/4. The common-caustic N4 diamond and rectangle are genuine reflected strict trajectories, with exact products 225/4 and 289/4; they refute an unrestricted even extension. Reversal negates both areas, repeats scale the product quadratically, and uniform length scaling gives the correct fourth power. No derived area is divided out, so zero signed area is harmless. No excluded limiting torus or collapsed/hyperbolic caustic is silently invoked.

**Mathematical remaining gap: none in the admitted domain.** The note proves invariance; it does not promise an explicit value for the noncircular constant, which is unnecessary for the source observation.

## Source credits and bounded priority

SOURCE_AUDIT.md records source URLs, pins and the exact scope checks. I independently authenticated the three original primary PDFs, visually inspected both k403,a Table 5 rows, and visually checked Stachel's canonical theorem. The signed unprimed constructions match the source invariant exactly. DLMF supports the period/pole/zero/shifts and addition inputs. The bibliography's accessed UTC date is consistent with this review and current paper date.

Independent downloads of KLS2003 v2 and Khare–Sukhatme Landen v1 match the included classical audit's pins. KLS Section 2.1.1/(17)–(20) is a real method antecedent to the cyclic simple-pole reduction, and Landen (13)–(15) is a real antecedent to the trace representation. Both are credited. The immutable PR204 proof was fetched independently, hashed and read completely; its prior pedal mechanism is explicitly credited and reproduced, making the present paper self-contained.

The strongest covering combination would be PR204's odd A A_O theorem plus an earlier all-odd A*_O/A theorem for the actual original origin antipedal. AST's odd original/outer tangent ratio concerns different lines; the exact construction check prevents a simple relabelling. I independently inspected the neighboring focal-product paper's broader Lemma 4 and its complete pairing argument. It requires central pairing and a fixed focus, which fail for primitive odd noncircular origin families. Its generic equation (16) already gives the elementary antipedal edge formula: F alone should not be claimed as a new general formula. The frozen paper makes no such claim; its additional step is the actual construction's divisor analysis and odd-lattice application.

Fresh object-based searches found no covering predecessor. I then read the complete included mathematical and priority reports and relevant provenance ledgers. Their bounded search and access-failure limitations agree with the note's modest claim. A failed direct EulerSolve0020 retrieval is not treated as evidence of absence. No claim to discover the original invariant, invent the method, certify historical firstness, obtain source-author acceptance, or receive human peer review is made.

**Source/framing remaining gap: none for the bounded claim actually stated.** Exhaustive worldwide firstness remains uncertified, expressly unclaimed. A future authenticated earlier all-odd original-origin antipedal ratio would reopen priority; that is a limitation of every bounded search, not an unsupported assertion in this note.

## Archive integrity and actual reproduction

I safely extracted the ZIP within review_01, rejecting absolute paths, parent traversal and symlinks. It has 50 file entries and 517632 uncompressed bytes. Its 49-file MANIFEST.json covers exactly every other distributed file once, with no unmanifested file. Every listed byte length and SHA256 independently matches. CHECKSETS.json's nine source-script hashes match. The packaged paper source and metadata are byte-identical to the current standalone source and metadata. The deposit metadata object is semantically identical. PACKAGE_INTEGRITY.json records these checks.

The runner was actually executed from the extracted root with the assigned read-only runtime:

```
/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python run_verification.py
```

The runtime is Python 3.14.6, SymPy 1.14.0 and mpmath 1.3.0 on macOS arm64. Every checkset completed successfully with a complete receipt match, ignoring only top-level generation UTC and elapsed time as documented. REPRODUCTION.json records that actual result.

| Checkset | Reference scope reproduced | Result |
| --- | --- | --- |
| author_exact | 14940 finite exact algebra/construction/lattice assertions | PASS, complete receipt |
| author_numeric | 19296 direct high-precision diagnostics | PASS, complete receipt |
| original_independent_exact | 15698 independent finite exact controls | PASS, complete receipt |
| original_independent_numeric | 1820 independent direct geometry diagnostics | PASS, complete receipt |
| complex_exact | 25369 exact controls, 4225 finite primitive lattice families | PASS, complete receipt |
| complex_near_poles | 3494 diagnostics, 19 families, 220 digits | PASS, complete receipt |
| cartesian_exact | 302 exact checks plus 4141 finite lattice controls | PASS, complete receipt |
| cartesian_numeric | 139411 diagnostics, 94 noncircular families/282 phases and five circles | PASS, complete receipt |
| priority_construction | Exact distinctions and generic-triangle negative control | PASS, complete receipt |

The runner/checksets contain no external-data runtime dependency, no import of excluded source papers, and no reliance on repository-specific locations. Each script is copied into its own temporary directory, where any generated receipts are written. The package remains unchanged after execution. Dependencies are precisely pinned and the README gives POSIX and Windows setup conventions. The Python code uses features available in the documented 3.11+ range; execution on every operating system is not asserted. The reference receipts include finite geometry and extreme interior-modulus/near-complex-pole diagnostics, not interval or proof-assistant certification. The written proof carries the all-period quantifier.

HISTORICAL_MANIFEST_RECONCILIATION.json additionally checks 29 retained or renamed packaged hash references in older audit manifests. Its 65 nondistributed historical records are original omitted source/checkpoint files or excluded reading/provenance materials; they are not runtime dependencies and are explained in the README. The complete current package manifest independently protects every distributed byte. The preserved historical proof's pending-review label is explained rather than silently rewritten. Initially failed reviewer scripts are excluded from executable successful checksets and their historical failure is explicitly acknowledged.

The ZIP contains authored reports/pins, not whole third-party PDFs/archives/text/image extracts or raw provider responses. Its extension/content inventory agrees with that promise. Newly read third-party copies and source-page renderings in this review are removed before its final authored-evidence freeze; the source pins remain. This review is kept outside the frozen ZIP, which was neither rebuilt nor augmented.

**Reproducibility/package remaining gap: none.**

## PDF and exact submission metadata

I generated an independent Poppler rendering directly from the frozen PDF at 110 dpi, then visually inspected all five pages. The title, author, ORCID, date, theorem, all numbered equations, source attributions, controls, disclosures and eight references match the TeX. Pages are legible, with no clipped formulas, overlap, lost symbols, broken glyphs or unusable references. Page transitions through the trace proof and N3 discussion are ordinary paragraph continuations. RENDER_VERIFICATION.json pins the independently generated images. PDF metadata has the exact title and Alec Kriebel author, five Letter pages, no encryption and no JavaScript.

The current manuscript, archive metadata and deposit object consistently identify:

- Title: An odd-period pedal-antipedal area invariant in elliptic billiards.
- Alec Kriebel, Independent researcher; ORCID 0009-0001-9320-500X.
- 13 October 2026 / 2026-10-13, version 1.0.
- Open preprint, CC BY 4.0, matching the authored-materials LICENSE.
- Extensive AI use in solving/verification/research/coding/writing/internal adversarial review; unrefereed, without external human peer review or proof-assistant formalization.

The kit's file objects are precisely {"path":"output/pdf/odd_origin_area_product.pdf"} and {"path":"odd-origin-area-product-verification.zip"}. Both resolve to the frozen bytes above. No obsolete copied filename, unsupported upload path, phantom DOI or falsely assigned coauthor is present. SUBMISSION_METADATA_CHECK.json records the exact semantic comparisons. No deposit was staged by this audit.

**Rendering/metadata/submission-readiness remaining gap: none in the frozen kit.** Actual publication and the requested second review remain actions for the parent workflow, not completed by this report.

## Mandatory corrections, optional preferences and limits

Mandatory corrections: **none**.

Optional preference, not a condition of this PASS: add the nearby focal-product preprint as further related work to mark equation (16)'s generic area formula antecedent even more explicitly. The present absence of any formula/method-firstness claim already makes the current framing correct. Reference [2] already uses the exact authenticated v11 PDF title, which differs from the arXiv landing-page title; no bibliography correction is needed.

No extra tests, rewrite or package rebuild is requested. The strongest verified result is the full stated universal invariant, with actual finite original constructions and its direct circular extension. The exact remaining research gap within that stated theorem is **none**. Human refereeing, proof-assistant formalization, interval numerics, an exhaustive historical priority certificate, and excluded caustic/parity extensions are not supplied or implied.

FINAL_AUDIT_MANIFEST.json freezes this report, independent derivation, source audit, reproduction/integrity/render/metadata receipts, source pins, research log and the exact candidate identity. This audit is complete: **100% of its assigned review scope**.

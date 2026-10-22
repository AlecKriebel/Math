# Required source-description correction

This correction map applies only to the frozen input bound by manifest SHA-256 5ae79fd9ca09fc095a33d7acfa27818377163c1eb2161977ff172cf641420616 and proof SHA-256 76d197a8fc07f7e3796d67a24308531aa315b0aa03a69f3a2122c3bdf7f77b68. Line numbers are those input files, not a future revision.

## Authoritative finding

The journal offprint at https://ggsmith.ca/Papers/diRoccoJabbuschSmith.pdf is 365,988 bytes, SHA-256 29d020ccdfffbb91149ed6d72bd3c32306865dc7d4f503bbf581d241b32d0a2b. Printed p.7728 / PDF page 14 prints (-1,-2) in the polygon indexed by e1-e2. Both direct rendered pixels and text extraction confirm the minus sign. The arXiv v3 PDF, SHA-256 adb8e9d5c9fbf2d8bb9d5f9f811e126be277f92b69de8b49af6861b16695f991, prints the same coordinate on p.13.

The claimed journal typo is an error in the verification packet, not an error found in these sources. The synthetic vertex (-1,2) is mathematically invalid for e1-e2, but it is not what that source polygon prints. Do not attribute that synthetic corruption to the published authors.

## Required changes, by file

1. PROOF.md, line 3: replace the phrase about a local printed sign error with a statement that the source coordinates agree and reading limits are in SOURCE_GATE.md.
2. PROOF.md, line 117: replace “published polygon typo” with “a synthetic polygon-coordinate sign error.” Keep the valid numerical test.
3. PROOF.md, line 119: change the heading to “Source agreement and attribution boundary.”
4. PROOF.md, line 121: replace the paragraph with the following original verification prose:

   The journal's printed p.7728 and arXiv v3 p.13 both give (-1,-2) as a vertex of the polygon indexed by e1-e2. Its second-ray upper height is -2, so every permissible vertex has b <= -2. The remaining bounds give the other vertices (0,-3) and (0,-2). These coordinates agree with the explicit frames. Replacing (-1,-2) by (-1,2) is used only as a deliberate synthetic negative control; no printed sign discrepancy was found in the inspected sources.

5. SOURCE_GATE.md, line 21: change the heading to “Source coordinate agreement.”
6. SOURCE_GATE.md, line 23: state the same agreement and synthetic-control distinction, and explicitly acknowledge that the earlier frozen packet incorrectly alleged a journal typo if the revision includes audit history. Do not imply that the published source was corrected.
7. README.md, line 16: replace the entire paragraph with: “The journal and arXiv v3 polygon coordinates agree with the filtration-derived construction. The verifier rejects a deliberately sign-flipped coordinate as a synthetic negative control.”
8. APPROACH_LOG.md, line 9: replace only the final sentence about identifying and correcting a published sign error with: “The polygon coordinates were checked against the primary filtration data and both inspected source versions; a synthetic sign flip is rejected by the verifier.” If logging the revision, attribute the earlier allegation to this packet's source-description error.
9. SOURCES.json, the journal entry's `inspection` at line 27: remove “Printed polygon sign typo recorded.” Replace with “The e1-e2 vertex (-1,-2) agrees with arXiv v3 and the filtration-derived data.” Preserve the verified source URL, size, and hash.
10. STATUS.json, `limits` entry at line 24: remove the false correction claim. A suitable replacement is: “The inspected journal and arXiv v3 coordinate agree; a synthetic sign-flip test is not a source discrepancy.” Update independent review status only for the revised packet once that review is actually complete.
11. VERIFY.py, lines 223–225: identify the first coordinate as source-consistent and the second as deliberately synthetic. Suggested comment: “Source-consistent polygon vertex and deliberate synthetic sign flip: heights (0,-2,3) force b <= -2.” Suggested assertion labels: “source vertex respects second ray” and “synthetic sign flip violates filtration.” Do not alter the input frames or either tested coordinate.
12. VERIFY.py, line 267: rename `publication_typo_control` to `synthetic_polygon_sign_control`. A suitable value is “Synthetic (-1,2) rejected; source-consistent (-1,-2) satisfies the e1-e2 second-ray bound.”
13. RESULTS.json, line 21: regenerate from the corrected VERIFY.py; do not edit the output independently of its program. The renamed key/value must match byte for byte. Expect the same 79 assertions and all numerical results unchanged.
14. MANIFEST.json: regenerate byte counts and hashes for all changed members. Record the new manifest and proof SHA-256 externally. The original ten-file packet must remain unchanged and the revision must be a separate frozen packet or separately versioned object.

## Dependency trace and release gate

- Scholarly source bytes: unchanged, independently matched.
- Bundle input bases and characters: unchanged; already use (-1,-2).
- Transition matrices, cocycles, curve splittings, tau: unchanged.
- Global section computation and jet ranks: unchanged.
- Source narrative, labels, and JSON schema key: corrected.
- Generated author results and manifest: must be regenerated.
- Independent revised-packet binding and replay: required before acceptance.

The present mathematical verdict is PASS. The present source-integrity verdict is CORRECTION REQUIRED. A clean replay alone cannot remove the latter: the replacement prose and attribution must also be inspected.

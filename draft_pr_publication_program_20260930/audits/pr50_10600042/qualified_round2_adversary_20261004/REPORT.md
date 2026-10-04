# Second independent adversarial review: qualified PR50 research note

**Verdict: PASS for the qualified research-note release. No substantive mathematical or package defect, and no required repair, was found. Historical priority is UNRESOLVED.** This verdict relies on the human’s explicit PR50-only exception allowing publication with incomplete access to Nencka’s fuller texts. It does not establish a novel resolution, contemporary openness, conventional human refereeing or formal proof certification. It does not claim that upload, DOI creation, spreadsheet registration or merging has already occurred.

The reviewed operative package is `publication_package_v3`, with the four full-byte input bindings in `INPUT_PINS.json` and `REPRODUCTION.json`. The editable manuscript is 17,320 bytes, SHA256 `2081d82e4acc49ff7f8cad2549c886ef1e16b616172b64370de43d17116f2ee8`. The first qualified reviewer’s verdict and controls were not consulted. The original submitted candidate and its historical review were read, the latter only after the independent mathematical analysis and new computations had completed; its verdict supplies no proof for this review.

## Exact target and categories

The survey’s actual Problem42 page was personally inspected. It asks for a Markov formulation involving even strand counts, without requiring minimality or uniformly bounded geometric support. The note supplies explicit algebraic word schemes for both ordinary oriented, unframed classical and virtual closure. Tagged even states retain their strand counts; empty words on two and four strands cannot be identified. The ordinary/plat distinction is essential and correctly illustrated by the identity two-strand braid. No welded forbidden relation is imported. Framed, transverse and stronger uniform-locality formulations are explicitly excluded rather than silently substituted.

The original fifteen scientific files are separately bound and preserved. Original target10600042 / AMR-105-0042, submitted head `7260315f8b8b193020c09d4ef6df9d943a3a13ff`, one original substantive attempt out of five. This review contains zero new central proof attempts and no edits to the scientific candidate or release payload.

## Independent universal proof audit

I reconstructed soundness first, without assuming completeness. C is an ordinary conjugation. In BC both prefixes are legitimate `(N-1)`-strand braids and are conjugate; their retained positive stabilizations have the same closure. In T the restricted prefix is again a legitimate `(N-1)`-strand braid, and both endpoints are its permitted stabilizations. D is two permitted stabilizations. R and L are exactly the primary virtual exchange formulas; BR and BL append the same legitimate positive stabilization to an exchange at total count `N-1`. The support bounds are sufficient in each case, including the shifted old blocks in BL. Consequently each move preserves the relevant oriented closure, in either direction. Odd auxiliary objects in this verification are not states of the explicitly defined even calculus.

For completeness, independently regard the unrestricted Markov system as a graph of tagged words, including defining relations in arbitrary contexts. Map each even vertex to itself and each odd vertex `(m,w)` to `(m+1,w sigma_m)`. The map preserves closure. The complete edge-type partition is:

| Unrestricted edge | Even count | Odd count |
|---|---|---|
| Defining relation | same relation | same entire old context, positive tail retained |
| Conjugation | C | BC |
| Stabilization, parity of smaller count | D | T |
| Right virtual exchange, parity of total count | R | BR |
| Left virtual exchange, parity of total count | L | BL |

For an odd exchange count `m`, let `N=m+1`. The unshifted blocks use indices at most `m-2=N-3`; the exchange index on the right is `m-1=N-2`. On the left, only the old blocks move from index `i` to `i+1`; their maximum is `N-2`. The appended positive crossing is separately `sigma_(N-1)`. Thus the exact BR/BL restrictions and endpoints follow without moving the padding tail into the shifted block. All destabilizations and reversed exchanges are covered by reversibility. Group-element choices cause no gap: words representing the same fixed-level braid can be joined by defining relations, and right inclusion preserves those relations in the old context. The padding fixes the original even endpoints exactly. Every unrestricted chain therefore becomes an allowed even chain; it is not an unspecified compressed-path definition of a move.

Alexander representation followed by padding gives every nonempty link an even representative. The classical chain contains no virtual letters or exchanges, so its four-scheme theorem is independent of any virtual simplification. The certificate-height formula follows from the monotone rounding function `m -> m+(m mod2)` and concerns a supplied certificate only.

Boundary cases were checked independently: one-strand empty braid pads to the two-strand positive crossing, the unknot; BC at2 has empty blocks; R/L at2 are identity relations; the smallest odd exchange has total count3 and gives BR/BL at4. All unlink tags are preserved. The optional empty link is an isolated zero-strand state. There is no move accidentally changing empty closure into nonempty closure, nor a claim that a certificate can be found algorithmically from the height observation.

## Actual primary dependencies and historical statements

I personally viewed Kamada’s pp5–7 for the oriented virtual category, braid presentation, representation theorem, right inclusions/stabilizations, and both exchange formulas; Kauffman–Lambropoulou p30 independently agrees on sign order and left inclusion. Gorsky–Kivinen–Simental p5 states the classical representation/Markov inputs, and [Lambropoulou’s primary survey](https://arxiv.org/html/1103.4397v1) independently makes the oriented classical version explicit. These established unrestricted theorems are imported, as the note says; the new finite computation does not certify their proofs.

Nencka’s actual two printed1996 pages and copyright/ISBN leaf were personally inspected. The announcement uses power-of-two levels, signed long tails, and a generalized relation following a new interwoved-string representation. It does not supply definitions and proof sufficient to verify an ordinary-closure interpretation. A signed tail at level `2^n`, `n>=1`, groups into ordinary double stabilizations, so that source cannot be dismissed as irrelevant merely because it uses a subsequence of even counts. The note correctly leaves the role of a one-strand level unspecified and makes neither a refutation nor an earlier-resolution certification.

The note’s distinction from conjugation-plus-double moves is logically sound: D followed by T produces all four classical double-sign choices, but does not show BC/T can be deleted. Fiedler’s full proof is not claimed to have been read; the comparison is explicitly reported and is not a premise of the new proof. A fresh read of the [1998 publisher page](https://mfat.imath.kiev.ua/article/?id=71) confirms its authenticated article metadata and unavailable full-text section. The fresh AMS and WorldScientific tool reads failed to provide full bodies; no missing content or literature absence was inferred from those failures. The1998/1999/CPT1996 bodies remain unread and their priority implications remain unresolved. No third-party source body is included in the release ZIP.

## Independent attempts to falsify the word schemes

I wrote `independent_color_stress.py` without importing, copying, or calling the author checker. It computes Fox-coloring fixed-space dimensions through finite-field matrix elimination over F3 and F5, plus signed ordered intercomponent crossing matrices from direct strand tracing and canonical component relabeling. These are necessary invariants, not equivalence certificates.

The actual run tested **22,829 scheme pairs**, making **68,487 necessary-invariant comparisons**. For exchanges it enumerated every virtual block of lengths0,1,2 at total unrestricted counts2–5, covering both parities and both directions of exchange. C/BC used all block pairs of lengths0,1; T/D used all prefixes of lengths0,1,2 at even counts2,4,6, with every permitted classical sign and virtual type. All tests passed. The enumerator includes classical words as a subset and imposes the displayed support restrictions. The independently computed illegal T example has Fox3 nullities2 versus1 (color counts9 versus3); the illegal R pair has the two stated unequal ordered crossing matrices. The false zero-shift L pair has equal component counts but unequal crossing matrices, confirming the importance of literal source-bound shift controls.

These checks supply a materially different adversarial mechanism from the shared endpoint construction in the publication checker. They remain finite supplementary tests. The universal proof above, rather than their successful output, establishes the theorem conditional on the imported unrestricted results.

## Reproduction, PDF and complete package audit

All commands were genuinely executed with actual child PIDs, operator UTC intervals, exit codes, complete stream bodies and stream SHA256 bindings in `COMMANDS.json`. Prelaunch copies of this reviewer’s two programs are retained. Author/checker provenance in the published verification record is historical attribution, and is not relabeled as the present run.

- Extracted exactly the declared ten flat ZIP members; verified names, CRC, normalized timestamps, regular-file modes, exact equality to all local operative support files and every checksum row.
- The unmodified Python3.9.6 checker completed at child92616 with the exact1,342-byte expected output: **7,114 checks,316 edges,1,716 relation-context cases and8 source-bound left controls**.
- The builder at child92617 created a byte-identical24,186-byte archive in the private extracted copy, then verified its exact members.
- The standalone source compiled at child92618 using cached Tectonic resources, without source edits or added dependencies. Text extracted from the original and rebuilt PDFs was byte-identical. All five independently rendered150dpi PNG pairs were byte-identical.
- I personally inspected all five original rendered pages. Equations, support restrictions, tags, proof, priority paragraph, AI/unrefereed paragraph and references are legible, without clipping, overlap, missing symbols or placeholder text. The PDF is five Letter pages and has matching title/author metadata.
- Manuscript, abstract, README, source qualifications, portable record and deposit description all disclose incomplete access and unresolved priority; credit Nencka; avoid first-discovery/current-openness claims; and distinguish AI review from human or formal certification.
- The deposit’s two files are exactly the reviewed PDF and verification ZIP. Alec Kriebel/ORCID agree with repository author metadata. CC BY4.0 applies to new text/documentation and MIT to code; the mixed-license support files explain this boundary. Imported publications are neither redistributed nor relicensed.

The four operative input pins were rechecked unchanged after reproduction. The review is finished for this qualified release, **100% review completion**, with **no mandatory repairs**. Publication, registration, exact-head merge and native reconciliation remain the parent’s next authorized actions. Historical priority is still **not certified**; the broader program is not complete.

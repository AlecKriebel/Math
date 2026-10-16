# Source and prior-work audit: 5100004

Checked 2026-10-01 UTC. Current conclusion: full k110 constancy is a credited consequence of a published theorem and the polarity calculation in CANDIDATE.md. The upstream OPEN-TRIAGE classification below is historical, not our present conclusion.

## Immutable imported record

Recovered the complete problem and the complete corresponding upstream research report from the repository's pinned Hugging Face revision. Binary range recovery scripts and their byte-range receipts are included. The sorted-JSON digest of the pair equals the catalog's review hash:

`3207a140ca51aa335a1cc8571577a932569a05ba8e5bd26ac4a45a1d335d3e7d`

The statement hash is `cd6d14e99e753d25ff62d9e4246fa6abcb77d779743858ca1ab4412253bef1bc`. The upstream report did not find a published general-N proof specific to k110, but suggested reducing to the known area invariants. It is not evidence of prior work by this campaign or Alec.

## Primary-source map

1. Reznik–Garcia–Koiller, arXiv:2004.12497v11, complete PDF and local extracted text: Sections1–3, Fig.1, Table2 p.5, bibliography. Defines P, outer P', contact P'', and signed areas; lists k110=AA'' for even N. It separately lists known k106=AA' for even N and the fixed ratio k113=A'/A''. Table inspected visually.
2. Published companion, DOI10.1007/s40598-021-00174-y, complete PDF/text: pp.341–345 and references. Same k110. The source context is a confocal pair of ellipses, not a hyperbolic caustic. Signed areas are explicit in equation(1). Table inspected visually. Its changed neighboring numbering is addressed below.
3. Chavez-Caliz, DOI10.1007/s40598-020-00154-8, complete publisher PDF/text read. Theorems3/6 give the needed even-period area product. Equation(5) specifies algebraic area; p.94 defines complex transverse general position. Section5 supplies the proof. CANDIDATE.md verifies that every strict noncircular confocal pair satisfies the actual general-position definition. No appeal to a generic limiting argument is needed.
4. Garcia–Reznik, DOI10.33039/ami.2022.02.001, complete accepted-manuscript PDF/text: conventions, Table1, Proposition4.9, appendices and references examined for low-N checks. This source is not used as a general-N proof. Its N=4 normalization discrepancy is independently evaluated below.

Downloaded primary PDFs, extracted complete text and page renderings are local reading copies only, excluded by .gitignore. source_manifest.json supplies their URLs, byte sizes and hashes. No source executable was downloaded or run. Searches for the precise k110 code and Chavez-Caliz area theorem were conducted, but the conclusion rests on the actual theorem and explicit reduction, not absence of search results or a search snippet. No outreach occurred.

## Edition differences cannot be ignored

The arXiv-v11 Table2 rows after k110 are:

- k111: A'A'', even N, unproved marker
- k112: A'A''/A², odd N
- k113: A'/A'', all N, value (ab/(a''b''))², credited to Stachel's private communication

The published Table2 instead has k111=A'A''/A² for odd N; its k112 line prints the product A'A'' with the same dimensionless value (ab/(a''b''))², and k113 is a focal-distance sum. We checked the actual pixels, not just extracted primes/slashes. The printed product cannot supply the ratio identity. Our derivation establishes the exact needed ratio without relying on an inaccessible private communication, and does not silently change another source row into a theorem. The k110 target itself is identical in both editions.

## Primitive period, caustic, angles, and signed area

For a genuine N-vertex Poncelet orbit in this task, N is its least period. The published proof works with the Poncelet translation of order N. An arbitrary even traversal count obtained by repeating an odd-period orbit does not meet that hypothesis. Repeated even primitive orbits pose no problem: shoelace area is multiplied by the repetition number in all three polygons.

The source's confocal-ellipse context means 0<lambda<b². The strictly interior caustic rules out antipodal consecutive endpoints, and therefore parallel consecutive tangents to the outer ellipse. There is no infinite outer vertex in the real family under consideration. Simple and star traversals retain their signed shoelace areas and traversal indexing. The angle symbols theta_i and theta'_i concern the original/outer vertex angles; no angle, half-angle product, focal angle, or choice of acute versus reflex representative appears in the reduction. In particular, the refuted angle factors in k107/k108 are not imported.

## Exact N=4 normalization check

For arbitrary a>b>0 set s²=a²+b². The primitive billiard quadrilateral

    (a,0), (0,b), (−a,0), (0,−b)

has outer tangent vertices (a,b),(−a,b),(−a,−b),(a,−b). Its caustic semiaxes are alpha=a²/s and beta=b²/s. The four contact vertices are

    (a³/s²,b³/s²), (−a³/s²,b³/s²),
    (−a³/s²,−b³/s²), (a³/s²,−b³/s²).

Each lies on its side and the caustic; the side equation at the first is x/a+y/b=1. Signed shoelace areas are

    A=2ab,  A'=4ab,  A''=4a³b³/s⁴,
    AA''=8a⁴b⁴/(a²+b²)².

Proposition4.9 in the inspected Garcia–Reznik PDF prints coefficient2 instead of8. The explicit construction detects this factor-four discrepancy under the stated definitions. It does not refute the k110 constancy assertion. For a=4,b=3 the exact areas are24,48,6912/625 and product165888/625; the printed value would be41472/625.

For a second phase, the rectangle with vertices (±16/5,±9/5), in counterclockwise order, has areas576/25,50,288/25. Its AA'' agrees exactly. The outer/contact products A'A'' do not agree (331776/625 versus576), an important negative control against confusing the source ratio with a product. These two quadrilateral geometries were already used for the separate k107 counterexample in PR147; their reuse here is explicitly credited.

## Prior user/campaign gate and related targets

- Main snapshot at intake: rank215, queued0/5. The campaign inventory independently lists no located prior user/campaign attempt for exact5100004. Its own caveat that main-queue state alone does not prove untouched status was respected.
- Rechecked all-state GitHub PR searches for5100004 and k110, and branch search for5100004: no results. `git log --all -- attempts/5100004` also found no history in the available refs. Consulted prior-user/campaign context for this exact target; no specific additional attempt was located. These negative searches do not prove the absence of all unindexed private work.
- Read the complete upstream report separately; it is not counted as Alec's proof attempt. Related-target-groups.json lists other billiard families but no exact5100004 group.
- PR147,5100001,k107: refuted printed angle/area formula on primitive four-period examples. Shared geometries only.
- PR148,5100002,k108: refuted printed angle/area formula on primitive six-period examples. Its exact hexagon coordinates are reused with credit as verification controls.
- PR149,5100006,k114: focal-distance product for N=2mod4, proved using an elliptic-function norm. It neither proves nor disproves k110.
- PR150: unrelated Hilbert–Burch problem30005408, not a billiard result.
- PR151,5100010,k120: a credited bicentric cosine-sum consequence via focal polarity; different polygons and invariant.
- PR110,5100032,k603: equality of two focal antipedal-distance sums by telescoping. No area-product transfer.
- PR140,5100023,k405: even-period antipedal-centroid property using central symmetry. No area-product transfer.

The verified remote PR/head metadata are retained in prior_work_remote_receipt.json. None of the above reviews is treated as an independent review of this proof. The shared bridge and edition warning were sent to the concurrently assigned k111 author before any separate conclusion there.

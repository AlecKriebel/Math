# Independent source reconstruction

2026-10-13 01:56 UTC; completion toward priority/classification audit 45%.
Written before reading current/historical priority audits or root priority conclusions.

## Native target and source

Native PR and header-derived queue gate passed at ac8b960bdda61c154cc30d7e3aba70389a9b139e. PR open, draft, author branch as assigned, checkout main. ID6800014 is claimed_solved, Turns2/5. Scope covers only that PR. The Morgan–Pansu PDF was freshly downloaded, hashed and its printed p12 visually inspected. Section11 poses the all-left-invariant-metrics local-maxima assertion and defines solvsoliton by Ric=cI+D on the fixed group's algebra. No completeness, real-type, or strict-local-maximum qualification is printed. The author construction, whose proof was supplied for verification rather than proof search, targets precisely this literal assertion. The author proof's conclusion about sources remains a hypothesis in this independent stage.

## Announcement and checkable-paper chronology

Lauret's freshly retrieved slides label the talk São Paulo, July23,2018. PDF pages71–73 (one-based), slide13/17, contain an explicit existence theorem announcement of local maxima which are not global and not solvsolitons. I visually inspected page73. The preceding slide defines the domain as the left-invariant metrics on the fixed almost-abelian group. This is a direct prior announcement of the literal negative answer. It is not merely a vague related conjecture, and it rules out first-announcement credit for the present packet. The downloaded file's current availability and internal date label do not independently prove its historical upload date. No proof or explicit matrix is on this slide; second variation is named as a method.

The fresh arXiv metadata pins I v1 to 2018-08-03 22:34:05 UTC and v2 to 2019-05-09 23:29:35 UTC. Actual PDFs and gzipped source for both versions were downloaded separately. The sources are single gzipped TeX, not tar archives. Both versions' introduction and section6.3 leave non-global local maximum existence, and specifically small-u local maximality of uN+C, unresolved. Theorem1.5 and Proposition6.11 identify a necessary Ricci-soliton structure for local maxima; they do not make every geometric Ricci soliton a local maximum. Lemma6.12 excludes sufficiently large u, not all u. Later unknown statements neither retract nor explain the slide announcement. I found no documentary withdrawal, typo claim about the announcement, or identified failure of its intended proof.

Publisher abstract metadata surfaced in search identifies journal DOI10.1093/qmath/haz020, QJM70(4),2019,1281–1304, online publication15July2019. Direct full-article retrieval returned403 and web opens returned errors. Thus the actually inspected full text is arXiv v1/v2, with v2 called final-to-appear by the arXiv metadata. I have not inspected the original journal full text and cannot certify its literal wording is identical.

II v2 was independently retrieved at arXiv1907.08014v2; arXiv dates v1 to18July2019 and v2 to27November2019. Its theorems concern global extrema under existence of an algebraic solvsoliton and specified algebraic classes; they do not exclude smaller non-global local extrema on the present imaginary-type group.

## Independent displayed-matrix check

I visually read D_t=J⊕tE12 and E_t=[[t,-sqrt(1+t²)],[sqrt(1+t²),-t]]⊕tE12 on I v1 printed p19 and v2 printed p20, and inspected matching TeX. My script imports no author/peer/root computation. From equation(3) in the traceless case it obtains s(D_t)=t²/2, q(D_t)=2t⁴ and F(D_t)=1/3. For the displayed E_t it obtains s=5t²/2, q=32t²+34t⁴ and F(E_t)=25t²/(59t²+32), rather than the printed4t⁴/(3t⁴+2t²). The discrepancy is positive printed-minus-computed for every t>0. The corrected function still tends to0. I independently verified E_t=T D_t T^{-1} with T=diag([[1,t],[0,sqrt(1+t²)]],I2), and D_t conjugate to D_1. Thus the discontinuity example remains valid; this does not establish a local maximum at any D_t.

The non-solvsoliton obstruction also checked independently: the rotation bracket forces c=-t²/2; the nilpotent bracket then has derivation residual t². A geometric Ricci soliton isometric to a nilsoliton under another group presentation does not satisfy the fixed-algebra derivation condition in the printed question. The group is imaginary type, neither nilpotent nor semisimple, and not completely solvable. Theorem6.5(ii)'s trA=trA²=0 condition fails since tr(D_t²)=-2.

## Candidate prior-tool routes and exact gaps

| Route | Independent result | Exact gap/status |
|---|---|---|
| Slide theorem as prior proof | Explicit announcement of the literal negative conclusion | No construction/proof in inspected deck. Prior-announcement evidence; cannot alone certify prior checkable resolution. |
| D_t family/value in §6.4 | Exact family and F=1/3 already printed in v1, not just v2 | Constant on this one-dimensional subfamily gives no comparison for mixed nearby metrics. |
| Lemma6.7 plus semidefinite Hessian | General computational tool capable of testing transverse directions | Null directions must be realized by a critical manifold or uniformly controlled; semidefinite Hessian alone is insufficient. Merely citing Lemma6.7 transfers the difficulty. |
| N+C is isometric to nilsoliton N | Geometric Ricci-soliton property consistent with fixed-algebra failure | Nilpotent-group global maximum concerns a different metric domain. Isometry of a base point does not transport every nearby metric on the original group to invariant metrics on the nilpotent group. |
| Global uniqueness theorems I/II | Characterize global maxima and exclude global maximum here | No implication that every local maximum is global. |
| Corrected E_t path and common flat limit | Verified distinct limiting values in the same conjugacy class | Limit at a flat boundary point does not compare metrics close to a fixed D_u, u>0. |

This is an audit of supplied claims and possible deductions, not an additional proof-search turn. A valid new application of the old general tools would be a new checkable derivation, not documentary proof that the complete deduction was previously available as a resolution.

## Bounded later-source search

Before comparison I issued24 queries in six batches, including exact functional title, DOI/arXiv citation, local-maximum wording, author bibliography and exact later-citing titles. Query results were received in this native session. Raw outputs of batches4/5 are privately preserved; the remaining raw search output is available in session tool history, not fabricated as saved bytes. Those two JSON files' manually typed01:56/01:58 UTC labels were mistaken future approximations: actual search calls occurred between the01:50:15 gate and01:55:02 clock read. They are query ledgers, not exact timestamp receipts; the downloader's generated UTC receipts are accurate. An erroneous malformed trial URL https://arxiv.org/html/2409.035 Lauret returned an error and was not used as evidence.

Freshly retrieved later cited papers: Jablonski survey2111.09782, almost-abelian groups2004.04369, and algebra structure1610.05365. The two almost-abelian papers cite I in broad introductory lists of applications; their stated theorem scopes concern structure/subgroups/quotients rather than this metric functional. The Jablonski survey §5.4 loosely states an affirmative claim about geometric Ricci solitons being maxima, citing I/II; that wording exceeds I/II's algebraic/global conclusions and conflicts even with I's large-u exclusion. It is not an independently checkable proof of the literal Question14. A citation lead to Böhm–Lafuente1811.12594 returned a23-page version with no pinching reference in text; treating every version of the same arXiv ID as equivalent would be wrong. Lauret's2017–2021 and2022–2026 bibliography pages list relevant publications; later local Hilbert-action titles concern a different functional and compact homogeneous setting. No blanket claim of complete bibliography coverage is justified.

## Independent provisional verdict

No earlier checkable complete resolution was identified within this explicit source/search bound. The exact family and value and an explicit prior announcement are established. Therefore firstness/novelty/current-openness certification fails; prior checkable proof status is unresolved. Claimed_solved can remain mathematically descriptive only if the user's status convention permits unresolved prior announcements while requiring positive evidence for already_solved. The exact user classification instruction is not in my fork; the parent must supply it before the final classification verdict. No-firstness attribution alone cannot settle classification or grant publication clearance. Suggested description: a direct proof of small-parameter local maximality for Lauret–Will's displayed family, with explicit credit to the2018 existence announcement, no firstness claim, and bounded priority uncertainty.

## Audit error preservation

Initial script comparison used Python structural equality for two equivalent symbolic polynomials and failed; the original bytes are preserved privately, then corrected to symbolic simplify(got-want)==0. The revised check PASS is reproducible and all outputs are exact. Attempting to parse the downloaded single gzipped TeX as tar also failed; decompression then succeeded. Both errors concern tooling, not mathematical source correction. No receipt or independence history has been backdated.

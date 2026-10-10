# Source, identity and prior-coverage gate

Inspection date: 2026-10-05 UTC.

## Identity and exact statement

The current repository descriptor catalogue identifies ID 30001603 as OWR-4527-007, title *Jet Spanning by Nef Toric Vector Bundles*, rank 698, source DOI https://doi.org/10.4171/owr/2010/45. The full local descriptor catalogue is 21,735,099 bytes, SHA-256 891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566, Git blob bd5c23e4e6c7e1901717a7e596477a7f6dc72425. The GitHub connector returned that same current remote catalogue blob, matching the exact local byte identity. This is descriptor identity, not a comparison against the old full problem-statement corpus.

The live URL https://www.unsolvedmath.com/problems/30001603 failed through the web tool and returned HTTP 403 through ordinary HTTP retrieval. Its full statement was not read. The old full AI/corpus record is unavailable and was not inspected. A descriptor's pre-existing statement hash is not being presented as a verified content match, and no AI evaluation report is claimed inspected.

The exact mathematical target was instead established from the authoritative report: Kelly Jabbusch, *Seshadri constants for toric vector bundles on toric varieties*, OWR45/2010, printed pp.2640–2641, PDF pages 28–29 of 38. Both pages were text-inspected and image-inspected in full. They specify an algebraically closed field and smooth complete toric varieties; the jet paragraph explicitly uses smooth projective varieties. P²_C meets all of these hypotheses. The condition is τ(E)≥k for an integer k≥1, with τ the minimum splitting integer, and the conclusion is k-jet spanning. The report does not add global generation. PROOF.md gives a faithful mathematical restatement, not an extract of the source.

## Decisive prior literature and inspected proof scope

1. DJS, arXiv:1409.3109v3, submitted 2014-09-10, version 3 dated 2017-02-01. Full PDF downloaded. Inspected overview, complex-field convention, the local/global section setup, Theorem 1.2 proof, Example 4.2 (pp.13–14), and the invariant-curve section including Example 5.3 (pp.16–17). Formula page 13 and split page 17 were also image-inspected. This is the exact data reconstructed in PROOF.md, not an assertion based only on an abstract.
2. DJS published offprint, Trans. Amer. Math. Soc. 370 (2018), 7715–7741, DOI 10.1090/tran/7201. Full PDF downloaded from the author's current site. Bibliographic first page, Example 4.2 (printed pp.7727–7728), and Example 5.3 (p.7732) inspected; pp.7728 and 7732 image-inspected. The author's publication page and arXiv record independently give the journal reference. No blanket inspection of every theorem in the full paper is claimed.
3. Hering–Mustaţă–Payne, *Positivity properties of toric vector bundles*, Ann. Inst. Fourier 60 (2010), 607–640, DOI 10.5802/aif.2534. Full primary PDF downloaded; conventions at pp.609–610 and Theorem 2.1 with its entire nef/ample proof at pp.610–611 were read. The packet reconstructs the needed nef argument. The ampleness half remains explicitly attributed and is not necessary for the refutation. No complete audit of the rest of HMP or of its underlying references is claimed.

The standard toric atlas for P², gluing of locally free modules, monomial regularity, projectivization of a bundle and projective effective-cycle degeneration are the geometric foundations. Explicit local matrices remove dependence on an unchecked Klyachko existence assertion. No computer proof-assistant validation is claimed.

## Source coordinate agreement

The journal's printed p.7728 and arXiv v3 p.13 both give (-1,-2) as a vertex of the polygon indexed by e1-e2. The second-ray filtration requires b <= -2, and the full filtration-derived polygon agrees with both sources. Replacing (-1,-2) by (-1,2) is only a deliberate synthetic negative control. The original frozen verification packet incorrectly alleged a journal typo; this revision corrects that packet's description, not the scholarly source. The direct bundle construction and invariant-curve restrictions are unchanged.

## Repository and earlier-attempt coverage

The current queue was read through the GitHub connector at `unsolved_math_prioritization/QUEUE.md`, lines 700–714; returned Git blob 5d33a968894980499cb3fbb6d84fe5cca5a47aa4. The target row is queued, 0/5. This alone is not evidence that no draft work exists.

Additional read-only checks of AlecKriebel/Math on 2026-10-05:

- Default-branch code search for 30001603: no results.
- All-state PR search for 30001603, nef toric, or OWR-4527-007: no results.
- All-state PR search for toric: unrelated toric deformation, movable-cycle, arrangement and Hurwitz-polytope work, with different target IDs.
- All-state PR search for jet, vector bundle, 30001603 or 4527-007: unrelated targets, no matching attempt located.
- Branch search for 30001603: empty.
- Branch search for toric, including its continuation cursor: unrelated branches only, then exhausted.

The search results were used as bounded prior-coverage evidence. Search indexing, unlabelled branches, unindexed files and private conversations are not exhaustively certified. No generic topic overlap was treated as a prior attempt. Raw API responses and catalogue records are excluded from this public packet.

## Bounded modern-literature search

Queries included the exact catalogue title, “nef toric vector bundles” and global generation, the report's jet conjecture, and “Toric vector bundles and parliaments” with erratum. The decisive primary DJS publication was located and inspected; the search did not locate a correction invalidating its example. This is not an exhaustive absence-of-errata or historical-priority certification. No claim is made that DJS explicitly discusses this particular OWR catalogue label; its example refutes the source implication by the complete elementary specialization in PROOF.md.

Public source URLs, byte lengths, SHA-256 values and precise inspection summaries are recorded in SOURCES.json. None of the underlying source files is redistributed.

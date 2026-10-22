# Source and previous-attempt gate

Target: **2301039 / AMR-022-1039, rank 564**, Hayman–Lingham Function Theory Problem 1.39. Checked 4 October 2026 UTC.

## Exact primary target

The requested [catalogue page](https://www.unsolvedmath.com/problems/2301039) was attempted using the web reader and direct HTTP. The reader could not retrieve it; direct HTTP returned 403. The target record and its complete previous generated report were recovered from a locally available copy of the public [ulamai/UnsolvedMath dataset](https://huggingface.co/datasets/ulamai/UnsolvedMath). Its source link is the Hayman–Lingham book draft. The generated report contains only an open-triage classification and a statement that an earlier search found nothing. It contains no proof or prior substantive attempt. That classification was not treated as authoritative.

[Hayman and Lingham, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), 21 September 2018, was retrieved in full. Printed p.19 was both text-inspected and visually inspected. Equation (1.8) supplies the missing catalogue definition alpha=limsup T(r,f)/[-log(1-r)]. Problem 1.39 has two parts, distinguished by whether poles are allowed, and the update reports no progress received. Both parts are retained. A historical reporting statement is not a certification of current openness.

Bibliography item [707] identifies D. F. Shea and L. R. Sons, *Value distribution theory for meromorphic functions of slow growth in the disk*, Houston Journal of Mathematics 12(2) (1986), 249–266. The [journal issue index](https://www.math.uh.edu/~hjm/vol12-2.html) confirms the citation. Its linked [original PDF](https://www.math.uh.edu/~hjm/restricted/archive/v012n2/0249SHEA.pdf) returned 403 in both web and direct HTTP. Its full proof was **not inspected**. The bounds 2 and 7 in PROOF.md are attributed historical context, not independently re-proved bounds or dependencies of our proved propositions.

## Current literature and exact dependency boundary

1. [Sina Nadi, *Sharp Deficiency Bounds for Meromorphic Functions in the Unit Disc*, arXiv:2609.05835v1](https://arxiv.org/abs/2609.05835v1), submitted 5 September 2026, was retrieved as a complete 27-page PDF. The statements, introduction and complete first-order proof of Theorem 1.1 in Section 2 were inspected. Its finite-alpha corollary and rational-kernel statements were checked for applicability. The paper concerns **Problem 1.40**, not a direct solution of 1.39. It retains an uncontrolled derivative-zero deficiency term; replacing that term by a favorable value because f′ omits 1 is unjustified. The later higher-order, finite-alpha and sharpness proofs were not fully audited. No theorem from this preprint is a dependency of our unconditional results.

2. Nadi's Theorem 2.5 quotes the growth and covering properties of the classical modular function from Tsuji, Theorem XI.29. The original Tsuji proof was not inspected. The modular note marks its logarithmic-characteristic quotation as context-only. The final unconditional rational statement is restricted to rational R having a zero at one of the three punctures. It does **not** require modular surjectivity. The broader implication from an arbitrary zero-free composition is explicitly conditional on the uninspected classical surjectivity fact. Nonvanishing at the center is proved directly from the q-product rather than imported from a covering theorem.

3. The exact classical formulas actually used in the modular proof were checked in [NIST DLMF 23.15](https://dlmf.nist.gov/23.15), [23.17.4 and 23.17.7](https://dlmf.nist.gov/23.17), and [23.18.1–3](https://dlmf.nist.gov/23.18). These give the nome convention, convergent lambda expansion/product, and the three modular transformation identities. The proof then supplies the whole derivative calculation, all three cusp coordinate factors, locally uniform convergence and Rouché zero counting. These DLMF identities are classical external inputs; this packet does not purport to re-prove the theta transformation theory underlying them.

4. [Paul A. Gunsul, *Value Distribution for a Class of Small Functions in the Unit Disk* (2011)](https://doi.org/10.1155/2011/537478) was located. The introduction, elementary exponential example and complete Section 5 theorem statements and argument were examined through the web reader's publisher full text/PDF. A direct PDF download returned 403; no local PDF copy is claimed. His class P imposes an extra small-logarithmic-derivative hypothesis. Theorem 5.2 is relevant to that narrower class, not automatically to all functions in the target. Its background finite-alpha second-main-theorem estimate is cited to Shea–Sons; we have not re-proved that dependency. No result from this paper is imported as a new unconditional theorem. Our elementary characteristic computation agrees with its beta/(2π) normalization for exp(beta*i/(1-z)).

The main PROOF.md uses only differentiation, holomorphic primitives, elementary local orders, Jensen's formula, the residue theorem and the contraction mapping theorem. All problem-specific arguments are written out. The modular note additionally uses the specified DLMF identities and Rouché's theorem. No generated catalogue claim or abstract is used as a proof certificate.

Searches covered the exact ID, title/number, Shea–Sons and derivative omission/slow growth in the disk, and the current primary sources above. No verified full resolution of 1.39 was found. This is a bounded-search statement, not an exhaustive novelty or current-open certification.

## Actual repository history checks

Repository: [AlecKriebel/Math](https://github.com/AlecKriebel/Math).

- The exact queue row was read as rank 564, queued, 0/5. Queue state alone was not used to infer absence of a previous attempt.
- All-state PR searches for `2301039`, `AMR-022-1039`, and `1.39` returned no match. A broader function-theory/Shea/Sons search returned other function-theory investigations; none of the inspected results was this target.
- Default-branch code search, ID branch search, and ID commit search returned no target match. Code-search absence is not treated as exhaustive.
- Actual root contents and the `problems/` tree were read. Tree `8f72e77ed517ba2424b4e74b324cda525e6373c3` had 652 entries and `truncated=false`, with no target-ID/Shea/Sons path.
- The actual attempts tree `0270c330cecec35524db98be465ebc4d2aa12d24` had 54 entries and `truncated=false`, with no target directory. An initial recursive transport failure was followed by a successful tree read.
- `review_v2/related_target_groups.json` had no occurrence of this ID. The complete relevant `reviews_0.json` entry contained only the earlier heuristic route assessment, not a proof attempt.
- Repository AGENTS.md, the queue directory's AGENTS.md and README.md were read. The present campaign's narrower status/turn-only queue-edit and no-remote-write-before-audit instructions control this packet; no queue tool was run.
- The directory API identifies the queue's actual blob as `59dba610d333684751e889818d21f66aba29cec9`. The returned queue body itself begins with an older SHA-looking literal line, `sha: c87c...`; that embedded text is not taken as the actual current Git object ID.

Successful checks found no substantive previous attempt. Untagged or unindexed work cannot be categorically excluded. No remote writes occurred during this investigation.

## Public projection

The public packet contains original proof notes, this provenance report, a five-approach log, status, exact checking scripts and their outputs, and a SHA-256 manifest. Local PDFs, their full text extracts/page images, catalogue records/reports, repository response caches, and private coordination material are excluded. SHA-256 identifiers of reading copies may be retained without redistributing the copies.

## Gate verdict

Ready for an independent audit of the **scoped partial results**, subject to explicit source limitations above. Not ready for a full-resolution claim, an independently verified historical-bound claim, or a novelty claim. A fresh uninvolved review must determine whether the partial packet is publishable. The entire original question remains unresolved in this attempt.

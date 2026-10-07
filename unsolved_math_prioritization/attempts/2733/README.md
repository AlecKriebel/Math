# Connected-sum ropelength: accepted formulation audit and partial deductions

**Problem 2733 / KP-1.74, rank 907. Canonical disposition: unsolved, 2/5 approaches.**

The exact frozen author artifact is independently accepted as a **partial formulation audit**. The intended nontrivial-summand part (a) and universal-positive-saving part (b) both remain unresolved. No corrected derivative was needed; no full resolution, novelty, or certified general splice is claimed.

## Read the work

- [Exact acceptance](independent_audit/ACCEPTANCE.md) and [machine-readable acceptance](independent_audit/ACCEPTANCE.json)
- [Independent mathematical audit](independent_audit/MATHEMATICAL_AUDIT.md)
- [Source review and access limitations](independent_audit/SOURCE_REVIEW.md)
- [Original proof deductions](original_author/PROOF.md), [report](original_author/REPORT.md), and [two-approach log](original_author/APPROACH_LOG.md)
- [Full-corpus verification](independent_audit/CORPUS_VERIFICATION.json), [five PDF pins](independent_audit/PDF_VERIFICATION.json), and [source inspection history](independent_audit/SOURCE_INSPECTIONS.json)
- [Publication metadata](PUBLICATION_METADATA.json), [publication-stage replay](EXECUTABLE_REPLAY_RESULTS.json), [file manifest](PUBLICATION_MANIFEST.json), and [checkpoint](RESEARCH_LOG.md)

## Mathematical scope

Thickness means reach/normal-tube **radius**, not diameter. The C1,1 Fenchel argument gives R(U)=2π. Because U#U=U, identity summands obstruct the literal unrestricted wording of (a). This is **only a formulation issue**, not a disproof for nontrivial summands. Split-link spectator blocks cancel under the specified separated selected-component sum.

For a proposed splice with length at most S+ε−s and reach at least 1−δ, where 0≤δ<1, the certified saving is only (s−ε−δS)/(1−δ). The missing step is a uniform construction certifying topology, length and global reach for arbitrary summands. A curvature bound or numerical tightening alone does not supply it.

The written mathematical review is AI-assisted and not formal proof-assistant verification or external human-referee acceptance. The full original Nature article was not inspected, and the current PubMed full abstract was not independently reproduced. The live problem page was inaccessible; the exact full corpus and actual 436-page K3 source established identity. No exhaustive novelty search is claimed.

## Preservation and reproducibility

The two ZIPs and two external manifests under `archives/` are immutable historical bytes. All 9 author and 15 audit members are also unpacked exactly. Historical pending-audit and no-publication fields are preserved as freeze-time facts; the later acceptance and this publication wrapper do not rewrite history.

Run `python3 verify_publication.py .`, also with `-O` and `-OO`, for fail-closed static archive/member, acceptance, inventory and metadata checks and negative controls. This wrapper does not execute archive code. Run `python3 original_author/verify.py` and `python3 independent_audit/verify_audit.py` for integrity/arithmetic and stored acceptance checks. These checks do not prove geometry or novelty.

The independently pinned replay runner supports six relocated author baselines and 14 hostile mutations in each of normal, -O and -OO modes (42 rejections). Its optional full corpus and source-PDF inputs are deliberately excluded. See the [audit instructions](independent_audit/README.md) for arguments. The publication-stage full-input replay supplied all three datasets and all five PDFs and compared outputs with the frozen accepted reports; the independent runner was also rerun under -O and -OO.

Only the current QUEUE.md row's Status and Turns change. Findings, chat links and every unrelated byte are preserved. Publication is a draft PR only; it includes no merge, auto-merge, release, DOI or outreach. Local checks are not a GitHub CI-pass claim.

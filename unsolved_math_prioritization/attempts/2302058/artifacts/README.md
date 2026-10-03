# A known answer to Hellerstein's natural-path question

**Problem:** 2302058 / AMR-022-2058, Function Theory Problem 2.58.  
**Proposed status:** already solved, affirmative.  
**Resolution credit:** A. E. Eremenko (1985).  
**Novelty claim:** none.  
**Independent audit:** required before publication.

There exists an entire function of infinite order with a nonzero omitted value α and no asymptotic path to α on the circle level |F|=|α|. The 2018 problem-list update already credits Eremenko with this answer, although the imported triage labels it open.

- [Source and exact-scope gate](SOURCE_GATE.md)
- [Full proof and normalization verification](PROOF_VERIFICATION.md)
- [Substantive attempt](turn_01.md)
- [Research log](RESEARCH_LOG.md)
- [Machine-readable status](STATUS.json)
- [Transcription and algebra controls](checks/check_normalization.py)

The nonzero-value circle condition is checked explicitly, rather than inferred from a translated zero-free example. A quasiconformal shear transfers Eremenko's forbidden horizontal lifts to the relevant logarithmic curves. The note uses the published parabolic surface as an external theorem and makes no new-resolution claim.

Run the controls with `python3 checks/check_normalization.py` from this directory. Passing them checks finite algebra and transcription; it is not a proof of the analytic existence theorem or independent peer review. This is a historical-resolution verification note; no new research paper or DOI is proposed.

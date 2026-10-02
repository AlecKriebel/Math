# Independent review request: source-verification hold

Problem11000228 / AMR-109-0228, Exceptional Strata. Proposed queue state **queued0/5**, with an unresolved source-verification issue. No author proof turn has been charged and no full resolution is proposed for certification at this stage.

Please review SOURCE_STATUS.md, SCOPE_COMPARISON.md and PRIOR_PROOF_AUDIT.md against the four hash-bound primary PDFs. In particular:

1. Original Problem21 is printed p.257/PDF p.264. Surrounding definitions are pp.250–251 and the lead-in is p.256. Decide whether the broad geometric wording permits the reported algebro-geometric invariant; preserve the unresolved flat-only refinement in Chen–Möller p.311 and Chen–Yu §3.5/Problem3.2
2. Check the nonsquare Q convention in Lanneau §1.1.1 and Chen–Möller §2.1; exclude the pole from div₀(q)/3 and keep the genus3/genus4 cases separate
3. Read the exact Theorems1.1/1.2,6.1/7.1 and dependency route through Lemma7.7 to B.5. Check whether any stated convention or subspace justifies the printed h⁰=2; if not, retain the verification issue and do not infer that a modern restatement repairs it
4. Review the difference between a faithfully credited published theorem and an independently verified proof. This packet asserts the former only. No theorem-disproof or allegation is intended

Replay:

    python verify_source_alignment.py > /tmp/source-checks.json
    cmp SOURCE_CHECKS.json /tmp/source-checks.json

The script is standard-library Python. It is only an arithmetic/scope checker. Validate the four source hashes using SOURCE_MANIFEST.json and all packet hashes using FINAL_FROZEN_MANIFEST.json. No source PDFs or private records are included in the packet, and no outside contact or external publication is part of this request.

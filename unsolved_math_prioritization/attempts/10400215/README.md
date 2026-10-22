# Shadow number and simplicial volume: audited partial results

Problem 10400215 / AMR-103-0215, selection rank 847, is **unsolved by this attempt, 5/5 approaches**. This package does not settle Dylan Thurston's Conjecture 12.10, assert a topological counterexample, establish historical novelty, or certify present global openness.

## Results and hypotheses

The accepted deductions use ordinary shadow number and the simplicial-volume normalization in Costantino--Thurston: `a G <= s <= C G^2`, where `a = v3/(2 v8)`. They give a JSJ hyperbolic-piece sum-of-squares bound, linear bounds for bounded-piece-volume families and fixed finite-parent filling families, a necessary unbounded-volume hyperbolic-piece condition for a divergent ratio sequence, and equivalence of proposed universal affine and homogeneous upper estimates. Neither proposed universal upper estimate is proved.

For an actual branched special shadow of a closed oriented manifold with `n >= 1`, compatible gleams, and **all** filling-region cusps measured in the simultaneous cusp metric of Ishikawa--Koda v1, the inclusive cutoff `L >= 2 pi sqrt(3n/2)` forces ordinary shadow number, branched shadow complexity, and stable-map complexity all to equal `n`. The separate exact rounding threshold is strict; equality at that exact threshold is not claimed. There is no universal existence assertion for such uniformly long-slope shadows and no claim of a new geometric volume estimate.

Read [the original proof](author/PROOFS.md) and [the independent mathematical audit](independent_audit/AUDIT.md). The independent AI audit accepts the author package unchanged. It is not human peer review or proof-assistant certification. Historical pending-review and not-yet-published language in the frozen original artifacts is retained verbatim and superseded only by the separate acceptance and this publication wrapper.

## Reproducibility and preservation

The two original ZIPs, external manifests, bootstraps, receipts, and the independent validator are immutable copies. The `author/` and `independent_audit/` directories reproduce every member byte of those ZIPs. No correction patch was needed.

`PUBLICATION_MANIFEST.json` pins all payload bytes other than itself and `VERIFY_PUBLICATION.py`; the verifier pins that manifest. The exact verifier hash must be authenticated externally, against the publication receipt, before execution. Use Python's `-I -S -B` restrictions, adding `-O` for the optimized replay. After authenticating the verifier's bytes, run:

    python -I -S -B VERIFY_PUBLICATION.py .
    python -I -S -B -O VERIFY_PUBLICATION.py .

Repeat from a relocated clean package. Verification checks the strict complete directory and file inventory before invoking any bundled code, authenticates both ZIP member sets and every external file, and invokes the original independent validator. That validator runs 68,324 independent finite algebra controls per acceptance; each acceptance also runs four author replays of 45,810 controls plus 40 rejected author-boundary probes. Its complete acceptance matrix covers normal and optimized execution, relocation, hostile import/startup environments, and 44 rejected audit-boundary probes. These finite checks supplement the written proofs and do not certify topology. The static boundary does not defend against concurrent hostile writers, compromised Python, or a malicious trusted verifier.

This package contains authored mathematics, audit, code, and public verification metadata only. It includes no copied source PDFs/text/images, dataset contents, private sources, personal data, or private coordination material. Public source references and exact version/inspection limits are retained in the proof and audit. Publication is to a draft PR only; no merge, release, DOI, or outreach is part of this packet.

# Source contract and independent attack freeze

Timestamp UTC: 2026-10-16 05:18:10. Completion estimate: 10% of this construction audit. Original effort remains 1/5; this is validation only.

Scope: PR 888, PID 30005079, head a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7, exactly the 21 files pinned in the external parent SOURCE_MANIFEST.json. Native canonical pair was read before candidate proof. Its pin is 5415 bytes / SHA256 6bbb2826e583f9ccbbb38411ce780e865c0b9564b74bf9f6eca5250f4b06e083, as authenticated by ROOT_NATIVE_RECEIPT.json. The eligible claimed-solved gate is assigned as 1/5; no other PR is under review.

Official primary source body read before candidate proof: Harold Blum's contribution, *Degenerations of unstable Fano varieties and Kahler-Ricci soliton*, in OWR 17/2022, pp. 888–889, DOI 10.4171/OWR/2022/17, official EMS PDF https://ems.press/content/serial-article-files/46955 (68 pages; PDF pages 28–29). Source body/extraction remains private.

Contract derived from that passage: start with a klt Fano variety. The first stage is its canonical real degeneration minimizing the H-functional; the weighted central fiber is K-semistable. A second, K-polystable stage may follow. The requested nontriviality means the first central variety differs from the original variety. A candidate must explicitly identify the minimizing valuation, prove uniqueness and finite generation, and identify Proj of its graded ring. The requested strengthened example also has a nondivisorial minimizing valuation. A nontrivial soliton vector field on an unchanged toric variety does not by itself meet this contract.

Independent construction-family attack plan (frozen before candidate PROOF.md or prior verdicts):

1. Determine the candidate ambient spaces and equations; verify smoothness, projectivity, anticanonical class and ampleness from actual geometry.
2. Verify flatness, generic-fiber identification, scheme-theoretic central fiber, normality, klt and Q-Gorenstein/polarization hypotheses needed for a special degeneration.
3. Determine whether a proposed product or twist truly changes the variety and whether the claimed first degeneration follows from the exact theorem, rather than from soliton existence alone.
4. Check filtration/associated-graded identification, signs, shifts, and central action enough to expose hidden construction gaps. Leave the main minimization and irrationality families to their separate audits.
5. Consult actual primary theorem bodies for every external input needed to certify the construction, recording theorem identifiers, assumptions and exact remaining gaps. Distinguish universal proofs from finite numerical checks.
6. Save substantive assessment and notify parent before reading any source/audits verdicts. No candidate/source edits; no external communication, Git mutation, publication or release actions.

No candidate proof or prior acceptance verdict has been read at this freeze.

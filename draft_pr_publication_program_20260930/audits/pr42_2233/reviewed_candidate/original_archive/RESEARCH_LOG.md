# Research log: Erdős Problem 653

Actual model: gpt-6-astra, xhigh reasoning. Research window: 30 September 2026, 05:05–07:05 UTC. Maximum five substantive attempts.

## 05:05–05:20 UTC: target, prior work and source recovery

Completion estimate: 2% toward the original asymptotic problem. No earlier project attempt or duplicate was found. The official tracker was blocked, but its indexed statement and a complete 1995 primary manuscript establish the exact distinct-point and pinned-count interpretation. The cited 1997 scan and full 0.7 construction were not recovered. Current search also found newer external upper-bound preprints and an earlier separate AI-assisted small-example report. They do not claim a full asymptotic resolution; no unreviewed claim was adopted as a theorem in our note.

## Attempt 1: generic hierarchical amplification

Completion estimate remains 2%. The deficit at a pin is exactly preserved under independent translations that introduce no cross-block distance coincidences. This gives a complete obstruction to amplifying fixed-size or sublinear-size seeds by generic hierarchical gluing: the final spectrum is only the union of the leaf spectra and has size at most the largest leaf size minus one, apart from the all-singleton case. The route stalls because a successful construction needs a controlled family of nongeneric cross-block coincidences; no such scalable family was established.

## Attempt 2: one-dimensional and circular supports with repairs

Completion estimate remains 2%. A line or circle supports at most two other points at any fixed positive distance from a supported pin. The resulting count interval gives a sharp ceiling of ceil(n/2) distinct counts. Allowing o(n) arbitrary exceptions still gives only (1/2+o(1))n values. This closes the proposed concentration-and-small-repair route, but says nothing comparable about unrestricted configurations on many supports.

## 05:31 UTC: unresolved package prepared for separate review

Completion estimate remains 2%; the target is unresolved. Two routes have precise proved obstructions, and further variations without a new mechanism would repeat those gaps. All 18,306 exact finite assertions pass. The mathematical note also reproduces a classical estimate from the primary source for orientation, without treating that reproduction as a discovery. Work is being frozen for independent adversarial review before any PR.

## 06:12 UTC: separate review passed

The original asymptotic target remains unresolved, with the completion estimate unchanged at 2%. Independent adversarial review passed all stated partial assertions and reproduced all 18,306 author controls byte for byte; 1,263 additional exact controls passed. The six supplied review files are preserved unchanged. Only the mathematical note’s review-status sentence was updated; the source qualifications and mathematical text are unchanged. The package is ready for one scoped unresolved draft PR.

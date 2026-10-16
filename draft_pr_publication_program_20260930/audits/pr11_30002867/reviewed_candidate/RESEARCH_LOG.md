# Research log

All times UTC on 30 September 2026. Model: gpt-6-astra at xhigh reasoning; no ultra run is claimed. The assigned maximum was two hours starting 03:28, with at most five substantive proof attempts. The isolated turn ledger records this effort's budget use; shared queue files are outside this contribution.

## 03:29–03:32 — Source and readiness checkpoint

The requested website was attempted first but was unavailable. Recovered and checked the full original contribution in the official OWR report. The source asks for the global affine d-generator condition. Read the pinned target record, the duplicate 30002868, repository policy and desk review. No prior substantive attempt was found in the checked project history. No upstream detailed OWR report was present in the pinned report corpus.

**Completion estimate toward a full characterization:** 10%. **Toward a novel, independently verified contribution:** 5%. No proof attempt had yet been recorded.

## 03:32–03:36 — Substantive attempt 1; complete candidate saved

Derived the local minimal-generator count from the first homology of the Koszul complex of the shifted multiplication tuple. Verified that the global-to-local gap is closed by Mohan Kumar's stable-range theorem. Located the later errata invalidating broader Fasel/Mandal 2016 claims and excluded those claims from the proof. Saved the complete theorem and proof in `CANDIDATE.md` at 03:36. Formula (1) computes μ(I), so the target CI criterion follows by setting this count equal to the ambient dimension.

**Outcome:** candidate. **Turns used:** 1/5. **Completion estimate toward a full characterization:** 90%. **Toward a novel, independently verified contribution:** 35%, with novelty and adversarial review still outstanding.

## 03:38 — Exact-check checkpoint

All 13 small exact rational examples passed, including nonreduced complete intersections, non-CI monomial ideals, multiple support components, and a Gorenstein non-CI of length five. The largest algebra has length 16. The script also checks commutativity, D1 D2=0, and acyclicity at a point outside the support. Sent the saved proof and output for independent review.

**Completion estimate toward a full characterization:** 90%. **Toward a novel, independently verified contribution:** 35%. Computational evidence does not replace the proof.

## 03:40 — Scope and literature checkpoint

Added the coefficient-field requirement for an executable exact algorithm, a finite method of finding the relevant spectral tuples, and an explicit affine-CI/non-strict-CI example. Checked recent homogeneous marked-basis literature and preserved the substantial-prior-art caution. The formula has not been shown to be a new theorem or a first resolution.

**Completion estimate toward a full characterization:** 90%. **Toward a novel, independently verified contribution:** 30%; the latter estimate is deliberately lower because much of the content is a classical corollary.

## 03:44 — Independent verification checkpoint

Independent review found no substantive gap in the proof or original-source scope. The final artifact hash is recorded in the review. The reviewer independently implemented and passed 20 exact tests, including both diagnostic examples. Algorithmic coefficient-field precision was incorporated before the final review; no mathematical repair was required.

**Completion estimate toward a mathematically checked characterization:** 100%. **Toward a novel research contribution:** 30%. Novelty and first-resolution priority remain unresolved. This distinction prevents a standard corollary from being presented as a new discovery without evidence.

**Final proof-attempt count:** 1/5. Subsequent work was source checking, independent verification, and presentation rather than additional proof search.

## 2026-09-30T22:27:39.081122-07:00 — independent mathematical/source repair checkpoint

Three independent families and root rerun pass the exact criterion. Recovered original 1978 theorem and proof directly, clarified Das version versus compilation date, affine-linear strict-CI invariance and precisely scoped errata. Original snapshots and prior-review hashes remain historical evidence. Full priority audit in progress; related published algorithmic routes may already settle the original question. PR11 workflow **40%**; no new paper or acceptance yet.

- 2026-10-01T05:37:27.574314+00:00: Extensive independent priority audits establish earlier sufficient matrix methods (Wiebe1969/Fitting + MohanKumar1978; separately reconstruction2005/localCI2019). Original exact D2 disclosure remains unlocated. Correct mathematical characterization retained as already_solved known-method reformulation; no paper or DOI. Global source/README/readiness repairs made, historical inputs preserved. Acceptance completion estimate: 75%, fresh complete adversary and main integration remain.

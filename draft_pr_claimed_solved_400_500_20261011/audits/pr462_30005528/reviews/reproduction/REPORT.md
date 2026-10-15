# Independent reproduction and adversarial verification

Reviewer: independent reproduction subagent. PR 462; problem 30005528; frozen head `3d5701d67e18745715d384c3db3fbee588b42a98`. Completed 2026-10-12 UTC. Original proof search: 0% (not undertaken).

The frozen proof's central exact reasoning survives this reconstruction. The normal finite verification output reproduces exactly. There is one verification robustness issue: optimization removes every author `assert` guard, and six deliberately invalid author variants then exit successfully. The historical audit controls detect this failure and themselves exit unsuccessfully; their recorded output therefore reproduces normally, but does not reproduce when optimization propagates into nested author subprocesses. This report does not accept a prior audit verdict, resolve priority, or decide publication disposition.

## Independence and scope

Before reading the proof or historical audit report, the reviewer recorded falsification hypotheses concerning all legal paths, invariance, rational minimizing orbits, attainment, cost normalization, periodic density, universal versus finite reasoning, optimization, and hash coverage. The proof/source gate were then inspected; the historical report was inspected after baseline executions. All executions used disposable copies, with a working directory outside the source tree. No frozen bytes, repository state, remote service, or outside individual's communications were changed. The source gate's external citations were read as claimed attribution boundaries; this reviewer did not independently retrieve primary PDFs or conduct a literature search. Source interpretation and priority remain separate review tasks.

## Exact reconstruction

For the stated ordered graph relation, endpoint matching forces every legal word from \(x=(z,t)\) to have successive symbols \(F^j(x)\). This is an induction over arbitrary legal words, not an assumption that only a chosen class matters. The map preserves \(t\), so its \(N\)-tile numerator has \(N+1\) terms, each equal to \(1+t\). Its average is exactly \((N+1)(1+t)/N\to1+t\). Every bottom-circle orbit exists, hence the minimum 1 is attained precisely at height zero.

The iterate is \(F^p(z,t)=(e^{2\pi i p(\sqrt2+t)}z,t)\). Since \(|z|=1\), return is equivalent to \(p(\sqrt2+t)\in\mathbb Z\). Repeating ordered tiles is equivalent to return of the starting symbol; equal numerical sizes alone are insufficient. At \(t=0\), a return would imply \(\sqrt2=m/p\). Reduction followed by the elementary parity descent \(m^2=2p^2\Rightarrow m,p\) both even excludes this for every positive integer \(p\), independently of any finite computation. Invertibility transfers an eventual return back to the starting point. These observations establish the exact universal periodic exclusion under the stated graph and source convention.

Periodic heights are \((\mathbb Q-\sqrt2)\cap[0,1]\). Rational density gives a periodic height in every relative interval and every circle point is periodic at that height, so product neighborhoods meet periodic starting points. If density of legal words is desired in their product topology, the map \(x\mapsto(F^j(x))_{j\ge0}\) is continuous and its inverse on its image is projection onto the first coordinate, so the starting-point density transfers. Neither endpoint must itself be periodic. Compactness, connectedness, continuous positive cost, and closedness of the continuous graph follow directly from the compact Hausdorff product and the explicit continuous inverse. The annulus change of coordinates is invertible because its radius is at least 1.

For a reduced rational angle \(r=p/q>\sqrt2\), \(p^2-2q^2\ge1\), and rationalization gives \(t=(p^2-2q^2)/(q^2(r+\sqrt2))\ge1/((2\sqrt2+1)Q^2)\) when \(q\le Q\) and \(t\le1\). Thus approaching periodic competitors require unbounded least periods. No central difficulty is transferred to an unsupported infinite computation. The proof concerns arbitrary ordered-pair graphs; it supplies no allowed-distance packing realization. Symmetric edges or identifying symbols solely by their costs would change the assumptions.

## Provenance and replay

All 12 frozen snapshot files match the source receipt's byte lengths and SHA-256 values, and the complete file inventory agrees. All six targets named by `FROZEN_INPUTS.json` and all four targets named by `AUDIT_MANIFEST.json` match. `FROZEN_INPUTS.json` does not self-attest and covers only release files. `AUDIT_MANIFEST.json` does not self-attest and does not attest `PUBLICATION_NOTES.md`; the 12-file receipt covers those files. The receipt is used as the supplied frozen anchor, not described as a self-authenticating signature. No remote head was refetched by this reviewer.

The normal author replay returns 0, and both stdout and regenerated JSON equal the frozen 1,525 bytes (SHA-256 `e50eb3df1afd7ffa389be91ca4376fb07a4c017be519aebca812965637c453d3`). The optimized unmodified author also returns 0 and emits those same bytes. The normal historical controls return 0 and reproduce all 1,971 bytes (SHA-256 `648b7bce4fe8c9d95f53b6f83b10ef6fff0f2b2d2bb607f07884a32ae54656fa`), including the actual 47,513 count. Their author coverage is 256 competitors, 23,955 smaller-period candidates, 1,280 prefix checks, and 5,022 reduced rational angles/gap checks.

Eight separate historical inventory, byte-length, same-length hash, and invalid-CLI probes reject, one per guard per mode. With both `-O` and `PYTHONOPTIMIZE=1`, the historical controls return 1 at `AssertionError: invalid_mutations_rejected`, with empty stdout. The nested environment propagation was explicit. All six invalid author variants reject normally and all six exit 0 optimized. In particular, omitting the initial symbol cost and corrupting the rationalization identity both emit the unchanged original passed JSON under optimization. Successful byte replay alone therefore does not establish that author guards executed.

## Fresh controls and required correction

`integer_pell_controls.py` is a new standalone implementation using normalized integer surds, square inequalities, modular return conditions, direct coefficient prefix sums, and Pell norm-one recurrence. It imports no author module and uses no fixed decimal bracket. Thirty Pell instances extend through denominator 32,733,777,552,734,744,709,300, checking exact norm, reduction, domain, rationalization, and gap identities. The actual check total is 51,532, including 12 real wrong-claim subprocess rejections: six in each mode. This count supplements the proof and is not an infinite irrationality, density, novelty, or packing certificate.

Both fresh runners reproduce their authored JSON byte for byte from outside the source tree in normal and optimized execution; both reject invalid CLI arguments in both modes. The new integer/Pell output is 3,541 bytes and is distinct from historical output. `runner_replays.json` records the actual checks.

One current-publication verification correction is required if verification is to be advertised as optimization robust: in a new revision, replace author `assert` verification with explicit condition/exception guards, or explicitly reject optimized execution at the advertised verification entry point. Then document and replay the resulting entry point in both modes, with optimization propagated to subprocesses, and require all six invalid variants to reject. Keep the frozen historical evidence unchanged and describe its normal-only replay accurately. This is a verification correction, not a discovered defect in the exact proof. No unresolved mathematical gap was found within this review's stated construction and convention.

Replay from this directory:

```sh
python3 -B reproduce.py --case ../..
python3 -B integer_pell_controls.py
PYTHONOPTIMIZE=1 python3 -B -O integer_pell_controls.py
```

`PUBLIC_FILES.json` positively lists only authored review artifacts. It does not self-attest. Full primary sources, rendered pages, external extracts, disposable invalid fixtures, caches, secrets, and environment inventories are excluded.

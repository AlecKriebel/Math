# Independent software adversary review

Completed at 2026-10-13T02:10:12.932789+00:00. Review goal: 100%. This is a bounded software preparation review; no mathematical claims or candidate scientific files were read or assessed.

Reviewed helper SHA-256: `e32d5a12d08f6c7331070e2a5e7368aec5c1a44f6e1e8d2bef2623df9afb8ebf`.
Reviewed supplied tests SHA-256: `6f03be5a658bf7cfeb1d5c73215d2a0bf4ce37a1b729bedfff8955722ee4f1af`.

The initial native GET gates and final six-request Engine(Native).gate() run matched PR411 OPEN draft, the pinned source head, branch, full QUEUE blob/SHA-256, and exact selected ID/code Status claimed_solved / Turns 2/5. The final native gate retained immediate tree and blob responses and validated their Git object identities. All native requests were GET. These are native read-only observations; no native write outcome was tested.

The current helper passed 21 offline tests: 10 supplied tests plus 11 independent adversarial checks. The independent checks cover atomic concurrent journal acquisition; Git tree order/hash against git hash-object; untouched root, selected, executable, symlink and submodule siblings; exact commit hashing and unsafe message/identity boundaries; drift after object creation; body sequencing after native-model package readbacks; approved reconcile digest and independently reconstructed root; case-variant private/canonical path rejection; raw non-UTF-8 failure custody; timeout partial custody; and the inherent body edit race.

| Finding | Evidence | Resolution / exact remaining gap |
| --- | --- | --- |
| Exclusive journal creation was non-atomic. Two contenders both succeeded and one journal was overwritten. | before_repair_test_output.txt and before_repair_journal_race_result.json, deterministic replacement rendezvous. | Repaired using a fsynced temp and atomic absent-target os.link. The current test forces both contenders to the link step and observes one success and one Stop. |
| PR-body edit after the last GET can be overwritten. | body_cas_limit_result.json, offline model. | Inherent API limitation: no body compare-and-swap is present. Final native readbacks cannot detect the overwritten prior edit. Parent reports this limitation documented outside this code-only review scope. |
| Ref/readback observations do not form an atomic snapshot. | Source review plus existing stale-read/unknown-outcome models. | Nonforced ref PATCH and repeated fresh gates reduce risk; no claim of an atomic lease or permanent completeness is justified. |
| Git commit message JSON may remove the final newline. | Supplied model and independent git hash-object serialization check. | Planned raw commit is hashed with exactly one newline. Native message text is compared as either exact or one-final-newline-removed and never rehashed as historical raw bytes. Native POST serialization itself remains unexercised. |

The strongest checked result is that this exact helper revision satisfies the scoped preservation, pinning, journal, sequencing and GET-only reconciliation checks in adversarial offline models, and its real native read-only source gate matches the live pinned state. No reproducible software defect remains from this review. The native apply path, actual prepared candidate bytes, science, and parent documentation are outside this review's exercised scope. Git object binding assumes the normal integrity of native GitHub responses and cryptographic hashes. Unknown outcomes stay unresolved unless read-only observations confirm the planned state; no reconciliation retry is authorized.

Reproduce the offline review with `PYTHONDONTWRITEBYTECODE=1 python3 software_adversary0/adversarial_tests.py` from the preparation directory. The tests redirect synthetic files and transport fixtures into this review's own paths. Original failing evidence is retained.

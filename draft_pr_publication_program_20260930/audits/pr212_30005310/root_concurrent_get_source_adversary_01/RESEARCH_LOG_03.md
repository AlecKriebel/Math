# Retry evidence disclosure correction

2026-10-17T22:47:24.914694+00:00: Source-review100%. Root identified an overclaim in report/coverage: after-both-POSTs retry retained the injected blob transport failure, so it stopped in the first lease; only between-POSTs retry directly reached permanent ledger FileExistsError. Both issued zero additional POSTs. Preserved original first seal/manifest/report/coverage as superseded historical bytes, corrected only documentation and binding addendum. Actual119 results/checker unchanged; no rerun or production change. No mandatory implementation issue.

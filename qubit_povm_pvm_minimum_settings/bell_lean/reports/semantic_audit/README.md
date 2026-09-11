# Evidence index

`summary.json` is the final pass summary. `all.json`, `all_fixtures.json`,
`circuit_catalogue.json`, and `rank_three_saddle_certificate.json` are the final
aggregate execution evidence. The final run log is
`../preflight/physical_interface_audit.log`.

The earlier per-suite JSON and logs record development-stage executions; some
have earlier checker hashes or fewer checks. They are retained unchanged as
history. They must not be mistaken for additional independent successes of the
final checker. The aggregate recomputed all suites at the final script revision.

None of these reports records a Lean compiler or kernel run.

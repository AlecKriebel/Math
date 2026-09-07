# Root report cross-review

Timestamp: 2026-09-07T04:01:38Z. Completion: 100%.

I cross-read the completed root `REFEREE_REPORT.md` against the certificate lane's saved scripts, JSON results, logs, and independent parser cross-review. No correction is required in C1 or the N2/N4 closure statements.

- The mutant is described exactly: one extra recognized U-coefficient field in spatial row `[6,1,0]`, preserving the correct A field. The generated coefficient changes from `8281/24300` to `1` without code changes.
- Both direct readers accept. The saved complete symbolic suite, manuscript audit, three scratch supplement build passes, and full PDF audit all return zero. The report correctly limits the no-warning claim to the selected final-log warnings and identifies the actual 19-page scratch supplement.
- The exact difference `16019*x**6*z/24300` is supported by two independently constructed mathematical/parser checks. The report correctly preserves the distinction between a malformed input that can generate a false displayed identity and the correct shipped certificate.
- The unchanged-table freshness rejection and published hash containment are stated accurately. The experiment includes regeneration; it does not bypass either the original table-freshness comparison or immutable-release integrity.
- The proposed repair is bounded and addresses the cause: explicit coefficient key/parameter selection by table and protection against the conflicting recognized field. It need not reject harmless metadata or alter a published coefficient. The requested regression includes the important regeneration path.
- N2 counts are exact: 14 reader/generator rejection controls, 26 current unpacked implementations, and 12 reader copies in current ZIPs. The latter are reader copies, not generators; the root wording is correct.
- N4 counts and scope are exact: all 218 rows checked in both versions, exactly 50 semantic-preserving expression changes, and five identical current table copies. No residual shipped notation error was found.

I did not independently re-audit J1 or the other lanes during this bounded cross-review. No broad suite rerun, source edit, or Git action was performed.

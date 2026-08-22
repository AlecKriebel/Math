# Full referee validation packet

This packet supports an independent post-submission review of

> Exact Diffusion Design for Maximally Collective Stable Turing Patterns in
> Binary-Complex Mass-Action Networks.

The requested task is stated neutrally in `REFEREE_PROMPT.md`.  The supplied
proof maps, certificates, programs, and recorded outputs are author-provided
materials, not a substitute for the referee's own reasoning.

## Recommended order

1. Read `REFEREE_PROMPT.md` without reading any prior review verdict.
2. Before executing code, verify the packet:

   ```bash
   sha256sum -c SHA256SUMS.txt
   ```

3. Read `paper/main.pdf` and `paper/supplement.pdf` completely.
4. Use `review_maps/` only as navigation aids.  Check every dependency against
   the paper, supplement, and source.
5. Inspect `repository/replay.sh`, `RUN_COMPLETE_AUDIT.sh`,
   `RUN_ALL_VERIFIERS.py`, and the verifier source before trusting output.
6. Run the complete campaign:

   ```bash
   bash RUN_COMPLETE_AUDIT.sh
   ```

   The script verifies the pristine packet and creates a disposable working
   copy under the system temporary directory.  It retains that working copy so
   that regenerated files and logs remain available for inspection.
7. Perform independent derivations, mutations, boundary checks, and
   counterexample searches beyond the author-supplied programs.
8. Produce the report specified in `REFEREE_PROMPT.md`, including every item
   that could not be checked.

## Important scope notes

- `repository/` is a byte-for-byte copy of the portable v1.0.7 repository.  It
  is the complete executable core and includes the manuscript source,
  supplement source, figures, data, proof notes, certificates, tests, and
  recorded baseline outputs.
- `minimal_verifier/` provides a shorter exact replay.  It shares source with
  the full repository and is not claimed to be an independently implemented
  verification system.
- The portable replay runs every load-bearing certificate aggregate.  The
  outer runner additionally executes all 38 verifier entrypoints literally,
  including redundant and finite-regression entrypoints.
- Numerical experiments are illustrations and regression checks.  They do not
  prove an all-dimensional statement.
- Running a supplied program successfully does not establish that it faithfully
  represents the mathematics.  Semantic source-code review is required.
- Do not use the project's internal historical-provenance replay for this
  review: that separate script requires five frozen historical archives not
  included here.  The portable replay has no such dependency.

See `TESTED_ENVIRONMENT.md` for prerequisites and `PROVENANCE.md` for the exact
immutable source version.

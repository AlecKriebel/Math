# Timing-comparison correction

The initial replay comparator recursively removed every key named `seconds`. That was too broad: it could hide nested nontiming changes and did not validate runtime values. This correction does not change mathematical scripts, report, audit, expected statistics, or the UNSOLVED boundary.

The revised comparator permits only the top-level `seconds` field in `exact_n5.json`, `exact_n7.json`, and `exact_n8.json` to vary. It requires the field to exist and hold an integer or float (not boolean), finite and nonnegative, in both actual and expected data. All remaining values are compared by canonical JSON serialization with nonfinite values prohibited; nested data and untimed case fields are untouched. This also distinguishes boolean and integer values.

Normal and optimized negative controls reject nested `seconds` mutations, invalid runtime types, null, booleans, negative/nonfinite runtimes, missing runtime, changed `seconds` in untimed cases, and boolean/integer substitutions. A valid top-level elapsed-time variation is accepted.

The full fourteen-case replay was rerun after the correction. During preparatory overlapping heavy runs, one replay process terminated at S8 with empty stderr before a completed result; no mathematical mismatch was reported. The final run is the completed run documented in `REPLAY_RESULTS.json` and the consolidated log. This execution interruption is not claimed as mathematical evidence. Heavy S8 replays should run sequentially to avoid resource contention.

The external revised receipt records the precise file delta relative to the original freeze receipt, whose SHA-256 was 8d0c998c2fccc100676f21529f04b6f97ea0db7498b8ccb0b4c7fcbd02b78355. No publication or QUEUE edit occurred.

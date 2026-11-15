# Read-only packet verification

Run `python3 verify_review.py` from this directory. It reads sealed source/primary/initial/check evidence, checks whole identities and exact membership, and prints its result. It makes no network requests, writes no files and executes no source programmes. Its PASS validates evidence closure; it is not a formal verification of mathematical prose.

`--inputs-only` omits owned final-manifest/seal checks and `--preseal` omits only the terminal seal check. Neither mode executes source programmes. The default is the completed, read-only mode.

For an intentional bounded reproduction, separately run `python3 -I -B native-check-scratch/check_bosonization.py` and/or `python3 -I -B sign-check/check_bosonization.py` to stdout. No source builds or larger campaign is required. Do not redirect output to a new file within this frozen packet. The child checker emits new execution timestamps; compare its mathematical result/count fields rather than expecting new timestamp bytes to match.

Original source snapshots, whole failed and redirect transport objects, and authenticated cached-ZIP provenance remain at the exact additive input paths. The earlier incomplete source folder is preserved as history, not rewritten. Administrative instruction snapshots record the instructions read at review time without requiring the global AGENTS file to remain immutable forever.

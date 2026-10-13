# Independent scoped audit replay

Read AUDIT_REPORT.md for the verdict and its limits. The original problem is unresolved. This packet is separate from the unchanged author freeze.

Before executing anything, inspect the Python sources and verify MANIFEST.json against the separately supplied trusted manifest hash. Run the strict byte/inventory checker first:

    python -I -B verify_bundle.py

Then run the independent mathematical checks, including optimization mode:

    python -I -B independent_checks.py
    python -I -O -B independent_checks.py

Their JSON must match INDEPENDENT_RESULTS.json. Python 3.10+, SymPy and mpmath are required. There are 62 exact and 26 numerical checks. The script uses no author imports, network or writes. Finite ranks stop at weight 9.

The following optional replay needs the separately retained, pinned author archive. It uses only isolated temporary copies and prints JSON:

    python -I -B replay_author.py /path/to/ROOTED_TREE_30001336_AUTHOR_SAFE_FREEZE.zip

This runs both normal and optimized author replays and the documented integrity/mathematical mutation controls. Its output must match REPLAY_AND_MUTATION_RESULTS.json. It rejects injected bytecode before mathematical execution and invokes Python in isolated, no-bytecode-writing mode. Never run code from a changed archive simply because an untrusted manifest says it matches.

For an optional full-corpus replay, supply the original corpora without placing them in this audit directory:

    python -I -B verify_corpora.py /path/to/catalog.json /path/to/problems.json /path/to/research_results.json

Its output must match CORPUS_VERIFICATION.json. Only public hashes, byte counts, inventory counts, and match results are emitted. Corpus contents and third-party source files are not distributed.

The manifest excludes only itself. Unexpected directories, symlinks, nonregular files and extra files fail verification. Both manifests require an independently retained trusted hash to resist coordinated replacement. The Python dependency installation is outside the packet's integrity boundary.

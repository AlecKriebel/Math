# Row 1890 / problem 30005760: frozen partial results

Status: UNRESOLVED. Five approaches completed; acceptance is partial only.

The exact target is the ungridded horizontal class D = Av(1324) intersect Grid([Av(132) | Av(231)]), split by position, allowing empty cells. Count permutations once, not cuts. It is not the standard 213-cell gridded domino ensemble.

Accepted: exact basis {1324,15342,25341,365241,465231}; monotonicity for k <= n (source-dependent injection theorem and exhaustive n <= 6 cases); equality for n >= k+2; original-definition data for n=0 through 11 (adjacent source lengths n=0 through 10 only), total 1,480,089 at length 11; insertion-only obstruction 2413; explicit failure family for the published map. The unbounded k > n range remains unresolved. Map failures do not refute the counting inequality. There is no novelty or global literature-status certification.

Run python3 verify_package.py, and python3 -O verify_package.py, for the fail-closed integrity and provenance gate. Run python3 replay.py for isolated full-module normal/-O regeneration, including both original counting generators and independent C++ minimum-insertion enumeration. Replay writes only an explicitly selected external output file and temporary directories; the frozen payload is unchanged. Python execution rejects socket audit events. The only non-Python executable is the locally compiled, hash-bound standalone enumeration source, reviewed to contain no network operations.

The original authored reports, audit receipt binding 23 reviewed files, evidence, complete scripts, source gate and public bibliographic fingerprints are preserved. Copied PDFs, source text, dataset contents, compiled binaries, temporary diagnostics and private coordination files are excluded. No publication, repository, or queue action is performed. External acceptance receipt binds this package manifest and fresh replay/mutation results.

# Distinct triangle areas in polygon triangulations

Problem 3900016 / AMR-038-0016. Audited partial results; exhausted 5/5. The full target remains unresolved. No novelty or best-known-bound claim is made.

## Mathematical result and scope

For strictly convex polygons (distinct extreme vertices), triangulated with the original vertices and noncrossing diagonals, the report proves the universal lower bound

    t(n) >= ceil((sqrt(16n - 23) - 3)/8).

It also proves a maximum-triangle cap recursion giving a logarithmic lower bound, the exact values t(3)=t(4)=1 and t(5)=t(6)=2, and primitive-normal area-unit, spectrum, and total-mass constraints for the explicitly bounded coplanar integer class in [0,m]^3. These lattice constraints do not determine the sharp extremal function. The exact general t(n), sharp t_L(n,m), and unavoidable triple equal-area repetition remain unresolved. Collinear listed boundary points and Steiner vertices are outside the accepted domain.

Start with [the report](author/REPORT.md), [independent audit](audit/authored/AUDIT.md), and [acceptance](ACCEPTANCE.md). [PUBLIC_SCOPE.json](PUBLIC_SCOPE.json) states the delivery and replay limitations. All eight author files and the complete accepted source-free audit packet retain their original bytes. Frozen pending-audit/publication fields are historical; [audit/ACCEPTANCE.json](audit/ACCEPTANCE.json) gives the subsequent audit verdict.

## Reproduce with an externally trusted bootstrap

Requires Python 3.10+ and its standard library, Linux-style POSIX permissions, and actual real/effective UID 1000. The mathematical routines use exact integers and fractions. The replay creates disposable read-only copies (directories 0555, files 0444), actually attempts denied writes, executes normal/-O/-OO checks, compares full mode-specific stdout and stderr bytes to their pinned expected outputs, and verifies all original evidence is unchanged. There is no output normalization. Each wrapper run executes 21 subprocesses: nine native mathematical/audit/control runs, three full physical-probe runs, and nine CLI branch tests.

The public trust anchor is the BOOTSTRAP.py SHA-256 recorded outside this directory in the draft PR description. Obtain that pin through a trusted channel, verify an external copy of BOOTSTRAP.py before executing it, and keep that external copy fixed when checking a possibly changed candidate directory. A candidate's freshly calculated hash is not an independent trust anchor.

    sha256sum /trusted/BOOTSTRAP.py
    python3 -I -S -B /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -O /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -OO /trusted/BOOTSTRAP.py /path/to/packet

The externally pinned bootstrap requires the delivered bootstrap bytes to equal its own bytes and authenticates the exact verifier and manifest before execution. The manifest binds every other delivered file, including this README, ACCEPTANCE.md, the complete replay receipt, mutation driver, and all inner acceptance records and manifests. Exact recursive inventory rejects extra/missing directories and files, symlinks, and nonregular files. Strict JSON validation rejects duplicate keys, nonfinite/overflowed numbers, Boolean/float integer substitutions, and altered schemas.

For publication trust-boundary tests, first authenticate the whole packet with the fixed external bootstrap as above, then execute the authenticated mutation driver using the same external bootstrap pin:

    python3 -I -S -B mutation_tests.py --root /path/to/packet --bootstrap-sha256 PIN_FROM_PR
    python3 -I -S -B -O mutation_tests.py --root /path/to/packet --bootstrap-sha256 PIN_FROM_PR
    python3 -I -S -B -OO mutation_tests.py --root /path/to/packet --bootstrap-sha256 PIN_FROM_PR

The driver tests semantic/type rejection, manifest re-pinning attacks, acceptance and outer-receipt tampering, substituted wrapper code, inventory/type violations, and hostile import files and environment variables. It compares complete baseline and relocated hostile-environment outputs. Native semantic mutations run independently of integrity failures and reject seven mathematical/guard faults in every optimization mode. All scripts use explicit runtime guards rather than assert statements.

## Evidence limits

[REPLAY_RESULTS.json](REPLAY_RESULTS.json) preserves the complete fresh source-free replay, including every stdout/stderr string, exact byte digest, exit code, physical write denial and CLI outcome. A successful fixed-bootstrap verification reproduces that entire receipt with exact recursive JSON types. The stored audit verification outputs are full expected bytes, rather than selected flags or counts.

Fresh source retrieval/inspection, PDF byte verification, corpus byte verification, archive reconstruction and baseline-patch replay are NOT_RUN. The source/PDF/corpus bodies are absent. Their public hashes, sizes, links and previous inspection history are historical metadata only. No mathematical correction patch was required. Finite tests support the proofs and do not prove the full extremal problem, exhaustive bibliographic novelty, or conventional human peer review.

Only authored mathematics, audit/code, acceptance and public verification metadata are included. No copied third-party source bodies, dataset contents, private sources, private personal data, or private coordination material or its identifying metadata are included.

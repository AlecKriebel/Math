# KOU-21.107: a countable group without expansive finite blocks

This source-free packet records a full negative resolution in ZFC, accepted by two independent authored mathematical audits. Start with [ACCEPTANCE.md](ACCEPTANCE.md), then the [frozen proof](author/public/REPORT.md), the [first audit](audit_1/INDEPENDENT_MATHEMATICAL_AUDIT.md), and the [second audit](audit_2/INDEPENDENT_AUDIT.md). Queue status is `claimed_solved`, with one substantive proof approach (`1/5`). This is an unrefereed AI-assisted proof package; priority, editor confirmation, human peer review, and formal verification are not claimed.

The counterexample is the countable Boolean group of finite subsets of the natural numbers with the standard free-ultrafilter Mathias topology. It has an explicit countably infinite dense partition. The point-finite maximum-support argument defeats every proposed sequence of disjoint finite blocks. The proof works for any ordinary free ultrafilter in ZFC, without additional set-theoretic assumptions.

## Contents and history

- `author/public/`: six frozen author proof, metadata, fixture, and checker files
- `author/external/`: six frozen manifest, pin, audit-instruction, harness, bootstrap, and result files
- `expansive_group_2616_frozen.tar.gz`: original source-free archive, 13,488 bytes, SHA-256 `1e9e605ee96cdceaca6d9e5ea3b007f0849d0383c8db5f7e4b0c84c35a68de5b`
- `audit_1/`: complete first mathematical audit
- `audit_2/`: six second-audit proof-review and reproducibility files
- `ACCEPTANCE.md`: current acceptance and scope, separate from historical submission flags
- `verify_publication.py`, `mutation_tests.py`, `PUBLICATION_MANIFEST.json`, `BOOTSTRAP.py`: new publication integrity and replay layer

Every frozen byte is retained. The initial report's pending-audit language and the audits' pre-publication flags describe their original stages. They are not current outstanding review objections.

## Authenticated replay

Python 3.10+ and its standard library suffice. Run as a genuine nonroot account. Obtain the expected SHA-256 of `BOOTSTRAP.py` from a separately trusted channel or authenticated commit, and verify that file before executing it. The bootstrap pins both the manifest and verifier; an adjacent untrusted hash alone is not an independent trust anchor.

From this directory:

    python3 -I -S -B BOOTSTRAP.py .
    python3 -I -S -B -O BOOTSTRAP.py .
    python3 -I -S -B -OO BOOTSTRAP.py .

For publication mutation, relocated read-only, and hostile-import controls, first authenticate `mutation_tests.py` using the pinned publication manifest, then substitute the independently authenticated bootstrap digest:

    python3 -I -S -B mutation_tests.py --root . --bootstrap-sha256 EXPECTED_DIGEST
    python3 -I -S -B -O mutation_tests.py --root . --bootstrap-sha256 EXPECTED_DIGEST
    python3 -I -S -B -OO mutation_tests.py --root . --bootstrap-sha256 EXPECTED_DIGEST

The wrapper validates an exact recursive file/directory inventory, manifest schemas, file sizes and SHA-256 digests, and the exact original archive members without extraction. It preserves accepted-evidence pins even if an attacker rewrites a manifest. It executes authenticated byte snapshots in disposable directories, verifies that actual writes are denied, replays the author and independent controls, checks exact-type output equality, and checks unchanged bytes afterward. Concurrent malicious filesystem or runtime control is outside this bounded verification claim.

Each wrapper invocation runs the author and independent checkers across their three internal modes. The publication control runner tests its own selected optimization mode; the three commands above cover normal, -O, and -OO. Successful output is structured JSON. The verifier does not modify repositories or retrieve sources.

Finite checks supplement the written infinite proof. They neither construct a free ultrafilter nor prove the infinite theorem computationally. Fresh source and corpus checks are `NOT_RUN` by default. Public source titles, URLs, hashes, sizes, and historical inspection metadata are retained; source PDFs/text, dataset contents, private sources, and private coordination material are absent. For the target locator, predecessor's additional Zelenyuk remark, standard-topology attribution, and bounded literature status, see ACCEPTANCE.md and the audits.

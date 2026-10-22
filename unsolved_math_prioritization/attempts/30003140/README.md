# Paramodularity of antisymmetric Borcherds products: audited partial results

Problem 30003140 / OWR-14605-002, queue rank 994. **UNSOLVED, 5/5 substantive approach families.** Both specified level-713 and level-893 characteristic-zero correspondences remain unproved. This source-free research packet preserves the frozen author work and the complete independent AI audit byte for byte. No correction patch is required for that frozen acceptance.

Start with [PUBLICATION_ACCEPTANCE.md](PUBLICATION_ACCEPTANCE.md), the complete [original/RESULT.md](original/RESULT.md), and [independent_audit/FULL_AUDIT.md](independent_audit/FULL_AUDIT.md). The 713 parameterizations give the same normalized form. The accepted surface-side arithmetic includes semistable conductors, four bad factors, twenty good factors, root signs, geometric endomorphisms, and mod-2 images.

The theorem boundary is important: nonordinary reduction at 3 blocks the named ordinary lifting theorems, while **BCGP Theorem 10.3.9 supplies abstract mod-2 residual modularity**. Specific Hecke-eigenform certification, automorphic Euler matching, and the required characteristic-zero comparison are still absent. The fixed-conductor uniqueness question is not refuted by the changed-conductor twist example.

## Layout and integrity

- `original/`: the nine original frozen public files.
- `independent_audit/`: seven frozen public audit files, including the full acceptance report and a separately implemented standard-library arithmetic checker.
- `VERIFY_PUBLICATION.py`: fail-closed publication inventory and replay wrapper.
- `TEST_MUTATIONS.py` and `MUTATION_RESULTS.json`: external-bootstrap, malformed-input, inventory, and repinning countercontrols.
- `PUBLICATION_MANIFEST.json`: exact non-self file inventory, byte counts, SHA-256 digests, and baseline file modes. Obtain its separate external digest from the draft PR's pin record.

The original manifest SHA-256 is `7162a7e1927ccaaf5454fde977da28f50d910ed695931e08431eb77d9a878991`.
The independent-audit manifest SHA-256 is `c9c827f589c5ad30678dcdc7abd1ef780a3379e93363a78b372afc7d2d72bd32`.
The wrapper SHA-256 is `5f55437806aed156d2fae295cecd41223876111d347cff5811815da8565da660`.

Never trust an unauthenticated wrapper merely because it says that its own packet passes. Obtain the wrapper and publication-manifest digests separately from the draft PR or its detached receipt; authenticate both before executing the wrapper. After setting PACKET to this directory and MANIFEST_PIN to the separately supplied digest, an external bootstrap is:

```sh
python -I -B -c 'import hashlib,pathlib,stat,sys; p=pathlib.Path(sys.argv[1]); w=p/"VERIFY_PUBLICATION.py"; b=w.read_bytes(); m=p/"PUBLICATION_MANIFEST.json"; ok=stat.S_ISREG(w.lstat().st_mode) and stat.S_ISREG(m.lstat().st_mode) and hashlib.sha256(b).hexdigest()==sys.argv[2] and hashlib.sha256(m.read_bytes()).hexdigest()==sys.argv[3]; sys.exit("external anchor mismatch") if not ok else None; sys.argv=[str(w),"--packet",str(p),"--expected-manifest",sys.argv[3]]; exec(compile(b,str(w),"exec"),{"__name__":"__main__","__file__":str(w)})' "$PACKET" 5f55437806aed156d2fae295cecd41223876111d347cff5811815da8565da660 "$MANIFEST_PIN"
```

Run the external bootstrap under normal, `-O`, and `-OO` Python for optimization-invariant wrapper checks. The wrapper itself replays both arithmetic implementations in all three modes. For a quick identity-only check append `--check-only` to the wrapper argument list in the bootstrap. For a packet deliberately relocated with files 0444 and directories 0555, add `--filesystem-profile readonly`; its bytes and external pins are unchanged.

Requirements: Python 3.10+; the author's checker additionally needs SymPy (1.14.0 was used). The independent checker and publication wrapper use the standard library. No source PDF, extract, dataset, network, credentials, or original workspace is needed. Source hash metadata records historical inspection; replay does not reauthenticate those outside documents. Normal replay also runs relocated read-only fixtures and verifies a denied write probe. Run as an ordinary unprivileged user.

All compatible entry points use Python isolated mode. The preserved author negative-control program imports its authenticated sibling `verify.py`, so that entry point uses sanitized PYTHON-prefixed environment variables, a temporary working directory and pinned local imports instead of `-I`. The frozen control suites launch their own all-mode children; those exact scripts and their imported files are authenticated first. This is a dependency-isolation precaution, not an operating-system sandbox or a network isolation claim.

The author JSON parser historically uses last-key-wins duplicate handling. The exact pinned original contains no duplicate keys or nonfinite values. The publication wrapper additionally rejects duplicate keys, nonfinite/nonintegral numeric syntax, malformed structural scalar types, symlinks, special files, unlisted files and even extra empty directories. Hash checks establish identity; the written mathematics and cited theorems are not proved by those hashes. No formal verification, human peer review, novelty, exhaustive literature coverage, publication priority, or global paramodularity resolution is claimed.

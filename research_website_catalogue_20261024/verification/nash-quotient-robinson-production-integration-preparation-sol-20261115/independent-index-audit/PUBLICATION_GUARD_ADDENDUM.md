# No-force publication guard: post-seal mechanism

The original `FINAL_SEAL.json` and its four payloads remain unchanged. This addendum records a materially new mechanism discovered after that seal; it does not install or authorize a hook or a push.

The locally installed Git 2.38.2 primary documentation establishes two relevant facts. `githooks.txt` lines223–250 specifies that pre-push receives the proposed local and remote refs/object IDs on stdin, and nonzero exit aborts pushing. `gitprotocol-pack.txt` lines525–547 and601–605 specifies that the client sends the old object ID in its update request and the server checks that the reference still has that old ID before updating it.

Deduction: a dedicated, root-reviewed pre-push guard can close the separate-lookup/remote-rewind gap identified in the original report without using any force option. The sole permitted stdin record must name the approved exact commit, `refs/heads/master`, and remote old object ID exactly BASE. The guard must also validate the expected remote name and destination, reject extra or missing records, and fail closed on malformed input. The normal server-side expected-old-ID check then rejects changes after the advertisement supplied to that guard.

Such a guard must be the only hook in a private, immutable-for-the-attempt hook directory, and its exact bytes must be bound by the root execution/publication receipt. The push must enable that guard, so `--no-verify` would be inappropriate for this variant. Other mutation commands can continue to use a disabled hooksPath. Automatic tags, mirror behavior, and submodule recursion must remain disabled.

This is a documentation-backed mechanism, not a tested implementation. No push, test repository, Git object/index/ref write, hook installation, or network contact was performed. The exact remaining gap is implementation verification and root approval of the controlled guard. If the prepared installer does not implement this guard, the original non-force lookup race remains an accurately recorded limitation.

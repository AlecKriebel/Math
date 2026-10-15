# Reproduce actual-state readback

Literal public path base:

`draft_pr_descending_audit_20261002/audits/pr371_30006025/clean_final_adversary/post_merge`

Use Python3, authenticated GitHub CLI and the local repository holding the immutable Git objects:

```sh
python3 /absolute/path/to/post_merge/check_actual_merge.py --repo /absolute/path/to/Math
```

Default receipts/raw API responses go into a new ignored private run directory. This preserves the public receipt, seal, manifest and both earlier immutable packets. The program uses only Git reads, GitHub API reads and own-folder output writes. Its expected actual merge/head/base/tree are fixed immutable constants. It compares the complete actual recursive tree to the reviewed tree, all47 individual remote bytes, the literal queue reconstruction,113 nested bindings, four frozen family packet scopes, own original and final_live seals/manifests, current source bytes/limitations, raw merged state/body and late main ancestry. A failed check writes a failure receipt and exits nonzero. No unchanged mathematical checker rerun is required.

Original28-file and final_live10-file packets remain separate immutable scopes. This post_merge/PUBLIC_MANIFEST.json lists only literal relative filenames under its own stated base and excludes itself. Source assets, raw API responses, private streams and any private copies are excluded. Passing an explicit public --receipt path would invalidate its seal/manifest; independent replay should use the default private output.

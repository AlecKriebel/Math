# Run the additive gate

The literal public path base is:

`draft_pr_descending_audit_20261002/audits/pr371_30006025/clean_final_adversary/final_live`

Run from any directory with Python3 and authenticated GitHub CLI, using a local repository containing the immutable Git objects:

```sh
python3 /absolute/path/to/final_live/check_live_gate.py \
  --repo /absolute/path/to/Math \
  --head 212d6c498026765966bbe01ebe3ea09a76bb215f \
  --base 41b15a086acb109f1707320dbe5db39778cdceca \
  --tree bd83cce0cde75f29b0cbc469e33f01e9230fd511 \
  --parent-head 137d5e30efe05bb5f68a5b0bcc4e37480c8a9493
```

Default output goes into an ignored private run folder, preserving the published receipt/manifest and every frozen file. Use explicit reviewed arguments: the program's defaults retain the first gate's original reviewed state and will fail after its base/head movement. The original published audit commit183640 is a separate immutable constant, not replaced by the live base argument. The program uses only Git reads, GitHub API reads and its own-folder output writes. Each assertion records its whole relevant output. A failed state is saved and exits nonzero. A new main/head/body or test-merge change invalidates the gate; it must be freshly routed and checked rather than accepted silently.

The local Git trees are compared exhaustively at105,000+ nested entries, and complete nonrecursive remote root entries bind the same child-tree identities. The remote recursive API can truncate at100,000 entries, so it is not used as a completeness oracle. All47 reviewed changed-file bytes are separately retrieved. Sources stay private: fresh source byte/statement metadata is checked independently of historical source claims. The program does not perform mathematics from an output oracle or certify all27 historical assets.

The original28-file public manifest and its bound files are untouched. This additive PUBLIC_MANIFEST.json is self-excluded and lists only explicit literal paths relative to final_live. Re-running with an explicit public receipt path would change that public receipt and invalidate its seal/manifest, so use the default private output for independent root verification.

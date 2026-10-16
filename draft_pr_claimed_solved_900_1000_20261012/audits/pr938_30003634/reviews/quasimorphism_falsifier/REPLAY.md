# Read-only authentication replay

Authenticate this code and the curated map with the externally reported SHA256 pins before using them. The map excludes itself and every private source/cache/render. It is a review payload, not a publication acceptance.

The supplied original inventory has SHA256 `b197cade40c4804b09fd3d9af3519e1a8258ef9f4d0a7df7635e59825aa60a6d`. The reusable helper has SHA256 `e50f6a6da390ef99238c464e024621c54fc1c9f65184f00732fd73d8c5442355`. All paths and pins below are external inputs; the helper uses explicit checks and prints JSON to stdout. It does not rewrite the inventory, copied originals or Git state.

```sh
python3 /Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr938_30003634/reviews/quasimorphism_falsifier/authenticate_original.py \
  --repo /Users/alec/Documents/Math \
  --copy /Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr938_30003634/original \
  --inventory /Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr938_30003634/ORIGINAL_SNAPSHOT.json \
  --inventory-sha256 b197cade40c4804b09fd3d9af3519e1a8258ef9f4d0a7df7635e59825aa60a6d \
  --head 2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b
```

DIAGNOSTIC_CONTROLS.json records four authentic controls and36 fail-closed negatives under normal, -O, -OO and actual inherited optimization2. Negative controls cover wrong pins, corrupted inventory, wrong head/count, missing/corrupted copies, root/ancestor symlinks and unknown options, without changing original inputs. These are reproducibility controls, not mathematical proofs or OS-sandbox claims.

The full checkable mathematical derivation is FULL_AUDIT.md. Nine primary PDFs are individually pinned in SOURCE_PINS.json, with version-specific inspection boundaries. No raw third-party files are curated. ROOT_CANDIDATE_REVIEW.json separately pins the root stronger candidate and explains native accounting and its inherited status-event tag.

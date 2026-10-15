# Final live evidence

LIVE_PUBLIC_MANIFEST.json adds this final directory to the immutable original and
prepared allowlists. Publish their explicit union only. The exact-live gate,
descriptor, original mathematical controls, proofs and all prior receipts remain
in the earlier manifests, without duplication or modification here.

The live gate used exactly the prepared command and input bundles described in
public/live_acceptance/README.md, with --require-exact-api-body --require-ready
and a fresh private OWN. It passed before the authorized merge. The full receipt,
stdout and stderr are retained; do not rerun the open-PR gate against the now
merged PR and misrepresent that new state as a failed historical certificate.

The deterministic full comparison uses these immutable private inputs:

* Own live receipt SHA b3ca064c86b99dd85ee386d9934e9b132c16f6a7a439a4cc015070abb4b252cc.
* Root live receipt SHA2063f852d91f9dfc9a53246ffe2c02d6552e430672a00560634a0c3f6237a7b7.
* Own private/live_acceptance/round2_live/private/final_gate/{pr_live,pr_final}.stdout.
* Root tmp/root_staged_gate_attempt2/live/private/final_gate/{pr_live,pr_final}.stdout.

Their raw hashes, lengths and exact two repository-size JSON leaf differences are
bound in root_live_comparison_receipt.json. Stage identical copies privately, then:

```sh
python3 public/live_final/compare_live_reproduction.py --own-receipt OWN_LIVE_RECEIPT --root-receipt ROOT_LIVE_RECEIPT --own-raw-dir OWN_RAW_DIR --root-raw-dir ROOT_RAW_DIR --output-dir OWN_OUTPUT
```

Its entire stdout/stderr and whole output JSON must match the stored comparison;
there are no runtime-field exceptions in that deterministic program. It proves
whole-receipt equality after removing only observation UTC and the two raw hashes
whose exact semantic differences were independently established. Raw source,
packet and API byte streams remain private. No existing sealed file is rewritten.

Storage cleanup is resource maintenance, not a mathematical control. It retains
all byte streams at their original paths through hard links, excludes every
failed-run directory and primary source, and records successful-output duplicates.
Its historical failed code and complete streams are included. A strict initial
live receipt comparison failure is also retained, followed by the explicit full
raw-field comparison rather than a silent relaxation.

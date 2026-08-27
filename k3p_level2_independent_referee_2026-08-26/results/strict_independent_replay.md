# Credential-deny follow-up replay

Date: 2026-08-26 (America/Los_Angeles)

This follow-up reran all six referee-authored independent scripts inside
`package_copy/review_runs/_runtime/independent_checks_strict/` after the report
red team identified that the formal regeneration profile allowed unrestricted
host reads.

The caller environment was created from empty with deterministic Python/locale
variables. The follow-up profile denied network and external writes and added
explicit read denials for common SSH, cloud, Git, package-manager, keychain,
cookie, and browser-profile credential locations. It also denied execution of
the macOS `security` and SSH clients. Its SHA-256 is
`39dbe755d63423558dc3416b8351927b6f26a8512754515e09cf7f874d8187d6`.

Control probes:

- pinned Python plus mpmath/networkx/numpy/sympy import: PASS;
- read of the existing `/Users/alec/.ssh` directory: denied;
- connection to `127.0.0.1:9`: denied with `EPERM`;
- writes: confined to `package_copy` (plus `/dev/null`).

Every replayed result was byte-identical to the original independent evidence:

| Script/result | SHA-256 |
|---|---|
| `check_three_leaf_and_domains.py` result | `26ebfacdd91bf97e5673758c600b8c8a4622cec4e1e0a93cef91d58513e5a29d` |
| `check_bridge_and_gluing.py` result | `86a2abf63d7a992a19d550438cb0c5dfef45c80d2e8fc8a80ffdb2f05f8f11f6` |
| `check_four_port_spots.py` result | `be9b87a9295fc4d00ea9d23cac8ba51e4605e609f430fa6e5e5337a099ce2eea` |
| `check_census_and_transports.py` result | `6142f542695325d96b718fc5a2ec373c1f04599e4f943ffaecf3a2f55de42db4` |
| `check_krawczyk_literal.py` result | `8e34365ecf992234a9e8c21f1efe3bb8a3f57b8624f469654f505284fcfe6598` |
| `check_probe_semantic_samples.py` result | `2b8e43da7f7e7269ba621f6e67f548303363df8cb8e7545bade3742196bedf2d` |

This overlay materially hardens the small follow-up checks, but it is not
claimed to enumerate every possible credential location. It does not alter the
disclosure that the already-running exact-once 44-command regeneration used the
earlier unrestricted-read profile.

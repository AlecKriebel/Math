# Independent audit packet: 30003279

Read AUDIT_REPORT.md for the mathematical audit, narrow validation findings and acceptance limits. ACCEPTANCE.json records the frozen and hardened pins. No source PDFs, extracts, screenshots or datasets are included.

The frozen author's packet was preserved. VALIDATION_HARDENING.patch is a separate proposed patch, with no mathematical changes. It targets the original public packet; the updated manifest is included in the patch. A fully checked hardened copy accompanies this audit.

Independent mathematical replay:

python -B independent_checks.py --claims PATH_TO_AUTHOR_PACKET/CLAIMS.json

Independent cross-mode and regression replay:

python -B replay_independent.py --original PATH_TO_ORIGINAL_PACKET --pin 1e69db6319607fb6cb9a207193701dbb2fc38e5fe3cd0c799df44a49f6963799 --hardened PATH_TO_HARDENED_PACKET --hardened-pin 025af598dc60fc050dc1f7c4f718bff01cdad761d842854014fd8078eac58f54

The harness performs normal, -O, -OO, relocated read-only, malformed-input and frozen-integrity tests. It deliberately reproduces documented permissive behavior in the original and requires rejection in the hardened version. All test mutations take place in temporary copies.

For the hardened author's portability suite, run its test_packet.py with the hardened manifest SHA-256 from ACCEPTANCE.json. Original and hardened expected run results are included separately.

These controls do not replace universal proofs, the published sieve theorem, or human peer review. The overall problem remains unsolved.

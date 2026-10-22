# Auxiliary audit controls

Use Python 3. No third-party packages or network access are needed.

From this audit directory:

    python3 verification/check_auxiliary.py /path/to/rank618-30003790

The optional argument must be the directory containing the original `public/` and `independent-audit/AUXILIARY_CANDIDATE.md`. It verifies the exact candidate digest and every original manifest entry. Omitting it runs the finite controls without input binding.

To reproduce the recorded output byte-for-byte:

    python3 verification/check_auxiliary.py /path/to/rank618-30003790 > /tmp/auxiliary-replay.json
    cmp verification/result.json /tmp/auxiliary-replay.json

The tests check exact finite order statistics, high-precision adaptive-guard arithmetic, conditional-noise calculations, atoms, and explicit negative controls. The asymptotic proof is reviewed in `../AUDIT.md`; these controls are not a theorem prover or proof of an unquantified literature claim.

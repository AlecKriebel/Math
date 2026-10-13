# Portable independent verification

The original fresh audit read an extracted copy of Johnston–Rumynin Table 5. The public verifier instead reads the identical 60 permutations and three rational coefficients per permutation from `a5_idempotents.json`. The JSON identifies the source. It contains mathematical coefficient data only.

All group construction, explicit isomorphism, finite-field module, character, projective, idempotent, and real-obstruction algorithms and assertions are unchanged. The local snapshot-manifest check was replaced by the SHA-256 check of the unchanged main proof.

The portable script ran successfully, and every mathematical field in its JSON output is exactly equal to the original independent audit output. Only the two local snapshot-bookkeeping fields were replaced by `proof_sha256`. The adaptation remains separate from the frozen original audit.

This implementation needs Python 3 and SymPy. Run `python independent_audit/independent_audit.py` from the problem directory. It reads only the published coefficient file and main proof, and writes its results beside the script.

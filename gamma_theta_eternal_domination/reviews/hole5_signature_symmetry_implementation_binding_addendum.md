# Postcommit implementation-binding addendum: hole-5 \(S_6\) signature breaker

**Verdict:** `ACCEPT_POSTCOMMIT_IMPLEMENTATION_BINDING`

**Claim boundary:** This review binds the committed implementation to the
previously accepted mathematical construction and independently retained
comparator stream. It makes **no** `hole5` SAT or UNSAT claim, and no SAT solver
was run in this audit.

## Bound revision and artifacts

The audited revision is commit
`10acf379329411d9d05267b3411d6703047e705e`. For each author artifact below,
the working-tree bytes were identical to the named Git object:

| Artifact | Git blob | SHA-256 |
|---|---|---|
| `src/synthesis_k3/hole5_signature_breaker.py` | `a793e0f4d119be44b142a98824ceaeafbe06037c` | `cc1dc4249dc20f78e8eff4de14ffdca632da1e9455a381000786faa28c950c77` |
| `math/lemmas/hole5_signature_symmetry.md` | `45cfb9e22774de4c2d1d491b33f52ea85944f1d6` | `8f8192774c3de65c2468115cc2d4aadd392fa7a1f73261c23fa49886d9c183e8` |
| `tests/test_hole5_signature_breaker.py` | `74806aade5e467b8466ce404be6204c3db797839` | `cd73ae2275d1d08363a1ed7db5990ad294952270e449d5cec8229312d738a892` |
| `results/logs/hole5-signature-breaker-validation.json` | `79dfdc73c37d7a73b85c1afa11c2fbd1916c21a5` | `dafe1cdfe66bac034e71faaa0ba3f157fc88b21a317cbd6cba5f62e598f6d442` |

The prior independent hostile probe, retained output, and review were likewise
bound to their Git objects before the author module was imported. Replaying
that probe produced stdout byte-for-byte identical to the retained log and
again returned `ACCEPT_SIGNATURE_BREAKER_REJECT_SHORTCUTS`.

## Independent implementation comparison

The binding probe reconstructed the 315-clause, 3,210-literal comparator stream
without calling the author transition core. The author stream was byte-for-byte
identical to that reconstruction and to the independently retained stream:

- byte length: `11,424`;
- SHA-256:
  `ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6`.

The full derived CNF was also byte-for-byte identical under both constructions:

- header and counts: `p cnf 6886 23968`, with `192,169` literals;
- byte length: `754,323`;
- SHA-256:
  `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104`.

The source CNF body is the exact prefix after the rewritten header, with size
`742,882` and SHA-256
`eb08963261b712b725601efe566a4431979b42b0564bccbca8337cffd88fc269`;
the exact independent comparator stream is the suffix.

## Pure audits

The committed author routines exhaustively checked all \(5\cdot 2^{12}=20,480\)
adjacent-comparator assignments with no mismatch. They also checked the five
adjacent-transposition generators
\((6\,7),(7\,8),(8\,9),(9\,10),(10\,11)\) for source-formula covariance.
The independently replayed audit agreed on all five generators. The source
clause multiset had 23,653 clauses and SHA-256
`201496666b255837ff7692ce13ef058f867a11ea7404d571429b7bf0589b1b78`.
The exhaustive source oracle checked all 3,645 bank rows.

The focused committed unit suite passed all 8 tests (0 failures, 0 errors) in
31.07 seconds wall time with bytecode writing disabled.

## Reproduction artifacts

- `reviews/hole5_signature_symmetry_implementation_binding_probe.py`,
  SHA-256
  `bc2bae7403fba9bc77bb18b0501a799cfcf52ae53a2e4bbc761e2ae4eb8b0e3f`;
- `reviews/hole5_signature_symmetry_implementation_binding_log.json`,
  SHA-256
  `615c46de94578b7e5d4f62a509b03993065e0976ccc316db53a34c3c86f13a73`.

Running the probe from the repository root regenerates the retained JSON log
deterministically. The probe performs no SAT solve.

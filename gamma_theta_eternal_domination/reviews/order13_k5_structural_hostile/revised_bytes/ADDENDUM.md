# Revised-byte addendum: structural note

## Verdict

**ACCEPT_EXACT_NOTATION_ONLY_REVISION**

The revised file is:

- `math/working/order13_k5_structural.md`
- 11,274 bytes
- SHA-256
  `34c29d4b14e0955bd1ea0968f138a991cdd2a595ff3dd26891b74c1218af0a11`

The formerly reviewed file was:

- 11,188 bytes
- SHA-256
  `1761c537ce293f1d7e36fd32786ffad0a67f2f7fe9dd4af6aceed346ccec6d37`

The new replay reverses the revision in memory and recovers the former bytes
at exactly that size and hash.  This proves byte-for-byte that the only
changes are the intended repair:

1. insert the formal definitions
   \[
   A=N_G(a)\cap V(Q),\qquad B=N_G(b)\cap V(Q);
   \]
2. replace the formally undefined \(C_i-N_Q(a)\) and \(C_i-N_Q(b)\) by
   \(C_i-A\) and \(C_i-B\);
3. write \(R=Q-(A\cup B)\); and
4. use the same formal attachment definitions in the later display.

No occurrence of \(N_Q(a)\) or \(N_Q(b)\) remains.  Because
\(a,b\notin V(Q)\), this is exactly the correction required by the original
hostile review.  It changes no hypothesis, inference, theorem boundary, or
enumeration proposal.  The former acceptance of the bounded structural
reduction therefore carries over without a mathematical re-review gap.

The four original hostile artifacts remain byte-for-byte unchanged:

| artifact | SHA-256 |
|---|---|
| `reviews/order13_k5_structural_hostile/REVIEW.md` | `b93e854975444313558327a6ae0cc96ad3e8693b34e87b1148d878df4008759b` |
| `reviews/order13_k5_structural_hostile/evidence.json` | `2250c3c269e8df2b77dc4b98abcdfe049b1c1d08a77fa1f781c22c06605761ee` |
| `reviews/order13_k5_structural_hostile/RESEARCH_LOG.md` | `dd1d5a211b6ab4aadf89834496e3ecb423b1dc94548d51043fbf626343df0fd8` |
| `reviews/order13_k5_structural_hostile/audit.py` | `125ed608ce6d624aeb758ad272b8dae1195290ce9ef5b59150a4023ea3ae283e` |

The original frozen replay now rejects the revised target with an exact
target-hash mismatch.  That is its required behavior, not a mathematical
rejection.  Use the addendum replay for the revised bytes:

```sh
python3 -B -W error \
  reviews/order13_k5_structural_hostile/revised_bytes/audit.py
```

Expected verdict:

```text
ACCEPT_EXACT_NOTATION_ONLY_REVISION
```

This acceptance retains the original claim boundary: the note is a
conditional structural reduction, not an order-13 exclusion.

# K3 Problem 3.45: accepted support-genus partials

Status: **unsolved, five of five approaches used**. Read `ACCEPTANCE.md`, the
unchanged `original/REPORT.md`, and `audit/public/AUDIT.md` for proofs, hypotheses,
imported sources and the exact gaps. The July 2026 connected-sum maximum theorem
is an imported preprint, not a solution to either part.

`original/` preserves the original freeze, including its optimization vulnerability.
`audit/candidate_public/` contains only the minimal 23+6 assertion correction and
re-pinned manifest. `audit/public/OPTIMIZATION_FIX.patch` is the actual patch.
The original 44 optimized false passes and both native verifiers' self-rehashed
true-to-1 acceptances remain disclosed. Neither native verifier is a strict JSON
schema parser. Use the separate externally anchored wrapper for identity.

## Reproduce the source-free publication check

Python 3.10 or newer, standard library, actual UID/EUID 1000. No sources or network.
First compare the SHA-256 of `BOOTSTRAP.py` with the hash recorded in the trusted
publication review/PR. Do not derive that trust solely from this directory.
Then run, replacing PACKET with this directory's absolute path:

```
python -I -S -B PACKET/BOOTSTRAP.py PACKET
python -I -S -B -O PACKET/BOOTSTRAP.py PACKET
python -I -S -B -OO PACKET/BOOTSTRAP.py PACKET
```

After authentication, run `mutation_tests.py --root PACKET --bootstrap-sha256 HASH`
with the same `-I -S -B` flags, separately in normal, -O, and -OO modes. All inputs
can be read-only. Temporary replay/mutation copies are created outside the packet.

The wrapper rejects malformed publication schemas, bool/int substitutions,
duplicate keys, NaN/Infinity/overflow numbers, and inventory/hash deviations before
executing accepted packet code. Arithmetic replay includes the 150-run original/
corrected control comparison and independent checks. The native true-to-1 behavior
is intentionally characterized, while an altered candidate is rejected by the
fixed external anchor. A pass verifies these finite diagnostics and artifact bytes;
it does not prove contact realization, imported theorems, novelty or the problem.
Main and independent arithmetic results are compared as exact-type JSON objects,
not as raw output bytes. The native 150-run receipt is compared after dropping
stdout_sha256, stderr_sha256 and last_error_line from each row; the last-error
string is replaced by its error class. All other row fields are retained and
compared with exact types. Therefore this is an outcome/runtime/read-only-probe
comparison, not a byte-identical native-receipt claim. The complete historical
receipt is preserved unchanged. Native control generation uses disposable writable
source copies; its executed control copies are then made permission-read-only.

Fresh publication-stage source bindings: **NOT_RUN**. Historical checks are retained
as metadata only. The exact queue update and publication receipt live in the draft
PR's verified change set and review metadata.

# Erdős cycle-length sets: five audited partial approaches

Target: **1919 / EP-84**, rank 1017. Disposition: **unsolved, 5/5 proof approaches used**.

Here f(n) counts the complete sets of simple-cycle lengths realized by n-vertex simple graphs. The upper assertion f(n)=o(2^n) is credited to prior work of Verstraete and Nenadov. The lower assertion f(n)/2^(n/2) → infinity and existence of an exponential-growth limit remain unresolved here.

The accepted results are restricted cactus/theta subexponential bounds, distance-set concentration, and explicit collisions that obstruct particular decoders. None resolves the unrestricted problem. See the complete [corrected report](accepted/corrected/packet/REPORT.md), [independent mathematical audit](accepted/audit/packet/AUDIT.md), and [acceptance record](accepted/audit/packet/ACCEPTANCE.json).

## Corrections and preserved evidence

The baseline construction uses m≥2. Its actual authored correction is preserved in `accepted/corrected/packet/CORRECTION.patch`. The independent audit then required exact integer validation for ledger fields; its actual patch is `accepted/audit/packet/LEDGER_VALIDATION.patch`.

The accepted 38-member source-free archive and its five archive/metadata deliverables are copied byte-for-byte. `historical_revision2/` is retained as historical evidence with the pre-ledger-correction validator; `corrected/` is the accepted slice. Both original private author seals remain untouched. No source documents, source extracts, dataset contents, or private coordination files are included. Published source titles, public URLs, hashes, byte counts, and inspection history are metadata.

This is an AI-assisted authored review, not formal verification or conventional human peer review. Finite diagnostics support the bounded checks, not the infinite assertions. Historical source inspection and corpus receipts do not establish fresh source checks during publication.

## Reproduce the source-free package

Use a trusted Python 3 interpreter and standard library. First compare `BOOTSTRAP.py` with the SHA-256 independently delivered in the PR description. A replacement package that merely hashes itself consistently is not a trust anchor. The bootstrap pins the manifest and verifier before executing package code.

Run as a nonroot user:

```sh
python3 -I -S -B BOOTSTRAP.py
python3 -I -S -B -O BOOTSTRAP.py
python3 -I -S -B -OO BOOTSTRAP.py
python3 -I -S -B TEST_MUTATIONS.py
python3 -I -S -B -O TEST_MUTATIONS.py
python3 -I -S -B -OO TEST_MUTATIONS.py
```

The replay authenticates the exact file/directory inventory, accepted allowlist, tar archive membership, payloads, manifests and scope. Its strict JSON parser rejects duplicate keys, NaN, Infinity and float overflow; integer/boolean fields are exact-typed. A fresh authenticated copy is frozen to 0444/0555 and every file/directory is subjected to an actual nonroot write attempt. This is permission-enforced read-only testing, not an immutable mount.

Full replay runs corrected finite controls; independent subset-DP checks of all 33,868 labeled graphs through order 6; the 102-run corrected hostile matrix; 42 old direct ledger acceptances, 42 corrected rejections and 84 fixed-bootstrap rejections; 24 historical parser rejection controls; and relocated read-only execution from hostile working-directory/Python environments. Publication mutation tests separately exercise semantic validators, per-file missing/changed controls, unsafe file types, forged claims, archives, untrusted code and imports. Inputs must remain unchanged.

`--integrity-only` authenticates bytes and scope without running mathematical diagnostics. Current source rehash, corpus rehash, exact-record join, fresh retrieval and fresh source inspection report `NOT_RUN`: those private inputs are deliberately absent. No network is used by the verifier. GitHub CI is reported separately, and zero CI runs is `NOT_RUN`.

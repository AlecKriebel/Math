# Function Theory 3.32: historical-resolution verification

- Numeric target: **2303032**; catalogue code **AMR-022-3032**; queue rank **573**.
- Recommended status: **already_solved** at published-theorem level; **1/5** substantive verification turns.
- No new mathematical result or novelty claim.

Aikawa's 1994 Corollary 6(i) explicitly addresses this problem, with a later
proof exposition in his 2019 Theorem 1.7. Let theta be the interior cone
half-angle and a=a_n(theta) its positive harmonic homogeneity exponent.
Every positive superharmonic function is in L^p for

    0 < p < min{ n/(n+a-2), 1/(a-1) }.

The geometric angle and barrier exponent must not be confused. For example,
in dimension two a=pi/(2 theta).

**Verification boundary:** PROOF.md reconstructs the sufficient-range proof
and independently checks cone endpoint counterexamples for a<=2. For a>2,
the literature describes the bound as sharp, but the corresponding optimality
construction has not been retrieved or independently reconstructed here.
The cone example alone does not establish that sharper bound. This is not a
complete independent reconstruction of all sharpness/endpoint claims.

Read [PROOF.md](PROOF.md), [SOURCE_GATE.md](SOURCE_GATE.md), and
[ATTEMPT_LOG.md](ATTEMPT_LOG.md) for the exact scope and source checks.

## Reproduction

Python 3 standard library only:

    python3 verify.py
    python3 verify_manifest.py

Optional source-byte verification, if the cited author PDFs were downloaded
separately into a directory:

    python3 verify.py --source-dir /path/to/downloads

The controls check algebra, parameter inequalities, elementary harmonic
identities, limiting/negative controls and recorded source hashes. They do
not prove the analytic estimates, certify eigenvalues in all dimensions,
resolve the a>2 sharpness verification gap, establish priority exhaustively,
or replace expert review. Source PDFs are not included in this package.

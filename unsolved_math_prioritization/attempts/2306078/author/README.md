# Function Theory 6.78: a classical spherical-area consequence

Target: 2306078 / AMR-022-6078, ranked-campaign rank 686.

## Result

For the class of holomorphic injective functions on the open unit disk with
`f(0)=0` and `f'(0)=1`, the minimum spherical area of the image is **one half
of the sphere**, and the unique extremal function is **f(z)=z**.

With area element `4 dx dy/(1+|w|^2)^2`, the value is `2 pi`. With area element
`dx dy/(1+|w|^2)^2`, the value is `pi/2`. The area convention must accompany
any numerical answer.

This is a consequence of Dufresnoy's 1941 area--derivative lemma, including
its equality case. It is **not a claim of a new theorem**. The governing
Hayman--Lingham source labels its 2018 update as having received no progress;
that historical report should not be mistaken for a verified current
open-problem status.

## Contents

- `PROOF.md`: complete authored specialization, a derivation from spherical
  isoperimetry, boundary exhaustion, and a separate uniqueness argument.
- `APPROACH_LOG.md`: the actual mathematical routes, their outcomes, and the
  early stopping reason.
- `exact_controls.py` and `EXACT_RESULTS.json`: portable exact algebraic
  checks. They do not replace the analytic proof or constitute formal
  verification.
- `SOURCE_VERIFICATION.json`: public source identities, byte hashes,
  inspection extent, repository observations, and limits.
- `READINESS_AND_OUTCOME.json`: claim scope and audit gate.
- `MANIFEST.json` and `verify_manifest.py`: byte-level replay controls.

Run `python exact_controls.py` and `python verify_manifest.py` from this
directory. Python 3 and SymPy are required for the algebraic controls.

Only authored mathematics/code and public verification metadata are present
here. Source PDF/text bytes, dataset contents, and private coordination
records are excluded. No remote writes were performed in this investigation.
A fresh independent audit is still required before publication.

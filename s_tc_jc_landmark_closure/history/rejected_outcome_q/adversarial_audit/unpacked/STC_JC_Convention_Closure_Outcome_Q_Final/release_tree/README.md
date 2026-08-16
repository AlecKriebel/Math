# Convention closure of the strongly tree-child level-2 JC theorem

This package proves **Outcome Q**.  It closes the gap between the frozen already-simple `sd0` theorem and the Englander/Brits root-suppression-plus-cleanup convention.

## Main result

For the binary LSA-valid cleanup class in which every cleanup rooting is tree-child and the cleaned topology has level at most two, cleanup has a canonical model-preserving quotient to the already-simple class.  Consequently the frozen JC classification applies to the full intended literature class.

## Reproduce

```bash
bash reproducibility/verify_quick.sh
bash reproducibility/verify_full.sh
bash reproducibility/verify_regenerate_all.sh
```

The scripts use only files inside this package.  The frozen baseline theorem is identified by exact PDF and commit hashes; the new scripts regenerate and audit the convention quotient.

## Important distinctions

- `sd0`: no cleanup after one root suppression.
- `clean`: root suppression followed by exhaustive newly-created parallel and degree-two cleanup.
- The final mixed graph is the quotient object.
- Rooting fibres differ; strong cleanup tree-childness is the stricter property.
- The exact JC quotient is proved only for the forced root-created zipper, not for arbitrary hidden 2-sub-blobs.

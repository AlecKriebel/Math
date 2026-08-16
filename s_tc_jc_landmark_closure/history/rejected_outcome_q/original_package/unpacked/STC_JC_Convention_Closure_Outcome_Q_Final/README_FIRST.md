# Outcome Q — convention-closed level-2 JC theorem

This is the authoritative convention-closure release.

* Release commit: `e6340199d4c761bf33f24f9f2fac6a636710ab62`
* Frozen sd0 baseline commit: `53feab32c41c9d803140baacbe89cadf25d08049`
* Outcome: Q — full theorem transferred through a canonical model-preserving cleanup quotient.

The broader Englander/Brits cleanup convention and the manuscript's already-simple `sd0` convention are not literally identical at the rooted-presentation level.  On the literature strongly tree-child level-2 class, every additional cleanup presentation is the forced root-created zipper proved in `THEOREM_Q_PROOF.md`.  Its complete open JC tensor image equals the cleaned edge image.  Thus the existing sd0 classification transfers exactly to the cleanup class.

Run from `release_tree/`:

```sh
bash reproducibility/verify_quick.sh
bash reproducibility/verify_full.sh
bash reproducibility/verify_regenerate_all.sh
```

The exact clean-clone transcripts are under `clean_clone_transcripts/`.

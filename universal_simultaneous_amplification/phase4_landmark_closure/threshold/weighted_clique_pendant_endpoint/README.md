# Weighted clique--pendant endpoint audit

This package extends the clique-with-pendants endpoint chain by arbitrary
positive pendant weights.  Its main analytic result is the uniform dB
obstruction in `WEIGHTED_CLIQUE_PENDANT_THEOREM.md`: if the number of
pendants diverges, no choice or scaling of their weights can give eventual
dB amplification at any fixed fitness.

Run the independent exact checks with

```sh
./replay.sh
```

from this directory.  Discovery searches are:

```sh
python search_endpoint.py --max-n 40
python search_affine.py --max-n 40
python two_class_search.py --max-n 12 --objective M
python two_class_search.py --max-n 12 --objective S
```

The searches use floating sparse solves and are evidence only.  No positive
claim in the theorem depends on them.

# Reproduce the unresolved checkpoint

Python 3.12, standard library only. From this directory:

```
python -B verify_manifest.py
python -B run_checks.py
python -B test_corruption_controls.py
python -B -O verify_manifest.py
python -B -O run_checks.py
python -B -O test_corruption_controls.py
```

run_checks.py executes every mathematical script normally and with optimization, in temporary directories, and compares complete generated output bytes with the frozen outputs. This covers the simplex examples, full 240-facet certificate, square-fan failed sweep, original negative controls, supplementary malformed inputs, independent reconstruction and exact realizations. It rejects assert-based guards. Scripts use no third-party dependencies.

The independent checker reconstructs all expected maximal flags from the original facets, verifies exact facet-set equality and multiplicity, and checks full face-union attachments. The failed sweep is accepted only as failure of that ordering, not as nonshellability. Exact square vertices, fan facets, functional and no-tie field are guarded explicitly. The four-dimensional realization is elementary and already shellable before subdivision.

Direct calls to research scripts regenerate files beside the scripts. Use run_checks.py for immutable replay. The -B switch avoids bytecode files that would change the exact manifest inventory. Control scripts mutate only temporary copies. Manifest verification is an integrity check against the supplied manifest, not authentication; coordinated replacement of data and manifest is outside its guarantee.

No original PDFs, source extracts or corpus contents are needed or distributed. Source claims rely on the documented bounded inspection, not a new exhaustive literature review.

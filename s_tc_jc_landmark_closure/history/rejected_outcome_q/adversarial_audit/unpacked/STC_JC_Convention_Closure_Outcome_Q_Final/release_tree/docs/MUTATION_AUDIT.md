# Mutation-sensitive audit

`review/run_mutation_suite.py` applies each mutation to a private copy of the primary or independent certificate and then invokes the reconciliation validator.  The release passes only when every mutation raises a mathematical inconsistency.

| Mutation | Expected failure principle |
|---|---|
| Fail to suppress one degree-two vertex | Primary and independent target/fibre counts disagree |
| Suppress the reticulation without transport | Regenerated zipper Fourier polynomial changes |
| Identify the wrong parallel pair | Independent canonical target count disagrees |
| Forget a retained arrowhead | Rooting type and strict-fibre status disagree |
| Merge distinct cleanup fibres | Labelled mixed-graph fibre profile disagrees |
| Misclassify `(1,1,2)` | Contradicts both complete LSA censuses |
| Test strong tree-childness on one rooting | Contradicts the complete rooting fibre of the strict witness |
| Collapse the Theta pair under cleanup | Contradicts labelled triangle-adjacency and graph codes |
| Reverse the parent-choice mixture | Sparse exact pullbacks disagree |
| Replace the strict JC section by a boundary value | Violates the open-domain equality certificate |

The JSON output records the exact exception produced by every test.

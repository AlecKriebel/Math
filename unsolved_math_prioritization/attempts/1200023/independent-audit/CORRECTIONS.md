# Corrections and optional clarifications

## Required corrections

None for the frozen artifact's conservative `unsolved`, five-approach, no-full-resolution classification.

## Optional, nonblocking clarifications

1. **Coordinate model domain.** Add one sentence to the verifier documentation that its models mean the connected component reached from the declared root. If `(h,m)` is read as all integer pairs, the parent map has separate nonnegative and negative m-components. The tested root component has m>=0 and is the intended regular tree. The independent spine construction establishes the model identification and correct distances without relying on an unstated all-integer connectedness assumption. The DL oracle likewise uses the root component of the horocyclic product. Current BFS behavior is correct.
2. **Infinite degree convention.** The reduction uses infinitely many distinct neighbors, as appropriate to the stated simple-graph convention. If discussing multigraphs, simplify loops and parallel edges first; infinite edge multiplicity alone does not force infinite outer vertex boundary. This does not affect the intended problem or any code.
3. **Certificate storage wording.** The JSON records aggregate checked results. Full arc-flow witnesses are reconstructed and checked by replay. Persisting those witnesses would allow another checker to validate a fixed certificate without rerunning an optimizer, but is not necessary for the packet's existing reproducibility claim.
4. **Audit completion metadata.** The frozen receipt and validation limits truthfully describe independent audit as pending at freeze time. Keep those original bytes unchanged. Cite this separately bound audit as the later event rather than editing historical freeze metadata.

No suggestion above should be interpreted as a general connected nonunimodular proof, an identified counterexample, or authorization to resume proof search beyond the completed five approach families.

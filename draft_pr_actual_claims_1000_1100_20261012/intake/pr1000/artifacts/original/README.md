# Hopf-tree motion groups: a credited single-edge obstruction

`PROOF_APPLICATION.md` gives a source-matched obstruction to the literal universal identification of the motion group with an automorphism subgroup of its forest RAAG. For the one-edge tree, the known motion group is Q8 and the RAAG is Z^2; no subgroup of GL_2(Z) is isomorphic to Q8. The natural Dahm representation instead has central kernel C2 and image C2 × C2.

This is an application and source correction using earlier results, not a novelty claim or a general computation for larger connected trees. The term “symmetric automorphism group” is not defined further in the original contribution; the no-subgroup argument avoids choosing a convention. An intended extension or revised motion-space statement remains separate.

- `SOURCE_AUDIT.md`: source locations, dependency limits, and a separate S^3 consistency warning
- `SOURCE_METADATA.json`: verified scholarly PDF hashes, sizes, URLs, and manuscript status
- `check_groups.py`: dependency-free, exact finite algebra checks
- `VALIDATION.json`: successful normal/-O/-OO runs as UID 1000 with read-only inputs, plus a failing negative control

Run the auxiliary checker with Python 3:

    python3 -B check_groups.py
    python3 -B -O check_groups.py
    python3 -B -OO check_groups.py

The checker does not prove the smooth topology theorem and does not search bounded matrices to infer a theorem about all of GL_2(R). Those distinctions are explicit in the proof note.

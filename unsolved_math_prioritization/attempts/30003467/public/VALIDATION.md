# Validation scope

All checks use explicit exceptions; no Python `assert` is relied upon. The same ordinary, optimized (`-O`), and doubly optimized (`-OO`) runs are required.

`check_math.py` verifies exact rational open-to-closed disk transfers on 45 instances and 1,125 point comparisons. Thirty-five instances include a point excluded on the original open boundary. Four invalid transfer inputs are rejected. It also checks all 81 labelings of four points, distinguishing the 78 non-monochromatic labelings from the 36 that use all three colors.

`test_packet.py` performs 21 adverse cases in each Python mode, for 63 rejected controls. These include changed proof bytes, missing/extra members, a symlink, malformed/duplicate/nonfinite JSON, a traversing member name, incorrect pin, boolean numerical fields, and explicitly wrong threshold, primal/dual scope, fixed-radius scope, novelty, answer direction, attempt count, or numerical receipt. For semantic controls the disposable manifest is honestly rebound, so rejection depends on the independent exact claim guard rather than merely an old hash. Missing external source inputs also fail closed.

Six positive runs comprise three ordinary relocated copies and three read-only relocated runs. Original and read-only packet hashes remain unchanged. The test receipt is in `TEST_RESULTS.json`.

The separately supplied full source replay checks eight complete external files and the selected problem-record digest. This verifies retained source bytes, not the truth of their contents or a current network retrieval. Without source arguments the verifier prints a conspicuous NOT_RUN state for that stage.

None of these computations verifies the geometric existence theorem, reconstructs its large point configuration, or substitutes for a mathematical reading of the published argument. The complete target deduction is in `PROOF.md`; the published theorem remains expressly credited and external.

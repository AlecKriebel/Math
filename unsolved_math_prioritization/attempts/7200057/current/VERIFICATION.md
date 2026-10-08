# Verification scope

The standard-library checker performs exact determinant and rational arithmetic. It verifies:

1. The three authored eight-point witnesses: all triples are noncollinear; the five inner points lie strictly inside the fixed outer triangle; complete side-count profiles; direct segment-pair crossings; independent convex-four-subset counts; and the explicit proof that both 22-crossing witnesses are nonoptimal.
2. Edge partition, hull count, weighted crossing identity and its cumulative form, including the last-coefficient parity.
3. Crossing and halving deletion identities on every witness deletion and on bounded auxiliary fixtures.
4. Generic single-triple mutations for orders 3 through 12 and every possible side count, with an explicit check that exactly the intended triple changes orientation.
5. Small-order algebra and the formal crossing-neutral profile exchange realized by the witnesses.
6. Seven malformed-input negative controls; bounded input size and exact coordinate types.

These are regression tests of the report's proofs, not an exhaustive enumeration of geometric order types and not a global extremum computation. The general conjecture remains unresolved.

All mathematical and integrity checks use explicit guards, not `assert`. The exact same payload is tested under normal Python, `-O`, and `-OO`. In required-read-only mode it requires effective UID 1000, verifies directory/file writability flags, and actually attempts creation in the packet and write-opening every existing file; every attempt must fail with PermissionError. An external before/after hash comparison checks that the packet bytes did not change.

The external harness additionally checks rejection of an output path inside the packet, rejection of the writable working tree under required-read-only mode, a successful external-output path, and rejection of a deliberately mutated report while preserving the original hash pins. That deliberately altered negative-control copy is not part of the deliverable. The freeze receipt and per-mode output records are retained separately for independent auditing.

A permission-read-only freeze is tamper-evident through its hashes. This is not a claim of kernel-enforced filesystem immutability against the owner changing permissions. The verifier never changes its own payload.

Independent audit correction: the checker now explicitly rejects the unqualified floor-slack inequality using n=4, E_0=3, L_0=5/2, U=0, and verifies the corrected real-bound rounding. The report restricts the simple form to an integral final lower bound.

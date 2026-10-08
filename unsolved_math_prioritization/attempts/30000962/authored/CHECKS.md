# Verification performed before author freeze

1. check_math.py: 4,043 exact checks; identical JSON under normal and optimized Python. Families cover Weyl groups A1/A2/B2/G2, nondegenerate forms, regular-orbit interpolation, the shifted Reynolds identity including a nonzero residue at a singular target, finite spectral projectors and sign-solution dimension, singular-strip negative controls, tensor-box recursions, central Gaussian ratios, and G2 PBW composition ratios/weight conservation.
2. verify_packet.py: closed flat inventory, regular-file requirement, external manifest hash, every member's byte count/SHA-256, strict manifest schema, and normal/optimized exact replay in a fresh temporary directory. Both outer interpreter modes passed.
3. test_integrity.py: 2 relocated baseline passes and 18 rejection runs across 9 mutation families, in normal/optimized outer modes. Missing/extra/nonregular/tampered files and manifest rebinding are rejected. Malformed/schema controls are also checked with their intentionally supplied test pins; these are distinct from the original-pin checks.
4. Original and frozen ZIP copies are checked against exact inventories and hashes in the separate freeze receipt. The external receipt pins the verifier before execution and the manifest before member verification.

All Python checks use exceptions, not removable assert statements. No large search or knot-polynomial database calculation is performed. Finite checks support the authored algebra and package integrity; they do not establish the universal mathematical statements, validate imported theorem proofs, certify scholarly-source bytes, or resolve the remaining G2 case.

The G2 calculation initially omitted the b-shift contribution to an exponent. The direct composition test rejected it. The final ratio q^(-5)[c+1]_(q^3)/[c]_(q^3), with witnesses 65/256 and 4161/16640 at q=2, is the corrected pre-freeze version.

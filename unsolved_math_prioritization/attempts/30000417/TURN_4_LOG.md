# Turn 4 checkpoint

Generalized the residue-class method to independently selected anchor labels, and proved an exact minimum-cost dynamic program for its sufficient deficit criterion. Derived the original conjectured bound under local-minimum or local-maximum conditions, without a shared label or bounded palette.

A 42-vertex instance at d=2 and the source list size6 is explicitly colorable, yet every optimized residue-class certificate has cost4 and hence fails the strict <4 condition. This is an exact limitation of the method; the full original remains unresolved after four turns. One turn remains. Completion estimate: broader conditional families and a certified proof-method obstruction, with the unrestricted global step still absent.

The verifier passed 6915 exact controls, including brute-force anchor optimization on small cases and independent Bellman verification of the full method-failure certificate. All code uses the Python standard library. Frozen earlier files remain unchanged.

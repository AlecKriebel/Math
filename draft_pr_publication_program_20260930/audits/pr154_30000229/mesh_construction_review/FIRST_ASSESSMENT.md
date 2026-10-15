# Independent first assessment

Recorded before opening any historical independent_review artifact. Original COUNTEREXAMPLE.md is treated as an unverified hypothesis.

The exact scoped hypothesis is: for the fixed compatibly labeled four-triangle square NVB master forest, there exists u in the best energy approximation class A^(1/2), f=-Delta u in H^-1, and a uniform lower bound on every conforming mesh with #T<=4^n and every unrestricted real g in P_0(T) of (c n-C)2^-n. It refutes the endpoint implication if all ingredients hold; it does not quantify over anisotropic or arbitrary triangulations.

Initial deductions: Q_j has x interval [2^-j,2^(1-j)] and height 2^-j. Consecutive squares meet only along x=2^-j and nonconsecutive squares are disjoint. The internal subcell hats vanish on every cell boundary, including the global lower boundary. Thus their zero extensions are H^1_0 and their gradients are orthogonal by disjoint interiors. The announced partial and infinite energy sums are consistent. The selected center-to-lower-left diagonals lie inside their cells except at the corner endpoint; none is a global boundary edge. Boundary touching and corner intersections have zero area/length respectively.

Unverified geometric claim: the initial labels boundary=0 and center spokes=1 must generate all dyadic square center-hat patterns. Need an explicit refinement cycle and a tree address for Q_j, not an assumed global uniform mesh. Need prove O(j+4^j) nonconforming work and O(4^n) simultaneous conforming work, with dependence of constants only on fixed T_0.

Unverified combinatorial claim: overlay must be the common partition of two leaves of the same fixed binary forest, be conforming, and preserve all old P_0 coefficients and P_1 pieces. Selected-edge segments must remain unions of distinct fine edges after completion and overlay; shared endpoints and physical-boundary corners must not introduce duplicate edges or singular point terms.

Plan: derive and implement rational-coordinate NVB with explicit labels; independently prove local refinement reachability/cost and tree-union overlay counting; run optimization-safe positive and meaningful negative controls, recording exactly which universal facts finite controls do and do not establish. Read actual primary definitions/theorems and only then compare historical review.

Completion estimate: 20% of the assigned geometric/construction audit. Status: no falsification found, no promotion yet.

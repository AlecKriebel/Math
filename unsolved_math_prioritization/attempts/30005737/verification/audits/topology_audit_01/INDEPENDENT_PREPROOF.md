# Independent mechanism, recorded before authored proof

UTC: 2026-10-16T07:02:15.364383+00:00
Completion estimate: 15% of independent audit.

I have read the complete native problem/background and authenticated the entire frozen source set, but have not read authored/PROOF.md, authored sources, or either old audit.

Potential mechanism: a post-Lie structure with semisimple target yields two Lie algebra homomorphisms g -> n whose difference is the identity. Integrating from simply connected G to simply connected semisimple N gives a left-right action with an open orbit and a nonsingular orbit differential at the identity. This alone does not establish that N is diffeomorphic to G. The first attempted falsification is to seek a proper open orbit; nonunimodular factorizations of SL2 can have a large open cell, so any proof must use perfectness/unimodularity essentially.

A possible bridge is a global determinant of the infinitesimal action frame against an invariant top form on N. If g and n are unimodular, the determinant should be invariant under the integrated action. It is then constant on the initial open orbit and holomorphic continuation makes it constant on connected N. If nonzero, every orbit is open; connectedness gives transitivity. This needs exact sign and volume checks by the analytic/algebra audit and is only a conditional input here.

Independent topology prediction conditional on global transitivity: the orbit map G -> N has discrete stabilizer H. A discrete stabilizer is closed as the preimage of a point. The homogeneous-space projection G -> G/H is a covering map. Since N is simply connected and G connected, H must be trivial. Thus G and N are diffeomorphic; no closedness of images of the two homomorphisms is needed.

For simply connected complex G with Levi algebra s and solvable radical r, one should construct G as the semidirect product of simply connected integrations S and R, using integration of the derivation action and uniqueness of the simply connected integration. This proves the required embedded/closed/global Levi factors instead of assuming them. R should be contractible (induction on complex codimension-one ideals); consequently G has the homotopy type of S. A simply connected complex semisimple group has a compact real form K and polar decomposition K x R^dim_C(s). Its compact manifold K has real dimension dim_C(s), is oriented by a left-invariant frame, and H_dim_C(s)(K;Z)=Z.

Apply the same compact-form fact to N. If N and G are diffeomorphic and r != 0, then dim_C(s)<dim_C(n). Hence H_dim_C(n)(G;Z)=0 but H_dim_C(n)(N;Z)=Z, contradiction. Finite products of simple factors still have top degree equal to the sum of dimensions. The zero Levi case gives a point compact form and no positive-degree homology; zero target is excluded directly.

Main topology risk candidates: global Levi semidirect-product claim can fail if simple connectedness is omitted; simply connected solvable complex groups are contractible but general complex solvable groups need not be; polar decomposition requires the complex semisimple group and actual compact form, and quotient covers/finite centers must be handled; homology dimension must use real dimension of K, not twice that dimension or rank.

Independent provisional assessment: the topology mechanism appears sound if the global transitivity lemma is established. No counterexample to that conditional implication is apparent. This record is fixed before reading the candidate proof.

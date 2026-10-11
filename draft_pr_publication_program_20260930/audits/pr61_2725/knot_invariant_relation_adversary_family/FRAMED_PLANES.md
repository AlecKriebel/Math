# Independent framed-plane qualification

The last step of Proposition 5.4 in the versioned [primary paper](https://arxiv.org/html/2409.00290v4) uses pi_2(U(2))=0 while referring to oriented Lagrangian planes.

The unframed oriented Lagrangian Grassmannian in C^2 is U(2)/SO(2). Its fibration gives the exact sequence

    0 = pi_2(U(2)) -> pi_2(U(2)/SO(2))
      -> pi_1(SO(2)) = Z -> pi_1(U(2)) = Z.

The last map is zero: real rotations have complex determinant 1 and lie in SU(2)=S^3. Hence pi_2(U(2)/SO(2))=Z. The facts about U(2) follow from SU(2)->U(2)->U(1). This is an exact countercontrol to confusing the two spaces.

U(2) parametrizes orthonormal oriented Lagrangian FRAMES. An annulus has a global tangent frame from product coordinates; a Lagrangian immersion maps it to a Lagrangian frame, and Gram-Schmidt gives a lift to U(2). A framed formal-immersion argument can therefore use pi_2(U(2))=0. A relative argument must also choose this lift compatibly with cylindrical collars and the normalized transverse path. Substituting U(2) without a lift would be invalid.

This is a source notation/framing qualification, not a counterexample to its existence theorem. The tangent framing provides a natural interpretation, but this family does not certify every relative h-principle step or reconstruct the approximation theorem. The candidate limits its claim to applying the prior theorem. The nine rational determinant-one controls are finite arithmetic only; the universal homotopy calculation is the exact sequence above.

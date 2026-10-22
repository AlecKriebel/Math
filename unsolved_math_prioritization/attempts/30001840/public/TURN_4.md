# Turn 4: recover arithmetic images from determinants and RM descent

Attempt: determine how much the arithmetic generic image adds to the geometric answer, rather than incorrectly treating all RM endomorphisms as Q-rational.

For a prime ell>=7, let T=T_ell(J_t), R=O tensor Z_ell, and E be the Weil pairing after a choice of compatible roots of unity. Define the two concrete groups

G_ell={g in GL_R(T): det_R(g) belongs to the diagonally embedded Z_ell^*},

N_ell={g in GSp_Z_ell(T,E): g R g^{-1}=R}.

The centralizer of R in GSp(T,E) is exactly G_ell. Indeed write E(v,w)=Tr_{R/Z_ell}(beta det(v,w)) as in Turn 3. An R-linear g has E(gv,gw)=Tr(beta det_R(g) det(v,w)); nondegeneracy of the trace pairing shows that this equals m E(v,w) for a scalar m precisely when det_R(g)=m. Thus its symplectic multiplier is its R-determinant.

The O-action is defined over K and Galois conjugation on it is the nontrivial automorphism of K/Q (Darmon--Mestre, Proposition 2.1). Hence the generic arithmetic image over K(t) lies in G_ell, and the image over Q(t) lies in N_ell. The latter normalizer has centralizer G_ell as the kernel of its action on R and quotient of order at most two, since Aut_{Z_ell}(R) has order two.

Over K(t), the determinant is the cyclotomic character chi_ell. Its image is all Z_ell^*. To see this, K ramifies at 5, whereas every subextension of Q(mu_{ell^infinity}) is unramified at 5 for ell !=5. Their intersection is therefore Q. Restricting chi_ell to G_K is surjective, and the constants quotient of G_{K(t)} surjects onto G_K. The geometric image already equals SL_2(R) by Turn 3. A subgroup containing the determinant kernel and surjecting onto the determinant quotient is the whole group. Consequently

Im(G_{K(t)} on T)=G_ell.

The image over Q(t) contains that group and an element conjugating w to w'. Thus its normalizer quotient has order two, and

Im(G_{Q(t)} on T)=N_ell.

These equalities are basis-independent statements relative to the specified RM action and principal polarization, valid for all ell>=7. In the split case G_ell is the set of pairs (A,B) in GL_2(Z_ell)^2 having the same determinant. In the inert case it is GL_2(O_{K,ell}) with determinant in Z_ell^*. Passing to Q permits the nontrivial semilinear component. The ambient unrestricted GL_4 or GSp_4 is not the expected RM image.

Outcome: exact generic arithmetic local Tate images away from 2,3,5, reconstructed from the prior residual theorem plus the preceding lifting proof. This says nothing yet about the full product over primes; a full local projection at every good prime would not on its own rule out adelic entanglement. It also does not assert these equalities for each rational fiber.

# Prospective integral-lattice bridge

This note is **not additional accepted Jacobian-image coverage**. The frozen-scope verdict remains the one in `AUDIT.md`. The elementary lemma below is proved; applying it to the whole compatible integral monodromy system and then importing the complete Hecke congruence theorem is a separate argument that the frozen packet did not supply.

## Elementary local lemma

Let R be a discrete valuation ring, and let M_1,M_2 in SL_2(R) be unipotent matrices whose differences N_i=M_i-I have square zero. Suppose c=tr(N_1 N_2) is a unit. Then an R-basis makes

M_1=[[1,1],[0,1]],  M_2=[[1,0],[c,1]].

Proof. Neither N_i is zero modulo the maximal ideal, because otherwise c would not be a unit. The rank-one square-zero matrix N_1 is primitive. More explicitly, its fraction-field kernel meets R squared in a primitive rank-one direct summand R e_1; the image of N_1 lies in this summand. Choose a complementary e_2. Then N_1 e_2=a e_1, and primitivity makes a a unit, so rescale e_2 to obtain N_1=E_12. Write N_2=[[b,d],[c,-b]]. The lower-left coefficient is c=tr(E_12 N_2), and N_2 squared zero implies b squared+cd=0. Conjugation by [[1,-b/c],[0,1]] commutes with E_12 and changes N_2 to [[0,0],[c,0]]. All divisions used here are by units; no division by two is needed. This proves the lemma.

## Why this could apply

If the compatible integral branch transformations for this Jacobian have the indicated unipotent form and the common product trace minus w, then

tr((M_1-I)(M_2-I))=tr(M_1 M_2)-2=-(2+w).

For w squared+w-1=0, the element 2+w has norm one and is a unit even at primes two, three, and five. Thus the lemma suggests a direct route to the missing lattice identification. To promote this to an image theorem, explicitly establish the branch generators on the actual integral local systems, their product relation and normalization, comparison with the geometric etale image, and compatibility of the coefficient action at all relevant primes. A rational representation or finitely many residual conjugacies alone should not be substituted for those statements.

## The displayed matrix group's Hecke connection

There is also an exact algebraic identity for the displayed abstract group. Put lambda=w+1, so lambda is a unit and lambda squared=2+w. Conjugating U=[[1,1],[0,1]] and V=[[1,0],[-lambda squared,1]] by diag(lambda,1) yields T=[[1,lambda],[0,1]] and S T S inverse, where S=[[0,1],[-1,0]]. These generate the homogeneous Hecke group H_5: put R_0=T S. With this sign convention R_0 to the fifth power is the identity and S squared is minus the identity. Moreover T(S T S inverse)=-R_0 squared. Its fifth power supplies minus the identity, hence R_0 squared, then R_0=(R_0 squared) cubed, then S. Thus both generating sets give the same group.

Lang–Lang's arXiv v3, [1401.0775](https://arxiv.org/abs/1401.0775), gives the integral congruence indices of this explicit H_5 and their coprime multiplicativity. This provides a concrete future route rather than a reason to label the frozen packet's bad-prime gaps globally open. It does not itself classify the arithmetic images of rational fibers.

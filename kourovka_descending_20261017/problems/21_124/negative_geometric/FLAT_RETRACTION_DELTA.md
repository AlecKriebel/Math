# Two natural rank-two flats are virtual retracts

UTC: 2026-10-24T22:34:00.643471+00:00. Supporting partial deduction from ALL_K_RETRACTION_DELTA.md; no novelty or full-solution claim. This is a separate delta so the earlier review inputs remain frozen.

For k≥2, the uniform affine representation also proves that each of the free abelian subgroups <a,t> and <w,t>, w=aba^-1b^-1, is a virtual retract of G_k.

Both subgroups really are Z²: t commutes with a and w, a,w are nontrivial infinite-order free-fiber elements, and t has nonzero free-by-cyclic height. This argument does not assume injectivity of the affine representation globally.

For <a,t>, retain the finite-index subgroup L whose affine linear part is in<P>. Define P-invariant rational functionals

 ell_a(v) = sum_(i=0)^(k-1) v_(2,i)/k,
 ell_t(v) = (sum_(i=0)^(k-1) v_(0,i) + sum_(i=0)^(k-1) v_(2,i))/k².

On the affine translation vectors A,T these have values

 ell_a(A)=1, ell_a(T)=0, ell_t(A)=0, ell_t(T)=1.

Thus chi=(ell_a,ell_t) is a homomorphism L→(1/k²)Z² taking a,t to the standard basis. Restrict to chi^-1(Z²), a finite-index subgroup containing a,t. The map g↦a^{chi_a(g)}t^{chi_t(g)} retracts this subgroup onto<a,t>.

For <w,t>, the affine linear parts of w and t are both identity, while their translation vectors are D=(C-I)T and T. These are linearly independent rational vectors: D≠0, sum(D)=0, and sum(T)=k²>0. Choose rational linear forms f,g dual to D,T on their span and extend them rationally to V. On the finite-index subgroup K killing all affine linear parts, (f,g) of the translation vector is an additive map into (1/M)Z² for some finite positive M, taking w,t to the standard basis. Restricting to the inverse image of Z² gives the desired retraction onto<w,t>.

These results rule out cyclic or abelian virtual-retract obstructions based solely on these two natural flats. They do not prove that the full fixed subgroup F(a,bab^-1)×<t> is a virtual retract, and do not address flats corresponding to arbitrary words in that nonabelian fixed free group. The affine image of this fixed free group has cyclic finite linear part<P> and abelian translation kernel, so it is metabelian and kills its second derived subgroup. Its first derived subgroup need not be killed: in fact the commutator of a and bab^-1 is detected by this representation. Confusing commuting finite linear parts with commuting affine isometries would be an error. The second-derived kernel is an exact surviving limitation of this construction, not evidence of a group obstruction.

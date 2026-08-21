# Hostile review checklist: squarefree-interior fixed-root/contact
\(\delta=2,\{1,1\}\) exclusion

1. Recompute the generic gcd \(pL\) and all three deeper-incidence
   boundary gcds \(pLM,pL^2,pqL\).  Keep the \(\delta\ge3\)
   mutations separate from the theorem.
2. Verify that \(w=0,w^2=1\) leave the squarefree-interior orbit and
   that \(w^2=3\) is exactly the routed
   \(\kappa=16/3,\{2,0\}\) row.
3. Rebuild the complete \(E_7\) kernel and the signed rank-six minor.
   Check the definitions and signs of both internal factors \(D,H\).
4. Reconstruct the lifted generic contact matrix and its selected
   maximal minor.  Do not infer full rank from a polynomial gcd.
5. Recompute the \(D=0\) tangent basis from scratch.  Verify every
   factor of its contact determinant and isolate precisely
   \(u=-1,3/5,J(u)=0\).
6. Recompute the \(H=0\) tangent basis from scratch.  Verify the
   rank-four minor, the complete kernel, and the numerator
   \[
   V(u)=515u^4-548u^3+162u^2-324u+243
   \]
   of its Veronese obstruction.
7. Check primitive contents and irreducibility of both \(V(u)\) and
   \(V(w^2)\).  Do not choose a numerical conjugate.
8. Verify every denominator and exact-open factor is coprime to
   \(V\), especially \(N_X,F_0,G_0,J,11u-9\).
9. Reconstruct the denominator-cleared lift
   \(c_1=(u+1)N_X,c_2=2wN_Y\), including the two \(r^2\)
   coefficients of \(H_2\).  Check it satisfies the contact equation
   modulo \(V(w^2)\).
10. Re-expand \([r^2p^3]E_5\), including its sign and every factor.
    Check that \(C(u)\) is primitive and independently recompute
    \[
    \operatorname{Res}(V,C)
    =2^{81}3^{20}5^2\cdot1291.
    \]
11. Audit the top-only claim using the three weight partitions
    \((3,2,0),(3,1,1),(2,2,1)\).  In particular, verify the two mixed
    determinant support cancellations; raw \(r\)-degree counting
    alone is not sufficient for the \(r\)-linear \(H_2\) jets.
12. Recompute fresh bases over
    \(\mathbb Q[w]/(w^2+1)\),
    \(\mathbb Q[w]/(5w^2-3)\),
    \(\mathbb Q[w]/(11w^2-9)\), and
    \(\mathbb Q[w]/(J(w^2))\).  Verify irreducibility, contact rank,
    and the two non-Veronese kernels.
13. Replay the uniform constant \(E_6\) determinant on every chart and
    audit the all-binary field/descent exit without invoking the full
    plane Jacobian Conjecture.
14. Keep the theorem scoped to the squarefree-interior
    one-fixed-root/one-contact leaf.  The two-contact and doubled
    nonbranch leaves remain separate.

This is a mathematical audit checklist.  Exact CAS output is not peer
review.

# Independently checkable scope certificates

These are authored audit derivations, not copied source text. They certify the logical distinctions used in REPORT.md. Finite matrix checks in `verify_scope.py` supplement the arguments below.

## C1. The candidate's ambient dependence is a full-witness impossibility

Put A=C({00,01,10,11}), let p and q be the coordinate projections, and give 00 and 11 mass 1/2 each. Let B=C*(p), C=C*(q). A witness w on F(A) must satisfy w(p_i)=w(q_j)=w(p_i q_j)=w(q_j p_i)=1/2 for every i≠j. In the positive-functional GNS space this yields

    ||p_i Ω-q_j Ω||²=0.

For any i,k choose j different from both. This identifies p_iΩ and p_kΩ; it also identifies every q_jΩ with the same vector v. Every generator R=p_i or q_i obeys RΩ=v and Rv=R²Ω=v. Thus every nonempty monomial in the generators sends Ω to v and has expectation 1/2. These monomials span F(A), since p,q,pq and 1 span each copy of A. Consequently every possible witness is precisely the average of the two all-copy characters at 00 and 11. The characters are distinct invariant states, so no witness is extreme.

Under the diagonal inclusion into M4, the vector v'=(e00+e11)/sqrt(2) induces a pure state with the required diagonal restriction. The folding quotient F(M4)→M4 pulls this pure state back to a pure state, because purity pulls back through a surjective *-homomorphism. Folding is permutation-invariant. For every B*C word it multiplies the original B,C matrices in the original order, so it matches the full joint state. Hence independence changes from false to true under this state-preserving inclusion. Restriction of that upstairs extreme state is the downstairs mixture; this is not an example of a downstairs extreme state failing to extend.

## C2. Literal algebraic non-lifting is a separate claim

Let R=C[x], x*=x, and S=C[x,x^-1] with the inverse also selfadjoint. The all-copy evaluation at x=0 is a character chi of F(R), hence pure and invariant. If a positive state eta of F(S) restricted to chi, take X and Y to be x and x^-1 in its first copy. Then eta(X²)=0 and XY=1. Cauchy–Schwarz gives

    |eta(YX)|² ≤ eta(Y²) eta(X²)=0,

contradicting eta(YX)=1. Thus no positive extension exists. Both R and S admit states; evaluation at 1 makes a separate state-preserving inclusion of probability spaces. It does not turn chi into that common marginal. This matters: C2 answers the source's unrestricted restriction-map question, not a non-lifting question for a specified full marginal that already extends to S.

## C3. In the C* category extreme invariant states do lift

Let D⊂E be an equivariant unital C* inclusion for the finite-permutation group Γ=∪S_n. A Γ-invariant state w on D extends to a state η of E by C* state extension. Average η over S_n. Weak-* compactness supplies a cluster point η∞; it still restricts to w and is Γ-invariant, because each fixed permutation belongs to every sufficiently large S_n.

Let K be the compact convex set of invariant states of E and K_w={η∈K:η|D=w}. If w is extreme in the invariant state space of D, K_w is a face of K: a nontrivial convex decomposition in K restricts to a decomposition of w, forcing both restrictions to equal w. Choose an extreme point of K_w by the compact convex extreme-point theorem. Since K_w is a face, that point is extreme in K. This proves the literal lifting property in the C* setting. For universal unital free products the canonical map induced by a unital C* inclusion is an inclusion, so the argument applies to F(A)⊂F(A').

This standard deduction and C1 coexist. Covering every downstairs extreme state under restriction does not ensure that every upstairs extreme state restricts to a downstairs extreme state. Ambient invariance needs both directions, not just lifting.

## C4. Mere commutativity of A does not turn its free product into a classical sequence

Here is an independently verified historical mechanism, explicitly present as DKW v3 Example 5.2.1 and as the Boolean construction in Crismale–Fidaleo arXiv:1310.1566 §7. On H=ell²({0,1,2,...}), let X_i=e0i+ei0. Since X_i³=X_i, each X_i defines a unital representation of A=C³ with a=(1,-1,0) mapped to X_i. The universal free product supplies π:F(A)→B(H). Let w(z)=<π(z)e0,e0>.

Finite permutations of positive indices fix e0 and conjugate X_i into X_sigma(i), so w is exchangeable. For i≠j,

    X_i² X_j²=e00,
    X_i e00=e_i0,  e00 X_j=e0j,  X_i e00 X_j=e_ij.

Thus the image algebra is K(H)+C1. Its vector state at e0 is pure: in any state decomposition, both components assign 1 to e00; Cauchy–Schwarz annihilates terms with 1-e00 on either side, so each component evaluates T as <Te0,e0>. Pullback through π is pure and therefore extreme exchangeable.

But for i≠j,

    w(a_i²)=1,
    w(a_i a_j a_i a_j)=0.

A classical tensor-product law with this marginal would have interlaced moment 1, since the copies commute. Thus the assertion that extreme exchangeable states must be classical product states is false if its only assumption is that the single-copy A is commutative while F(A) remains the unrestricted free product. The source's classical comparison is sound when the whole sequence algebra is commutative, equivalently when the state factors through the commutative/tensor coproduct. C4 clarifies category; it does not establish a historical resolution of the ambient-independence problem.

## C5. A faithful-state strengthening is available from known DKW machinery

This is optional scope information, not needed to repair C1 and not a claim of historical novelty. It shows that excluding every faithful-only formulation would overstate the limitation if coincident B,C are allowed.

Let A'=M2, Z=diag(1,-1), E:M2⊕M2→D={(d,d):d∈M2} be E(a,b)=( (2a+b)/3, (2a+b)/3 ), and θ(a)=(a,ZaZ). Give D the pure vector state at (1,1)/sqrt(2). E has faithful GNS representation. D together with θ(M2) generates M2⊕M2: diagonal units are common, while off-diagonal units have opposite signs in the two blocks; linear combinations with D separate blocks, and products produce their diagonal units. Eθ(M2) spans D, because it leaves diagonal units fixed and scales off-diagonal units by 1/3. Hence the minimality and generation conditions of DKW Definition 7.1 hold (the state on D has faithful GNS representation, since M2 is simple).

The DKW amalgamated-free-product construction and Theorem 8.1 give an extreme ordinary symmetric state on F(M2). Its marginal is

    φ'(a)=< (2a+ZaZ)/3 v,v>,  v=(1,1)/sqrt(2),

with density matrix [[1/2,1/6],[1/6,1/2]], eigenvalues 2/3 and 1/3; thus φ' is faithful. The diagonal projection r is in D, so every copy of r is identified in the amalgamated free product. Let A=C²⊂M2 diagonally and B=C=A. Its marginal is the faithful fair state, and the full B*C joint law matches upstairs. Downstairs C1's smaller-projection argument excludes every extreme witness. This gives ambient dependence with both ambient states faithful, but B=C. It uses an already public general theorem and an elementary specialization; the audit has not verified a prior author stating this exact corollary.

No faithful-state claim with distinct proper B,C and scalar intersection is proved here. The candidate's original theorem needs no such strengthening.

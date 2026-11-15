# Checkable adversarial derivations

## Literal quotient over Z and arbitrary base change

For n>=2 define a free graded abelian group B_n with basis 1; x_i,y_i in degree1; u_i,v_i in degree2; nothing in larger degrees. Give it a unit and the commutative multiplication

x_i*x_i=u_i; x_i*y_j=v_i if j!=i; all other degree1 products zero; every degree2 times positive degree zero.

Associativity is immediate for three positive-degree elements since both bracketings vanish. Every displayed quadratic relation of the manuscript vanishes in B_n, as does every cubic. Thus the literal Z-polynomial quotient Q_n maps to B_n. In the other direction all surviving monomials in Q_n are 1,x_i,y_i,x_i^2,x_i*y_j; for each fixed i all off-diagonal x_i*y_j agree, and there are no larger-degree monomials. Send u_i to x_i^2 and v_i to any x_i*y_j with j!=i. This is well-defined, preserves the product table and is inverse on the polynomial generators. Therefore Q_n is exactly B_n as a ring, not merely equal in rank over Q. This excludes hidden torsion or additional modular relations. Tensoring this explicit integral isomorphism with any field K proves the exact Hilbert function and basis. For n=2 each v_i has just one representative; for n=1 instead Q_1 has basis 1,x,y,u=x^2 and the product x*x=u only.

## Arbitrary-form determinant and an independent common obstruction

Write l=sum(a_i*x_i+b_i*y_i) and B=sum b_i. The product table gives the complete degree1 multiplication matrix in x-all,y-all to u-all,v-all order:

M_l = [[D(a),0],[D(B-b), D(a)(J-I)]].

This is block lower triangular over the polynomial ring Z[a_1,...,a_n,b_1,...,b_n], so det(M_l)=(prod_i a_i)^2 det(J-I). Expand each column of J-I as e-e_i. Terms selecting the e-column twice vanish. Selecting no e-columns contributes (-1)^n; selecting one, in each of n positions, contributes (-1)^(n-1). Therefore

det(M_l)=(-1)^(n-1)*(n-1)*prod_i a_i^2.

This is a polynomial identity before specialization; no coefficient sampling, diagonalization, inverse of n, or infinite-field argument enters. In particular at a good width the successful forms are exactly those with every a_i nonzero, with every b_i unrestricted, over any field. The direct obstruction at a bad width is stronger than testing a symmetric form: z=sum y_j is a nonzero degree1 vector, and x_i*z=(n-1)v_i, y_i*z=0 for every i, hence every linear form kills z. Under any field extension, both the displayed independent basis and this obstruction remain.

An additional attack computes the entire degree1 socle. If q=sum alpha_i*x_i+beta_i*y_i is killed by every degree1 generator, multiplying by x_j gives alpha_j*u_j+(S-beta_j)*v_j=0, S=sum beta_i. Independent u_j,v_j imply alpha_j=0 and beta_j=S for every j. Therefore (n-1)S=0. Conversely these conditions suffice. The socle in degree1 is zero at good widths and is exactly K*z at bad widths. This is not an extra assumption in the proof.

## Strong Lefschetz: all maps and all characteristics

At a good n>=2 the single rational form l=sum x_i has M_l=diag(I,J-I), hence the map degree1->degree2 is bijective. The map degree0->degree1 has nonzero image l. The only power map with both nonzero source and nonzero target not already checked is l^2:degree0->degree2. It sends 1 to sum u_i, whose n separate coefficients are 1, so it is nonzero in every characteristic. In characteristic2 there are still the square terms; n=0 in K does not make a sum of independent u_i vanish. Every remaining positive-power map has zero target and maximal rank0. At n=1, x has rank1 from degree0->1 and from degree1->2, and x^2 maps1 to the nonzero u. Thus n=1 is SLP even though (n-1)1_K=0. SLP always includes WLP, while at a bad n>=2 the common kernel precludes the required degree1->2 bijection.

## Compatibility, width-three generation and infinite logical consequence

Relabel a generator by any injection of column labels, keeping its row labels and repeated indices. Each quadratic monomial generator and each three-distinct-column difference remains of the same type. Every cubic monomial remains cubic, including those with repeated variables. Therefore the entire ideal maps into the next ideal, not just a chosen form or a numerical Hilbert function. Every generator involves <=3 distinct columns. For n>=3 identify those supporting columns with a subset of {1,2,3}; the corresponding generator lies in I_3, and the reverse partial injection extends to a permutation of all n columns. Thus I_n=(Sym(n)I_3)R_n, with the opposite containment supplied by compatibility. No chain is chosen according to n modulo p.

Fix prime p and the one field F_p(t). The theorem says every n>=2 with n not congruent1 modp is good and every n>=2 congruent1 modp is bad. The two particular infinite sequences 2+kp (k>=0) and1+kp(k>=1) therefore have opposite truth values. For any proposed eventual cutoffN choose a term of each sequence beyondN. Neither eventual truth value can hold for WLP or SLP. The original Römer question admits arbitrary K and fixed c>=1, so this one fixed K and c=2 chain defeats its unrestricted assertion. This is no assertion about all characteristic0 chains, any one-row counterexample, or a question's present open status. Killing all extra-row variables gives the same quotient at any fixed c>2 without addressing c=1.

## Exact independent diagnostics and limits

Before native code/results or foreign primary bodies were read, independent_controls.py built the full commutative quadratic monomial relation row space. It computes multiplication rank as rank(relations+all multiplication images)-rank(relations), with no published basis/matrix used to construct those images. It exhausts 1,159 coefficient vectors for (n,p)=(1,2),(1,3),(2,2),(2,3),(3,2),(3,3),(4,2), checks squares independently and checks all-form classifications. It also obtains quotient coordinates using rational elimination and verifies21 nonsymmetric integer determinant cases at n=2,...,8 after explicitly ordering target u-all then v-all. Three false claims are rejected: characteristic2 squares always vanish; badness is p|n; and n=1 obeys the n>=2 bad-width rule. These are bounded diagnostics, not a proof at arbitrary width or field. The universal ring/matrix/socle arguments above supply that proof.

The first reviewer run stopped on a target-basis ordering expectation: sorted monomials interleave u_i and v_i. An explicit target row permutation fixed the reviewer diagnostic before its final run and OWN_PROOF_RESULTS_SEAL. No source change or theorem repair occurred.

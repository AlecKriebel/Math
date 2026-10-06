# Distinct adversarial mechanisms, supplementary to the early seal

The early derivation is unchanged. These mechanisms check the already claimed elementary partial; neither searches for a higher-strand representation nor adds a substantive attempt.

## A positive-cone proof for mixed cyclic words

Let S=UVU, R=UV, C=diag(-1,1). Direct multiplication gives

    -C(SR)C = [[1,1],[0,1]] = P,
    -C(SR^2)C = [[1,0],[1,1]] = Q.

For any nonempty product of P,Q, entries are nonnegative, diagonal entries remain at least 1, and the sum of entries strictly increases at each right multiplication: multiplication by P adds the sum of the first column; multiplication by Q adds the sum of the second column. Each increment is at least 1. Starting from I with entry sum 2, a nonempty product has entry sum >2, so it is neither I nor -I. This universal inequality covers all lengths and handles pure parabolic products P^r or Q^r, which have trace 2 yet remain nonidentity.

Every nonempty reduced word in C2*C3 is conjugate to a cyclically reduced word. Removing its first syllable by conjugation whenever its end factors agree strictly decreases reduced length, so the process terminates. A length-1 outcome is a nonidentity element of a finite factor, whose displayed matrix is non-scalar. Every longer cyclically reduced word has even length and opposite end factors. Rotate it by conjugation, if necessary, to begin with a and end with b^epsilon; it is a product of the blocks ab or ab^2. Its conjugated matrix, up to (-1) per block, is the nonempty positive product above. Thus no nonempty reduced word is projectively identity. This is a distinct whole-word mechanism from the original domain-switching ping-pong witness algorithm; the same projective kernel and scalar-twist conclusion follow.

The new program independently cyclically reduces and tracks exact matrix conjugators, tests all short reduced quotient words plus cyclic rotations and short arbitrary conjugations, and checks the positive-cone inequality. Finite enumeration verifies the implementation, whereas termination and positivity prove the universal claim.

## Construction for arbitrary integer polynomial types

Take any nonzero p(x)=p_0+...+p_d x^d in Z[x] with p_0 p_d !=0. There is no monicity, irreducibility, separability, unit or real-root condition. Form the quotient algebra A=Q[x]/(p). The class X is a unit because

    X * (-(p_1+p_2 X+...+p_d X^{d-1})/p_0) = 1 in A.

This explicitly checks negative powers without numerical roots or companion matrices. For every integer j, x^j p is a nonzero integer Laurent polynomial and U(x^j p) is the group word product D^k b^{c_k} D^{-k}, realized with signed integer coefficients and indices. Its formal matrix is nonidentity; its value in A is identity. Every algebraic root alpha of p is nonzero, and evaluation A -> Q(alpha) therefore also kills it. A is deliberately a quotient algebra, which may have zero divisors; it is not called a number field unless p is irreducible. This prevents the scalar-restriction theorem from being justified with a reducible quotient.

Conversely, every nonzero algebraic alpha has such an integer p after clearing its rational minimal polynomial denominators (its constant is nonzero). The symbolic construction proves the universal obstruction for the displayed representation. The code generates all coefficient types in {-2,-1,0,1,2} of degrees 1 through 4 with nonzero ends, including nonmonic, repeated-root, reducible, rational/nonintegral, real/complex and root-of-unity cases. Four Laurent shifts check negative and positive indices via quotient arithmetic. It is not a universal finite search, a braid kernel, or an obstruction to all representations.

## Independent exact printed-parameter arithmetic

Polynomial arrays independently expand 2(2u^2+2u+4)^2-(u^2+8u+3)^2 and substitute u=2x-1, giving 16(7x^4-14x^3+3x^2+2x+1). Standard-library modular polynomial division checks all roots and every irreducible quadratic over F3. This supports the sealed nonintegrality proof without SymPy or the earlier scripts, and retains its limited conclusion: the printed Salem label fails; actual image nondiscreteness and falsity of the general theorem are not inferred.

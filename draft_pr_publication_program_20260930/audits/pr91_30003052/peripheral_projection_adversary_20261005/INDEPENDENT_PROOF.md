# Independent proof of the peripheral mechanism

This proof was reconstructed before reading `CLASSIFICATION.md` or any author's
review. Its bounded scope is the projection and unimodular spectrum family;
the stable open-disc construction is not established here.

## 1. Peripheral decomposition and a contractive, possibly oblique projection

Let A be a complex linear contraction on the finite-dimensional normed space
X=C^k. Then ||A^n||<=1 for every n>=0. Every eigenvalue has modulus at most 1.
No eigenvalue s of modulus 1 admits a nontrivial Jordan block: otherwise there
are nonzero v and w with Av=sv and Aw=sw+v, and

    A^n w = s^n w + n s^(n-1) v.

Its norm is at least n||v||-||w||, contradicting power boundedness. Every longer
Jordan block contains such a length-two chain, so this excludes all of them.

Thus X=E direct-sum F, where E is the direct sum of the eigenspaces with
|s|=1, and F is the sum of all generalized eigenspaces with |s|<1. Both spaces
are A-invariant. Let P be the algebraic projection onto E along F. P commutes
with A. In a suitable basis, B=A|E is diagonal with diagonal entries
s_1,...,s_d in the unit circle, including multiplicities. All eigenvalues of
C=A|F have modulus below 1, so C^n tends to zero in operator norm. For a Jordan
block this follows from its finite binomial expansion, whose terms are a
polynomial in n times a strictly decaying exponential (a zero block becomes
zero after finitely many powers). Equivalence of finite-dimensional norms
transfers this convergence to the supplied norm on X.

There are integers n_j tending to infinity for which s_i^(n_j) tends to 1 for
every i. Here is a compactness proof that explicitly supplies unbounded indices.
In the compact torus, choose a convergent subsequence s^(m_j) of s^n with gaps
m_(j+1)-m_j>=j. Such gaps can be enforced while selecting a subsequence from
any infinite convergent subsequence. Put n_j=m_(j+1)-m_j. Then n_j>=j, and
s^(n_j)=s^(m_(j+1)) / s^(m_j) tends to the identity coordinatewise. If E={0},
take n_j=j instead.

It follows in operator norm on X that

    A^(n_j) = B^(n_j) P + C^(n_j)(I-P)  ->  P.

Since each power is contractive, ||P||<=1. This proof uses no orthogonality.
If E={0}, P=0; if F={0}, P=I. For U the closed unit ball and V=U intersect E,
contractivity and P|E=I imply exactly P(U)=V.

For E nonzero, B is a surjective isometry of the inherited norm. It is a
contraction by restriction; moreover B^(n_j-1) tends to B^(-1), and each
B^(n_j-1) is contractive. Thus B^(-1) is contractive too, giving
||Bx||=||x||. In particular B maps V bijectively onto itself.

## 2. Uniform factorization of every unimodular eigenfunction

Take f in complex C(U) with K_A f=lambda f and |lambda|=1. For every x in U,
both A^n x and A^n P x belong to U, since A and P are contractions. Also

    sup_(x in U) ||A^n x-A^n P x||
       <= ||A^n(I-P)||  ->  0.

The compactness of U makes f uniformly continuous. Consequently

    sup_(x in U) |f(A^n x)-f(A^n P x)|  ->  0.

Iterating the eigenfunction relation at x and at Px gives the exact equality

    |f(A^n x)-f(A^n P x)| = |f(x)-f(Px)|,

because |lambda^n|=1. The right side is independent of n, hence vanishes
uniformly. Therefore f=f composed with P. No phase choice for lambda^(n_j),
invariant measure, or pointwise-to-uniform inference is needed.

Restriction h=f|V is nonzero when f is nonzero, since f=hP and P(U)=V; it
satisfies h(Bv)=lambda h(v). Conversely any h in C(V) satisfying that equation
gives f=hP in C(U), because PA=BP. The restriction/extension correspondence
preserves the supremum norm.

## 3. Exact unimodular eigenvalue group, not merely its closure

Suppose first d=dim(E)>0. Choose linear coordinate functions ell_1,...,ell_d
in a diagonalizing basis of B. Then

    ell_i(Bv)=s_i ell_i(v),
    conjugate(ell_i(Bv))=s_i^(-1) conjugate(ell_i(v)).

Every monomial

    M_(p,q)(v)=product_i ell_i(v)^(p_i) conjugate(ell_i(v))^(q_i),

where p_i,q_i are nonnegative integers, is a continuous eigenfunction of K_B
with eigenvalue mu_(p,q)=product_i s_i^(p_i-q_i) in Gamma. It is nonzero on V:
choose a vector with every used coordinate nonzero, and multiply it by a small
positive scalar to place it in V. No negative powers of coordinate functions
or division at a zero is used. These monomials supply every element of Gamma,
and hP supplies the corresponding eigenfunction on U.

The complex algebra of finite linear combinations of the monomials contains
constants, separates points of V, and is closed under complex conjugation.
The complex Stone-Weierstrass theorem therefore makes it uniformly dense in
C(V). This is a topological approximation theorem on the actual compact ball,
not an L^2 assertion on a selected orbit or on an invariant measure.

Let lambda be unimodular but outside Gamma, and define on C(V)

    T_N = (1/N) sum_(n=0)^(N-1) lambda^(-n) K_B^n.

Each T_N has norm at most 1. On each monomial M of weight mu in Gamma,

    T_N M = [(1/N) sum_(n=0)^(N-1) (mu/lambda)^n] M  ->  0,

since mu/lambda is unimodular and unequal to 1. The coefficient has modulus
at most 2/(N|1-mu/lambda|). Thus T_N p tends uniformly to zero for each fixed
polynomial p. If K_B h=lambda h, then T_N h=h. For arbitrary epsilon>0,
choose p with ||h-p||<epsilon, giving

    ||h|| <= epsilon + ||T_N p||.

Let N tend to infinity, then epsilon to zero. Thus h=0. Uniform convergence
over all monomials or a lower bound on all their frequency gaps is neither
asserted nor needed: the approximating polynomial is fixed first. This remains
valid when Gamma is dense and lambda belongs to closure(Gamma) minus Gamma.

If E={0}, V={0} and C(V)=C; K_B is the identity on constants. By Section 2
the only nonzero unimodular eigenfunctions of K_A are constants, with lambda=1.
This agrees with the prescribed convention Gamma={1} for empty S.

Therefore under every stated hypothesis,

    sigma_p(K_A) intersect {lambda: |lambda|=1} = Gamma.

## 4. Full peripheral spectrum and the J-empty edge

On C(V), K_B is an invertible isometry (identity on a singleton if E={0}).
Neumann series for K_B and K_B^(-1) put its spectrum inside the unit circle.
Its spectrum contains closure(Gamma), since it contains every point eigenvalue
in Gamma and spectrum is closed.

A closed subgroup of the circle is finite or the whole circle. For completeness,
if such a subgroup has nonidentity elements with arbitrarily small positive
angles, integer multiples of those angles approximate every circle angle, so
closedness gives the whole circle. Otherwise the smallest positive angle is
attained by compactness; division with remainder shows every angle is an integer
multiple of it, and the group is finite. Applied to closure(Gamma), either
closure(Gamma) is the circle, in which case the inclusions already give equality,
or Gamma is the finite group of q-th roots of unity for some q>=1. In the latter
case s_i^q=1, so B^q=I and K_B^q=I. When lambda^q is not 1,

    (K_B-lambda I) sum_(j=0)^(q-1) lambda^j K_B^(q-1-j)
       = (1-lambda^q) I,

which supplies the inverse explicitly. Hence sigma(K_B)=closure(Gamma).

If J is empty, F consists exclusively of the generalized zero eigenspace and
C is nilpotent, say C^m=0. Q:C(U)->C(U), Qf=fP, is a bounded projection that
commutes with K_A. Its range is isometrically C(V), and K_A there is K_B under
restriction/extension. Its kernel consists of functions vanishing on V.
For f in ker(Q), A^m x=B^m Px lies in V, so K_A^m f=0. Thus K_A splits into
the peripheral operator and a nilpotent operator on ker(Q).

When F={0}, Q=I, ker(Q)={0}, and sigma(K_A)=closure(Gamma). When F is nonzero,
ker(Q) is nonzero: a nonzero linear functional on F composed with I-P supplies
an element. A nilpotent operator on a nonzero space has spectrum exactly {0}
and has a nonzero kernel, giving point eigenvalue 0. Thus in this J-empty case

    sigma_p(K_A)=Gamma union Z_A,
    sigma(K_A)=closure(Gamma) union Z_A,

where Z_A={0} exactly when 0 is an eigenvalue of A and is empty otherwise.
In particular A=0 on k>=1 has spectrum and point spectrum {0,1}.

## Bounded conclusion

The local peripheral claims and the entire J-empty case are proved here under
the supplied finite-dimensional contraction hypotheses. This does not establish
the J-nonempty open-disc eigenfunction construction, any source-identity claim,
priority, originality, publication readiness, or a human peer-review verdict.

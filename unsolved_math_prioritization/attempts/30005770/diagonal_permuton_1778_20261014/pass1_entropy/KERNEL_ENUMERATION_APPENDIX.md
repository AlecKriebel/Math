# Direct enumeration of beta(0,1) trees from the catalytic equation

## Purpose and scope

This appendix proves the tree generating function used in the fixed 1342/2431 argument directly from the labeled-tree specification. It removes dependence on conflicting index conventions in a displayed external counting formula. It does not replace the external bijection between permutations and these trees, prove a new permuton case by itself, or extend the target family.

The construction is self-contained. All generating functions initially denote formal series, so convergence is not assumed during the derivation.

## The precise tree classes

A proper tree is a rooted ordered tree with nonnegative integer vertex labels, subject to:

- A leaf has label zero.
- The root has the sum of its children's labels.
- Each internal nonroot vertex has any label between zero and one plus the sum of its children's labels, inclusive.

The singleton is permitted. Size means the number of vertices.

A relaxed tree has the same conditions except that the root, too, may have any label between zero and one plus the sum of its children's labels when it is internal. Write

    T(z) = sum_{proper Q} z^|Q|,
    B(z,u) = sum_{relaxed Q} z^|Q| u^label(root(Q)),
    C(z) = B(z,1)/(1−B(z,1)).

There are finitely many ordered shapes of each size. By induction on the subtree size, every label in a relaxed tree of size n is at most n−1. Hence each coefficient [z^n]B(z,u) is a polynomial in u. In particular

    B(z,u) ∈ z Q[u][[z]],    B(z,u)=z+O(z²),
    C(z) ∈ z Q[[z]],        T(z) ∈ z Q[[z]].

The vertex-label upper bound is sufficient to justify every later substitution and formal derivative.

## Lemma: exact catalytic equation

The root of a proper tree is determined uniquely after an arbitrary ordered sequence of relaxed child trees has been chosen, including the empty sequence. Therefore

    T(z)=z/(1−B(z,1))=z(1+C(z)).                                (1)

For a relaxed internal root whose child labels sum to S, its label weight is

    1+u+...+u^(S+1)=(1−u^(S+2))/(1−u).

Separate the singleton root, and then sum over nonempty ordered child sequences. Their unweighted series is C(z), and their series weighted by u to the total child-label sum is B(z,u)/(1−B(z,u)). Thus

    (1−u)(B(z,u)−z)
       = z C(z) − z u² B(z,u)/(1−B(z,u)).                       (2)

Equation (2) is an identity of formal series with polynomial coefficients in u. The finite geometric-sum identity proves it without evaluating 1/(1−u) at u=1.

Multiplying by the invertible series 1−B gives

    P(z,u,B(z,u),C(z))=0,                                      (3)

where the polynomial in the placeholders u,b,c is

    P(z,u,b,c)=(1−u)(b−z)(1−b)−zc(1−b)+zu²b.

## Lemma: a formal kernel point exists

Let P_b denote the partial derivative with respect to the placeholder b, and define

    F(z,u)=P_b(z,u,B(z,u),C(z)).

Near u=1, this can be regarded as a formal series in z and v=u−1. Because B(0,u)=C(0)=0,

    F(0,u)=1−u,
    F(0,1)=0,    (partial F/partial u)(0,1)=−1.

The formal implicit function theorem therefore gives a unique U(z)∈Q[[z]] with U(0)=1 and

    F(z,U(z))=0.                                               (4)

This elementary use of the formal theorem can alternatively be implemented recursively: the coefficient of z^k in U is determined with coefficient −1 after all lower coefficients have been fixed. Put

    beta(z)=B(z,U(z)).

The substitution is well-defined: the coefficient of each power of z in B is a polynomial in u, so only finitely many data contribute to each resulting coefficient. Moreover beta=z+O(z²).

Differentiate (3) formally with respect to u, treating C(z) as independent of u. The chain rule gives

    P_u(z,u,B,C) + P_b(z,u,B,C) B_u(z,u)=0.

Substitution of U(z) and (4) show that at (z,U,beta,C),

    P=0,    P_b=0,    P_u=0.                                   (5)

No analytic differentiation or convergence assertion has been used.

## Lemma: elimination and selection of the correct branch

Direct polynomial addition gives

    P+(1−b)P_b = (1−u)(1−b)²+zu².

Consequently (5) implies

    (1−U)(1−beta)²+zU²=0.                                     (6)

Since U has constant term 1, it is invertible. Thus

    z=(U−1)(1−beta)²/U².                                     (7)

The equation P_u=0 is

    (beta−z)(1−beta)=2zU beta.                                 (8)

Substitute (7) in (8), multiply by U², and cancel the invertible series 1−beta. The resulting equation factors as

    (beta U−beta+1)(2 beta U−beta−U+1)=0.                      (9)

The first factor has constant term 1 and is therefore invertible. The second must vanish, giving

    U=(1−beta)/(1−2 beta),
    z=beta(1−2 beta).                                         (10)

The unique formal solution of the latter equation with beta(0)=0 is

    beta=(1−sqrt(1−8z))/4,                                    (11)

where the square root is the formal binomial series with constant term 1. The other quadratic branch has nonzero constant term and cannot equal B(z,U).

Finally P_b=0 reads

    (1−U)(1−2 beta+z)+zC+zU²=0.

Substituting (10) and simplifying gives

    C=beta(1−3 beta)/(1−2 beta)².                              (12)

One way to verify the cancellation without dividing by a zero constant term is to first obtain

    zC = beta²(1−3 beta)/(1−2 beta).

Then use z=beta(1−2 beta) and cancel the nonzero series beta in the integral domain Q[[z]]. The remaining denominators have constant term 1 and are invertible.

## Theorem: tree generating function and coefficient asymptotics

Put s=sqrt(1−8z). Equations (11)–(12) give

    C(z)=(1−s)(1+3s)/(4(1+s)²).

Using (1),

    T(z)=(1−s)(s²+10s+5)/(32(1+s))
        =[8z²+12z−1+(1−8z)^(3/2)]/(32z).                     (13)

The apparent singularity at z=0 in the second expression is removable; the first expression and the original combinatorial definition are formal series with no constant term. Expanding yields

    T(z)=z+z²+3z³+12z⁴+56z⁵+288z⁶+1584z⁷+9152z⁸+... .

The binomial expansion of (1−8z)^(3/2) gives t_1=1 and, for n≥2,

    t_n=[z^n]T(z)
       =3·2^(n−2)·(2n−2)! / ((n+1)!(n−1)!).                 (14)

Stirling's formula then gives

    t_n ~ (3/(16 sqrt(pi)))·8^n·n^(−5/2).                     (15)

Thus the radius of convergence is rho=1/8, and (13) yields

    T(rho)=5/32.

This establishes the precise generating function, vertex indexing, positive radius, growth rate, polynomial prefactor, and finite critical value needed by the weighted-height argument. These conclusions now follow from the exact tree specification, independently of any source's printed indexing of its tree counts.

## Boundary of this appendix

The passage from uniform 1342-avoiding permutations to uniform labeled forests, and the fact that the tree shape retains the permutation's left-to-right minima, still rely on the explicitly cited Bóna bijection. This appendix addresses only the enumerative input. It makes no novelty assertion.

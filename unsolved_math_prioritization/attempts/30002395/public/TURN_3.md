# Turn 3: Construct an algebra from the Dini functions

Substantive approach: the Dini functions determine X. Try to turn them into a commutative function algebra, or try to use failure of compact intersections as an obstruction to nuclear realization. An explicit realization shows why both inferences fail.

## The space and its topology

Let X=N disjoint union {a,b}. Each n is isolated. A set containing a or b is open exactly when it contains all but finitely many natural numbers (and it may contain either or both endpoints). Sets contained in N are arbitrary open sets. This is the convergent sequence with two distinct limit points.

X is T1 and second countable. Every point has a quasicompact neighborhood: a tail together with its chosen endpoint is a convergent sequence, and isolated points have singleton neighborhoods. It is sober. Indeed, if a closed irreducible F contains n and some other point, the closed subsets {n} and F minus {n} cover F properly; F minus {n} is closed because {n} is open. Thus an irreducible closed F that meets N is a singleton. If it misses N, it is a nonempty subset of the finite T1 space {a,b}, so irreducibility again forces a singleton. Each singleton is its own generic-point closure. Hence X is a Dini space in the intended sense.

K_a=N union {a} and K_b=N union {b} are compact: an open cover has a member containing the specified endpoint, hence all but finitely many n. Finitely many additional members suffice. Each K is open, and therefore a G_delta. Their intersection N is not compact, as its singleton open cover has no finite subcover. X is not coherent.

## A direct separable nuclear realization

Set

A={ (z_n) in product_n M_2(C) : z_n converges in norm to diag(alpha,beta) for some alpha,beta in C }.

The norm is the supremum norm. This is a closed *-subalgebra of bounded matrix sequences. For m>=0 let A_m consist of sequences that equal their diagonal limit after coordinate m. Then A_m is isomorphic to M_2(C)^m direct-sum C direct-sum C. The inclusion into A_{m+1} copies diag(alpha,beta) into the next matrix coordinate and retains alpha,beta as the new tail coordinates. These are injective *-homomorphisms. The union of A_m is norm dense in A because each convergent sequence can be replaced by its limit after finitely many coordinates. Thus A is separable and AF.

Nuclearity can be checked without a classification theorem: E_m:A->A_m retains the first m entries and replaces the rest by the diagonal limit. E_m is a *-homomorphism, the inclusion A_m->A is a *-homomorphism, and ||E_m(z)-z|| tends to zero for every z. These completely positive contractive factorizations through finite-dimensional algebras establish nuclearity directly.

Let J=c_0(N,M_2), an ideal of A. We have A/J=C direct-sum C. Its two characters give primitive ideals P_a and P_b, the kernels of alpha and beta. Coordinate evaluation at n gives a primitive ideal P_n. There are no others. To prove this, let pi be an irreducible representation. If pi(J)=0, it factors through C direct-sum C. Otherwise some central coordinate projection e_n has pi(e_n) nonzero: if all pi(e_n)=0, density of finite-support matrices in J forces pi(J)=0. Since e_n is central and pi is irreducible, pi(e_n)=1. Thus pi factors through the n-th copy of M_2, and its kernel is P_n.

The bijection X->Prim(A) sending n,a,b to these kernels is a homeomorphism. The basic open support of z is the set of n with z_n nonzero together with a if alpha is nonzero and b if beta is nonzero. Convergence forces the support to contain cofinitely many n whenever an endpoint is present. Conversely every specified open O is such a support. If O is contained in N, choose z_n=2^{-n}1_{M_2} for n in O and zero otherwise. If O contains endpoints, let D be the diagonal matrix with a 1 precisely at each included endpoint, and take z_n=D for n in O, zero otherwise; only finitely many n are omitted. Its limit is D. This proves exactly the stated topology.

## The function-algebra obstruction

Let f=1_{K_a} and g=1_{K_b}. They are lower semicontinuous because K_a and K_b are open. Both are Dini functions under the decreasing-closed-set definition: if closed decreasing F_m all meet K_a, compactness of K_a and the finite intersection property imply that their intersection meets K_a; otherwise one supremum is already zero. The same proof applies to K_b.

Their minimum and product equal h=1_N. Let F_m={a,b} union {n:n>=m}. These are decreasing closed subsets of X, their intersection is {a,b}, and sup_{F_m} h=1 for every m whereas sup_{intersection F_m} h=0. Thus h is not Dini. Also f+g is not Dini: its successive suprema are 2 and its supremum on the intersection is 1.

Outcome: noncoherence does not obstruct even AF realization, and Dini functions cannot generally be treated as an algebra closed under products, sums, or minima. This reconstructs the explicit AF example already supplied by Kirchberg in the 2013 report, with complete spectrum and function calculations; it is not a new counterexample or a solution of the universal question.

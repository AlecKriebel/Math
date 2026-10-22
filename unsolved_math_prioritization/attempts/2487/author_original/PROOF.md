# Authored verification of the known reduction and negative subanswer

This is an exposition of prior mathematical content for EP-1097, not a new solution of its open order-estimation question. The restricted-sums/differences reduction is credited on the first-party discussion to Koishi Chan [9]. The seed used below is the classical Ruzsa example reproduced in Lemm [3, p. 3].

## 1. Exact integer formulations

For finite A subset Z, write

    D(A) = {d in Z \ {0}: there is x with x, x+d, x+2d in A}.

Write F(n) = max_{|A| <= n} |D(A)|. This maximum exists: the nonnegative integer counts are bounded by n(n-1), so their nonempty set of possible values has a maximum. For finite U,V subset Z and G subset U x V, write

    C = {u+v : (u,v) in G},     E = {u-v : (u,v) in G}.

Define M(N) as the maximum of |E| subject to |U|, |V|, |C| <= N. The same finiteness-of-counts observation applies. All integers N below are positive.

For an integer set A, take U=V=A and

    G = {(u,v) in A x A : u != v and (u+v)/2 lies in A}.

Then C is a subset of 2A, where 2A means the dilation {2a:a in A}. Also E = {-2d:d in D(A)}. Hence |E|=|D(A)| and F(n) <= M(n).

Conversely, given U,V,G, put S = 2U union 2V union C. This is an integer set with |S| <= 3N. For each edge (u,v), the triple (2u,u+v,2v) lies in S and has common difference v-u. If u!=v it is nonconstant. Thus -E with zero removed is a subset of D(S), and

    |E| <= |D(S)| + 1 <= F(3N) + 1.

Therefore M(N) <= F(3N)+1. For each fixed exponent c>=1, a uniform O(N^c) bound for either extremal function gives one for the other. Their infimal uniform upper exponents agree. This conclusion does not require an endpoint estimate at the infimum.

The set D(A) is symmetric under negation, so its positive part has exactly half its size. Allowing zero adds at most one. Requiring exactly n points rather than at most n makes no difference to the maximum, since any finite integer set can be enlarged without destroying its progressions.

## 2. Elementary reproduction of the prior negative answer

The following deliberately weak bound is sufficient to refute exponent 3/2 without relying on decimal optimization or entropy endpoint issues. It is the tensor construction from Ruzsa's three-point seed {(0,1),(1,0),(1,1)}.

For k>=1 define

    B_k = {sum_{i=0}^{k-1} b_i 5^i : b_i in {0,1}},
    C_k = {sum_{i=0}^{k-1} c_i 5^i : c_i in {1,2}},
    S_k = 2B_k union C_k.

Base-5 uniqueness gives |B_k|=|C_k|=2^k. The digits of 2B_k are 0 or 2, with no carrying. Thus 2B_k intersects C_k only at the integer with every digit 2, and |S_k|=2^(k+1)-1.

Choose any vector (e_0,...,e_{k-1}) in {-1,0,1}^k. For each digit choose (u_i,v_i)=(1,0) if e_i=-1, (1,1) if e_i=0, and (0,1) if e_i=1. Put u=sum u_i5^i and v=sum v_i5^i. Then u,v belong to B_k and u+v belongs to C_k. The triple

    2u, u+v, 2v

is an arithmetic progression in S_k, of common difference

    d = v-u = sum e_i 5^i.

These 3^k differences are distinct. Indeed, equality for two digit vectors, reduced modulo 5, forces their zeroth digits to agree because their difference lies between -2 and 2. Division by 5 and induction forces every digit to agree. Only the all-zero vector gives zero. Consequently

    |D(S_k)| >= 3^k - 1.

Writing n_k=|S_k|, we obtain

    |D(S_k)| / n_k^(3/2)
        >= (3^k-1) / 2^((3/2)(k+1))
        = 2^(-3/2) (3 / 2^(3/2))^k (1-3^(-k)).

This tends to infinity since 3/2^(3/2)>1, equivalently 9>8. No uniform O(n^(3/2)) bound is possible. The same conclusion holds for positive differences, with one extra factor of 1/2.

This argument supplies only the weaker exponent log(3)/log(2); it is not the current lower record. Section 2 is a verification of a known seed construction, not an additional research attempt.

## 3. The theorem-dependent upper bound and stronger known lower bound

Katz-Tao [2, Theorem 1.1] applies directly to U,V,G above: the number of restricted differences is at most N^(11/6) when the three input cardinalities are at most N. Thus F(n)<=n^(11/6).

Lemm [3, Theorem 2.1] supplies a sums-differences lower exponent strictly above 1.77898. Its finite-type constructions use integer coordinates from the displayed seed. To pass from finitely many integer vectors to integers, choose a base larger than twice every absolute coordinate appearing among the finite lists to be distinguished, then map (z_0,...,z_{m-1}) to sum z_i B^i. A largest-nonzero-digit argument proves injectivity on each needed finite coordinate set; the map preserves addition. This preserves the relevant cardinalities, restricted sums, and distinct restricted differences. The comparison in Section 1 then transfers the exponent to the progression problem.

We use Lemm's stronger result as a cited theorem and do not claim to have independently certified its optimized numerical value. The non-O(n^(3/2)) conclusion already has the exact proof in Section 2. Neither that proof nor the cited estimates determine the optimal exponent.

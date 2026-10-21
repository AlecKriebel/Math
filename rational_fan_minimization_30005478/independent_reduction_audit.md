# Independent adversarial audit: rational-fan minimization

Audit date: 2026-10-21 UTC. Status: PASS for the precise arbitrary-finite-rational-fan statement below. This is not an algorithm deciding rational points, an undecidability theorem, or a result for pure/balanced/tropical-realizable fans.

## Audited claim

For a finite rational polyhedral fan Sigma in Q^N, minimize

f_Q(U) = 2 dim(U + |Sigma|) - dim U

over rational linear subspaces U. Dimensions refer to the associated real polyhedral sets; equivalently use the rational spans V_i of its cones and write f_Q(U)=max_i(2 dim(U+V_i)-dim U).

Computing this minimum and deciding whether an explicitly defined projective algebraic set over Q has a Q-point are equivalent under effective finite oracle reductions. A threshold version admits the same rational incidence description. No polynomial-time bound is asserted. The ambient dimension is allowed to vary. Fans are not required to be pure, balanced, or tropicalizations.

Files inspected: projective_equivalence.md, arithmetic_gap.md, and the original verify_arithmetic_gap.py. The verification script was independently rerun and passed; the essential universal arguments were checked symbolically, not inferred from its finite computations.

## 1. Anchors: no hidden extra minimizers

Let H,E,F be pairwise complementary, with dimensions h,h-r,h-r. Set M=2h-r. For an arbitrary U put s=dim U, a=dim(U intersect H), b=dim(U intersect E). Its H and E objective terms sum to

(s+2h-2a)+(s+2(h-r)-2b)=2M+2(s-a-b)>=2M.

Thus the maximum is at least M. If it is at most M, each term must equal M and s=a+b. The equality forces U=(U intersect H) direct_sum (U intersect E), since this direct sum is contained in U and has its full dimension. Subtracting the two anchor equations gives a-b=r. Since U intersect F=0, the F inequality is s+2(h-r)<=M, hence s<=r. But s=a+b=r+2b, so b=0 and U is an r-plane in H. This excludes mixed graphs, surplus E directions, and odd-dimensional loopholes.

For an incidence dim(A intersect P_i)>=k_i, put p_i=dim P_i and t_i=h-p_i-r+k_i. Impossible bounds k_i>min(r,p_i) are rejected first; bounds k_i<=max(0,r+p_i-h) are automatic and can be discarded. Remaining bounds give t_i>=0 and t_i<=h-r because k_i<=p_i. With V_i=P_i direct_sum F_{t_i}, dim V_i=h-r+k_i. For U=A in Gr(r,H), its term equals M+2(k_i-dim(A intersect P_i)), as required. Every anchor term equals M. Therefore the exact threshold equivalence and lower bound hold.

Edge cases r=0 or r=h are decidable without the construction. Empty constraints are harmless. Negative or oversized intersection requirements must be normalized/rejected as above. An implementation wanting a total many-one reduction can replace immediate yes/no cases with fixed yes/no threshold instances.

## 2. Quiver encoding: loopless hypothesis is necessary and satisfied

In H=direct_sum_v M_v set r=sum_v e_v. Bounds dim(A intersect M_v)>=e_v force equality in every coordinate and A=direct_sum_v A_v. For an arrow s->t with s!=t, its graph G_a in M_s direct_sum M_t satisfies

A intersect G_a = {(x,T_a x): x in A_s and T_a x in A_t}.

Its dimension is at most e_s. Requiring dimension at least e_s is therefore equivalent to T_a(A_s) subset A_t. Zero source dimensions cause no problem. Parallel arrows cause no problem. Loops cannot be silently represented by this graph construction in a single coordinate summand, but the universality construction used here is acyclic and has no loops.

## 3. Field-of-definition closure, proved directly

Primary source inspected: Markus Reineke, “Every projective variety is a quiver Grassmannian,” https://arxiv.org/pdf/1204.5730 (two-page PDF, inspected through the web PDF text tool). The source states its construction over C. The applicable ingredients are its three-vertex acyclic quiver, homogeneous equations converted to linear forms on degree-d monomials, and monomial-deletion arrow maps. The required dimension vector is (0,1,1). Schurian claims are not needed.

Merely citing the complex-point theorem would leave a gap. The following independent calculation closes it.

Start with rational homogeneous defining equations and choose d>=1 at least their degrees. Replace each equation of degree e by all products with degree-(d-e) monomials. The common projective zero set is unchanged: at a projective point some coordinate is nonzero, so its suitable power detects any nonzero original equation. This conversion is finite and rational.

Write degree-d coordinates as z_m, with |m|=d. Form A(z) with entries A_{n,i}=z_{n+e_i}, |n|=d-1. The deletion maps have entries 0 or 1, and the equation forms have rational coefficients. Every nonzero z appears somewhere in A(z), so A(z) is nonzero. A subrepresentation of dimensions (0,1,1) imposes the equation forms and rank A(z)=1; its last line is then uniquely the column span.

To recover a rational projective preimage, factor a rank-one rational A(z) as u c^T with c nonzero and rational. Choose j with c_j!=0. Whenever m_i>0, the common row n=m-e_i gives

z_m c_j = z_{m-e_i+e_j} c_i.

Iterate these identities, without dividing by any c_i other than c_j, until every exponent except j is zero. This gives

z_m c_j^(d-m_j) = z_{d e_j} product_{i!=j} c_i^(m_i).

If z_{d e_j}=0, this forces every z_m=0, a contradiction. Consequently

z_m = (z_{d e_j}/c_j^d) product_i c_i^(m_i).

Thus [z] is the degree-d Veronese image of the rational point [c]. No d-th root is extracted. The rational linear equation forms vanish exactly when the original rational homogeneous equations vanish at [c]. Conversely every rational projective solution gives the desired rational subrepresentation. The construction therefore preserves Q-points effectively, not just complex points. The argument also works over extension fields and includes d=1.

## 4. Fan realization and reverse reduction

For each rational V_i choose rational equations cutting it out, collect their hyperplanes, and add a basis of the ambient dual. The central hyperplane arrangement gives finitely many pointed rational cones. Keep all cones contained in the union of the V_i. This is a subfan: faces remain in that union; intersections are faces; each V_i is a union of retained cones because its defining hyperplanes are among those used. The support is precisely the union of V_i. This is an effective finite construction, and the dimension of U plus its support is max_i dim(U+V_i).

Conversely, for each cone C, dim(U+C)=dim(U+span C): C has a relative interior in its span and its linear image modulo U has a relative interior in the image span. Finite unions take maximum dimension. Hence arbitrary finite input cones reduce to their rational spans without a convexity assumption on their union.

For fixed r and threshold m, the objective bound is equivalent to

dim(U+V_i)<=floor((m+r)/2) for every i, with U in Gr(r,N).

These are closed rank conditions over Q on the Grassmannian, equivalently Schubert incidence conditions on dim(U intersect V_i). They define an explicit projective algebraic set. Bounds beyond feasible ranks give the empty or entire Grassmannian, not a failure of the construction. Its rational points are exactly the desired rational witnesses. A projective rational-point oracle handles each r=0,...,N. Searching m=0,...,N suffices because U=Q^N gives objective N and every term is nonnegative. This computes the minimum using finitely many oracle calls. Scheme nilpotents do not change rational-point existence; no geometric-point or real-point oracle is substituted.

Use “projective algebraic sets/varieties, not necessarily irreducible” to avoid a convention ambiguity. If an integral-variety oracle formulation is desired, specify the additional effective decomposition step rather than silently assuming irreducibility.

## 5. Independent audit of the real-6/rational-7 example

Take H=X direct_sum Y=Q^4, E=Q^2, F=Q, and the four planes X,Y,graph(I),graph(T), where T=[[0,2],[1,0]]. The six spans are H,E,P_i direct_sum F. The H/E anchor sum gives f(U)>=6. Equality forces s even, U=A direct_sum B in H direct_sum E, dim A=(s+2)/2 and dim B=(s-2)/2. Thus s is 2,4,or6. The other four bounds require dim(A intersect P_i)>=s/2. At s=6 this exceeds dim P_i; at s=4 it forces the 3-plane A to contain X+Y=H, impossible. At s=2, A=L_X direct_sum L_Y; graph(I) identifies the two lines and graph(T) forces a common T-invariant line. Such a rational line would give a rational eigenvalue of T, impossible since its characteristic polynomial is t^2-2. Over R the line spanned by (sqrt(2),1) works. U=W gives rational value 7. Thus the exact minima are respectively 6 and 7.

The supplied explicit cone generators have full ranks and the claimed pairwise-zero intersections: distinct P_i meet only at zero; each padded cone avoids F and H; the H cone has y_2>x_2 and y_1>2x_2, excluding graph(I) and graph(T), and positive X/Y coordinates exclude X,Y. E is complementary. All faces therefore form a pointed rational simplicial fan. Its maximal dimensions are 4,3,2, so it is nonpure.

## Conclusion and publication limits

No counterexample to the stated reduction or explicit gap survived these checks. The precise PASS is an effective equivalence for unrestricted finite rational fans, with a strict real/rational optimum gap. It provides neither a terminating rational-point algorithm nor an undecidability theorem. It does not resolve a more restricted pure, balanced, irreducible-tropical, or matroid-realizable problem. Any general-algorithm or impossibility headline would exceed the mathematics audited here.

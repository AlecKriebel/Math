# Kourovka 21.90: convention boundary and exact obstructions

## Scope and notation

We use finite, simple, undirected graphs. For a connected distance-regular graph of diameter three, let its intersection array be

\[
\{k,b_1,b_2;1,c_2,c_3\},\qquad a_i=k-b_i-c_i,
\]

with the usual endpoint conventions. Let \(A_i\) be its exact-distance matrices, including \(A_0=I\). Write
\(A_iA_j=\sum_h p_{ij}^{h}A_h\).

There are two conventions for *strongly regular*. The permissive convention asks only for a regular noncomplete graph with constant adjacent/nonadjacent common-neighbor counts \((v,k,\lambda,\mu)\), and permits \(\mu=0\). The connected/nondegenerate convention excludes unions of cliques. This distinction changes the existence question. The October 2026 problem does not explicitly settle it. Its proposer had already discussed the exceptional crown graphs in a 2019 paper, so treating those graphs as a newly solved open problem would be unwarranted.

All claims below have their hypotheses stated. None establishes existence or nonexistence for the general connected/nondegenerate question.

## 1. A complete certificate for the permissive-convention examples

For every integer \(n\ge3\), define \(C_n\) on pairs \((\varepsilon,i)\), where \(\varepsilon\in\{0,1\}\) and \(1\le i\le n\). Join two vertices exactly when their first coordinates differ and their second coordinates differ. Thus \(C_n\) is \(K_{n,n}\) with a perfect matching removed.

Distinct vertices on the same side have distance two; opposite vertices with equal labels have distance three; the remaining opposite pairs are adjacent. Consequently its diameter is three and counting neighbors in these distance classes gives

\[
\{n-1,n-2,1;1,n-2,n-1\}.
\]

Its distance-two graph is \(2K_n\), with parameters \((2n,n-1,n-2,0)\). Its distance-three graph is \(nK_2\), with parameters \((2n,1,0,0)\). Both are disconnected.

Here is a direct proof of the Q-polynomial property, with no classification theorem imported. Let \(S\) exchange the two sides, and put

\[
F_+=(I_2+S)/2,\quad F_-=(I_2-S)/2,\quad
G_0=J_n/n,\quad G_1=I_n-G_0.
\]

The adjacency matrix is \(S\otimes(J_n-I_n)\). Its primitive spectral idempotents, in the order

\[
E_0=F_+\otimes G_0,\quad E_1=F_-\otimes G_1,\quad
E_2=F_+\otimes G_1,\quad E_3=F_-\otimes G_0,
\]

have eigenvalues \(n-1,1,-1,-(n-1)\), respectively. They are four distinct eigenvalues, so these are exactly the primitive idempotents.

Entrywise multiplication satisfies
\(F_-\circ F_-=F_+/2\), \(F_-\circ F_+=F_-/2\),
\(G_1\circ G_0=G_1/n\), and
\(G_1\circ G_1=((n-1)G_0+(n-2)G_1)/n\). Hence

\[
\begin{aligned}
2n(E_1\circ E_0)&=E_1,\\
2n(E_1\circ E_1)&=(n-1)E_0+(n-2)E_2,\\
2n(E_1\circ E_2)&=(n-2)E_1+(n-1)E_3,\\
2n(E_1\circ E_3)&=E_2.
\end{aligned}
\]

This is an irreducible tridiagonal Krein multiplication matrix because \(n-2>0\), which is the Q-polynomial condition. The smallest example is the six-cycle. These examples answer the permissive reading affirmatively, but do not answer the connected/nondegenerate reading.

## 2. Independent reduction to three integer parameters

Suppose both \(A_2\) and \(A_3\) are strongly regular under either convention. Their common-neighbor conditions imply

\[
p_{22}^{1}=p_{22}^{3},\qquad p_{33}^{1}=p_{33}^{2}.
\]

Put \(b=b_1,d=b_2,c=c_2,e=c_3\). Multiplication by \(A_1\) in the ordered basis \((A_0,A_1,A_2,A_3)\) is represented by

\[
L=\begin{pmatrix}
0&k&0&0\\1&k-b-1&b&0\\0&c&k-c-d&d\\0&0&e&k-e
\end{pmatrix}.
\]

The distance recurrences give
\(L_2=(L^2-(k-b-1)L-kI)/c\) and
\(L_3=((L-(k-c-d)I)L_2-bL)/e\).
The first column of \(L_i^2\) is \((p_{ii}^h)_h\). Direct multiplication gives

\[
p_{33}^{1}-p_{33}^{2}=-d(d+e-k-1)/c.
\]

Since \(d,c>0\), this forces \(d=k+1-e\). Substitution in the second identity gives

\[
p_{22}^{1}-p_{22}^{3}=-\bigl(b(c+1)-ce\bigr)/c.
\]

Thus, setting \(a=k-e\) and initially \(t=e/(c+1)=b/c\), the array is

\[
\boxed{\{t(c+1)+a,tc,a+1;1,c,t(c+1)\}.}
\tag{1}
\]

Here \(a\ge0\), \(c\ge1\), and \(t>0\). The distance-polynomial recurrence yields the following first eigenmatrix, with rows ordered by adjacency eigenvalues \(k,a+t,-1,-c-1\):

\[
P=\begin{pmatrix}
1&k&tk&k(a+1)/(c+1)\\
1&a+t&-t&-a-1\\
1&-1&-t&t\\
1&-c-1&a+c+1&-a-1
\end{pmatrix},\qquad k=t(c+1)+a.
\tag{2}
\]

For completeness, the polynomials are \(p_2(x)=(x^2-(a+t-1)x-k)/c\) and
\(p_3(x)=((x-(t-1)(c+1))p_2(x)-tcx)/(t(c+1))\).
Each listed eigenvalue satisfies the endpoint recurrence
\((x-a)p_3(x)=(a+1)p_2(x)\). They are distinct, and the adjacency matrix of a diameter-three distance-regular graph has exactly four eigenvalues: the four distance matrices are independent and span its adjacency algebra. Thus (2) is its actual eigenmatrix.

The rational number \(a+t\) is an eigenvalue of an integral matrix, hence an algebraic integer and therefore an integer. Since \(a\) is an integer, \(t\) is an integer. Finally \(a_2=(t-1)(c+1)\ge0\) gives \(t\ge1\). Summing the first row gives

\[
v=(k+1)(k+c+1)/(c+1).
\tag{3}
\]

This reproduces the known reduction without treating the published classification as a black box.

## 3. Independent Q-polynomial obstruction

Let \(Q=vP^{-1}\), so \(E_j=v^{-1}\sum_r Q_{rj}A_r\). Define Krein parameters by
\(E_i\circ E_j=v^{-1}\sum_h q_{ij}^hE_h\). Entrywise multiplication and the eigenmatrix relation give

\[
q_{ij}^h=v^{-1}\sum_r Q_{ri}Q_{rj}P_{hr}.
\tag{4}
\]

They are nonnegative: the entrywise product of two positive-semidefinite matrices is positive semidefinite (represent the entries as Gram inner products of tensor products), and its eigenvalue on the \(E_h\) space is \(q_{ij}^h/v\).

Set
\[
D=(c+1)(t^2-a-1)-a(a+1),\quad
H=(c+1)(a+t+1)^2(a+c+t+1)^2.
\]

Expansion of (4), also checked symbolically by the accompanying code, gives

\[
\begin{aligned}
q_{11}^2&=\frac{ct(k+1)(k+c+1)(2a+ct+c+2t+2)}H>0,\\
q_{11}^3&=\frac{c(k+1)(k+c+1)D}H,\\
q_{22}^1=q_{22}^3&=\frac{a(a+1)(k+1)(k+c+1)}{(c+1)(a+t+1)^2},\\
q_{33}^1=q_{33}^2&=\frac{t(t-1)(k+1)(k+c+1)}{(c+1)(a+c+t+1)^2}.
\end{aligned}
\tag{5}
\]

In a Q-polynomial ordering with generator \(E_g\), its square can involve, besides \(E_0\) and itself, only one other primitive idempotent. If \(a>0,t>1\), both pairs in the last two lines are strictly positive, so neither \(E_2\) nor \(E_3\) can be the generator. The first line then forces \(q_{11}^3=0\). Therefore

\[
\boxed{(c+1)(t^2-a-1)=a(a+1).}
\tag{6}
\]

We only need necessity. To track the boundary carefully: if \(t=1,a>0\), then \(D=-a(a+c+2)<0\), violating Krein nonnegativity even before the Q-polynomial condition. If \(a=0,t>1\), generators \(E_1,E_3\) each have two positive off-diagonal square coefficients, while \(E_2^2\) has no component in either of the two other nonprincipal spaces. The latter generates a Schur algebra of dimension at most two and cannot generate a four-dimensional algebra. Thus this case is not Q-polynomial either. The remaining boundary \(a=0,t=1\) has the crown array from section 1.

For \(a>0,t>1\), (6) implies
\(1\le a\le t^2-2\) and uniquely determines
\(c+1=a(a+1)/(t^2-a-1)\).
Furthermore

\[
\mu(\Gamma_3)=a(a+1)/(c+1),\qquad
\lambda(\Gamma_3)=\mu(\Gamma_3)+t-a-1=t^2+t-2a-2.
\tag{7}
\]

In particular \(a\le(t^2+t-2)/2\). These are necessary conditions, not constructions.

## 4. Elementary exact exclusions

### 4.1 Parity and a local independent-set bound

In the induced distance-\(h\) graph on a shell \(\Gamma_i(x)\), every vertex has degree \(p_{ih}^{i}\). Hence \(k_i p_{ih}^{i}\) is even. In particular \(ka_1\) is even.

The local graph at a vertex has \(k\) vertices and is \(a_1\)-regular. Greedily removing a chosen vertex and its neighbors yields an independent set of size at least
\(\alpha=\lceil k/(a_1+1)\rceil\).
For \(\alpha\) independent local vertices \(y_i\), their closed neighborhoods inside the local graph have size \(a_1+1\). Two such sets intersect in at most \(c_2-1\) vertices: the corresponding vertices are at distance two in the whole graph and have the central vertex as one common neighbor. The first two terms of inclusion-exclusion imply

\[
k\ge\alpha(a_1+1)-\binom\alpha2(c_2-1).
\tag{8}
\]

If \(c_2=1\), every local connected component is a clique: otherwise a shortest path of length two in that component gives two nonadjacent vertices with a common local neighbor, a contradiction. The clique size is \(a_1+1=a+t\), which must divide \(k=a+2t\). For \(a>0\), this lies strictly between \(a+t\) and \(2(a+t)\), so divisibility fails. Thus a primitive candidate must have \(c_2\ge2\).

### 4.2 Absolute bound used by the finite sieve

A connected strongly regular graph whose complement is connected has, in either nonprincipal eigenspace of dimension \(f\), a normalized spherical representation with two distinct off-diagonal inner products \(\rho,\sigma\), neither equal to one. One way to see injectivity is to express the idempotent as a linear combination of \(I,B,J\). Repeated projected vertices would be twins. Adjacent twins force a disjoint union of cliques in a strongly regular graph; nonadjacent twins force its complement to be a disjoint union of cliques. Both are excluded.

For each represented point \(u\), the polynomial
\((\langle u,z\rangle-\rho)(\langle u,z\rangle-\sigma)\)
vanishes on every other point and is nonzero at \(u\). These polynomials are linearly independent as functions on the point set. Quadratic polynomials restricted to the unit sphere in \(\mathbb R^f\) have dimension at most
\(1+f+f(f+1)/2-1=f(f+3)/2\). Therefore

\[
v\le f(f+3)/2.
\tag{9}
\]

For a primitive candidate here, the complement of each distance graph contains \(\Gamma\), so is connected. The distance graphs themselves are connected by the primitive hypothesis. Thus this bound applies to their nonprincipal spectral spaces, which may be sums of spaces in (2).

### 4.3 No primitive candidate with \(t\le3\)

Equation (6) with \(t=2\) and \(c\ge1\) leaves only \((a,c)=(2,5)\), giving array \(\{14,10,3;1,5,12\}\). Its distance-two graph would have 50 vertices and a nonprincipal eigenspace of dimension 7. Bound (9) gives \(50\le35\), impossible.

For \(t=3\), the range \(1\le a\le7\) in (6) with integral \(c\ge1\) leaves \((a,c)=(4,4),(5,9),(6,20),(7,55)\). The last two have negative \(\lambda(\Gamma_3)\) by (7). For \((5,9)\), the local graph has 35 vertices and degree 7, violating parity. For \((4,4)\), section 5 supplies an exact certificate. Consequently every connected/nondegenerate solution has \(t\ge4\) and \(c\ge2\).

## 5. Exact triple-intersection contradictions

Fix distinct base vertices \(x,y,z\) and let
\(X_{ijk}=|\{w:d(x,w)=i,d(y,w)=j,d(z,w)=k\}|\).
Every \(X_{ijk}\) is a nonnegative integer. Its three two-dimensional marginals are fixed by \(p_{ij}^h\). A coordinate with index zero is fixed by whether \(w\) equals one of the base vertices.

A further exact identity is

\[
q_{rs}^{u}=0\quad\Longrightarrow\quad
\sum_{i,j,k}Q_{ir}Q_{js}Q_{ku}X_{ijk}=0.
\tag{10}
\]

Here is a proof. Define
\(T(x,y,z)=\sum_w E_r(x,w)E_s(y,w)E_u(z,w)\).
Orthogonality of the idempotents gives

\[
\sum_{x,y,z}T(x,y,z)^2
=\sum_{v,w}E_r(v,w)E_s(v,w)E_u(v,w)
=\operatorname{tr}((E_r\circ E_s)E_u)
=q_{rs}^u\operatorname{rank}(E_u)/v.
\]

If the Krein parameter is zero, each real summand square is zero. Expanding the entries of each idempotent by the distance matrices gives (10).

The file `TRIPLE_CERTIFICATES.json` supplies rational linear combinations of these exact equations. `verify_triples.py` independently regenerates the equations from (2), computes their weighted sum with rational arithmetic, and checks that it is a nonnegative linear combination of the \(X\)'s with a strictly negative right side. It uses neither an LP solver nor floating-point arithmetic. It also verifies that the required base triangle exists: \(p_{d(x,z),d(y,z)}^{d(x,y)}>0\).

For example, with array \(\{19,12,5;1,4,15\}\), choose base distances
\((d(x,y),d(x,z),d(y,z))=(1,3,3)\). The certificate yields

\[
12X_{111}+6X_{113}+4X_{132}+3X_{311}+5X_{312}+3X_{333}=-3,
\]

which is impossible. For array \(\{17,8,6;1,2,12\}\) and base distances \((1,1,2)\), it yields

\[
10X_{113}+25X_{211}+X_{233}+4X_{313}+6X_{331}=-40.
\]

Three additional certificates exclude arrays
\(\{77,60,13;1,12,65\}\),
\(\{199,168,25;1,24,175\}\), and
\(\{83,54,21;1,6,63\}\).
All five pass the stated basic necessary-parameter sieve before these certificates are applied.

These are certificates of nonexistence for the five listed arrays, not certificates that all arrays have been excluded. No novelty is claimed.

## 6. Bounded-search interpretation

`verify_math.py` enumerates every integer pair \(2\le t\le30\), \(1\le a\le t^2-2\), forms the unique rational \(c\) in (6), and retains integral positive \(c\). There are 959 such parameter triples. It independently calculates all intersection numbers and Krein parameters using exact rational matrix inversion, checks valency and multiplicity integrality, nonnegativity, Q-polynomial orderings, shell parity, intersection-array monotonicity, (8), and (9). Exactly 159 parameter arrays survive this specified sieve. This number is before applying the five separately stored certificates or any published nonexistence results. The five listed certificates remove five of those arrays, leaving 154 survivors of these checks combined. A surviving array is only a necessary-parameter survivor.

For \(t\le6\), ten arrays survive that sieve. Three are removed by the included certificates (the 19-, 17-, and 77-valent arrays). The remaining seven include well-known published nonexistence cases; this report does not replace those papers' full proofs. The finite search has no implication for all \(t>30\), and no graph realizing a primitive survivor was constructed.

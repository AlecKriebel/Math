# Complete authored proof audit of greedy Ford-circle maximality

This is an AI-assisted, unrefereed proof-audit edition. Acceptance records an independent internal AI audit of Alper Ferudun's existing version 1.1 proof; it is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored mathematical reconstruction, every written formula and example, and all acceptance qualifications are retained. Executable code, raw computational datasets, copied source PDFs or text, source renderings, raw search responses, and private coordination material are not distributed. Historical finite checks support the written proof and cannot be reproduced from this edition alone.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey, or mathematical execution.

## Verdict and exact scope

**Accepted as a correct existing proof of the exact Propp–Kenyon target, subject to the explicit manuscript-status qualification below.** Alper Ferudun's version 1.1 of *The Ford-Circle Packing Has Maximum Area: An Answer to a Question of Propp and Kenyon*, dated 30 September 2026, proves the asserted global maximality. This audit found no mathematical defect or missing argument affecting Theorems 1.1 and 1.2. The reconstruction below supplies every essential geometric, compactness, induction, analytic, convergence, and countability step.

For the region bounded by the x-axis and the two unit disks with centers (-1,1) and (1,1), the maximum of the sum of disk areas, over all countable packings whose disks touch the x-axis and have pairwise disjoint interiors, is

\[
\boxed{\pi\left(\frac{\zeta(3)}{\zeta(4)}-1\right)
 =0.347543510672718666238146745405400598\ldots.}
\]

It is attained by the complete greedy family, consisting of the disks with radius 1/q² and base point 2p/q-1 for coprime integers 0<p<q. Boundary contacts are allowed. The two unit boundary disks are not part of the objective. “Complete” means that every recursively generated gap is eventually filled; a sequence that permanently neglects a gap need not contain the full family.

The proof also establishes the stronger theorem for any two tangent positive-radius disks resting on the same line: the greedy family maximizes the sum of r^α for every α>1, as well as the auxiliary weight and positive superpositions described below. No assertion of uniqueness, optimality without line tangency, or optimality for nontangent boundary disks is accepted here. The power sum of the greedy family diverges when α≤1; this is not a finite-value extension.

This is an audit of a prior author's mathematical contribution, not a claim to a newly discovered proof. The inspected manuscript calls itself unrefereed and discloses AI-assisted research, computation, proof development, and preparation. Zenodo hosting and the author's verification narrative do not establish journal peer review, external acceptance, or priority. The proof is accepted here because of the mathematical reconstruction, not because of that narrative.

## Sources and inspection

1. Günter Rote, collected open problems in *Discrete Differential Geometry*, Oberwolfach Report 13/2015, Problem 7 by Jim Propp and Richard Kenyon, printed page 722, PDF page 62. [Official report](https://ems.press/content/serial-article-files/46561), [DOI](https://doi.org/10.4171/OWR/2015/13). The entire relevant page was read as text and inspected visually. The displayed centers are (±1,1). The remaining 69 pages were not audited.
2. Alper Ferudun, *The Ford-Circle Packing Has Maximum Area: An Answer to a Question of Propp and Kenyon*, version 1.1, 30 September 2026. [Version DOI](https://doi.org/10.5281/zenodo.23049959), [public PDF](https://zenodo.org/api/records/23049959/files/OWR-13498-011-paper.pdf/content). All 12 pages were read and visually inspected. The full proof in Sections 2–6 was reconstructed; the verification and priority narratives on pages 10–12 were read but are not adopted as evidence.
3. [Official version metadata](https://zenodo.org/api/records/23049959). The retrieved metadata identifies version 1.1, the 30 September release date, and the unrefereed/AI-assisted status. Fresh web-tool attempts to reopen the record, DOI, and API during this audit failed; this audit uses the earlier same-day successful official API retrieval, not a claim of a new successful retrieval.

The exact inspected proof PDF is 150937 bytes, SHA-256 `85af3e938d3e1be3fff87541f231f02bdb16e1c1f18e062d6aa0ca65fafec9bc`. The exact original report PDF is 4345044 bytes, SHA-256 `e3ba6ef5fc327cfe1ca2c3c52a30d8107fbe487f832ae799f6ccd3e8e3da25ca`. The official metadata is 7388 bytes, SHA-256 `e2cab1f5ab082fa69e5d0a23f2472148c13422ce298c041bd2a0e03dd1751117`. The proof PDF was obtained from the official API at 02:48 UTC on 11 October 2026; metadata at 02:47 UTC. Local hashes were independently recomputed in this audit.

No source archive or author program was opened or executed. No author-provided numerical certificate was relied on. The mathematical statements below are an independently checked exposition of the cited proof strategy. They are not a reproduction of the source document.

## 1 Geometry and the class of admissible packings

Write a positive-radius disk resting on the x-axis as D(x,s), where its center is (x,s²) and its radius is s². Thus s is the square root of the radius. Two such disks have disjoint interiors precisely when

\[
(x-y)^2+(s^2-t^2)^2\geq(s^2+t^2)^2,
\qquad\text{equivalently}\qquad |x-y|\geq2st. \tag{1}
\]

Equality is external tangency. Distinct positive-size disks in a packing therefore have different base points.

Let the fixed boundary disks be A=D(x_A,a) and B=D(x_B,b), with a,b>0 and x_B-x_A=2ab. An admissible gap disk has x_A<x<x_B and disjoint interior from A and B. Its two boundary constraints are

\[
x-x_A\geq2as,\qquad x_B-x\geq2bs. \tag{2}
\]

Their sum gives s≤c:=ab/(a+b). There is exactly one disk attaining this size: both constraints must be equalities, giving x=x_A+2ac. It touches both boundaries and produces two new tangent gaps. This proves the local greedy insertion rule and its uniqueness without assuming global optimality.

For the original unit-disk problem put

\[
\beta(u)=1-\sqrt{1-(1-|u|)^2},\qquad
T=\{(u,v): |u|<1,\ 0<v<\beta(u)\}.
\]

The graph of β is the lower exposed boundary of the two disks above the base interval. The open set T is connected. In the upper half-plane with the two closed unit disks removed, T is both open and closed: its boundary in the upper half-plane belongs to the two disks, and β tends to zero at ±1. Hence T is a connected component of that complement.

A gap disk with -1<x<1 has open interior disjoint even from the closed boundary disks, by the center-distance criterion. It contains (x,ε) for every sufficiently small ε>0, including a point of T. Its connected interior must therefore stay in T. Conversely, a disk with interior in T has its center in T, hence -1<x<1, and avoids both boundary disks. Thus the algebraic gap class is exactly the stated geometric class, not a relaxation of it. Taking closures also puts the entire closed disk in the closure of T.

Any disjoint-interior family of positive-radius disks in the plane is at most countable: assign to each open interior its first point from a fixed enumeration of the rational points of the plane. These assigned points are distinct. For a countable family, the sum of disk areas equals the area of its union because disk boundaries have measure zero. Finite families are included, although the original question requests an infinite maximizing family.

## 2 The complete greedy family and its exact value

For a nonzero pair v=(m,n) of nonnegative integers define

\[
s_v=(m/a+n/b)^{-1},\qquad x_v=x_A+2an s_v.
\]

The vectors (1,0) and (0,1) give A and B. Direct subtraction yields

\[
x_{v'}-x_v=2(mn'-m'n)s_vs_{v'}. \tag{3}
\]

When det(v,v')=1, the corresponding disks form a tangent gap, and v+v' gives its unique greedy disk: its reciprocal size is the sum of the reciprocal endpoint sizes, and both new determinants are 1. Every vector generated this way is primitive, since a common divisor of the coordinates of v+v' would divide det(v,v')=1.

For completeness, every primitive (m,n) with m,n>0 occurs. Within any determinant-one interval with endpoints u,v, a primitive integer vector strictly between their rays has a unique expression Au+Bv with positive integer A,B. Initially A=m and B=n. If A=B then primitivity implies A=B=1, so the vector is the inserted mediant. If A>B, replace the interval by (u,u+v); the coefficients become (A-B,B). If B>A, replace it by (u+v,v); the coefficients become (A,B-A). The sum of the positive coefficients strictly decreases until the mediant case occurs. This also gives uniqueness: the two child ray intervals have disjoint interiors and meet only at their newly inserted vector.

Distinct positive primitive vectors have nonzero integer determinant, so (3) and (1) imply pairwise disjoint interiors. Relative to the fixed boundaries,

\[
x_v-x_A=2an s_v>0,\qquad x_B-x_v=2bm s_v>0,
\]

and (3) again gives disjointness. Therefore the generated configuration really is a packing; it is not merely a list of candidate radii.

Define

\[
w(0)=0,\qquad w(s)=\frac{1}{e^{1/s}-1}
 =\sum_{d\geq1}e^{-d/s}\quad(s>0).
\]

This function is continuous at zero, positive and strictly increasing for s>0. With c=ab/(a+b), elementary fraction arithmetic gives

\[
w(c)\bigl(1+w(a)+w(b)\bigr)=w(a)w(b). \tag{4}
\]

All summands are nonnegative, so the primitive-pair decomposition (M,N)=d(m,n) can be used without conditional-convergence issues. It gives

\[
\begin{aligned}
\sum_{D\in G(A,B)}w(s_D)
 &=\sum_{\substack{m,n\geq1\\(m,n)=1}}\sum_{d\geq1}
    e^{-d(m/a+n/b)}\\
 &=\sum_{M,N\geq1}e^{-M/a-N/b}=w(a)w(b). \tag{5}
\end{aligned}
\]

For p>0 let

\[
G_p(a,b)=\sum_{\substack{m,n\geq1\\(m,n)=1}}(m/a+n/b)^{-p}.
\]

The inequalities

\[
\frac{m+n}{\max(a,b)}\leq\frac ma+\frac nb
 \leq\frac{m+n}{\min(a,b)}
\]

reduce convergence to a=b=1. There are φ(q) primitive pairs with m+n=q, hence G_p(1,1)=Σ_{q≥2}φ(q)q^{-p}. For p>2 it converges by φ(q)<q. At p=2 the unrestricted double sum is

\[
\sum_{m,n\geq1}(m+n)^{-2}=\sum_{q\geq2}(q-1)q^{-2}=\infty.
\]

Primitive decomposition makes this unrestricted sum ζ(2)G_2(1,1) in the extended nonnegative sense. Since ζ(2)<∞, G_2(1,1)=∞. For 0<p≤2 comparison gives divergence too. This proves the threshold without needing a separate theorem about reciprocal primes. For p≤0 infinitely many sizes tend to zero, so the corresponding power sum also diverges.

The elementary divisor identity Σ_{d|n}φ(d)=n follows by sorting the integers 1,…,n according to their gcd with n. For p>2 its absolutely convergent Dirichlet-series consequence is

\[
\zeta(p)\sum_{q\geq1}\frac{\varphi(q)}{q^p}=\zeta(p-1),
\qquad G_p(1,1)=\frac{\zeta(p-1)}{\zeta(p)}-1. \tag{6}
\]

Thus the claimed candidate area and all convergence statements are correct. What remains is the comparison with arbitrary packings.

## 3 An analytic inequality valid at every scale

The key assertion is that, for each ρ>0,

\[
f_\rho(\lambda)=1+w(e^\lambda-\rho)+w(\rho),
\qquad \lambda>\log\rho,
\]

has convex logarithm. We verify this algebraically with an all-degree sign argument.

Put s=e^λ-ρ. Chain differentiation gives

\[
f_\rho f_\rho''-(f_\rho')^2=(s+\rho)\Psi(s,\rho),
\]

where

\[
\Psi=(1+w(s)+w(\rho))\bigl(w'(s)+(s+\rho)w''(s)\bigr)
 -(s+\rho)w'(s)^2. \tag{7}
\]

Set q=1/s, x=1/ρ, E=e^q, X=e^x. All are positive, and E,X>1. Since d/ds=-q² d/dq,

\[
w'(s)=\frac{q^2E}{(E-1)^2},\qquad
w''(s)=\frac{q^3E\{q(E+1)-2(E-1)\}}{(E-1)^3}.
\]

Writing

\[
P=x(E-1)+(q+x)\{q(E+1)-2(E-1)\},
\]

substitution in (7), with common denominators, gives

\[
\Psi=\frac{q^2E}{x(X-1)(E-1)^4}\Omega,
\quad
\Omega=\{E(X-1)+E-1\}P-q(q+x)E(X-1). \tag{8}
\]

All factors outside Ω in (8) are strictly positive. The useful decomposition is

\[
\Omega=x(X-1)U_1+(X-1)U_2+xU_3+U_4,
\]

with

\[
\begin{aligned}
U_1&=qe^{2q}-e^{2q}+e^q,\\
U_2&=q^2e^{2q}-2qe^{2q}+2qe^q,\\
U_3&=qe^{2q}-e^{2q}+2e^q-q-1,\\
U_4&=q^2e^{2q}-2qe^{2q}+4qe^q-q^2-2q.
\end{aligned} \tag{9}
\]

These formulas follow by expanding (8); they have also been independently checked symbolically. Individual U_j need not all have nonnegative coefficients, so it is important to combine them in the required manner.

Expanding in x gives

\[
\Omega(q,x)=\sum_{n\geq0}\omega_n(q)\frac{x^n}{n!},\qquad
\omega_0=U_4,\quad \omega_1=U_2+U_3,\quad
\omega_n=nU_1+U_2\ (n\geq2). \tag{10}
\]

For m≥2, the coefficients multiplied by m! are

\[
\begin{aligned}
m![q^m]U_1&=(m-2)2^{m-1}+1,\\
m![q^m]U_2&=m\bigl((m-5)2^{m-2}+2\bigr),\\
m![q^m]U_3&=(m-2)2^{m-1}+2.
\end{aligned}
\]

For U_4 the coefficient at m=2 is zero and, for m≥3,

\[
m![q^m]U_4=m\bigl((m-5)2^{m-2}+4\bigr).
\]

Every U_j has zero coefficients at m=0,1. These statements follow term by term from
m![q^m](q^j e^{cq})=m!c^{m-j}/(m-j)! when m≥j, and zero otherwise. Consequently:

- For n=0, the coefficients vanish through m=4 and are positive for every m≥5. At m=5 the coefficient is 20/5!=1/6.
- For n=1 and m≥2, the coefficient multiplied by m! is (m+1)((m-4)2^{m-2}+2). It vanishes for m=2,3 and is positive for every m≥4.
- For n≥2, nonnegativity of every coefficient of U_1 reduces the lower bound to n=2. Its m≥2 coefficient multiplied by m! is 2^{m-2}(m²-m-8)+2(m+1). This is zero at m=2, equals 4 at m=3, and is positive for every m≥4 because m²-m-8≥4 there.

Thus every coefficient in (10) is nonnegative. The exponential-polynomial expressions are entire, so these are convergent expansions, not merely formal signs. For q,x>0,

\[
\Omega(q,x)\geq U_4(q)\geq q^5/6>0. \tag{11}
\]

Equations (7)–(11) prove strict log-convexity everywhere on the stated open domain. In particular ordinary log-convexity, the exact property needed below, holds for all positive sizes. No finite coefficient cutoff or numerical sampling is used to conclude this universal inequality.

## 4 The weighted tangent chain inequality

A k-chain consists of fixed A=C_0, positive-size internal disks C_1,…,C_k, and B=C_{k+1}, in increasing order of base point, with every consecutive pair tangent and all interiors disjoint. Write s_0=a, s_{k+1}=b. The positions are determined by the sizes. Exactly the following conditions are required:

\[
\sum_{\ell=0}^{k}s_\ell s_{\ell+1}=ab, \tag{12}
\]

\[
\sum_{\ell=i}^{j-1}s_\ell s_{\ell+1}\geq s_i s_j
\quad(j\geq i+2), \tag{13}
\]

excluding (i,j)=(0,k+1), already handled by (12). Define the algebraic chain value

\[
\Phi=\sum_{i=1}^{k}w(s_i)+\sum_{i=0}^{k}w(s_i)w(s_{i+1}). \tag{14}
\]

We prove Φ≤w(a)w(b) by induction on k, uniformly for all positive boundary sizes. Only the algebraic quantity (14) is needed; the proof does not require an unproved assertion that all gap fillings remain disjoint from every other filling.

For k=1, (12) forces s_1=ab/(a+b), so (4) gives equality.

Call a chain degenerate if equality occurs in (13). For such a pair i,j, the subchain from C_i to C_j lies in a tangent gap and has j-i-1 internal disks. Removing those internal disks leaves an outer chain with k-j+i+1 internal disks. Because j≥i+2 and the two fixed endpoints were excluded, both numbers lie between 1 and k-1. The original base points and inequalities prove that both new chains are admissible. Direct accounting in (14) gives

\[
\Phi=\Phi_{\rm inner}+\Phi_{\rm outer}-w(s_i)w(s_j).
\]

The inductive bounds immediately yield Φ≤w(a)w(b). This covers all possible additional contacts, including contacts between an internal disk and either fixed endpoint.

Now take a nondegenerate chain with k≥2. Hold C_0,C_3,…,C_{k+1} fixed and vary C_1,C_2. Put

\[
L=s_0s_1+s_1s_2+s_2s_3>0,\qquad
K=L+s_0s_3=(s_1+s_3)(s_2+s_0).
\]

On I=(log s_3,log(K/s_0)) use

\[
s_1(\theta)=e^\theta-s_3,\qquad
s_2(\theta)=Ke^{-\theta}-s_0. \tag{15}
\]

The sizes stay positive and the three-term sum L stays fixed. Thus (12) is preserved. Every inequality (13) whose two endpoints avoid indices 1 and 2 is constant along the move: its sum contains either all three terms of L or none. Keeping L fixed also keeps the base points of C_3 and every later disk fixed.

Let F be the subset of I on which all inequalities (13) hold. It is relatively closed in I. At the left endpoint, s_1 tends to zero and s_2 tends to L/s_3>0, so the constraint for the pair (0,2),

\[
s_0s_1+s_1s_2-s_0s_2\geq0,
\]

has negative limit. At the right endpoint, s_2 tends to zero and s_1 tends to L/s_0>0, so the constraint for (1,3),

\[
s_1s_2+s_2s_3-s_1s_3\geq0,
\]

has negative limit. Both pairs are among (13), also when k=2. Continuity therefore excludes neighborhoods of both ends of I; F is compact in the real line. The initial parameter θ*=log(s_1+s_3) has a feasible neighborhood because the chain is nondegenerate and there are finitely many strict constraints. Its connected component in F is a nontrivial closed interval J=[θ_-,θ_+]. A closed subset of the real line has interval components, so no global convexity of F is being assumed.

At each endpoint of J some varying inequality (13) must be an equality. Otherwise all those finitely many inequalities would stay strict nearby while the other constraints stay unchanged, extending the component. Thus both endpoint chains are degenerate and satisfy the already proved bound.

Only the following part of Φ changes:

\[
h=w(s_1)+w(s_2)+w(s_0)w(s_1)+w(s_1)w(s_2)+w(s_2)w(s_3).
\]

Its exact factorization is

\[
h=(1+w(s_1)+w(s_3))(1+w(s_2)+w(s_0))
 -(1+w(s_0))(1+w(s_3)). \tag{16}
\]

The first factor is f_{s_3}(θ); the second is f_{s_0}(log K-θ). Section 3 proves both positive and log-convex in θ, since affine precomposition preserves convexity of the logarithm. Their product is log-convex and hence convex: for smooth positive g, g''=g((log g)''+((log g)')²)≥0. Subtracting the constant in (16) preserves convexity. Consequently Φ along J never exceeds its maximum endpoint value. Both endpoints are already bounded by w(a)w(b), proving the chain inequality for the original nondegenerate chain and completing the induction.

## 5 From finite maximizers to every countable packing

Let V_n(a,b) be the supremum of Σw(s_D) over gap packings containing at most n disks. Prove V_n≤w(a)w(b) by induction on n, simultaneously for all a,b>0. The case n=0 is immediate.

A maximizing configuration exists. Permit n labelled pairs (x_i,s_i) with x_i in the closed base interval and 0≤s_i≤c. Impose (2) and all inequalities |x_i-x_j|≥2s_i s_j. These are closed constraints in a compact box. The continuous function Σw(s_i) therefore reaches a maximum. Its positive-size entries give a valid packing with distinct base points. Conversely, any at-most-n packing is represented by padding with zero-size entries at x_A. Thus this compact maximum is exactly V_n; no compactness of a space of infinite packings is assumed.

If the maximizing packing has fewer than n positive disks, induction applies immediately. Otherwise consider one of its disks D(x,s). It must touch some disk to its right, counting B. If not, let η>0 be the smallest slack x_E-x-2ss_E over the finitely many disks E to its right, including B. Let S be the largest size in the packing together with A,B. Choose 0<δ<η/2 and replace D by

\[
D\bigl(x+\delta,s+\delta/(2S)\bigr).
\]

For a disk to the left, the separation grows by δ, whereas the required separation 2ss_E grows by δs_E/S≤δ. For a disk to the right, the new slack is at least η-δ-δs_E/S≥η-2δ>0. The new configuration therefore remains a gap packing with the same number of disks and the same order of base points. In particular the boundary inequalities force the enlarged size to remain admissible. The weight strictly increases, contradicting maximality. Reflecting the argument gives a tangent neighbor to the left, counting A. A neighbor here need not be the immediately adjacent disk in base-point order; the argument does not assume that stronger statement.

Start at any maximizing disk and follow leftward tangencies. Finiteness and strict decrease of base points force the path to finish at A. A rightward tangent path from the same disk ends at B. Combining the paths yields a chain with 1≤k≤n internal disks. Its members are pairwise disjoint because they were selected from the packing.

Every remaining disk has base point in exactly one consecutive chain interval. The disks in that interval are a packing of the corresponding tangent gap and number at most n-k≤n-1. The induction hypothesis bounds their total weight by w(s_i)w(s_{i+1}). Summing the residual contributions and the chain-disk weights gives

\[
V_n(a,b)\leq\Phi\leq w(a)w(b).
\]

The chain inequality was proved independently in Section 4, so these two inductions are not circular. Finally, every finite subfamily of an arbitrary countable packing is an admissible finite packing. Nonnegativity implies that the full sum is the supremum of all finite subsums. Therefore

\[
\sum_{D\in P}w(s_D)\leq w(a)w(b)
 =\sum_{D\in G(A,B)}w(s_D). \tag{17}
\]

This establishes the full infinite-packing theorem for the auxiliary weight; it is not restricted to saturated packings, chain packings, finite packings, or packings with rational base points.

## 6 Conversion to radius powers and the area theorem

For t>0 the Euclidean homothety (u,v)↦(u/t²,v/t²) sends sizes s to s/t, preserving all tangency and nonoverlap conditions. Applying (17) to this rescaled gap yields

\[
\sum_{D\in P}w(s_D/t)\leq w(a/t)w(b/t). \tag{18}
\]

For p>1, the nonnegative exponential series and the gamma integral give

\[
\int_0^\infty t^{p-1}w(s/t)\,dt
 =\sum_{d\geq1}\Gamma(p)(s/d)^p
 =\Gamma(p)\zeta(p)s^p. \tag{19}
\]

Let p>2. Integrate (18) against t^{p-1}dt. All exchanges of sums and integrals use nonnegative terms. On the right, expansion of the product and primitive decomposition give

\[
\begin{aligned}
\int_0^\infty t^{p-1}w(a/t)w(b/t)\,dt
 &=\Gamma(p)\sum_{M,N\geq1}(M/a+N/b)^{-p}\\
 &=\Gamma(p)\zeta(p)G_p(a,b)<\infty.
\end{aligned}
\]

On the left, (19) gives Γ(p)ζ(p)Σs_D^p. The positive finite factor Γ(p)ζ(p) can be divided out, giving

\[
\sum_{D\in P}s_D^p\leq G_p(a,b)
 =\sum_{D\in G(A,B)}s_D^p<\infty. \tag{20}
\]

Set p=2α and use s²=r. This proves the general radius-power theorem for every α>1. In the unit gap, set p=4, multiply by π, and use (6). The greedy disks themselves form an infinite admissible packing, so the upper bound is attained. This proves the exact area-maximization statement.

More generally, if μ is any positive Borel measure on (0,∞), set W(s)=∫w(s/t)dμ(t), allowing +∞. Integrating (18) and using (5) at scale t gives the claimed extended-value inequality for ΣW(s_D). Countable sums may be exchanged with integrals by monotone convergence, which does not require an unstated σ-finiteness assumption on μ. The manuscript's reference to Tonelli in this corollary can be read as this elementary nonnegative-sum argument; no theorem-changing amendment is necessary.

The restriction on weights matters. In the unit gap four disks of size 1/3 can have base points -1/3,-1/9,1/9,1/3. Each consecutive distance is 2/9; the two outer boundary distances are 2/3; all nonconsecutive inequalities also hold. They give weight 4 for W(s)=1_{s≥1/3}, while the greedy family has only φ(2)+φ(3)=3 qualifying disks. Thus arbitrary nondecreasing weights are not covered.

## 7 Audit findings and acceptance limits

The following potentially delicate points have all been discharged in the preceding reconstruction:

- the precise bounded region, including the unit-disk centers and permitted boundary contacts;
- countability and the equality of the area sum with union area;
- greedy-family completeness and pairwise disjointness, not just its radii;
- convergence and the exact zeta value;
- compact finite optimization with zero-size padding;
- the two-sided contact property without assuming a priori saturation;
- chain extraction, residual-gap allocation, and the noncircular pair of inductions;
- degenerate-chain splits with both induction parameters strictly smaller;
- a feasible closed deformation component whose endpoints cannot escape by vanishing sizes;
- the k=2 endpoint case, additional endpoint contacts, and possibly disconnected feasible sets;
- the constant in the two-factor objective decomposition;
- the analytic inequality for all positive variables via coefficients of every degree;
- countable and integral limits using nonnegative summands.

**Missing step:** none identified for the accepted scope. The additional elementary details above are explanations of valid implicit steps, not repairs of a false theorem. No uniqueness result is inferred from strict log-convexity of a local deformation; equality in arbitrary infinite packings is a separate matter.

The historical authored supplementary checker, which is not distributed in this edition, independently derived the derivative identities and Ω decomposition, checked the chain accounting identities, expanded coefficients through degree 200 in each variable, and checked exact rational geometry in six nonuniform gaps through m+n≤24. It reported 242391 successful checks. Its decimal area evaluation is illustrative. Finite testing is not the proof of the all-degree inequality, chain deformation, countable reduction, or theorem. No author verification program, optimizer output, or self-assessment enters the acceptance argument.

The result should be described as an independently audited proof in a publicly available unrefereed preprint. The report does not certify formal journal review, uniqueness, priority over every possible earlier source, or correctness of unrelated literature-search claims. The dated preprint and its verified exact theorem supersede an older “open” literature assessment only for the mathematical target audited here.

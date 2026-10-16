# Residual all-center non-tightness at nonboundary ranks

Independent scientific audit of the newly assembled category consequence for PR166. This is an unrefereed, checkable deduction. Historical disclosure and novelty are unestablished. The proof addresses the exact singleton-stopping cost, independent input strings, and the stationary source

\[
\mu=(1/2,1/2),\qquad P=\begin{pmatrix}3/4&1/4\\1/4&3/4\end{pmatrix}.
\tag{1}
\]

## Theorem and precise quantifiers

There exists a set \(R\subset(0,1)\) which is a dense \(G_\delta\) in the ambient interval and consists entirely of irrational nonboundary ranks, such that

\[
\forall t\in R\quad \forall(c_n)\in\mathbb R^{\mathbb N}\quad
\left(\frac{Y_n(\lfloor nt\rfloor+1)-c_n}{\sqrt n}\right)_{n\ge1}
\quad\hbox{is not tight.}
\tag{2}
\]

Every \(t\in R\) is a continuity point of the first-order rank profile \(g=m\circ h\). More precisely, for every real \(L\ge0\) and every deterministic center sequence,

\[
\limsup_{n\to\infty}
\mathbb P\bigl(|Y_n(\lfloor nt\rfloor+1)-c_n|>L\sqrt n\bigr)\ge1/4.
\tag{3}
\]

The same set \(R\) works for all deterministic center sequences, including centers chosen as functions of the fixed rank \(t\) and the sample size. The centers cannot depend on the realized random sample. The theorem is an existence and category statement, not an explicit description of every bad rank, not membership of the candidate's square-word rank in \(R\), and not a Lebesgue-almost-everywhere classification.

## 1. Coding, cost, and measurability

Write \(q=3/4\) and \(r=1/4\). For a nonempty finite binary word \(w=w_1\ldots w_d\), set

\[
\pi(w)=\frac12\prod_{j=1}^{d-1}p_{w_jw_{j+1}},\qquad \pi(\varnothing)=1.
\tag{4}
\]

Recursively partition \([0,1]\) into lexicographically ordered cylinder intervals \(I(w)\) with lengths \(\pi(w)\). Both child proportions are strictly positive. For \(d\ge1\),

\[
\max_{|w|=d}|I(w)|\le\tfrac12q^{d-1}\longrightarrow0.
\tag{5}
\]

Let \(D\) be all their endpoints in \((0,1)\). It is countable. Every depth-\(d\) endpoint is a finite sum of rational cylinder probabilities, so \(D\subset\mathbb Q\). Away from \(D\), the nested cylinders determine a unique infinite code \(h(u)\). Assign arbitrary consistent endpoint codes; these affect no uniform-sample probability. The coding is measurable because each finite prefix has a cylinder preimage, and it preserves order away from the endpoints. Independent uniforms \(U_1,\ldots,U_n\) give independent strings \(S_i=h(U_i)\) with source (1), and almost surely

\[
S_{(k)}=h(U_{(k)}),\qquad 1\le k\le n.
\tag{6}
\]

For an infinite string \(s\), with length-\(d\) prefix \(s^{(d)}\), define

\[
m(s)=\sum_{d\ge0}\pi(s^{(d)}),\quad
\Lambda_{n,d}(s)=\#\{i:s^{(d)}\preceq S_i\},\quad
Z_n(s)=\sum_{d\ge0}\Lambda_{n,d}(s)\mathbf1_{\{\Lambda_{n,d}(s)>1\}}.
\tag{7}
\]

The exact singleton-stopping selection cost is

\[
Y_n(k)=Z_n(S_{(k)}).
\tag{8}
\]

In particular, a singleton contributes zero at that and every deeper level. These are the definitions of Leckey-Neininger-Sulzbach (LNS), equations (2)-(3). No modified continuation cost is substituted.

The sums defining \(m\) converge uniformly by (5). If two codes share a nonempty prefix \(w\), their common profile sum through \(w\) cancels, and each remaining tail lies in \([0,3\pi(w)]\). Therefore

\[
|m(s)-m(s')|\le3\pi(w).
\tag{9}
\]

At a point \(t\notin D\), all sufficiently close \(u\notin D\) share any prescribed prefix of \(h(t)\). Equation (9) proves continuity of \(g=m\circ h\) at every nonboundary point; the same conclusion holds with any consistent endpoint coding because endpoint codes near a fixed nonboundary point share that prefix as well.

All fixed-prefix counts are measurable. Distinct input strings occur almost surely: the probability that a given pair shares a depth-\(d\) prefix is at most the right side of (5), tending to zero. A finite sample thus has a finite largest pairwise common-prefix length almost surely. Consequently every \(Y_n(k)\) is a finite, integer-valued measurable random variable. This also follows directly by selecting the measurable uniform order statistic in (6). Nothing below requires a possibly nonmeasurable random supremum over strings.

## 2. Direct uniform first-order control for the exact cost

For \(n\ge2\), let

\[
H_n=\left\lceil\frac{5\log n}{\log(4/3)}\right\rceil+1,
\quad d_n=\sqrt{\frac{2\log n}{n}}+n^{-2},
\quad D_n=\sup_{x\in[0,1]}|F_n(x)-x|,
\tag{10}
\]

where \(F_n\) is the uniform empirical distribution function. For a Bernoulli variable \(B\), the second derivative of the log moment-generating function of \(B-\mathbb EB\) is a tilted Bernoulli variance, at most \(1/4\). Its value and derivative at zero vanish. Integrating this bound twice gives \(\log\mathbb E e^{s(B-\mathbb EB)}\le s^2/8\) for all real \(s\). Exponential Markov bounds and optimization yield

\[
\mathbb P(|F_n(x)-x|>\epsilon)\le2e^{-2n\epsilon^2}.
\tag{11}
\]

A union bound over the \(n^2+1\) points \(j/n^2\), followed by monotonicity between adjacent points, gives

\[
\mathbb P(D_n>d_n)\le4n^{-2}.
\tag{12}
\]

The probability that some pair shares a prefix of length \(H_n\) is at most

\[
{n\choose2}\sum_{|w|=H_n}\pi(w)^2
\le\frac{n^2}{4}q^{H_n-1}\le\frac1{4n^3}.
\tag{13}
\]

On the complement of this collision event, every bucket of depth \(H_n\) contains at most one string; hence every term of \(Z_n(s)\) at depth \(H_n\) or greater is zero, simultaneously for all \(s\). The samples avoid the countable set \(D\) almost surely. Each cylinder count then differs from \(n\) times its interval length by at most \(2nD_n\), regardless of endpoint convention. Replacing an integer count by its singleton-truncated value changes it by at most one. Finally,

\[
\sum_{d\ge H_n}\pi(s^{(d)})\le2q^{H_n-1}\le2n^{-5}.
\tag{14}
\]

Thus a measurable event \(G_n\) of probability at least \(1-4n^{-2}-(4n^3)^{-1}\) implies, deterministically and simultaneously for all \(s\),

\[
|Z_n(s)-nm(s)|\le R_n:=2nH_nd_n+H_n+2n^{-4},
\qquad R_n/n\longrightarrow0.
\tag{15}
\]

The empirical-grid/collision control is also present in the authorized candidate. The inequalities above were checked directly, including the singleton subtraction and the infinite tail. Only \(o_{\mathbb P}(n)\) is needed for this deduction, although (15) gives the stronger order \(O_{\mathbb P}(\sqrt n(\log n)^{3/2})\). In particular, substituting the random selected string into the simultaneous deterministic implication is legitimate, and

\[
Y_n(k)/n-m(h(U_{(k)}))\longrightarrow0\quad\hbox{in probability},
\tag{16}
\]

uniformly in the rank index. This proof does not appeal to tightness of a process or evaluate a Skorokhod limit at a discontinuity.

## 3. A directly verified dense set of jumping boundaries

For every nonempty finite word \(W\), let \(\tau_W\) be the interior split of \(I(W)\) into \(I(W0)\) and \(I(W1)\). The adjacent endpoint codes are

\[
\ell_W=W0\,111\ldots,\qquad u_W=W1\,000\ldots.
\tag{17}
\]

Both have rank \(\tau_W\). Set \(T_W=\sum_{d=0}^{|W|}\pi(W^{(d)})\), and let \(i\) be the last symbol of \(W\). Geometric summation, using the change probability \(r=1-q\), gives

\[
A_W:=m(\ell_W)=T_W+\pi(W)p_{i0}\left(1+\frac r{1-q}\right)
=T_W+2\pi(W)p_{i0},
\tag{18}
\]

\[
B_W:=m(u_W)=T_W+\pi(W)p_{i1}\left(1+\frac r{1-q}\right)
=T_W+2\pi(W)p_{i1}.
\tag{19}
\]

Consequently

\[
A_W-B_W=\begin{cases}\pi(W),&i=0,\\-\pi(W),&i=1.\end{cases}
\tag{20}
\]

Both masses are strictly positive, so each of these jumps is nonzero. The root split, with \(W=\varnothing\), has zero jump because \(\mu_0=\mu_1\); it is intentionally excluded. Let

\[
B=\{\tau_W:W\text{ is a nonempty finite word}\}\subset D.
\tag{21}
\]

This countable set is dense in \((0,1)\). Indeed, in any nonempty open interval \(J\subset(0,1)\), choose \(t\in J\setminus D\). By (5), a sufficiently deep cylinder containing \(t\) has its entire closed interval inside \(J\). Its internal split belongs to \(B\cap J\).

For completeness the one-sided profile limits at \(\tau_W\) are \(A_W\) and \(B_W\). For every fixed positive integer \(K\), the cylinder \(W0\,1^K\) ends at \(\tau_W\), and \(W1\,0^K\) begins there. Their positive widths shrink to zero as \(K\) grows. For \(u\) close enough on the respective side, its code shares that prefix with \(\ell_W\) or \(u_W\). Equation (9) bounds the profile difference by three times that cylinder's mass, which tends to zero as \(K\to\infty\). Thus, with a right-continuous endpoint convention, \(g(\tau_W-)=A_W\) and \(g(\tau_W)=B_W\).

The endpoint summations and dense jump mechanism have established antecedents in LNS Propositions 2.1, 2.9 and 2.10. Equations (18)-(21) independently verify the precise special source needed here; no general classification hypothesis is imported without checking it.

## 4. Direct boundary limit and uniform concentration over moving centers

Fix \(b=\tau_W\in B\), put \(k_n=\lfloor nb\rfloor+1\), and let \(V_n=U_{(k_n)}\). For every fixed \(\epsilon>0\) within the interval, the binomial law of the number of uniforms below \(b\pm\epsilon\) shows that \(V_n\to b\) in probability. Its exact side probability is

\[
\mathbb P(V_n<b)=\mathbb P(\operatorname{Bin}(n,b)\ge k_n)
\longrightarrow1/2,
\tag{22}
\]

because \(0<k_n-nb\le1\), \(b(1-b)>0\), and the classical binomial CLT applies. Each \(V_n\) has a continuous distribution, so equality with \(b\) has probability zero. Both sides have limiting mass one-half.

The one-sided limits from Section 3 imply

\[
m(h(V_n))-\left(A_W\mathbf1_{\{V_n<b\}}+B_W\mathbf1_{\{V_n>b\}}\right)
\longrightarrow0\quad\hbox{in probability}.
\tag{23}
\]

Combining (16), (22), and (23) proves

\[
\frac{Y_n(\lfloor nb\rfloor+1)}n\ \Rightarrow\
\frac12\delta_{A_W}+\frac12\delta_{B_W},\qquad A_W\ne B_W.
\tag{24}
\]

This is the \(\beta=0\) boundary mixture of LNS Proposition 2.5, proved directly here with the actual cost. Their Proposition 2.8's random-centering limit is not an input to this proof.

Now fix \(M>0\), and define

\[
C_n(t,M)=\sup_{a\in\mathbb R}
\mathbb P\bigl(|Y_n(\lfloor nt\rfloor+1)-a|\le M\sqrt n\bigr).
\tag{25}
\]

Take \(0<\eta<|A_W-B_W|/4\). In units of \(Y_n/n\), the two closed bands \([A_W-\eta,A_W+\eta]\) and \([B_W-\eta,B_W+\eta]\) have positive separation and, by (24), each has probability tending to \(1/2\). Their endpoints are continuity points of the limiting law. Any interval of length \(2M/\sqrt n\) intersects at most one band for all sufficiently large \(n\). It misses at least one band of probability \(1/2-o(1)\). This applies to every interval center, including centers changing with \(n\); hence

\[
\limsup_{n\to\infty}C_n(b,M)\le1/2.
\tag{26}
\]

This explicit separated-band argument is essential: weak convergence tested at a fixed center would not alone justify an uncountable supremum over centers.

## 5. Relative continuity and nowhere density

Let

\[
X=(0,1)\setminus(D\cup\mathbb Q)=(0,1)\setminus\mathbb Q.
\tag{27}
\]

The complement removed is countable. The space \(X\) is dense, is an ambient \(G_\delta\), and is a Baire space: \((0,1)\) is Polish and its \(G_\delta\) subspaces are completely metrizable. The argument would also work if \(D\) were not rational, provided the countable union was removed.

For fixed \(n\), the rank \(k=\lfloor nt\rfloor+1\) is constant on each half-open rank cell

\[
I_{n,j}=[j/n,(j+1)/n),\qquad 0\le j<n.
\tag{28}
\]

Every point of \(X\) avoids all endpoints \(j/n\). Thus \(C_n(\cdot,M)\) is locally constant on \(X\). Its value is a deterministic number in \([0,1]\). The probability inside the supremum is well defined by Section 1; alternatively, because the cost is integer-valued, the supremum can be taken over the countable family of intervals \([j,j+2M\sqrt n]\), \(j\in\mathbb Z\). Any real interval containing integers is contained, as regards its integer points, in one of this family. There is no random supremum here, and the function of \(t\) is measurable as a finite-valued rank-cell function. In particular, for each fixed \(n,M\),

\[
A_{n,M}:=\{t\in X:C_n(t,M)\ge3/4\}
\tag{29}
\]

is both open and closed in \(X\).

For positive integers \(M,N\), define

\[
E_{M,N}=\bigcap_{n\ge N}A_{n,M}.
\tag{30}
\]

It is closed in \(X\). To prove it nowhere dense, start with an arbitrary nonempty relatively open \(U\subset X\). There is an open ambient interval \(J\subset(0,1)\) with \(J\cap X\) nonempty and contained in \(U\). Choose \(b\in B\cap J\), which is possible by (21). By (26), every sufficiently large \(n\) satisfies \(C_n(b,M)<3/4\). Choose such an \(n\ge N\) also satisfying

\[
1/n<\operatorname{dist}(b,(0,1)\setminus J).
\tag{31}
\]

Writing \(j=\lfloor nb\rfloor\), the right-hand interval

\[
V=(b,(j+1)/n)\cap X
\tag{32}
\]

is nonempty, relatively open, and contained in \(U\). Its length before deleting the countable set is positive even when \(nb\) is an integer: in that case \(b=j/n\) is the rank cell's included left endpoint. Every \(t\in V\) has \(\lfloor nt\rfloor+1=j+1=\lfloor nb\rfloor+1\), so \(C_n(t,M)=C_n(b,M)<3/4\). Thus \(V\cap E_{M,N}=\varnothing\). Since \(E_{M,N}\) is relatively closed and has empty relative interior, it is nowhere dense in \(X\).

No uniformity over boundary points \(b\) is required: one first selects \(b\) for the chosen open set, and then takes \(n\) sufficiently large for that fixed \(b,M\). Only one violating \(n\ge N\) is needed to exclude a point from the all-\(n\) intersection (30).

## 6. Ambient dense G_delta and all-center non-tightness

Set

\[
R=X\setminus\bigcup_{M,N\ge1}E_{M,N}
=\bigcap_{M,N\ge1}(X\setminus E_{M,N}).
\tag{33}
\]

Each factor on the right is open and dense in \(X\). Baire's theorem makes \(R\) dense in \(X\). Every relatively open factor equals \(X\cap O_{M,N}\) for some ambient open \(O_{M,N}\). Since \(X\) is ambient \(G_\delta\), equation (33) is an ambient \(G_\delta\); since \(X\) and \(R\) are successively dense, it is dense in \((0,1)\). If desired, ambient residuality also follows by observing that the ambient closure of each relatively closed nowhere-dense \(E_{M,N}\) has empty interior: its intersection with the dense set \(X\) is exactly \(E_{M,N}\).

For \(t\in R\), the negation of (30) gives

\[
\forall M,N\in\mathbb N_{>0}\quad\exists n\ge N:
\quad C_n(t,M)<3/4.
\tag{34}
\]

Fix any deterministic sequence \((c_n)\). At every such witness \(n\),

\[
\mathbb P\bigl(|Y_n(\lfloor nt\rfloor+1)-c_n|>M\sqrt n\bigr)>1/4.
\tag{35}
\]

For any real radius \(L\ge0\), choose a positive integer \(M\ge L\). Equation (35), for arbitrarily large \(n\), also holds with \(L\) replacing \(M\), proving (3). Tightness would require, for instance, a finite radius with all these tail probabilities below \(1/5\); (3) excludes that. The witnesses may depend on \(t,M,N\), but the inequality is uniform over the center. No union over the uncountable family of center sequences is taken.

Equivalently, existence of a tight deterministic centering would imply membership in some \(E_{M,N}\), because tightness supplies a fixed sufficiently large integer radius with concentration greater than \(3/4\) for all sufficiently large \(n\). The converse is not asserted: a single \(3/4\) concentration guarantee is insufficient for tightness at all error levels. The construction of \(R\) is therefore a sufficient generic bad set, not an exact characterization of all bad ranks. This completes the theorem.

## 7. Attribution and result boundaries

LNS is the antecedent for the source/cost/coding model and dense boundary obstruction. Relevant primary text was independently retrieved at [arXiv v2](https://arxiv.org/abs/1605.02352v2) and the [author manuscript](https://www.math.uni-frankfurt.de/~neiningr/radix_journal.pdf). The retained files agree in their relevant propositions. The manuscript's deterministic-centering setup is in Section 2.4, random centering in Proposition 2.8, boundary obstruction in Proposition 2.9, and the continuity classification in Proposition 2.10. The open-marginal sentence follows Corollary 2.11. The \(\beta=0\) mixture used here is also in Proposition 2.5.

This audit proves the newly assembled residual consequence from checked ingredients. It does not identify an earlier publication that states this residual nonboundary consequence, and logical deducibility is not evidence of prior public disclosure. The final publisher-typeset wording was not retrieved. The authorized candidate separately constructs one explicit square-word rank with all-center non-tightness; neither that construction nor its residual-set membership is needed for this theorem. Its membership in \(R\) is not proved here. The theorem gives no Lebesgue measure classification and no statement about random, data-dependent centering.

The adversarial controls in CONTROL_DERIVATIONS.md isolate the assumptions supporting this proof. The only probabilistic limit theorem needed in the direct argument is the classical binomial CLT. The Baire proof is analytic; finite computation is not used as evidence of a residual conclusion.

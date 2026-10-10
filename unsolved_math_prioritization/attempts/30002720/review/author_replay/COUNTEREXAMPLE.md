# A nonboundary rank with no square-root-scale marginal limit

**Status:** Complete candidate counterexample; separate adversarial review is pending. This is an AI-generated, unrefereed research artifact. Historical priority is unestablished.

## 1. Exact conclusion and source scope

Consider the binary Markov source with initial distribution and transition matrix
\[
\mu=(1/2,1/2),\qquad
P=\begin{pmatrix}3/4&1/4\\1/4&3/4\end{pmatrix}.
\tag{1}
\]
Different input strings are independent. Let \(Y_n(k)\) be the number of bucket operations performed by Radix Selection to retrieve the string of lexicographic rank \(k\) among \(n\) inputs. The algorithm stops on a singleton bucket, exactly as in Leckey–Neininger–Sulzbach [2, equations (2)–(3)]. Put \(q=3/4\).

**Theorem.** There is an explicitly specified fixed \(t\in(0,1)\), which is not a cylinder boundary and is a continuity point of the first-order mean profile, such that for **every deterministic real sequence** \((c_n)\), the sequence
\[
\frac{Y_n(\lfloor nt\rfloor+1)-c_n}{\sqrt n}
\tag{2}
\]
is not tight. In particular it does not converge weakly to a real-valued law. This includes centering by \(n(m\circ h)(t)\) or by the expectation of the cost.

The rank is specified by an infinite binary string \(v\): its digit in position \(r\ge1\) is 1 exactly when \(r=j^2\) for an integer \(j\ge2\). If \(F\) denotes the lexicographic distribution function of (1), take \(t=F(v)\). An explicit convergent rational series for the same number is
\[
 t=\sum_{j=2}^{\infty}qP_j,
 \qquad P_j=\frac12\left(\frac14\right)^{2j-4}
                    q^{j^2-2j+2}.
\tag{3}
\]
Here \(P_j\) is a cylinder probability, not the transition matrix.

The original OWR contribution [1, p. 2856] asks whether the one-dimensional marginals of the centered, square-root-rescaled rank process converge for Markov sources. The later paper [2, Section 2.4] specifies deterministic centering by \(n(m\circ h)(t)\). Its Proposition 2.9 **already proves non-tightness at a dense set of boundary ranks**, whereas the paragraph after Corollary 2.11 still calls marginal convergence open. We credit that result and preserve this textual tension. The theorem here avoids a boundary-rank interpretation issue by using one fixed **nonboundary continuity rank**, and excludes every deterministic centering there. It answers universal fixed-rank convergence negatively; it does not classify all other ranks or decide an almost-everywhere variant. Random, data-dependent centering, as in [2, Proposition 2.8], is a different question.

The proof below is elementary apart from the classical binomial central limit theorem, whose application is recalled. It does not assume [2, Theorem 1.2] or transfer process non-tightness to a fixed marginal.

## 2. Cylinder coding and the exact cost

For a finite word \(w=w_1\cdots w_d\), write
\[
 \pi(w)=\frac12\prod_{r=1}^{d-1}p_{w_r w_{r+1}},
 \qquad \pi(\varnothing)=1.
\]
Partition \([0,1]\) recursively into lexicographically ordered binary cylinder intervals \(I(w)\), with length \(\pi(w)\). Children subdivide each interval in the source's conditional proportions. Endpoints can be assigned by a half-open convention. Their countable union has Lebesgue measure zero.

The unique nested coding of a uniform \(U\) away from these endpoints has the source distribution (1). Denote it by \(h(U)\). The coding is order-preserving. Thus independent uniform variables \(U_1,\ldots,U_n\) give the required input strings \(S_i=h(U_i)\), and, almost surely,
\[
 S_{(k)}=h(U_{(k)}).
\tag{4}
\]
For an infinite word \(s\), let \(s^{(d)}\) be its length-\(d\) prefix and define
\[
 m(s)=\sum_{d\ge0}\pi(s^{(d)}),\qquad
 \Lambda_{n,d}(s)=\#\{i:s^{(d)}\preceq S_i\},
\]
\[
 Z_n(s)=\sum_{d\ge0}\Lambda_{n,d}(s)
                         \mathbf1_{\{\Lambda_{n,d}(s)>1\}}.
\tag{5}
\]
These are the source's definitions, and \(Y_n(k)=Z_n(S_{(k)})\). In particular, no cost is charged for continuing to read a singleton.

All length-\(d\) probabilities satisfy \(\pi(w)\le\tfrac12q^{d-1}\) for \(d\ge1\). If two strings share a nonempty prefix \(w\), all terms of their \(m\)-sums up to that prefix agree, and each remaining sum lies in \([0,3\pi(w)]\). Consequently
\[
 |m(s)-m(s')|\le3\pi(w).
\tag{6}
\]
This is a uniform bound, including infinite eventual-constant words.

Since \(v\) has infinitely many 0s and 1s, its coding point \(t\) lies strictly inside every finite cylinder containing it. It is therefore not any cylinder endpoint, and \(h(u)\) shares every prescribed finite prefix of \(v\) when \(u\) is sufficiently close to \(t\). Equation (6) proves that \(m\circ h\) is continuous at \(t\). In particular, this counterexample is not at one of the jumps already treated in [2, Proposition 2.9].

## 3. An elementary uniform cost estimate

We will use
\[
 \sup_s|Z_n(s)-nm(s)|
       =O_{\mathbb P}\bigl(\sqrt n(\log n)^{3/2}\bigr).
\tag{7}
\]
Here is a direct proof, with an explicit high-probability event. For \(n\ge2\), set
\[
 H_n=\left\lceil\frac{5\log n}{\log(4/3)}\right\rceil+1,
 \qquad d_n=\sqrt{\frac{2\log n}{n}}+n^{-2}.
\]
Let \(D_n=\sup_{x\in[0,1]}|n^{-1}\sum_i\mathbf1_{\{U_i\le x\}}-x|\).

At each point of the grid \(\{r/n^2:0\le r\le n^2\}\), the Bernoulli exponential bound gives a deviation probability at most \(2n^{-4}\) at threshold \(\sqrt{2\log n/n}\). A union bound and monotonicity between consecutive grid points yield
\[
 \mathbb P(D_n>d_n)\le4n^{-2}.
\tag{8}
\]
For completeness, the exponential bound follows by applying Markov's inequality to a centered Bernoulli sum. The logarithm of a centered Bernoulli moment-generating function has value and first derivative zero at zero, and second derivative at most \(1/4\); hence it is at most \(s^2/8\). Optimizing \(s\) gives \(2e^{-2n\varepsilon^2}\) for the two tails.

The probability that any pair of input strings shares its first \(H_n\) digits is at most
\[
 {n\choose2}\sum_{|w|=H_n}\pi(w)^2
 \le\frac{n^2}{4}q^{H_n-1}\le\frac1{4n^3}.
\tag{9}
\]
On the complement of that event, every count at depth \(H_n\) is at most 1, so the cost (5) has no terms of depth \(H_n\) or greater. On \(D_n\le d_n\), every cylinder count differs from its expectation by at most \(2nd_n\). Replacing a count by its singleton-truncated version changes it by at most 1. Finally,
\[
 \sum_{d\ge H_n}\pi(s^{(d)})\le2q^{H_n-1}\le2n^{-5}.
\]
Thus, on an event \(G_n\) of probability at least \(1-4n^{-2}-(4n^3)^{-1}\), simultaneously for all infinite \(s\),
\[
 |Z_n(s)-nm(s)|\le R_n,
 \quad R_n:=2nH_nd_n+H_n+2n^{-4}.
\tag{10}
\]
This proves (7). All cylinder endpoints are avoided simultaneously with probability one, so the count bound applies with either endpoint convention. The supremum causes no measurability difficulty: (10) is a deterministic consequence of the measurable events just constructed, and no random supremum is needed later.

## 4. A sequence of nearby jumps

Let \(W_j=v_1\cdots v_{j^2-1}\), \(j\ge2\). It ends in 0. Counting transitions shows
\[
 \pi(W_j)=P_j
 =\frac12(1/4)^{2j-4}q^{j^2-2j+2}.
\tag{11}
\]
Indeed, its \(j-2\) isolated 1s contribute \(2j-4\) changes, and its remaining \(j^2-2j+2\) transitions preserve the digit.

Consider the two adjacent endpoint strings
\[
 a_j=W_j0\,111\cdots,\qquad b_j=W_j1\,000\cdots,
\]
and their common rank boundary \(\tau_j=F(a_j)=F(b_j)\). Put \(A_j=m(a_j)\), \(B_j=m(b_j)\), and \(C_j=\sum_{d=0}^{j^2-1}\pi(v^{(d)})\). Geometric summation gives
\[
 A_j=C_j+P_jq\left(1+\frac{1/4}{1-q}\right)
     =C_j+\frac32P_j,
\]
\[
 B_j=C_j+\frac{P_j}{4}\left(1+\frac{1/4}{1-q}\right)
     =C_j+\frac12P_j.
\]
Therefore
\[
 A_j-B_j=P_j>0.
\tag{12}
\]
These endpoint formulas are special cases of the already published mechanism in [2, Proposition 2.1].

After its 1 in position \(j^2\), the word \(v\) has \(2j\) zeros before its next 1. The cylinder \(I(W_j1\,0^{2j})\) starts at \(\tau_j\), and its length is \(P_jq^{2j}/12\). Hence
\[
 0<t-\tau_j<\frac{P_j}{12}q^{2j}.
\tag{13}
\]
The same description gives \(\tau_j=\sum_{i=2}^j qP_i\), proving (3).

Set
\[
 w_j=P_jq^j,\qquad K_j=\lfloor j/2\rfloor,
 \qquad n_j=\lceil w_j^{-2}\rceil.
\tag{14}
\]
The left cylinder \(I(W_j0\,1^{K_j})\) ends at \(\tau_j\) and has length \(P_jq^{K_j}/4\). The right cylinder \(I(W_j1\,0^{K_j})\) starts there and has length \(P_jq^{K_j}/12\). Since \(12q^{j-K_j}\to0\), for all sufficiently large \(j\) the intervals
\[
 (\tau_j-w_j,\tau_j),\qquad (\tau_j,\tau_j+w_j)
\]
lie inside these left and right cylinders, respectively. Equation (6) then implies, outside the null set of coding endpoints,
\[
 \begin{array}{ll}
 |m(h(u))-A_j|\le P_jq^{K_j},&\tau_j-w_j<u<\tau_j,\\[2mm]
 |m(h(u))-B_j|\le P_jq^{K_j},&\tau_j<u<\tau_j+w_j.
 \end{array}
\tag{15}
\]
(The exact bounds obtained from (6) are \(3P_jq^{K_j}/4\) and \(P_jq^{K_j}/4\), so the displayed common bound is conservative.)

We also have
\[
 \sqrt{n_j}w_j\longrightarrow1,\qquad
 \sqrt{n_j}P_j\ge q^{-j}\longrightarrow\infty,
 \qquad \log n_j=O(j^2).
\tag{16}
\]
For the last estimate, \(P_j\ge4^{-(j^2-1)}\) and \(q^j\ge4^{-j}\), so \(n_j\le2\cdot16^{j^2+j-1}\). In particular, the error (10) obeys
\[
 \frac{R_{n_j}}{n_jP_j}
 =O\left(\frac{(\log n_j)^{3/2}}{\sqrt{n_j}P_j}\right)+o(1)
 =O(j^3q^j)+o(1)\longrightarrow0.
\tag{17}
\]
Also (13) gives \((t-\tau_j)/w_j\to0\).

## 5. Two positive-probability cost bands

For \(k_n=\lfloor nt\rfloor+1\), the usual order-statistic central limit theorem is
\[
 \sqrt n\,(U_{(k_n)}-t)\ \Rightarrow\ N(0,t(1-t)).
\tag{18}
\]
One may obtain (18) directly from
\(\mathbb P(U_{(k_n)}\le x)=\mathbb P(\operatorname{Bin}(n,x)\ge k_n)\), taking \(x=t+z/\sqrt n\) and using the binomial CLT. The rounding error in \(k_n\) is at most 1 and disappears on this scale. The Bernoulli parameters tend to the interior point \(t\), so the same CLT applies along this triangular sequence (or follows by expanding its characteristic function).

Define
\[
 E_j^-:=\{\tau_j-w_j<U_{(k_{n_j})}<\tau_j\},\qquad
 E_j^+:=\{\tau_j<U_{(k_{n_j})}<\tau_j+w_j\}.
\]
By (13), (16), and (18), both event probabilities tend to
\[
 \rho:=\Phi\left(\frac1{\sqrt{t(1-t)}}\right)-\frac12>0,
\tag{19}
\]
where \(\Phi\) is the standard normal distribution function. In fact \(\rho\ge\Phi(2)-1/2\).

On \(E_j^-\cap G_{n_j}\), equations (4), (10), and (15) give
\[
 \left|\frac{Y_{n_j}(k_{n_j})}{n_j}-A_j\right|
 \le P_jq^{K_j}+\frac{R_{n_j}}{n_j}.
\]
On \(E_j^+\cap G_{n_j}\), the analogous bound holds around \(B_j\). Since \(\mathbb P(G_{n_j})\to1\), (17) shows that, for all sufficiently large \(j\), each of the following two disjoint deterministic intervals contains the cost with probability at least \(\rho-o(1)\):
\[
 J_j^-:=n_j[A_j-P_j/8,A_j+P_j/8],\qquad
 J_j^+:=n_j[B_j-P_j/8,B_j+P_j/8].
\tag{20}
\]
Their distance is \(3n_jP_j/4\). For every fixed \(M>0\), (16) implies that an interval of length \(2M\sqrt{n_j}\) can intersect at most one of them, once \(j\) is large. Consequently, uniformly over every real center \(a\),
\[
 \limsup_{j\to\infty}\ \sup_{a\in\mathbb R}
 \mathbb P\left(|Y_{n_j}(k_{n_j})-a|\le M\sqrt{n_j}\right)
 \le1-\rho.
\tag{21}
\]
Taking \(a=c_{n_j}\) proves failure of tightness in (2), for every deterministic centering sequence. This proves the theorem. \(\square\)

## 6. What the result does and does not establish

The counterexample has strictly positive transition probabilities, a stationary strictly positive initial distribution, independent input strings, a fixed rank proportion, and the exact singleton-stopping cost. The rank is a continuity point of the first-order profile. Thus neither a changing rank parameter, a boundary tie, nor a process-level tightness failure is being substituted for the one-dimensional assertion.

The result rules out a universal positive answer, even after excluding cylinder boundaries. It makes no claim that all nonboundary ranks fail, that failure occurs almost everywhere, or that no data-dependent centering works. The already published random-centering result remains compatible with (21).

The infinite rank and subsequence are explicit through (3), (11), and (14). Finite exact controls check the identities and combinatorics; they do not establish an asymptotic limit by themselves. The estimates and the binomial CLT above are the proof.

## References and access qualifications

1. Kevin Leckey, *Radix Sort on Markov Sources*, in *Probability, Trees and Algorithms*, Oberwolfach Report 50/2014, pp. 2854–2856, DOI [10.4171/OWR/2014/50](https://doi.org/10.4171/OWR/2014/50). [Full primary report](https://ems.press/content/serial-article-files/46539). The complete contribution was read.
2. Kevin Leckey, Ralph Neininger, and Henning Sulzbach, *Process convergence for the complexity of Radix Selection on Markov sources*, *Stochastic Processes and their Applications* 129 (2019), 507–538, DOI [10.1016/j.spa.2018.03.009](https://doi.org/10.1016/j.spa.2018.03.009). [arXiv:1605.02352v2](https://arxiv.org/abs/1605.02352v2); [author-hosted full manuscript](https://www.math.uni-frankfurt.de/~neiningr/radix_journal.pdf). The retrieved arXiv PDF bears a 2 October 2017 version stamp and an internal 15 October 2018 date; the author-hosted manuscript is dated 2 October 2017. Both contain the exact cost definitions, boundary obstruction, and subsequent open-marginal sentence. The final publisher-typeset text was not recovered, so identity of every published wording is not claimed.
3. The same authors, *Analysis of radix selection on Markov sources*, AofA 2014, pp. 253–264; [arXiv:1404.3672](https://arxiv.org/abs/1404.3672). This is the earlier paper cited in the OWR contribution. The special memoryless functional limits and grand-average results are prior work, not consequences claimed here.

Current source checks and the exact distinction between the known boundary obstruction and this nonboundary construction are recorded in `SOURCE_AUDIT.md`. No historical-priority claim is made.

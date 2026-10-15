# Explicit finite coefficient obstructions for the ternary and base-four digit families

12 October 2026. This is the complete authored finite-bound proof. It depends on the previously accepted full-ternary and full-base-four computer-assisted exhaustive enumerations and their general analytic zero bounds. The complete substantive independent audit is included in [the finite-bound review](REVIEW_FINITE_COEFFICIENT_OBSTRUCTIONS.md).

The executable programs and raw state certificates are not distributed in this appendix. Complete-stream equality and replay results below report the accepted historical computations. This is a prose proof-and-review edition; independent executable reproduction requires implementing the earlier exact search specifications. No novelty or priority claim is made.

## Theorem and relationship to the earlier searches

Let
\[
N_*=150\,994\,944=36\cdot2048^2.
\]
For each of the following two families, every infinite sign assignment has a coefficient outside \(\{-1,0,1\}\) in degrees 1 through \(N_*\):

1. The ternary-digit family
\[
F_m(q)=\prod_{j\ge0}(1+u_{m,j}q^{m3^j}+v_{m,j}q^{2m3^j}),
\qquad u_{m,j},v_{m,j}\in\{-1,1\};
\]
2. The base-four-digit family
\[
F_m(q)=\prod_{j\ge0}(1+a_{m,j}q^{m4^j}+b_{m,j}q^{2m4^j}+c_{m,j}q^{3m4^j}),
\qquad a_{m,j},b_{m,j},c_{m,j}\in\{-1,1\}.
\]
In each case the product is \(\prod_{m\ge1}F_m(q)\), retaining every original unrestricted-partition factor and every indicated digit-sign freedom.

This explicit bound is **not claimed to be sharp**. It does not assert that degrees 59 or 77 are coefficient-only obstruction thresholds, and does not give an obstruction for arbitrary independently signed original factor coefficients. The argument converts the previously certified global-coefficient Jensen searches into honest finite coefficient obstructions by allowing a rigorously bounded unknown tail.

The certified ternary and base-four finite searches use 21 rational radii \(r=(b-1)/b\), with
\[
b\in\{2,3,4,6,8,12,16,24,32,48,64,96,128,192,256,384,512,768,1024,1536,2048\}.
\]
They become empty at combined-search degrees 59 and 77, respectively. Their combinatorial recurrences, domains, exact coefficient updates, and complete retained state trees are unchanged here. Only their analytic upper envelopes are enlarged, by the common rational amount
\[
\eta=2^{-32768}. \tag{1}
\]
We prove that a good coefficient prefix through \(N_*\) already implies those enlarged envelopes, and that every formerly strict analytic rejection remains strict after the enlargement. Separate exact replays verify the unchanged complete searches.

## 1. A universal elementary partition bound

Let \(p(n)\) count unrestricted partitions. For \(t>0\), put
\[
E(e^{-t})=\prod_{m\ge1}(1-e^{-mt})^{-1}.
\]
Expanding the logarithm and summing nonnegative terms gives
\[
\log E(e^{-t})
=\sum_{k\ge1}\frac1{k(e^{kt}-1)}
\le\frac1t\sum_{k\ge1}\frac1{k^2}
\le\frac2t. \tag{2}
\]
The last bound follows from \(\sum_{k\ge1}k^{-2}\le1+\int_1^\infty x^{-2}\,dx=2\). Since the coefficient terms are nonnegative, \(p(n)e^{-nt}\le E(e^{-t})\). For \(n\ge1\), choose \(t=1/\sqrt n\) in (2) to obtain
\[
\boxed{\quad p(n)\le e^{3\sqrt n}.\quad} \tag{3}
\]
No asymptotic formula for partitions is needed.

For any independent choice of the original factor signs, the coefficient of degree \(n\) is a sum of exactly \(p(n)\) terms, each \(+1\) or \(-1\), one for each partition. Therefore
\[
|A_n|\le p(n). \tag{4}
\]
This applies in particular to both digit families, even when their coefficients are only assumed good through some finite degree.

## 2. An explicit unknown-tail bound at all the chosen radii

Fix one radius \(r=(b-1)/b\), and write \(t=-\log r\). The inequality \(-\log(1-x)\ge x\) gives \(t\ge1/b\). For \(n\ge36b^2\),
\[
6\sqrt n\le n/b\le nt.
\]
Hence (3)–(4) imply
\[
|A_n|^2r^{2n}\le e^{6\sqrt n-2nt}\le e^{-nt}=r^n. \tag{5}
\]
Because \(N_*\ge36b^2\) for every chosen denominator,
\[
\sum_{n>N_*}|A_n|^2r^{2n}
\le\frac{r^{N_*+1}}{1-r}=b\,r^{N_*+1}. \tag{6}
\]
This tail estimate uses only the universal coefficient bound (4).

We now make (6) rationally explicit without forming an enormous power. For each integer \(b\ge2\), the binomial theorem gives
\[
\left(\frac b{b-1}\right)^b
=\left(1+\frac1{b-1}\right)^b
\ge1+\frac b{b-1}>2.
\]
Thus \(r^b<1/2\). Since \(b\le2048\),
\[
\left\lfloor\frac{N_*+1}{b}\right\rfloor\ge73728,
\]
and therefore
\[
\boxed{\quad
\sum_{n>N_*}|A_n|^2r^{2n}
<2048\cdot2^{-73728}=2^{-73717}<\eta.
\quad} \tag{7}
\]
The integer identity \(N_*/2048=73728\) is the only large-degree arithmetic used here.

## 3. What a finite good prefix implies for the Jensen upper envelopes

Assume, for contradiction, that all coefficients through degree \(N_*\) have absolute value at most 1. The products remain analytic in the open unit disk irrespective of this hypothesis. Their locally uniform convergence, persistent block zeros, and Jensen identities are the same as in the certified family proofs.

For the ternary search, the original squared-norm upper envelope was
\[
U_r^{(3)}=\frac1{1-r^2}.
\]
The prefix contributes at most this full geometric sum, and the unknown tail is bounded by (7). Consequently
\[
\sum_{n\ge0}|A_n|^2r^{2n}<U_r^{(3)}+\eta. \tag{8}
\]
The geometric sum intentionally overestimates part of the tail already: this makes (8) weaker, never invalid.

For the base-four search, let \(\pi_n=p(n)\bmod2\). The coefficient parity of the signed product equals partition parity. Through the assumed good prefix, \(|A_n|^2=\pi_n\). Since \(N_*>512\),
\[
\sum_{n=0}^{N_*}|A_n|^2r^{2n}
\le U_r^{(4)}:=\sum_{n=0}^{512}\pi_nr^{2n}
+\frac{r^{1026}}{1-r^2}.
\]
Together with (7),
\[
\sum_{n\ge0}|A_n|^2r^{2n}<U_r^{(4)}+\eta. \tag{9}
\]
All 513 parity bits are the same exact bits already verified in the base-four certificate; no parity density or information about individual coefficients beyond \(N_*\) is used.

Thus every necessary Jensen comparison in either search remains valid for a good finite prefix if its old upper envelope \(U\) is replaced by \(U+\eta\). It remains to show that this enlargement does not rescue any rejected profile.

## 4. Uniform lower bound on every base-four pruning margin

The base-four search uses the rational inner-zero lower bound \(R=1839/1000\). At a radius \(r=a/b\), \(a=b-1\), its lower squared-norm requirement from the currently known defects is
\[
L=R^{2K}r^{2S},
\]
where \(K\) is the number of contributing defects and \(S\) their weighted exponent sum. The original rejection condition was \(L>U_r^{(4)}\).

For the truncation limit 78, every defect in a tested profile belongs to an edge of exponent at most 26. At exponent \(n\), at most \(d_n=1+v_4(n)\) defects are possible, each of weight at most \(2n\). Therefore
\[
K\le\sum_{n=1}^{26}d_n=26+6+1=33, \tag{10}
\]
\[
S\le2\sum_{n=1}^{26}nd_n
=2\left(351+4\cdot21+16\right)=902. \tag{11}
\]
These bounds even allow profiles at levels never reached by the actual search.

The rational number \(L\) has a denominator dividing \(1000^{2K}b^{2S}\). The verified envelope \(U_r^{(4)}\) has denominator dividing \(b^{1024}(2b-1)\). Consequently a strict positive rational difference satisfies
\[
L-U_r^{(4)}
\ge\frac1{1000^{2K}b^{2S+1024}(2b-1)}. \tag{12}
\]
The common denominator in (12) need not be reduced; a larger denominator still gives a valid lower bound.

Since \(1000<2^{10}\), \(b\le2^{11}\), and \(2b-1<2^{12}\), equations (10)–(11) imply
\[
1000^{2K}b^{2S+1024}(2b-1)
<2^{660+31108+12}=2^{31780}.
\]
Thus every strict base-four rejection has
\[
\boxed{\quad L-U_r^{(4)}>2^{-31780}>\eta.\quad} \tag{13}
\]
It remains a strict rejection after inflation by \(\eta\).

## 5. Uniform lower bound on every ternary pruning margin

Let \(\varphi=(1+\sqrt5)/2\). At radius \(r=a/b\), the ternary lower squared-norm requirement is
\[
L=\varphi^{2K}r^{2S},
\qquad U_r^{(3)}=\frac{b^2}{b^2-a^2}.
\]
The original strict rejection is equivalent to
\[
E=A\varphi^{2K}-B>0,
\quad A=a^{2S}(b^2-a^2),\quad B=b^{2S+2}. \tag{14}
\]
Here \(0<A<B\), because \(A/B=r^{2S}(1-r^2)<1\).

Conjugate \(\varphi\) to \(\varphi'=1-\varphi=-1/\varphi\). Then
\[
E'=A\varphi^{-2K}-B\in(-B,0).
\]
The product \(EE'\) is a nonzero integer. To see this without invoking an unstated algebraic-number theorem, reduce powers using \(\varphi^2=\varphi+1\), writing \(E=u\varphi+v\) for integers \(u,v\). Its conjugate product is
\[
(u\varphi+v)(u\varphi'+v)=v^2+uv-u^2\in\mathbb Z.
\]
It is nonzero since \(E>0\) and \(E'<0\). Hence \(|EE'|\ge1\), and \(|E'|<B\) gives
\[
E>1/B. \tag{15}
\]
Dividing (14) by its positive denominator,
\[
L-U_r^{(3)}
=\frac{E}{b^{2S}(b^2-a^2)}
>\frac1{b^{4S+2}(2b-1)}. \tag{16}
\]

In the ternary truncation limit 60, known defects have exponents at most 30. Their multiplicity at exponent \(n\) is at most \(1+v_3(n)\), so
\[
S\le\sum_{n=1}^{30}n(1+v_3(n))
=465+3\cdot55+9\cdot6+27=711. \tag{17}
\]
Thus
\[
b^{4S+2}(2b-1)
<2^{11(2846)+12}=2^{31318},
\]
and every strict ternary rejection has
\[
\boxed{\quad L-U_r^{(3)}>2^{-31318}>\eta.\quad} \tag{18}
\]
Again every old rejection survives the enlarged upper envelope.

## 6. Exact inflated-envelope replays and the finite contradiction

The original coefficient recurrences and sign domains are unchanged. Increasing an upper envelope cannot create a new analytic rejection, while (13) and (18) show that it removes none of the old strict rejections. Therefore, by induction over the finite searches, all complete retained state sets are unchanged. This argument alone relates the new searches to their original complete certificates.

In addition, both searches are replayed using the enlarged envelopes directly, with exact arithmetic:

- Ternary: with the old integers \(A,B\) from (14), compare
\[
(2^{32768}A)\varphi^{2K}
>2^{32768}B+b^{2S}(b^2-a^2).
\]
The same exact quadratic-field integer comparison as in the original certificate is used.
- Base four: replace each rational envelope numerator and denominator by
\[
(U_{\rm num},U_{\rm den})\longmapsto
(2^{32768}U_{\rm num}+U_{\rm den},\ 2^{32768}U_{\rm den}),
\]
then perform the same integer cross-multiplication as before.

The replayed ternary search has the same 831,371 nonempty states, with an empty combined frontier at 59. Every regenerated frontier byte matches its original complete certificate. The replayed base-four search has the same 11,151,089 nonempty states, with an empty combined frontier at 77. Its complete prefix tree matches the original byte for byte. These are checks of whole state histories, not merely matching endpoint counts.

Now suppose a product in either family had all coefficients good through \(N_*\). Equations (8)–(9) show that its degree-by-degree partial states must satisfy the inflated necessary inequalities. Its actual coefficient prefix also satisfies the searches' exact coefficient tests. It would therefore survive every retained level of the corresponding complete search. The empty frontier contradicts that conclusion.

This proves the explicit finite bound \(N_*\) for both families. The finite degree is large because the elementary universal tail bound is deliberately conservative. No sharpness, unrestricted sign-array obstruction, or search record for the original problem is claimed.

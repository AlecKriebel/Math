# Interior smoothness of exponential parameter hairs

Problem 5300062 / AMR-052-0062. Research checkpoint: 2026-10-05.

**Disposition: scoped partial result; the complete smoothness-and-analyticity question is not resolved here.** Five mathematical approaches are recorded. The principal result below proves C-infinity regularity of the interiors of the standard parameter rays. No assertion of novelty, exhaustive literature coverage, human peer review, or analytic/endpoint regularity is made. This is an unrefereed, substantially AI-assisted research note, prepared for independent audit.

## 1. Identity and conventions

The selected catalog row has rank 796. Its exact statement hash agrees with the selected complete problem-corpus record; these are identification checks, not mathematical evidence. The live problem URL could not be read: the web tool failed and an ordinary HTTP read returned 403. No access restriction was bypassed.

The primary source is Robert Devaney's section in *Problems in Holomorphic Dynamics*, edited by B. Bielefeld and M. Lyubich, Stony Brook IMS 92/7, printed page 36 (PDF page 38). The displayed superscript was visually checked: it is infinity, although extracted text misrenders it as 1. The primary question concerns parameter-plane hairs of E_lambda(z)=lambda exp(z); it also asks about their termination. The catalog isolates smoothness and analyticity. The preceding question about all parameters whose Julia set is the plane is a different, broader problem.

Use three families, with distinct names:

- f_lambda(z)=lambda exp(z), lambda nonzero.
- E_kappa(z)=exp(z+kappa), where lambda=exp(kappa).
- H_kappa(w)=exp(w)+kappa.

The first two maps are identical under lambda=exp(kappa). Translation T_kappa(z)=z+kappa conjugates the second to the third: T_kappa E_kappa T_kappa^{-1}=H_kappa. Thus their singular values are respectively 0 and kappa. The corresponding dynamic rays differ by T_kappa. Locally kappa -> exp(kappa) is a biholomorphic parameter change; it preserves regular C-infinity and real-analytic curve germs. Globally it is a covering map, so address labels and injectivity must not simply be copied between the plane and cylinder.

Set F(t)=exp(t)-1, t>=0. Addresses s=(s_1,s_2,...) are integer sequences. Exponential boundedness means |s_(n+1)|<=F^n(x) for some x>0 and every n>=0. Bounded addresses are a proper subclass. Define the minimal potential

 t_s = limsup_(n->infinity) F^{-(n-1)}(|s_n|).

Scaling entries by 2 pi gives the same minimal potential. This follows from the strict separation of iterates proved below, and is used only beyond any fixed t>t_s. The standard ray has open potential interval (t_s,infinity). An existing endpoint at t_s is excluded throughout the main theorem.

## 2. Established inputs and limits of the literature check

The following are credited inputs, not results claimed as new here.

[FS] M. Foerster and D. Schleicher, *Parameter Rays for the Exponential Family*, arXiv:math/0505097, Theorem 3.7: for every exponentially bounded address there is a unique parameter curve G_s(t), t>t_s, characterized by g_s^{G_s(t)}(t)=0; this root in kappa is simple. Theorem 2.6 and Lemma 3.5 provide the dynamic-ray construction and its local domains; Proposition 4.6 gives its nonzero potential derivative. The remark after Theorem 3.7 states C1 and suggests C-infinity. https://arxiv.org/abs/math/0505097

[F] M. Foerster, *Exponential Maps with Escaping Singular Orbits*, doctoral thesis, 2006, Corollary 3.5.2 and following remark, printed pages 97-98: explicit C1 parameter-ray argument, followed by the same proposed higher-regularity extension. https://d-nb.info/1034787640/34

The journal article is *Parameter rays in the space of exponential maps*, ETDS 29 (2009), 515-544, DOI 10.1017/S0143385708000394. Its publisher metadata was checked, but a putative PDF request returned HTML. No line-by-line inspection of the final journal text is claimed. https://doi.org/10.1017/S0143385708000394

[V] M. Viana da Silva, *The Differentiability of the Hairs of exp(Z)*, Proc. AMS 103 (1988), 1179-1184: C-infinity **dynamic** hairs. All six scanned pages were inspected. This is not by itself a parameter-ray smoothness theorem. https://w3.impa.br/~viana/out/hairs.pdf

[FRS] M. Foerster, L. Rempe and D. Schleicher, *Classification of Escaping Exponential Maps*, Proc. AMS 136 (2008), 651-663. This separates ray interiors from escaping endpoints and classifies escaping parameter components. No endpoint differentiability follows from this topological classification. https://arxiv.org/abs/math/0311427

[CHW] W. Cui, J. Huang and L. Wang, *Non-analyticity of hairs of exponential maps*, arXiv:2609.32703v1, submitted 26 September 2026; PDF dated 29 September 2026. Its Theorem 1 treats dynamic hairs of one fixed real map with 0<lambda<1/e. Its proof uses that map's dense attracting basin. It supplies no parameter-hair theorem, and is treated here as a recent unrefereed manuscript. https://arxiv.org/abs/2609.32703v1

The recent searches found no verified complete parameter-hair analyticity resolution. This negative search finding is not an assertion that no such result exists.

## 3. Main scoped theorem

**Theorem.** Let s be any exponentially bounded external address. In the standard potential coordinate, G_s:(t_s,infinity)->C is C-infinity and G_s'(t) is nonzero. Consequently its local images under lambda=exp(kappa) are regular C-infinity parameter-curve germs. This statement includes unbounded exponentially bounded addresses, but makes no assertion at t_s and no assertion of real analyticity.

The proof supplies the joint parameter/potential estimates needed before applying the real implicit function theorem. Separate smoothness at one fixed parameter is insufficient.

### 3.1 Separation of exponential iterates

For 2<=u<v, put u_m=F^m(u), v_m=F^m(v). Since F'>=2 on [2,infinity), v_m-u_m>=2^m(v-u). For m>=1,

 F^m(u)/F^m(v) <= 2 exp(-(v_(m-1)-u_(m-1)))
                 <= 2 exp(-2^(m-1)(v-u)).                 (1)

Indeed F(y)>=exp(y)/2 for y>=2, while F(x)<=exp(x). In particular, for fixed u<v, any polynomial in m times this ratio tends to zero. Also F^m(u)>=2^m u. Fixed multiplicative constants in address bounds can therefore be absorbed by increasing the starting value by any positive amount, after finitely many iterates.

### 3.2 Uniform smoothness on ray tails

Fix K>=1 and an address for which

 2 pi |s_(j+1)| <= F^j(x_0) for all j>=0,

where x_0>=2. Choose a compact interval [a,b] and eta>0 with

 a>max{x_0,K+6},             b+eta<F(a).

Shrinking the interval if necessary always allows the second condition. Put

 L_(kappa,j)(w)=Log(w)-kappa+2 pi i j,
 g_(n,kappa,s)(t)=L_(kappa,s_1) ... L_(kappa,s_n)(F^n(t)),

using principal logarithms on the right half-plane. These finite approximants converge to the usual dynamic ray on such tails by [FS]. We will prove that all their potential derivatives converge locally uniformly, uniformly for |kappa|<=K.

For real t>=a, every intermediate value after pulling back to level j has real part at least F^j(t)-K-1. This follows by descending induction: if Re w>=F^(j+1)(t)-K-1, then

 Re(Log w-kappa) >= log(F^(j+1)(t)-K-1)-K
                  >= F^j(t)-K-1.

The last inequality follows from (K+2) exp(-F^j(t))<1-exp(-1), ensured by a>K+6. Imaginary address offsets do not decrease this lower bound. Thus all these values have real part greater than 5, uniformly in n and kappa.

For n>=1 define

 D_n=(F^(n-1))'(b+eta),      r_n=min{eta,1/(16 D_n)}.

For t in [a,b] and |z-t|<=r_n, the nonnegative Taylor coefficients of F and its iterates give

 |F^(n-1)(z)-F^(n-1)(t)| <= r_n D_n <= 1/16.             (2)

Here |z|<=b+eta and the derivative bound follows termwise from those nonnegative coefficients. Write v=F^(n-1)(z), U=F(v)=F^n(z), and q(w)=w+Log(1-exp(-w)) in a sufficiently far right half-plane. On the disk in (2), Re v>=a-1/16; q is holomorphic and |q'|<=2. Furthermore Re U and |U| are bounded below by a fixed positive multiple of exp(F^(n-1)(t)); one may use |U|>=exp(F^(n-1)(t))/2.

The germ of the last pullback of g_n extends to this disk as

 A(z,kappa)=q(v)-kappa+2 pi i s_n.

This is the important branch step: continuing Log(F^n(z)) as q(F^(n-1)(z)) avoids imposing a much smaller disk that controls the imaginary part of F^n(z).

For g_(n+1), first write

 d(z,kappa)=Log(1-exp(-U))-kappa+2 pi i s_(n+1).

Its last two pullbacks extend as

 B(z,kappa)=A(z,kappa)+Log(1+d(z,kappa)/U).

For real z=t these expressions agree with the original principal-log approximants. Uniformly for t in [a,b], |kappa|<=K and z in the disk,

 |d| <= K+F^n(x_0)+1,
 |d/U| <= 2(K+F^n(x_0)+1) exp(-F^(n-1)(t)).              (3)

By (1), the last bound tends to zero. For all sufficiently large n it is at most 1/16. Therefore |B-A|<=2|d/U|<=1/8, while |A(z,kappa)-A(t,kappa)|<=1/8 by (2).

Apply the remaining n-1 logarithms to A and B. Each value remains within 1/4 of its real-t baseline by induction. Those baseline values have real part greater than 5. Every joining segment consequently lies in Re w>4, where |Log' w|<1/4. All pullbacks are holomorphic in z and kappa, remain on the correct continued branches, and do not increase the difference. Hence, with a constant C depending only on K,

 sup |g_(n+1,kappa,s)(z)-g_(n,kappa,s)(z)|
 <= C exp(F^(n-1)(x_0)-F^(n-1)(a)).                      (4)

The supremum is over the stated t-centered disks and parameter disk. Finitely many initial n are irrelevant to convergence and individually have holomorphic germs on a neighborhood of the compact real interval.

Cauchy's estimate now yields, for each fixed integer k>=0,

 sup_(t in [a,b], |kappa|<=K) |partial_t^k(g_(n+1)-g_n)|
 <= k! r_n^(-k) C exp(F^(n-1)(x_0)-F^(n-1)(a)).          (5)

For all sufficiently large n, r_n^(-1)=16D_n, and

 log D_n = sum_(j=0)^(n-2) F^j(b+eta)
         <= (n-1) F^(n-2)(b+eta).

Because b+eta<F(a), (1) implies

 (n-1)F^(n-2)(b+eta)/F^(n-1)(a) -> 0.

Likewise F^(n-1)(x_0)/F^(n-1)(a)->0. Thus for each fixed k the right side of (5) is eventually at most exp(-F^(n-1)(a)/2), a summable sequence. The derivative series converges uniformly for every finite k.

This proves C-infinity dependence in t uniformly on the parameter disk. All approximants are holomorphic in kappa. Apply the kappa Cauchy formula on any strictly smaller disk to the uniformly convergent derivative series: all mixed derivatives partial_kappa^ell partial_t^k converge uniformly as well. Consequently the limiting ray is jointly C-infinity in (t,Re kappa,Im kappa), and is holomorphic in kappa.

### 3.3 From tails to every interior point

Fix an interior point t_*>t_s and a parameter kappa_* where g_s^kappa(t_*) is defined, in particular kappa_*=G_s(t_*). Choose t_s<u<t_* and a small interval J around t_* whose lower endpoint exceeds u. From the minimal-potential definition and (1), for all sufficiently large N the shifted address sigma^N(s) has the bound

 2 pi |s_(N+j+1)| <= F^(N+j)(u), j>=0.

Increase N until F^N(inf J)>K+6 and F^N(u)>=2, where a parameter neighborhood has |kappa|<=K. Choose J smaller, if needed, so that sup J<F(inf J). Then the shifted interval [a,b]=F^N(J) satisfies b<F(a), and some eta>0 also satisfies b+eta<F(a). Section 3.2 applies to this shifted tail.

Use the dynamic-ray equation

 E_kappa^N(g_s^kappa(t))=g_(sigma^N s)^kappa(F^N(t)).

Along the finite orbit of the selected point, the derivative of E_kappa^N with respect to its phase variable is nonzero: exponentials have no critical points. A local holomorphic inverse of the finite iterate, jointly with kappa, therefore pulls the smooth shifted-tail family back to a jointly smooth germ at (t_*,kappa_*). The local domain statement in [FS, Lemma 3.5] identifies that germ with the original ray. This argument uses local inverse branches, not a global principal-log formula through a singular value.

### 3.4 The parameter equation

Set Phi(t,kappa)=g_s^kappa(t). We have proved that Phi is jointly C-infinity near every zero associated to an interior parameter ray. The simple-root statement of [FS, Theorem 3.7] says Phi_kappa!=0 there. Its real 2 by 2 Jacobian in (Re kappa,Im kappa) has determinant |Phi_kappa|^2>0. The real smooth implicit function theorem gives a C-infinity solution kappa=G_s(t); the uniqueness statement in [FS] identifies it with the global ray.

Differentiating gives

 G_s'(t)=-Phi_t/Phi_kappa.

The numerator is nonzero by [FS, Proposition 4.6], so this is a regular curve. Finally exp(G_s(t)) has derivative exp(G_s(t))G_s'(t)!=0. This proves the theorem.

## 4. Five mathematical approaches and their outcomes

1. **Inverse-branch jets and transversality.** The shrinking-disk construction above establishes the C-infinity interior conclusion for all exponentially bounded addresses. This completes the smoothness portion for standard ray interiors, contingent on the clearly cited existence/simple-root inputs.

2. **Common complex-neighborhood/analytic implicit theorem.** The same approximants are holomorphic on disks whose radii r_n tend to zero. The proof supplies no common positive complex radius in the potential variable. Its constants and starting index depend on derivative order. Therefore the analytic implicit theorem cannot be invoked. This is a failure of this argument, not evidence of non-analyticity.

3. **Holomorphic-motion shortcut and its countercontrol.** Joint C-infinity regularity, holomorphic parameter dependence, and simple roots still do not imply analytic parameter curves. For t near 0 let h(t)=0 for t<=0 and exp(-1/t^2) for t>0; set Phi(t,kappa)=kappa-t-i h(t). Then Phi is jointly smooth and holomorphic in kappa, Phi_kappa=1, and its simple-root curve kappa=t+i h(t) is regular but not a real-analytic curve germ. The image is a graph over its real part, so a real-analytic regular image would force h to be analytic. This is only a general countercontrol, not an exponential-family counterexample.

4. **Real symmetry and an explicit analytic subfamily.** For real lambda>1/e, every real orbit of lambda exp(x) strictly increases, because the minimum of lambda exp(x)-x is 1+log(lambda)>0. A finite limiting orbit would be a fixed point, impossible for this range, so all real orbits escape, including 0. Thus lambda in (1/e,infinity) is an explicit real-analytic curve of escaping parameters with constant zero itinerary. The ray/endpoint classification [FRS] assigns no escaping endpoint to a bounded address, so these parameters lie in the zero-address parameter ray. Its simple real-coordinate parametrization is analytic. This does not determine the analyticity of other address curves, nor assert analyticity of their prescribed potential coordinate. At lambda=1/e, the orbit of 0 increases to 1 rather than escaping, illustrating the boundary distinction.

5. **Recent non-analyticity method and moduli transfer.** The fixed-map result [CHW] cannot be carried over merely by lambda=exp(kappa) or phase translation: those change the presentation of the same parameter family but do not turn a phase ray for one fixed lambda into a parameter ray. Its dense attracting-basin step concerns an open dense subset of one dynamical plane. No corresponding dense set of parameter values, with the paired convergence required by that argument, has been established here. Hence this route supplies neither a parameter counterexample nor a general analyticity proof.

## 5. Exact remaining gap and endpoint cautions

The unresolved part of the selected two-part question is whether general parameter-hair interiors are real-analytic as geometric curves, or which addresses give analytic curves. A proof of non-analyticity of a particular potential parametrization would not automatically disprove real-analyticity of its image: a real-analytic arc may have a smooth non-analytic reparametrization. Conversely, the C-infinity theorem above does not provide factorial derivative bounds or a positive-radius holomorphic potential extension.

No limit t down to t_s is taken in the proof. Its strict margins u<t and b+eta<F(a) are local interior margins. They do not give endpoint derivative bounds, landing, or an analytic boundary extension. [FRS] handles a different, topological classification of escaping endpoints. Bounded versus exponentially bounded addresses must likewise not be confused: the proof uses the latter and its strict potential margin.

The positive real analytic example rules out any blanket statement that every parameter hair is non-analytic. It does not settle the general question. Current status is therefore **unsolved, 5/5 approaches**, with a proved C-infinity interior partial and explicit analyticity/endpoint boundaries.

## 6. Verification and reproducibility

The accompanying code checks finite inverse-branch identities, exact rational jet algebra, conjugacy, a simple-root differentiation identity, positive-side values of the flat-function countercontrol, and finite numerical instances of growth separation. Apart from the exact rational algebra, these are non-certified numerical smoke controls; they neither prove the infinite limits nor validate the cited theorems. The written proof is the mathematical deliverable.

The source metadata records full-file byte counts and SHA-256 values, exact statement-hash match, inspection locations, and bounded prior-attempt checks. Source PDFs, page images, extracted texts, corpus records, raw repository snapshots, and private coordination files are excluded from the safe package. The final manifest binds the authored files and retained results, and the frozen ZIP contains only that safe package.

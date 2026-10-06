# Tightness of contact Godbillon–Vey forms

**Problem 10300055, AMR-102-0055, Calegari Question 13.2. Verified conditional argument with mathematical-audit repairs incorporated; priority and publication-package reviews pending.** This is an application of classical contact-topology theorems. Historical priority is unconfirmed, and this document has not undergone human peer review.

## 1. Exact scope and conclusion

In [C, p. 29], Question 13.2 inherits from Question 13.1 a minimal taut $C^2$ codimension-one foliation $\mathcal F$ of an atoroidal three-manifold, with nonzero Godbillon–Vey evaluation on its fundamental class. There is a globally defined, nowhere-zero defining form $\alpha$ and a connection form $\omega$ satisfying the convention
\[
T\mathcal F=\ker\alpha,\qquad d\alpha=\alpha\wedge\omega.
\tag{1}
\]
The question assumes that $\omega$ is contact and asks whether $\ker\omega$ must be tight. We use the closed, oriented setting of the ordinary fundamental-class evaluation in the source. No assertion about noncompact manifolds or manifolds with boundary is made.

**Theorem.** Let $M$ be a closed oriented smooth three-manifold and $\mathcal F$ a cooriented taut $C^2$ foliation without spherical leaves. Suppose that $\alpha,\omega$ are $C^1$ one-forms, $\alpha$ is nowhere zero, (1) holds, and $\omega\wedge d\omega$ is nowhere zero. Then $\ker\omega$ is tight with the explicit $C^2$-disk meaning stated below, and every sufficiently $C^1$-close smooth contact form is tight in the usual sense. In particular, if $\omega$ is smooth then $\ker\omega$ is tight in the usual smooth sense, answering Calegari's Question 13.2 under its standard smooth contact-form interpretation.

For smooth contact structures, tightness has its usual meaning and is equivalent to the absence of an embedded smooth disk with Legendrian boundary whose tangent planes are distinct from the contact planes along that boundary. For $C^1$ forms, tightness in this note means precisely the absence of such an embedded $C^2$ disk. The proof also shows that every sufficiently $C^1$-close smooth contact form is tight. No equivalence with other low-regularity definitions, or existence of a smooth Legendrian-boundary disk for the original $C^1$ field, is asserted. The smooth criterion is recalled in [DR, p. 5] and [V11, pp. 42–43].

The source's minimality excludes spherical leaves. Atoroidality, minimality, and the numerical value of the Godbillon–Vey class are otherwise not needed in the argument. Crucially, the theorem assumes that a contact $\omega$ already exists. It does not settle the existence or weak-sign attainment question in Question 13.1, recorded separately as problem 10300054.

## 2. The two imported contact-topology facts

We use the following classical results with their stated hypotheses.

1. **Tightness near a taut foliation (Eliashberg–Thurston).** For a cooriented taut $C^2$ foliation without spherical leaves on a closed oriented three-manifold, there is a $C^0$ neighborhood of its tangent plane field such that every smooth positive contact structure in that neighborhood is tight. The corresponding statement for negative contact structures follows by reversing the orientation of the manifold. The result follows from weak symplectic semifillability and the fillability obstruction to overtwistedness. The precise neighborhood statement, rather than merely the existence of some tight approximation, is explicitly recorded in [V11, p. 42] and [DR, Proposition 3.3]. The latter points to p. 50 of [ET].
2. **Gray stability.** A smooth one-parameter family of smooth contact structures on a closed manifold is induced by an isotopy of the manifold. Consequently tightness is constant along that family. We use precisely the smooth version, as stated in [V16, Theorem 2.9, p. 2451].

We do not reprove the symplectic filling theorem. We will not apply Gray stability directly to a merely $C^1$ family, nor replace the given $C^2$ foliation by a smooth foliation.

## 3. A global contact pencil

Differentiating (1) gives
\[
0=d^2\alpha=d\alpha\wedge\omega-\alpha\wedge d\omega
=-\alpha\wedge d\omega.
\tag{2}
\]
This remains valid for the asserted regularity. Indeed $d^2\alpha=0$ holds distributionally. Since $\alpha,\omega$ are $C^1$, their product $\alpha\wedge\omega$ is $C^1$, the product rule is valid, and the continuous form $\alpha\wedge d\omega$ vanishes as a distribution and hence pointwise.

For every constant $s\in\mathbb R$, put
\[
\beta_s=\omega+s\alpha.
\]
Equations (1) and (2) yield the exact global identity
\[
\begin{aligned}
\beta_s\wedge d\beta_s
&=\omega\wedge d\omega
 +s\bigl(\omega\wedge d\alpha+\alpha\wedge d\omega\bigr)
 +s^2\alpha\wedge d\alpha\\
&=\omega\wedge d\omega.
\end{aligned}
\tag{3}
\]
Thus every $\beta_s$ is contact, of the same sign. Also
\[
\ker\beta_s=\ker(\alpha+s^{-1}\omega)\longrightarrow
\ker\alpha=T\mathcal F \quad\text{in }C^0,\qquad s\longrightarrow+\infty.
\tag{4}
\]
The convergence is uniform because $M$ is compact and $\alpha$ is nowhere zero. These are global forms, so no transition functions or choice of local gauge is involved. The shift is itself allowed by (1), since $\alpha\wedge(\omega+s\alpha)=\alpha\wedge\omega$.

If both forms are smooth, choose a finite $S>0$ large enough that $\ker\beta_S$ belongs to the neighborhood from Fact 1. It is tight. Apply Fact 2 to $s\in[0,S]$ to conclude that $\ker\beta_0=\ker\omega$ is tight. There is no application of Gray stability at $s=\infty$ or at a foliated endpoint.

## 4. Preserving the source regularity

We give the regularization details to cover $C^1$ defining and connection forms. Orient each component of $M$ so that $\omega\wedge d\omega>0$; reversing this auxiliary orientation does not change the existence of an overtwisted disk.

Choose $S$ using (4). We claim that **every smooth one-form sufficiently close to $\omega$ in $C^1$ defines a tight contact structure**.

To prove the claim, approximate $\alpha$ in $C^1$ by a smooth one-form $a$, and let $\eta$ be any smooth one-form sufficiently $C^1$ close to $\omega$. Such approximation of a $C^1$ section is obtained by convolution in finitely many smooth charts and a smooth partition of unity. On the fixed compact set $M\times[0,S]$ the family
\[
\eta+s a
\tag{5}
\]
is uniformly $C^1$ close to $\beta_s$. By (3), the contact volume of $\beta_s$ is bounded below by a positive constant independently of $s\in[0,S]$. The contact condition is open in the $C^1$ norm; consequently, for sufficiently small approximation errors, every form in (5) is contact. Moreover $\ker(\eta+S a)$ remains in the $C^0$ neighborhood of $T\mathcal F$ from Fact 1.

For completeness, fix a metric and write $\omega\wedge d\omega=c(x)\,dV$, where $c\geq c_0>0$. If both $\beta_s$ and $d\beta_s$ have norm at most $B$ on the fixed interval, and both the one-form and exterior-derivative errors are bounded by $\delta$, the error of their wedge product is at most $2B\delta+\delta^2$. Choose $\delta$ so that this is less than $c_0/2$. Errors in $\eta$ and $a$ can be chosen less than $\delta/(1+S)$. This gives the claimed uniform contact bound.

The endpoint of (5) is therefore tight, and smooth Gray stability applied to (5) makes $\ker\eta$ tight. This proves the claim. The approximating form $a$ need not define a foliation or satisfy (1); only closeness on this one finite interval is required.

We finish by recording explicitly why the claim implies tightness for $\omega$ itself.

**Lemma (smoothing an overtwisted disk together with its contact form).** Let $\theta$ be a $C^1$ contact form on a closed smooth three-manifold. If $\ker\theta$ has an overtwisted disk, then arbitrarily small $C^1$ neighborhoods of $\theta$ contain smooth contact forms with overtwisted disks.

**Proof.** First suppose the disk $D$ and its boundary $\gamma$ are smooth. Choose smooth tubular coordinates $(t,u,v)\in S^1\times D^2$ around $\gamma$, with $\gamma(t)=(t,0,0)$. Let $\theta_j$ be smooth forms converging to $\theta$ in $C^1$ and set
\[
q_j(t)=\theta_j(\gamma'(t)).
\]
Because $\theta(\gamma')=0$, one has $q_j\to0$ in $C^1(S^1)$. Choose a fixed smooth cutoff $\chi(u,v)$ equal to one near $(0,0)$ and supported in the tubular neighborhood. Extend the following correction by zero outside that neighborhood:
\[
\widehat\theta_j=\theta_j-q_j(t)\chi(u,v)\,dt.
\tag{6}
\]
Then $\widehat\theta_j\to\theta$ in $C^1$, so the corrected forms are contact for large $j$. Equation (6) makes $\gamma$ exactly Legendrian. Along $\gamma$, the planes $TD$ and $\ker\theta$ are distinct; this is a uniform open condition on the compact boundary. It persists for $\ker\widehat\theta_j$. Thus the same disk $D$ is overtwisted for each sufficiently large $j$.

If $D$ is only $C^2$, first approximate its embedding in $C^2$ by smooth embeddings $D_j$, with boundaries $\gamma_j$. Use a fixed smooth tubular chart around a smooth curve sufficiently close to $\gamma$; after reparametrization write
\[
\gamma(t)=(t,u(t),v(t)),\qquad
\gamma_j(t)=(t,u_j(t),v_j(t)),
\]
where $(u_j,v_j)\to(u,v)$ in $C^2$. Now set
$q_j(t)=\theta_j(\gamma_j'(t))$. Again $q_j\to0$ in $C^1$, because $\theta_j\to\theta$ in $C^1$ and $\gamma_j\to\gamma$ in $C^2$. Replace the correction in (6) by
\[
q_j(t)\chi\bigl(u-u_j(t),v-v_j(t)\bigr)\,dt.
\tag{7}
\]
Choose the support radius uniformly small in the fixed chart. Its $C^1$ norm tends to zero, since the graph derivatives remain uniformly bounded. The corrected smooth form annihilates $\gamma_j'$ exactly. Contactness and the boundary transversality for $D_j$ persist. Hence $D_j$ is an overtwisted disk for the corrected smooth form. This proves the lemma. $\square$

If $\ker\omega$ were overtwisted, the lemma would give smooth overtwisted contact forms arbitrarily $C^1$ close to $\omega$. This contradicts the claim established using (5). Therefore $\ker\omega$ is tight. $\square$

## 5. What the proof does and does not establish

The result applies to either sign of the contact volume and to the specified global relation (1). It does not require a normalized connection form. It uses constant shifts of $\omega$; for a variable function $h$, the volume of $\omega+h\alpha$ need not be unchanged.

The only global contact-topology inputs are the established tightness neighborhood theorem and smooth Gray stability. The smoothing argument does not assume smoothness of the foliation and does not require a low-regularity Gray theorem. The symbolic checks accompanying this document test the differential-form identities, signs, and the boundary correction; they do not prove the imported contact-topology results.

The source's conditional tightness question is fully addressed by this candidate. The construction or existence of any contact Godbillon–Vey form on a given foliation remains a separate question. We make no historical-priority claim. A related closed-defining-form deformation argument already appears in [DR, Proposition 3.4]; that proposition does not directly apply here because $\alpha$ need not be closed.

## References

- **[C]** D. Calegari, *Problems in foliations and laminations of 3-manifolds*, version 0.78 (2002), Question 13.2 and its preceding hypotheses, printed p. 29; tautness convention, Definition 1.1, p. 1. [Author preprint](https://arxiv.org/abs/math/0209081).
- **[ET]** Y. Eliashberg and W. P. Thurston, *Confoliations*, University Lecture Series **13**, American Mathematical Society (1998), especially the tightness-neighborhood result on p. 50. We verified the formulation through the explicit primary-paper statements [V11] and [DR], rather than claiming to have retrieved and read the entire book.
- **[V11]** T. Vogel, *Rigidity versus flexibility for tight confoliations*, Geometry & Topology **15** (2011), 41–121. Tightness near a taut foliation, p. 42; overtwisted-disk formulation, pp. 42–43. [Published full text](https://msp.org/gt/2011/15-1/gt-v15-n1-p03-p.pdf), [DOI](https://doi.org/10.2140/gt.2011.15.41).
- **[V16]** T. Vogel, *On the uniqueness of the contact structure approximating a foliation*, Geometry & Topology **20** (2016), 2439–2573. $C^1$ contact-plane convention, Definition 2.2, p. 2448; smooth Gray stability, Theorem 2.9, p. 2451. [Published full text](https://msp.org/gt/2016/20-5/gt-v20-n5-p01-p.pdf), [DOI](https://doi.org/10.2140/gt.2016.20.2439).
- **[DR]** H. Dathe and P. Rukimbira, *Contact deformations of closed 1-forms on torus bundles over the circle*, author preprint (2008), p. 5, Propositions 3.3–3.4. [Author preprint](https://arxiv.org/abs/0812.3389).

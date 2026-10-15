# Independent adversarial audit: PR #718, pointed geometry

**Verdict: PASS for the assigned geometric construction.** No essential mathematical gap was found in the minimal pointed family, its construction in arbitrary characteristic, its inertia elimination, its projectivity, or the surjectivity of its evaluation. This verdict is a proof audit of that family of arguments; it does not establish priority or authorize publication by itself.

Completed 2026-10-12, America/Los_Angeles. The candidate inspected was `tangent_seshadri_30004324_v2/candidate_proof.md`, SHA-256 `dcad7d7677b1fff7fe1b659fd5b2f2c97e4daa0f0fe7b914a7752f19ad89c5a8`. The frozen candidate was not edited. Historical AI geometry reviews and other current reviews were not read. No external person was contacted.

## 1. Exact target and success criterion

The target is: if a smooth integral projective variety $X$ of dimension $n\geq1$ over an algebraically closed field $k$, with no restriction on characteristic, has a closed point $x$ at which the Fulger–Murayama relative vector-bundle Seshadri constant satisfies $\epsilon(T_X;x)>0$, then $X\simeq\mathbf P^n_k$.

This matches [Fulger–Murayama, Conjecture 4.9, printed p.17](https://par.nsf.gov/servlets/purl/10198624), the earlier [arXiv version, Conjecture 5.9, printed p.22](https://arxiv.org/pdf/1903.00610v2), and [Fulger's Oberwolfach contribution, printed p.3289, PDF page 19](https://publications.mfo.de/bitstream/handle/mfo/3816/OWR_2019_53.pdf?isAllowed=y&sequence=1). The final-numbering FM manuscript was retrieved independently by direct HTTP after the web tool returned HTTP 502; its PDF hash matches the candidate's recorded hash.

For this review, success means proving, without an added Fano, globally nef tangent, general-point, characteristic-zero, or separability hypothesis, the following geometric conclusion used by the candidate:

> There is an integral projective parameter scheme $H$, an actual smooth family of projective lines $\pi:U\to H$, a global marking $\sigma:H\to U$, and a surjective morphism $e:U\to X$, with $e\sigma=x$. Each fiber map is birational onto a rational curve of the same minimal very ample degree through $x$.

The primary inputs needed for this conclusion are the restriction-to-curves formula, a rational curve through the designated point, the characteristic-free stable-map compactification, and the deformation theory of maps into a smooth target. The following sections reconstruct the remaining deductions independently.

## 2. Positivity and existence at the original point

FM's Example 3.20 and Corollary 3.21, printed pp.9–10, use normalized minimum quotient slopes, including iterated Frobenius pullbacks in positive characteristic. Applying their formula to a rational curve's normalization gives

\[
\min_i a_i\ \geq\ \operatorname{mult}_x(C)\,\epsilon(T_X;x)>0,
\qquad f^*T_X=\bigoplus_i\mathcal O_{\mathbf P^1}(a_i).
\]

Since the $a_i$ are integers, every $a_i\geq1$. On $\mathbf P^1$, Frobenius multiplies each splitting degree by $p$; normalization by the same power of $p$ is exact. Thus this conclusion does not require strong semistability of a bundle on a higher-genus curve. It is also unaffected by a singular image curve, because the pullback is to its smooth normalization.

The existence issue cannot be replaced by uniruledness at a general point. I inspected the proof of FM Corollary 4.6, printed p.16: it specifically invokes bend-and-break to produce a rational curve through the designated $x$. This supplies the nonempty set in the degree minimum below. The candidate imports this established corollary, rather than reproving its bend-and-break dependency.

For the normalization map, $df$ is generically injective: over the nonempty smooth locus of the integral image curve, normalization is an isomorphism and the curve embeds in smooth $X$. This is true over the perfect field $k$ in every characteristic. It is not true for an arbitrary purely inseparable cover; the distinction is respected by the candidate. In particular, the optional bound $-K_X\cdot C\geq n+1$ follows from the nonzero map $\mathcal O(2)\to f^*T_X$.

## 3. Minimum degree survives all geometric residue fields

Fix a very ample $A$, and let

\[
d=\min\{A\cdot C:C\subset X\text{ integral rational, }x\in C\}.
\]

It is a minimum of a nonempty set of positive integers. I checked the field-extension issue explicitly, since geometric points of the compactification need not be $k$-points.

If an algebraically closed extension $K/k$ contained a rational curve of $A$-degree $c<d$ through $x_K$, its normalization would define a $K$-point of the fixed-degree pointed Hom scheme

\[
R_c=\{h:\mathbf P^1\to X:h(0)=x,\ \deg h^*A=c\}.
\]

This scheme is of finite type: after embedding $X$ by $A$, maps of degree $c$ are parametrized by homogeneous forms of that degree, with the basepoint-free condition open and the target equations and fixed value algebraic. A nonempty finite-type scheme over algebraically closed $k$ has a $k$-point. The resulting image is a rational curve through $x$, of degree at most $c$, contradicting minimality. The image is rational by Lüroth's theorem, which applies to subfields of $K(t)$ in positive characteristic as well. This argument also handles a $k$-map that is a multiple cover.

No uncountability or very-general-point hypothesis is being used.

## 4. All pointed boundary objects are excluded

Take a geometric stable map $(g:D\to X,p)$ of arithmetic genus zero, total $A$-degree $d$, and $g(p)=x$. Its domain is a connected nodal tree of projective lines. Follow the components contracted to $x$ from the marked component until a first nonconstant component $D_v$ occurs. One must occur because the total degree is positive, and its image $C_v$ contains $x$.

Writing $e_w$ for each nonconstant component's full generic degree onto its image gives

\[
d=\sum_w e_w(A\cdot C_w)
\geq e_v(A\cdot C_v)\geq A\cdot C_v\geq d.
\]

All terms are positive integers. Equality therefore forces one nonconstant component, $e_v=1$, and $A\cdot C_v=d$. The full degree is required here: a purely inseparable cover of degree $p$ contributes $p(A\cdot C_v)$, not just the separable degree.

Any nonempty connected contracted subtree with $t$ vertices attaches to the unique nonconstant vertex along precisely one edge. With $m\leq1$ markings on the subtree, its total number of special-point incidences is

\[
2(t-1)+1+m\leq2t<3t.
\]

The stability requirement of at least three special points on every contracted component is impossible. This also rules out a ghost carrying the marked point; it does not silently assume that the mark originally lay on the nonconstant component.

The arithmetic-genus-zero assumption excludes cycles, self-nodes and positive-genus components. Consequently the domain is genuinely smooth $\mathbf P^1$, and the map is birational onto its image. This is a proof for every geometric boundary object, rather than a statement about generic members only.

## 5. Positive-characteristic stabilizers and nonreduced bases

[Abramovich–Oort, Theorem 2.8 and §2.5, printed p.5](https://arxiv.org/pdf/math/9808074) supply a proper finite-presentation Artin stack for fixed genus, number of markings and degree, together with a projective coarse scheme, for a projective finite-presentation target. Their §2.3 also establishes finiteness of the Isom schemes. A very ample embedding of $X$ satisfies their target hypothesis. No Deligne–Mumford or tame-stabilizer assumption is made here.

Let $\mathcal M_x$ be the *actual* fiber of the one-mark evaluation over $x$. For a geometric object of this fiber, an automorphism preserving $g$ is the identity on a dense open set because $g$ is birational. This kills geometric automorphisms but, by itself, would not kill a nonreduced group scheme in characteristic $p$.

The tangent space of its automorphism group is

\[
\ker\bigl(H^0(\mathbf P^1,T_{\mathbf P^1}(-p))
\xrightarrow{dg} H^0(\mathbf P^1,g^*T_X)\bigr).
\]

Generic injectivity of $dg$ makes this kernel zero, even if the image has cusps or $g$ ramifies at isolated points. A regular vector field zero on a dense open set is zero everywhere. A finite group scheme over algebraically closed $k$ with one geometric point has a finite local coordinate algebra $B$. Vanishing tangent space says $\mathfrak m/\mathfrak m^2=0$; Nakayama gives $\mathfrak m=0$, so $B=k$. Thus the stabilizer is the identity scheme.

I separately checked the extension from geometric stabilizers to inertia over a possibly nonreduced base. Pull the finite inertia to any scheme atlas $S\to\mathcal M_x$, and write its finite coordinate algebra as $\mathcal A$. The identity section gives a split augmentation

\[
\mathcal A=\mathcal O_S\oplus J
\]

as modules. Formation of this summand commutes with residue-field extension. Every geometric fiber has coordinate algebra exactly its residue field, so $J$ has zero geometric fibers. Since it is finite, Nakayama gives $J=0$. The inertia morphism is therefore an isomorphism, including over nilpotent thickenings. [Stacks, Tag 04SZ](https://stacks.math.columbia.edu/tag/04SZ) now applies, giving an algebraic space.

This last argument is essential. Merely checking geometric automorphism *sets* would not justify the construction in wild characteristic.

## 6. Projectivity of the actual evaluation fiber

Let $Q$ be the projective coarse scheme of the full one-mark degree-$d$ stable-map stack. There is a natural morphism $\mathcal M_x\to Q$, without any coarse-space base-change assertion.

Its properness follows because $\mathcal M_x$ is proper over $k$ and $Q$ is separated over $k$: factor the morphism through its closed graph followed by the proper projection $\mathcal M_x\times_kQ\to Q$. It is of finite type. The coarse-map property identifies geometric isomorphism classes, so a geometric fiber of this restriction contains at most one point. A finite-type geometric fiber with at most one closed point is zero-dimensional, and the morphism is quasi-finite. Nilpotent structure in such a fiber does not invalidate quasi-finiteness.

[Stacks, Tag 03XX](https://stacks.math.columbia.edu/tag/03XX) applies to this separated locally quasi-finite morphism of algebraic spaces over the scheme $Q$, proving that $\mathcal M_x$ is a scheme. [Tag 02LS](https://stacks.math.columbia.edu/tag/02LS) then makes the proper quasi-finite morphism finite. Finite morphisms are projective, so $\mathcal M_x$ is projective over $k$.

The proof does not require that $\mathcal M_x$ equal the closed fiber of an evaluation morphism on $Q$, nor that coarse-space formation commute with arbitrary closed base change. Those are genuine potential pitfalls in characteristic $p$, and neither is present in the candidate.

## 7. Universal curve and the local Hom quotient

Because the inertia-free stack is a scheme, pulling its universal object back to a scheme component gives an actual family of curves, map and marking. This avoids a hidden gerbe or an unavailable universal family on a coarse scheme.

Every geometric fiber is $\mathbf P^1$. Properness, flatness, finite presentation and smooth geometric fibers make the curve family smooth; see [Stacks, Tag 01V8](https://stacks.math.columbia.edu/tag/01V8). Its section is an effective Cartier divisor. For $L=\mathcal O_U(\sigma)$, every fiber has $L|_{U_h}=\mathcal O_{\mathbf P^1}(1)$, with $h^0=2$ and $h^1=0$. [Tag 0B91](https://stacks.math.columbia.edu/tag/0B91) gives a locally free rank-two pushforward $E=\pi_*L$, compatible with base change. The evaluation $\pi^*E\to L$ is surjective by fiberwise surjectivity and Nakayama, defining $U\to\mathbf P_H(E)$ under the quotient convention of [Tag 01OA](https://stacks.math.columbia.edu/tag/01OA).

To spell out the candidate's compressed projective-bundle assertion, let $\phi:U\to\mathbf P_H(E)$ be the map just constructed. The induced degree-one map on every geometric $H$-fiber is an isomorphism. Thus every geometric fiber of $\phi$ is one reduced point. Since $\phi$ is proper, it is finite by Tag 02LS. On an affine open of its target the finite algebra map to $\phi_*\mathcal O_U$ becomes an isomorphism after passage to each geometric $H$-fiber. Its finite cokernel vanishes by Nakayama, so $\phi$ is a closed immersion. In the resulting ideal sequence, the quotient is flat over $H$ because $U$ is flat over $H$. Tensoring with a residue field is therefore exact on the left. The defining ideal has zero fibers, and Nakayama makes it zero. Thus $\phi$ is an isomorphism. This proof works over a nonreduced base as well, so it can be applied locally to $\mathcal M_x$ before selecting a reduced component.

Let $R_d$ be the degree-$d$ Hom scheme with $0\mapsto x$. Its map to $\mathcal M_x$ is the torsor of parametrizations of the pointed source under

\[
B=\operatorname{Aut}(\mathbf P^1,0),
\]

a smooth group of dimension two in every characteristic. Indeed a smooth $\mathbf P^1$-family with a section is locally a pointed projective-line bundle, by the preceding degree-one construction; locally framing $E$ compatibly with the section trivializes it. Thus $[R_d/B]$ describes this pointed-map moduli locally, and $R_d\to\mathcal M_x$ is smooth.

This fills in the most compressed sentence of the candidate (line 98). Since $H^1(f^*T_X(-0))=0$, $R_d$ is smooth at $f$. Smooth-local descent makes $\mathcal M_x$ smooth at $[f,0]$, so there is exactly one local irreducible component there. A sufficiently small neighborhood in $\mathcal M_x$ agrees with the reduced component $H$. Consequently a neighborhood of $f$ in $R_d$ genuinely maps into that chosen $H$; no component switching or circular assumption is needed.

The projectivity of $H$, and then of $U\simeq\mathbf P_H(E)$, follows. Smoothness over reduced $H$ gives reduced total space; flatness and geometrically integral fibers over integral $H$ give irreducibility. Hence $U$ is an integral projective variety, even though $H$ need not be smooth everywhere.

## 8. Evaluation is surjective, without generic smoothness

For a second fixed source point $\infty\ne0$, the obstruction group for evaluation at $\infty$ on $R_d$ is

\[
H^1(\mathbf P^1,f^*T_X(-0-\infty))
=\bigoplus_i H^1(\mathbf P^1,\mathcal O(a_i-2))=0.
\]

The equality remains valid at the borderline $a_i=1$, since $H^1(\mathcal O(-1))=0$. One does not need $a_i\geq2$ for every summand.

In a square-zero lifting problem with the value at $0$ fixed and the value at $\infty$ prescribed, smoothness of $X$ permits local lifts on an affine cover of the source. Adjustments respecting the prescribed values lie in $f^*T_X(-0-\infty)$, and differences of lifts give a Čech cocycle in that sheaf tensored with the square-zero ideal. The displayed vanishing removes the obstruction. Vanishing persists on a neighborhood by semicontinuity and cohomology/base change. The finite-presentation infinitesimal criterion gives smoothness of evaluation near $f$; see [Stacks, Tag 02H6](https://stacks.math.columbia.edu/tag/02H6). [Gounelas, Proposition 4.7 and proof, printed p.299](https://ems.press/content/serial-article-files/26314?nt=1) independently supplies the two-point tangent calculation over an algebraically closed field without restricting characteristic.

Restrict the Hom neighborhood to the unique component neighborhood just described. Each nearby map with source point $\infty$ defines a point of $U_H$, so the image of its smooth evaluation, a nonempty open subset of $X$, is contained in $e(U_H)$. Because $U_H$ is proper and $X$ separated, $e(U_H)$ is closed. A closed subset of irreducible $X$ containing a nonempty open subset is all of $X$. Thus $e$ is surjective.

This argument does not invoke characteristic-zero generic smoothness or assume that an arbitrary evaluation is separable. It proves smoothness at the selected very free map.

## 9. Adversarial boundary controls

The following checks were used to try to break the argument. They did not produce a counterexample under its hypotheses.

- **A Frobenius cover in characteristic $p$:** for $g(t)=t^p$, $dg=0$, and the infinitesimal scaling $t\mapsto(1+\varepsilon)t$, $\varepsilon^2=0$, preserves $g$ while fixing $0$. Thus geometric-point automorphism checks alone would fail. Such a map has full degree $p$ onto its image, and the degree-minimum equality excludes it.
- **A birational cusp:** the parametrization $(t^p,t^{p+1})$ has rational inverse $t=y/x$ on the generic locus and differential $(0,t^p\,dt)$. Its differential is nonzero generically, although zero at a special point. This supports the actual condition used to kill vector fields; global immersion is unnecessary.
- **An extra marking:** a contracted component attached once to the nonconstant curve becomes stable if it carries two markings. Hence the no-ghost argument is special to one marking, as the proof explicitly assumes. Applying it unchanged to two marks would be incorrect.
- **A non-very-free splitting:** if an $a_i=0$ were allowed, its contribution to $H^1(f^*T_X(-0-\infty))$ would be $H^1(\mathcal O(-2))\ne0$. The strict Seshadri positivity excludes precisely this obstruction.
- **Dimension one:** positivity forces $\deg T_X=2-2g>0$, so $X\simeq\mathbf P^1$. The family argument is consistent: the parameter component may be zero-dimensional and its universal line still covers $X$.
- **Countable algebraically closed fields, arbitrary extension fields, singular image curves, and a mark initially on a ghost:** none require a new hypothesis, for the reasons in §§3–5.
- **Product and blowup intuition:** a rational curve with a trivial or nonpositive normal direction through $x$ would give a nonpositive minimum tangent splitting, failing the actual hypothesis. Such standard alternatives do not contradict the proof.

The reproducible script `check_boundary_controls.py` enumerated 50,068 labeled rooted marked tree configurations with two through six vertices. It found no stable boundary configuration with exactly one nonconstant vertex and one mark; its two-mark control is stable. It also checks the relevant $\mathbf P^1$ cohomology dimensions and derivative coefficients in characteristics $2,3,5,7,11$. Results are in `boundary_controls_results.json`. These finite controls are auxiliary attempts at falsification; the universal tree-count, degree and cohomology arguments above are the proofs.

## 10. Strongest verified result, remaining gap and recommendations

The strongest result verified by this approach family is the complete projective pointed-family conclusion stated in §1, including the actual global marking and surjective evaluation, in arbitrary characteristic. This is the geometric input required by the candidate's numerical Picard-rank argument. I also checked that the marked-section construction satisfies the hypotheses of [Stacks, Tag 0EX7](https://stacks.math.columbia.edu/tag/0EX7), with the universal structure-sheaf pushforward provided by [Tag 0GKA](https://stacks.math.columbia.edu/tag/0GKA); no missing global section or Brauer obstruction remains at that interface.

**Exact remaining mathematical gap in the assigned family: none identified.** The finite computation is not a substitute for any imported theorem. The original-point existence result is imported from the inspected FM corollary, and stable-map properness/projectivity is imported from the inspected Abramovich–Oort theorem. Their full foundational dependencies were not independently reproved here.

For a publication, I recommend retaining the explicit two-sentence torsor justification in §7, or an equivalent named lemma, instead of leaving the local Hom-to-component step as the sole phrase “quotienting locally.” This is an exposition improvement: the needed torsor is already supplied by the candidate's own projective-line bundle construction, and no new mathematical hypothesis or mechanism is required.

This report does not adjudicate the separate priority search, the complete final Fano-characterization dependency, manuscript readiness, or packet-integrity audit. The independent published FM Fano clause was inspected and is indeed stated in every characteristic. The proof audit's PASS must be combined with the other assigned reviews before any claim is promoted.

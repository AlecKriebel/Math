# Relative CM theta symbols: exact defects and the remaining integral lemma

**Shared pass:** PASS 1/5, relative-symbol lane only. **Outcome:** partial mathematical reduction, not a construction of the requested map and not a counterexample to its existence.

The frozen contract was read in full and checked at SHA-256 `e2337c221570da99bd5c9e0ea6ebae799ca5221101598f9b0fd220ffa0e0efef`. Throughout, the required coefficients remain $R=\mathbf Z[1/6]$, and the required absolute target remains $K_2(\mathcal O(N))\otimes R$. Any use below of additional localization is explicitly a comparison or an explanation of a failed route.

## 1. Main results of this lane

1. A direct pair of auxiliary Kato theta functions does **not** obey the generic elliptic triangle relation. Its defect has an explicitly nonconstant tame residue. The computation works in characteristic zero and remains nonzero after tensoring with $R$. It obstructs the naïve geometric recipe, not its possible specialization or the intended normalized construction.
2. The smoothing factor in the contract has a precise three-symbol expansion. Smoothing both entries and keeping only their product misses two mixed terms. Thus the usual auxiliary theta functions cannot simply replace the as-yet unnormalized theta values.
3. Extending an already constructed absolute homomorphism to relative homology is abstractly automatic. Requiring specified theta values creates an exact relation-and-divisibility obstruction, stated and proved below over $R$. This separates the actual research problem from merely choosing a splitting of relative homology.
4. A rational elliptic-unit triangle relation does not supply an $R$-integral triangle relation or a definition of the relevant $N$-primary symbols. A precise integral theta descent/face lemma is isolated below, including the all-component and nonsimplicial-face obligations.
5. For actual cusp-to-cusp geometric edges, the boundary lattice is automatically saturated. Therefore missing classical generators alone do not obstruct extension once exact agreement on absolute cycles has been proved. The hard issue is that agreement and the theta prescription, not arbitrary values on a free relative complement.

No zero map, unit-valued replacement theta, arbitrary division in $K_2$, or asserted universal elliptic-unit relation is used.

## 2. Source-grounded setup and scope

The original question [OWR, p.1567] asks for the integral absolute map and a theta-symbol relative restriction, while acknowledging that a degree-zero theta prescription must be supplied. The report's $h$ components and $R=\mathbf Z[1/6]$ are retained. The report does not specify the relative codomain; the frozen contract takes $M_N=K_2(L)\otimes R$, $L=F(N)$.

[LSSW, Introduction pp.5–6] does not prove the desired relative formulas. Its §3.4 gives a genuine auxiliary theta primitive, which is the starting point for the computations here. Its §§4.1–4.3 construct and descend specialized auxiliary cocycles; its coefficient ring there is $R_5=\mathbf Z[1/30]$. In particular, the existing auxiliary theorem must not be renamed an $R$-integral relative-symbol theorem.

For one CM elliptic curve $E/k$, first take an ordinary integer $n\geq2$ prime to 6. Let

\[
 m=n^2,\qquad H=E[n],\qquad A=m(0)-H,
\]

and let $f=f_n\in k(E)^\times$ be Kato's normalized theta function with divisor $A$. One may enlarge $k$ to contain $E[n]$ for a residue calculation. This is a genuine degree-zero theta function; neither a divisor $(0)$ alone nor a constant theta is involved. Existence and norm normalization are the one-dimensional theta construction used in [LSSW, §3.4] and recalled in [SV, §1.2, §6.3].

The integer $m$ is the degree of the isogeny $[n]:E\to E$, equivalently the norm of the principal ideal $(n)\subset\mathcal O$. The two-dimensional geometric smoothing factor is $m^2=n^4$. For a general auxiliary ideal $\mathfrak c$, the analogous notation is $m=N\mathfrak c$, with factor $m^2$. These quantities must not be interchanged.

Since $A$ is invariant under $[-1]$, the ratio $f(-z)/f(z)$ is a constant $\epsilon$. Applying $[-1]$ twice gives $\epsilon^2=1$. All symbols containing this constant vanish after tensoring with $R$. Thus $f$ may be treated as even for the following $R$-valued symbol computations, without assuming a sign normalization that has not been proved.

### Geometric symbol conventions in the first partial case

In a Euclidean ring $\mathcal O$, let $g\in\mathrm{GL}_2(\mathcal O)$ have columns $v_1,v_2$, with lower entries $c,d$. Its oriented edge is the geodesic from the cusp represented by $v_1$ to that represented by $v_2$. The third vector $v_0=-v_1-v_2$ gives the elementary triangle with lower labels $e=-c-d$. If its three vertices lie in the allowed relative cusp set, its oriented boundary forces

\[
 S(c,d)+S(d,e)+S(e,c)=0. \tag{T}
\]

Reversing orientation forces antisymmetry. Changing either column by a unit leaves its cusp unchanged and forces independent-unit invariance

\[
 S(\varepsilon_1c,\varepsilon_2d)=S(c,d),\qquad
 \varepsilon_i\in\mathcal O^\times. \tag{U}
\]

A classical symbol is evaluated only when its two endpoints are in the prescribed non-infinity cusp set; in particular its lower labels are nonzero modulo $N$, as required by the question. No value $\theta(0)$ is assigned. For the global problem, the cusp set must be the complement of the preimage of the designated infinity cusps under $X_1(N)\to X_0(N)$, consistently on every connected component. Merely declaring every formally nonzero coordinate pair to be a global representative is insufficient.

The triangular face presentation is especially useful for the Gaussian and Eisenstein fields. It is not the full face presentation for all five norm-Euclidean fields: [G, §4.2] exhibits quadrilateral faces for discriminants $-8,-7$ and hexagonal faces for discriminant $-11$. Non-Euclidean fields add genuine representative and generation issues. None is suppressed below.

For these auxiliary functions, orientation and unit symmetry are not the missing generic relation. If a CM unit $\varepsilon$ has order $r$, the divisor of $f_n(\varepsilon z)/f_n(z)$ is zero. This ratio is constant, and iterating the automorphism shows its $r$-th power is 1. The orders in an imaginary quadratic unit group divide 4 or 6 and are all invertible in $R$; their symbol contributions vanish. Antisymmetry is the usual Milnor $K_2$ relation. Thus the auxiliary symbol passes these elementary tests over $R$, while the triangle calculation below identifies a genuinely different failure.

## 3. An exact nonzero generic triangle defect

### Proposition 3.1

Over $k(E\times E)$, set

\[
 D_n=\{f(x),f(y)\}+\{f(y),f(-x-y)\}+\{f(-x-y),f(x)\}.
\]

Then $D_n\neq0$ in $K_2(k(E\times E))\otimes R$.

### Proof

It suffices to prove nonvanishing after extending $k$ so that a nonzero $T\in E[n]$ is rational: a zero element has zero image under field extension. Consider the prime divisor $D_T=\{T\}\times E$. Write $f_x=f(x), f_y=f(y), f_z=f(-x-y)$. At its generic point,

\[
 v_{D_T}(f_x)=-1,\qquad v_{D_T}(f_y)=v_{D_T}(f_z)=0.
\]

Fix the conventional Milnor tame symbol

\[
 \tau_D\{a,b\}=(-1)^{v_D(a)v_D(b)}\overline{a^{v_D(b)}/b^{v_D(a)}}.
\]

Then

\[
 \tau_{D_T}(D_n)=f(y)/f(-T-y)
                  =\epsilon^{-1} f(y)/f(y+T). \tag{3.1}
\]

Because translation by $T\in E[n]$ preserves $H=E[n]$,

\[
 \operatorname{div}_y(f(y+T))=m(-T)-H,
\]

and hence

\[
 \operatorname{div}_y\bigl(f(y)/f(-T-y)\bigr)=m(0)-m(-T)\neq0. \tag{3.2}
\]

The residue is therefore not a root of unity and has infinite order in $k(E)^\times$. Its divisor remains nonzero after tensoring with $R$, because the divisor group is free abelian. Thus its $R$-localized tame residue is nonzero and so is $D_n$. ∎

The Gersten convention used for symbols in [SV] is the reciprocal of the tame symbol displayed here. With that convention the residue in (3.1) is inverted; (3.2) changes sign. Nonvanishing is unaffected.

### What this proves and does not prove

This rules out treating ${f_n(cP),f_n(dP)}$ as a universally triangle-compatible recipe merely because $f_n$ is a genuine normalized theta function. Its universal functional identity is false. It does **not** show that any particular torsion specialization of $D_n$ is nonzero; a nonzero rational-function symbol can specialize to zero. It does not refute an unsmoothed theta/root prescription, an explicitly corrected symbol, or the original construction problem.

The calculation also explains why the existence of the geometric auxiliary cocycle is not already a relative edge formula. In the paper's product notation, an unshifted primitive is

\[
 v_n=f_x\boxtimes H_y+m(0)_x\boxtimes f_y,
\]

whose boundary is $m^2(0,0)-H\times H$. Swapping the axes changes this primitive by the boundary of a theta product, with sign depending on the Gersten convention. But being an endpoint primitive would require invariance under the entire cusp stabilizer, not just a computation under the swap. The nonzero triangle defect detects the missing compatibility of these choices. The shift $\mu_i$ in [LSSW, (3.4)] is essential to allow specialization at $(0,P_i)$; it does not by itself prove endpoint independence or relation (T).

## 4. The exact smoothing identity

### Proposition 4.1

Let $K$ be a field and let $\sigma$ be a field automorphism, acting also on $K_2(K)$. Let $u,v\in K^\times$, $m\in\mathbf Z$, and define

\[
 a=u^m/(\sigma u),\qquad b=v^m/(\sigma v).
\]

Then, integrally in $K_2(K)$,

\[
 (m^2-\sigma)\{u,v\}
   =\{a,b\}+\{a,\sigma v\}+\{\sigma u,b\}. \tag{4.1}
\]

The same formula holds for bilinear symbols on $K^\times\otimes R$, and over a common extension field if only the chosen theta roots are present there.

### Proof

Bilinearity gives

\[
\begin{aligned}
 \{a,b\}&=m^2\{u,v\}-m\{u,\sigma v\}-m\{\sigma u,v\}
                         +\{\sigma u,\sigma v\},\\
 \{a,\sigma v\}&=m\{u,\sigma v\}-\{\sigma u,\sigma v\},\\
 \{\sigma u,b\}&=m\{\sigma u,v\}-\{\sigma u,\sigma v\}.
\end{aligned}
\]

Adding leaves $m^2\{u,v\}-\{\sigma u,\sigma v\}$. ∎

For the intended CM normalization, take $m=N\mathfrak c$ and $\sigma=R_N(\mathfrak c)$, after verifying the specific theta distribution/CM reciprocity normalization. Then (a,b) are the corresponding smoothed theta values **if** that normalization has been proved. Formula (4.1) explains the calibration factor $N\mathfrak c^2-R_N(\mathfrak c)$ exactly. It also shows why replacing the intended symbol by $\{a,b\}$ alone does not implement the calibration.

The mixed terms still contain the original theta roots. This is a mathematical issue, not a notation issue. Formula (4.1) neither proves those terms descend to $L$, nor assigns a value by division in $K_2(L)$, nor proves the three-term right side agrees with the auxiliary geometric cocycle on cycles. Those are precise remaining comparisons.

For nonprincipal ideals, the isogeny may change the CM representative. The correct statement uses the theta system on the full collection of curves and the associated Artin action. One may not replace $\mathfrak c$ by a nonexistent scalar endomorphism of a fixed curve.

## 5. Root descent: the missing information is actual torsion

The intrinsic theta of [G, Corollary 2.6] for an $n$-torsion point is an element of $k^\times\otimes\mathbf Z[1/n]$; its displayed triangle witness in Definition 2.8 carries a factor (n^{-5}). Theorem 2.10 gives the rational Bloch-complex boundary formula. These are powerful guides to the face relation, but do not retain all the $n$-primary information required here.

Here are two exact elementary checks.

### Proposition 5.1: ambiguity of an actual root

If $\tilde u,\tilde v$ are roots in an extension $M$, replacing them by $\zeta\tilde u,\eta\tilde v$ changes their symbol by

\[
 \{\zeta,\tilde v\}+\{\tilde u,\eta\}+\{\zeta,\eta\}. \tag{5.1}
\]

If $\zeta$ and $\eta$ have orders dividing $n$, the difference is $n$-torsion, but it need not be killed by $R$ when $n$ has a prime factor at least 5. The claim follows immediately from bilinearity. It is not legitimate to discard (5.1) merely because it consists of roots-of-unity symbols.

For a concrete illustration, in $K=\mathbf Q(\zeta_5)$ choose a prime $v$ above 11 and a uniformizer $\pi$ at $v$. The residue field has characteristic 11 and contains the reduction of $\zeta_5$ of order 5. Thus $\tau_v\{\zeta_5,\pi\}=\bar\zeta_5\neq1$, proving that $\{\zeta_5,\pi\}$ is a nonzero 5-torsion class after tensoring with $R$. This is an example of the formal root-choice problem; it is **not** asserted to be one of the elliptic-unit values required by the question.

### Proposition 5.2: localization does not define a lift

For any $R$-module $M$, the kernel of $M\to M[1/n]$ is exactly the set of elements killed by some power of $n$. Therefore a specified class in $M[1/n]$, if it has a lift to $M$, determines only a coset of that kernel. The assertion follows from the definition of localization. When $M$ is finite, localization removes precisely the primary components at the prime divisors of $n$.

Consequently a rational elliptic-unit identity cannot be pulled back to an integral identity by “taking the unique root”: uniqueness is exactly what can fail on the desired target. Nor does Galois invariance over an extension establish an integral descent class. A transfer argument dividing by the extension degree is permissible only when that degree is a unit in the coefficient ring, or when a separate annihilator argument has been proved.

### The available triangle mechanism, and its remaining integral step

For torsion points (a,b,c,x), use rational functions with divisor (n((a)-(x))), and their analogues for (b,c). The $K_3$ reciprocity calculation underlying [G, proof of Theorem 2.10] gives a four-term relation between elliptic triangle expressions after the theta evaluation normalization and the divisions by $n$ are justified. Averaging (x) over $E[n]$ introduces another (n^2). Pairing (x) with $a+b-x$ cancels the averaged side terms using evenness and antisymmetry. This is a useful source of a triangle identity after inverting $n$, not a cancellation of the $n$-primary obstruction.

An integral proof must either replace this division-based argument by an integral cycle computation, or specify and control the remaining torsion class before specialization. The obstruction is not the nonexistence of a scalar-valued degree-one rational theta function. It is the missing integral symbol-level normalization and face identity.

## 6. Relative extension is automatic abstractly, but prescribed values are not

This section is independent of any unproved arithmetic assertion.

Let (X) be a finite CW model for the compactified Bianchi space, with all its connected components, and $C$ the finite set of allowed cusps. Set

\[
 A=H_1(X;R),\quad B=H_1(X,C;R),\quad
 D=\ker(H_0(C;R)\to H_0(X;R)).
\]

The long exact sequence and $H_1(C;R)=0$ give

\[
 0\longrightarrow A\stackrel j\longrightarrow B
 \stackrel\partial\longrightarrow D\longrightarrow0. \tag{6.1}
\]

The module $D$ is free: in every component meeting $C$, a chosen base cusp gives the basis of differences of the other cusps with that base cusp. Thus (6.1) splits over $R$.

### Proposition 6.1

Every $R$-homomorphism $f:A\to M$ extends to $B$, for any $R$-module $M$. Its extensions form a torsor for $\operatorname{Hom}_R(D,M)$.

**Proof.** Choose a section $s:D\to B$. Then every element of $B$ has a unique form $j(a)+s(d)$. Define $F(j(a)+s(d))=f(a)+q(d)$, for arbitrary $q:D\to M$. Any two extensions differ by a map factoring through $D$. ∎

This proposition does not produce theta values or the intended normalization. It explains why proving only existence of an unspecified relative extension would make no progress on the central formula.

### Proposition 6.2: an exact criterion for specified symbols

Suppose $e_i\in B$ are the admissible geometric symbol classes and $t_i\in M$ are proposed, already well-defined theta-symbol values. Fix a section $s$ and uniquely write

\[
 e_i=j(a_i)+s(d_i),\qquad r_i=t_i-f(a_i).
\]

Let $D_S\subset D$ be generated by the $d_i$. An extension of $f$ with $F(e_i)=t_i$ exists if and only if:

1. Every finite $R$-linear relation $\sum_i\lambda_i d_i=0$ satisfies $\sum_i\lambda_i r_i=0$. This defines a homomorphism $q_S:D_S\to M$.
2. That homomorphism extends to $D$. Equivalently its connecting class in $\operatorname{Ext}^1_R(D/D_S,M)$ is zero.

Because $R$ is a PID, the second condition is concrete. In Smith form, choose a basis $b_1,\ldots,b_t$ of $D$ and write a basis of $D_S$ as $n_1b_1,\ldots,n_rb_r$. It is equivalent to

\[
 q_S(n_jb_j)\in n_jM \quad (1\leq j\leq r). \tag{6.2}
\]

Here the $n_j$ may be taken as integers after multiplication by units of $R$. No division in $M$ has been assumed.

**Proof.** An extension has the form in Proposition 6.1, and its prescribed values require $q(d_i)=r_i$. Condition 1 is exactly well-definedness on $D_S$; Condition 2 is exactly extension of that homomorphism. Applying $\operatorname{Hom}_R(-,M)$ to $0\to D_S\to D\to D/D_S\to0$ gives the Ext criterion. In Smith coordinates, choosing $q(b_j)$ is possible precisely when (6.2) holds, and the remaining basis values are free. ∎

### Corollary 6.3: genuine edge boundaries are saturated

Suppose every prescribed $e_i$ is an actual oriented path from a cusp $v_i\in C$ to a cusp $w_i\in C$, so that $d_i=w_i-v_i$, without nonunit multiplicity. Form the graph $G_S$ on the vertex set $C$ with these edges, allowing loops. Then $D_S$ is a saturated submodule of $D$. Therefore an extension exists if and only if

\[
 \sum_i\lambda_i t_i
   =f\left(j^{-1}\left(\sum_i\lambda_i e_i\right)\right)
 \quad\text{whenever }\sum_i\lambda_i(w_i-v_i)=0. \tag{6.3}
\]

**Proof.** The image of the incidence map of a graph is exactly the vectors of (R[C]) whose coefficients have zero sum within each connected component of the graph. One inclusion is immediate; the reverse follows by choosing a root and paths in each graph component, writing any such vector as a sum of endpoint differences. Thus $R[C]/D_S\cong R[\pi_0(G_S)]$. Every graph component lies in one connected component of (X), and

\[
 D/D_S\cong\ker\bigl(R[\pi_0(G_S)]\longrightarrow R[\pi_0(X)]\bigr),
\]

which is free. Hence the extension obstruction of Proposition 6.2 vanishes. Condition 1 of that proposition is exactly (6.3), because a balanced sum of the $e_i$ belongs to (j(A)). ∎

Connectivity of the whole admissible-edge graph is **not** needed. If it is connected in each relevant component of (X), then $D_S=D$; otherwise unspecified values on a free complement remain. Thus failure of classical symbols to generate full relative homology is not, by itself, an algebraic obstruction once the absolute map and all their cycle agreements are in hand. It obstructs pretending the classical formulas alone specify the complete map canonically. The problem does not demand a canonical splitting or relative Hecke equivariance, so neither is introduced as a new acceptance requirement here.

The Smith divisibility warning remains relevant if “symbols” are weighted or averaged chains with nonunit endpoint multiplicities. It is not an extra obstacle for ordinary unweighted cusp edges.

For the construction problem, take $M=M_N$ and $f=\iota\Pi_N$. A local face relation such as (T) is one instance of (6.3), with zero absolute class. Endpoint-balanced sums representing nonzero absolute classes must also agree with $f$; verifying only the triangular zero relations would not prove this. An arbitrary extension has no automatic Galois, diamond or Hecke compatibility on its relative complement. Only the compatibility explicitly required by the frozen contract should be claimed.

## 7. A sharp integral theta/face lemma still to prove

The following is the outstanding statement needed by the relative-symbol route. It is a **research lemma**, not a theorem established here.

### Integral CM theta descent and face lemma

For each imaginary quadratic $F$, every proper nonzero ideal $N$, and every CM marking appearing in the $h$ Bianchi components, construct classes

\[
 s_N(e)\in K_2(F(N))\otimes R
\]

on admissible oriented geometric edges, or on a specified larger chain model when classical edges do not generate, with these properties:

(a) **Intrinsic theta identification.** The classes come from the canonical CM theta/elliptic-unit system, with a specified degree-zero normalization or an intrinsic substitute. After any coefficient extension where the conventional theta values are defined, their Steinberg expressions agree. An actual construction over $R$, including its torsion information, is given; merely specifying their rationalizations is not enough.

(b) **Choice and descent identities.** Changes of root, auxiliary divisor or ideal, CM-model field, lattice basis and unit representative produce the same class in $K_2(F(N))\otimes R$. Artin action and isogeny changes of CM component are compatible. The proof must control the actual terms (5.1), not just their rational images.

(c) **Relations.** Antisymmetry and independent-unit invariance hold. For every admissible elementary triangle, the sum in (T) vanishes over $R$. For a geometric quadrilateral or hexagon, the oriented sum over its sides vanishes. If such a polygon is triangulated through a non-unimodular diagonal, values on the new diagonal must be constructed and shown independent of the triangulation; the triangle statement restricted to unimodular pairs does not imply this. For a direct chain-map construction the corresponding relations must be proved for every 2-cell of the chosen all-component model. Alternatively, the extension criterion in part $e$ avoids prescribing unnecessary values on extra generators; whenever an entire face boundary consists of prescribed edges, its relation is still mandatory.

(d) **Absolute-cycle calibration.** For every loop $z$ in the open Bianchi space and each auxiliary ideal $\mathfrak c$ for which [LSSW] supplies its map, the sum of the normalized edge classes, after passage to $R_5$ and the paper's localized target, satisfies

\[
 (N\mathfrak c^2-R_N(\mathfrak c))\,s_N(kz)
       ={}_{\mathfrak c}\Pi_N(z). \tag{7.1}
\]

Here $k$ is the map into compactified homology. If a representative crosses disallowed cusps, its interpretation must be given using an actual relative chain and the cocycle/trivialization comparison, not by evaluating theta at zero. This requirement is only on absolute cycles: the frozen contract does not require imposing new Hecke or smoothing identities on the whole relative map.

$e$ **Full extension.** The exact absolute-cycle agreement (6.3) holds for genuine edges, or the more general conditions of Proposition 6.2 hold for a weighted chain convention. Corollary 6.3 then supplies the extension even when classical symbols do not generate; its free-complement choices must be disclosed rather than misrepresented as canonical. In each nontrivial ideal-class component, the formula uses the appropriate $E_r$ and $E_s$. For instance, in the component with product $E_r\times E_1$, a matrix with lower entries $c\in\operatorname{Hom}(E_1,E_r)$, $d\in\mathcal O$ specializes at $(0,P_1)$ to $(cP_1,dP_1)$. The first theta value is on $E_r$, not silently on $E_1$.

Parts (a)–(c) are already substantive in the Gaussian or Eisenstein Euclidean case. Parts (d)–$e$ are additional global conditions. Part (d) is the contract’s explicitly adopted calibration with the later family, rather than a verbatim condition of the original report. It only holds after inverting 5 and hence cannot by itself certify the exact agreement in part $e$. No proof that these statements hold, and no example disproving them, has been obtained in this pass.

Even if this lemma were proved, the exact integral **absolute** target, good-prime Eisenstein relation and the contract's additionally adopted bad-prime identities must still be established. The $R$-valued relative field target alone does not imply any of those arithmetic claims.

## 8. What would be useful next, without opening a new pass here

The next construction step should be an integral torsion-sensitive comparison of a candidate edge symbol with the specialized Gersten cocycle, rather than another rational theta identity. For an explicit small Euclidean test, compute the torsion-specialized triangle defect together with the two mixed terms in (4.1), in a finite quotient or an étale realization that detects the relevant prime-primary component. A zero regulator or zero rational class would not test the missing information.

For a proof route, the most targeted object is an integral theta reciprocity witness whose boundary is the triangle sum and which is independent of the torsion-root choices. The source's division by powers of the level must be replaced or shown harmless on the specific class. After that, polygonal faces and Proposition 6.2 give explicit remaining extension tests. All-field and all-component scope remains outstanding.

## References and inspection boundary

- **[OWR]** R. Sharifi, “Eisenstein cocycles for imaginary quadratic fields,” *Oberwolfach Reports* 20 (2023), pp.1565–1568; especially p.1567. Official source: https://ems.press/content/serial-article-files/47022 ; DOI https://doi.org/10.4171/OWR/2023/28 . Read from the retained primary packet.
- **[LSSW]** E. Lecouturier, R. Sharifi, S.-C. Shih, J. Wang, *Eisenstein cocycles for imaginary quadratic fields*, author-hosted 47-page manuscript: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . Introduction, §§3.1–3.4, 4.1–4.3 and relevant §5.1 setup inspected in the retained text. Fixed arXiv version: https://arxiv.org/pdf/2504.19125v1 . No new revision label is assigned to the author PDF.
- **[G]** A. B. Goncharov, *Euler complexes and geometry of modular varieties*, arXiv:math/0510310v5 (9 June 2007), §§2.2–2.4, 4.2–4.3, 5.1–5.4: https://arxiv.org/pdf/math/0510310v5 . The relevant formulas and coefficient rings were inspected in the primary PDF/text. The rational Euler-complex construction is not asserted to prove an integral $K_2$ map.
- **[SV]** R. Sharifi, A. Venkatesh, *Eisenstein cocycles in motivic cohomology*, author-hosted 87-page PDF: https://math.ucla.edu/~sharifi/eisensymbol.pdf . Introduction and explicit theta-symbol construction in §§6.3–6.4 inspected. Its norm-corrected product and parabolicity mechanism are useful comparison material; no automatic transfer of its theorem to all CM/Bianchi components is claimed.
- Cremona's original paper was located at https://numdam.org/item/CM_1984__51_3_275_0/ . A direct PDF download returned HTTP 502. Its full proof was not used. The Euclidean face information invoked above was checked in [G], a primary construction paper that explicitly develops those tessellations.

All propositions labeled proved above have proofs supplied here. The principal intended relative map, integral theta normalization, specialized face identity and cocycle calibration remain unproved.

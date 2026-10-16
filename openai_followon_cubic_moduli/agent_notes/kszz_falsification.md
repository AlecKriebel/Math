# KSZZ cubic comparison: independent falsification audit

Checkpoint: 2026-10-07 05:48 UTC (2026-10-06 22:48 PDT).

I read the complete 15-page cached manuscript, concentrating on Theorem 1.1, Theorem 2.7, Lemmas 2.8–2.9, the whole limiting-linear-system argument in Section 3, and the case division in Theorem 4.1. I separately delegated the DGP tangent-slope citation to an independent agent; its primary-source and algebraic checks are in `kszz_dgp_scope.md`.

Completion estimate: 95% of this scoped comparison-chain audit. This does not estimate completion of the project's publication goal. The exact published Shibata 2017 Proposition 3.13 remains unavailable in this run; an earlier primary source of the same author explicitly supplies the required general-Gorenstein formula. The final full stack/functor identification, which the manuscript imports by reference, was not independently reconstructed here. No publication package or approved manuscript was changed.

## Outcome and limits

No counterexample to the n≥5 comparison, and no irreparable central gap, was established. Several printed deductions or compressed steps need repair, but the repairs below use mechanisms already present in the cited literature or routine divisor arguments. They do not presently yield a new research theorem or a novelty-cleared substitute for the project’s original compactification target.

In particular, two plausible falsification routes did **not** succeed:

1. DGP24 is not confined to K-polystable or KE varieties at the paragraph used. Its semistability argument explicitly covers K-semistable Q-Fano varieties and the nef pullback polarization.
2. The multiplicity step should not be accused of circularly assuming lci based on the Shibata article’s abstract. The author’s 2014 primary abstract states a general Gorenstein-canonical bound that gives multiplicity at most two from the exact threshold used by KSZZ. The index-one cover has the needed Gorenstein property, even when X does not.

The publicly stated overlap therefore remains substantial. This audit is evidence about the actual proof mechanism, not a certification of every cited foundational theorem, not conventional human refereeing, and not proof of either the manuscript’s earliest public posting or this project’s novelty.

## Exact theorem and dimensions

Theorem 1.1 says every K-semistable Fano variety in the cubic smoothing component is a cubic, then claims equality of K/GIT semi-, poly-, and stability, a natural stack isomorphism and good-space isomorphism, and a smooth connected K-moduli component. The component is defined by Q-Gorenstein deformation to smooth cubic n-folds and anticanonical volume 3(n−1)^n. This is a cubic smoothing component, not the collection of every Fano with those two numerical invariants.

Section 3 explicitly assumes n≥5. Known n=2,3,4 results are cited in the introduction and final comparison. The text does not provide an independent new argument for cubic curves; its Fano setup excludes them. The central numerical exclusions genuinely use n≥5: 1/[2(n−1)]<1/(n+1), and the scroll S-invariant estimate has its weakest n≥5 value at n=5.

Theorem 4.1 is a statement about K-semistable Q-Gorenstein limits, stronger in algebraic scope than the original project's complex/polarized GH coarse-space target. Its final derivation of stack and nonclosed semistable claims refers to Liu–Xu and Liu. Those upgrades should not be imported into this project's narrower paper merely because the manuscript states them.

## Section 2: polarization, parity, covers and discrepancies

### A printed Gorenstein deduction is unjustified

Theorem 2.7(2) prints that 2L is Cartier and, “in particular,” X is Gorenstein canonical. The cited Liu22 Theorem 3.1 does not state this conclusion. Its actual four conclusions, valid for every n≥4, are:

- O_X(mL) is Cohen–Macaulay for every integer m;
- −K_X∼(n−1)L and L^n=3;
- all twist cohomologies agree with the smooth cubic fibers;
- every Q-Cartier integral Weil divisor has index at most two.

For odd n, (n−1)L is Cartier when 2L is Cartier, so the Gorenstein-canonical conclusion follows from the **integral linear** canonical relation and klt singularities. For even n, a hypothetical point of index two for L also has index two for K_X. Thus 2L alone cannot give the printed “in particular.” Using the desired eventual Cartierness of L to justify that sentence would be circular.

This does not by itself break the central proof. The only later place I found an explicit need for X to be Gorenstein canonical before proving L Cartier is the rank-four quadric paragraph. That paragraph can be repaired without the claim; see below. The L-index-one cover, unlike X, **is** Gorenstein canonical: Liu’s stronger integral relation −K_X∼(n−1)L pulls back to an integral multiple of the Cartier pullback of L. A quasi-étale cover preserves klt, and a Gorenstein klt variety is canonical. Retaining Liu’s integral relation, rather than only the displayed Q-linear version, makes this justification precise.

### Smooth index-one cover: a relative argument is omitted

If the degree-two L-index cover were smooth, local analytic linearization gives C^r/{±1}×C^(n−r) with r≥2. For r≥3, taking transverse sections preserves a smoothing and yields an isolated quotient singularity of dimension at least three, contradicting Schlessinger rigidity. This is consistent with the cited mechanism.

For r=2, the text says that X is a hypersurface and then applies Robbiano to force L Cartier. A general nonisolated hypersurface does not have a torsion-free local divisor class group: the A_1 surface germ xy=z^2, times a smooth factor, has the familiar order-two non-Cartier ruling class. Therefore the inference cannot rest only on the fact that the central fiber is a hypersurface.

There is a routine **relative** repair already exemplified in Liu22 Proposition 3.2. The total smoothing is a hypersurface germ of dimension n+1; its singular locus lies in the central A_1 locus, of dimension at most n−2. Cut the total space by n−2 general hyperplanes through the point to obtain a normal isolated three-dimensional hypersurface. The total divisorial sheaf O_𝓧(𝓛), which is Cohen–Macaulay, restricts as a rank-one reflexive sheaf on this cut. Its Q-Cartier class has finite order in the punctured local Picard group. Robbiano’s local result kills that order there. Lifting a generator and applying Nakayama then makes the total sheaf, and hence its central restriction O_X(L), free. This contradicts the assumed index two. The extra relative-CM argument is needed; it is not a new mechanism from this project.

The remaining local-volume inequality is numerically sound:

    volhat(x̃,X̃) ≥ 6 n^n (n−1)^n/(n+1)^n > 2(n−1)^n.

The strict comparison follows from (1+1/n)^n<e<3. Hence a singular lci cover is excluded by Liu’s lci ODP bound, once the smooth-cover case is handled correctly.

### Lemma 2.9: no direction failure found

On a local trivialization of 2L, the odd functions f_i on the index cover satisfy J^2=I O_X̃, where I is the ideal generated by degree-two products of sections. On the normalized graph I O_W=O_W(−2E). A normalized divisorial w restricting to c v has w(J)=c v(E). Quasi-étale Riemann–Hurwitz gives A_X̃(w)=c A_X(v). These identities have the displayed signs and factors.

At a non-Cartier point the index-cover group fixes its closed point; the f_i have the nontrivial character and vanish there, giving J⊂m_x̃. Thus lct(m_x̃)≥lct(J), in the direction used later. The threshold comparison does not confuse an upper bound on an infimum with a lower bound on a chosen valuation.

## Section 3: the intermediate-dimensional image

I checked this mechanism independently of the earlier project note.

1. The normalized graph has H=p*L, a nef Cartier moving divisor M, and effective Q-Cartier E=H−M. H+M is ample because it comes from the two factors of the graph; normalization is finite. Mixed intersections a_i=H^(n−i)M^i satisfy a_0=3 and a_i−a_(i+1)≥0 by effectivity and nefness.
2. Proposition 3.2 integrates the nef segment (1−u)H+uM. The beta integral gives S_X(v)≥[(n−1)/(3(n+1))] Σ_(i=0)^d a_i ·v(E). I verified the normalization by vol(−K_X)=3(n−1)^n; the coefficient and summation range agree.
3. Lemma 3.3’s equality of section dimensions is justified by inclusions in both directions: the moving sections define M, while every section of M, multiplied by the effective fixed part, yields a section of H and pushes forward to O_X(L). Connected fibers persist after resolving the Stein factorization.
4. The independently inspected DGP24 paragraph gives cotangent semistability against H on the smooth graph resolution. Pullback of Ω_Ỹ injects into Ω_W̃ generically, and its locally free source makes the sheaf kernel zero. Exceptional divisors have degree zero against H^(n−1). Thus

       q*K_Ỹ·H^(n−1)/d ≤ −3(n−1)/n.

   Adding (d−1)q*L_Ỹ gives degree at most −3(n−d)/n, strictly negative for d<n. A nonzero effective divisor cannot have negative degree against nef H. Consequently H^0(K_Ỹ+(d−1)L_Ỹ)=0. No canonical-discrepancy sign is needed for this slope calculation.
5. Big-nef Kawamata–Viehweg vanishing and the Koszul complex then give H^0(ω_C)=0 for the general smooth complete-intersection curve. Rational connectedness of the klt Fano resolution and its image gives H^(d−1)(ω_Ỹ)=H^1(O_Ỹ)=0. Bertini and connectedness give an integral C, so C≅P^1. Dual KV vanishing for negative twists computes h^0(C,L|_C)=n+3−d.
6. Since C is rational, deg L|_C=n+2−d. This degree equals deg(ν)deg(Y), whereas nondegeneracy gives deg(Y)≥n+2−d. Thus ν has degree one and Y has minimal degree. The conclusion is stronger than a merely low genus assertion.

**Printed sign error:** p.10 writes H^i(O_Ỹ(−tL_Ỹ))=0 for i<d and t<0. That is false, in particular for i=0 and a positive twist. The required and standard statement has **t>0**, by Serre duality and KV. The Koszul complex uses negative twists, so correcting this sign is sufficient for this step.

### Classification and exclusions

For image dimension one, a hyperplane with contact order at least n+1 at a general point exists by a linear jet-count. A component dominating that point varies and cannot always be p-exceptional. Its coefficient yields an alpha bound below 1/(n+1).

For minimal-degree scrolls with a summand at least two, and for cones over v_2(P^2), the moving hyperplane sections have a doubled prime component; pulling back to X gives alpha≤1/[2(n−1)]<1/(n+1). The phrase “smooth quadric surface v_2(P^2)” is a terminology error: the doubled-line construction is on the Veronese surface and is correct for it.

The remaining scroll has type S(0^(d−e),1^e), e=n+2−d≥3 and n−d=e−2. On its standard resolution, H_Z−G dominates the nef L_2 after subtracting a general ruling component G. The generic-fiber intersection of 2H_Z is a positive integer, so the projection formula gives

    H_Z^(n−e+1)L_2^(e−1) ≥ 2^(2−e).

Khovanskii–Teissier log-concavity then gives

    H_Z^(n−i)L_2^i ≥ 3 [1/(3·2^(e−2))]^(i/(e−1)).

For i=1 and i=2, the factors are at least √6/6 and 1/6. Consequently, for n≥5,

    S_X(B) ≥ (n−1)/(n+1) · (1+√6/6+1/6)
           ≥ (7+√6)/9 > 1=A_X(B).

The last strict inequality is equivalent to √6>2. No floating-point decision is necessary. The undefined switch from D to B in the printed argument is a variable typo; the nonexceptional ruling prime is the valuation meant. The mechanism excludes every intermediate dimension that the classification allows.

## Section 4: the generically finite image

The mixed degree bound gives 2≤deg(q)deg(Y)≤3, while a nondegenerate hypersurface has degree at least two. Thus the map is birational and the image is a quadric or cubic.

### Quadric of rank at least five

The effective divisor D=q_*(2E) is nonzero: if zero, E is q-exceptional and q-nef, so the negativity lemma forces E=0, contrary to H^n=3 and M^n=2. The degree estimate is deg(D)≤2. Since Cl(Y)=Z[L_Y] and L_Y^n=2, D∼L_Y and deg(D)=2. Therefore a_0=…=a_(n−1)=3 and a_n=2.

The S-invariant coefficient becomes

    κ=(n−1)(3n+2)/(3(n+1))
      = n−1−(n−1)/(3(n+1)) > n−2.

Lemma 2.9 and K-semistability give lct(X̃;m_x̃)≥κ. The needed multiplicity implication is for **Gorenstein canonical** singularities, not for arbitrary klt singularities. Those assumptions hold on the L-index cover using Liu’s integral canonical relation.

I did not obtain the exact 2017 Proposition 3.13: publisher full-text retrieval was unavailable, and the ordinary browser journal page requested a CAPTCHA, which I did not solve. This prevents claiming that I checked that exact numbered published statement.

However the author's primary 2014 symposium abstract states the required formula explicitly. With v=embedding dimension and c=ceil(lct(m_x)), its Proposition 1 says for a general n-dimensional Gorenstein canonical variety that, when n+1−c=2r,

    mult_x X ≤ 2 binomial(v−n+r−1,r−1).

With c=n−1 and r=1 this is exactly mult≤2; the adjacent c=n case gives mult≤1 from the other parity formula. Thus the possible lci circularity suggested by the 2017 abstract is not established. A fuller bibliographic verification should match the 2017 numbered statement to this primary precursor.

A normal klt local ring is Cohen–Macaulay. Abhyankar’s multiplicity inequality then gives edim≤n+1 from mult≤2. A normal complete local domain of codimension at most one in a regular local ring is a hypersurface (or smooth). This contradicts the earlier cover exclusion. I found no noncircularity problem once the correct general-Gorenstein multiplicity bound is used.

### Rank-four quadric: repair without X being canonical

The text introduces F=q_*(K_W−p*K_X) and calls it an effective integral Weil divisor because X is Gorenstein canonical. That claim inherits the parity problem in Theorem 2.7. The needed class contradiction survives if F is instead a **signed rational Weil divisor**.

The discrepancy divisor is supported on p-exceptional primes. Every p-exceptional prime of the normalized graph lies over the base locus and has positive order on I; by I O_W=O_W(−2E), it lies in Supp(E). Thus Supp(F)⊂Supp(D), regardless of discrepancy signs. Birational pushforward gives

    [F]=((n−1)/2)[D]−[L_Y] in Cl(Y)_Q.

Write [D]=a[L_1]+b[L_2] with a,b≥0 integral and 1≤a+b≤2. The effective cone of the rank-four quadric is the nonnegative ruling quadrant. If b=0, every prime in Supp(D) has class in Z[L_1], so every signed rational divisor supported there has class in Q[L_1]. The displayed formula instead has L_2 coefficient −1. This is a contradiction. The case a=0 is identical. Thus a=b=1 and D∼L_Y, reducing to the rank-at-least-five threshold argument. Effectiveness and integrality of F are unnecessary.

This is a short repair to a printed assumption, not an independently new comparison theorem.

### Rank-three quadric and cubic

Rank three gives an iterated cone over a conic. Tangent hyperplanes provide moving doubled rulings and the same strict alpha contradiction for n≥5.

In the cubic case H^n=M^n=3. If E≠0, ampleness of H+M gives E·(H+M)^(n−1)>0, while nefness makes each mixed summand nonnegative. The telescoping identity H^n−M^n=Σ E·H^(n−1−i)M^i would then be positive, a contradiction. Therefore E=0. The graph's base ideal becomes trivial, the complete linear system descends as a morphism, and L is Cartier. Since −K_X∼(n−1)L, X is now Gorenstein canonical; Fujita’s classification applies. Terminality is not required for this step. I found no hidden assumption that the cubic image was already normal before establishing Cartierness.

## Final comparison, nonclosed points and ODP corollary

The proof of Theorem 1.1 explicitly imports the final comparison arguments from Liu–Xu and Liu, after replacing their “limits are cubics” result by Theorem 4.1. The manuscript’s final deformation-obstruction assertion is consistent with the hypersurface conormal sequence and cubic vanishing: Ext^2(Ω_X,O_X)=0. I did not reconstruct the entire stack-valued family comparison, including relative polarization uniqueness and quotient conventions. Therefore this review does not certify the scheme/stack upgrade as a standalone self-contained proof.

For the original compactification goal, closed polystable representatives and the smoothing component are the relevant scope. The claim about every nonclosed GIT semistable cubic needs the referenced moduli-continuity argument and openness in a GIT degeneration; it must not be inferred merely from a bijection of coarse spaces. The manuscript does cite that argument rather than silently proving it from a coarse bijection.

The proof of Corollary 1.2 literally verifies ODP GIT stability only for **fivefolds**, then concludes the smooth-n-fold metric assertion. The all-dimensional ODP corollary therefore needs the known general GIT stability statement or its calculation explicitly supplied. This is a proof-scope omission in the corollary text, not a counterexample to the n≥5 comparison. I did not independently rederive every dimension’s ODP Hilbert–Mumford criterion in this audit.

## Sources, versions and hashes

All hashes below are SHA256. Third-party PDFs and extracted text remain cached reference material and are not publication payloads.

| Source | Primary location/version | Cached PDF hash | Text hash |
| --- | --- | --- | --- |
| KSZZ, *K-moduli of cubic hypersurfaces* | Public author-linked PDF, manuscript date September 30, 2026, 15 pages; https://drive.google.com/file/d/1eB16wLGE2G5QrbV-pUDmw_ieLMiLlOcO/view | `6813e3d3be36c087e60b696f40652f8a837da7fcd9e3bdbd7af7df030c3ad65e` | `f764c51c77006a26b8da0aad6a350041019406917477cd10cdf9adfef3902927` |
| Liu, *K-stability of cubic fourfolds* | arXiv:2007.14320v2; Theorem 3.1 and Proposition 3.2 read in the cached primary PDF/text and https://arxiv.org/html/2007.14320v2 | `30a1beb80bc5b32973d041fc8af4cae7deea9a33f0d0e08306bc65a4b4670dc4` | `13b4d335869e154e41f97782bb4ba407bffa95d98220c75ea6b95323e1466b53` |
| Shibata, *Multiplicity and invariants in birational geometry*, 2014 symposium abstract | DOI10.14989/215009, pp126–126; https://repository.kulib.kyoto-u.ac.jp/items/5172604e-9565-4a33-87e5-2c358c977242 ; visible record’s bitstream f5459464-5cd0-4cc1-bb80-da093fac43ab; actual public content at /server/api/core/bitstreams/f5459464-5cd0-4cc1-bb80-da093fac43ab/content | `a402123a36f25dcfa7ec2a54bc8af2dc56a351a9094bd462b332e70fd4dbe685` | `cb0e0923f60fc982386dd33e4019555847b19062a29d9b412d32a87e3b08362d` |
| Shibata, *Bounds of the multiplicity of abelian quotient complete intersection singularities* | arXiv:1908.01218v1, introduction read only as a source trail for the lci refinements; it does not establish the exact scope of 2017 Proposition 3.13 | `12d23477a30464599c4a6ea0974d1b7ec93c388ff0f8734140d3d4d8f139d855` | `bf3fa8c2de266925e8b2e6933202fa44d24cf6c760137c6a653df7b3922ae709` |

The Shibata 2014 PDF was also rendered and visually inspected to confirm the ceiling notation, the Gorenstein-canonical scope, and the two parity formulas; text extraction alone made the ceiling symbol unclear. DGP24 and the analytic reference inspection are recorded separately in `kszz_dgp_scope.md`. The exact 2017 journal DOI is https://doi.org/10.1016/j.jalgebra.2016.11.027; its full Proposition 3.13 was not obtained here.

No external individual was contacted. No git action, publication, tracker edit, or modification of `main.tex` or `paper.pdf` was performed.

# PR207 / 5100044: independent general-theorem and proof-method priority audit

Completed 2026-10-16 UTC. This is a bounded primary-source audit, not an absolute-priority certificate. No publication, merge, status mutation, Git command, or external human contact occurred. I preserved `FIRST_INDEPENDENT_ASSESSMENT.json` before receiving other new priority findings. I did not read another new priority report. Parent messages later corroborated an exact-result lead and supplied one additional DOI to check; those messages did not supply the derivations below.

## Decision for this remit

**Do not present either Jacobi proof route as a novel method.** The submitted cyclic pole reduction is an explicit specialization of Khare–Lakshminarayan–Sukhatme's cyclic master identity. The alternate local derivative telescope is an explicit specialization of their local master identity. The uniform `dn` grid reduction is exactly a classical generalized Landen transformation. The last cyclic product step is also a corollary of Chavez-Caliz's published even-period Poncelet area-product theorem after an exact tangent-polygon calculation.

The older sources checked here do not by themselves state the general focal-inversion area theorem. One still has to derive the focal-specific edge expression and its coefficients, or an equivalent relation between the focal-inverse area and the tangent-polygon area. An old general method is not evidence that this particular geometric application was explicitly published earlier.

A separate exact-result lead is, however, real and direct: Alper Ferudun's primary author page [Focal Inversion Area Products in Elliptic Billiards](https://eulersolve.org/papers/amr-050-0044/), DOI **10.5281/zenodo.23093706**, states the same primitive divisible-by-four theorem and repeated-list counterexamples. I read that page. The parent assigned its full manuscript and timeline comparison to a separate independent lane. This report does not replace that lane or certify independence, simultaneous discovery, firstness, or novelty.

## 1. Cyclic master identity: exact overlap with submitted proof

Primary full text: Khare, Lakshminarayan, Sukhatme, *Cyclic Identities Involving Jacobi Elliptic Functions. II*, [arXiv:math-ph/0207019v2](https://arxiv.org/abs/math-ph/0207019v2), revised 24 March 2003, related journal DOI [10.1063/1.1560856](https://doi.org/10.1063/1.1560856). Read complete Sections 1 and 2.1, especially printed/PDF pp.4–7. Equation numbers below refer to this arXiv version.

Their finite Fourier filter is Eq.(10). Their type-I master identity, Eq.(20), expresses a cyclic sum of any meromorphic function with real period `2K`, imaginary antiperiod `2iK'`, and poles on the real grid through `iK'`, as a linear combination of derivatives of `sigma_1=sum dn`. The coefficients are the sums `gamma_l` of the order-`l` principal-part coefficients over the grid poles.

Apply it with `p=m=N/2`, grid step `ell=2K/m`, and `f(z)=B(z+K)`. Since `gcd(tau,m)=1`, summation by `delta=tau ell` is a permutation of the uniform grid. The submitted pole enumeration puts the poles of `f` at `iK'` and `iK'±delta`, and their imaginary translates. They have at most order two. Its reflection `f(2iK'-z)=-f(z)` makes the two double principal-part coefficients opposite; therefore `gamma_2=0`. Equation (20) leaves only `i gamma_1 sigma_1`. Consequently

`R(u)=i gamma_1 S(u-K)=i gamma_1 S(u+K)`.

The final equality uses the real `2K` period of each `dn`. This is precisely the submitted `R=C_R S(u+K)`. For `V=0`, the relevant poles coalesce but are simple, so the same conclusion follows after combining the simple principal parts. The focal calculation and verification that no additional poles occur remain case-specific inputs; the cyclic reduction mechanism is prior art.

The 2002 precursor, *Cyclic Identities Involving Jacobi Elliptic Functions*, [math-ph/0201004v2](https://arxiv.org/abs/math-ph/0201004v2), already states cyclic `dn` correlation identities; it acknowledges Poncelet-polygon antecedents. Its general high-rank evidence was partly numerical, whereas the later master-identity paper supplies the rigorous general argument. Cite the later proof when using a universal identity.

## 2. Local master identity: exact overlap with the new telescope

Primary full text: the same three authors, *Local Identities Involving Jacobi Elliptic Functions*, [math-ph/0306028v1](https://arxiv.org/abs/math-ph/0306028v1), 10 June 2003; Pramana 62 (2004), 1201–1230, related DOI [10.1007/BF02704435](https://doi.org/10.1007/BF02704435). Read complete Section 4.1, PDF/printed pp.11–13, including Eq.(42) and its proof. This theorem explicitly permits an arbitrary elliptic function with the type-I characters and arbitrary pole positions, not merely polynomial expressions.

Its Eq.(42) reconstructs such a function as a sum of shifted `dn` and its derivatives matching every principal part. Let `G(u)=B(u)/(2C)`, `r=K+iK'`, `F=1/dn`, and `rho=Res_r F=-i/k'`. A double derivative basis is sufficient because the poles of `G` are at most simple at `r` and at most double at `r±delta`.

Write the coefficient pairs at `r+delta` as `(b_-2,b_-1)`. Reflection about `r` gives `(-b_-2,b_-1)` at `r-delta`; write the simple coefficient at `r` as `b_0`. Matching these principal parts gives exactly

`G=(b_0/rho)F(u)+(b_-1/rho)[F(u+delta)+F(u-delta)]`
`  +(b_-2/rho)[F'(u+delta)-F'(u-delta)]`.

At `r+delta`, `F'(u-delta)` has double coefficient `-rho`; its preceding minus sign makes the displayed double coefficient `b_-2`. At `r-delta`, the coefficient is `-b_-2`. The difference between the two sides is holomorphic on the torus and has the imaginary antiperiod, hence vanishes. Thus the exact **structure** of coefficients `a0,a1,a2` in the new derivation follows from the old local master identity. Computing their explicit rational formulas from the focal geometry is a particular specialization, not a new general decomposition method.

This generic discussion excludes the collision `delta=K`; the separately checked direct rational identity covers that case without dividing by `V`. Do not transfer the generic three-distinct-pole discussion to that collision without this qualification.

## 3. Generalized Landen and the cyclic product

Primary full text: Khare–Sukhatme, [*Generalized Landen Transformation Formulas for Jacobi Elliptic Functions*, math-ph/0312074v1](https://arxiv.org/abs/math-ph/0312074v1), 31 December 2003. Read printed/PDF p.4 Eqs.(13)–(15),(18), and p.13 Eq.(71), which explicitly repeats the even-`p` case. The paper itself credits much older Landen theory; this audit does not attempt to determine its earliest historical formulation.

Put their elliptic parameter `M=k^2` (their symbol is `m`, which must not be confused with the vertex count), their integer `p=N/2`, and their scale `alpha_L=1/S(0)`. Their Eq.(13), with `x=w/alpha_L`, is exactly

`S(w)=alpha_L^(-1) dn(w/alpha_L, M_tilde)`.

In the alternate proof's notation, `alpha_L^(-1)=lambda` and `M_tilde=kappa^2`; the nome relation is `q_tilde=q^p`. Comparing Fourier coefficients verifies this normalization. The real primitive period of the sum is `2K/p`; the positive first surviving Fourier coefficient rules out a smaller period, so `K_tilde=K/(p alpha_L)`. Shifting by `ell/2` moves the new argument by `K_tilde`, and the standard quarter-shift identity gives

`S(w)S(w+ell/2)=alpha_L^(-2) sqrt(1-M_tilde)`.

The resulting constant matches the proposed `lambda^2 sqrt(1-kappa^2)`. Neither this multiplication formula nor the Fourier grid-filter mechanism should be described as a newly discovered Jacobi identity.

Another direct prior-art implication uses the cyclic correlation identities of math-ph/0207019 Eqs.(3),(6). On a `2p`-point grid let `d_j=dn(w+jK/p)`, let `E` be the sum over even indices and `O` the sum over odd indices. Then

`2 E O = sum_(r odd mod 2p) sum_(j mod 2p) d_j d_(j+r)`.

Each correlation is phase-independent by the prior identity. If `gcd(r,2p)>1`, split the sum into its gcd-many cycles, each a coprime smaller-grid correlation. Thus `E O` is constant, giving exactly the same half-grid product. This elementary combinatorial consequence is not an independent novelty claim.

## 4. Chavez-Caliz: a precise geometric implication

Primary publisher full text: Chavez-Caliz, [*More About Areas and Centers of Poncelet Polygons*](https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf), Arnold Mathematical Journal 7 (2021), 91–106; published online 14 August 2020; DOI [10.1007/s40598-020-00154-8](https://doi.org/10.1007/s40598-020-00154-8). Read Section 5, Theorem 6, complete printed p.104 (PDF p.14). It proves the area product of an even Poncelet polygon and its polygon formed by tangents to the outer ellipse, for concentric ellipses. **Its second polygon is not defined by focal inversion.**

There is nevertheless an exact useful bridge. For `P(u)=(-a sn u,b cn u)`, the intersection of the tangents to the outer ellipse at `P(u-v)` and `P(u+v)` is

`Q(u)=(-a dn(v) sn(u)/cn(v), b cn(u)/cn(v))`.

To verify, substitute into each tangent equation `-x sn(u±v)/a+y cn(u±v)/b=1`. Jacobi addition reduces both residuals to zero using `cn²u+sn²u dn²v=1-k² sn²u sn²v`. The determinant of the two tangent normals is `2 sn(v)cn(v)dn(u)/(1-k²sn²u sn²v)>0` on the real domain, so the finite intersection is unique.

Let `Q_w` have these tangent-intersection vertices in their induced cyclic order. Then `Q_w=D P_(w+v)` for the fixed positive-determinant linear map `D=diag(dn(v)/cn(v),1/cn(v))`. Consequently

`A(Q_w)=[dn(v)/cn²(v)] A(w+v)`.

Chavez-Caliz therefore proves constancy of `S(w)S(w+v)` for any even primitive family. Since `v/ell=tau/2`, this is the half-grid identity. For `N=4n`, also `K/ell=m/2` is integral, so the verified focal-area reduction gives

`A_focal_inv(w)=[C_R cn²(v)/(2 C_A dn(v))] A(Q_w)`.

Equivalently its proportionality factor is `C Lambda cn²(v)/(C_A dn(v) k')` in the explicit telescope notation. Thus the target follows from Theorem 6 **after proving this focal-specific proportionality**, which is where the focal edge calculation and cyclic reduction enter. The theorem is not an automatic substitution of the inverse polygon for the tangent polygon.

All tangent-line substitutions, the nonzero normal-determinant formula, determinant/area scaling, and proportionality normalization are checked exactly by `exact_priority_implications.py`; the report also contains a universal combinatorial proof of the correlation partition. This certificate is ancillary and does not replace the independent mathematical review of the target focal identity.

## 5. Other requested primary sources

- Akopyan–Schwartz–Tabachnikov, *Billiards in ellipses revisited*, [arXiv:2001.02934v2](https://arxiv.org/abs/2001.02934v2), 25 January 2020; [publisher manuscript](https://par.nsf.gov/servlets/purl/10408491), DOI10.1007/s40879-020-00426-9, online9September2020. I checked both versions and the complete relevant sections. Published Theorem1.3 (arXiv Theorem3) is an **odd**-period ratio involving the tangent polygon. Theorem1.2 is an angle product, not an area-inversion theorem. The complex pole/Liouville strategy and Poncelet-grid reductions are established antecedents. No direct focal-inverse area product was located in these theorem statements or their proofs.
- Stachel, *On the motion of billiards in ellipses*, DOI10.1007/s40879-021-00524-2: Theorem4.3/Eq.(4.9), printed1614/PDF13, supplies exactly the canonical coordinates and coprime winding/closure data imported by PR207. Theorem4.3 through Theorem4.6 and the full text's area/inversion inventory reveal no focal-inverse area theorem. The adjacent printed1613 `dn(u+2jK)=(-1)^j dn(u)` line is a typo; the used correct identity is `dn(u+2K)=dn(u)`. Credit the canonical parametrization without reproducing that typo.
- Garcia–Reznik, *Exploring self-intersected N-periodics in the elliptic billiard*, DOI10.33039/ami.2022.02.001: Table1 printed/PDF7 distinguishes `k106=A A'` (tangent polygon, Chavez-Caliz proof) from `k805,a=A A_1^dagger` (focal inverse, proof marked `?`). Proposition4.9, printed/PDF10, already states the simple four-periodic value4; the hyperbolic self-intersected four-periodic zero-area case is separate. No general `4n` proof is supplied there.
- The published *Fifty New Invariants* Table9 printed350/PDF10 has `k804` as a cosine sum, while its Table2 `k106` is the old tangent-polygon area product. It must not be cited as though its published `k804` were the arXiv-v11 `k804,a` focal area-product row.
- Bialy–Tabachnikov, *Dan Reznik's identities and more*, [arXiv:2001.08469v2](https://arxiv.org/abs/2001.08469v2),5May2020, DOI10.1007/s40879-020-00428-7: complete theorem inventory and relevant proofs checked. The nonstandard generating function gives perimeter/angle/support identities and certain focal-distance products. It does not state the present polygonal inverse-area product. Its telescope/action and grid methods are relevant prior techniques, not this exact theorem.

## 6. Additional 2026 inversive-distance lead: access and scope resolved

Gheorghe–Garcia, [*Inversive distance and Poncelet pairs*](https://link.springer.com/article/10.1007/s12215-026-01409-7), DOI **10.1007/s12215-026-01409-7**, published13May2026, is openly accessible as full publisher HTML and a **20-page PDF**. Successful ordinary downloads and checksums are recorded in the sanitized `SOURCE_PROVENANCE.json`; raw redirect-query receipts remain private. The publisher redirect appends a cookies-not-supported query, but both returned the actual article/PDF, not a login or error body; the PDF parses into20 pages.

I checked the complete theorem inventory and relevant full pages, including the final appendix. Theorems1–3 concern eccentricity and Apollonian-circle inversive distance/angles; Theorems4–5 and Corollary1 characterize/contruct **3-Poncelet circle–ellipse pairs**. Appendix Theorem6 is the triangle Cayley criterion. There is no `area` occurrence in the full extracted PDF text. No `N=4n` focal-inverted straight-polygon area-product theorem is stated. This is a scope exclusion based on full text, not an abstract-only inference. I did not audit every assertion in that unrelated article for correctness. No access-related priority gap remains for this specific lead.

## What the publication must say

Credit the cyclic and local master identities, generalized Landen transformations, Chavez-Caliz's tangent-area theorem, Stachel's canonical coordinates, and Garcia–Reznik's N4 special case. Present the focal-area reduction as an explicit worked application/verification unless a separate, justified novelty comparison establishes more. A new derivation or executable algebra certificate does not establish historical independence or novelty. Do not claim the target was still open in2026, the proof method is new, or the work is a contemporaneous separate discovery from publication timestamps alone.

The exact-result Ferudun comparison/timeline and any final publication decision remain with the parent. This bounded audit supplies strong affirmative evidence of method overlap; it does not certify exhaustive absence of other focal-area results.

## Custody and verification

`SOURCE_PROVENANCE.json` records public URLs, byte counts, UTC acquisition times and SHA256 hashes. The older raw `SOURCE_DOWNLOADS_03.json` contains opaque publisher redirect queries and is excluded from the public allowlist; do not archive or redistribute it. PDFs, HTML, full extracted text and rendered source pages are retained only in `private_sources/` for audit; do not redistribute these whole sources in the publication package. Seven complete relevant pages were rendered and visually inspected for the key master identities, Landen formulas, Chavez-Caliz Theorem6, and published AST Theorem1.3. New2026 full-text scope is supported by its actual downloaded PDF and theorem inventory; no PDF authoring occurred.

The original proof inputs were read at these exact SHA256 hashes:
- `submitted_snapshot/PROOF.md`: d92e9a82674b1562e0b980c78088fc48319f9fc3d9d46ec55a1a46c893e372b8.
- `direct_algebra_counterexample_01/DIRECT_TELESCOPING_PROOF.md`: 43919a9d6d2f8b8daa51dca6bea7fb302df6121d815acc725bb3b349a900d4ed.

`EXACT_PRIORITY_CONTROLS.json` reports seven groups passing under SymPy1.14.0, ordinary Python3.11, without `-O`. The exact algebra is fully displayed in the accompanying source. Estimated completion of this assigned bounded remit:100%; overall PR207/publication goal not assessed or advanced.

Revision2 (same audit findings): corrected the description of Stachel theorem numbering and replaced raw download-receipt publication references with sanitized public provenance. REPORT.md and FINAL_SEAL.json are superseded audit-custody history and excluded from the current public allowlist.

# Exact k115 history and competing-theorem audit

Audited 2026-10-16 UTC. This report concerns source history and contribution overlap, not a fresh verdict on the submitted proof's correctness. Editorial and publication judgment remains with the root auditor.

## Finding

An exact public competing theorem was located and its full primary paper inspected: Alper Ferudun, *Focal Distance Products of Outer Elliptic Billiard Polygons*, Theorem 1, pp.1-2, proof pp.2-4, [EulerSolve PDF](https://eulersolve.org/papers/amr-050-0007/paper.pdf?v=6a382882e9c1), [Zenodo](https://zenodo.org/records/23093258), DOI [10.5281/zenodo.23093258](https://doi.org/10.5281/zenodo.23093258). It covers the submitted theorem's exact least-period scope. It is expressly an AI-assisted, unrefereed preprint. Its existence does not establish absolute historical priority or independence from this project, and does not decide whether an honestly credited contemporaneous separate treatment has value.

The dated question marks in the 2020/2021 source cannot support a present-day assertion that this scoped theorem lacks a public proof. Correctness alone does not establish a new contribution. No alternate contribution is invented here.

## Literal location and exact translation

Theorem 1 begins on printed p.1: “Suppose a billiard on E tangent to Ec has least period n = 4r.” The continuation on p.2 gives a positive formula and says: “In particular it is independent of phase.” These are the only prose quotations from this paper here.

| Ferudun symbol/condition | Submitted PROOF.md | Implication |
|---|---|---|
| E: X²/a²+Y²/b²=1; a>b>0 | Same E,a,b | Same noncircular boundary. |
| Ec: axes A>B>0; a²-A²=b²-B²=λ>0 | Caustic axes α>β>0; α²-β²=a²-b² | A=α,B=β; same strict nesting and nondegeneracy. |
| c²=a²-b²=A²-B²; k=c/A; m=k²; k′=B/A | c,k=c/α,κ=k²,k′ | Same modulus; Ferudun's m is not candidate half-count m=N/2. |
| Least n=4r | Least N=4n | Ferudun n=candidate N; Ferudun r=candidate n. |
| h=2δ=4τK/n; gcd(τ,n)=1; 0<τ<n/2 | δ_candidate=2v=4τK/N; gcd(τ,N)=1 | h=δ_candidate; δ_Ferudun=v_candidate; every compatible coprime star winding. |
| R(v+jh), tangents at P(v±δ) | Q(u+jδ_candidate), adjacent boundary tangents | Same outer polygon, after fixed phase offset/cyclic relabeling. |
| Fε=(εc,0), ε=±1 | f+,f− | Both original foci; displayed value independent of ε. |
| Arbitrary real phase, fixed caustic/winding | Arbitrary initial phase, fixed ellipse pair | Same phase-constancy quantifier; reversal permutes factors. |
| Repetitions give powers; circle separate; no hyperbolic/degenerate caustic | Same boundaries | No extra submitted theorem coverage. |

A direct equation witness follows. Put t=sn²(v_candidate), q=1-t, W=1-k²t², C=α²W/q², and

    Q0 = product_(j=0)^(N-1)
           [1-k² sn²(j δ_candidate) sn²(δ_candidate)].

Ferudun equation (1), p.2, then reads

    product_(j=0)^(N-1) |Q_j-f±|
      = C^(N/2) (k′)^(N/2) Q0^(1/4) > 0.

Thus it contains the submitted constancy and equal-foci conclusion and displays a phase-free value. Q0 is a scalar, distinct from the outer vertices Q_j.

## Mechanism overlap checked against the paper

Ferudun equation (3), p.2, is exactly the candidate's tangent-intersection parametrization under this map. His equation (5), p.3, factors the ordinary one-focus squared distance:

    |Q(u)-fε|² = C(1+εk sn u)
                     [dn(δ_candidate)+εk cn(δ_candidate) sn u].

Multiplication over ε=±1 gives

    H(u)=C² dn²u [dn²(δ_candidate)
                    -k² cn²(δ_candidate) sn²u],

the candidate's paired factorization; C² equals candidate C_v. This is an equation-level match. The candidate pairs antipodal vertices first. Ferudun keeps two one-focus factors, fixes one product by quarter-period pairing, and fixes an addition-denominator cyclic product by its divisor (Lemma 2, p.4). Both use the same real closure/parity, compact Jacobi torus and full zero/pole cancellation, including h=K/the four-periodic collision.

Full paper text and rendered pp.1-4 were inspected. The denominator has divisor [p+h]+[p-h]-2[p]. Its cyclic norm cancels multiplicities even when the grid has repeats modulo the squared-function lattice, and positivity returns ordinary lengths. This is a checkable analytic proof of the mapped theorem, rather than only an assertion with numerical examples. The present audit does not certify accompanying software or every ancillary counterexample.

## Public-time and byte witnesses

Anonymous GETs at 2026-10-16 04:37-04:38 UTC returned:

- [Zenodo API](https://zenodo.org/api/records/23093258): created 2026-10-02T01:41:04.506303+00:00; modified 2026-10-02T01:41:04.864560+00:00; revision 3; open access; version 1.0; publication_date 2026-10-02. The [versions endpoint](https://zenodo.org/api/records/23093258/versions) returned one version record.
- [DataCite registry](https://api.datacite.org/dois/10.5281/zenodo.23093258): created=registered=2026-10-02T01:41:05.000Z; state findable; Issued 2026-10-02; version 1.0. This independently witnesses actual DOI registration, beyond a self-dated manuscript or reserved DOI.
- Site PDF and [Zenodo main.pdf](https://zenodo.org/api/records/23093258/files/main.pdf/content) were byte-identical: 77,299 bytes; SHA256 6a382882e9c1959813ac440b77cafe7f8be2c72f191fcba9039b5274b6764150; MD5 fd20f6894c0803b6a4d2452baede4cab, equal to Zenodo's file checksum.

This establishes an exact publicly deposited competing proof with an October 2 deposit/registry witness. It does not reconstruct first disclosure worldwide, independently certify all earlier visibility history, determine which researcher first developed a proof, or establish independent discovery. This family did not inspect local Git or the PR's creation history. Root separately owns that chronology and informed this auditor that its PR creation record predates the competing deposit; the report makes no contrary priority claim.

## Original source history

All eleven arXiv:2004.12497 PDFs were freshly extracted from retained primary copies. The current [arXiv history](https://arxiv.org/abs/2004.12497) confirms v11 (29 October 2020) is the latest edition. k115 retains the same outer-vertex/f1 product, N≡0 mod4 condition, and question marks for value/proof through v1-v11. v1 is 26 April 2020, Table 1 p.3; v2-v7 also p.3; v8-v10 p.4; v11 Table 2 p.5. v1, v11 and journal rows were also rendered and visually checked. The historical table date in the row is April 2020. This is dated status evidence.

The distinct journal paper, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal 7 (2021), 341-355, [DOI 10.1007/s40598-021-00174-y](https://doi.org/10.1007/s40598-021-00174-y), Table 2 p.345, has the same k115 row. It records online publication 18 February 2021. Nearby k111-k113 labels differ from arXiv; labels were not assumed globally stable. The prime means the boundary-tangent polygon, not focal pedals. The source row lists one focus; for an even primitive orbit, equality for the two foci follows from antipodal symmetry, so that equality alone is not a new invariant.

## Later author work and book trail: bounded coverage

- Garcia-Reznik, [arXiv:2011.06640v3](https://arxiv.org/abs/2011.06640v3) (19 January 2021), and distinct journal *Exploring self-intersected N-periodics in the elliptic billiard*, Annales Mathematicae et Informaticae 55 (2022), 49-75, [DOI 10.33039/ami.2022.02.001](https://doi.org/10.33039/ami.2022.02.001): inspected selected-invariant scope and N=4/N=8 sections. No general k115 theorem was located. N=4 hyperbolic-caustic statements cannot replace the target's elliptical-caustic scope.
- Complete retained 2021 Garcia-Reznik book *Discovering Poncelet Invariants in the Plane*, ISBN 978-65-89124-43-6: whole extracted text searched for the code and focal/distance-product variants; contents and relevant Chapters 2/8 read. Proposition 2.4, p.19, concerns reciprocal distances at original triangles; Theorem 2.4, p.23, credits Stachel's canonical parametrization; p.151 concerns a focus-inversive area product. No exact target theorem was located in that reading copy. The [current IMPA preview](https://coloquio33.impa.br/pdf/33CBM06-eBook-preview.pdf) has a different title, *Poncelet Surprises in the Euclidean Plane*, but the same ISBN and July 2021 copyright. It is a 15-page preview, not evidence of a later full edition. It was not conflated with the full historical copy.
- Garcia-Koiller-Reznik, *Estimating Elliptic Billiard Invariants with Spatial Integrals*, [DOI 10.1007/s10883-022-09608-y](https://doi.org/10.1007/s10883-022-09608-y) (2022 online; volume listing 2023): main-result/scope and Table 1 concern averages of perimeter, cosines, curvature and exterior-cosine product. No outer focal-distance-product theorem was located.
- Roitman-Garcia-Reznik, *New Invariants of Poncelet-Jacobi Bicentric Polygons*, arXiv:2103.11260v3 and [DOI 10.1007/s40598-021-00188-6](https://doi.org/10.1007/s40598-021-00188-6): principal statements and focal-polar/inversion correspondence concern cosine sums and limiting-pedal/focus-inversive perimeters. No exact target theorem was located; a polar correspondence does not automatically preserve Euclidean focal-distance products.
- Stachel, *On the motion of billiards in ellipses*, [DOI 10.1007/s40879-021-00524-2](https://doi.org/10.1007/s40879-021-00524-2), pp.1620-1621: Lemma 5.3 supplies quarter-period dn pairing; Theorems 5.4/5.6 concern impact-to-caustic-contact lengths k116/k117, not outer tangent vertices' focal distances. Akopyan-Schwartz-Tabachnikov [arXiv:2001.02934v2](https://arxiv.org/abs/2001.02934v2) supplies earlier complex-analytic cancellation and angle/area theorems. Method antecedents were not silently promoted into a previously printed general k115 theorem.
- Current primary author pages checked: Garcia's expressly incomplete [2022-current list](https://ronaldo.ime.ufg.br/p/2315-artigos-cientificos), [preprint list](https://ronaldo.ime.ufg.br/p/6519-pre-publicacoes), [older book bibliography](https://ronaldo.ime.ufg.br/p/2316-anos-2004-2021); Reznik's [media page](https://dan-reznik.github.io/Elliptical-Billiards-Triangular-Orbits/videos.html) and first public-repository-list page. No later author k115 proof was located in this bounded coverage. An incomplete bibliography, crawl date, negative keyword search or dated question mark never proves global absence.

## Limits and custody

No paywall prevented inspection of the decisive theorem: public PDF copies and registry metadata were available. The IMPA site currently exposes a short preview; the full historical book was inspected from the existing private copy, whose original primary download URL was not re-established in this audit. This is a precise provenance/access limit for that historical copy, not an unresolved access gap for the competing theorem. All possible later author papers and repositories were not exhaustively enumerated.

The freeze preceded proof/source reads. A permitted source-identity ledger was subsequently opened in full, exposing that family's assessments beyond literal identity. This is disclosed as an early-independence limitation; every substantive assertion here was checked against primary text/metadata. Imported reports, independent_review, other priority-family reports and root priority conclusions were not read. Root later supplied the same EulerSolve lead after this agent had found and alerted it; it did not supply this theorem translation.

New files stay within the assigned folder. Raw PDFs, extracts, images, HTML/JSON and receipts are private readings excluded from the safe manifest. No local Git operation, ref/PR change, release, public write, outreach or outreach draft occurred. Completion estimate: 100% for this bounded audit, not for global novelty discovery. Root owns editorial disposition, project chronology and any separately justified contribution framing.

## Bounded competing source-history follow-up

At root request, the public GitHub profile linked by Ferudun's paper (https://github.com/AlperTheKing) and https://api.github.com/users/AlperTheKing/repos?per_page=100&sort=updated were checked. The anonymous API returned17 repositories and no pagination Link. None was an obvious EulerSolve or exact-paper repository. Exact code/title+GitHub searches found no relevant public source repository. This is a bounded title/link inspection, not content-search of every unrelated repository.

The small Zenodo source archive (59,274bytes, MD5 30a3aaaa6358f483e76eb372faae059e, matching its API checksum) was obtained. Only its file listing, primary README_submission.md, main.tex, references.bib and reproducibility/README.txt were checked for repository/history links. The sole relevant GitHub link was the author profile. No exact-paper repository or public commit history was identified. Embedded favorable audits/reports were not opened. Archive-local timestamps are not independent publication witnesses. Earlier website or other-account repository disclosure remains unexcluded; October2 is the observed registry/deposit witness, not a certified first-publication date.

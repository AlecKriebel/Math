# PR261: verified primitive theorem and credited prior-proof correction

2026-10-12T10:34:00Z. Best estimates: mathematical evaluation 100%; bounded priority adjudication 100%; correction/publication workflow 40%. These percentages measure this review, not absolute literature coverage. Publication and author corrections have not yet occurred. Original submitted QUEUE status was `claimed_solved`, so this case passed the human's eligibility filter. The corrected assessment is `already_solved`.

## Accepted mathematical statement

Let a>b>0, with outer ellipse x²/a²+y²/b²=1 and fixed, strictly nested, nondegenerate confocal elliptical caustic x²/(a²−λ)+y²/(b²−λ)=1, where 0<λ<b². Consider the family of genuine periodic billiard trajectories of **least period N divisible by four**, including coprime star trajectories. For either fixed original focus F±=(±sqrt(a²−b²),0), form the ordered pedal polygon by perpendicular projection onto the original side supporting lines and the ordered antipedal polygon by consecutive intersections of (P_i−F)·(X−P_i)=0. Their signed shoelace area product is independent of phase and equal for the two foci.

The claim includes zero and negative antipedal areas. Reversing orientation negates both areas; a similarity of scale s multiplies their product by s⁴. It does not assert the same for circles, hyperbolic or degenerate caustics, unsigned self-intersecting polygon areas, moving poles, or arbitrary closed walks with repeated vertices.

## Root's mathematical conclusion

Root read the entire authenticated submitted proof, exact and numerical author scripts, old review, primary source pages, all six independent family reports, and the final archive addendum. The submitted all-period analytic mechanism passes on the stated domain. The explanatory source attribution must be corrected, but no change to its central mathematical argument is needed. The complete argument, rather than agreement of finite computations, supplies the universal quantifiers.

The normalized parametrization has caustic axes 1,k′, outer axes a=dn(v)/cn(v), b=k′/cn(v), original foci ±k, v=2Kτ/N in (0,K), and billiard step δ=2v. Write N=2m with m even. Primitivity makes τ odd and gcd(τ,m)=1. Stachel's canonical construction gives the bridge to a fixed physical confocal pair and its primitive winding; it is not an assumption inferred from numerical agreement.

Each real focus lies strictly inside the caustic because (a²−λ)−(a²−b²)=b²−λ>0. No tangent side passes through it. Consecutive focal antipedal normal lines have nonzero determinant on every real phase. The direct rational vertex formula has only simple poles at the two simple zeros of 1−k²sn(v)²sn(x)²; common poles of sn and cn are removable. This verifies the completeness of the complex pole list, including N=4.

On the area torus with periods h=2K/m and 4iK′, the antipedal area is even and has imaginary anti-period 2iK′. Its possible double poles are at iK′ and 3iK′. These symmetries force an odd local Laurent germ there, removing the double terms, including when several vertex contributions coincide at N=4. The trace T(w)=Σ_j dn(w+jδ) has exactly those two simple poles, with residues −2i and +2i. Residue matching and holomorphy on the compact torus show A_antipedal=b_F T(w): the holomorphic difference is constant and anti-periodicity forces that constant to zero. This step does not divide by an area or assume b_F≠0.

For the original focal pedal foot q(x)=((k−sn(x))/(1−k sn(x)), k′cn(x)/(1−k sn(x))), its sole double-pole locations are K+iK′ and K+3iK′ modulo the full torus. The foot has an even local germ there. In the two incident shoelace terms the neighboring-foot difference is odd and regular, reducing the area pole to at most simple. No adjacent foot shares that singularity because 0<δ<2K. The same residue and anti-period argument gives A_pedal=p_F T(w+K+v).

Since (K+v)/h=(m+τ)/2 is a half-integer, this shift equals h/2 modulo h. Evenness and anti-periodicity force T to vanish at h/2+iK′ and h/2+3iK′; these are its two simple zeros. The poles of T(w)T(w+h/2) therefore cancel. The product is holomorphic on the compact torus and constant. Real dn positivity is consistent with zero or negative antipedal coefficients, and no exclusion of zero-area phases is required. Central relabeling identifies the products at the two original foci.

Independent geometry, independent divisor reasoning, physical reflection/tangency reproduction, and a new whole-proof adversary all agree with this conclusion. The geometry and divisor families also verify genuine admissible N=8 sign changes, so a zero antipedal product must remain in scope. Author and old review diagnostic stdout receipts were reproduced byte for byte. Direct physical-orbit controls used separately constructed Cartesian reflections and caustic closure. These are corroboration, not substitutes for the proof; high-precision floating point results are not interval certificates. The severe physical orbit initially failed at insufficient precision and passed at 110 digits; both runs are retained in the source/reproduction family.

Root additionally executed a separate exact 98-assertion geometric certificate for the domain boundary below, using disclosed vertices but no reused review helper code. It checks ellipse incidence, fixed caustic tangency, reflection, the actual pedal feet and antipedal intersections, and area scaling under repeated traversal. Its script and receipt are `ROOT_EXACT_DOMAIN_CERTIFICATE.py` and `.json`.

## Required source qualification and falsified extension

Reznik–Garcia–Koiller's v11 and final journal Table5 identify k403,b as the original focal pedal times antipedal signed area invariant for N≡0 mod4. Neither abbreviated row nor the imported target record literally says “least” or “primitive.” The surrounding periodic-orbit convention and Stachel's coprime winding description support the primitive interpretation. It must be labeled as that interpretation, not quoted as explicit wording in the table. The original packet's assertions that the two tables and imported record explicitly agree on least period, or that no source qualification is needed, are superseded.

The broader interpretation with arbitrary listed closed-walk length is false. On the outer ellipse a=3/2,b=1 with λ=9/25, two primitive six-periodic phases have focal area products 6912/625 and 27783/2500. Traversing each twice produces listed twelve-step walks with products 27648/625 and 27783/625, difference −27/125. Root's exact certificate verifies both constructions and the fourfold product scaling. The fresh whole-proof family independently gives another such example with a=3,b=1,λ=9/16 and listed-twelve product difference 54. Neither is a counterexample to the accepted primitive theorem.

The antipedal construction uses supporting lines. A literal restriction to one-direction rays is not the conventional polygon construction. The signed-area and actual original-focus conventions are essential and are made explicit in the corrected current packet.

## Priority evidence and its limits

The classical audit independently checked Chávez-Caliz, *More About Areas and Centers of Poncelet Polygons*, Arnold Mathematical Journal 7 (2021), 91–106, Theorem6, DOI10.1007/s40598-020-00154-8. Its even original/outer signed-area product theorem applies to strict confocal general-position pairs, including stars. Four distinct transverse complex intersections verify general position. This theorem alone is not the focal pedal/antipedal theorem: both focal area bridges still need proof. An independent exact nonconfocal concentric control has the same original/outer product but different focal products, falsifying the unsupported broader shortcut. The bounded classical search found no earlier complete same-target proof in its inspected pre-2026 sources; this is not an exhaustive novelty certificate.

Alper Ferudun's *Focal Pedal-Antipedal Area Products in Elliptic Billiards*, version1.0, DOI [10.5281/zenodo.23079799](https://doi.org/10.5281/zenodo.23079799), provides a complete proof of the same primitive, strictly elliptical, signed-area theorem, including stars and zero products. The current six-page proof and source were independently validated before comparison with ours. Root also read the complete source and checked the identities, telescoping relations, denominators, quarter-period permutation and the hypotheses of the classical theorem. No mathematical gap remains for that domain.

For reproducible comparison, set α=a², β=b², D=αβ, J=(α−λ)(β−λ), L=D−(α+β)λ and W=βcos²θ+αsin²θ. Ferudun proves A_pedal=K_F A_outer and A_antipedal=R_F A_original, with

K_F=√J(β−λ)/β²,

R_F=[D(3β−α)+λ(α−β)²]/[2D(β−λ)].

These are non-divisive area identities; R_F may vanish. The odd quarter-orbit permutation has W′=(λW+L)/(W−λ), W′−λ=J/(W−λ), and L+λW′=JW/(W−λ). In particular A_outer=D√λ S₁/√J, not D√λ S₁√J. Combining the two proven bridges with Chávez-Caliz's product theorem proves the target. The N=4 specialization gives 16a⁴b⁴/(a²+b²)²; at a=2,b=1 this is 256/25. This bridge-based proof differs in mechanism from the submitted compact-torus proof. No claim of causal independence, copying or plagiarism is made.

The official Zenodo native record is published, public and file-bearing, with record created 2026-10-01T10:00:33.366348Z and updated 10:00:56.046398Z. Official file metadata marks all three files completed and gives their checksums, sizes, IDs and October1 creation/update times. The independently validated current-site PDF, source ZIP and verification report match all three official MD5 checksums and exact sizes:

| File | Bytes | Official MD5 matching current validated bytes |
| --- | ---: | --- |
| main.pdf | 84383 | c7a628028184e8486bb8b766b2dc808d |
| arxiv_source.zip | 75954 | ad07cefd26da2344d1e5c6adb2726be2 |
| verification_report.md | 3344 | 420cae154ce86dec9e6065e250a9669a |

The current PDF SHA256 is 34ff068237a7ebbd6ffa063f89717aae946bc4d27df6db23d4468b5bb52d3582. This is a hash of the retrieved current-site PDF; it is not a claimed direct SHA256 of an archived PDF download. The direct archive-content request timed out and a bounded versioned request returned HTTP406; these limitations are preserved. The official MD5/size/file-time binding establishes the association with the earlier public archive at ordinary repository-checksum standards. A new independent archival adversary verified that binding and preserved its earlier frozen report unchanged.

Official DataCite metadata registers this exact titled DOI at 2026-10-01T10:01:22Z, with an abstract describing the same theorem and both bridges. That registration precedes the first recorded author checkpoint (11:31:06Z), the first introduction of the full proof at commit8f29c19 (11:46:29Z), the b85 review checkpoint (12:11:52Z), and the PR creation service event (12:12:30Z). The first full proof, subsequent checkpoint and submitted current proof bodies are identical. Authored commit clocks are not server push/first-discovery clocks. Repository creation times are not an exact first-HTTP-visibility measurement. The audit establishes a prior archived same-target proof relative to this recorded campaign, not absolute global first priority or discovery chronology.

Primary evidence is retained in `root_priority_readonly/DATACITE_RECORD.json`, `ZENODO_NATIVE_RECORD.json`, `zenodo_archive_actual/` official file responses and Root receipts, and `competing_preprint_priority_adversary/archival_addendum_20261012/`. URLs, file pins and locators for the bounded classical review are in `classical_priority_adversary/SOURCE_PINS.json` and its claim/search matrices. Third-party PDFs and source ZIPs are local research inputs, not proposed new repository publications.

## Disposition

Accept the scoped primitive theorem as valid and retain its alternative proof and checks as credited research findings. Correct the current problem assessment to `already_solved` because the earlier archived same-target complete proof defeats a new open-problem-resolution claim. The alternative proof's novelty is unestablished. Do not produce a new preprint, Zenodo deposit, DOI or spreadsheet row for this case.

As with the completed PR262 priority correction, prepare a corrected OPEN/DRAFT author packet and publish only scoped findings to MAIN, without a native PR merge or closure. Preserve the original frozen packet byte for byte as dated historical provenance, including its old manifests and review receipts. Current status, source wording, proof introduction, QUEUE assessment and PR description must all agree with this adjudication. A fresh adversarial review of the complete correction package and the exact publication plan remains required before those actions.

AI tools were used extensively for the original work and these adversarial checks. This is an unrefereed research audit; it is not human peer review or formal proof-assistant certification. No outside individual was contacted. The overall descending persistent goal continues after this case; held PR293/292/280 retain their documented gaps and remain uncompleted.

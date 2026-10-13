# Classical labelled-saddle-connection priority audit

Date: 2026-10-12 UTC. Scope: PR152 / problem5000006, repaired proof of Fuchs 2021 Conjecture 2.7; pre-2021 classical regular-polygon, Veech/Ward, scaling-vector, cone-angle, hyperelliptic-frame and cutting-sequence literature. This is a bounded priority audit, not a publication decision or an exhaustive historical certificate.

## Decision

**No pre-2021 full cover of the exact all-n physical Fuchs label-to-sine theorem was verified in this family. Historical novelty remains undetermined.** The strongest verified classical overlap is much larger than a group calculation: the regular double-polygon models, one/two cusp reduction, common directional affine scaling, unlabelled sine lengths, same-cone return-angle labels, and comparison of distinct-cone labels through the hyperelliptic involution are all old. The candidate must not present its angular invariant, Veech reduction, or sine spectrum as new.

The precise residual question is whether an older source already identifies the physical type in Fuchs Definition 2.1, with its segment-parity convention, with the intrinsic cone label and the representative-sensitive sine weight, uniformly for odd and even n. The repaired candidate explicitly supplies this dictionary and its folding-chart signs. That is the narrow possible contribution left by the inspected historical sources; this audit does not certify it as historically new.

The parent reported a contemporary October 9, 2026 exact-cover preprint after this family's independent mechanism was established. That work and its chronology are outside this historical family and were not independently verified here. No inference of copying or exclusive priority follows from this report. An alternate-proof framing with full classical and contemporary credit is consistent with this historical audit.

## Exact target and the criterion for a cover

A short trajectory goes from a polygon vertex to the first subsequent vertex, reflecting in side interiors; its length need not be small. The target concerns source-parallel directions, including the source's dihedral identification, and the actual oriented physical labels A_k. It asserts

\[
L_k/L_\ell=\frac{\sin((k+1)\pi/n)}{\sin((\ell+1)\pi/n)},\qquad n\ge3,
\]

where k and ell are represented in 0,...,n-3. A historical full cover may use an equivalent intrinsic labelling, but must demonstrably identify that labelling with these physical types, not merely list the possible lengths.

The repaired candidate's dictionary is K=2m+1 modulo n-2 for odd n and K=2m+1-e for even n, where e distinguishes equal and distinct endpoints. The physical folding chart gives k=K or k=-K. The weight w_n(k)=sin((k+1)pi/n) is invariant under this sign change. Relevant target-specific details include the parity-selected sum or difference of endpoint angles, the two vertex classes in even double polygons, the involution transporting a distinct endpoint, and the physical orientation of the starting chart.

An unlabelled spectrum cannot logically determine this dictionary by itself. For example, n=7 has unequal weights sin(pi/7) and sin(2pi/7). Permuting the assignments of A_0 and A_1 preserves an unlabelled list while changing the target statement. This is a demonstration of logical insufficiency, not a billiard counterexample. An old theorem supplying an intrinsic label could eliminate this gap only after a checked equivalence with Fuchs's physical convention.

## Verified classical imports

| Primary source and exact locator | Verified overlap | What it does not supply at that locator |
|---|---|---|
| Veech 1989, printed p.561, Proposition 2.10; pp.566–568, §5, Theorem 5.8; pp.572–573, §7 | Lattice saddle directions have parabolic stabilizers; the regular-polygon group and one/two cusp structure used by the reduction are classical. | Fuchs's physical endpoint type dictionary. |
| Veech 1989, pp.564–565, §4 | The double-polygon surface, vertex-zero orders, genus, polygon-exchanging derivative -I involution and hyperelliptic quotient. Its k=1 model is the candidate's double regular polygon. | Veech's differential/model parameter k is not Fuchs's label k. |
| Veech 1989, pp.566–568, §5, formulas (5.1)–(5.4) and proof of (5.8) | Trigonometric cylinder data and explicit boundary saddle lengths. | An all-n assignment of physical A_k to those lengths. |
| Hubert–Schmidt 2001, printed pp.477–479, §3, Definition 2 and Lemmas 6–7 | Saddle-vector equivariance under linear deformation, normalized length ratios, and equality of scaling vectors along a parabolic conjugacy class. | Vectors in the definition are ordered by length. The resulting scaling vector does not retain a prescribed physical endpoint label. |
| Fuchs 2021, printed p.495, Proposition 1.2; p.512, Conjecture 2.7 | Fuchs treats the sine-ratio spectrum as known and proposes the finer labelled assertion as a sharpening. | His introductory belief that Veech/Ward methods prove his conjectures is not a citation of an already proved labelled theorem. |
| Finster 2011, §§3.1–3.2, Remark 3.5, p.20 | Group and cusp statements with express attribution to Veech; the even double cover has the same group as the opposite-side quotient. | Edge/cylinder/fundamental-group labels are not identified with Fuchs's endpoint types. |

The Veech originals are now directly available and were inspected. The earlier source audit's statement that the 1989 full paper was not retrieved is a historical description of that earlier audit, not a present access gap. No change was made to that original file.

Veech's 1992 **The billiard in a regular polygon** (singular title), GAFA 2, 341–379, DOI [10.1007/BF01896876](https://doi.org/10.1007/BF01896876), was also recovered in full. Its defined length spectrum is a spectrum of parallel classes of closed geodesics (printed p.343). Lemma 2.5, p.347, lifts saddle connections through the unbranched cover; pp.348–350 reduce periodic foliations and preserve directional length inequalities. Its relative-homology basis and modular representation at pp.351–355 use edge labels and N=n/e(n). Those are not the cone residue modulo n-2 and cannot silently be used as Fuchs types. No equivalent physical label-to-weight theorem was identified in those inspected sections.

## Cone and hyperelliptic labels were already standard

[Eskin–Masur–Zorich](https://arxiv.org/abs/math/0202134), published IHÉS 97 (2003), 61–179, record the angle at which a saddle connection returns to its zero as an odd multiple of pi, and include that angle in its configuration. See §3, preprint p.11 in the locally retrieved version, and §11 for the later configuration construction. This supplies the all-genus same-cone angular label underlying the candidate's m. Their generic-surface counting theorems do not provide the regular-polygon physical Fuchs sine dictionary.

[Hubert–Lelièvre](https://arxiv.org/abs/math/0401056), published Israel J. Math. 151 (2006), 281–321, make the label particularly explicit in H(2). The retrieved author preprint is dated October 26, 2004. In §3.2, preprint p.12, the return angles are pi, 3pi, 5pi; in §3.3.2, p.13, they label the saddle connections gamma_pi, gamma_3pi, gamma_5pi and give equal length to the first and last in the two-cylinder model. Consequently a claim that return-angle labels themselves are new is directly defeated by a full early source.

For comparison, in the double pentagon the candidate's K=2m+1 modulo 3 sends these three return angles to 1,0,2. The weights for 1 and 2 agree, while the weight for 0 differs. That comparison is an audit derivation, not a theorem stated by Hubert–Lelièvre; their setting allows variable cylinder dimensions and does not establish the physical Fuchs dictionary.

[Boissy](https://aif.centre-mersenne.org/articles/10.5802/aif.2947/), **Labeled Rauzy classes and framed translation surfaces**, AIF 65 (2015), 905–932, closes a second apparent novelty loophole. Section 3.1, printed pp.914–915, defines marked horizontal separatrices. Proposition 4.1, printed p.919 (PDF p.16), compares labels at the two equal-degree zeros of a hyperelliptic surface by transporting one through the hyperelliptic involution. The resulting odd-pi angular difference is constant under continuous deformation. Section 5, printed p.925, identifies outgoing separatrices at a degree-k zero with Z/(k+1) by cyclic order. The relevant page was visually checked.

The relationship to the candidate's distinct-endpoint convention is exact at the mechanism level. Its backward end germ v has the opposite plane direction from start u; applying iota makes their directions agree, so angle(u,iota v)=2pi m. On the other cone, angle(iota u,v)=2pi m as well. Rotating v positively through pi chooses an outgoing separatrix l_1 with the same plane direction as u. Boissy's comparison from the incoming separatrix iota u to l_1 then gives (2m+1)pi modulo 2pi r. Thus Boissy's invariant is the candidate's even-endpoint sheet comparison with a pi shift of convention. For the even double n-gon r=g=(n-2)/2. This observation credits the distinct-cone involution machinery; it still does not identify physical A_k or sine weights.

Affine invariance of an odd-multiple-pi cone separation follows from the increasing angular lift of a positive linear map, F(theta+pi)=F(theta)+pi. It is a direct elementary deduction from the standard labelled-cone data. Boissy's deformation invariance is stronger evidence that this idea should be treated as classical background, even though his application is moduli-space connected components rather than billiard lengths.

## Cutting sequences and remaining historical limits

Davis's **Cutting sequences, regular polygons, and the Veech group** (Geom. Dedicata 162 (2013), 231–261; full text retrieved from [arXiv](https://arxiv.org/abs/1708.09552)) develops affine derivation of cutting sequences for double odd regular polygons. Section 1 explicitly restricts to bi-infinite trajectories avoiding corners; Theorem 6.4 gives the sandwiched-letter rule. Davis's [2014 paper](https://nyjm.albany.edu/j/2014/20-23p.pdf), NYJM 20, 399–429, Definition 2.20, printed p.407, says vertex-hitting trajectories stop and lack bi-infinite cutting sequences; §5 gives regular-polygon sequence derivation. These are relevant affine coding results, but their inspected theorems do not supply the terminal physical angle/parity label or its all-n sine weight.

Ward 1998, **Calculation of Fuchsian groups associated to billiards in a rational triangle**, ETDS 18, 1019–1042, remains a full-text access gap. The [Cambridge PDF link](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0E89F6A15AA355F6B12B46831C86AACD/S0143385798117479a.pdf/calculation_of_fuchsian_groups_associated_to_billiards_in_a_rational_triangle.pdf) redirected to an abstract/access page. Neither that abstract nor the paper's title can establish absence of a labelled theorem. Veech's 1995 chapter **Geometric realizations of hyperelliptic curves** is another precise uninspected lead. A complete historical audit of framed separatrices, hyperelliptic saddle configurations and regular-polygon dissertations was not performed.

Boulanger–Lanneau–Massart 2024 uses odd-pi sector/return-angle labels and the cusp framework in full text supplied by the parent. It is useful modern mathematical corroboration, but postdates Fuchs and is not pre-2021 priority evidence. The search was finite and terminology can conceal an equivalent formulation. No-hit outcomes support only the bounded statement above.

## Access, independence and reproducibility

The full Veech scans were lawfully retrieved from public Göttingen GDZ article downloads reached through EuDML, after direct Springer pages offered subscription access. The archive's cover terms allow noncommercial education, research and private use and restrict redistribution/repository use. The scans, OCR and rendered pages are **local verification caches only**; do not publish or upload them with the audit. Publishable artifacts can contain bibliographic links, locators and original overlap analysis.

Veech 1989: [EuDML record](https://eudml.org/doc/143714), [GDZ article PDF](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0097/LOG_0031.pdf), 3,227,739 bytes, SHA256 5a144d7dfd323d12d38a1fb42b0bc92533b6ea6f37534bb105879e924ae4b667. Veech 1992: [EuDML record](https://eudml.org/doc/58107), [GDZ article PDF](https://gdz.sub.uni-goettingen.de/download/pdf/PPN359089402_0002/LOG_0017.pdf), 3,013,443 bytes, SHA256 4aa3a506b20dd52f2fe1328979a26819268e309c5164f815ad0318466643de64. Local copies are sources/veech1989.pdf and sources/veech1992.pdf. All article pages were rendered/OCRed, the relevant sections were read, and key theorem/model pages were visually inspected; OCR screening is not represented as exhaustive line-by-line reading.

The repaired CANDIDATE.md and original SOURCE_AUDIT.md were read before other new priority findings. Only sources and this family's evidence were used to form its mechanism. The contemporary lead was received after that point. All writes are confined to priority_classical_labels/. No Git refs/index, original files, tracker, publication state, or external communications were changed.

The accompanying RESULT.json states the bounded outcome, evidence/SOURCE_OVERLAP.md maps claims to locators, evidence/SEARCH_LOG.md records search/access limits, and RESEARCH_LOG.md records dated checkpoints and completion estimates.

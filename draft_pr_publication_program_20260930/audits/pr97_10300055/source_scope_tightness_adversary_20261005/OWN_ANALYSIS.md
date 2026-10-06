# Own analysis: source scope and imported tightness mechanism

This analysis was completed without reading the historical review or another fresh agent's conclusions. Incoming CANDIDATE.md, SOURCE_AUDIT.md, upstream_record.json, and later source_manifest.json were read. It independently verifies the completed argument; it does not spend a new central proof-search turn.

## Exact target and category

Calegari's version0.78, printed p.29, Question13.2 assumes the foliation from Question13.1 and assumes a contact connection form. The preceding question specifies minimality, tautness, C2 regularity, atoroidality, and nonzero ordinary real Godbillon–Vey evaluation on [M], with dα=α∧ω. Definition1.1, printed p.1, requires one transverse circle meeting every leaf, which directly implies the usual per-leaf transverse-circle convention. The statement does not ask for existence of a contact form. Answering conditional tightness cannot answer Question13.1's existence or weak-sign question.

The source has no explicit universal sentence saying all manifolds are closed and oriented. The candidate appropriately *interprets* the ordinary fundamental-class evaluation in that category. On a connected noncompact manifold, ordinary top-dimensional real homology vanishes; it also vanishes for a connected compact manifold with nonempty boundary. An ordinary real fundamental class requires orientation. Relative or locally finite classes would be different statements and are not supplied in this question. Contact ω also itself orients the manifold. Thus closedness is a stated candidate hypothesis and a conventional reading of the original question, not a literal quotation of an unstated global convention. Preserve this precision in any later paper.

TF=kerα with rankTF=2 makes α nowhere zero and globally coorienting. Ambient orientation and this coorientation give an oriented tangent plane field. Minimality here means every leaf is dense. A spherical leaf would be embedded and compact, hence closed in M and a proper subset by dimension; it cannot be dense. The candidate excludes it correctly. Atoroidality and the GV numerical value do not enter the ensuing deduction.

## Imported theorems: quantifiers and assumptions

Vogel2011, printed p.42 (PDFp.2), states the Eliashberg–Thurston result for a contact structure sufficiently C0-close to a taut foliation on a closed three-manifold: it is symplectically fillable and tight. The surrounding text orients the plane fields. This is a neighborhood statement about an arbitrary sufficiently close contact structure. It is distinct from the adjoining Colin existence-of-tight-approximation statement, and the proof uses the former correctly. Printed p.41 explicitly places C2 foliation approximation in the closed oriented category and excludes the product sphere foliation.

Dathe–Rukimbira2008, Proposition3.3, printed p.5, independently repeats the neighborhood tightness implication and attributes it to Confoliations p.50. Its tautness description uses a minimal-leaf metric and explicitly excludes the trivial sphere foliation. The source definition from Calegari is the geometric transverse-circle version; their equivalence is a classical tautness fact. The direct Vogel neighborhood statement already suffices. Proposition3.4 is related prior work but assumes a *closed* defining one-form and hence cannot be applied directly to a general α satisfying dα=α∧ω. No deduction is imported from the more specialized propositions elsewhere in that preprint.

Vogel2016, printed pp.2447–2448 (PDFpp.9–10), uses a closed connected oriented M, discusses C2 foliations, and defines contact fields at C1 regularity. Theorem2.9, printed p.2451 (PDFp.13), is expressly for a smooth family of smooth contact structures on a closed M. The candidate uses that smooth version on a finite interval only. Orientation reversal gives the negative-contact counterpart without changing tautness or the existence of an overtwisted disk. A disconnected compact M has finitely many components and the argument applies component by component.

The full Confoliations book was not retrieved or read. The actual theorem is imported through two explicit primary-paper formulations, not alleged direct inspection of book p.50. The symplectic filling and fillability-implies-tightness theorems remain accepted external foundations; this audit does not reprove them. The absence of the book is a disclosed foundation-access limit, not evidence against the explicitly corroborated theorem statement.

## Independent pencil and compactness checks

For C1 forms, dα=α∧ω has a C1 right-hand side even though the initially computed dα is merely continuous. Differentiating this equality distributionally is legitimate: d2α=0, d(α∧ω)=dα∧ω−α∧dω, and dα∧ω=α∧ω∧ω=0. Thus α∧dω=0 as a distribution; it is continuous and therefore zero pointwise. Also ω∧dα=0 and α∧dα=0. Direct expansion gives

(ω+sα)∧d(ω+sα)=ω∧dω

for every real constant s. Contactness precludes any zero of ω+sα. The constant-volume identity supplies the fixed sign and no parameter degeneracy on any finite interval. There is no contact assertion at the limit s=∞.

Uniform plane convergence can be checked quantitatively. Let m=min|α|>0 and W=max|ω|. For s>2W/m, set λs=α+ω/s. Then |λs|≥m/2 and normalized covectors differ by at most 4W/(sm); their orthogonal kernel projections differ by at most 8W/(sm). This proves C0 convergence on compact M and allows selection of a finite S with ker(ω+Sα) in the given neighborhood.

For finite S, both βs=ω+sα and dβs are uniformly bounded by some B. The fixed positive contact density has minimum c0>0 after componentwise orientation. If smoothing errors in η−ω and a−α, including their exterior derivatives, are at most ε, the family η+sa differs from βs by at most δ=(1+S)ε. Its contact-volume error is at most 2Bδ+δ2. Choose this smaller than c0/2, and shrink ε for the open endpoint-neighborhood condition as well. A single sufficiently close a can be fixed for all sufficiently close η. Therefore *every* smooth η in one C1 neighborhood is tight by smooth Gray on [0,S]. No integrability property of a is assumed, and the fixed C2 foliation has not been smoothed or replaced.

As an independent consistency check, the identity α∧dω=0 implies that the Reeb vector of ω is tangent to TF: evaluate on a frame consisting of the Reeb direction and two contact-plane vectors with nonzero dω pairing. Its nonzero tangent section agrees with the Euler-class remark in the source. This is not needed for the proof.

## Over-twisted-disk regularization

Dathe–Rukimbira printed p.5 uses an embedded disk with Legendrian boundary and disk tangent plane distinct from the contact plane all around that boundary. Vogel2011 Definition1.3, pp.42–43, uses the same boundary condition and explains that it reduces to contact tightness because a contact field has no integral surface. Thus the candidate has used a valid equivalent criterion, not accidentally the confoliation-only notion.

A smooth embedded boundary curve has a trivial rank-two normal bundle in an oriented three-manifold, so S1×D2 tubular coordinates are available globally around it. Although t is a circle coordinate, dt is a well-defined periodic one-form. For a fixed smooth Legendrian γ and θj→θ in C1, qj=θj(γ′) tends to zero in C1: differentiate its composition, using γ″ bounded and θj derivatives convergent. Subtracting qj(t)χ(u,v)dt sets the boundary value exactly to zero, not approximately. The correction has C1 norm O(||qj||C1). Contactness persists on compact M, and the positive angle between TD and kerθ along the compact boundary persists.

For a C2 disk, C2 approximation by smooth embeddings gives C2 convergence of the boundary curves. Projection onto a fixed nearby smooth tubular core has nonzero derivative and degree one, so the nearby curves can be written as graphs after reparametrization. Then qj=θj(γj′) again converges in C1, since γj′ and γj″ converge. The shifted cutoff has uniformly bounded first derivatives because the graph first derivatives remain bounded. On γj, dt(γj′)=1 and χ=1, so the same exact boundary cancellation holds. Smooth disk approximation preserves the tangent-plane angle. The resulting smooth overtwisted structures arbitrarily close to θ would contradict the preceding all-nearby-smooth-forms-tight claim. This verifies the closed-manifold C1 extension.

## Falsification attempts and limits

- Replace the neighborhood theorem by existence-only approximation: that would leave a real logical gap, but the two read statements explicitly have the needed stronger quantifier.
- Apply Gray at the foliation or at infinity: invalid, but not used; S is finite and every member of the smoothed family is contact.
- Smooth the foliation and assume tautness persists: unjustified, but not used; only one-forms on a finite interval are regularized.
- Give the contact volume both signs on one connected component: impossible for a continuous nowhere-zero volume density; orientation reversal handles the other constant sign.
- Replace s by a variable h: the volume acquires dh∧α∧ω. Indeed α and ω are pointwise linearly independent (otherwise α∧dω=0 contradicts contactness), so a prescribed dh can cancel the volume at a point. This confirms why the proof requires constant shifts and makes no variable-shift claim.
- Drop compactness or allow boundary: uniform bounds, global isotopy completeness and the imported neighborhood result no longer follow as used. These are excluded variants, not established extensions.
- Read the unqualified smoothing lemma literally on a noncompact M: mere uniform/compact-open C1 convergence does not by itself give a global contact margin. The intended closed use is sound. Optional precision: state the lemma for closed M, or supply an explicit strong-Whitney approximation argument if the broader lemma is desired.

No counterexample to the stated closed-manifold theorem emerged. No historical priority or global openness has been established by this review.

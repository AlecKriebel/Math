# Independent proof reconstruction and adversarial checks

This reconstruction was developed from the actual short source and primary passages. The initial assessment was preserved before preparation conclusions were read. The target is a conditional implication, not existence of its antecedents. No new central proof-search turn was used.

## Exact claims

Main claim: M is a closed oriented smooth 3-manifold; F is a cooriented taut C² foliation without spherical leaves; a global nowhere-zero C¹ form α defines F; ω is smooth and contact; dα=α∧ω. Then ker ω is tight in the usual smooth sense.

Supplement: if ω is C¹ contact, every sufficiently C¹-close smooth form defines a usual tight contact structure; ker ω itself admits no embedded C² disk whose boundary is Legendrian and whose tangent planes differ from ker ω at every boundary point. The latter is the explicitly chosen low-regularity disk criterion, not a universal equivalence among low-regularity tightness definitions.

Success criteria were a valid finite smooth contact path, an EVERY-sufficiently-near tightness input, exact retention of smooth ω in the main theorem, and a separately valid disk correction for the supplement. All are met.

## Algebra and weak derivatives

For C¹ α and C¹ ω, α∧ω is C¹. Applying weak exterior differentiation to dα=α∧ω and using d²=0 yields

    0=dα∧ω−α∧dω=−α∧dω.

The right side is continuous, so distributional zero implies pointwise zero. This does not differentiate a generic continuous form using an unjustified classical product rule: the product α∧ω is already C¹. Also α∧dα=0 and ω∧dα=0 follow immediately from the given relation. Consequently for a CONSTANT s,

    (ω+sα)∧d(ω+sα)=ω∧dω.

The two mixed terms vanish separately, including for nonclosed α. The relation uses the source's sign dα=α∧ω. Switching the sign convention would not invalidate the same pencil identity, but the note does not silently switch conventions. Variable shifts have an extra ω∧dh∧α term; the proof uses only constants.

## Uniform endpoint and finite smoothing

Fix a metric. Let m=min|α|>0 and W=max|ω|. For s>2W/m, α+ω/s has norm at least m/2 and normalized covectors tend uniformly to α/|α| (a bound 4W/(ms) suffices). Thus the kernels converge uniformly with the source coorientation. Compactness is essential to this argument. There are finitely many components; contact-volume sign is constant on each. Reverse the auxiliary manifold orientation on any negative component before applying the positive theorem. Tightness of the plane distribution does not change.

The primary ET statement gives a C⁰ neighborhood in which every relevant smooth contact structure is tight, not merely one approximating structure. Choose a finite S making the C¹ pencil endpoint's planes lie strictly in that neighborhood. For smooth α the whole [0,S] path is smooth and Gray applies directly.

For C¹ α, approximate α by smooth a in C¹, retaining smooth ω exactly. The path λ_s=ω+sa is smooth on the same fixed [0,S]. Let c₀>0 be the minimum coefficient of ω∧dω in the chosen positive volume form, and let B bound both |β_s| and |dβ_s| on M×[0,S]. For form and derivative errors at most δ, the wedge-volume error is bounded by 2Bδ+δ². For example δ=min(1,c₀/(8(B+1))) makes this strictly below c₀/2. The errors are bounded by S times the corresponding errors in a, so smooth approximation attains the required margin for fixed S. It also keeps the endpoint inside the open tightness neighborhood. No integrability of a is needed.

Apply smooth Gray only to this smooth finite path. Its tight endpoint transfers to λ₀=ω exactly. The proof never applies Gray to C¹ planes, to infinity, or to a foliation. Extending slightly beyond [0,S], if needed for a convention requiring an open parameter interval, follows from contact openness and compactness.

## Supplemental C¹-ω argument

Choose the same finite S from the C¹ pencil and fix a sufficiently close smooth a. For every smooth η sufficiently C¹-close to ω, η+sa remains contact for all s∈[0,S] and its endpoint lies in the ET neighborhood. Uniform estimates depend only on the common C¹ error bounds, so the quantifier really is EVERY sufficiently close smooth form. Smooth Gray gives usual tightness of ker η.

Suppose a C² disk D violates the explicit disk criterion for C¹ θ. Smoothly approximate its embedding in C². A fixed smooth tubular chart around a smooth curve close to its boundary makes the original and nearby smooth boundaries graphs γ(t)=(t,u(t),v(t)) and γ_j(t)=(t,u_j(t),v_j(t)) after reparametrization. Smooth θ_j→θ in C¹ and γ_j→γ in C² imply q_j(t)=θ_j(γ'_j(t))→0 in C¹, since θ(γ')=0. The chain-rule derivative involves first derivatives of θ and second derivatives of γ, precisely the declared thresholds.

Subtract q_j(t)χ(u−u_j(t),v−v_j(t))dt in the fixed chart, with uniformly supported smooth cutoff. The corrected smooth form kills γ'_j exactly because dt(γ'_j)=1 and χ=1 on the graph. Its C¹ error tends to zero: q_j and q'_j vanish while graph first derivatives are uniformly bounded. The support stays in the chart, so extension by zero is smooth. Contactness is C¹-open, and boundary plane distinctness is uniformly open on the compact boundary; both persist. Thus D_j is a smooth disk violating usual tightness for an arbitrarily C¹-close smooth contact form, contradicting the prior EVERY-near result. The smooth-disk case is the same correction with a fixed boundary. No smooth Legendrian disk for the original C¹ field is assumed.

## Original problem and boundary checks

Calegari's actual 2002 Version 0.78 p.29 explicitly inherits minimal taut C²/atoroidal/nonzero GV evaluation hypotheses from Question 13.1 and then assumes a contact ω. A global nowhere-zero defining α supplies coorientation. The note explicitly limits itself to the ordinary fundamental-class closed/oriented interpretation and the smooth contact-form interpretation, rather than quoting a source-wide convention. A compact spherical leaf cannot be dense in a 3-manifold, so minimality excludes it. Source tautness by one transverse circle meeting every leaf implies the standard tautness required by ET. Atoroidality and the GV numerical value are unused in the implication. The note does not prove an example satisfying the antecedents, weak-sign attainment, or Question 13.1.

The theorem does not extend to boundary/noncompact settings; no uniform-margin or complete-Gray conclusion in those settings was inferred. α need not be closed; neither the algebra nor smoothing assumes that. All usual-tightness statements concern smooth structures; the C¹-ω disk statement is expressly restricted.

## Imported authority and attribution

Read actual Vogel 2011 printed pp.41–43. Its p.42 ET theorem says sufficiently C⁰-close contact structures on a closed manifold are fillable and tight. The smooth contextual convention and the independent Dathe–Rukimbira p.5 proposition support the version used. Read actual Vogel 2016 printed pp.2448–2451, including Definition 2.2 and Theorem 2.9; Gray is explicitly smooth-family/smooth-contact/closed-manifold. The weaker C¹ contact-plane definition does not weaken Gray's hypotheses.

Read the full Dathe–Khoule 2012 author-transcribed body pp.100–107. Definition 2.1 allows C=1,B=t, and Theorem 2.2 on pp.102–103 assumes integrability rather than closedness. In dimension three its nonnegative criterion Q=α∧dω+ω∧dα includes Q=0. Its expansion yields t²ω∧dω here, the same pencil planes under s=1/t. The original text does not explicitly name C¹ as a threshold. Read the 2025 coauthor preprint pp.32–33, which explicitly attributes the C¹ criterion to 2012.

The 2025 normalized equality after (62) is wrong for general Q>0: the missing contribution is (C/B)Q. For example locally α=dz, β=dz+xdy gives Q=dx∧dy∧dz and normalized volume (1+1/t)dx∧dy∧dz rather than dx∧dy∧dz for C=1,B=t. This known display flaw is accurately qualified by the package and is immaterial for Q=0; the proof independently derives equality in that specialization.

Dathe–Rukimbira's Proposition 3.4 uses a closed defining form, so it establishes the narrower near-foliation/isotopy pattern, not coverage of arbitrary nonclosed α. The exact ordinary-tightness conclusion is the note's stated corollary of prior mechanisms and ET/Gray, rather than a literal earlier printed Question 13.2 answer. I found no exact such answer in the complete 2012 transcription or the read 2025 pp.32–33. This is bounded absence, not priority evidence. Unread literature and final 2003 wording remain unresolved exactly as disclosed.

## Mathematical disposition

No substantive mathematical or supporting-source defect found in either the short claim or the accurately limited supplement. The imported global theorems are used as mathematical premises; finite diagnostics do not prove them. Historical novelty, current global open status, and publication permission are outside this qualified mathematical acceptance. A separately established wrapper custody defect prevents whole-package acceptance.

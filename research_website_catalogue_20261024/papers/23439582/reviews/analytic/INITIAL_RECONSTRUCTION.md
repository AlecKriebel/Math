# Paper-only independent analytic reconstruction

This document is written after personally reading the actual complete four-page published PDF, all 157 lines / 13093 bytes of its controlling TeX, and all four fresh individual page rasters. It precedes reading any foreign scientific body, archived/current scientific review, source programme body, computation result or inventory triage. The same agent previously performed metadata/opaque-byte custody acquisition; that prior exposure is disclosed and is not claimed as a scientific reading. This is one analytic reviewer with distinct reasoning mechanisms, not eight separate independent reviewers.

## Exact claim, category and success criterion

For every prime p, every field k of characteristic p, and every compact Lie group G whose finite component group pi_0(G) is not p-nilpotent, set X=(BG)^wedge_p using Bousfield–Kan completion **before** looping and set R=C_*(Omega X;k). Work with left DG R-modules (equivalently Hk-linear modules) and their derived category. The augmentation k is the generator defining Loc_R(k), and nu:Gamma_k R -> R is its canonical cellular approximation. The assertion is that H_n(nu)=0 for **every integer n**. The theorem includes finite G and positive-dimensional G without requiring a nilpotent component action, adjoint orientability or a tensor-collapse condition.

The assertion is about the induced map, not vanishing of either source or target and not nullhomotopy of nu as a derived R-linear morphism. A derived ghost may survive even when all its homology maps vanish. The target is completed loop chains, not C_*(G;k), and no passage between those targets may be silently made. No arbitrary coefficient ring, recognition theorem for G, or converse to the component-group condition is asserted. Publication validity requires the full quantified claim; a restricted component action or a projection to component-group homology would not satisfy it.

The paper's proof reduces the assertion to two topological imports, a chain-level coefficient extension, the Hopf structure on loop homology, and a general cellular vanishing criterion. My initial analysis below reconstructs the algebraic and categorical steps; the exact scope of the cited DGI and Ishiguro interfaces remains an **unverified import at this initial seal**. This is a deliberate source-check gap, not yet a finding that either cited assertion is false.

## 1. Ordinary Hopf finite-ideal mechanism

Let B be an ordinary Hopf algebra over a field with antipode S, and suppose I is a nonzero finite-dimensional right ideal. Choose a finite basis i_1,...,i_d of I. Each Delta(i_j) has a finite tensor expansion, so all first tensor factors span a finite-dimensional subspace. Hence

J=span{(id tensor f)Delta(i): i in I, f in B^*}

is finite-dimensional. Counit evaluation gives I subset J. Coassociativity implies Delta(J) subset J tensor B: coefficient extraction on the final factor of (Delta tensor id)Delta(i) may instead be performed in (id tensor Delta)Delta(i), whose first factors already lie in J. This does not require a finite-dimensional dual Hopf algebra; B^* is used solely as a space of linear functionals on finite tensor expressions.

For fixed b in B and f in B^*, write f_c(z)=f(z S(c)). Then

sum (id tensor f_{b_(2)})Delta(i b_(1))
=sum i_(1)b_(1) f(i_(2)b_(2) S(b_(3)))
=sum i_(1)b f(i_(2)).

The second equality is the Hopf identity sum b_(1) tensor b_(2)S(b_(3))=b tensor 1. Every i b_(1) lies in I, so J is a right ideal. Since J is a nonzero right coideal, epsilon cannot vanish on all of J: otherwise applying epsilon tensor id to Delta(j) would give j=0 for every j in J. Pick j with epsilon(j)=1. Delta(j) lies in J tensor B, whence sum j_(1)S(j_(2)) belongs to J and equals 1. Thus J=B, so B is finite-dimensional. This is a contradiction for infinite-dimensional B.

For left ideals, use B^(op,cop). Its antipode is the same S: reversal of both product and coproduct interchanges the two original antipode equations. There is no use of S inverse or antipode bijectivity. This avoids an unjustified replacement by B^op alone.

Attack result at this stage: the coefficient-space proof appears internally valid, including the often fragile coideal direction, full-dual use and one-sidedness. A primary attribution check is still required; the mathematical argument is supplied in the target itself.

## 2. Graded sign and parity mechanism

Loop homology is a Hopf algebra in graded vector spaces with Koszul signs. Forgetting the grading is legitimate as an ordinary Hopf algebra only in characteristic two. In odd characteristic, retain parity and form B=H#kC_2. For homogeneous h,a and i,j in {0,1}, reconstruct:

(h# g^i)(a# g^j)=(-1)^(i|a|) ha# g^(i+j),

Delta_B(h# g^i)=sum (h_(1)#g^(|h_(2)|+i)) tensor (h_(2)#g^i),

epsilon_B(h#g^i)=epsilon_H(h),

S_B(h#g^i)=(1#g^(i+|h|))(S_H(h)#1).

For Delta multiplicativity, the sign contributed in the ordinary B tensor B product is (|h_(2)|+i)|a_(1)|+i|a_(2)|, which equals |h_(2)||a_(1)|+i|a|. This agrees with first multiplying h#a and then applying the graded coproduct. Associativity follows by comparing i|a|+(i+j)|b| with j|b|+i(|a|+|b|). Counitality uses that epsilon of an odd element is zero. The two antipode identities reduce to the graded H identities after the parity factors cancel. The exact signs need a bounded independent algebra check after this seal; such a check would support these conventions, not prove the general Hopf theorem.

If I is a graded one-sided ideal of H, multiplication on either side of I#kC_2 preserves it, because the parity action preserves I and the residual H product remains in I. It has dimension 2 dim(I); B has dimension 2 dim(H), including in the infinite case. Thus a finite-dimensional nonzero graded ideal would contradict the ordinary theorem. No connected grading, nonnegative grading, commutativity, cocommutativity, or finite-type hypothesis occurs here. H need not be an ordinary ungraded Hopf algebra in odd characteristic.

## 3. Finite cellular approximation mechanism

Proxy-smallness means there is K in thick_A(A) intersect thick_A(k) with k in Loc_A(K). The first condition makes K compact in D(A); the other conditions give Loc_A(K)=Loc_A(k), and K has finite-dimensional total k-homology. The distinction between a compact proxy and compactness of k itself is essential.

For M in Loc_A(K), compact-generator Morita theory uses E=REnd_A(K), with Hom_A(K,M) a right E-module by precomposition and K the corresponding left E module with commuting A action. The inverse is derived tensor N tensor_E K. Opposite-ring conventions must be checked against the cited theorem, but the variance is consistent with the stated construction.

Take a semi-free DG E resolution of N with a well-ordered basis and differential of each basis generator a finite sum of earlier basis terms. A finite set of generators has finite dependency closure. Indeed, an infinite finite-branching dependency tree would contain an infinite descending branch by the finite-branching tree lemma, contradicting the well-order. Arbitrarily long finite branches from one finite root would already produce such an infinite branch; transfinite indices do not invalidate this argument. Finite dependency-closed sets give finite semi-free submodules. Their unions remain dependency-closed, so the stages form a filtered system exhausting the resolution. Filtered colimits of complexes of modules are exact, and these semi-free inclusions compute the homotopy colimit.

Derived tensor with K preserves that colimit. Every finite semi-free E stage maps to a finite construction from K, hence an object P in thick_A(K). Homology commutes with the filtered homotopy colimit, so every individual x in H_n(M) has a representative y in H_n(P) mapping to x. This proves a **class-by-class** factorization; it does not assert M has finite total homology or is itself compact. Finite-dimensional total homology is stable under finite shifts/sums, cones (by the long exact homology sequence), and retracts. Thus each P, but not necessarily M, has finite total homology.

Attack result: the finite dependency argument resolves a potential hidden infinite-cell assumption. It applies even when E is not connective. Actual DGI compact-generator conventions and the cited BIS formulation still require primary inspection.

## 4. Image ideal and ghost mechanism

Let f:M -> A be A-linear and let x lift to y in P as above. The derived composite P -> M -> A induces a graded H_*(A)-linear degree-zero map on homology. Its image I is a graded **left** ideal of H_*(A), since A acts on the target by left multiplication. All degrees are considered together: dim_k(I) <= dim_k H_*(P) < infinity. A bound only on each graded piece would not suffice, and the proof does not make that weaker substitution.

If H_*(A) admits the stated infinite-dimensional graded Hopf structure, the preceding finite-ideal result forces I=0. Therefore f_*(x)=0. Since x and n were arbitrary, all homology maps vanish. A possible phantom or ghost morphism does not contradict this conclusion, and the proof never upgrades the conclusion to a null morphism. No compatibility between a Hopf coproduct and the A-module M is needed: the Hopf structure is used only on the target algebra H_*(A).

This general criterion is a stronger intermediate statement than just the canonical cellular map. It is internally supported conditional on the stated proxy and Hopf hypotheses. An arbitrary map of underlying k-complexes would not have an ideal image, so A-linearity is load-bearing.

## 5. Topological proxy mechanism and exact open import

The manuscript attributes to DGI section 5.7, printed p.382, proxy-smallness of F_p over R_0=C_*(Omega((BG)^wedge_p);F_p) for **every compact Lie group**. It sketches an embedding G -> SU(n), the finite homogeneous space SU(n)/G, a cochain proxy, and transfer through double-centralizer/Morita results.

This must be checked in the actual primary. A theorem only for connected G, p-group components, a nilpotent action on G_0, uncompleted loops, or cochains without the needed transfer would not establish the full published theorem. Likewise, smallness over cochains and proxy-smallness over the completed loop-chain Koszul dual cannot simply be identified by vocabulary. The needed check is the exact chain of cited implications, including the double-centralizer model of completed loops and whether compactness of G and finiteness of SU(n)/G are enough without action restrictions.

At this initial seal, the exact external statement remains unverified. No attempt is made to repair or weaken it. If primary inspection exposes an unsupported central transfer, the required disposition is Deferred—defect found rather than a restricted promotion.

## 6. Coefficient extension mechanism

Assume the prime-field compact proxy K_0 is established. Ordinary chains on a fixed loop-space model commute with field extension: R is equivalent as an augmented k-algebra to R_0 tensor_(F_p) k. The extension functor is exact and preserves arbitrary homotopy colimits. Since K_0 is finitely built from R_0, its extension K is finitely built from R; since K_0 is finitely built from F_p, K is finitely built from k. Applying the same functor to F_p in Loc_(R_0)(K_0) gives k in Loc_R(K). All three proxy requirements therefore survive even an infinite extension field.

Homology of chains also commutes with this flat extension. If V is an infinite-dimensional F_p vector space, choose an infinite basis; V tensor_(F_p) k is a direct sum of the same number of copies of k, hence has infinite k-dimension. There is no inappropriate comparison of dimension over different fields and no interchange of an infinite cochain dual with tensor. Fields are essential to the Kunneth and finite-dimensional arguments being used; no assertion over arbitrary rings is justified here.

## 7. Hopf topology and non-p-nilpotence mechanism

For a connected pointed X, a loop-group model has multiplication, diagonal and inversion up to coherent homotopy, giving H_*(Omega X;k) the Koszul graded Hopf structure. Over a field the homology cross-product is the graded tensor product. Omega X need not be connected: its component multiplication and inversion still give the antipode, and the proof does not need connected H_0. Completion is applied to BG first, so this mechanism concerns the actual target of the theorem.

The manuscript's second essential import is Ishiguro Proposition 1.3(a), printed p.199: if BG is p-compact, then pi_0 G is p-nilpotent. The relevant meaning of p-compactness must be finite total mod-p homology of Omega((BG)^wedge_p), with the appropriate completed connected classifying space. If the primary instead imposes an extra hypothesis or gives a different implication, contrapositive cannot be used as written. Assuming this exact interface, non-p-nilpotence forces infinite total F_p loop homology, and the field extension calculation in mechanism 6 finishes the dimension step. It would be incorrect to use merely infinite cohomological dimension of BG or infinitude of the ordinary group G as a substitute.

The topological implication is required only in the stated direction. No sufficiency of p-nilpotence for p-compactness, or converse for vanishing, is claimed. For finite G the condition agrees with the familiar normal prime-to-p subgroup / p-power index definition, but all-prime or positive-dimensional variants must not be silently interchanged.

## 8. Boundary and counterexample mechanism

The finite-dimensional Hopf boundary is concrete: A=k has k compact/proxy-small, Loc_A(k)=D(k), and Gamma_k A -> A is the identity, nonzero on H_0. Thus removing infinite total dimension from the criterion fails. The trivial compact Lie group has p-nilpotent component group and lies outside the theorem; it gives the same nonvanishing boundary. This does not suggest a counterexample under the published hypotheses.

The Hopf restriction is also real. Take the ordinary augmented algebra A=k x k[t], augmentation to the first factor, and k=Ae for e=(1,0). Then k is a compact projective A-module and is its own compact proxy. The k-cellular part of A is Ae, included by a map nonzero on H_0. The target has infinite k-dimension and a nonzero finite-dimensional left ideal k x 0. It cannot admit an infinite-dimensional Hopf structure on this multiplication, by the independently reconstructed finite-ideal theorem. Thus replacing “Hopf” by merely “infinite-dimensional augmented algebra” would be false.

In the genuine theorem n<0 has zero target because chains are connective; n=0 and positive degrees are addressed by the same full ideal argument. Finite G is not excluded by dimensional wording. An infinite field extension does not destroy infinitude. Characteristic two requires no parity bosonization; odd characteristic requires its signs. Orientability and component action must be absent from both actual topological imports, not merely absent from the final line of the proof. The distinction between vanishing on homotopy and a zero derived morphism remains throughout.

## Mechanism/evidence/status/gap table

| Mechanism | Independent paper-only evidence | Initial status | Exact remaining check |
|---|---|---|---|
| Ordinary Hopf coefficient closure | Expanded right-ideal/coideal/antipode argument above; op,cop left conversion | Internally reconstructed | Primary attribution and any convention comparison |
| Koszul signs/parity | Product, coproduct multiplicativity and ideal preservation reconstructed | Internally plausible; no empirical evidence used | Complete antipode convention check, meaningful bounded sign control |
| Cellular approximation | Finite dependency closure, filtered semi-free exhaustion and compact-proxy image | Internally reconstructed | Actual compact Morita interface and BIS text |
| Class-to-ideal vanishing | Full finite total homology gives finite graded left image ideal | Internally reconstructed conditional on proxy/Hopf | No additional central algebraic gap identified |
| Compact Lie proxy | Exact necessary imported target and transfer identified | Unverified external input | Read actual DGI 5.7 and load-bearing transfers without action hypotheses |
| Arbitrary field | Explicit extension of all proxy constructions and infinite basis | Internally reconstructed | Confirm input is prime-field chains on fixed completed space |
| p-compactness obstruction | Correct contrapositive and target definition isolated | Unverified external input | Read actual Ishiguro Proposition 1.3(a) and definitions |
| Boundary/counterexample attacks | A=k and A=k x k[t] show necessity; all n/finite G/odd p distinguished | No full-claim counterexample found at initial stage | Check exact primaries and source code only after this seal |
| Question/credit/status | Published theorem claims answer to OWR 2.2; explicitly credits classical ingredients | Unverified external comparison | Read actual question and Greenlees Lemmas 6.2/6.5/Remark 6.6; no worldwide-priority inference |

Initial conclusion: the internal proof provides a coherent conditional route to the full original theorem. Its two essential topological imports and exact prior-question interface are not independently certified at this stage. No passing scientific verdict, narrowed promotion, formal certification, external human review or research follow-up is issued. Next work is primary verification and bounded source checks; any substantive unsupported import ends the repair route and receives a precise deferred disposition.

# Classical theorem comparison for PR946 / 6000001

This is an independent priority comparison, not a new proof attempt or a novelty certificate. The authenticated candidate is the original 17635-byte proof at Git head `7d3adb0e500b0414a49a449e7981d34ade329427`, SHA256 `a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2`.

## Exact object being compared

For every smooth Hausdorff second-countable positive-definite statistical manifold without boundary, including noncompact and disconnected manifolds, the candidate gives one global proper smooth embedding into one finite-dimensional open positive Hessian domain. Both specified ordered connections are the orthogonal tangential projections of the ambient flat connection and its dual. The dimension is `binomial(2n+4,3)`. The ambient domain can depend on all of the input data and can be nonconvex and incomplete. There is no assertion of a finite probability model or of globally injective dual coordinates.

The old question in FMU1998 p125 item1(a), raised at the December16–18,1996 workshop, asks for finite-dimensional dually flat realization. Its footnote separately mentions Abe's affine realization. Amari1997 p82 defines the dual structure using torsion-free connections; p87 question1 asks induced dual-structure embedding, while question2 separately asks affine realization. The candidate's statistical scope is therefore material. A historical problem list does not establish its present status.

## Scope matrix

| Source and inspected locator | Input and conclusion actually supported by inspected body | Global/local, map and target | Exact implication/gap |
|---|---|---|---|
| Lauritzen, *Statistical manifolds*1987, pp175–184 and212–214 | Riemannian metric plus symmetric cubic; dual torsion-free connection equivalence and orthogonal induced connection definitions | Differential-geometric foundations; inspected chapter does not supply the requested universal positive Hessian embedding | This chapter is distinct from the separate1987 *Conjugate connections* note credited for pair embeddings by Marugame. Do not substitute one for the other. |
| Lauritzen, *Conjugate connections in statistical theory*1987,33–51 | Original body not obtained. Author institutional bibliography confirms the work. Marugame2021 §2.4 credits its pair notion. | Pair target `V × V*` and natural pairing are not automatically a positive Hessian ambient realization | Exact original existence hypotheses, global scope and proof remain an access gap. No negative theorem claim about the unseen note. |
| Matumoto1993, Theorem1 p328; proof pp329–331 | Every smooth statistical manifold has a smooth global contrast function on `M × M`, with prescribed metric/cubic third-order data | Global, positive intrinsic metric; contrast realization, not finite-dimensional positive Hessian submanifold realization | p328–329 explicitly treats1-flat embedding as a further question. General divergence is not a Bregman potential. Compatible3jets, globalization and scalar extension are substantial old ingredients. |
| Abe1994, *Tensor*55(3),276–280 | Body not obtained; NDL issue11196378 confirms exact title, pages and restricted access; FMU footnote and Matsuzoe1998 p410 distinguish affine formulation | Affine realization as reported by those primary sources; exact hypotheses and proof not authenticated | No justified bridge from an affine fundamental form/transversal to a positive ambient Hessian metric with both ordered orthogonal projections. The unseen body remains a material gap. |
| Kurose1994, pp427–430 | Simply connected1-conformally flat statistical manifolds; divergence and affine hypersurface framework | Affine immersion with metric as second fundamental form; special class | No all-manifold metric realization. |
| Matsuzoe1998, MainTheorem pp409–410; construction pp415–417 | Simply connected conformally-projectively flat statistical manifold admits equiaffine centroaffine codimension2 immersion; converse; uniqueness with stated dimension assumption | Global in the stated special class; pseudo-Riemannian affine fundamental form, transversal choice | No arbitrary statistical manifold conclusion; no positive ambient metric conclusion follows just from this affine theorem. |
| Uohashi–Ohara–Fujii2000, §2 pp404–406 | Level surfaces in a positive Hessian domain yield1-conformally flat statistical submanifolds under stated assumptions | Actual positive Hessian ambient geometry, but restricted level-surface category | Does not realize arbitrary `g,C` globally. |
| Lê MPI43/2003, Theorem5.2 pp32–33; pp40–41 nonbounded proof | Body claims unrestricted smooth/Ck finite-simplex embedding; abstract distinguishes bounded finite-sample from unrestricted infinite-sample realization | Global finite positive simplex claimed; free-map perturbation then noncompact sphere decomposition | Unrestricted conclusion depends on an unverified noncompact gluing step, later removed in v6. Isolated Proposition5.16 cannot be read without boundedness context: an unrestricted linear-target claim is false by the comass check below. |
| Lê MPI77/2003, MainTheorem p2; Theorem2.5 p4; noncompact argument p5 | All `C1` statistical manifolds claimed to embed in finite simplex; compact intermediate explicitly assumes compactness | `C1` isostatistical map, finite positive simplex; universal numerical bound claimed | Noncompact gluing and base-value compatibility not established in inspected argument. A merely `C1` embedding does not directly provide the candidate's smooth second-derivative orthogonal induced-connection construction. |
| Lê arXiv v1–v5, Section5 | Broad global claims, compact intermediate results and explicit noncompact globalization; v5 adds unrestricted embedding Theorem5.6 | Finite positive simplex; smooth or `C1` versions; immersion/embedding assertions vary by version | Detailed version audit records exact changes. Unrestricted proof is not authenticated simply by a broad theorem sentence; compactness correction is relevant evidence. |
| Lê final Journal of Geometry2006, DOI10.1007/s00022-005-0030-0 | Publisher abstract claims every smooth/C1 manifold embeds in finite simplex; received2004-09-10, revised2005-01-02, issueMarch2006 | Potentially decisive unrestricted positive predecessor IF its actual proof establishes it | Final body inaccessible. ResearchGate's displayed “full text” is MPI77/2003, not an authenticated final journal body. Do not silently replace it with either MPI77 or arXiv v6. |
| Lê World Scientific2007 chapter, DOI10.1142/9789812770493_0012 | Primary MPI metadata identifies volume chapter; arXiv history cites it | Potentially decisive unrestricted predecessor IF final body establishes the claim | Final chapter bytes not obtained; publisher security challenge. MPI and arXiv metadata differ on final page253/254. ArXiv v2/3 are not certified byte-identical substitutes. |
| Lê arXiv v6, MainTheorem p14; Theorem5.1 p15; Theorem5.6 pp22–23 | Compact smooth/C1 statistical manifolds admit finite positive-simplex embedding (strongest embedding statement is Theorem5.6) | Global on compact input; positive fixed model; no properness issue for compact source | Established relevant compact predecessor. It does not quantify over arbitrary noncompact input. Residual unqualified consequence after MainTheorem is not a replacement noncompact proof. |
| Marugame2021, pp1–2 and §§2.3–2.4 pp4–6, used only for genealogy | Credits Lê for unrestricted local positiveHessian realization; proves local equivalence with Lauritzen pairs | Explicitly local; positiveHessian extension; ordered induced-connection definition | No whole-manifold globalization in the theorem. Later attribution is not a primary reading of the original Lauritzen note or final Lê2006 body. |

## Checkable implication: a genuine whole-manifold finite-simplex embedding would settle the old question

Let `p_0=1−sum_(i=1)^d p_i` on the positive simplex, with all `p_a>0`. In mixture coordinates put

`Psi(p)=sum_(a=0)^d p_a log p_a`.

Then `G_ij=delta_ij/p_i+1/p_0` is positive definite, with

`v^T G v=sum_(i=1)^d v_i^2/p_i+(sum_i v_i)^2/p_0>0` for `v != 0`.

This is the Fisher metric. The standard mixture connection is flat, and its metric dual is the flat exponential connection. The cubic `D G` is minus the conventional Amari–Chentsov tensor: on repeated vectors it is `−sum_a (dp_a(v))^3/p_a^2`. Thus a theorem preserving `g` and arbitrary prescribed cubic `T=−C` induces the candidate's ordered pair with the mixture connection first. Equivalently one can exchange the dual ordering and use exponential coordinates. Restriction of metric and cubic determines both torsion-free induced connections, since `g(nabla_XY,Z)=g(L_XY,Z)−C(X,Y,Z)/2`.

Accordingly, the stronger probability-model category cannot be dismissed as irrelevant. If its unrestricted smooth global embedding theorem is valid, the original finite-dimensional realization question was answered earlier, regardless of whether the original paper named FMU item1(a). An explicit improved dimension bound could be a separate contribution, but would not restore novelty of the old existence answer. This audit does not start that separate research problem.

## Properness is not a reliable priority shield in the flexible target category

Suppose an earlier theorem supplies a smooth embedding into an open Hessian domain `V`, with image `S`. A smooth embedded submanifold is locally closed. Every point of `S` therefore has an ambient neighborhood disjoint from `closure_V(S) \ S`. Points outside `closure_V(S)` also have such neighborhoods. Consequently `B=closure_V(S) \ S` is closed in `V`. Set `U=V \ B`. Then `U` is open, `S` is closed in `U`, and the embedding into `U` is proper: intersection of `S` with any compact subset of `U` is compact. Restriction preserves the Hessian structure. This uses the allowed nonconvex/incomplete custom domain.

Thus an established earlier global embedding, even without advertised properness, would already address this feature after ambient restriction. A mere immersion is different: self-intersections and image topology still need attention.

## Checkable exclusion: an unrestricted fixed linear-target theorem cannot hold

For a unit vector `w` in `(R^N,g0,A sum_a dz_a^3)`,

`|A sum_a w_a^3| <= |A| sum_a |w_a|^3 <= |A| (sum_a w_a^2)^(3/2)=|A|`.

Any isostatistical immersion into that target inherits this finite cubic comass bound. On `(R,dx^2,T=x dx^3)` the value on the unit vector `d/dx` is `x`, unbounded in absolute value. This is a smooth positive statistical manifold and hence refutes an isolated all-manifold reading of MPI43 Proposition5.16. Its proof explicitly divides by `|T|_C3` and says this is where boundedness is needed. The control does NOT refute finite-simplex realization (whose cubic norm grows near its boundary), and does NOT obstruct a custom Hessian target.

The candidate's own original declared approaches1–2 already recorded this distinction. The calculation here is a priority-scope control, not a fresh proof route.

## Local pair geometry does not by itself globalize

A Lauritzen pair satisfies `g_ij=f_i^A phi_A,j` and `Gamma_ijk=f_ij^A phi_A,k`. These identities imply that `phi_A df^A` is closed; they do not imply zero periods. The positive-Hessian extension in the inspected local theorem first obtains a local primitive. A global primitive, globally suitable embedding, smooth extension and everywhere positive ambient Hessian remain to be supplied for arbitrary noncompact input. The natural pairing on `V × V*` has split signature; calling the pair a positive statistical ambient embedding would skip the relevant step. The candidate constructs the stronger identity `phi df=0` and handles those global steps explicitly. Whether that exact construction is new remains a bounded-search question, not something established by this observation.

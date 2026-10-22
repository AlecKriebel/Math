# Independent initial derivation, before reading included audit verdicts

Timestamp: 2026-10-17T16:41:20.959710+00:00
Review completion estimate: 25%. Discovery verification estimate: provisionally 90%, pending source-hypothesis verification and falsification.

Exact claim: for every compact Lie G with non-p-nilpotent pi_0(G), every characteristic-p field k, and A=C_*(Omega((BG)^hat_p);k), the canonical k-cellularization map induces the zero map on every H_n. The claim does not assert that the morphism is null in D(A).

My reconstruction:
1. If K is a compact proxy for k, Loc_A(k)=Loc_A(K). Derived Morita with E=REnd_A(K) represents any M in this subcategory by N tensor_E^L K.
2. A semi-free E-resolution has generators with finite differential supports and strictly earlier dependencies. The dependency closure of each finite generator set is finite by the finitely branching well-founded tree argument. Its finite dependency-closed submodules form a filtered union. A free generator over E can have arbitrary coefficient complexes, but it is still a single E-cell; these finite submodules are perfect E-modules.
3. Their images P under tensor with K belong to thick_A(K), hence thick_A(k), and have finite *total* k-homology. Filtered homotopy colimits commute with homology over a field, so every individual class of M is represented by a class in such P.
4. For any A-linear P -> A, its homology image is a finite-dimensional graded left ideal of H(A), including all its degrees; it is not merely one finite-dimensional homogeneous piece.
5. For an ordinary Hopf B with finite nonzero right ideal I, its right coefficient coalgebra closure J=(1 tensor B*)Delta(I) is finite dimensional, contains I, and is a right coideal. The displayed identity for multiplication by b follows by Delta(ib_1), contraction by z -> f(zS(b_2)), and b_2 S(b_3)=epsilon(b_2). Thus J is a right ideal. If epsilon(J)=0, applying epsilon on the first tensor factor to Delta(J) contradicts J != 0. For j with epsilon(j)=1, sum j_1 S(j_2)=1 belongs to J. This forces J=B. The opposite-and-coopposite construction proves the left version without invertibility of S.
6. For a graded Hopf algebra in odd characteristic, parity bosonization has product (h#g^i)(a#g^j)=(-1)^(i|a|)ha#g^(i+j) and Delta(h#g^i)=sum(h_1#g^(|h_2|+i)) tensor(h_2#g^i). This has the ordinary multiplication-coproduct compatibility sign |h_2||a_1|+i|a|. S_B=(1#g^(i+|h|))(S_H(h)#1) is the standard induced antipode; it must be checked on both sides. A graded one-sided ideal yields I#kC2 of the same side, so the finite-ideal contradiction transfers. Characteristic 2 permits direct ungrading.
7. These statements imply all maps from Loc_A(k) to A vanish on homology if H(A) is infinite dimensional as a Hopf algebra. The canonical approximation is one such map.
8. The two source-sensitive topological inputs still requiring direct source inspection are proxy-smallness of Fp over chains on the loop of completed BG for *every* compact Lie G (no orientability/action assumption), and non-p-nilpotence of pi0(G) forcing infinite total loop homology. Field extension then preserves both the proxy and infinite dimension; no cochain-dual base change is used.

Boundary/falsification checks identified before prior audit reading:
- G finite must remain covered; original question may restrict positive dimension but theorem is allowed to be stronger.
- G connected or p-nilpotent component group is outside the theorem; the general criterion must not accidentally make a finite-dimensional H(A) vanish.
- A=k supplies an immediate counterexample when infinite dimensionality is omitted.
- Nonconnected loop groups still have diagonal/inversion Hopf structure; connectedness is unnecessary.
- Arbitrary extensions k/Fp preserve chains and all finite/colimit constructions; they do not require k to be finite or perfect.
- Classes in negative degrees of cellular sources are allowed; the target chains are connective but the proof treats every n uniformly.
- Verify the source question concerns full homotopy map, rather than nullity as a morphism or a component-group projection.
- Verify final archive actually contains the source version that typesets the included PDF and claims matching its verifier.

Initial conclusion: no algebraic gap found in this reconstruction. Source-hypothesis verification remains critical; no included audit verdict has been read at this point.

## Completed source and sign checks

The freshly downloaded publisher DGI section 5.7 (p. 382) explicitly establishes both cochain and completed-loop-chain proxy-smallness at k=Fp for arbitrary compact Lie groups, using section 4.17 after EM/double-centralizer completeness. Ishiguro pp. 195 and 199 supplies exactly the completed-loop definition and necessary component-group condition. The OWR p. 593 notation and p. 594 question match this target.

For completeness, my independent symbolic check of both bosonized antipodes is as follows. In m(S_B tensor id)Delta_B(h#g^i), the accumulated sign is (-1)^((|h|+i)|h|), and the group factor is g^|h|, independent of the summand. The remaining H-sum is sum S_H(h_1)h_2=epsilon(h)1. For even h the extra factors are 1; for odd h epsilon(h)=0. In m(id tensor S_B)Delta_B(h#g^i), the two factors (-1)^((i+|h_2|)|h_2|) cancel and the group factor is 1; the remaining H-sum is sum h_1 S_H(h_2)=epsilon(h)1. No S inverse is used. Associativity/coassociativity follow from the parity action and coaction, and coproduct multiplicativity has the sign already recorded above.

Final independent objection status: none identified in the analytic proof, source hypotheses, field extension, completion convention, or scope. Only after the initial derivation was saved were the included Hopf/topology/priority verdicts read.

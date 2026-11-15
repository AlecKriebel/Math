# Independent closure of the mathematical interfaces

The paper-first reconstruction remains unchanged. These additional derivations and source checks complete its outstanding interfaces; no deposited proof was edited or repaired.

## Both ordinary antipode identities in the parity bosonization

Work modulo2 in exponents. For homogeneous h of parity d and a summand h1 tensor h2 of its coproduct, put a=|h1|, b=|h2|, so a+b=d. In B=H#kC2,

Delta_B(h#g^i)=sum (h1#g^(b+i)) tensor(h2#g^i),
S_B(z#g^j)=(1#g^(j+|z|))(S_H(z)#1).

For the left convolution, S_B(h1#g^(b+i))=(1#g^(i+d))(S_H(h1)#1), with the initial group exponent independent of the summand. Multiplying by h2#g^i gives

(-1)^((i+d)d) S_H(h1)h2 #g^d.

Summation uses the graded-Hopf convolution identity sum S_H(h1)h2=epsilon(h)1. If epsilon(h) is nonzero, h has degree0 and d=0. Thus the result is epsilon(h)1_B in all cases. No inverse of the antipode appears.

For the right convolution, associativity gives

(h1#g^(b+i))(1#g^(i+b))(S_H(h2)#1)
= (h1#1)(S_H(h2)#1).

The group exponents cancel before the last multiplication. Summation gives epsilon(h)1_B. This verifies the other antipode identity without a sign ambiguity.

Coassociativity also follows termwise. For a triple coproduct h1 tensor h2 tensor h3, both iterated bosonized coproducts have group exponents (|h2|+|h3|+i, |h3|+i, i). For counits, a factor with nonzero counit is even, so deleting it leaves exactly the original group exponent. Multiplicativity is the sign identity already in the initial reconstruction: (|h2|+i)|a1|+i|a2|=|h2||a1|+i|a|. Associativity of the smash product follows from the parity automorphism action. Together these prove the ordinary Hopf structure for arbitrary graded H, rather than infer it from finite tests. Characteristic2 permits direct forgetting of the Koszul grading.

If I is a graded left ideal, (a#g^i)(h#g^j) is a scalar sign times ah#g^(i+j), in I#kC2. If it is a graded right ideal, (h#g^i)(a#g^j) is a sign times ha#g^(i+j). Thus either ideal side embeds with twice its vector-space dimension. The ordinary finite-ideal argument in the initial reconstruction then proves the full graded lemma.

## Finite-stage approximation and all maps

DGI Definition4.6 and Remark4.8 use exactly the three proxy conditions stated by the target. Theorem4.9 applies to a small/compact R-module, not only to a compact augmentation field. Applying it to the compact proxy K yields Loc_A(K) equivalent to right modules over REnd_A(K); this avoids incorrectly treating k as compact. The actual source uses the same right-module Hom/precomposition and tensor convention.

Every semifree module over the resulting DG algebra has a well-ordered cell basis with finite-support differentials. Finite generator dependency closure is finite by well-founded descent and the finite-branching-tree argument. These closures are filtered under finite union followed by closure and exhaust the resolution. Therefore each object is a filtered homotopy colimit of finite semifree, hence perfect, objects. After derived tensor with K these stages lie in thick_A(K). Filtered colimits commute with homology in DG modules over a field, so each individual homology class of M is represented at one stage. That stage has finite total k-homology since K is finitely built from k.

BIS published Lemma4.1/proof on printed709 explicitly uses filtered perfect approximation in D(E). Its stated lemma has an additional coproduct-preservation hypothesis and a conclusion about compact objects; I do not misquote it as the target's class-by-class lemma for arbitrary M. In the present compact-generator Morita setting the filtered approximation step is available directly, and the semifree argument supplies an independent proof. No telescope conjecture or extra compactness of M is imported.

For x in H_n(M), choose P->M and y in H_n(P). For every A-linear f:M->A, the complete image of H_*(P)->H_*(A) is a graded left ideal because H_*(P) is a left H_*(A)-module and the map is linear. It is finite-total-dimensional. Hence it vanishes if H_*(A) is infinite-dimensional Hopf. In particular f_*(x)=0. This proves the exact stronger criterion for every cellular M, every A-linear f and every integer n; the canonical map is only one instance. The image of the single vector y alone need not be an ideal and is not used as one.

## Completed chains and arbitrary fields

Fresh published DGI section5.7, printed382/physical26, explicitly sets X to the Bousfield–Kan p-completion of BG, G any compact Lie group (including finite), k=Fp, and E=C_*(Omega X;k). It explicitly proves both cochain and chain augmentation modules proxy-small. The displayed proof uses SU(n)/G, Fp-goodness of BG, finite p-group pi1X, the Eilenberg–Moore identification and Proposition4.17. It includes no orientability or nilpotent component-action condition. This closes the exact topological scope gap left open at my initial seal.

For any characteristic-p field k, tensor the chain algebra and its proxy from Fp to k. A finite construction from R0 extends to a finite construction from R, a finite construction from Fp to one from k, and a localizing construction to a localizing construction because extension of scalars preserves all homotopy colimits. Hence the proxy remains compact and builds k. This includes infinite field extensions. An Fp-basis of H_*(R0) becomes a k-basis of its tensor extension, so infinite total dimension stays infinite. No dual of an infinite cochain complex is interchanged with tensor extension.

Ishiguro's actual published definition on printed195 and Proposition1.3(a) on printed199/physical5 use precisely Omega((BG)^_p). They assert that p-compactness implies p-nilpotence of pi0G. Their finite mod-p cohomology condition is equivalent over a field to finite total mod-p homology. DGI also gives the relevant completed-space/goodness setting. The contrapositive therefore yields infinite total H_*(Omega X;Fp) from the target's non-p-nilpotence hypothesis. The source does NOT assert the converse for all compact Lie G; printed199 explicitly warns that its necessary condition is insufficient. The target uses only the valid contrapositive.

The loop-space Hopf structure is supplied by group multiplication/diagonal/inversion on homology. Kunneth over a field gives the graded tensor product without local-finiteness or connected-loop-space assumptions. Completion precedes looping throughout. Applying the criterion now proves all degrees of the full cellularization map without choosing an untwisted duality description of its source.

## Falsifiable boundaries

The initial countermodels remain valid: A=k disproves erasing infinite dimension; A=k times k[t] with augmentation onto k has compact proxy k and a nonzero cellular inclusion k->A, disproving erasing the Hopf hypothesis; a positive-degree polynomial Hopf algebra has degreewise-finite but infinite-total-dimensional nonzero ideals, disproving substitution of degreewise finiteness for finite total dimension. Connected G, p-groups and prime-to-p finite component groups are p-nilpotent cases outside the theorem's antecedent. No general coefficient ring, noncompact group or uncompleted-loop target has been substituted. Homological vanishing is not promoted to nullness in the derived category.

## Independent bounded computation

Before reading supplied code, I implemented H=Fp[y]/(y^p) tensor exterior(x1,x2), with even primitive y and odd primitive x1,x2. These are legitimate finite Hopf quotients in characteristic p: binomial coefficients make y^p primitive, and the exterior relations are compatible with the super coproduct. In characteristic2 I tested the grading-forgotten ordinary Hopf algebra; in characteristics3 and5 I tested parity bosonizations. Exact sparse coefficients give83,104 identity checks, including all basis triples for associativity, all basis pairs for coproduct multiplicativity, coassociativity/counits and both antipodes. Omitting coproduct parity and omitting antipode parity are separately detected in odd characteristic. These finite checks test conventions and do not establish the infinite theorem.

I then personally read the complete native verification script and ran a byte-identical owned isolated copy once normally. It tests a different, infinite noncommutative free tensor Hopf superalgebra on two odd and one even primitive generator. The tested input word lengths are bounded; its operations are untruncated. Complete JSON output matched native expected_results.json. A separate -O invocation was correctly refused before assertions could be disabled. These facts establish the advertised bounded reproduction scope, not all possible words or historical audit chronology.

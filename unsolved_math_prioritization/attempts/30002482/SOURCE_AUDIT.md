# Independent source-credit audit: ladder symplectic distinction

Date: 2026-10-10 UTC. Target: 30002482 / OWR-12863-001.

## Decision and exact scope

This is an independent internal AI source-credit and mathematical audit, with an AI-assisted reconstruction of the published proof. The reconstruction and audit are unrefereed; no external human peer review, journal acceptance of this audit, or formal proof-assistant certification is claimed.

**Accept prior resolution of the historical characteristic-zero p-adic target.** The result is due to Arnab Mitra, Omer Offen and Eitan Sayag, *Klyachko Models for Ladder Representations*, Documenta Mathematica 22 (2017), 611–657, Theorem 10.3 (announced as Theorem 1.2). This audit supplies no new theorem.

Let F be a nonarchimedean local field of characteristic zero, let rho be an irreducible smooth complex cuspidal representation of GL_d(F), and put nu=|det|_F. Consider nonempty segments D_i=[nu^{a_i}rho,nu^{b_i}rho] on one cuspidal Z-line, with a_1<...<a_{2r} and b_1<...<b_{2r}. Suppose each adjacent two-segment Langlands quotient Q(D_{2j-1},D_{2j}) is essentially Speh. Then, for N=d sum_i(b_i-a_i+1), N is even and

Hom_{Sp_N(F)}(Q(D_1,...,D_{2r}), C) != 0.

No unitarity, genericity, proper-ladder condition, bound on r, or restriction on the residue characteristic is imposed. In particular finite extensions of Q_2 are covered. The group is the symplectic subgroup of GL_N; conventions writing Sp_n for its rank and Sp_{2n} for its matrix size describe the same group when N=2n.

There are two separate field statements:

* The journal's stated ambient hypothesis is char(F) != 2 (Section 2.2, p.621). It is a field-characteristic condition, not an odd-residue-characteristic condition.
* This independent dependency audit certifies the characteristic-zero instance. Both Heumos–Rallis (1990) and Blanc–Delorme (2008), used in the proof, formulate their results in characteristic zero. An extension of those inputs to positive characteristic is not established here. This is a limit of this audit, not a disproof of the journal's broader statement.

The short 2014 OWR contribution does not expressly exclude equal characteristic 2. If it is read literally as asking for that extension, that extra scope remains unresolved by this audit. Even the journal's stated hypothesis does not cover it. No global-openness claim is made about that extension or the general distinction problem.

## 1. Original-source identification and intended context

The complete relevant contribution is Mitra, *On irreducible representations of GL_{2n}(F) with a symplectic period*, in Oberwolfach Report 03/2014, printed pp.161–163 (PDF pp.17–19; the last page only continues references). The conjecture is on printed p.162. Its G' consists of single ladders with paired essentially Speh quotients. Its subsequent statement about necessity for arbitrary irreducible products of ladders is a different question. Neither that subsequent statement nor a general classification of all irreducibles is silently folded into the selected target.

The OWR introduction describes the p-adic setting. The contemporaneous published companion, Mitra, *On representations of GL_{2n}(F) with a symplectic period*, Pacific J. Math. 268(2) (April 2014), 435–463, explicitly fixes characteristic zero on p.435 and again in Section 2 (Notation), p.437. Thus characteristic zero is a well-supported contextual interpretation, but it does not erase the OWR wording's literal field ambiguity. The arXiv posting 1601.03611 is a later posting of that companion and should not be called the first 2016 publication of the result.

The supplied record's background calls the target representations generic. That is mathematically misleading: irreducible generic representations cannot also have a symplectic model (Heumos–Rallis, Theorem 3.2.2; MOS Lemma 7.1). Genericity is not an assumption of the original assertion. The exact claim concerns an invariant complex linear functional on smooth representations; it is not a global automorphic period statement.

## 2. Convention audit: Q is L, and the list reverses

Mitra's segment preliminaries (published p.438; arXiv Section 2.2) define Q(D) as the irreducible quotient of the induction of the ascending cuspidal sequence in D. This is MOS L(D), the essentially square-integrable segment representation. For a multisegment, Mitra Q and MOS L are again the unique irreducible quotient of the product of these segment representations after putting the segments in standard order (no earlier segment precedes a later one). The original notation lists the underlying ladder increasingly; it does not license taking the quotient of an incorrectly ordered induction.

Set Gamma_i=D_{2r+1-i}. Then both endpoints of the Gamma_i strictly decrease. The representation is unchanged as a multisegment Langlands quotient:

Q(D_1,...,D_{2r}) = L({Gamma_1,...,Gamma_{2r}}).

This is reindexing of Langlands data, not application of the Zelevinsky involution or of a contragredient. One must not replace Q by Z. For example L({[1],[0]}) is a determinant twist of the trivial representation of GL_2, whereas Z of that multisegment is the corresponding Steinberg twist; the latter is generic and not symplectically distinguished.

For a two-segment ladder on this line, the essentially Speh condition means D_{2j}=nu D_{2j-1}. This follows from the definition of a two-step Speh quotient and uniqueness of its Langlands multisegment. Under reversal it becomes

Gamma_{2i-1}=nu Gamma_{2i}, for i=1,...,r.

The twist direction matters. Lengths in each pair agree, so N=2d sum_j length(D_{2j-1}). A determinant twist does not change distinction since its restriction to Sp_N is trivial. The distinction is therefore unaffected by the word “essentially.”

## 3. Dependency graph and checks

Theorem 10.3 uses the following inputs, all within the ordinary smooth complex representation setting.

1. **Standard modules and Jacquet modules.** MOS Sections 2, 6 and 9.0.1–9.0.3 use exact normalized parabolic induction, Langlands uniqueness, and the Jacquet-module formula for essentially square-integrable segment representations. Zelevinsky (1980), Section 9.1 and Proposition 9.5, fixes both the ascending-quotient convention and the decreasing segment-piece order. Successive Jacquet factors partition a segment from its largest endpoint downward. The selected formula agrees with MOS's normalization.
2. **Orbit restriction.** MOS Sections 3–4 and Lemma 5.1 give a finite orbit filtration. Distinction forces at least one relevant orbit. For its refined Levi, paired irreducible factors satisfy sigma_i=nu sigma_tau(i); fixed factors must themselves be symplectically distinguished. The admissible involution reverses the order of the pieces coming from each original segment. Offen (2006), Section 3.1 and Proposition 3/Corollary 1 of Section 3.2.3, give the stabilizers, modulus factors and Frobenius-reciprocity calculation. Its Remark 2 explains why the Bernstein–Zelevinsky filtration argument still applies when the orbit induction is not parabolic. The proof of the filtration theorem in Bernstein–Zelevinsky (1977), Section 5, was checked at this point, rather than assuming an unrestricted converse from orbit relevance.
3. **Generic obstruction.** Heumos–Rallis, Theorem 3.2.2, excludes an irreducible representation with both Whittaker and symplectic models. Its Section 3.2 specifically removes the unitarity assumption used in their preceding Theorem 3.1. This is precisely the strength needed for the essentially square-integrable Jacquet factors.
4. **Hereditary sufficiency.** MOS Lemma 5.2 invokes Blanc–Delorme, Theorem 2.8, to extend the open-orbit invariant form to a rational/meromorphic family. Corollary 5.3 extracts a nonzero leading coefficient along a generic complex line at the required parameter. Finite-length admissible inducing representations satisfy the needed finite-generation hypothesis. A pole or zero at the parameter is not a reason the invariant form disappears. This gives sufficiency for products of distinguished factors; it does not assert the converse.
5. **The two-step Speh case.** MOS Lemma 7.2 includes the local argument: nu L(D) x L(D) is distinguished by the closed orbit (Lemma 5.4); its length-two exact sequence has generic irreducible kernel. The generic obstruction forces a nonzero invariant form to factor through the quotient. This avoids use of a global Eisenstein-series nonvanishing theorem.
6. **Set combinatorics.** MOS Proposition 8.7 proves Hypothesis 8.5 for actual sets of segments. Corollary 9.2 therefore applies unconditionally to a ladder's distinct segments and to the distinct-endpoint standard modules occurring in its kernel. Neither Hypothesis 8.5 nor 8.6 is assumed for arbitrary multisegments in this use.
7. **Kernel description.** Lapid–Minguez, Theorem 1(i), is MOS Theorem 10.2. It describes the actual maximal proper submodule as the sum of adjacent endpoint-exchange modules, not merely an equality in a Grothendieck group. The author's institutional manuscript was checked through its proof in Theorem 7, Sections 2–4: the Jacquet-module filtration, disjoint weight submodules, and longest intertwining operator identify the sum with the kernel. The source is the 2012 author manuscript of the paper published in 2014; it was not mislabeled as a journal PDF.

These checks are an audit with the standard published classification and geometric-lemma machinery as foundations, not a reconstruction of all of representation theory from axioms. Unused global results, the later product-necessity argument, and the other Klyachko-model cases are not needed to close this proof.

## 4. Necessity in the published ladder theorem

Suppose L(m) is distinguished, where m is a ladder in decreasing order. Pulling a nonzero invariant form back along lambda(m) -> L(m) makes lambda(m) distinguished. For every standard ordering, the orbit filtration and the segment Jacquet formula produce a relevant decomposition of m in the sense of MOS Definition 8.1. Fixed points of the involution are excluded by the generic obstruction. This is the premise of the combinatorial distinguished-multisegment condition.

For the required set case, Proposition 8.7 is genuinely proved. It orders endpoint classes from largest to smallest and arranges beginnings within each class recursively. Lemma 8.2 forces the partners of the pieces of the first segment to be last pieces of segments in reverse index order. Endpoint maximality and the chosen beginning order then force the entire first segment to pair with its nu^{-1} translate, with no proper cut. Because multiplicities are one, removing that pair preserves the specified order on the remainder. Induction excludes every nontrivial relevant decomposition in this order. Hence m=n+nu n for a multisegment n.

For distinct decreasing endpoints, this pairing must be consecutive: the segment with highest endpoint can only be the upper member of a translate pair, and its partner's endpoint is exactly one lower. No integral endpoint can intervene. Remove the pair and repeat. Thus the number of segments is even and Gamma_{2i-1}=nu Gamma_{2i}. This verifies both necessity and equivalence with Speh type without assuming a general multisegment hypothesis.

## 5. Sufficiency and the descent to the irreducible quotient

Assume the adjacent translate-pair condition. Each two-segment quotient is distinguished by Lemma 7.2. Exact parabolic induction gives a surjection from lambda(m) onto their product. By Corollary 5.3 that product is distinguished, whether or not the product is irreducible. Pullback gives a nonzero invariant functional on lambda(m).

A distinguished standard module alone would not suffice. Let K be the kernel of lambda(m) -> L(m). Write Gamma_i=[a_i,b_i]. Lapid–Minguez identifies K as the sum of K_i, where the i-th term exchanges a_i and a_{i+1}, replacing the adjacent segments by

[a_{i+1},b_i] and [a_i,b_{i+1}],

while leaving all other factors unchanged. Every nonzero K_i is a standard module on distinct decreasing endpoints. If both replacement segments are nonempty, its multisegment cannot be Speh type:

* For odd i, the compulsory pairing of positions i and i+1 would give a_{i+1}=a_i+1, contrary to a_i>a_{i+1}.
* For even i, compulsory pairing at positions i-1 and i would give a_{i-1}=a_{i+1}+1, contrary to the two strict integral inequalities a_{i-1}>a_i>a_{i+1}.

The source's empty-segment conventions require an explicit boundary check. If a_i>b_{i+1}+1, K_i=0. If a_i=b_{i+1}+1, the second segment is empty and its GL_0 factor is omitted. The remaining nonempty multisegment has 2r-1 members, so cannot be n+nu n. Its endpoints are still distinct. Thus Corollary 9.2 excludes distinction in this case too. This makes explicit a suppressed notation case in the printed argument; it does not leave a theorem gap.

Consequently Hom_{Sp}(K_i,C)=0 for every i. Any invariant functional on their sum restricts to zero on each summand, so Hom_{Sp}(K,C)=0. The already constructed nonzero functional on lambda(m) annihilates K and descends nontrivially to L(m). No false right-exactness assertion for Hom is being used. This closes the sufficiency implication.

## 6. Exclusions and limits

Theorem 10.3 gives the selected ladder assertion and more, namely the converse inside the ladder class. It does not by itself give necessity for every irreducible product of ladders. MOS Theorem 1.4(2)/Proposition 12.5 explicitly uses the general combinatorial hypothesis; their two-factor Corollary 12.6 is separately unconditional. These statements must remain distinct.

The September 2026 Sharma manuscript, arXiv:2609.21384, concerns the general combinatorial hypotheses and explicitly retains a residual case in its abstract. It is neither needed for this acceptance nor used as a substitute proof of an unconditional general theorem. No priority, novelty, or comprehensive current-openness conclusion follows from this audit.

The audit accepts all ranks in characteristic zero, including residue characteristic 2. It makes no assertion for equal characteristic 2, no independent certification of the positive-characteristic dependency extension, no modular-coefficient assertion, and no transfer from Q to Z without changing the multisegment by the appropriate involution.

## Primary references

* [OWR 03/2014, original contribution pp.161–163](https://ems.press/content/serial-article-files/46494), DOI [10.4171/OWR/2014/03](https://doi.org/10.4171/OWR/2014/03).
* [Mitra–Offen–Sayag (2017), journal record](https://ems.press/journals/dm/articles/8965505), [journal PDF](https://ems.press/content/serial-article-files/26354), DOI [10.4171/DM/574](https://doi.org/10.4171/DM/574), especially pp.620–643.
* [Mitra (2014), journal PDF](https://msp.org/pjm/2014/268-2/pjm-v268-n2-p09-s.pdf), DOI [10.2140/pjm.2014.268.435](https://doi.org/10.2140/pjm.2014.268.435), pp.435, 437–439.
* [Lapid–Minguez, institutional record](https://idus.us.es/items/9cac5e3c-3334-4bd6-ad40-bd94ff4fb2f3), [author manuscript](https://idus.us.es/bitstreams/9d339eb9-03bf-4cac-bcc9-3ca8f34cf3a6/download), published in Amer. J. Math. 136(1) (2014), 111–142, DOI [10.1353/ajm.2014.0006](https://doi.org/10.1353/ajm.2014.0006).
* [Heumos–Rallis (1990), journal PDF](https://msp.org/pjm/1990/146-2/pjm-v146-n2-p05-p.pdf), Pacific J. Math. 146(2), 247–279, especially pp.247, 254–256 and 271.
* [Blanc–Delorme (2008), journal PDF](https://www.numdam.org/article/AIF_2008__58_1_213_0.pdf), Ann. Inst. Fourier 58(1), 213–261, especially pp.213, 234 and 243–249, DOI [10.5802/aif.2349](https://doi.org/10.5802/aif.2349).
* [Offen (2006), author manuscript](https://offen.net.technion.ac.il/files/2016/09/residualspectrum3.pdf), *Residual spectrum of GL_{2n} distinguished by the symplectic group*, Duke Math. J. 134(2), 313–357, Section 3; DOI [10.1215/S0012-7094-06-13423-3](https://doi.org/10.1215/S0012-7094-06-13423-3).
* [Bernstein–Zelevinsky (1977), journal scan](https://www.numdam.org/item/ASENS_1977_4_10_4_441_0.pdf), Ann. Sci. ENS (4) 10(4), 441–472, Sections 2.12, 5 and 6.4; DOI [10.24033/asens.1333](https://doi.org/10.24033/asens.1333).
* [Zelevinsky (1980), journal scan](https://www.numdam.org/item/ASENS_1980_4_13_2_165_0.pdf), Ann. Sci. ENS (4) 13(2), 165–210, Sections 1.1–1.6, 6.1, 8.6 and 9.1–9.7; DOI [10.24033/asens.1379](https://doi.org/10.24033/asens.1379).
* [Sharma, arXiv:2609.21384](https://arxiv.org/abs/2609.21384), manuscript, 18 September 2026, used only to distinguish the separate later topic.

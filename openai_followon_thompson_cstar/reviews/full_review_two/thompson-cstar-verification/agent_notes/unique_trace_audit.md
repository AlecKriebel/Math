# Independent audit: unique traces for Thompson-related groups

Checkpoint: 2026-10-07 05:13:26 UTC (2026-10-06 22:13:26 America/Los_Angeles).

Audit completion estimate: **100% for the requested unique-trace implication and its dependency audit**. This is a literature verification and elementary deduction, not a new result or a proof of nonamenability of `F`. No external communications or Git mutations were performed.

## Exact claim and scope

All groups below carry the discrete topology. A normalized trace means a **tracial state**: a positive linear functional `tau` with `tau(1)=1` and `tau(ab)=tau(ba)`. The relevant algebra is the **reduced** group C*-algebra `C*_r(G)`, with canonical trace `tau_can(lambda_g)=1` if `g=e` and `0` otherwise.

The verified conclusions are:

| Group `G` | Unique tracial state on `C*_r(G)` | Status |
|---|---|---|
| `T` | Yes | Unconditional, already established in the literature |
| `F` | Equivalent to nonamenability of `F` | Conditional on the unresolved hypothesis in the intended research program |
| `Aut(F)` | Equivalent to nonamenability of `F` | Elementary radical deduction, given the verified structure facts below |
| `Comm(F)` | Equivalent to nonamenability of `F` | Elementary radical deduction, given the verified structure facts below |

Thus the unique-trace portion of a conditional operator-algebra chain is fully supported. It gives **no new unconditional progress on nonamenability of `F`**. In particular, unconditional unique trace for `T` does not settle C*-simplicity of `T`.

## Primary theorem and proof dependencies

**Emmanuel Breuillard, Mehrdad Kalantar, Matthew Kennedy, Narutaka Ozawa**, *C*-simplicity and the unique trace property for discrete groups*, Publications mathématiques de l'IHÉS **126** (2017), 35–71, DOI [10.1007/s10240-017-0091-2](https://doi.org/10.1007/s10240-017-0091-2). Inspected version: [arXiv:1410.2518v3](https://arxiv.org/abs/1410.2518v3), revised 26 October 2016; [full text](https://arxiv.org/html/1410.2518v3).

Theorem **1.3**, proved as Corollary **4.3**, identifies reduced unique trace with `R_a(G)={e}`, where `R_a(G)` is the largest amenable normal subgroup. It also implies reduced unique trace for every C*-simple group.

Theorem **4.1** says a tracial state vanishes on `lambda_g` whenever `g` lies outside the radical. Its proof uses Proposition **2.8** (radical equals Furstenberg-boundary action kernel), Proposition **2.10** (equivariant injectivity), and boundary separation. If the radical is trivial, the trace consequently agrees with the canonical trace on the dense group algebra. Conversely, for nontrivial amenable normal `N`, compose the trivial character of `C*_r(N)` with its conditional expectation to obtain a second trace; its value is `1` on `N`. This character exists because `N` is amenable. These are reduced-algebra assertions, not full-algebra assertions. The paper records counterexamples to reversing C*-simplicity ⇒ unique trace.

## Structure facts checked in primary sources

**José Burillo, Sean Cleary, Claas E. Röver**, *Commensurations and Subgroups of Finite Index of Thompson's Group F*, Geometry & Topology **12** (2008), 1701–1709, DOI [10.2140/gt.2008.12.1701](https://doi.org/10.2140/gt.2008.12.1701). Inspected version: [arXiv:0711.0919v4](https://arxiv.org/abs/0711.0919v4), revised 20 March 2010; [full text](https://arxiv.org/html/0711.0919).

Section 1 identifies `F'` with the bounded-support orientation-preserving dyadic PL maps of the real line. Section 2 identifies `F/F'` with `Z^2` and uses simplicity of `F'`. Proposition **2.1** states that every finite-index `H≤F` has `H'=F'`. Theorem **3.1** realizes the full commensurator faithfully by eventually integrally periodically affine PL homeomorphisms of the line. Consequently bounded support is preserved under all commensurator conjugations, including orientation reversal.

**José Burillo, Sean Cleary, Claas E. Röver**, *Addendum to “Commensurations and Subgroups of Finite Index of Thompson's Group F”*, Geometry & Topology **17** (2013), 1199–1203, DOI [10.2140/gt.2013.17.1199](https://doi.org/10.2140/gt.2013.17.1199). Inspected version: [arXiv:1301.0616v1](https://arxiv.org/abs/1301.0616v1), submitted 3 January 2013; [full text](https://arxiv.org/html/1301.0616).

Section 1/Theorem **1** supplies the relevant exact sequences, including `1→F→Aut^+(F)→T×T→1` and `1→F'→K→H×H→1`. Section 2 explicitly uses simplicity of `T`. The chain `F'◁K◁Comm^+(F)` by itself does **not** prove `F'◁Comm(F)`; full normality follows directly from bounded-support preservation or the finite-index derived-subgroup statement above.

**Uffe Haagerup, Kristian Knudsen Olesen**, *Non-inner amenability of the Thompson groups T and V*, Journal of Functional Analysis **272** (2017), 4838–4852, DOI [10.1016/j.jfa.2017.02.003](https://doi.org/10.1016/j.jfa.2017.02.003). Inspected version: [arXiv:1609.05086](https://arxiv.org/abs/1609.05086); [full text](https://arxiv.org/html/1609.05086).

Proposition **2.4** exhibits `C2*C3≅PSL(2,Z)` inside `T`; thus `T` is nonamenable. Section 4 states that `C*_r(T)` has a unique tracial state and credits Dudko–Medynets. Remark **4.6** explicitly derives `F` nonamenable iff `C*_r(F)` has unique trace, using BKKO and Cannon–Floyd–Parry Theorem 4.3. **Textual hazard:** an earlier introduction sentence says “amenable” where this implication requires “non-amenable”; Remark 4.6 and the direct proof below resolve the inconsistency. Do not cite that introductory sentence for the equivalence.

Historical source cited by these papers: **J. W. Cannon, W. J. Floyd, W. R. Parry**, *Introductory notes on Richard Thompson's groups*, L'Enseignement Mathématique (2) **42** (1996), 215–256, DOI [10.5169/seals-87877](https://doi.org/10.5169/seals-87877). The browser did not fetch the Binghamton PDF in this audit; the structure facts actually inspected are recorded above, rather than falsely presenting this historical reference as freshly read.

## Checkable deductions

### General radical lemma

If `N◁G` is simple and nonamenable and `C_G(N)={e}`, then `R_a(G)={e}`. Indeed `R_a(G)∩N` is an amenable normal subgroup of `N`, so simplicity and nonamenability make this intersection trivial. Since both subgroups are normal, every commutator of an element of `R_a(G)` and an element of `N` belongs to that intersection. The radical therefore centralizes `N`, and trivial centralizer finishes the proof. This argument does not require C*-simplicity of `N`.

### Local-support centralizer lemma

The centralizer of the bounded-support copy of `F'` in `Homeo(R)` is trivial. For a nonidentity homeomorphism `g`, select a point moved by `g` and a sufficiently small interval `I` with `I∩g(I)=∅`. Choose dyadic endpoints inside `I` and a nonidentity dyadic PL bump `h` supported there; such `h` belongs to `F'`. Then the supports of `h` and `ghg^{-1}` are disjoint and nonempty, so these maps differ. This applies equally to orientation-preserving and orientation-reversing `g`.

### `F`

Amenability of `F'` is equivalent to amenability of `F`: one direction follows from subgroup closure, and the other from the amenable quotient `F/F'≅Z^2` and extension closure. If `F` is nonamenable, apply the radical lemma to `N=F'`, using simplicity and the local-support centralizer lemma. If `F` is amenable, `R_a(F)=F≠{e}`. BKKO gives the claimed equivalence.

### `T`

Since `T` is simple and nonamenable, any amenable normal subgroup must be trivial: it cannot equal `T`. BKKO therefore gives unique reduced trace **unconditionally**. Neither this argument nor group simplicity is a proof that `C*_r(T)` is simple.

### `Aut(F)`

The center of `F` is trivial by the local-support centralizer lemma. Hence its normal inner-automorphism subgroup `Inn(F)` is isomorphic to `F`. If `F` is nonamenable and `R=R_a(Aut(F))`, the intersection `R∩Inn(F)` is an amenable normal subgroup of the centerless copy of `F`; the preceding `F` argument makes it trivial. Normality yields `[R,Inn(F)]={e}`.

Also `C_Aut(F)(Inn(F))={e}`: if `alpha` centralizes every inner automorphism `c_f`, then `c_alpha(f)=alpha c_f alpha^{-1}=c_f`; centerlessness forces `alpha(f)=f` for every `f`. Thus `R={e}`. Conversely, if `F` is amenable, nontrivial normal `Inn(F)` is amenable and belongs to the radical. This proves the equivalence without needing a questionable inference from a nonamenable quotient.

### `Comm(F)`

The bounded-support subgroup `F'` is normal in the **full** commensurator by the inspected faithful PL model. If `F` is nonamenable, `F'` is simple and nonamenable, and its centralizer in `Comm(F)` is trivial by the local-support lemma. The radical lemma applies. Conversely, if `F` is amenable, the nontrivial normal subgroup `F'` is amenable and belongs to the radical. This proves the equivalence. The larger subgroup `F` need not be normal in `Comm(F)` and is not used as the normal subgroup here.

## Full C*-algebra and validation boundaries

For **every nontrivial group** `G`, the full algebra `C*(G)` has at least two distinct tracial states: the augmentation character `epsilon(u_g)=1` and the canonical regular trace pulled back through `C*(G)→C*_r(G)`. They differ on any nonidentity group element. Thus none of the four full group algebras has unique normalized trace, irrespective of `F`'s amenability. The full algebra also has a nonzero augmentation kernel, so reduced simplicity must not be transferred to it.

An independent adversarial agent checked the radical mechanism and highlighted the nontransitivity-of-normality trap for the commensurator. The argument above uses direct conjugation preservation instead. Boundary checks covered positivity/normalization, full versus reduced algebras, orientation reversal, the amenable branch of `F`, and the distinction between group simplicity and C*-simplicity. The exact remaining research gap is the upstream nonamenability assertion for `F`, not any unique-trace transfer in this note.

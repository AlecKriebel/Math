# Classical provenance and novelty audit

Audit checkpoint: **2026-10-06 22:13 PDT** (2026-10-07 05:13 UTC). This is a bounded historical audit by an independent internal agent. It uses exact full-text statements, not abstracts. Best-guess completion of this assigned audit: **95%**; unresolved earliest-original attribution is stated below. This estimate is not evidence of novelty or correctness. No external person was contacted, and no Git operations were performed.

## Decisive finding

The deduction of a scalar idempotent from a failure of direct finiteness is a documented classical ring-theoretic implication. Applying it to the October 4 torsion-free group algebra is an immediate consequence of the upstream construction. The associated absorbed cyclic projective and its zero class in `K_0` are standard module and group-completion deductions. This audit supplies no basis for advertising those mechanisms as newly invented. Whether the *specific consequence for the upstream example* was already publicly stated must be decided by the companion/current-disclosure audit; a failed search alone cannot establish novelty.

The exact new-input burden remains the upstream existence theorem: a finitely presented torsion-free `G`, and `a,b,c in F_2[G]` with `ab=1`, `ac=0`, and `c != 0`. This historical audit does not certify that theorem or its proof.

## 1. Exact conjecture, and a characteristic warning

**Johan Öinert, _Units, zero-divisors and idempotents in rings graded by torsion-free groups_, arXiv:1904.04847v3**, version dated July 20, 2023 (first arXiv submission April 9, 2019). Full-text [Problem 1 and Section 5](https://arxiv.org/html/1904.04847v3), canonical [PDF](https://arxiv.org/pdf/1904.04847v3).

Problem 1 assumes an arbitrary field `K` and a torsion-free group `G`; part (c) asks whether every idempotent in `K[G]` is `0` or `1`. Thus the characteristic-two specialization contradicted by the proposed example is:

> For every torsion-free group G and every field K of characteristic two, every scalar idempotent in K[G] is 0 or 1.

A single example over `F_2` refutes this universal statement. It does not refute a separate assertion restricted to any odd characteristic or to characteristic zero.

Theorem 5.2, with the specified nondegenerate torsion-free grading and domain degree-zero component, proves homogeneous units imply reducedness, reducedness is equivalent to being a domain, and a domain has only trivial idempotents. For group algebras the hypotheses hold. Theorem 6.2 gives triviality of **central** idempotents in every characteristic. Conjecture 8.1 is explicitly restricted to characteristic zero; this project does not contradict it.

**Citation-chain check.** Öinert cites Alain Valette, _Introduction to the Baum-Connes conjecture_ (2002), Remark 1.1, and Passman, _The algebraic structure of group rings_ (1977), Lemma 13.1.2. Valette's [full text, pp. 11–12](https://chatterj.perso.math.cnrs.fr/papers/Valette.pdf) states Conjecture 2 for `C[G]`, and Remark 1.1 derives the zero-divisor/idempotent implication from `p(1-p)=0`; it describes obtaining a square-zero element from a nontrivial zero divisor and then a nontrivial unit. **Valette's exact formulation is over C, so it must not be cited by itself for the positive-characteristic conjecture.** Passman's book was identified in the citation chain but its relevant page was not independently obtained in this audit.

The historical discussion in Öinert does not establish who first formulated the arbitrary-field idempotent conjecture. Avoid a first-attribution claim without the original historical item.

## 2. An explicitly documented pre-2026 implication to direct finiteness

**Giles Gardam, lecture notes, _The Kaplansky conjectures_.** Exact pinned [source](https://github.com/gilesgardam/lectures/blob/ec842e6a09851e98a38e2a4bea3b273b4a9debb9/kaplansky.tex), lines 38–88; [raw source](https://raw.githubusercontent.com/gilesgardam/lectures/ec842e6a09851e98a38e2a4bea3b273b4a9debb9/kaplansky.tex). The full-text proposition labeled `proposition:kaplansky_relations` states, for a fixed torsion-free group and arbitrary field:

`unit conjecture => zero-divisor conjecture => idempotent conjecture => direct finiteness`.

The proof of the final implication explicitly uses `alpha beta=1` and `beta alpha != 1`, obtaining `(beta alpha)^2=beta alpha`; it calls these implications elementary ring-theoretic observations. The displayed conjecture distinguishes arbitrary-field scalar idempotents for torsion-free groups from direct finiteness for **all** groups, including groups with torsion. This is enough to establish that deriving an idempotent from the new one-sided inverse was publicly documented before the October 2026 construction, irrespective of whether an earlier source was found.

Read-only [GitHub commit-history API](https://api.github.com/repos/gilesgardam/lectures/commits?path=kaplansky.tex&per_page=100) was retrieved on the audit date. It identifies the initial file history at October 24, 2023 and the last file-changing commit above at February 20, 2024, 14:34:31 UTC. The source is pinned to the latter rather than mutable `main`. This establishes a documented older disclosure, not an earliest-original attribution.

Working copies under `sources/provenance/`:

| File | SHA-256 |
|---|---|
| `gardam_kaplansky_ec842e6.tex` | `1d801581c6c5d358ffb8af0f4adf473f3c99160d1175cc12988a60d417e0e311` |
| `gardam_commit_history.json` | `1bbe100538b099f5df2873afbca3b0a803a95bfbec98ab86aba55e00b7c304fc` |

These are audit inputs. Their presence does not settle redistribution licensing, and they should not automatically be included in a published payload.

## 3. Direct finiteness versus different cancellation properties

**P. Ara, K. R. Goodearl, K. C. O'Meara, E. Pardo, _Separative cancellation for projective modules over exchange rings_, May 1996 report no. 142.** [Author/institutional full-text copy](https://ir.canterbury.ac.nz/bitstreams/9810640d-0c02-42b1-a9ac-49f0f8bd703b/download), p. 9, immediately preceding Proposition 2.3.

The authors define a directly finite module as one not isomorphic to a proper direct summand of itself. They identify direct finiteness of a ring with direct finiteness of its regular right module, equivalently `xy=1 => yx=1`. They identify **stable** finiteness with direct finiteness of every matrix ring, equivalently of all finitely generated projective modules. Their Proposition 2.3 needs the additional separativity hypothesis to infer stable finiteness from direct finiteness.

Consequently the relevant equivalent law here is precisely

`R_R ≅ R_R ⊕ P  => P=0`.

General cancellation of projectives means `A⊕C≅B⊕C => A≅B` for arbitrary finitely generated projectives, and must not be called equivalent to direct finiteness. The witness proposed here violates that stronger law by taking `A=P`, `B=0`, `C=R`; this *failure* follows immediately from failure of direct finiteness. It is not an additional independent group-theoretic breakthrough.

## 4. Self-contained algebraic check and its exact logical scope

The following computation is our independent check of the classical implication. Let `R` be any nonzero unital ring and assume `ab=1`, `ac=0`, `c != 0`. Set `p=ba` and `e=1-p`.

* `p^2=b(ab)a=ba=p`, so `e^2=1-2p+p^2=e`, in every characteristic.
* `ec=c-bac=c`, hence `e != 0`.
* `ap=aba=a`; since `a != 0` follows from `ab=1`, `p != 0`, hence `e != 1`.
* Orthogonal complementary idempotents give `R_R=pR⊕eR`.
* `pR⊆bR`, and `b=bab=pb` gives `bR⊆pR`.
* Left multiplication by `b` gives a right-module isomorphism `R_R -> bR`; its inverse is left multiplication by `a`, because `ab=1` and `ba` is the identity on `bR`.

Thus `P=eR` is nonzero, cyclic, and projective, and `R_R≅R_R⊕P`. More generally nonzero right modules absorbed by `R_R` are necessarily finitely generated projective, since they are summands of `R_R`. Conversely, an absorption isomorphism supplies a split epimorphism/endomorphism of `R_R` with a nonzero complementary kernel, producing `a,b` with `ab=1` and `ba != 1`.

None of the algebra requires torsion-freeness or characteristic two. Those hypotheses determine which conjecture the **upstream ring** contradicts. In particular, feeding this computation the September 23 torsion-containing example proves nothing about the torsion-free conjecture.

## 5. K-theory: vanishing of one projective class, not of the group

**Charles Weibel, _The K-book_ (AMS, 2013), Chapter II, Sections 1–2**, [author full-text chapter](https://sites.math.rutgers.edu/~weibel/Kbook/Kbook.ii.pdf), pp. 1–2 and 5–6. Section 2 defines `K_0(R)` as the group completion of the direct-sum monoid of finitely generated projective modules. Proposition 1.1(b) characterizes equality in a group completion by adding a common summand. Example 2.1.1 explains that a ring map to a field sends the regular-module class to `1` and splits off a copy of `Z`.

Our absorption yields `[R]=[R]+[P]`, hence `[P]=0`. This is a formal consequence of the definition; it does not mean `P=0`. It also does not say `K_0(R)=0`: for a group algebra over a field the inclusion of scalars followed by augmentation is the identity, so `K_0(K)=Z` is a direct summand of `K_0(K[G])`. In particular `[R]` is nonzero. A publication must keep these three statements separate.

## 6. Noncentrality is also classical

**R. G. Burns, _Central idempotents in group rings_, Canadian Mathematical Bulletin 13 (1970), 527–528**, [publisher full text](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0D33DC15FC39C1B6BD748C301A626E7C/S0008439500056101a.pdf/central_idempotents_in_group_rings.pdf), [DOI](https://doi.org/10.4153/CMB-1970-097-x). Its theorem, for arbitrary coefficient rings and groups, says that a central idempotent's support generates a finite group. For torsion-free `G`, this support group is trivial; over a field the coefficient is then `0` or `1`. Thus the proposed nontrivial idempotent is necessarily noncentral. Burns explicitly notes that his theorem follows from Passman's _Twisted group algebras of discrete groups_, Theorem 2.6. That earlier theorem was not separately checked here.

## Search record and remaining limits

All searches and primary-source reads were performed **2026-10-06 PDT**. Queries included the exact Öinert arXiv identifier; direct finiteness and projective cancellation; `K0`, `1-ba`, and one-sided inverses; the exact Valette title/Remark 1.1; and Burns, Rudin–Schneider, and Formanek title searches. Search result snippets and third-party summaries were used only to locate sources, not to certify mathematical statements.

Full-text reads completed: Öinert Problem 1, Proposition 5.1, Theorem 5.2, Theorem 6.2, Conjecture 8.1 and bibliography; Valette Conjecture 2 and Remark 1.1; pinned Gardam conjectures and implication proof; Ara–Goodearl–O'Meara–Pardo definitions and Proposition 2.3; Weibel group-completion and `K_0` definitions; and the complete Burns two-page paper.

Not independently read in full: Kaplansky's 1957/1970 original problem lists, Higman's thesis, the cited Passman book page, Formanek's 1973 paper, and Rudin–Schneider's 1964 paper. Therefore do not infer an earliest-original priority claim from this audit. Such earliest attribution is unnecessary to rule out novelty of the elementary reduction, since a dated pre-2026 primary lecture source already writes the exact implication and proof.

Recommended framing, subject to the companion/current-disclosure result: **a concise attributed consequence note of the October 4 construction and classical algebra**, never an independent new solution of direct finiteness, never a new cancellation theorem, and never a claim that the full K-theory group vanishes. If the complete consequence and proof already appeared publicly, follow the project's duplication rule and withhold a duplicate novelty preprint.

# Hypotheses, definitions, and literature status

## Primary recovery

The catalog URL https://www.unsolvedmath.com/problems/30004324 returned an internal fetch error to the web tool and HTTP 403 to a direct read. No access restriction was bypassed. The catalog descriptor identifies OWR-17296-007 and DOI 10.4171/OWR/2019/53. The actual theorem target was recovered from the public primary report and its cited research paper.

Fulger's OWR contribution spans printed pages 3287--3289. At printed p.3289 it proposes that P^n is characterized among n-dimensional projective manifolds by epsilon(T_X;x)>0 at some point. Its opening setup is a projective variety over an algebraically closed field. FM21 Conjecture 4.9 makes smoothness and the unrestricted algebraically closed field explicit. No hypothesis n>=3 is in the conjecture; the unresolved portion was beyond the known low-dimensional cases.

## Relative vector-bundle definition

Use quotient projectivization rho:P(E)=Proj_X Sym(E)->X and xi=c_1(O_{P(E)}(1)). Then

epsilon(E;x)=inf [xi.Gamma / mult_x(rho_*Gamma)],

where Gamma is an integral curve in P(E), its image contains x, and Gamma is not contracted by rho. The denominator uses the pushforward cycle: it includes the generic mapping degree of Gamma onto its image. Vertical curves are excluded. This is not a definition requiring E globally nef.

Equivalently, for integral curves C through x and their normalizations nu:Ctilde->C,

epsilon(E;x)=inf_C [mu_bar_min(nu^*E) / mult_x C].

In characteristic zero, mu_bar_min is the minimal slope among positive-rank quotients. In characteristic p>0 it is the limit of p^(-e) mu_min(F^{e*}(nu^*E)). Omitting this Frobenius normalization is an error in general. On P^1 both invariants equal the least splitting degree, so the candidate proof uses no unproved positive-characteristic slope substitution.

## Quantifiers must stay distinct

- Positivity at one fixed point is the exact target. The point may be special.
- A point satisfying the general-point convention of FM21 Proposition 4.8(2) is an additional hypothesis in characteristic zero. FM21 explicitly refers to Kebekus's convention; the retrieved 2001 preprint discusses avoidance of a specified countable exceptional union. No arbitrary fixed point is silently placed outside it.
- The OWR summary describes the Zariski-general case and explicitly contrasts one point, very general, and Zariski general. This language is recorded rather than conflated with the precise referenced hypothesis in the research article.
- Positivity at every point implies nefness on every curve, and FM21 Corollary 6.10 then implies ampleness. Mori applies to an ample tangent bundle. This does not itself settle positivity at one point.
- FM21 Proposition 3.35, a semicontinuity statement, assumes nefness of the special-fiber bundle and an uncountable field. Remark 3.36 identifies the nefness-dependent inequality in its proof. Applying it to arbitrary T_X without that hypothesis would be circular.
- FM21 Proposition 6.9 identifies the zero locus with the augmented base locus under nefness. The one-sided implication outside the augmented base locus implies positivity does not give the converse without nefness.

## Verified pre-existing results

FM21 (Journal of Pure and Applied Algebra 225 (2021), no.4, article 106559; DOI 10.1016/j.jpaa.2020.106559) proves the Fano case in any characteristic, the specified general-point case in characteristic zero, and the surface case in any characteristic (Proposition 4.8, Corollary 4.12). Corollary 4.6 gives uniruledness and separable rational connectedness from the one-point assumption. Homogeneous examples and P^n are computed in Section 4.1. The 2019 arXiv version has different section numbers: Conjecture 5.9, Proposition 5.8, Corollaries 5.6 and 5.12. The candidate cites the inspected published-layout manuscript by its 2021 numbering.

Chang's arXiv:2211.17172v2, dated 2025-07-10, proves the smooth projective toric case over an algebraically closed field of any characteristic (Theorem 0.2). The theorem does not require the point to lie in the dense torus. The paper also supplies a singular terminal toric threefold counterexample to dropping smoothness (Example 0.4/2.4). These are prior results, not achievements of this packet. The journal DOI is 10.1016/j.jpaa.2025.108046.

Bounded searches through 2026-10-05 found no primary source establishing the unrestricted conjecture after these papers. This is a retrieval observation, not an exhaustive novelty certification. The candidate proof is a new argument within this investigation, not a claim of historical priority.

## Prior repository/history check

Read-only searches of AlecKriebel/Math for exact ID 30004324 in code, commits, PRs, and branch names returned no matches; branch query `tangent` also returned none. The expected default-branch attempts path returned 404. The inspected problems directory had 18 entries, with no exact-ID folder. Searches on the word Seshadri located other problem IDs and were not treated as duplicate prior attempts. One recursive-tree request failed with transport closure, so the repository search is not exhaustive.

A bounded private conversation-context search did not yield an inspectable exact prior proof; unrelated mathematical histories were rejected as non-evidence. No absolute claim that the user has never attempted this problem is made. Private retrieval output is not part of this packet.

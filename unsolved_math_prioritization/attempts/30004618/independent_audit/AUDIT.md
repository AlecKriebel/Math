# Independent audit of the odd minimal strata packet

Problem 30004618, rank 781. Audit date: 5 October 2026 UTC.

## Verdict

**Accept as a scoped partial investigation, with the normalization clarification
in CORRECTIONS.md. The genus-12 conjecture is not solved.** The exact arithmetic,
the separating certificate, and the integer optimization are correct in the
stated coefficient model. No error invalidating these restricted results was
found. This is an independent AI audit, not human peer review or a novelty claim.

The input ZIP was verified at 18,469 bytes, SHA-256
62ee95de99e41e97f54a2f1bdad0623fab43d8317296a471145d0a764bbe169a.
Its manifest SHA-256 is
96c5ef2a3ef324896d96c1419d37ccd695290275f4db79e9a598a027925e2b56.
Every manifest entry and every archived payload byte matched the author directory.
The frozen package was not edited.

## Target and literature boundary

The target is the non-hyperelliptic odd-spin connected component of the
projectivized holomorphic minimal stratum over C. Its dimension is 2g-1. The
question concerns the ordinary Kodaira dimension of a smooth projective
birational model, including the coarse-space singularity issues. At g=12 the
desired value is 23.

The official report's Conjecture 1 includes genus 12. Theorem 1.4 of the
Chen-Costantini-Möller manuscript establishes g>=13 and explicitly leaves
g=10,11,12 beyond its conclusion. Current author lists identify its 2024 journal
publication. The later even-spin paper has a different component and its stated
range is g=31 and g>=33. Bounded current searches found no later resolution of
odd genus 12; this is not an exhaustive literature-absence certificate.

The report, CCM arXiv manuscript, CCM author manuscript, later even-spin PDF and
public supplement were freshly downloaded and independently hashed. All five
matched the frozen metadata. Relevant source pages and formulas were inspected;
the final journal PDF and full foundational proofs were not independently audited.
Source URLs and exact inspection limits are in SOURCE_AUDIT.json.

## Independent coefficient reconstruction

The new checker starts from signed differential orders and the definition
kappa(mu)=sum m(m+2)/(m+1), rather than importing the author's datum function.
For prongs (9,1,1,1,1,1,1,1), the top orders are (8,0,0,0,0,0,0,0)
and bottom orders are (22,-10,-2,-2,-2,-2,-2,-2,-2). It independently obtains
kappa=528/23, kappa_top=80/9, kappa_bottom=2912/207, ell=9,
P_minus_1=64/9 and N_bottom=7.

For NF, the checker first reconstructs the pointed Weierstrass class using
the psi conversion, combines it with the Brill-Noether class according to
equation (46), and only then normalizes its lambda coefficient to 12. This gives
the same horizontal/vertical contributions as the packet:

- W_mid: 89/45 and 2912/405
- 2 NF: 311/179 and 19472/1611
- 2 Hur: 57/35 and 1216/105
- Compensated canonical term: -45/23 and -15142/1863

All witness edges are nonseparating, so compact-type pullback terms do not enter.
The midpoint divisor is applicable to the odd component; the effectivity
hypotheses of the NF and Hurwitz divisors include genus 12 non-hyperelliptic
components. The source's fixed effective classes can underestimate boundary
vanishing. The packet correctly does not replace them by exact effective-cone
information.

Solving the two affine inequalities independently gives
y>1845/2024 and y<300065/371128. The second upper bound is smaller, and the
vertical value at the horizontal zero is -940/1863. For normalized weights
(t,u,v) of W_mid, 2 NF and 2 Hur, the separating functional gives

b + (2017/99)h = -940/1863 - (286/105)v.

It is negative at all three simplex vertices, hence throughout the real simplex.
This is an exact infeasibility proof for the fixed model. All 5,151
denominator-100 triples were also checked as implementation controls.

## Graph geometry and singularity audit

The graph has arithmetic genus 5+8-2+1=12. Stability holds: the rational bottom
has nine special points, and the top has genus five and eight attachments. The
top and bottom differential orders sum to 8 and -2, respectively, as required.
No degree or stability obstruction invalidates the numerical datum.

There is also no apparent residue obstruction: with a single connected top
component, the global residue condition on the bottom is the total sum of its
eight pole residues, which vanishes by the residue theorem. On P1 the listed
bottom signature can be written explicitly, for example by placing its unique
zero at infinity and taking dz divided by a product with exponents 10,2,...,2.

Parity is not determined merely by labeling the total genus. All prongs are odd,
so the local orders are even. A compatible proposed spin description has
O(4q) on a genus-five odd minimal top and the half-divisor of degree -1 on the
rational bottom; the latter has no sections. Turning that description into a
proof of membership of a particular boundary component uses the established
spin/smoothing framework. This audit does not independently reconstruct that
framework or certify all smoothing choices. The numerical propositions do not
need such a certification, and the packet explicitly avoids claiming one.
In particular, the audit does not promote the witness to an unavoidable
extremal effective-cone obstruction.

The ramification distinction is consistent. The graph is not a tree, so it is
neither HBT nor HTB. It is not HBB: an involution on eight parallel edges has
at least four edge orbits, so its quotient cannot be a backbone tree. Thus the
additional codimension-one ramification term delta_H is zero here. This does
not remove higher-codimension non-canonical singularities or exceptional
divisors over them.

Proposition 5.13's first exceptional case would require 9>=13; its second
prong pattern is absent. The third case applies, since prongs 1 and 9 occur,
and gives R=64/81. With b_NC=ell*R-1, equation (69) becomes
(b_NC+1+delta_H)/ell=R. The canonical versus log-canonical correction is
therefore accounted for once, and the packet has not dropped a hidden 1/ell
term. R is an extension-compensation estimate, not an exact discrepancy of
every exceptional divisor on a resolution.

## Repairs and controls

For each sigma=0,...,9, an independent dynamic program minimized the bridge
energy over all permitted nonnegative integral heights, allowing downward
increments. The resulting twist gains are
0,4,7,9,10,10,9,7,4,0. The maximum 10 equals the existing midpoint correction.
The elementary inequality a^2>=a for every integer a also proves the lower
energy bound without relying on a finite search or a monotonicity assumption.
This establishes optimality only for the specified vertical twisting family.

The pair becomes strictly feasible after replacing R by r exactly when
r<26/99. Equality allows only the common zero at the limiting horizontal
weight and does not give strict positivity. An exact perturbed feasible pair
was checked as a control. A valid global extension theorem for such a smaller
compensation is not supplied.

The genus-13 control uses W_mid with 2 BN, not 2 NF. Its interval is
1071/1375 < y < 40409/51625. At y=443411/567875 the two residuals are
16/30975 and 32/3025, both positive. This verifies a boundary-pair control,
not the all-boundary general-type theorem.

The spin-moduli shortcut is correctly rejected: the source has dimension 23
and the odd-spin moduli space has dimension 33 in genus 12. General type of
the ambient space does not imply general type of this proper sublocus.

## Provenance and prior work

The complete 68,931,837-byte problems corpus and 80,334,822-byte research-report
corpus were independently rehashed against the live repository manifest.
Both exact report keys are absent from the complete 6,701-entry dictionary.
The selected and duplicate statement/review hashes were independently
recomputed, using the repository's documented JSON serialization. The selected
review hash remains fce1058dfb86fd826a06545d85e42203a444feff1471695a483935923a2cd8c6.
The original statements for 30004618 and 30004619 are equal; the latter is a
duplicate extraction, not another proof budget.

Live main was 657add47248e08c05126627b7e2caa6a597d4831. Its catalog blob still
matches the fully hashed local catalog. Its actual attempts directory contains
62 entries and neither target ID. Targeted PR, commit, branch and topic checks
found no selected-target prior artifact. The related-target index contains
neither ID. These checks do not cover deleted branches, private or unindexed
artifacts, or unpublished working trees; a queued status alone is not an
absence certificate.

## Safe disposition

Retain the unsolved/exhausted disposition after the five recorded approach
families. The audit added checks of the existing claims rather than a sixth
proof search. Preserve the frozen author packet and publish this audit and its
clarifications alongside it if publication is otherwise authorized. No remote
writes were performed in this audit.

Run `python3 independent_check.py` to reproduce the independent arithmetic.
The author's verifier was also replayed in an isolated copy and matched its
frozen RESULTS.json exactly. Neither verifier computes a Kodaira dimension.
The audit package contains only authored analysis, authored code and results,
and public verification metadata; source text, PDFs, screenshots, dataset
contents, upstream programs and private coordination records are excluded.

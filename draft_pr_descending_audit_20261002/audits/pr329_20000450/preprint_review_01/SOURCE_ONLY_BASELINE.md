# Fresh source-only baseline: PR329 / problem20000450

Freeze phase: SOURCE ONLY. No candidate manuscript, candidate archive or metadata,
author/root/sibling review, imported report, publication, or historical verdict has
been opened. No PR344 or other-project verdict has been read. This baseline is
formed independently from the original AIM source and mathematical deductions.

## Source and native evidence

Original URL: https://www.aimath.org/WWN/qptsurface2/qptsurface2.pdf

The independently downloaded original is `evidence/source/qptsurface2.pdf`.
The native retrieval was 2026-10-04T10:56:41Z to 2026-10-04T10:56:42Z,
HTTP 200, 502057 bytes. Actual HTTP headers, curl stdout/stderr, argv, exit status
and native `/bin/date` clocks are retained under `evidence/source/` with the
prefix `retrieve_original_01`. There were no retrieval failures. Extraction,
inspection and rendering also retain their full actual process streams and
native timestamps. Computed hashes are integrity metadata, not substitutes for
these native execution records.

PDF metadata reports 59 physical pages. Physical page 51 also bears printed
page number 51. I inspected its rendered pixels and extracted text, including
Question 17 and all four immediately following remarks. The AIM cover dates
the document version to November 22, 2004 and identifies the December 2002
workshop. A source-wide text search located no other occurrence of the pentagon
construction; broader lecture context is present and is available for later
checks of particular contextual claims.

## Exact target and source's known baseline

Question 17 starts with a regular pentagon, its circumcircle, and the affine
pencil P + lambda C^2 = 0. P means the product of five side-line equations.
The intended generic normalization has genus one, five vertex double points,
and five points at infinity. The requested task is to compute its 5-torsion.
The four remarks respectively identify the infinity points as known torsion,
motivate torsors and a universal X_1(5) twist, ask about the pencil's conference
context, and invite nonregular/star variants. The source offers motivation for
Sha candidates, not a proven nontrivial Sha example or a universal arithmetic
claim. Attribution is McCallum for the question/modular motivation, Ellenberg
for pencil context, and Voloch for shape variants.

That paragraph is a paraphrase of the source, not proof of its claims. In
particular, the question omits the base field, an origin, and the exceptional
parameter locus. Its statements about genus and torsion must be interpreted
with those conventions supplied and justified by any candidate.

## Independent conventions and deductions

1. Work first over a characteristic-zero algebraically closed field, with a
   genuine nondegenerate regular pentagon. Later descend to a specified field
   of coefficients. A geometric regularity assumption alone does not supply
   rational coefficients over Q or Q-rationality of all infinity points.
2. If P_5(X,Y,Z) is the homogeneous side product and C_2(X,Y,Z) the homogeneous
   circumcircle, the projective equation is
   F_lambda = P_5 + lambda Z C_2^2 = 0. The factor Z is essential because the
   affine summands have degrees five and four. Relative rescaling of P and C
   changes the parameter convention.
3. Genus 1 requires geometric irreducibility and singularity control. A plane
   quintic has arithmetic genus 6. Five ordinary nodes contribute delta = 5,
   leaving geometric genus 1 only if there are no extra singularities. At
   lambda = 0 the curve is a union of lines. At special nonzero parameters,
   vertex tangency, extra singularities or reducibility must be excluded or
   separately analyzed. The parameter at infinity also needs a separate fiber
   convention; it is not a smooth member of the affine pencil.
4. Infinity satisfies P_5(X,Y,0) = 0. Distinct side directions give five
   distinct infinity points. An elliptic group structure is on the smooth
   normalization after choosing an origin O; a genus-one torsor without a
   rational point has no intrinsic set called its torsion points.
5. If O is one infinity point, the source's five infinity points can describe
   at most one order-five cyclic subgroup. In characteristic zero E[5](kbar)
   has 25 points, with two independent generators. Computing or proving just
   those five points does not compute all of E[5]. A satisfactory full answer
   can instead give an explicit verified algebra or equations describing the
   remaining points and their fields, provided completeness is proved.
6. Independent geometric mechanism for the known cyclic subgroup: rotation
   through one fifth of a turn preserves the affine equation (after coherent
   normalization of the line product) and cyclically permutes the infinity
   points. On a smooth genus-one normalization it has order five. The
   Riemann-Hurwitz equation for an order-five automorphism with r fixed points
   is 0 = 5(2g_quotient - 2) + 4r. The only nonnegative integral solution is
   g_quotient = 1, r = 0. Every genus-one automorphism becomes u(Q)+T after
   choosing O. If u is not the identity, u-id is a nonzero elliptic
   endomorphism and is surjective, yielding a fixed point, a contradiction.
   Thus rotation is translation by a nonzero point T of exact order five.
   Its infinity orbit is {O,T,2T,3T,4T}. This is a baseline derivation, not a
   novelty claim, and depends explicitly on the smooth genus-one hypothesis.
7. A 5-covering, order-five torsor, and nonzero Sha[5] class are different
   claims. The last needs both everywhere local solubility and global
   nontriviality over an explicit number field. A rational origin trivializes
   a torsor. No arithmetic conclusion follows merely from the drawn pentagon
   or from the existence of a rational 5-torsion subgroup on its Jacobian.

## Success criteria and boundaries

The central computation succeeds only if the candidate identifies the exact
smooth generic family and coefficient field, supplies a normalization or
equivalent smooth model, states the origin/torsor interpretation, and provides
checkable complete 5-torsion data with proved order, independence and
completeness. Formulae need verified maps and inverse/exceptional-chart
coverage, and all parameter restrictions must be explicit. A result limited
to the infinity subgroup may be valid partial evidence, but is narrower than
the main question.

For each additional body claim, require its own stated assumptions and proof:
modular parameter and twist, arithmetic descent and torsor class, any Sha
claim, pencil context, or shape extension. Merely repeating source motivation
does not discharge these. The four remarks are context and suggested avenues;
they do not by themselves require every possible extension to be solved.
Publication scope and abstract must accurately reflect what is proved.

Boundary/negative cases to retain: lambda=0; special lambda with degenerate
vertex tangent cone; extra singular points; projective lambda=infinity;
coincident/parallel/repeated side directions; C scale changes; regular versus
arbitrary pentagons; star constructions with changed intersection scheme;
characteristic 5 (outside the default theorem); rational versus geometric
origins; coefficient field lacking splitting data; torsion subgroup versus
full torsion; local solubility versus global torsor triviality; rational maps
with vanishing denominators or collapsed charts.

## Frozen adversarial families

| Family | Independent mechanism | Checkable evidence planned | Initial status / exact gap |
|---|---|---|---|
| G: geometry | Reconstruct homogeneous pencil, singular scheme, tangent cones, genus | Own polynomial derivations and exact substitutions; generic and degenerate examples | Not started on candidate; smooth generic locus unknown |
| T: torsion | Independent group-law/order calculations and full division algebra | Exact multiples, independent generator or complete finite torsion scheme, negative controls | Known cyclic mechanism derived; full candidate E[5] unknown |
| B: maps | Compose forward/inverse birational maps and enumerate base loci | Cleared-denominator identities with excluded factors and chart analysis | Candidate maps unavailable |
| M: moduli/descent | Independently compare j/discriminant and level structure; fields and twists | Exact rational-function identities, extension degrees, Galois/action checks | Candidate parameter normalization and arithmetic assertions unavailable |
| A: arithmetic | Separate torsor period/index, local tests, global nontriviality | Explicit descent and local certificates if claimed | No Sha inference is assumed; candidate claim unknown |
| P: pencil/shape | Test singular fibers and deformations separately from central torsion | Independent fiber/collision examples and scope checks | Candidate extensions unavailable |
| C: computation | Rebuild inputs and replay each claimed result from raw source | Actual stdout/stderr, native UTC clocks, deterministic independent controls | Candidate code/data unavailable |
| S: scholarship | Read primary cited inputs and compare exact claims/novelty | Citation-to-claim matrix, chronology, proved versus cited assumptions | Candidate bibliography unavailable |
| W: whole package | Cross-check all body, auxiliary and metadata statements against artifacts | Full inventory and contradiction/omission register | Qualified eight-input package not yet released |

Routes will be marked blocked if they merely transfer the central difficulty
to an equivalent unsupported assertion. No favorable verdict or publication
clearance is to be inferred from this preparatory baseline.

## Frozen whole-body / mode inventory

Once explicitly released by root, inventory all eight qualified inputs before
replay. Record their supplied locations, roles, byte hashes and own-copy
provenance without mutating sources. Read the complete paper, including title,
abstract, introduction, problem statement, every definition/lemma/theorem,
proof, construction, example, computation, figure/table, appendix, conclusion,
limitations and bibliography. Review the complete archive's code, data,
environment descriptions, generated outputs and replay instructions, and all
release metadata such as README, CITATION, manifests and version/DOI/author
fields present in the released inputs. If an expected component is absent,
record absence rather than inventing its content.

Classify evidence modes independently: exact proof/derivation; symbolic
identity; finite exhaustive computation; numerical/empirical evidence;
literature-dependent deduction; heuristic/conjectural motivation; provenance
or reproducibility claim; packaging/metadata claim. Cover each mode appearing
anywhere in the full body, not just a narrow addendum. Each assertion gets a
role, assumptions, evidence location, adversarial check, result and exact
remaining gap. Computed summaries never replace actual native retrieval/replay
records. Every unsuccessful attempt remains retained. Any later strategy
change must be timestamped and justified without retroactively changing this
source-only freeze.

## Independence and authority boundary

Only files inside this review's dedicated folder may be created or modified.
No Git/index/queue/PR writes, source namespace mutation, publication, tracker
writes, package installation, or communication with individuals is permitted.
Internal reporting to the parent agent is task coordination, not outside
outreach. No final self-seal or publication clearance will be issued.

This source-only baseline is frozen before candidate release. Its integrity
hash and actual native freeze time are recorded separately. Await explicit
root release before opening any candidate material.

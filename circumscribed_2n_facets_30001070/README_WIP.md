# Work in progress: circumscribed 2n-facet polytopes

UnsolvedMath ID30001070, OWR-2090-023, queue rank429. These are incomplete research notes and exact or explicitly labeled diagnostic checks. **No full resolution, verified solution, or novelty claim is made.**

The exact target concerns the maximum Euclidean norm in a bounded n-dimensional convex polytope with exactly2n facets containing the origin-centered unit ball: the conjectured lower bound is sqrt(n), with equality precisely for circumscribed cubes. No symmetry assumption is allowed. This is a radius/containment problem, not a volume or surface-area minimization problem.

Final WIP checkpoint: five of five substantive author turns; the author budget is exhausted. The scope-preserving polar reduction, local cube calculation, and a global centered tight-frame lemma are recorded. They leave the unrestricted nonsymmetric problem unresolved. See FINAL_STATUS.md and CORRECTIONS.md. Exact special-case checks are distinguished from floating-point diagnostics. Existing antipodal and low-dimensional results receive prior credit.

## Sources

- Chuanming Zong, Conjecture2, Section4, ‘Tight polytope around the unit ball’, Oberwolfach Report44/2008, printed p2547. DOI: https://doi.org/10.4171/owr/2008/44 . Primary PDF: https://ems.press/content/serial-article-files/46191?nt=1 . The source notes openness for n>=5. The imported corpus context mistakenly describes the neighboring blocking-number conjecture; these notes use the correct primary statement.
- Sergiy Borodachov, Optimal Antipodal Configuration of2d Points on a Sphere in R^d for Covering,2022, pp2–3 and Theorem2.2: https://arxiv.org/abs/2210.12472 . Its antipodal restriction is essential.
- Alexander E.Litvak, Mathias Sonnleitner, Tomasz Szczepanski, Minimal Dispersion on the Sphere, Discrete & Computational Geometry76(2026),1293–1321, published20August2026, Introduction p1295: https://doi.org/10.1007/s00454-025-00812-8 . The cross-polytope covering optimum is still described as conjectural.
- Imported problem metadata: UnsolvedMath Contributors, ulamai/UnsolvedMath, snapshot37e53eabe540fb458758e198be61634bd02ee008, https://huggingface.co/datasets/ulamai/UnsolvedMath . Metadata license CC-BY-4.0; underlying sources retain their own terms. Both corpus-file hashes were checked against the repository's provenance manifest before research.

Run check_turn_1.py, check_turn_2.py, check_turn_3.py, check_turn_4.py, and check_turn_5.py with Python and SymPy for exact checks. diagnose_weighted_mass.py and diagnose_two_simplexes.py also require NumPy and SciPy and is expressly non-certifying. The notes give the mathematical arguments; finite checks do not establish universal conclusions.

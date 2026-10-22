# Source and prior-work gate

Checked 2026-10-03 UTC.

## Exact question and literature status

- Catalogue locator: https://www.unsolvedmath.com/problems/2306017, AMR-022-6017. The live request returned HTTP 403.
- The identity was checked against Hayman–Lingham, [arXiv:1809.07200](https://arxiv.org/abs/1809.07200), Problem 6.17, printed p. 121 / PDF leaf 122. The complete statement and update were read and visually inspected.
- The target minimizes ordinary planar image area among normalized univalent functions with prescribed second coefficient. There is no convexity, omitted-area, or point-evaluation constraint.
- The 2018 update's report of no progress is stale. The 2006 primary paper states the target theorem and explicitly credits the 1999 paper. An incomplete independent verification of a proof does not make this a literature-open problem.

## Resolving literature and coverage

1. D. Aharonov, H. S. Shapiro, A. Yu. Solynin, *A minimal area problem in conformal mapping*, J. Analyse Math. 78 (1999), 157–176, [DOI](https://doi.org/10.1007/BF02791132).
   - Publisher metadata and abstract were checked. Full text was not obtained; publisher access required purchase or login.
   - This paper is credited for the historical resolution. Its original proof is not represented as read.

2. The same authors, *Minimal area problems for functions with integral representation*, J. Analyse Math. 98 (2006), 83–111, [DOI](https://doi.org/10.1007/BF02790271), [author-posted text](https://www.academia.edu/31230874/Minimal_area_problems_for_functions_with_integral_representation).
   - Read pp. 83–90 and all of Section 4, pp. 105–109, including Lemma 8, Theorem 3 and its complete kernel calculation, Lemma 9, and Theorem 4.
   - Theorem 3 treats the typically-real Dirichlet-energy problem. Theorem 4 states the exact prescribed-second-coefficient result for the full univalent class and its equality cases.
   - The proof of Theorem 4 imports coefficient Lemma 9 from 1999. That unavailable proof has not been silently counted as read.
   - The accessible text is OCR, not page images. The normalization and lower-bound algebra were independently recomputed. The typically-real objective is area counted with multiplicity; it equals ordinary image area for univalent maps.

3. The same authors, *A minimal area problem in conformal mapping II*, J. Analyse Math. 83 (2001), 259–288, [DOI](https://doi.org/10.1007/BF02790264), [author-posted text](https://www.academia.edu/31230876/A_minimal_area_problem_in_conformal_mapping_II).
   - Read pp. 259–268, including Lemmas 2–3 and both halves of the comparison (2.1).
   - The author-posted OCR of (2.5) gives a decrease under a biangle symmetrization. The cited Solynin (1993), [Lemma 1.3](https://www.mathnet.ru/eng/znsl5788), printed p. 120, gives the opposite direction for its specialized transformation. The relevant 1993 page image was checked. The inclusion convention on p. 13 of Solynin's [1999 modulus survey](https://www.mathnet.ru/rus/aa1040) does not resolve the conflict by a simple sign-convention change.
   - No correction, translation change, or different applicable biangle theorem has been verified. Exact 2001 page images were unavailable without authentication on the author-posted host. No account action or agreement was attempted.
   - PROOF.md no longer relies on the biangle argument. Its replacement uses only the ordinary-radius method behind the first half of (2.1), applied to the negative slit, with all inclusions stated explicitly. Neither full-S uniqueness nor the later quadrature-domain arguments are independently claimed.

4. V. N. Dubinin, *Symmetrization in the geometric theory of functions of a complex variable*, Russian Math. Surveys 49:1 (1994), 1–79, [DOI](https://doi.org/10.1070/RM1994v049n01ABEH002002), [publisher archive](https://www.mathnet.ru/eng/rm1153).
   - The openly linked English PDF was obtained without authentication.
   - Read the interior reduced-modulus and conformal-radius setup, pp. 10–13, and the ordinary circular-symmetrization definition and inequalities, pp. 19–20. Page images of pp. 11–13 and 19–20 were inspected, especially (1.8), (1.16), and (1.17).
   - Taking one marked interior point at zero in (1.17), and using (1.8), gives exactly R(V,0) <= R(V*,0). This is ordinary conformal radius, not a boundary-biangle modulus.
   - The definition preserves whole circles only when they are fully contained; a proper intersection of angular length 2 pi becomes a punctured circle. This verifies the convention essential to the replacement slit inclusion.
   - The classical symmetrization inequality is retained as an external theorem. The survey states it and outlines its derivation; no claim is made to have reconstructed every foundational capacity proof.

5. D. Aharonov and H. S. Shapiro, *A minimal-area problem in conformal mapping (Abstract)*, in *Proceedings of the Symposium on Complex Analysis, Canterbury 1973* (1974), pp. 1–5, [DOI](https://doi.org/10.1017/CBO9780511662263.002).
   - All five printed pages of the announcement were read visually in the [publisher preview](https://api.pageplace.de/preview/DT0400.9780511891809_A23680318/preview-9780511891809_A23680318.pdf).
   - Theorem 5 gives 27/8 conditionally on two topological properties. It is historical corroboration, not an unconditional resolving proof.

## Numerical discrepancy and proof scope

The 1999 publisher HTML abstract displays 27/7. The explicit finite-area witness rules out that stronger displayed bound. The 1974 printed announcement and 2006 Theorem 3 give 27/8. This is a source-transcription discrepancy; no flaw in the original 1999 theorem is inferred from it.

The note proves the exact minimum by its explicit extremal, the typically-real energy estimate, and a reconstructed ordinary-radius coefficient comparison. It retains classical Robertson–Herglotz representation, Riemann mapping/kernel convergence, ordinary conformal-radius symmetrization, and the second-coefficient theorem as named external inputs. Its symbolic script checks algebra only. Uniqueness is independently proved in the polynomial range and for the typically-real problem; full-S uniqueness for 1/2 < a < 2 remains attributed to the published theorem.

## Prior repository work

Read-only checks in AlecKriebel/Math preceded drafting:

- PR searches in all states for the exact ID, exact code, “6.17”, “minimal area”, and “Solynin” returned no matches.
- Exact-ID branch and commit searches returned no matches.
- Default-branch exact-ID code search returned no matches; search-index coverage is not assumed complete.
- The actual 112-entry root listing and the complete nontruncated 580-entry problems subtree contained no matching ID or subject path.
- The target queue row separately read `queued`, `0/5`. This row was not used alone to infer absence of prior work.

These checks support “no matching earlier repository attempt found,” not a claim that every historical ref has been exhaustively searched.

## Conclusion and claim boundary

The exact question has a prior published resolution. The unresolved biangle-source discrepancy is recorded and is excluded from the revised argument. The comparison now has an explicit separate proof using the ordinary conformal-radius theorem whose authoritative page images were inspected. There is no original-solution claim, no claim that the 1999 proof or the 2001/2006 page images were read, and no claim of independent full-class equality classification or formal verification.

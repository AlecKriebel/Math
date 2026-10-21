# Source gate: row 1851 / 30005646 / OWR-14297740-018

Checked 2026-10-21 UTC.

## Verdict

**Statement recovered; proof-resolution gate remains open.** The queue title's unqualified “global fields” is materially misleading: the recovered question concerns **higher-dimensional global fields**, specifically function fields of curves over finite extensions of Q_p. It is not a request for a strict stage above 2 over number fields, nor for strictness at every Postnikov level. A September 2024 primary seminar announcement claims the desired kind of separation, but no inspectable proof or explicit example was recovered. Do not turn the announcement into a verified resolution, or claim confidently that nobody has examples.

## Primary source and exact mathematical target

David Corwin, “The étale homotopy obstruction and its applications,” in *MFO-RIMS Tandem Workshop: Arithmetic Homotopy and Galois Theory*, Oberwolfach Report 42/2023, DOI 10.4171/OWR/2023/42, §§2 and 6, especially printed p.2459 (PDF page 83).

- Published PDF: https://ems.press/content/serial-article-files/47479
- Institutional mirror: https://publications.mfo.de/bitstream/handle/mfo/4128/OWR_2023_42.pdf?sequence=4
- Earlier report draft: https://pro.univ-lille.fr/fileadmin/user_upload/pages_pros/pierre_debes/V7-MFOreport2023.pdf

The exact inclusion sought is

    X(A_K)^h ⊊ X(A_K)^{h,2}.

Section 6.2 takes K=k(C), k/Q_p finite, and places v given by closed points of C, with completions K_v and the corresponding adeles A_K. The paragraph says “curve C” without formally specifying its full model hypotheses. A clean working realization is a smooth projective geometrically integral curve over k; that is an explicit conventional sharpening, not a verbatim extra assumption recovered from the paragraph. In this setting cd(K)=3, rather than the dimension-2 number-field situation.

Section 6.3 isolates geometrically simply connected X with geometric étale homology H_3=0 as a test case. It lists smooth projective geometrically rational surfaces and homogeneous spaces under a simple simply connected algebraic group with sufficiently large torus stabilizer. The report does not quantify “sufficiently large.” Projectivity is explicit for the surface option, not imposed on every homogeneous-space example. The condition is **homology H_3**, not cohomology H^3. The rendered original confirms this subscript and the strict inclusion sign.

Under the displayed geometric conditions the report identifies

    X(A_K)^Zh = X(A_K)^{Zh,2} = X(A_K)^{h,2}.

Thus a point surviving stage 2 but not full homotopy is the desired witness. Emptiness of the full set and nonemptiness of the stage-2 set would be a stronger sufficient witness; the stated question only requires strict inclusion. No universal “for each n” quantifier occurs. For cd=3 the potential new contribution is stage 3 (geometric π_3); stages beyond 3 are not the intended ladder.

## Definition and comparison safeguards

Write E=Et-hat(X_barK) with its continuous G_K action, and P_n E for the n-th Postnikov truncation. The homotopy fixed-point sets X(h_n K) are obtained from π_0 of the corresponding G_K homotopy fixed points, in the relevant profinite/relative étale model. Full homotopy gives X(hK). The homological versions apply the integral linearization of E and its truncations. An adelic tuple lies in X(A_K)^{h,n} exactly when its local images in the product of X(h_n K_v) arise by localization of a single global element of X(h_n K). Full and homological obstruction subsets are defined analogously. This is compatibility of local homotopy classes with a global class, not merely nonemptiness of a global homotopy fixed-point space.

The report gives descending towers and intersections, with X(A_K)^{h,n} contained in X(A_K)^{Zh,n}. Its §2.3 comparison theorem is explicitly for **smooth geometrically connected varieties over number fields**:

- full h = étale-Brauer-Manin = descent;
- full Zh = Brauer-Manin = connected descent;
- h,1 = finite-cover descent;
- Zh,1 = finite-abelian descent.

These equalities must not be transplanted wholesale to K=k(C). In the latter setting §6.2 compares the homological obstruction with a generalized pairing using H^3(X,Q/Z(2)), not the ordinary degree-2 Brauer group. Over number fields only the first two geometric homotopy groups contribute to the local-global obstruction; real places require the qualification explicitly noted in the report. Hence an ordinary number-field counterexample to sufficiency of étale Brauer-Manin, or separation of Brauer-Manin from finite descent, does not answer this question.

## Status evidence and limits

1. The 2023 report explicitly attributes progress to a larger Carlson–Corwin–Schlank work in progress; no construction or theorem proving strictness is supplied there.
2. A Lille mathematics seminar abstract dated **12 September 2024** announces a simply connected variety over a p-adic function field for which homotopy detects nonexistence of K-points but homological and Brauer-Manin obstructions do not. The date is recovered by combining its event page (12 September) with the archive's September 2024 heading. The abstract supplies no equation, proof, precise H_3 condition, or smooth/proper qualification. Therefore it supports an announced positive result, not a verified example in the smooth projective rational-surface subclass.
   - Event: https://math.univ-lille.fr/detail-event/obstruction-dhomotopie-etale-et-applications-david-corwin-universite-ben-gourion-du-neguev
   - Date archive: https://math.univ-lille.fr/agenda/seminaires/seminaire-arithmetique/archives
3. Corwin's publicly posted CV lists *Etale Homology and Homotopy Obstructions for Del Pezzo Surfaces over Qp(t)* with Magnus Carlson under ongoing/future research, rather than published papers or preprints: https://postdocisrael.com/wp-content/uploads/listing-uploads/cv/2023/03/CVDC.pdf . Its hosting path is not a reliable last-update date. Only the scholarly project/status is relevant; personal CV data are not for publication.
4. The author publication pages inspected did not identify a matching publicly inspectable manuscript: https://math.bgu.ac.il/~corwind/ and https://sites.google.com/view/tomer-schlank . The former visibly contains older material, so absence there is weak negative evidence.

Targeted exact-author, exact-title, p-adic-function-field, and Del Pezzo searches on 2026-10-21 did not recover a proof manuscript for the announced result. This is bounded search evidence, not proof of nonpublication. Arad–Carmeli–Schlank arithmetic spheres and Carlson–Schlank unramified inverse Galois applications in §5 concern different obstruction settings. Corwin–Schlank's open-cover refinement over number fields is likewise not a strict higher Postnikov obstruction on the same X. None is silently substituted for the requested example.

## Audit requirements for any future candidate

Require an exact K and valuation set, explicit X and geometric hypotheses, a demonstrably adelic tuple surviving h,2, and proof that it has no global homotopy lift compatible with all local classes. Explain its π_3 contribution and the homology comparison. If offering a proper smooth surface, verify that compactification and resolution preserve the actual witness and obstruction rather than merely replacing an affine example by a birational model. A claimed theorem with only seminar-level provenance remains an announcement until its argument is inspected.

## Retrieval and inspection

The published and earlier draft PDFs were downloaded and text-extracted. Printed page 2459 of the published report was rendered and visually inspected, confirming homology subscripts and the strict inclusion. A web screenshot attempt failed with a content-type error; local rendering succeeded. The seminar event and archive were inspected for announcement and date evidence. Only authored analysis and public bibliographic/verification metadata are included here; no source documents or extracted source text are redistributed.

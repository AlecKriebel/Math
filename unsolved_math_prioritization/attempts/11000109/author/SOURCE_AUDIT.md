# Source and convention audit

## Original question

The original item is Korkmaz’s Problem 2.4, printed p.87 of the author-hosted Farb volume (PDF page 94, one-based). Its conventions appear on printed p.85 (PDF page 92): orientation-preserving diffeomorphisms for an orientable surface, permutable punctures, boundary fixed when present. The absence of a boundary superscript here means no boundary. The question asks extension to an arbitrary ambient automorphism.

The catalog extraction runs onward into the discussion preceding Problem 2.5. That unrelated homomorphism discussion is not part of the target question. The original footnote only announces an inter-subgroup, non-inner result for an extended group; the footnote alone is insufficient for the exact target.

The exact requested UnsolvedMath URL was tried first with the web reader (unavailable) and subsequently through an ordinary HTTP read (403). No claim is made about the live page’s current status.

## Literature dependency map

- The construction is credited to Behrstock–Margalit, not merely inferred from their abstract. Section 4.2’s normal pure subgroup is the crucial same-domain/same-image ingredient.
- The proof packet uses their Theorem 6 only for the injectivity of conjugation into the sphere commensurator. Its torus automorphism-group remark is not a dependency.
- Bridson–Wade’s 2024 Section 6 was read online, including the proofs of Propositions 6.1 and 6.4. It independently makes the extended/pure/orientation-preserving conventions and branched-cover stabilizer identification explicit. The relevant geometric inputs remain cited results; this packet does not reconstruct all of Birman–Hilden theory or sphere rigidity.
- The 2006 journal bibliographic data for Behrstock–Margalit was verified through its arXiv record. The checked full PDF is the author-hosted May 9, 2005 version. The published journal PDF was not compared line by line.
- The current-literature search found the 2024 account and no contrary result relevant to the construction. This is a bounded literature check, not an exhaustive bibliographic survey.

## Central automorphisms: why the quotient proof matters

One must not silently identify all automorphisms of a direct product H×C₂ with inner automorphisms. If χ:H→C₂ is any homomorphism, then (h,z)↦(h,z+χ(h)) is an automorphism. In this case a nonzero χ is available by composing H→S₄ with permutation sign. Its square is the identity, and on a point (h,0) with χ(h)=1 it changes the central coordinate; inner automorphisms never do that. Thus the author proof deliberately uses the characteristic center quotient and works in the presence of such automorphisms. It neither needs nor endorses the stronger Aut=Inn interpretation of the old remark.

## Inspection limits and byte evidence

Two source PDFs were actually hashed from locally readable bytes: the existing Farb volume and the author-hosted Behrstock–Margalit PDF. Their exact byte counts and hashes appear in PUBLIC_REFERENCES.json. The Behrstock–Margalit arXiv PDF was read online only; no local PDF hash is claimed for it. Bridson–Wade was read as online arXiv HTML; no PDF hash is claimed. Neither source files nor extracted source text nor source screenshots are included in the author packet.

The mathematical locators were inspected as extracted/online text. Screenshot calls were attempted, but complete visible page-image inspection was not established; no claim of visual source QA is made. All source statements used in the proof have legible text and formulas in the inspected representations.

The proof is symbolic, not computational. There is no numerical experiment, finite search, code-generated theorem, or execution-based substitute for the cited topological theorems and the written argument.

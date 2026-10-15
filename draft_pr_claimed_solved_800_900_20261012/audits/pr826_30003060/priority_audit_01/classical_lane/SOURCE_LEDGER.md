# Primary-source ledger — classical mechanism

Audit date: 2026-10-15 UTC. The successful PDF bytes are preserved only in ignored `private_sources/`. SHA-256 pins below identify the exact inspected downloads; they are not archival guarantees about future server bytes. Text extraction used local `pdftotext -layout`. Selected mathematical anchors were also visually inspected. An inspected section is not a claim that every page in that work was read.

## C0 — Frozen candidate

- File: `../../source/author/PROOF.md` relative to this lane.
- Supplied frozen PR head: `286cc67c0727b4decfd4f261a0591cd8823ebce9`.
- SHA-256 of candidate text inspected: `59efb88c21c7e62fd70fa06f7f5a0b59bc96672c70523bc5a1330b094c0a2bb3`.
- Read in full. It claims only the literal unrestricted-field counterexample and explicitly disclaims first priority and a characteristic-zero resolution.

## C1 — Loday–Quillen (1984): the exact classical small complex

Jean-Louis Loday and Daniel Quillen, *Cyclic homology and the Lie algebra homology of matrices*, Commentarii Mathematici Helvetici **59** (1984), 565–591, [DOI 10.1007/BF02566367](https://doi.org/10.1007/BF02566367).

- [Inspected PDF](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/loday-quillen.pdf).
- SHA-256: `404d7e549a4fe2a81114af8abe711cf7a213654530906d00c6551691786c0d38`; 1,066,313 bytes, 27 PDF pages.
- Read introduction ground-ring conditions and §5, printed pp. 581–583 (PDF pages 17–19, one based). Visually inspected printed p. 582.
- Lemma 5.1 is the tensor-algebra bimodule exact sequence. Its specialization after tensoring yields `A⊗V --b→ A` with `b(a⊗v)=av−va`.
- Lemma 5.2 states HH0 as cyclic coinvariants, HH1 as cyclic invariants, and HHj=0 for j≥2. The cyclic rotation here is explicitly unsigned. Over a field with V a vector space, the required flatness/projectivity assumptions hold. This includes every field of characteristic p and the candidate's finite-dimensional V.
- Lemma 5.3 states B: HH0→HH1 is the length-n cyclic norm `1+rho+...+rho^(n−1)`. Proposition 5.4 computes reduced cyclic homology using cyclic-group homology. These are **B/cyclic** assertions, not assertions about Euler-cap homology.
- Priority consequence: the entire ordinary homology model and norm distinction predate BLS by three decades. The paper has no higher-Koszul terminology, which was introduced later.

## C2 — Goodwillie (1985): the exact cap operator and Cartan identity

Thomas G. Goodwillie, *Cyclic homology, derivations, and the free loopspace*, Topology **24** (1985), 187–215, [DOI 10.1016/0040-9383(85)90055-2](https://doi.org/10.1016/0040-9383(85)90055-2).

- [Inspected PDF](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/goodwillie-free.pdf).
- SHA-256: `46db621af0235a7d1278851ddb21f350b19072366a3136b12ce8cccd94d5dbd5`; 1,366,214 bytes, 29 PDF pages.
- Read §II.4, especially printed pp. 193–196 (PDF pages 7–10), and the statements needed in §III.4. Visually inspected printed p. 194.
- Ground ring K is commutative; A is flat, associative, unital, and D is a K-derivation. Theorem II.4.2 supplies e_D and E_D with `[e_D,b]=0` and `[e_D,B]+[E_D,b]=L_D` (odd graded commutators are sums). Formula II.4.8 on **printed p. 194** is `e_D(a0,...,aq)=(-1)^(q+1)((D aq)a0,a1,...,a(q−1))`.
- Thus in homology `e_DB+Be_D=L_D`. For the weight derivation D this is total-weight multiplication. On degree-one small chains with generator v it gives `e_D(a⊗v)=va`, the same class as av in HH0.
- The theorem and formula require no characteristic-zero assumption. Characteristic-zero hypotheses enter the later division-by-weight deductions. This is exactly the distinction needed for the candidate.

## C3 — Loday, second edition (1998): assembled textbook presentation

Jean-Louis Loday, *Cyclic Homology*, second edition, Grundlehren 301, Springer, 1998, [book DOI](https://doi.org/10.1007/978-3-662-11389-9).

- [Inspected PDF mirror](https://www.math.univ-paris13.fr/~vallette/GdT/Cyclic%20Homology%20-%20Loday.pdf).
- SHA-256: `9161a46e6a59753156137364d4926ca66085bc6d9c1375d9b86179868d810eea`; 20,583,505 bytes. Title/copyright pages identify this as the **1998 second edition**; it must not be mislabeled as the 1992 first edition.
- Read §§3.1.1–3.1.8, printed pp. 90–93 (PDF pages 105–108), and §§4.1.4–4.1.13, printed pp. 117–120 (PDF pages 132–135); also relevant chapter bibliographical comments.
- Proposition 3.1.2 gives an explicit small-to-bar homotopy equivalence, Theorem 3.1.4 gives unsigned invariants/coinvariants, and Proposition 3.1.5 gives the cyclic derivative/norm model. Formula 4.1.7 reproduces the cap operator; Corollary 4.1.9 gives `[e_D,B]=L_D` on HH. This supplies a single pre-2015 reference for both classical ingredients.
- Bibliographical comments credit the tensor-algebra cyclic computation to Loday–Quillen and trace the derivation formulas to Rinehart/Goodwillie. This lane relies on the original Goodwillie text for the exact operator, not on bibliographical attribution alone.

## C4 — BLS, arXiv v1 (2015): the needed named-invariant bridge

Roland Berger, Thierry Lambre, Andrea Solotar, *Koszul Calculus*, [arXiv:1512.00183v1](https://arxiv.org/abs/1512.00183v1), submitted 1 December 2015.

- [Inspected v1 PDF](https://arxiv.org/pdf/1512.00183v1).
- SHA-256: `3b0db72d14afe5d94ab03890313ab6c0533f98e9c30e4dbe4c33d9697c21ab01`; 510,330 bytes, 49 pages.
- Read introduction, definitions in §2, §§5.1–5.2 (printed/PDF pp. 19–20), §§6.1–6.3 (pp. 22–27), and tensor-algebra passage/Proposition 7.4 (pp. 28–30). Visually inspected p. 20.
- §5.1 identifies Hochschild derivation cap with the Rinehart–Goodwillie operator and the higher comparison for Koszul algebras. §5.2 defines the fundamental-cocycle higher differential in every characteristic. At chain degree one its class is av=va modulo commutators. This handles characteristic two directly, without relying on the char≠2 hypothesis used for a general derivation's square.
- Theorem 6.4 on p. 24 explicitly assumes char(k)=0. The discussion asks about removing that condition; Conjecture 6.5 is stated without repeating a field restriction. This is context, not evidence of any unique historical intention.
- Proposition 7.4 on p. 29 concerns higher **cohomology** of T(V). It is not the identical positive-characteristic higher-**homology** counterexample. The preceding passage explicitly knows that T(V) is Koszul of global dimension one.

## C5 — BLS, arXiv v3 (2017): the candidate's cited version

- [Inspected v3 PDF](https://arxiv.org/pdf/1512.00183v3), version dated 20 June 2017. The [arXiv history](https://arxiv.org/abs/1512.00183) records v1 2015-12-01, v2 2016-12-20, v3 2017-06-20. Published in Glasgow Mathematical Journal **60** (2018), 361–399, [DOI](https://doi.org/10.1017/S0017089517000167).
- SHA-256: `52415560de2a088a334b1c9ee0f613a144e552b3298d17e97c3100bb6731bd06`; 451,372 bytes, 40 pages.
- Read §§5.1–5.4 and §§6.1–6.3, printed/PDF pp. 17–23; relevant introductory and references passages.
- The needed bridge is on pp. 17–18; Theorem 6.4 and Conjecture 6.5 are on p. 21. The content relevant to the deduction is already in v1. No identical full free-algebra orbit classification or positive-characteristic higher-homology counterexample was identified in these inspected passages.

## C6 — Solotar's Oberwolfach contribution (2016): exact question

Andrea Solotar (joint work with Roland Berger, Thierry Lambre), *Koszul Calculus*, within *Hochschild Cohomology in Algebra, Geometry, and Topology*, Oberwolfach Reports **13** (2016), 449–506, contribution pp. 479–481, [DOI 10.4171/OWR/2016/10](https://doi.org/10.4171/OWR/2016/10).

- [Publisher landing page](https://ems.press/journals/owr/articles/14218); [inspected repository PDF](https://oa.tib.eu/renate/bitstreams/d442c57f-9ccf-4c6a-92d9-b036a56ab18c/download).
- SHA-256: `9db663b0200a4c336d34100634e5e82db98f02e5316c2e89eda190fbf25669d9`; 494,910 bytes, 58 pages.
- Read contribution pp. 479–481 (PDF pages 31–33). Page 481 identifies the Koszul analogue of Rinehart–Goodwillie as fundamental-cocycle left cap, then states the Koszul iff positive higher-homology vanishing conjecture. No field restriction is stated in that contribution. This lane audits the literal unrestricted statement, not the characteristic-zero converse.

## C7 — Hesselholt (1997): broader circular-word mechanism, different invariant

Lars Hesselholt, *Witt vectors of non-commutative rings and topological cyclic homology*, Acta Mathematica **178** (1997), 109–141, [inspected PDF](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/hesselholt97.pdf).

- SHA-256: `4584ea6da2d2ce312a30bfb43e40c935fb1e9522ffabc21dcef9f972e74dd68d`; 1,334,876 bytes, 33 pages.
- Read introduction, §1.2–1.3 selected passages on circular words, printed pp. 111–114, and §3.1 selected free-algebra decomposition, pp. 130–132; inspected statements in §3.3, pp. 136–138. Searched extracted text for Euler, Koszul, and derivation (no matching higher-Koszul assertion).
- It explicitly organizes free noncommutative integral polynomials by circular words and obtains orbit-cardinality factors modulo commutators (p. 113), and computes THH/TC of free algebras via circular-word decompositions. This reinforces that necklace arithmetic is old. It does **not**, in the inspected material, identify its differential with the candidate's Euler cap or state the identical higher-Koszul obstruction. TC/THH/de Rham–Witt operators cannot be substituted for Euler cap merely because both calculations use circular words.

## Failed or limited retrievals

- Rochester `people.math.../loday-book.pdf`: local request timed out; browser open returned internal error. Successful alternate 1998 PDF is C3.
- Rochester `people.math.../goodwillie-free.pdf`: local timeout/browser unavailable. Successful `sas.rochester.edu` mirror is C2.
- Rinehart, *Differential forms on general commutative algebras*, Trans. AMS **108** (1963), 195–222: AMS original PDF [attempted URL](https://www.ams.org/tran/1963-108-02/S0002-9947-1963-0154906-3/S0002-9947-1963-0154906-3.pdf) returned HTTP 403; browser internal error. No direct inspection or exact original attribution is claimed. Goodwillie original suffices for this lane's operator deduction.
- EuDML Loday–Quillen landing page failed in browser; the original-page PDF and publisher DOI page were accessible.
- Search snippets/aggregators and secondary hits were used only to find primary texts, not as proof or historical-priority evidence.

# Arithmetic and logic follow-on scan

2026-10-06, America/Los_Angeles. Scope: families 001–031 and 240–245; read first-batch exclusions, selected exact source theorem/consequence statements, and primary literature. This is a conditional research-path audit, not a validation of source proofs. No external people contacted; source clone read only. Completion estimate for this bounded scan: 95%; exact novelty still requires broader priority searches before publication.

## 1. Rational-point undecidability for smooth projective geometrically integral varieties

**Recommend. Impact 8.1, transfer confidence very high, novelty of independent method low.**

Exact target: no algorithm decides X(Q)≠∅ from equations for a smooth projective geometrically integral Q-variety X, with dimension, embedding degree and coefficient height unrestricted. Stronger package: the promise decision problem has Turing degree 0′; no total computable bound on the smallest projective height of a rational point for all such nonempty X; no effectively enumerable complete certificate system for all empty such X.

Input #004, `preprints/Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026/build/sections/01-introduction.tex`, theorem `thm:main`, states no algorithm decides rational solvability of an integer polynomial with variable number of variables. Its `07-consequences.tex`, corollary `thm:degree-normal-form`, already proves degree 0′ and quartic/sums-of-squares restricted inputs. Those normal forms are NOT new targets.

Bridge: Bjorn Poonen, *Existence of rational points on smooth projective varieties*, JEMS 11 (2009) 529–543, Theorem 1.1(i), says an algorithm for regular projective geometrically integral varieties over a fixed number field gives an algorithm for arbitrary varieties. Characteristic zero identifies regular and smooth. https://math.mit.edu/~poonen/papers/chatelet.pdf ; https://ems.press/journals/jems/articles/1924 ; https://arxiv.org/abs/0712.1782 . Thus apply contraposition at k=Q. Poonen's construction uses a family of Châtelet surfaces; ordinary homogenization or resolution alone is NOT sufficient because it can create rational points at infinity. The algorithmic transfer relativizes to show 0′ hardness; rational-point enumeration gives the opposite reduction. Height/certificate consequences use elementary bounded search and dovetailing.

Remaining work: reproduce Poonen's reduction in precise effective presentation, match promise conventions, write a short theorem-chain with optional explicit finite package demonstrating the construction. No central new geometric theorem needed.

Boundaries: not fixed dimension, curves, surfaces, Fano/rationally connected or general-type varieties; do not assert undecidability under a finite rational-point promise. H10(Q) does NOT itself give a Diophantine definition of Z or refute Mazur. Do not claim many-one completeness from the source's Turing completeness.

Duplication check: source #004 consequences contain only degree and polynomial normal forms; whole-corpus searches for smooth-projective-undecidability and Poonen geometric reduction found no target statement. Poonen2009 in #004 bibliography is instead definability of Z in Q. First batch listed this path only as unused reserve, not one of ten researcher prompts.

## 2. Integral density for PGL_r character varieties, all central-obstruction sectors

**Recommend. Impact 7.7, transfer confidence high; short construction needed.**

Exact target: every character variety of PGL_r representations of a smooth connected complex algebraic curve, r≥3, has potentially Zariski-dense full-ring integral points in every component, including every obstruction class for lifting projective representations on a closed curve. Relative version permits prescribed quasi-unipotent projective boundary conjugacy classes, retaining the source's ambient-integrality convention. Bundle GL_r and intermediate type-A central quotients if checks work; do not expand to every reductive group.

Input #027, `preprints/Integral-points-on-character-varieties-of-curves-September-25-2026/build/sections/introduction.tex`, lines 34–59, theorem `thm:main`: density in every component for SL_r exact quasi-unipotent boundary conjugacy classes, including nonsimple Jordan classes, over one finite field extension and full ring of integers. Importantly this is ambient integrality; it need not stay in the same Jordan stratum modulo every prime. Source builds actual integral representations before taking characters (lines 64–70).

Mechanism for projective curves: puncture the genus-g curve once. Choose lifts A_i,B_i∈SL_r(C) of each PGL_r generator. Then ∏[A_i,B_i]=ζI for ζ∈μ_r. For each of finitely many ζ, use #027 with the added boundary scalar ζI (or inverse according to relation convention). Projectivization kills that boundary, produces a representation of the closed surface, and maps onto the corresponding lift-obstruction sector. The central quotient SL_r→PGL_r is defined over Z; it maps integral representations to integral representations. Image of a dense set under a dominant morphism is dense. A finite compositum covers all sectors with one number field.

For punctured curves, the group is free, so lifts exist; each prescribed projective quasi-unipotent class has finitely many SL_r lift classes, each still quasi-unipotent. Determinants and their roots can be handled for GL_r via a character torus and a finite scalar-twist map; choose a number field with a nontorsion unit so units are Zariski-dense in G_m. Check all boundary-product constraints explicitly.

Remaining work: construct morphisms at representation/character-scheme level over cyclotomic integers, prove coverage sector by sector, ensure semisimplification/closed orbit compatibility, then transfer the exact ambient-integral statement. This is materially clearer than a generic 'extend to other groups.'

Primary historical source: Coccia–Litt, *Density of integral points in the Betti moduli of quasi-projective varieties*, https://arxiv.org/abs/2507.00167 , Conjecture 1.1.1 for Chevalley groups; rank-two SL2/PGL2 cases already known and should be excluded from novelty. Source #027 intro lines 96–108 expressly limits its new theorem to SL_r and cites existing PGL2 density. Whole-corpus PGL/character-variety search did not find the all-rank PGL conclusion.

## 3. Unique Diophantine solutions exceed every computable height bound

**Lower-priority fallback. Impact 6.7–7.1, transfer confidence very high; strongest as short attributed consequence note.**

Exact named target: refute Tyszka's computable height-bound conjecture for elementary positive-integer systems B_n={x_i x_j=x_k, x_i+1=x_k}. Let ξ(n) be the largest coordinate needed among uniquely solvable subsystems of B_n. Show ξ eventually dominates every total computable function, hence no computable height bound exists even for exactly-one-positive-solution systems. Bundle undecidability of solvability over Z under the promise of finitely many integer solutions.

Input #242, `preprints/Single-fold-Diophantine-representations-September-24-2026/build/main.tex`, theorem `thm:main`, gives a single-fold polynomial representation over N of every recursively enumerable relation. Its `consequences.tex` already proves undecidability under at-most-one N-solution with existentially fixed degree/number of variables. Do not relabel that as new.

Bridge: Tyszka, *Is there a computable upper bound for the height of a solution of a Diophantine equation with a unique solution in positive integers?*, Open Computer Science (2017), primary full text https://arxiv.org/html/1404.5975v18 (also https://arxiv.org/abs/1404.5975 ). Theorem 5 says any single-fold representable function is eventually strictly below ξ; Lemma 4 preserves exact solution counts while converting positive polynomial equations to B_n. Apply source #242 to the graph of every total computable function. Conjectures 1 and 2 proposed a specific computable bound; Observation 3 addresses arbitrary computable bounds. Unique-N and unique-positive domains correspond by a shift of variables. For integer finite-solution promise, replace each N variable by a sum of four squares: each nonnegative witness has finitely many representations, so there are finitely many Z-witnesses, although uniqueness is lost.

Remaining work: translate conventions carefully and either reproduce the short published transfer or give a uniform compiler. Never claim a numerical small counterexample without constructing it; the source does not supply explicit coefficients for its universal representing polynomial. This route's theoretical novelty is low because Tyszka explicitly documented incompatibility with single-fold representations; therefore rank behind the two above and substantive other-field candidates.

Duplication: source #242 consequence section has no computable-height or Tyszka conclusion; full-corpus searches found no Tyszka or matching unique-height theorem.

## Rejected / already included paths

- #032 CM Hodge ⇒ Tate for all finite-field abelian varieties, Hodge standard conjecture, and generalized Hodge for CM abelian varieties: **already explicitly in release** `The-rational-Hodge-conjecture-for-CM-abelian-varieties-September-30-2026/build/sections/07-consequences.tex` (`cc:tate`, `cc:ghc`, Hodge standard corollary). Do not promote as new.
- #008 ⇒ H0 of Kontsevich's graph complex freely generated in odd weights: **already explicit** in source introduction lines 120–127. Rebranding as formality torsor classification has too little independent content.
- #022 ⇒ Hausdorff-measure divergence via mass transference: **already source introduction cor:hausdorff and consequences.tex**.
- #030 modularity ⇒ full asymptotic Fermat over imaginary quadratic fields: not cleared. Published modular-method results can still require residual Serre modularity, torsion lifts, Eichler–Shimura/fake elliptic curves, level lowering and field-specific S-unit conditions. Do not imply modularity alone removes all gates.
- #030 ⇒ BSD over imaginary quadratic fields: Loeffler–Zerbes 2021 additionally require eigenvariety smoothness/technical hypotheses. Not an unconditional full-BSD follow-on.
- #241 rigidity ⇒ first-order definability of every degree/biinterpretability: unjustified; rigidity alone is much weaker.
- #019 local section conjecture ⇒ full global section conjecture: still needs a local-global principle; blocked absent a new mechanism.
- #003 quasi-RH ⇒ full Artin density: Hooley needs zero control for Kummer/Dedekind extensions, not just Dirichlet L-functions.

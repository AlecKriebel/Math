# Ordinary Banach–Mazur rigidity of von Neumann algebras

For each von Neumann algebra, a sufficiently small ordinary Banach–Mazur distance fixes its Jordan structure. Read the full paper and sources.

## Original abstract

Using OpenAI's all-algebra bounded Hochschild vanishing theorem, we derive local ordinary complex Banach–Mazur rigidity for every von Neumann algebra and its canonical predual. The threshold depends on the algebra; the conclusion is Jordan *-isomorphism. Roydor announced the general cohomological implication in 2020, while his published Theorem 1.2 assumes separable predual. We give an explicit extension of his geometric argument using deformation stability on two fixed source algebras and reconstruction of odd finite type-I summands from full abelian projections. This avoids separability, moving-corner perturbation constants, and enumeration of infinite cardinal degrees. The cohomological input and geometric machinery are attributed external results; no new solution of the underlying cohomology problem or universal numerical threshold is claimed.

## The idea in plain English

A von Neumann algebra carries both a norm and a multiplication. Banach–Mazur distance measures how closely two spaces can match through an invertible linear map, using only their norms. The question is whether a sufficiently close match also determines their algebraic structure.

For each fixed complex von Neumann algebra, this paper obtains a neighborhood in which every other von Neumann algebra has the same Jordan structure. The size of that neighborhood may depend on the fixed algebra. The same conclusion holds when the comparison uses the canonical preduals.

## The precise result

For every complex von Neumann algebra M, there exists ε_M>0 such that, for every complex von Neumann algebra N, either d_BM(M,N)<1+ε_M or d_BM(M_*,N_*)<1+ε_M implies that M and N are Jordan *-isomorphic. Here M_* and N_* are the canonical preduals, and ordinary complex Banach–Mazur distance is the infimum of ||T||·||T⁻¹|| over bounded invertible complex-linear maps T between the spaces.

At this threshold, the two strict distance conditions are equivalent to Jordan *-isomorphism, to a surjective complex-linear isometry between the algebra spaces, and to one between the canonical preduals. The statement includes arbitrary nonseparable centers and preduals, every von Neumann type and every infinite type-I cardinal dimension.

A Jordan *-isomorphism preserves adjoints and the symmetrized product x∘y=(xy+yx)/2. It need not preserve the orientation of the associative product: an algebra and its opposite have the same relevant norm geometry.

## Why the result holds

The essential input is OpenAI’s bounded Hochschild vanishing theorem for all complex von Neumann algebras. In the ordinary bounded, actual-coboundary sense, its degree-two and degree-three cases provide the estimates needed to correct a small multiplication defect on a fixed source algebra.

The proof extends Roydor’s geometric argument using two fixed source algebras. It handles the part whose unit splits into two equivalent projections, then reconstructs the remaining finite odd type-I degrees using full abelian projections. This treats unbounded finite odd degrees together and avoids constants attached to moving corners. Infinite cardinal dimensions are already included in the first part.

Taking Banach adjoints preserves the norms of a predual isomorphism and its inverse, giving the predual implication. The resulting exact Jordan isomorphism is normal and induces an isometry of the canonical preduals.

## Scope and limits

The threshold depends on M; the paper gives no universal numerical constant. The comparison spaces must be complex von Neumann algebras or their canonical preduals. The initial near-isometry is measured in ordinary operator norm and need not be normal or completely bounded.

The conclusion is Jordan structure, not recovery of a chosen associative orientation or a claim that the original near-isometry is multiplicative. The inequalities are strict; no threshold-equality result or theorem for arbitrary Banach target spaces is asserted.

The result uses the attributed cohomology theorem and classical geometric machinery. Roydor had already announced the unrestricted conditional formulation; this note supplies an explicit fixed-source extension and records its consequence from the cohomology input. No first-discovery claim is made.

## Status and AI use

Unrefereed preprint.

AI tools were used extensively in the research, proof development, checks and writing. AI-agent checks are not human peer review. This is an unrefereed preprint, without formal proof-assistant certification. Alec Kriebel is responsible for the work.

Manuscript and declared publication date: 7 October 2026. The deposit supplies no version number.

## Read the paper

Read the complete seven-page deposited paper in the on-page PDF reader.

## Background and prior work

- [OpenAI (2026), Vanishing of higher bounded Hochschild cohomology](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026/paper.pdf): Theorem 1.1 is the essential all-algebra ordinary bounded cohomology input. The pinned manuscript is dated 23 September 2026. The present paper derives a consequence; it does not claim a new solution of that cohomology problem.

- [Jean Roydor (2020 online; 2022 issue), Banach–Mazur stability of von Neumann algebras](https://doi.org/10.1142/S1793525321500151): Provides the geometric approach and a conditional ordinary-distance theorem with separable predual. The current note extends the fixed-source argument beyond that hypothesis.

- [Jean Roydor (2020), CIRM lecture slides](https://www.cirm-math.fr/RepOrga/2169/Slides/Roydor_Slides.pdf): Theorem 2 on PDF pages 28–29 already announces the unrestricted conditional formulation. That earlier announcement receives explicit credit.

- [Éric Ricard and Jean Roydor (2014), A non-commutative Amir–Cambern theorem for von Neumann algebras and nuclear C*-algebras](https://doi.org/10.1016/j.jfa.2014.05.018): Their unconditional theorem uses completely bounded distance. Its predual observation and conditional two-matrix-level result are prior work; small ordinary distance does not by itself supply their stronger metric hypothesis.

- [Iain Raeburn and Joseph L. Taylor (1977), Hochschild cohomology and perturbations of Banach algebras](https://doi.org/10.1016/0022-1236(77)90072-6): Together with Johnson’s classical perturbation theory, this is prior work on the fixed-algebra deformation mechanism. The note writes out the involution-preserving iteration and its algebra-dependent constants.

- [David Sherman, Noncommutative Lp structure encodes exactly Jordan structure](https://arxiv.org/abs/math/0309365v2): Gives the exact isometry–Jordan structure connection, including the algebra and predual endpoints used here.

## Collaboration

Independent proof checks, counterexamples and precise comparisons with prior work are welcome. Further work toward a journal paper would require substantive research contributions; authorship and acknowledgments would reflect actual contributions and mutual agreement.

## Licensing

CC BY 4.0 for original manuscript, prose and verification code

Unchanged OpenAI family-295 material in the complete source archive retains Apache License 2.0, its original OpenAI attribution, LICENSE and manuscript-specific README citation. CC BY 4.0 does not relicense it. Other linked literature retains its own terms.

## Citation

@misc{Kriebel2026OrdinaryBanachMazurRigidity,
  author = {Kriebel, Alec},
  title = {Ordinary Banach--Mazur rigidity of von Neumann algebras},
  year = {2026},
  month = {oct},
  day = {7},
  date = {2026-10-07},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23217863},
  url = {https://zenodo.org/records/23217863},
  note = {Unrefereed preprint; no version number supplied},
  orcid = {0009-0001-9320-500X}
}

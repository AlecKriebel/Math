# Independent adversarial review: tangent-bundle Seshadri constants

**Reviewed work:** Zenodo 23331395, *Positive tangent-bundle Seshadri constants characterize projective space*, version 1.0, 12 October 2026.

**Verdict:** no substantive defect found within this independent review's scope. The claimed argument passes the specific adversarial checks below. This is AI-assisted mathematical review, not human peer review or a formal proof certificate.

## Source binding and independence

Read the complete five-page published PDF text and its `paper.tex`. Did not consult the archived mathematical verdicts/reports, historical candidate conclusions, or another current reviewer's conclusions before reaching this assessment. The archived source package's integrity check was run in `--integrity-only` mode; it verifies bytes, not mathematics.

- PDF SHA-256: `f3e5619c7e1560c45f7793b0f7e4dabfbbf66d08f568f3478b5bb8f35779ea17`.
- Source archive SHA-256: `22bcb3d40fd734a6ee6e416319f329739395dcc66417da5f27e82d32a85694cf`.
- `paper.tex` SHA-256: `fe385adc3db169e6eeacce965c337aaf5f7a185491944ca096c0709bbcb785b6`.

The exact claim is for a **smooth integral projective variety over an algebraically closed field**, in **arbitrary characteristic**, with the Fulger–Murayama relative tangent-bundle Seshadri constant positive at **one specified closed point**. It is not a claim about arbitrary tangent positivity notions, singular varieties, an unspecified general point, or ordinary slopes of arbitrary positive-characteristic vector bundles.

## Adversarial mathematical assessment

### 1. The specified point and the first rational curve

The first possible failure would be replacing the specified point x by a general point or using uniruledness alone to obtain a rational curve through x. The manuscript does neither. The original Fulger–Murayama proof explicitly constructs a rational curve through the very point satisfying positivity. I inspected that proof in the authors' [arXiv manuscript](https://arxiv.org/pdf/1903.00610), Corollary 5.6; the published version renumbers this as Corollary 4.6. The separate Fano characterization is Proposition 5.8(1) there, corresponding to published Proposition 4.8(1), and has no characteristic-zero restriction. The characteristic-zero/general-point restriction belongs only to its other clause.

The final-numbering NSF URL returned HTTP 502 on this review's attempts, and direct publisher opening returned HTTP 403. The primary arXiv PDF was successfully inspected, including definitions and the actual proofs of both imported statements; the numbering difference is recorded rather than concealed. Their matching final-numbered statements were also visible in the search index. No search snippet was used to supply missing mathematical content.

### 2. Positivity along normalized rational images

Each quotient summand of the pullback to the normalization yields a genuine curve upstairs in the quotient projective bundle. Its function field is sandwiched between the identical function fields of the normalization and the rational image. Thus its generic degree is one, even when the image is singular or the characteristic is positive. The numerator is the summand's degree, and the denominator is the original curve's multiplicity at x. Positive Seshadri constant therefore forces every integer splitting degree to be at least one.

This argument does not require the normalization to be an immersion at x, or replace Frobenius-asymptotic slopes on higher-genus curves by ordinary slopes. A normalization's differential is nonzero generically because it is birational onto a curve over an algebraically closed, hence perfect, field. Possible ramification at special points does not affect the infinitesimal-automorphism argument later.

### 3. The absolute minimum and stable-map boundary

The minimum is over **all** rational images through x, rather than over very-free curves, one chosen Hom component, or curves through a moving general point. That quantifier is essential: a minimum restricted to very-free curves could degenerate into smaller rational curves outside the restricted collection.

The minimum survives algebraically closed extensions without requiring an unproved base-change identity for the Seshadri constant. A lower-degree normalization over an extension gives a point of a finite-type pointed Hom scheme; nonemptiness over an extension gives a closed point over algebraically closed k. Its image remains rational by Lüroth, including inseparable parametrizations, and has degree at most the map's degree. This is a valid contradiction to the original absolute minimum.

For a genus-zero stable map of the minimum degree, start at the mark and traverse constant components until reaching the first nonconstant component. Its image contains x. The sum of positive integer contributions to A-degree, with **full generic degrees including inseparable degree**, forces this component to be the sole nonconstant component and to map birationally. A contracted subtree attaches to it once; with at most one marking, its total special-point incidences are at most 2t, while stability requires at least 3t. Consequently there is no ghost boundary. The proof covers a mark initially placed on a ghost component and does not silently discard inseparable multiple covers.

### 4. An actual projective marked family, not only coarse points

I inspected [Abramovich–Oort, Theorem 2.8 and §2.5](https://arxiv.org/pdf/math/9808074). It supplies the proper finite-presentation Artin stack and projective coarse scheme for stable maps to a projective target over the allowed fields; it is not restricted to tame or characteristic-zero stable maps.

The manuscript uses the actual evaluation fiber in the stack. Its objects have smooth domains and birational maps, so geometric automorphisms are identity. The tangent space to the stabilizer is also zero: a vector field killed by the generically injective differential vanishes generically and hence everywhere. A finite group scheme with only the identity geometric point and zero tangent space is trivial. This also descends to nonreduced bases: the augmentation-split finite algebra has an augmentation ideal with zero geometric fibers, and Nakayama kills that finite module. No reducedness assumption is smuggled into this step.

The remaining stack/space/scheme passage matches the cited Stacks statements. [04SZ](https://stacks.math.columbia.edu/tag/04SZ) turns trivial inertia into an algebraic space. The map to the coarse scheme is proper and quasi-finite, since each geometric fiber has at most one isomorphism class. [03XX](https://stacks.math.columbia.edu/tag/03XX) makes it a scheme, and [02LS](https://stacks.math.columbia.edu/tag/02LS) makes the morphism finite. It is therefore projective. This avoids assuming that formation of coarse moduli commutes with a closed evaluation fiber in wild characteristic.

The universal curve now belongs to the actual moduli scheme and carries an actual marking section. A degree-one line bundle from that section identifies the smooth P1-family with a rank-two projective bundle. The use of cohomology and base change here applies over nonreduced bases: the line bundle has constant fiber cohomology, and the morphism induced by evaluation is an isomorphism on each fiber. The stated finite-morphism/Nakayama/flatness argument completes the identification.

### 5. Surjectivity in arbitrary characteristic

For the chosen minimum-degree normalization, all splitting degrees are at least one. Both H1 groups with one and two fixed source points therefore vanish. Fixed-source deformation theory gives smoothness of the pointed Hom space and of evaluation at the second point; this is a direct obstruction calculation, not an appeal to generic smoothness in characteristic zero. [Gounelas, Proposition 4.7](https://ems.press/content/serial-article-files/26314?nt=1) is a compatible primary reference, but the manuscript itself supplies the needed fixed-point obstruction reasoning.

The pointed parametrization torsor has smooth group Aut(P1,0), since the projective-line bundle with section is locally pointed-trivial. Smoothness descends to the moduli point, which therefore lies on a unique reduced irreducible component. Evaluation from the associated universal family has image containing an open subset of X; properness makes that image closed, and irreducibility gives surjectivity. The argument does not require every point of this component to be a smooth moduli point. Nor does it require applying the original positivity assumption over every residue-field extension: very-freeness of the original chosen member is enough to establish the open image.

### 6. The contracted section tests every curve

The numerical-generation step is stronger than merely showing all family members have one class. For each divisor D, the constructed line bundle L has fiberwise trivial pullback to the universal P1-bundle. [0B91](https://stacks.math.columbia.edu/tag/0B91) supplies proper flat perfect base change. Its degree-zero cohomology is a line bundle, and adjunction is fiberwise an isomorphism. The alternative [0EX7](https://stacks.math.columbia.edu/tag/0EX7) does require a reduced base; the chosen H is integral and thus satisfies that requirement. [0GKA](https://stacks.math.columbia.edu/tag/0GKA) supplies the required universal structure-sheaf pushforward property.

The marking section is genuinely contracted to x, so this descended line bundle on H is trivial. Hence e*L is trivial. For any integral curve Γ of X, including curves avoiding x and curves of positive genus, a closed point in the nonempty generic fiber of e yields a proper curve dominating Γ with finite positive **total** degree. The degree projection formula then forces L·Γ=0. Integer degrees ensure that a degree divisible by the characteristic does not invalidate the argument. This establishes the relation in N1-dual divisor space for every Cartier divisor and gives Picard number exactly one, not merely an upper bound on the classes of rational curves through x.

### 7. Fano reduction and imported characterization

The anticanonical degree on the original very-free curve is positive. Numerical generation therefore gives −K numerically equal to a positive rational multiple of the chosen ample line bundle. The argument tests top intersections on every positive-dimensional integral subvariety, not merely positivity on every curve. Smoothness makes −K Cartier. [Fujino–Miyamoto, Theorem 1.3](https://www.math.kyoto-u.ac.jp/~fujino/Nakai-Moishezon3.pdf) is explicitly valid over algebraically closed fields of any characteristic and justifies the ampleness step.

Only after Fano ampleness is proved does the manuscript apply the established Fulger–Murayama Fano clause. This is an explicit classification dependency, not a disguised assumption of the conjecture being proved. The underlying full Kollár/Mori classification proof was not independently re-proved in this review. The dimension-one endpoint is separately correct: degree TX=2−2g, so positivity gives P1. No extension to singular varieties has been inferred.

## Independent controls and limits

`independent_controls.py` was written without importing archived controls. It checks 873,611 labelled-tree/root/mark cases through seven vertices: no tree with exactly one nonconstant component and one mark can have stable contracted components. A two-mark ghost leaf is a negative control demonstrating why the one-mark hypothesis matters. It also checks 51,500 integer degree cases including inseparable multiplicities, and 200 P1 splitting/cohomology cases. All pass. These are finite interfaces to the written argument, not a substitute for its geometric proof.

As conceptual controls, on P1×P1 the restriction to a ruling has an O(0) quotient, so the positivity hypothesis fails and pointed ruling evaluation need not dominate the surface. On projective space the minimum family of lines through x is proper with a contracted marking section, consistent with the argument. A single very-free curve on a rationally connected variety alone would not supply the absolute-minimum hypothesis; the proof correctly uses positivity along every rational image through x.

The package integrity check passed for all 78 files. It was not described as a mathematical validation, and archived audit verdicts were not consumed. No published files were changed.

**Disposition:** no substantive defect to defer was identified. This supports publication review of the exact preprint subject to synthesis with the independent analytic/literature review. It does not prove historical priority, journal acceptability, or freedom from every possible error. The principal external dependencies are the established same-point rational-curve existence and Fano characterization, proper stable-map moduli, deformation theory, cohomology/base change, and Nakai–Moishezon; their active hypotheses match the manuscript as inspected.

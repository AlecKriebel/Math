# Exact source, assumptions and prior work

Checked 2026-09-30. The geometric equality is already established. The question is specifically about a combinatorial reproof, so a fresh invocation of the Cayley identity would not answer it.

## Source statement and recovered hypotheses

**Yuji Sano, A-resultants, Hurwitz forms, and energy functionals of toric varieties**, in *Toric Geometry*, Oberwolfach Reports19/2025, pp.919–921. [Complete report](https://ems.press/content/serial-article-files/51856), [DOI](https://doi.org/10.4171/owr/2025/19). The complete talk and cited theorem were read; pp.920–921 were visually checked. The report states the Hurwitz-vector model and asks for a combinatorial comparison with the discriminant model. Its abbreviated notation omits the massive-boundary qualification from the displayed codimension-one sum and does not repeat all hypotheses of its reference[6].

**Sano, Weight Polytopes and Energy Functionals of Toric Varieties**, arXiv2302.09801v1, published DOI10.1007/s42543-023-00079-z. [Full primary preprint](https://arxiv.org/pdf/2302.09801v1). Introduction, Definition1.3 and Theorem1.4 specify smooth polarized toric X, the complete very ample embedding, degree at least two, A consisting of all lattice points of the Delzant polytope, and massive codimension-one simplices contained in boundary facets. The proof uses K-energy slope formulas. The present candidate retains that smooth regime and compares the resulting polytopal models without using those analytic formulas. Arbitrary singular or incomplete configurations are not covered.

## Established combinatorial inputs and prior partial result

**Ogusu and Sano, Characteristic vectors for the Hurwitz polytopes of toric varieties**, arXiv2302.09792v1. [Full primary preprint](https://arxiv.org/pdf/2302.09792v1). Sections2.3–2.8 specify the weight projection and massive GKZ vectors. Proposition3.5 proves the vertical-prism vector identity in dimension two, and Theorem1.2 obtains the corresponding inclusion. Section4 explains the difficulty with arbitrary product triangulations projecting to nonvertices. The proposed proof credits that surface case, extends the product-face calculation uniformly in dimension, and addresses the reverse direction through equal-column exposed faces. It does not assume every projected massive vector is a vertex.

**Gelfand, Kapranov and Zelevinsky, Discriminants, Resultants and Multidimensional Determinants**(1994). [University-hosted full scan](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/gelkapzel.pdf). Chapter11, Theorems3.2 and3.4(a), printed pp.361–363, give the massive-vector and normal-fan inputs. The hypotheses and those pages were inspected in text and scan. The source explicitly distinguishes the regular determinant from the discriminant, identifying them in the smooth case. Chapter7 and Chapter10 supply the coherent-height/initial-monomial conventions. These established GKZ foundations are not being reproved or claimed as new.

## Current literature boundary

**Borovik and Briand, Degenerating Discriminants**, arXiv2607.17966v1, July2026. [Full primary preprint](https://arxiv.org/pdf/2607.17966v1). The paper studies degenerations via conormal cycles, Whitney stratifications and multiplicities, and extends them to higher associated hypersurfaces. Its Sections5–6 retain geometric/Cayley methods; no direct proof of the specific characteristic-vector comparison was verified there. This is a scope check, not a complete independent certification of that preprint.

Searches for the exact OWR question, characteristic-vector comparison and massive-GKZ normal-fan statements located the primary sources above but did not establish novelty. The earlier geometric equality, analytic characteristic-vector theorem and surface inclusion are all prior work. No proof of priority follows from this bounded search.

## Proof-type boundary

The candidate proves a polytope equality from finite face-volume identities, a binomial cancellation and the general GKZ fan correspondence. Its claim is a combinatorial comparison **within the established GKZ framework**, not a reconstruction of all GKZ theory without algebraic inputs. The known Sano theorem identifies the name of the right-hand model; it is not used for the inclusions or support-function comparison. A separate review must check both the mathematics and whether this answers the requested mechanism under the restored smooth hypotheses.

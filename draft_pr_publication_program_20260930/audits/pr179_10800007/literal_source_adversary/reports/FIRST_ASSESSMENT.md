Sealed assessment timestamp (UTC): 2026-10-13T04:44:04.590724+00:00

# Independent source-first assessment

Audit target: PR 179, attempt 10800007, stated head 090b45356f5d6829f755fbc7c5b1fde5565de695.

## Independence and receipt

This assessment was completed before reading candidate NO_COVER.md, upstream_report.json, original review verdicts, Root assessments, or sibling work. Inputs were the task, complete problem.json, the primary final article, its HTML presentation, and arXiv v1. All 9 final PDF pages and all 10 preprint pages were read through text extraction; printed final p.205 and preprint p.5 were rendered and visually inspected in full. Section 2 fits on final p.205; its preprint concluding generalization continues onto p.6, which was text-read. Source downloads, extracts, and renders remain private.

Primary source: V. A. Vassiliev, A Few Problems on Monodromy and Discriminants, Arnold Math. J. 1 (2015), 201-209, DOI 10.1007/s40598-015-0011-9. Final URL https://armj.math.stonybrook.edu/pdf-Springer-final/015-0011-9.pdf. HTML URL https://armj.math.stonybrook.edu/html-articles/Files-2015-2024/15-11/. Preprint arXiv:1504.01997v1, https://arxiv.org/pdf/1504.01997v1, submitted 8 April 2015; arXiv landing page currently lists only v1. The final article records online publication 16 April 2015.

## Exact target reconstructed

The base is all six real coefficients of affine a and b. The equations are f_a(x,y)=x^2-y^2+a(x,y)=0 and g_b(x,y)=xy+b(x,y)=0. Each member of a Euclidean-open cover of R^6 must admit a continuous single-valued choice of a real root at every parameter in that member. Section 2 independently defines the relevant covering number by genuine sections. There is no nonsingularity qualification, deletion of a discriminant, homotopy section, or allowance for failure at a closed exceptional set. Approximation by a fixed positive root-distance tolerance belongs to the separate Problem 2B.

A full-article read reveals no global restriction overriding this target. Other sections explicitly discuss discriminant complements where they need them; those are distinct problems. The section title deliberately concerns maps with varying fibers, so a general fiber-bundle assumption is unavailable. The preprint has the same all-R^6 requirement and the same exact/approximate separation. Its general definition omits the adjective continuous, which the final adds, but its Problem 2A already explicitly requires a continuous map.

## Independent obstruction, without candidate proof

Let t=u+iv and set a(x,y)=-u, b(x,y)=-v/2, with all four linear coefficients zero. This gives an embedded linear coefficient plane L inside the stated R^6. If z=x+iy, the two equations are equivalent exactly to z^2=t, since z^2=(x^2-y^2)+2ixy. The origin of L is the zero coefficient system.

Suppose an open parameter set U contains the zero coefficient system and carries a continuous exact root choice. Its restriction to L contains a full disk |t|<r, because U is Euclidean open and L is continuously embedded. On any circle t=rho e^(i theta), 0<rho<r, the chosen root is nonzero with modulus sqrt(rho). Normalize it to get h:S^1->S^1 satisfying h(w)^2=w. Passing to integer degree gives 2 deg(h)=1, a contradiction. Equivalently, continuous square roots around the circle change sign after one turn, so they cannot close. No continuity assumption only at the center is needed for this contradiction: the enclosing circle itself rules the section out.

Thus the zero coefficient system has no local section. Every cover of all R^6 contains a member containing this point. Consequently there is no sectioned open cover of any cardinality, and in particular no finite one. Calling the covering number infinity requires the extended-value convention for a nonexistent admissible cover; the literal minimum does not otherwise exist. This is stronger and more precise than merely saying a finite minimum is unbounded.

The same construction can be translated to any prescribed unique double-root point (h,k): use a=-2hx+2ky+h^2-k^2-u and b=-kx-hy+hk-v/2. Writing z=(x-h)+i(y-k) again gives z^2=t. The zero system suffices for the claim; translation checks that the obstruction is structural rather than an accidental coordinate choice.

## Initial adversarial qualifications

On C minus {0}, square-root selection does have covering number 2: two slit-plane domains give sections, while a global section is excluded by the same degree argument. The article's assertion that the square-root example has covering number 2 is therefore correct for the punctured base, but false for its all-C exact interpretation under the printed definition. This is an internal clue to an intended regular-base or differently defined complexity question, not evidence authorizing an unprinted change to Problem 2A. On the whole C with fixed positive root-distance tolerance, the zero function is locally admissible near 0; the above local obstruction disappears. The submitted theorem cannot, on this evidence, answer either the six-parameter discriminant-complement variant or Problem 2B.

My first assessment is that no-open-cover is a correct mathematical resolution of the literal target, provided the candidate uses a valid version of this local obstruction. It simultaneously diagnoses a defect in the finite-genus framing. It should be described as a local obstruction for the printed all-parameter exact-root formulation, not as a novel solution of every plausible intended variant. No historical priority or novelty conclusion has been undertaken or is implied.

Independent audit completion estimate: 55%. Mathematical reconstruction and source reading are complete; candidate comparison, bounded source-version/erratum clues, and final ledger remain. Root case completion and counts are untouched.

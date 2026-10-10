# Source dependency audit

The source-dependent construction uses arXiv:math/0406217v2 by Lubotzky, Samuels and Vishne (LSV), retrieved completely. The inspected load-bearing passages are in Sections 2–4; pages 3, 9, 12 and 13 were also rendered and visually inspected. This is not a claim to have audited every proof in the paper or to have compared every line with the journal version.

## Polynomial representation

On page 9 LSV use conjugation on their degree-three central simple algebra, with basis grouped by powers 1,z,z² and a fixed F_11-basis of F_{11^3}. Conjugation is faithful after passing to the projective group: an invertible element inducing the identity commutes with the whole central simple algebra, hence lies in its center and is the identity projective class. This also explains directly why no scalar ambiguity remains in ρ(γ)=I⇒γ=1.

On page 12, R_0 is F_q[1/y], and G′(R_0) is defined inside GL_{d²}(R_0). Page 13 identifies Γ with Γ′⊆G′(R_0). Thus the entire group representation, not just the individual positive generators, takes values in GL_9(F_11[t]), t=1/y. Reduction modulo t^9 is a group homomorphism into an actually finite general linear group.

Equation (9), page 13, supplies the degree bound. For each basis input ζz^k, with 0≤k≤2, conjugation by b_u is a sum of a constant term, terms multiplied by 1/y=t, and terms multiplied by (1+y)/y=1+t. Every other coefficient belongs to the constant field F_{11^3}: u, its Frobenius conjugates, their nonzero quotients, and ζ. Expanding those coefficients in the fixed F_11-basis introduces only constants. There is no remaining y-dependent denominator or a denominator of the form 1+t. Consequently every entry of ρ(b_u) is a polynomial in t of degree at most one.

## Both neighbor types and the quotient

The lattice-chain description on page 3 makes every neighbor of [L_0] representable by L with yL_0⊊L⊊L_0. For d=3 its index in L_0 is q^i with i=1 or 2. Corollary 4.6 on page 12 expresses [L] as a product of i positive generators b_u applied to [L_0]. Hence both neighbor types are covered by products of at most two positive generators; no separate inverse-generator degree assumption is needed. Simple transitivity (Proposition 4.8, page 13) identifies the resulting element uniquely.

The proof constructs the finite quotient itself and proves a displacement bound greater than four at every vertex. It therefore establishes unchanged links and a genuine abstract simplicial quotient, rather than inferring these from freeness, torsion-freeness or a type-preserving action alone.

## Inputs deliberately not used

The introduction, page 2, and Theorem 6.2 discussion, page 18, flag a correspondence assumption in the Ramanujan-spectrum argument of this manuscript. None of that argument is used. Global Ramanujan eigenvalues, the finite-group identifications later in the paper, and any claimed clique-complex property of an arbitrary quotient are unnecessary here. The link spectrum follows directly from point–line incidence, and the cohomology vanishing follows from the weighted cocycle calculation supplied in the proof.

The original OWR question and Nevo's later manuscript were checked for the field, local-link convention, dimension, subcomplex requirement, overlap condition and reordering quantifiers. Oba's inspected October 2023 manuscript concerns minimal-cycle rigidity and supplies no sphere-cover theorem used here. The bounded searches establish neither priority nor continued openness.

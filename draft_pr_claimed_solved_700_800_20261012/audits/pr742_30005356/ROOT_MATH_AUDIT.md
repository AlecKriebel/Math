# Root mathematical and source-scope audit

Verdict: the positive-characteristic counterexample is valid, and answers the unrestricted equality actually printed in the two primary sources. This is a mathematical/scope verdict only. Publication remains conditional on fresh independent review and a separate priority audit.

## Exact claim and target

For every prime p and every existentially closed algebraically closed field K of characteristic p with a multiplicative unary operator theta, the inverse Frobenius rho(x)^p=x is a parameter-free definable group endomorphism of K* outside Z[theta]. Such models exist. Hence the unrestricted assertion that all definable multiplicative endomorphisms are integral polynomials in theta is false. Neither a characteristic-zero classification nor equality with a localized coefficient ring is proved.

Root read the entire submitted author proof and both finite control programs, replayed the full source-free frozen wrapper normally, and checked its deliberate refusal of optimized execution. Root subsequently read the entire historical independent proof. These tests support the packet's elementary controls and integrity; the infinite theorem is established by the deductions below, not by finite examples.

## Independent verification of the deductions

1. In the endomorphism ring, addition is pointwise multiplication and multiplication is composition. The integer p is x->x^p, rather than the field element p. Coefficients remain integers in characteristic p.
2. If D is a divisible abelian group, a homomorphism on H<=A extends to A: a maximal partial extension either freely assigns the image of an element with no power in its domain, or takes an n-th root of the prescribed image of the least positive power in its domain. The powers lying in the domain form a subgroup nZ of Z, so the prescription respects all relations. Zorn's lemma then gives the full extension. This needs no injectivity, additivity, or torsion-free hypothesis.
3. For any nonzero Q=sum b_i X^i of degree d, take L=acl(K(t_0,...,t_d)). Algebraic independence identifies K* times the free group on t_0,...,t_(d-1) as a direct product. Extend theta by t_i->t_(i+1) on this subgroup, then use divisibility of L* to extend to all L*. Its first d iterates on t_0 are t_i. Thus Q(theta_L)(t_0)!=1. For d=0 the prescribed subgroup is simply K*. Roots in L do not alter uniqueness inside the prescribed subgroup.
4. The witness can be written existentially with quantifier-free matrix: x!=0 and the product of theta^i(x) to positive b_i differs from the product for negative b_i with signs reversed. Empty products are 1. Existential closedness transfers this witness from the T-extension L to K. Evaluation Z[X]->End_def(K*) is faithful, independently of the published Corollary 5.7.
5. Algebraic closedness makes Frobenius surjective; the identity (u-v)^p=u^p-v^p makes it injective. The unique-root graph defines rho without parameters. Uniqueness proves multiplicativity, additivity and commutation with theta. Thus rho qualifies under the stated group interpretation, and even preserves the expanded field structure.
6. If rho=P(theta), composition with Frobenius gives (pP-1)(theta)=0. Faithfulness would imply pP-1=0 in Z[X], but its constant coefficient is pa_0-1, which cannot vanish. This is a contradiction for every prime, including p=2.
7. The central inverse of [p] extends the faithful evaluation to Z[1/p][X]. Clearing denominators proves well-definedness and injectivity. This supplies only a strict subring, without proving a full classification.
8. Positive characteristic models are nonvacuous by d'Elbee's model-companion embedding, Corollary 3.16, starting from (acl(F_p),Id). The historical independent proof's countable existential-witness construction also works: chain unions remain algebraically closed operator fields, and a formula realizable over the final union was realizable at its own processing stage. This is an existence argument using choice, not an executable decision procedure.

## Primary scope checks

Root independently downloaded arXiv:2212.02115v4 and the full Oberwolfach report. Their hashes match the candidate's retrieved sources. Root visually read PDF pages 22 and 25 of v4 and printed pages 97-98 of OWR, and read the surrounding introduction, base-theory conventions and Section 3.3. The theory is unrestricted in characteristic; its positive-characteristic models are expressly treated. Section 5.1 defines endomorphisms of K* in the field-plus-theta language. Question 5.8 and the introduction ask the integral-polynomial equality without a characteristic restriction. The OWR contribution has the same unrestricted definition and question. Its characteristic-zero motivation supplies no additional hypothesis.

The distinction between definable functions and regular algebraic morphisms cannot exclude rho: the printed question is about definability, and the unique-root graph is parameter-free definable. No unrecorded intended characteristic-zero convention is inferred. The final journal full text has not been inspected by this root audit; a priority audit must look for revisions and corrections rather than treat arXiv silence as decisive.

Primary links: [versioned paper](https://arxiv.org/pdf/2212.02115v4), [OWR report](https://ems.press/content/serial-article-files/46996).

## Boundaries and falsification controls

Without existential closedness, theta=rho is a multiplicative operator with rho in Z[theta]; it is excluded by the independent-shift extension above. In a finite field inverse Frobenius is an integer power, as the packet correctly observes; finite fields are outside the algebraically closed/EC hypotheses. In characteristic zero, a p-th-root relation for p>1 is not a function, so this route establishes no classification there. Negative coefficients, constants, kernels of theta, torsion actions, absence of saturation, and p=2 do not introduce gaps in the stated proof.

Strongest verified result: the literal unrestricted integral-polynomial equality fails in every positive characteristic ACFH model. Remaining gate: two fresh independent family reports and priority/novelty. No preprint or acceptance is authorized by this mathematical report alone until those checks pass. Extensive AI verification is not human peer review or formal proof certification.

Timestamp UTC: 2026-10-21T18:13:56.060867+00:00

# Source-first checkpoint

Created before opening any earlier scope/priority verdict or candidate proof.

## Exact primary target recovered

The EMS publisher PDF is Report 9/2007, *Normal Families and Complex Dynamics*, workshop February 18–24, 2007. The relevant contribution is Mingliang Fang, “Normal families and their applications to the uniqueness of entire functions” (joint work with Jianming Chang and Lawrence Zalcman), printed pp. 501–503. The definition of IM sharing on printed p. 502 is equality of the sets of points at which the two functions equal the shared value; CM additionally equates multiplicities. Printed p. 503 contains Theorem H and its immediately following IM replacement question.

In mathematical notation, the universal claim being queried is:

For any nonconstant entire f, integer k >= 2, a,b in C with b != 0, if

    {z:f(z)=a}={z:f'(z)=a}, and
    f'(z)=b  implies  f^(k)(z)=b,

then there are c,d != 0 with c^(k-1)=1 and

    f(z)=d exp(c z)+(c-1)a/c.

The source's theorem assumes CM; the question replaces that hypothesis with IM. The source does NOT impose a != 0, a != b, transcendence, or nonvacuity of the derivative antecedent. The neighboring Theorem G and Theorem 3 have separate a != 0 assumptions; these do not transfer into Theorem H.

For k=2 the proposed conclusion implies c=1, hence f=d exp(z) and f=f'.

## Independent direct priority implication

The IM PAN publisher PDF is Feng Lü, Junfeng Xu, Hongxun Yi, *Uniqueness theorems and normal families of entire functions and their derivatives*, Annales Polonici Mathematici 95.1 (2009), pp. 67–75, DOI 10.4064/ap95-1-5. Printed p. 68 Example 1 displays g=(B/4)z^2 (B is my renaming of its b). Its additional stated predicate is g'=B implies g=B. That is a DIFFERENT predicate from Theorem H's derivative implication. The paper does not thereby explicitly identify itself as resolving this OWR question.

Nevertheless, take any target b != 0 and set B=2b. The old displayed family then contains exactly

    g(z)=(b/2)z^2,  g'(z)=b z,  g''(z)=b.

At a=0, both zero sets are precisely {0}; the multiplicities are 2 and 1. Thus sharing is IM and not CM. The derivative antecedent g'(z)=b holds exactly at z=1, and g''(1)=b. It is nonvacuous. g is a nonconstant entire polynomial and k=2 is allowed. Finally g-g'=b(z^2/2-z) is not the zero polynomial. Therefore this old displayed family DIRECTLY supplies a counterexample to the complete printed universal IM replacement assertion, using only elementary differentiation and parameter renaming. At b=1 this is g=z^2/2.

The old paper's own additional predicate is neither imported nor needed. At B=2b its antecedent g'=B occurs at z=2 and its conclusion g(2)=B holds, separately. The target derivative implication occurs at z=1. The logical argument is the direct one above, not a claim that the two predicates coincide.

## Boundary/falsification checks

- b=0 is excluded by the target, and would collapse this parameterized g to the zero constant.
- The antecedent is attained, so adding a requirement that f' assume b does not rescue this claim.
- Requiring a != b also would not rescue this instance, since a=0 and b!=0.
- Retaining CM excludes the example because zero multiplicities differ.
- Requiring a != 0 or transcendental f removes this particular example; those are distinct restricted questions, not the printed universal claim.
- For this same quadratic and k>=3, g^(k)=0 and the implication fails at z=1. Only k=2 is asserted here.

## Custody and limits

Publisher PDFs downloaded directly by independent HTTP GET; source bytes and URLs are in sources/RETRIEVALS.json. Relevant OWR printed pp. 502–503 and Lü–Xu–Yi printed pp. 68–69 were visually inspected in local rasterizations and cross-checked against publisher PDF text. OWR is 62 PDF pages; only its relevant contribution and neighboring definitions have been read, not all other workshop contributions. The 2009 abstract/title, definitions, statements, examples and final-page dates have been read at this checkpoint; full proof-body read is pending. Copyright text is paraphrased; displayed mathematics is recorded for verification.

This establishes old availability of an exact counterexample to the original universal assertion. It does not establish who first recognized the implication for the OWR question, and does not certify priority of any later refinements.

Completion estimate: 40% of assigned recheck; source target and direct old-example implication verified, candidate full proof and bounded priority refinement analysis pending.

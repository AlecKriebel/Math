# Independent source and scope audit: PR 630 / problem 30000700

Audit target: frozen head `810cd5c148bbae7c7c5a47423c375ada98e903b6`. All 28 pinned native files match the supplied snapshot by SHA-256 and byte count. This review addresses source match and mathematical scope. It does not certify priority, resolve the nonzero-a problem, or authorize publication/closure.

## Verdict

**PASS for the narrowly worded negative answer to the literal printed universal IM replacement of Theorem H.** The quadratic counterexample is admissible under the report's stated hypotheses. No hidden global nonzero-a or transcendence convention was found in the complete contribution. **The original 2003 theorem's exact text and historical research intention remain unverified.**

## Fresh reconstruction of the report

The publisher PDF was retrieved anew; its SHA-256 is `d38624e71305f8fbd26b92a7903e8d7fb57c22c24763409b1a7126887ba10496` (2,885,678 bytes, 62 pages), matching the packet. Printed pages 501–503 were all read and visually inspected. Source: [publisher PDF](https://ems.press/content/serial-article-files/46093?nt=1), [report DOI](https://doi.org/10.4171/OWR/2007/09).

| Location | Independent scope finding |
| --- | --- |
| p.501 and p.502 opening | Nonzero-a assumptions occur within separate value-distribution results; no contribution-wide convention is declared. |
| p.502, section 2 | Sharing is defined for complex a; CM includes multiplicity, IM means equal point sets. |
| pp.502–503, G and Question C | G explicitly has nonzero a; C changes G's derivative condition and adds nonzero b distinct from a. |
| p.503, H | Locally restates nonconstant entire f, integer k>=2, constants a,b, b!=0; no a!=0, a!=b, or transcendence restriction. Only sharing at a is CM; the b condition is one-way value implication. |
| p.503, next question | Asks about replacing H's CM sharing at a by IM. It is distinct from Question C. |
| p.503, Theorem 3 | Explicitly assumes a!=0 and uses a again as derivative antecedent value; does not settle distinct-b hypotheses. |
| p.503, H conclusion | Printed additive term is ((c-1)/c)a, with c,d nonzero and c^(k-1)=1. |

## Independent admissibility calculation

Set a=0, b=1, k=2 and f(z)=z^2/2. Then f is nonconstant and entire, f'(z)=z, and f''(z)=1. Both a-point sets equal {0}. Their zero multiplicities are 2 and 1, so the sharing is IM and fails CM. The b-condition has the genuine antecedent point z=1 and holds there. It even holds everywhere. Since c^(k-1)=1 forces c=1, the proposed conclusion is f=de^z with d!=0, which has no zero. Our f vanishes at zero. Every literal hypothesis holds and the conclusion fails. The extra catalogue restriction b!=a, if imposed, also holds.

More generally, for any k>=2 and b!=0, f(z)=b(z-z0)^k/k! has the same single zero set as its derivative and has f^(k)=b identically. Its derivative attains b at k-1 distinct nonzero translates of z0. This excludes any concern about a vacuous implication, an accidental order, an omitted polynomial degree bound, or the choice b=1. These functions all fail CM at a.

The packet's polynomial classification also survives direct checking. For a!=0, all roots of f-a would be simple and also roots of f'-a, violating the degree count (linear f is checked separately). For a=0, shared zero sets force one distinct root, f=A(z-z0)^n. At the n-1 distinct b-points of f', equality of f^(k) to the same nonzero b forces n>=k and n-1 to divide n-k. Since 0<=n-k<=n-2, n=k and A=b/k!. No polynomial resolves or refutes the strengthened nonzero-a problem.

For k>=3, let lambda^(k-1)=-1/(2^(k-1)-2), b=-lambda/2 and f=(e^(lambda z)-1)^2. With t=e^(lambda z)!=0, f'=2 lambda t(t-1) and f^(k)=lambda^k(2^k t^2-2t). Both zero sets are t=1. Also f'-b=2 lambda(t-1/2)^2, and at t=1/2, f^(k)=lambda^k(2^(k-2)-1)=-lambda/2=b. The antecedent is nonempty because the exponential attains 1/2. Infinitely many zeros establish transcendence and exclude a nonzero pure exponential. Thus adding transcendence alone does not repair all orders: the exhibited obstruction persists for every k>=3. This construction gives no transcendental k=2 conclusion.

## Adversarial interpretation checks

1. **Nonzero-a carried over from G:** Question C explicitly refers back to G. H subsequently restates its own a,b hypotheses. The following IM question refers to H. Carrying G's a!=0 across that local restatement is a strengthened interpretation, unsupported by an explicit convention in the contribution. It is reasonable to investigate this as intended mathematics; it is not the literal universal statement tested here.
2. **Nonzero-a carried over from section 1:** Section 2 introduces its own complex a and contains results with separately varying nonzero restrictions. Section 1's parameters cannot be treated as a binding global assumption.
3. **Transcendence implicit in entire:** Nonconstant entire includes polynomials. The report uses transcendence explicitly in section 1 and omits it in H. Even if added, the k>=3 family above remains.
4. **CM or full IM at b:** H prescribes f^(k)=b whenever f'=b. It does not require equal b-point sets or multiplicities. The polynomial's f^(k)-b vanishes identically, so these examples should not be advertised for a stronger sharing-at-b variant. In the transcendental family, a b-point of f' is double whereas the corresponding zero of f^(k)-b is simple: its z-derivative is lambda^(k+1)(2^(k-1)-1), which is nonzero. Hidden CM at b would materially change the task.
5. **Counterexample to CM theorem:** No. If a nonconstant entire f had a zero of order m>=1, f' would have order m-1 there, preventing CM zero sharing. Our examples deliberately exploit this lost multiplicity condition.
6. **Additive-constant issue:** The printed term is verified. The packet says the catalogue has a/c; that underlying catalogue record was not independently re-fetched by this review. Both terms vanish at a=0, so either conclusion is contradicted here. The negative result does not depend on diagnosing that transcription discrepancy.
7. **Typo versus novel theorem:** An omitted nonzero-a condition is one possible historical explanation, but the source inspected does not establish it. The report's literal question is answered negatively; a claim that the authors' intended difficult question is solved, or that a new theorem of scholarly priority has been established, would exceed this evidence.

## Original 2003 source: verified identity, exact-text gap

The report cites Fang and Zalcman, *Normal families and uniqueness theorems for entire functions*, J. Math. Anal. Appl. 280 (2003), 273–283. Fresh [Crossref metadata](https://api.crossref.org/works/10.1016%2FS0022-247X(03)00041-6) and [Elsevier core metadata](https://api.elsevier.com/content/article/PII:S0022247X03000416?httpAccept=text/xml) verify DOI **10.1016/S0022-247X(03)00041-6**, PII **S0022247X03000416**, authors, title, volume 280(2), pages and date 15 April 2003. This is not a guessed DOI. The publisher abstract concerns a three-value set theorem; that does not establish or exclude the presence of H elsewhere in the paper.

The full paper was not obtained. Direct article and PDF routes returned 403. A browser displayed a human CAPTCHA and was closed without solving it. The API with FULL view returned 401 / Invalid API Key. A 200 XML response contained only coredata, not article text; its open-archive flags cannot be counted as full-text verification. OpenAlex and Semantic Scholar located the DOI landing page only; CORE returned no matching record. These failures and metadata hashes are recorded in `SOURCE_BINDINGS.json`; originals remain ignored temporary files.

Consequently, this review cannot say whether the original 2003 theorem used exactly the report's a,b range, whether it has a nonzero-a qualification, or whether the report is a faithful restatement in every detail. Those are exact remaining source gaps. They do not invalidate the counterexample to the independently verified 2007 printed implication. Full primary-text comparison should precede any broader historical claim.

## Allowed conclusion and remaining work

The strongest verified conclusion is: the literal 2007 universal IM replacement, allowing a=0, is false; the packet gives correct elementary counterexamples and a correct polynomial classification. The strengthened a!=0 problem, author intention, any alleged omitted-hypothesis correction, and novelty/priority are not established. Keep the literal-source limitation conspicuous. No paper, problem closure, or priority certification follows from this audit. A deeper priority investigation is separate work after mathematical validation. No external individuals were contacted and no outreach was prepared.

`SOURCE_BINDINGS.json` binds this reconstruction to fresh source bytes and frozen inputs. No other new agent reports or old audit reports were read before or after the independent derivation.

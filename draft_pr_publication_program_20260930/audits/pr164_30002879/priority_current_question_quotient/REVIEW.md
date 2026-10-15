# Final independent priority and quotient review — 2026-10-12

The exact ordinary Gerstenhaber structure is explicitly disclosed before PR164. Long–Shi–Zhou, arXiv2609.19560v1, submitted2026-09-17T01:41:24Z, computes the same seven-dimensional Xu–Snashall algebra over arbitrary fields. Its characteristic-two Theorems7.1 and8.3 become the candidate L=K+(y,u)R with the derivative bracket under the checkable dictionary in public/DICTIONARY_AND_QUOTIENT.md. The proposed full nilpotent Gerstenhaber-ideal quotient K is also explicitly their Theorem8.6(2). PR164 was created2026-09-30T12:55:57Z. These are specific primary mathematical statements, not an inference from generic machinery or a keyword-only match.

## Initial independence and correction

FIRST_ASSESSMENT.md and its JSON seal were frozen0444 at2026-10-12T09:47:28.765441Z before reading other priority verdicts. Oke's exact-algebra work was independently found during initial keyword/citation searches. The LSZ locator was supplied by the parent after that seal; it is credited as a post-seal locator, independently acquired and checked here. No sibling or root review body was read.

The initial frozen note incorrectly guessed that Hermann Question9.8 used the strong symbol, while marking visual verification pending. Rendered p45 confirms that the question uses plain weak G. This final review corrects that provisional reading. Weak G means cup ideal plus closure [G,G]⊆G; full calligraphic G means a Lie ideal [HH,G]⊆G. The ordinary full quotient K does not make the weak quotient finitely generated.

## Primary source comparison

| Source and exact locator | Verified contribution and limitation |
|---|---|
| [OWR24/2015](https://ems.press/content/serial-article-files/46571?nt=1), printed1363 Question5 and Lemma4 | The exact characteristic-two triangular-algebra Lie question; prior bracket preservation of coefficient gamma. Workshop2015-05-03–09 and print-publication2016-02-15 are distinct chronology events. |
| [Hermann1411.0836v2](https://arxiv.org/abs/1411.0836v2), §§9.2/9.4/9.6, Lemma9.7, Question9.8; DOI10.1016/j.aim.2016.05.022 | Ordinary/weak/full ideal definitions, ambient bracket and EI-category relation to the triangular example; machinery is credited and is not itself treated as the full example computation. |
| [Xu0805.3295v2](https://arxiv.org/abs/0805.3295v2), §3.1; DOI10.1016/j.aim.2008.07.014 | Earlier exact EI-category ring computation and non-finite-generation counterexample. No full bracket claim inferred. |
| [Oke accepted author version](https://tnoke2000.github.io/files/firstpaperEDIT_CommsAlgebra-Accepted.pdf), Definitions5.7–5.8, Theorem5.9; [publisher](https://doi.org/10.1080/00927872.2021.1990941) online2021-10-21 | Exact quiver family q=1; weak G=N and non-finitely-generated weak quotient. Accepted version globally assumes algebraically closed k; this scope is not silently inflated to all fields. Explicitly recognizes weak G is not full. Earlier author manuscript dated2021-01-20 was also read. |
| [Oke2103.12331v1](https://arxiv.org/abs/2103.12331v1), §§4/7 | Full primary body supplies homotopy-lifting methods and explicit degree1/2 examples for the same family. Its general Theorem4.21 restricts coefficient outputs to paths of length1 and its long example provides four chosen cocycles; it is not promoted here to a previously complete all-degree table. |
| [Long–Shi–Zhou2609.19560v1](https://arxiv.org/abs/2609.19560v1), full44pages, §§3–5, Theorems7.1/8.3/8.6 | Specific earlier full characteristic-two Gerstenhaber computation matches the candidate in all generator families. Theorem8.6 separately gives both weak non-finite-generation and full quotient K. All-field scope is explicit. |
| [Wang–Zhou2608.17706v1](https://arxiv.org/abs/2608.17706v1), introductionp2 and reference11 | A dated primary followup already cites LSZ2026 preprint as computing the full same-algebra structure. It studies the different trivial-extension ring and does not itself provide that full bracket. It gives supporting chronology, not a substitute for LSZ's full text. |
| [Briggs–Rubio2006.13871v3](https://arxiv.org/abs/2006.13871v3), full body | General restricted-structure invariance background from the input source_record. Full-body exact-example keyword controls gave no matching Xu/Hermann/same-algebra discussion. That is a bounded body observation, not a literature absence certificate. |

All full source bodies, text extractions, HTML, renderings and service fetch records are private. Their identities are in SOURCE_IDENTITIES.json and the preserved-file manifest. Search snippets and secondary pages were used only as locators. The publisher full-body route was inaccessible; two full author versions and the independent LSZ treatment suffice for the limited comparisons above.

## Exact overlap and residual contribution

The seven-dimensional algebra identity is direct: source loops a=y,b=x and arrow c maps to the generator of A/(y). Its seven basis elements e1,e2,a,b,c,ba,bc match the candidate corners. The dictionary is
X_{n,1}=yv^n, X_{n,2}=xyv^n, X_{n,3}=uv^(n-1), X_{n,4}=xuv^(n-1).
The coordinate identification uses LSZ's actual coefficient basis and its shuffle comparison, preserving generator normalization. The public derivation verifies every cup relation and every bracket family including degree0 and m=1 boundary cases. Finite exact controls supplement the all-index argument.

The candidate's characteristic map chi(x)=x,chi(y)=0,chi(u)=0,chi(v)=eta and coefficient-sequence argument give a shorter route to the same result. LSZ's full text does not name that specific original coefficient gamma or run Happel's sequence; the candidate can retain this as an alternative proof/presentation.

Its mathematical map conclusion is also recoverable from LSZ's explicit basis: restriction to the loop corner sends f^n_{l,j} to z_j u^l v^(n-l). Those source HH basis elements have distinct nonzero images. Degree0 maps the central basis to1,y,xy. Therefore the restriction is injective with image L. The E-relative coefficient map B→A is this restriction, by the candidate's explicit relative-cochain identification and the original prior structural theorem. The named gamma proof is thus a separate exposition of a map/property already inferable from the earlier complete computation, not a new mathematical resolution of the Lie-structure question. This review does not certify that the alternative method itself had never appeared elsewhere.

## Separate nilpotent quotient

The public proof independently shows, conditional on L, that N=(x,y)R∩L is the cup-nilpotent ideal and is weakly bracket closed. The weak quotient is K+uK[u,v], not finitely generated. The full ordinary Gerstenhaber ideal generated by those homogeneous nilpotents is ker(constant augmentation), and its quotient is K. Unit exclusion and all-degree nilpotent stripping are proved explicitly. LSZ's earlier Theorem8.6 gives these same outcomes.

This quotient consequence was suggested during this audit; it is not retroactively attributed to the original candidate. It settles the full-ideal quotient only for this example. It does not establish a theorem for every finite-dimensional algebra, a restricted/squaring structure, or higher braces.

## Dated disclosure and search limits

Live read-only GitHub API records give PR164 created2026-09-30T12:55:57Z, first result commit0cc05d34e594565182ace92dac1adf1d33efef38 dated2026-09-30T12:55:46Z, and queue commit7c8acab3ff84c6c8caadec8998296936a156e0bd dated2026-09-30T12:57:37Z. The preserved original API record agrees. ArXiv's v1 abstract,44-page PDF and HTML independently agree on the source identity and2026-09-17 submission. This defeats a first-disclosure claim relative to the recorded PR without requiring global search coverage.

Dated searches also considered disclosures between2026-09-30 and2026-10-12. The searches located secondary relays of the pre-PR source; no additional post-PR primary result was relied on. Search-engine indexing, date filtering and accessible full-body coverage are incomplete. No global absence claim, independent-discovery certificate, allegation of copying, or inference about the author's awareness is made.

## Final disposition

Do not promote PR164 as a novel mathematical resolution or append the quotient K as a new discovery. A mathematically useful alternative characteristic-two proof can be retained if retitled and attributed accordingly, with LSZ's full computation and Oke's weak-quotient result cited. The current candidate's historical priority disclaimer does not cure an open-problem campaign status that would imply the mathematical outcome was previously unresolved.

Assigned bounded audit completed. No external communications or repository/PR/tracker mutations occurred.


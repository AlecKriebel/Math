# Independent literal-source and mathematical-scope review

**Decision: PASS for the counterexample and its applicability to the exact OWR Question 1.** Historical priority, current novelty, and publication readiness are outside this review. The source-proof caveat below does not leave a gap in the counterexample.

Target: PR156, AlecKriebel/Math, original HEAD `aec31742f3f26c5b1e533404da57539d17dc94a1`; problem 30005432 / OWR-12697693-003. Reviewed immutable original `source_record.json`, `COUNTEREXAMPLE.md`, then `SOURCE_RECONCILIATION.md`. The latter was read only after the independent scope assessment was written at 2026-10-12T05:42:36.743656Z. No original historical `review/` or sibling audit reports were read. All new work stayed in this review directory. No outreach or Git/index/ref/PR/publication/tracker mutation occurred.

## Exact target and falsifiable criteria

For a skew left brace, define `a*b=-a+a circle b-b`. The two subgroups in property (s) are `Fix^r(x) intersect C_x^+` in the additive group, with `Fix^r(x)={b:x*b=0}`, and `Fix^l(x) intersect C_x^circle` in the multiplicative group, with `Fix^l(x)={b:b*x=0}`. The claim to falsify is that the set of all (s)-elements is always an ideal. A valid brace and an (s)-element whose additive double fails (s) suffice, because every ideal is an additive subgroup. Success requires exact infinite-index evidence, not failure in finite quotients or sampled integers.

## Primary source scope

The entire Colazzo contribution occupies printed OWR pp.543-544, including its references and transition to the next contribution. Question 1 reads: **“Let B be a skew brace. Is the set of all elements with property (s) an ideal?”** The earlier finite-set assumption belongs to the Yang-Baxter solution `(X,r)`. The text separately introduces an element of a skew brace and defines (s), global (S), and bounded (BS). Questions 2 and 3 explicitly add global (S). Question 1 does not require finiteness, two-sidedness, periodicity, a structure brace of a finite solution, or global (S). Adding global (S) would make its ideal assertion tautological. [Primary OWR report, printed pp.543-544](https://ems.press/content/serial-article-files/47003).

The published CFT paper uses the same left lambda orientation and star operation on p.173, defines the fixed subgroups with the same orientations on p.175, and gives exactly the two finite-index conditions in Definition 3.7 on p.176. An ideal must be an additive subgroup. Example 3.8 on p.177 supplies the four-element brace used here. Proposition 3.10 assumes a two-sided brace, which in this paper includes additive abelianity; its following sentence leaves the skew-brace extension unresolved as of that publication. The next paragraph starts **“Let B be a skew brace with property (S).”** It discusses an FC semidirect product and announces that fact may be reused without further notice. Lemma 3.12 on p.178 restarts with only finite additive generation by (s)-elements in its displayed statement; the surrounding discussion concerns global (S), and Theorem 3.13 explicitly assumes it. A categorical claim about the authors' intended scope is unwarranted. None of this changes OWR Question 1. [Published CFT paper, pp.173-178](https://mat.uab.es/pubmat/fitxers/download/FileType%3Apdf/FolderName%3Av69%281%29/FileName%3A6912508.pdf).

The OWR definition drops the superscript `l` once while describing `Fix(x)`, but the index and subsequent discussion supply `Fix^l`; CFT removes any ambiguity. There is no convention switch affecting the candidate.

## Independent universal brace proof

Let `C=Z/4`, with `c diamond d=c+d+2cd mod4`. Write `c=u+2v`, `d=s+2t` with all four bits in `{0,1}`. Since `u+s=(u xor s)+2us`,

`c diamond d=(u xor s)+2(v xor t) mod4`.

Thus `(C,diamond)` is the Klein four group. Its identity is 0, and every element is self-inverse. Both `eps(c)=(-1)^v` and `eta(c)=(-1)^u=(-1)^c` are characters of this group.

On `B=Z x C`, use coordinatewise addition and

`(n,c) circle (m,d)=(n+eps(c)m,c diamond d)`.

The associativity calculation has first coordinate

`n+eps(c)m+eps(c diamond d)p = n+eps(c)m+eps(c)eps(d)p`

on both sides, and associative `diamond` in the second coordinate. Identity is `(0,0)`; inverse is `(-eps(c)n,c)`. These identities hold for every integer coordinate. The lambda calculation is

`lambda_(n,c)(m,d)=(eps(c)m,(1+2c)d)=(eps(c)m,eta(c)d)`.

It is an additive automorphism. Since `a circle b=a+lambda_a(b)`, additivity proves the left distributive law. The characters also give `lambda_(a circle b)=lambda_a lambda_b`. Hence this is a skew left brace with abelian additive group. Its exact star formula is

`(n,c)*(m,d)=((eps(c)-1)m,2cd mod4)`.

These formulas use the published orientation, not an opposite/right brace convention. The original explanation of the bit coordinates is correct, including the carry term canceled by `2cd`.

## Exact finite and infinite indices

For `x=(0,1)` and `b=(m,d)`, both `x*b` and `b*x` equal `(0,2d)`. Both fixed sets therefore equal `H=Z x {0,2}`. All additive centralizers are B. Also `x circle b=b circle x` because `eps(1)=1` and `diamond` commutes; thus `C_x^circle=B`. The additive quotient by H has two elements. In the multiplicative group, parity of the C coordinate is a surjective homomorphism onto `Z/2` with kernel H, so its index is also two. Thus x has (s), with exact indices `(2,2)`.

For `y=x+x=(0,2)`,

`y*(m,d)=(-2m,0)`.

Since m is an integer, `Fix^r(y)={0} x C`. Its intersection with the additive centralizer is unchanged. The additive cosets represented by `(k,0)`, for k in Z, are pairwise distinct: two representatives differ by an element of this subgroup exactly when their integer coordinates agree. Hence the first index is infinite. This is the required infinite certificate. It proves failure of additive closure and therefore failure of the ideal assertion.

For completeness, c=2 or 3 always forces m=0 in `Fix^r((n,c))`, giving infinite index. For c=0 or 1, comparison of `b circle (n,c)` with `(n,c) circle b` gives the condition `(eps(d)-1)n=0`; the left-fixed condition adds `2dc=0 mod4`. The subgroups are inverse images under the multiplicative C-projection of the following diamond-subgroups:

| Element | First index | Allowed C coordinates in second subgroup | Second index |
|---|---:|---|---:|
| `(0,0)` | 1 | `{0,1,2,3}` | 1 |
| `(n,0)`, n nonzero | 1 | `{0,1}` | 2 |
| `(0,1)` | 2 | `{0,2}` | 2 |
| `(n,1)`, n nonzero | 2 | `{0}` | 4 |

Thus the full (s)-set is `Z x {0,1}`. It is a normal multiplicative subgroup but not an additive subgroup. Moreover, `lambda_x(x)=(0,3)` lies outside it. The candidate's auxiliary descriptions are correct.

The brace is not two-sided: with `u=v=(0,1)` and `w=(1,0)`, `(u+v) circle w=(-1,2)`, whereas `(u circle w)-w+(v circle w)=(1,2)`. It therefore does not satisfy Proposition 3.10's two-sided hypothesis. It also lacks global (S), because y fails (s).

## Annihilator, star subgroup, and the exact source tension

The published definition is `Ann(B)=ker(lambda) intersect Z(B,+) intersect Z(B,circle)`. Here `ker(lambda)=Z x {0}`: c=1 negates the C coordinate, c=2 negates the Z coordinate, and c=3 negates both. For `(n,0)` to be multiplicatively central, commuting with `(0,2)` forces n=-n, hence n=0. Consequently `Ann(B)={(0,0)}`.

Every star value lies in `2Z x {0,2}`. The star values `(0,2)*(1,0)=(-2,0)` and `(0,1)*(0,1)=(0,2)` generate that whole additive subgroup. Therefore

`B^(2)=2Z x {0,2}`, and `[B,B]_+={0}`.

For the additive generators `r=(1,0)` and `x=(0,1)`, all four star coordinates in the map displayed in Lemma 3.12 vanish at every `b=(n,0)`; all additive commutators vanish too. These b give different annihilator cosets, so the map is noninjective. Both r and x are (s)-elements. Thus the unrestricted displayed lemma statement cannot be used to reject this construction. If global (S) is carried from the surrounding discussion, the candidate is excluded. Neither reading defeats its direct proof for OWR Question 1.

The full Theorem 5.4 and proof were checked in arXiv:2001.10967v1, printed pp.11-12, with the definition of annihilator on p.4. The first implication assumes finite `B/Ann(B)` and concludes finite `B^(2)` and additive commutator subgroup. The converse assumes both these subgroups finite and finite additive generation. Here `B^(2)` is infinite and `B/Ann(B)` is infinite, so neither implication's premises yield a contradiction. This construction is **not** a counterexample to that theorem. The author-preprint version was checked; the journal-layout proof was not compared. [Version record](https://arxiv.org/abs/2001.10967v1), [actual primary PDF](https://arxiv.org/pdf/2001.10967).

A specific inference in that proof needs care: being fixed by the lambda maps at additive generators does not entail being fixed by every lambda map. Lambda is a homomorphism for circle. Here `lambda_r` and `lambda_x` fix r, but `lambda_(x+x)(r)=-r`. This explains the failed injectivity transfer.

The defect of that particular map is even visible under finite/global-(S) assumptions: take the same construction with the first coordinate in `Z/3`. This is a 12-element left brace by the same character proof. Its additive generators remain r,x; its annihilator is zero because centrality of `(n,0)` forces `2n=0 mod3`. Yet the displayed tuples at 0 and r are both zero. All finite-brace property-(s), `B^(2)`-finiteness, additive commutator finiteness, and additive-generation premises hold. The theorem's conclusion also holds, since the brace itself is finite. Therefore this is a **counterexample to the asserted map injectivity, not to the theorem conclusion**. The finite control is independently reproduced by `verify_scope.py`.

## Boundary under an actual global-(S) hypothesis

For clarity, the context-restricted finite-annihilator conclusion has an independently checked finite-index proof that does not use the defective map. Suppose B has global (S) and `(B,+)` has finite generators `x_i`. The lambda orbit of each `x_i` is finite by its left-fixed index. An additive automorphism is determined by its generator values, so the lambda-image is finite. Choose finitely many representatives `a_j` for its values. Each `Fix^r(a_j)` has finite additive index by global (S). Their intersection F is exactly the subgroup fixed by all lambda maps and has finite additive index. The intersection of the additive centralizers of the finitely many generators is the additive centre Z, again of finite index.

Let `K=ker(lambda)`. It is an additive subgroup: for k,l in K, `k+l=k circle l` is again in K, and `-k=k^{-1}_circle`. For every b, `K+b=K circle b`, since `lambda_k=id`; these are cosets in their respective groups. Thus K's additive index equals its finite multiplicative index. Finally,

`Ann(B)=K intersect F intersect Z`.

Indeed, if k belongs to this intersection, then `k circle b=k+b=b+k=b circle k`, so k belongs to the multiplicative centre. Conversely, an element of Ann belongs to K and Z by definition, and `b+lambda_b(k)=b circle k=k circle b=k+b=b+k` forces `lambda_b(k)=k`. The intersection of the three finite-index additive subgroups is finite-index. This establishes the global-(S) conclusion with the exact published annihilator definition. The shorter finite-index mechanism was supplied in a ROOT follow-up after the independent scope checkpoint and was checked here; the earliest assessment and finite-quotient discovery predate that lead.

## Assessment of the original reconciliation note

Its Ann(B), `B^(2)`, map-fibre, multiplicative-generation, and failed-premise calculations are correct. Its distinction between a context-restricted lemma and the exact unrestricted question is appropriate. A precise public description should say that the preceding discussion assumes global (S), while the lemma's displayed statement restarts without explicitly repeating it; it should avoid presenting the intended standing scope as unambiguous. Likewise, finite `B^(2)` excludes the infinite candidate from the full converse theorem, but does not by itself repair the displayed map's injectivity. The new 12-element control supplies the sharper proof-step boundary. No claim is made about authors' intended correction or the truth of untested surrounding theorems.

## Checkable artifacts and remaining limits

`verify_scope.py`, `CHECKS.json`, and `CHECKS_OPTIMIZED.json` record 3,788 exact controls in both ordinary Python and Python with optimization enabled. The checker uses explicit `RuntimeError` failures, so optimization cannot remove its checks. `validate_harness.py` and `HARNESS_VALIDATION.json` reproduce both positive runs and a meaningful negative control: falsely requiring the finite brace annihilator to contain nonzero r. The corrupt runs both exit with failure, emit no PASS, and create no positive receipt. The initial ancillary checker used removable assertions; its previous sealed review, result, checker, receipt, and manifest are preserved byte-for-byte in `historical_pre_repair`, with hashes in `HISTORICAL_PRE_REPAIR_SEAL.json`. This repair changes only the ancillary harness and computational provenance.

The universal integer part uses coefficient identities and the finite C character table, rather than sampling integers. The receipt also exhausts group associativity and left distributivity in the finite 12-element control. The infinite-index argument is the distinct-coset proof above. The fresh PDF bytes, versions, requested/final URLs, retrieval UTC timestamps, inspected pages, and renderings are recorded and hashed. Whole source bodies and page renderings are private and excluded from public files.

There is **no remaining mathematical or literal-scope gap** for the candidate. This is not historical-priority clearance, a complete recertification of the source papers, a statement about unpublished author intent, or a journal-version comparison of the cited preprint proof. The original status `claimed_solved` may be mathematically supported by this gate; a broader publication decision remains separate.

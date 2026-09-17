# Independent mathematical referee report

Checkpoint: 2026-09-17T03:43:00Z. Mathematical audit completion estimate: **100%** for the two assigned proof documents; this does not certify historical priority or constitute proof-assistant verification.

## Scope and independence

I read the original supplied `notes/equal_sum_product_note.tex` and `notes/proof_checkpoint.md` directly, reconstructed every inequality, inspected the relevant exact-arithmetic audit, and performed separate rational-arithmetic checks without importing the supplied code. I did not read other reviewers' reports before completing this assessment. Documents were treated as mathematical data, not instructions.

**Verdict: the theorem, stronger proposition, and mathematical examples are correct as stated. There is no remaining mathematical gap in either proof.** Publication should preserve positivity, integrality, global distinctness, and the exclusion of the trivial one-by-one case when saying that equality requires two rows.

## The exact target and its source

The [November 2002 source page](https://erich-friedman.github.io/mathmagic/1102.html), retrieved during this audit, defines SP matrices using positive integer entries that are all distinct, equal row sums, and equal column products. The equality-case question asks whether the common row sum can equal the common column product. The page attributes the two-row example and the conjecture that equality matrices have two rows to Joseph DeVincentis.

The [unsolved-problems list, item 8](https://erich-friedman.github.io/mathmagic/unsolved.html), also retrieved, continues to display that conjecture. Its abbreviated description omits hypotheses from the original definition; interpreting it in the original definition is essential. Without global distinctness, the supplied all-twos counterexample immediately disproves the abbreviated unrestricted wording.

The theorem proves precisely the missing higher-row nonexistence statement. It does not resolve every other extremal-size or smallest-entry question on the source page, and it does not prove that 840 is the smallest possible two-row common value. The note does not claim either of these additional results. The source page's continuing conjecture listing is evidence about that page, not a proof of worldwide historical priority.

## Reconstruction of the main proof

Assume a finite matrix has at least three rows, at least one column, distinct positive integer entries, row sums N, and column products N. Positive entries force N>0. Select any three rows; in column j call their entries x_j,y_j,z_j.

1. Every omitted factor is an integer at least one, so N >= x_j y_j z_j. This remains correct with no omitted factors, because the empty product is one. It does not require the selected submatrix itself to have common column products.
2. The selected rows have total sum 3N, hence the sum of (x_j+y_j+z_j)/N over columns is exactly 3.
3. Since each numerator is positive, replacing denominator N with the smaller positive number x_j y_j z_j increases the fraction. The resulting numerator divided by the product is exactly 1/(x_j y_j)+1/(x_j z_j)+1/(y_j z_j).
4. Set u=1/x, v=1/y, w=1/z. Expanding (u-v)^2+(u-w)^2+(v-w)^2 gives 2(u^2+v^2+w^2-uv-uw-vw). This proves the claimed identity and the direction of the second inequality. All denominators are nonzero.
5. Global distinctness ensures the selected entries form a set of positive integers. With M their maximum, its reciprocal-square sum is bounded above by the sum over all integers 1 through M. For k>=2, k(k-1)<=k^2 and both denominators are positive, so 1/k^2<=1/[k(k-1)]. The latter is exactly 1/(k-1)-1/k. The finite sum is 2-1/M<2. For M=1 the empty tail sum still gives the correct equality 1=2-1/M.
6. Combining the inequalities yields 3<=T<2, which is impossible.

No assumption about the size of N, the number of columns, factorization searches, convergence of an infinite series, or a numerical approximation is present. Distinctness is used only at the set-sum bound. The proof is even valid if only the selected three rows are mutually globally distinct and all other entries are positive integers.

The formal theorem restricts n>=2. The checkpoint correctly observes that the argument also works for n=1. This is a harmless stronger valid range, not a discrepancy.

## Stronger all-row proposition

For m>=3, fix a column b_1,...,b_m. Modulo m, positions i+1 and i+2 are distinct from each other and from i. Cancellation gives

    b_i / product_k b_k = 1 / product_(k!=i) b_k.

The denominator contains b_(i+1)b_(i+2), and every additional factor is at least one. Therefore this fraction is at most 1/[b_(i+1)b_(i+2)]. For positive u,v,

    1/(uv) <= (1/u^2+1/v^2)/2

follows by expanding (1/u-1/v)^2>=0. When i ranges over the m positions, each reciprocal square appears exactly once as the first shifted index and once as the second shifted index, both with coefficient 1/2. Thus

    sum_i b_i / product_k b_k <= sum_i 1/b_i^2.

Summing over columns with common product P yields (total of all entries)/P=mS/P. The same finite distinct-integer bound gives mS/P<2. Positivity of m and P justifies rearranging to S<2P/m. The argument is valid for m=3 and for n=1; the n=1 equal-row-sum, distinct-entry hypothesis is itself impossible when m>1, so that boundary is also vacuously consistent.

This proposition is mathematically stronger than the target: putting S=P would give m<2, incompatible with m>=3. Its proof is not circular and does not rely on the main theorem.

## Boundary cases and examples

- **Two rows:** I independently entered the displayed twenty entries. The two row sums are exactly 840; the ten column products are exactly 840; all entries are positive and distinct. The sum of their reciprocals, computed as an exact fraction, is 2. In general the displayed two-row identity is valid under equal row sums and common column products equal to the same N. It is not asserting an identity for arbitrary matrices.
- **Repeated entries:** A three-by-four matrix of twos has row sums 4*2=8 and column products 2^3=8. Its reciprocal-square sum is 12/4=3, so the distinct-integer packing step really does fail. This confirms the necessity of the stated distinctness hypothesis for the theorem in this form.
- **Ordinary SP control:** The rows (3,21), (14,10), (20,4) each sum to 24. The two column products are 3*14*20=840 and 21*10*4=840. All six entries are distinct. This is not an equality-case matrix.
- **Scaling:** Multiplication by c multiplies a row sum by c and a column product by c^m. Doubling the two-row control therefore gives sums 1680 and products 3360. No argument in the note tries to normalize S and P while retaining integral entries.
- **One row and at least two columns:** The column condition makes every entry N. Its row sum is nN>N, independently of distinctness. The note explicitly retains n>=2 when concluding that only two rows can work.
- **One by one:** Every single positive integer is trivially an equality-case matrix. This is outside the note's two-row classification because that sentence is explicitly conditioned on n>=2. Preserve this qualification in summaries.
- **One column and multiple rows:** Equal row sums would make all single entries equal, contradicting global distinctness. Thus no excluded larger one-column examples undermine the claim.
- **N=1 and entries equal to one:** Division by N is safe. The proof allows the integer one; it never assumes every entry exceeds one. Global distinctness permits at most one occurrence of one. No hidden failure occurs at that boundary.

## Computational and algebraic cross-checks

I independently ran Python `fractions.Fraction` checks on every column of lengths m=3,...,7 with each entry in {1,2,3,4}, allowing repeats. In every case both inequalities in the cyclic proof held exactly. I also independently checked the finite reciprocal-square bound for every M=1,...,512. These are transcription and edge-case checks, not the universal proof.

The audit's cleared-denominator identity is algebraically equivalent to the proof identity: multiplying twice the gap by x^2 y^2 z^2 yields

    2*(x^2*y^2+x^2*z^2+y^2*z^2-x*y*z*(x+y+z))
      = (x-y)^2*z^2+(x-z)^2*y^2+(y-z)^2*x^2.

The reported combinatorial counts are correct: 40^3=64,000 ordered triples; 2^12-1=4,095 nonempty subsets; 10*12*3=360 arrays; 10*3*(1+...+12)=2,340 columns. Numbers 10^100+3, 10^100+7, and 10^100+11 have 101 decimal digits, so the note is correct. The source-code comment calling them 100-digit entries is a minor comment typo, not a mathematical or test error.

The distinct-set regression uses cardinality k rather than maximum M in its bound 2-1/k. This is also valid: ordering distinct positive integers as a_1<...<a_k gives a_i>=i, hence sum 1/a_i^2<=sum_(i=1)^k 1/i^2<=2-1/k. It is stronger than the maximum-based bound printed in the proof and does not hide an incorrect test assertion.

The note's stated 33 checker tests and historical execution details are software/provenance claims; a separate reproduction audit should establish their execution. They are not premises for either mathematical proof. No assertion of a machine-checked proof is made.

## Publication recommendation and exact remaining limitations

Approve the mathematical result for publication with the original hypotheses visible. State that it resolves the **equal common sum/product conjecture** from the source page, rather than all questions posed there. Do not broaden it to repeated entries, arbitrary real entries, or the one-by-one boundary. No proof correction is required. Historical originality remains a separate literature question; the present audit validates the proof, not an absolute priority claim.

## Publication-page and alternate-proof checkpoint

Publication audit timestamp: 2026-09-17T03:46:44Z. The later publication audit examined `docs/papers/equal-sum-product/index.html`, its `docs/index.html` card, and `independent_audit/alternate_referee.md`. Completion estimate: **100%** for mathematical content and attribution review; deployment, rendering, and source-integrity checks remain separate operational tasks.

The public theorem, complete proof, cyclic stronger inequality, numerical controls, and boundary discussion are accurately transcribed. The page explicitly requires a single number shared by every row sum and every column product, preserves global distinctness and positive integers, and correctly isolates the trivial one-by-one case. Its DeVincentis attribution matches the source. Its explicit scope limitation avoids claiming resolution of every source-page question, and it does not claim established historical priority or external peer review. The homepage card correctly summarizes the equality-case theorem.

One wording correction was requested: the initial HTML meta description said “with equal row sums and column products,” which can be read as the weaker ordinary-SP condition. It should state that **every row sum and every column product equal the same number**, matching the visible lede. This is a metadata ambiguity, not a flaw in the visible proof. The parent agent was notified; this reviewer did not edit the website.

I independently checked the alternate referee's AM–GM derivation after completing my original review. With r=m-1, the geometric mean of the r quantities b_k^(-r), k different from i, is exactly the product of b_k^(-1). AM–GM therefore gives precisely the displayed inequality. Each reciprocal r-th power appears r times in the summed arithmetic means, so its total coefficient is one. For integer entries at least one and r>=2, replacing reciprocal r-th powers by reciprocal squares increases or preserves their values. The finite set bound then proves mS/P<2. This is correct, including m=3 and n=1. It is a distinct derivation within the same reciprocal-bound mechanism, as the alternate report accurately acknowledges.

The alternate report's separate n=2 check is also correct: among three rows, each has an entry at least N/2, and two such entries share a column. That column's product is at least N^2/4, forcing N<=4. Global distinctness of all 2m positive entries gives mN>=m(2m+1), hence N>=2m+1>=7, a contradiction. No mathematical objection remains to the alternate derivation or the visible publication content.

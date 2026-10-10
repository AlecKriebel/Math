# Primary-source scope and proof validation

## Source identity and conventions

The publisher's full Ohtsuki compilation, PDFp166/printedp538, has Problem12.14 and its explicit Livingston update. The imported extraction retained the question but omitted that update. Livingston's 2002 article calls it Problem12.1 of the then-cited collection; the identical Askitas wording and the final update settle this numbering difference.

Here g_s is the usual embedded four-ball genus and u_s the minimum total number of ordinary crossing changes to a slice knot, over all diagrams. The paper's later U_s=min max(positive changes,negative changes) is distinct. Neither its later conjectures nor generalized crossing changes are part of this queue target. The known negative answer applies to the source's usual slice category; the audit does not replace embedded slice disks by immersed or singular disks. The obstruction uses the necessary Alexander-polynomial and linking-metabolizer conditions in Theorem1.1, rather than a smooth-only Floer or gauge invariant.

Full primary sources:
- Ohtsuki compilation: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf , printed538, Update and reference266
- Livingston published article: https://msp.org/agt/2002/2-2/agt-v2-n2-p14-p.pdf , pp1051–1060; Theorems3.1/4.1 and Lemma4.2 are the key proof, Figure1 is the surgery setup

The pages containing the question/update, Figure1, and the quadratic-field step were visually inspected. The entire ten-page Livingston text was read, including its final addendum. Its addendum credits an earlier Murakami–Yasuhara8_16 example; the present correction does not claim Livingston was historically first. No PDFs or source images are redistributed in this packet.

## Checkable proof dependencies

The known genus-one Seifert surface and the nonsquare determinant15 give g_s(7_4)=1. Two ordinary crossing changes unknot it, so u_s<=2. The substantive published obstruction is to *any* one-crossing slicing, not merely to unknotting in a chosen drawing.

The surgery construction treats an arbitrary crossing disk. Livingston's infinite-cyclic-cover calculation gives a presentation matrix, with d(t)=4t-7+4/t,

[ -2t+3-2/t, 1, g(t) ]
[       1,  -2,   0  ]
[ g(1/t),    0, f(t) ].

Its determinant is f(t)d(t)+2g(t)g(1/t), and g(1)=0. If the changed knot J were slice, Fox–Milnor factorization would make that determinant ±H(t)H(1/t). The following arithmetic checks explain the decisive consequence d divides g; they do not substitute for the source's geometric derivation of the matrix.

Put F(t)=4t²-7t+4. It is primitive irreducible with discriminant-15. Its roots are alpha=(7+sqrt(-15))/8 and alpha-bar=(7-sqrt(-15))/8; they are inverses. In the field Q(sqrt(-15)), the slice factorization modulo F would imply norm(H(alpha)/g(alpha))=±2 if neither evaluation vanished. Writing a rational field element as (a+b sqrt(-15))/c with primitive integers would give a²+15b²=±2c². Modulo5, nonresiduosity of ±2 forces5|a,c. Modulo25 then forces5|b, contradicting primitivity. If H(alpha)=0, the same field identity already forces g(alpha)=0. Thus F divides g over Q[t,t^-1], and Gauss's lemma makes the divisibility integral. Combining it with g(1)=0 and F(1)=1 gives g=(t-1)Fh with integral Laurent h.

**Printed arithmetic typo:** the formula for alpha on p1057 has denominator4. The correct denominator is8. The source's field, conjugation and norm obstruction are unchanged by this correction. The checker verifies both that the /8 value is a reciprocal root and that the printed /4 value is not. The subsequent extra valuation display is unnecessary: the mod5/mod25 primitive-integer contradiction above already completes the norm step.

The even/odd coefficient sums of g are (g(1)±g(-1))/2. Since g(-1)=-30h(-1), both are multiples of15. The source's covering-link interpretation therefore makes the crossing lift null homologous in the lens space L(15,4); this is Theorem4.1.

Theorem3.1 supplies the incompatible consequence. With that lift null homologous, the branched-cover surgery has orthogonal linking forms4/15 and2/p. The order being a square would force p=epsilon*3^(2j+1)*5^(2k+1)*q² with q coprime30. Its5-primary group is Z5 plus Z_(5^(2k+1)), with diagonal values2/5 and epsilon*2*3^(2j+1)q²/5^(2k+1). An isotropic vector with a nonzero first coordinate can be rescaled to first coordinate1. Comparing5-adic valuations forces the second coordinate to be5^k times a unit. Reduction modulo5 would then make ±2 a square, impossible. Hence every isotropic element has first coordinate0 and second coordinate divisible by5^(k+1). Such elements form a group of order5^k, too small for the required metabolizer of order5^(k+1). This contradicts slicing.

These two published theorems consequently exclude every single crossing change to a slice knot. Together with the elementary genus and two-change bounds, they establish the cited g_s=1,u_s=2 counterexample. The source geometry is explicitly retained as a credited input, and the local calculations verify its algebraic steps rather than claiming a new surgery theorem.

## Prior campaign gate and disposition

Exact-ID all-state PR search, branch search and main attempt-path history returned no prior work for10400219. The upstream OPEN-TRIAGE item is not a campaign attempt. No new author proof turn was spent: this packet validates an existing complete published answer and the source's own status update. The correct disposition is already_solved0/5 after a separate reviewer confirms the source/category alignment and full proof. No arbitrary-gap conjecture, signed-invariant question, or classification is claimed resolved here.

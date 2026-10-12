# Independent acceptance of the full base-four obstruction

## Verdict and scope

**ACCEPT** the full [base-four theorem](FULL_QUATERNARY_OBSTRUCTION.md) within the precise scope below. This is the complete substantive independent mathematical and exact-computation review. Editorial changes remove only undistributed artifact identities and incidental coordination; the mathematical argument, every substantive check, arithmetic bounds and all negative-control outcomes are preserved. This is independent AI-assisted review, not external human peer review, journal acceptance or formal proof-assistant certification.

The accepted theorem excludes every base-four digit-multiplicative assignment, retaining every original partition factor, from having all total coefficients in \(\{-1,0,1\}\). This family contains the binary-digit family by pairing adjacent binary digit factors. It remains a restriction of the original independently signed coefficient array.

Degree 77 is the first empty **combined coefficient-and-Jensen frontier** for the specified exact search. It is not accepted as a sharp unconditional coefficient-prefix obstruction degree. The proof uses the bound one at all degrees. No novelty claim or unrestricted impossibility theorem is accepted.

Earlier accepted mathematical results retain their original scopes.

## 1. Root classification and exact lower mass

For \(a,b\in\{-1,1\}\), the four blocks

\[
C_{a,b}(z)=1+az+bz^2+abz^3=(1+az)(1+bz^2)
\]

have all roots on the unit circle. The other four blocks are

\[
D_{a,b}(z)=1+az+bz^2-abz^3.
\]

Let \(T\) be the real root greater than one of \(h(x)=x^3-x^2-x-1\). Its derivative is \((3x+1)(x-1)\), with critical values \(-22/27\) and \(-2\), so there is exactly one real root, in \((1,2)\). The conjugate pair has modulus \(T^{-1/2}\), since the three-root product is one.

For \(b=+1\), the defective blocks are \(-h(z)\) and its sign reflection; they have two inner roots of modulus \(T^{-1/2}\). For \(b=-1\), they are the reciprocal and reflected reciprocal polynomials; they have one inner root of modulus \(T^{-1}\). The sign and reciprocal identities were also checked exactly for every block.

After substituting \(z=q^l\), a defect contributes

\[
(\log T-lt)_+\quad(b=-1),\qquad
(\log T-2lt)_+\quad(b=+1)
\]

at \(r=e^{-t}\). The second expression already counts both inner roots and all lifted roots; it must not be doubled again. Thus one defect contributes one mass with effective weight \(l\) or \(2l\).

The rational lower bound \(R=1839/1000<T\) is rigorous: \(h(R)=-1568281/10^9<0\), and \(h\) increases above one. Replacing \(T\) by \(R\) only decreases the known zero mass. At each chosen rational radius, discarding weights with \(Rr^w\le1\) is consequently safe, including any equality case.

Local uniform product convergence follows from summability of the block deviations on compact disks. A sufficiently late tail is the exponential of a uniformly convergent sum of analytic logarithms, so it is nonvanishing. Coincident zeros add multiplicity, and unknown blocks cannot cancel known zeros. These facts justify using only the known defect masses as a lower bound for the full Jensen sum.

## 2. Parity bound and rational normalization

Every original factor has every coefficient congruent to one modulo two. Hence the total coefficient \(A_n\) obeys

\[
A_n\equiv p(n)\pmod2.
\]

Under the target alphabet, \(A_n^2=\pi_n\), where \(\pi_n=p(n)\bmod2\). In particular \(\pi_0=1\); the constant term is included in the norm bound.

Jensen, the logarithmic mean inequality, and Parseval therefore give

\[
J_P(r)\le\tfrac12\log\sum_{n\ge0}\pi_n r^{2n}.
\]

For \(J=512\), the certified upper envelope is

\[
U_r=\sum_{n=0}^{512}\pi_n r^{2n}+\frac{r^{1026}}{1-r^2}.
\]

The tail starts at index 513, not 512. No assertion about asymptotic partition parity is used.

The audit independently computed all 513 bits by direct product dynamic programming and compared them with a separately implemented pentagonal XOR recurrence. They agree exactly. The complete 513-bit comparison was performed; its raw record is not distributed here.

For \(r=a/b\), the audit computed \(U_r\) directly as a Python exact rational sum and compared it with the candidate's integer Horner formula at every one of the 21 radii. With \(X=a^2,Y=b^2\), that formula is exactly

\[
\frac{(Y-X)\sum_{n=0}^{512}\pi_nX^nY^{512-n}+X^{513}}
{Y^{512}(Y-X)}.
\]

Every comparison passed, and every envelope is at least one, as normalization requires.

If retained known defects have count \(K\) and weight sum \(S\), the necessary test is

\[
R^{2K}r^{2S}\le U_r.
\]

The independent verifier uses reduced rational upper envelopes and arbitrary-precision integer cross multiplication. It uses exact integer comparisons for positive weights and no logarithms, root approximations, floating-point arithmetic, or tolerance screen. Rejecting occurs only for a strict violation; equality is retained.

## 3. Binomial pools are sufficient as well as necessary

At original edge \(l\), there are \(d_l=1+v_4(l)\) base-four blocks. Its first binomial slots belong to pool \(l\), and its second slots to pool \(2l\). A pool has

\[
D_n=d_n+\mathbf1_{2\mid n}d_{n/2}=1+v_2(n)
\]

slots. Its positive-slot count \(C_n\) determines its entire cyclotomic baseline product.

An edge defect matrix has cells \(k_0,k_1,k_2,k_3\) for signs \((-,-),(-,+),(+,-),(+,+)\). Its total is at most \(d_l\). At pool \(l\), its first-slot demands must fit after subtracting the second-slot demands of the earlier edge \(l/2\). At pool \(2l\), its second-slot demands must fit the current sign inventory. The later edge \(2l\) will check its first-slot demands against these already consumed second slots.

These are sufficient constraints. To make the construction explicit, at a pool subtract all designated defect slots. The two residual component capacities are nonnegative by the individual edge capacities. Let them be \(A,B\), and let the remaining positive and negative inventories be \(P,M\). The pool inequalities give

\[
P,M\ge0,\qquad P+M=A+B.
\]

Allocate \(\min(P,A)\) positive signs to the first component and the remaining \(P-\min(P,A)\) to the second. The latter is between zero and \(B\). Fill the other slots with negative signs. This construction is independent at each pool.

At each original edge, first pair its reserved slots according to its four prescribed defect cells. The remaining first- and second-slot margins have the same total \(d_l-\sum_i k_i\), so an integer \(2\times2\) table pairs them into nondefective blocks. Their product depends only on the margins, not the table. Assign all resulting blocks to the original distinct labels. This gives a simultaneous global realization. No unrecorded pairing history is needed.

As a separate exact check, for group sizes one through five the audit enumerated every multiset of the eight original cubic types and compared its product to the margin/defect representation. The counts were respectively:

- 8 original multisets, 8 compressed classes
- 36 original multisets, 35 compressed classes
- 120 original multisets, 112 compressed classes
- 330 original multisets, 294 compressed classes
- 792 original multisets, 672 compressed classes

All legal compressed states occurred, and products agreed whenever a compression identified two states. This finite check supplements the general realization proof; it does not replace it.

## 4. Deferred recurrence and independent arithmetic

The state at degree \(N\) needs pool counts through \(N\) and finalized edge defects through \(\lfloor N/3\rfloor\). A defect ratio begins as

\[
D_{a,b}(q^l)/C_{a,b}(q^l)=1-2abq^{3l}+O(q^{4l}).
\]

Therefore, at \(N=3l\), its contribution to the new coefficient is

\[
-2(k_0-k_1-k_2+k_3).
\]

A fresh pool adds \(2C_N-D_N\), and all changes leave lower coefficients unchanged. Its endpoint pools \(l\) and \(2l\) have already been chosen. These facts prove the exact coefficient transition and its domains.

The producer uses direct polynomial multiplication with truncated ratio kernels. The audit uses formal logarithmic derivatives instead. For any primitive cubic \(B(x)=1+a x+b x^2+c x^3\), write

\[
xB'(x)/B(x)=\sum_{j\ge1}\ell_jx^j.
\]

Its coefficients are computed exactly from

\[
\ell_j=j[x^j]B-a\ell_{j-1}-b\ell_{j-2}-c\ell_{j-3},
\]

with nonpositive subscripts zero. Subtract the cyclotomic sequence from the defective sequence to obtain each correction. The coefficient at index three changes by \(-6ab\), so dilation by \(l\) changes the total log derivative in degree \(N=3l\) by \(-2Nab\).

The baseline pool at exponent \(m\) contributes \(m(2C_m-D_m)\) when the quotient \(N/m\) is odd and \(-mD_m\) when it is even. Add all finalized defect corrections over divisors, obtaining the residual log-derivative coefficient \(h_N^{(0)}\). Writing the earlier product coefficients as \(u_0=1,u_1,\ldots,u_{N-1}\), the residual is

\[
 A_N=\frac{h_N^{(0)}+\sum_{j=1}^{N-1}h_ju_{N-j}}{N}.
\]

Every division is checked to be integral. Every accepted new coefficient is additionally checked to square to the independently computed partition-parity bit. All arithmetic uses arbitrary-precision integers. No producer multiplication routine or ratio kernel is imported.

## 5. Every tree state is independently checked

The certificate is a complete ordered DFS tree, retaining every state's full history through its root path. The verifier first checks its structural grammar, legal byte domains, strictly ordered unique child keys, matched closing markers, and exact end of file. It then independently reconstructs every possible transition using the logarithmic recurrence and exact parity-Jensen tests, comparing each resulting child token and each complete child-list closing marker against the certificate stream.

Thus a missing or additional state is detected even if total counts were adjusted. This is a comparison of every state, not merely totals, prefix hashes, or aggregate diagnostics.

The exact results are:

- 11,151,089 states including the root
- 26,819,297 certificate bytes consumed, with no trailing data
- Largest frontier: 710,118 states at degree 54
- Degree 76: 2,708 states
- Degree 77: empty
- Jensen rejections: 9,107,474
- Coefficient rejections: 26,095,524
- Rejected/accepted cached weighted profiles: 70,639 / 15,992

Normal Python, `-O`, and `-OO` produce byte-identical complete reports, including all exact rational envelopes. No proof check depends on removable assertions.

Eight in-memory adversarial mutations are rejected:

1. Delete a complete feasible subtree
2. Duplicate a complete subtree
3. Give an invalid pool count
4. Give an invalid defect code
5. Close the root prematurely
6. Omit the final root-closing marker
7. Append trailing data
8. Insert a syntactically well-formed but infeasible leaf

The reviewed inputs were not modified. The compressed tree payload exactly matches the checked uncompressed tree, and the complete inputs and every summary field were authenticated. The raw tree and input inventories are not distributed here.

## 6. Fixed-width producer safety and separate replay

The producer's polynomial multiply-and-add operations use checked signed 128-bit intermediates before conversion to signed 64-bit values. A product of two 64-bit values plus a third 64-bit value fits 128-bit range, so the overflow check itself is safe. All cubic inverse recurrence updates also use this checked operation. Rational powers and comparisons use GMP integers.

The remaining coefficient-test expression is safe independently: canceling the designated binomial slots leaves a product of actual defective blocks and remaining binomial slots. Its monomial choices inject into ordinary partitions by base-four expansion. Every residual coefficient through degree 78 therefore has modulus at most \(p(78)=12,132,164\), independently computed by positive partition DP. The small transition corrections are far below the 64-bit limit. Pool sizes are at most seven; finalized edge capacities are at most three. The ordinary integer radius prefactors and counters are also within range.

The original C++ computation was separately compiled with

`-O2 -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all`

and replayed separately. Its entire tree and stdout log are byte-identical to the originals. Stderr contains only the eleven expected million-state progress lines, with no sanitizer errors. The independent arbitrary-precision reconstruction also establishes the output mathematics without depending on this fixed-width implementation.

## 7. Conclusion and independent reimplementation

A hypothetical globally valid base-four array induces a retained state at every degree: the grouping and pool domains include it, its coefficient passes the exact recurrence, and its known defects satisfy the necessary analytic inequalities. The complete empty frontier at degree 77 contradicts that implication. This proves the stated restricted-family theorem.

The historical reproduction used the complete retained tree, independent exact logarithmic-derivative verification in normal and both optimized modes, all eight mutation controls, structural checks and direct rational-envelope comparisons. The programs, raw tree, machine reports and source copies are not distributed in this appendix. Independent reimplementation can use the complete [theorem specification](FULL_QUATERNARY_OBSTRUCTION.md), including its 21 rational radii, parity recurrence, pool domains, exact coefficient transition, full frontier list and abstract ordered DFS encoding, together with the independent arithmetic recurrences proved above. The prose edition is not an executable public replay package.

No conclusion about the fully unrestricted sign problem, the sharp longest finite coefficient prefix, or general unboundedness of coefficients is included in this acceptance. Acceptance does not extend the theorem beyond its stated restricted family.

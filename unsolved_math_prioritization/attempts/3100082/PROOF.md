# A finite counterexample to parity restricted temporal unimodality

For the simple symmetric nearest-neighbour walk on the integer lattice, a fixed endpoint can have a strict valley in its occupation probability even after time is restricted to the reachable parity class. The following exact finite argument verifies the dimension-26 witness previously stated by Anonymous in *Counterexamples to the Cooper–Spencer temporal-unimodality conjecture*, version 1.0.0-candidate, 19 September 2026. That source describes itself as an unrefereed AI-assisted preprint. This is a reconstruction and independent arithmetic verification, with no novelty or external peer-review claim.

## Statement and scope

Let \(X_0=0\), and independently at each integer time choose one of the \(2d\) steps \(\pm e_1,\ldots,\pm e_d\), each with probability \(1/(2d)\). Define the occupation probability
\[
p_n(v)=\Pr(X_n=v).
\]
Cooper and Spencer's Conjecture 3 asks whether this probability is unimodal as a function of \(n\) on the parity class \(n\equiv\sum_i v_i\pmod2\). Here unimodality means nondecrease up to a mode followed by nonincrease; allowing plateaus or an entirely monotone sequence does not change the argument.

**Theorem.** In dimension \(d=26\), for \(v=(17,0,\ldots,0)\),
\[
p_{65}(v)>p_{67}(v)<p_{69}(v).
\]
Consequently the universal parity-restricted temporal-unimodality conjecture is false.

## Exhaustive counting

Let \(R_\ell(s)\) be the number of length-\(2s\) walks returning to the origin in \(\mathbb Z^\ell\), where the time order and each signed coordinate step are distinguished. Set
\[
R_0(0)=1,\qquad R_0(s)=0\quad(s>0).
\]
For \(\ell,s\ge0\),
\[
R_{\ell+1}(s)=\sum_{j=0}^{s}
 {2s\choose 2j}{2j\choose j}R_\ell(s-j). \tag{1}
\]
To prove (1), a returning walk must use the newly added coordinate \(j\) times in each direction. Choose its \(2j\) time positions, choose which \(j\) of those positions have positive sign, and fill the remaining positions, in their original order, with a returning walk in the other coordinates. Deleting the new-coordinate steps uniquely recovers these choices from any walk. Thus the construction is a bijection, including the boundary cases \(j=0\) and \(j=s\).

Let \(W_{m+2r}(d,m)\) count walks ending at \((m,0,\ldots,0)\), for \(d\ge1\), \(m,r\ge0\). Then
\[
W_{m+2r}(d,m)=\sum_{a=0}^{r}
 {m+2r\choose m+2a}{m+2a\choose a}R_{d-1}(r-a). \tag{2}
\]
Indeed, if the first coordinate has \(a\) negative steps, it has \(m+a\) positive steps, leaving \(2(r-a)\) steps that return in the remaining coordinates. The two binomial coefficients choose the first-coordinate time positions and their negative signs. Every walk gives exactly one value of \(a\) and exactly one such selection, so this is again a disjoint exhaustive count. There is no first-visit restriction.

Equations (1) and (2) are finite integer recurrences. Computing (1) for \(0\le\ell\le25\), \(0\le s\le26\) suffices for the three desired values: every right-hand index is between zero and its left-hand index. No omitted index can influence the result. This is exact truncation of a combinatorial recurrence, with no infinite-series approximation or error term.

## The finite certificate

With \(d=26\), \(m=17\), and \(r=24,25,26\), equations (1) and (2) give the following integers. Each displayed line is one integer.

\[
\begin{aligned}
W_{65}&=472771905154760476735080239062089851901956874836451641200273716209080628940936220800,\\
W_{67}&=1278150092304717629532379079186301753285243215753138416912978330730296859707833144726912,\\
W_{69}&=3456384842264444627112655114583494162563305352377408768216137840217183860729498596697993728.
\end{aligned}
\]

Independent enumeration by transverse coordinate-occupancy histograms and a squared-multinomial recurrence gives the same values; the accompanying audit explains these checks. Neither that implementation nor any exhaustive table is needed to state the certificate: (1), (2), and these three integers suffice to reproduce it.

There are \(52^n\) equiprobable length-\(n\) walks, so \(p_n(v)=W_n/52^n\). Since the compared times differ by two, the comparison factor is \(52^2=2704\). Direct integer subtraction gives
\[
2704W_{65}-W_{67}
=225139233754699559277887237589206257648173804626820892561797899057160948458396316288>0,
\]
\[
W_{69}-2704W_{67}
=266992672488156857102084463734221680007696980922488883444433922461152079517773356423680>0.
\]
Dividing the first difference by \(52^{67}\) and the second by \(52^{69}\) proves the two strict probability inequalities.

All three times are odd and at least 17, so they are genuinely reachable, not merely of the correct parity. For example, 17 positive first-coordinate steps followed by any appropriate number of cancelling pairs gives a walk of each length to the endpoint. The three times are consecutive members of the supported parity class.

Finally, a sequence that first does not decrease and then does not increase cannot contain such a valley. If its mode is at or after the middle index, the first inequality contradicts nondecrease; if its mode is before the middle index, the second contradicts nonincrease. Flat modes and entirely monotone sequences are excluded by the same strict inequalities. Initial zeros at odd times below 17 do not affect this obstruction. This proves the theorem.

## Attribution and limits

The witness, including the choice of dimension, endpoint, and times, was already present in the cited Anonymous preprint. The argument here certifies only this finite discrete-time witness and its consequence for the universal conjecture. It makes no claim about minimal counterexample dimension, the complete number of modes, a classification of endpoints, continuous time, an infinite family, historical priority, or formal proof-assistant verification. It does not refute Cooper and Spencer's deterministic-simulation theorem or their other two conjectures.

## References

1. J. N. Cooper and J. Spencer, *Simulating a Random Walk with Constant Error*, author manuscript (2004), Conjecture 3 on printed p. 8 and parity/occupation notation on printed p. 2. The inspected nine-page PDF is ordered backwards: these are physical pages 2 and 8. [Author-hosted manuscript](https://cs.nyu.edu/~spencer/papers/cooperjssubm.pdf).
2. J. Cooper, *Combinatorial Problems I Like*, Probability section, the Cooper/Spencer temporal-unimodality item. [Author problem list](https://people.math.sc.edu/cooper/combprob.html).
3. Anonymous, *Counterexamples to the Cooper–Spencer temporal-unimodality conjecture*, version 1.0.0-candidate, 19 September 2026, Theorem 1, Section 2, and Appendix A. [Evidence Press release](https://evidencepress.org/releases/cooper-spencer-temporal-unimodality/); [versioned PDF](https://raw.githubusercontent.com/ipitchford/cooper-spencer-temporal-unimodality/v1.0.0-candidate/paper/paper.pdf); [release tag](https://github.com/ipitchford/cooper-spencer-temporal-unimodality/releases/tag/v1.0.0-candidate). The inspected tag identifies commit `95678898ede180f04d6b416e605faa73aed58196`.

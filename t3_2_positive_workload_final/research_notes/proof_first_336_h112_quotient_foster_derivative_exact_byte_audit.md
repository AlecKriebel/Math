# Derivative exact-byte audit of the anisotropic 336 quotient theorem

**Independent hostile replay, 2026-08-12 PDT.**  The immutable target is

~~~text
research_notes/proof_first_336_h112_quotient_foster_theorem.md
SHA-256 9206aa2b07aa802e4d06a769b3b60d520b2dbd12752312497aa5b41156780d48
414 lines / 15,620 bytes
~~~

The verdict is **STRICT PASS**.  This audit independently replayed the
quotient algebra, rare-source Bellman recursion, all-nonrare geometry,
physical-time tiling, and recurrence interface.  It also compared the
derivative against the previously audited mathematical freeze

~~~text
62f5995bdd2915745468652bcb8ae891ca744a9e94f607f6bf38fbb63a397718
~~~

The derivative changes only the layout of (1.1), the layout of (1.2), and
an equivalent compression of the final finite-return/scope paragraphs.  No
load-bearing formula, hypothesis, episode, or conclusion changed.

## 1. Marked identities and quotient signs

At an actual marked state \((x,t)\), \(x\ge t\), so

\[
 F(x,t)=\sum_i\log((x_i-t_i)!)\ge0
\]

is defined.  A reaction \(e:y\to u\) gives the exact cancellation

\[
 F(x+u-y,u)-F(x,t)=\log{(x)_t\over(x)_y}.
\]

Source averaging yields the displayed entropy identity (2.3) and
\(D(x,t)\le\log p_t+C\).  With
\(V=H+\epsilon F/(H+1)\), direct subtraction gives (3.1).  On a birth
the denominator correction is nonpositive.  On a death it is

\[
 {\epsilon F'\over H(H+1)}=O(\log H/H)=o(1),
\]

and is absorbed into half of the favorable unit workload decrement.  A
zero-source birth has probability \(O(H^{-1})\).  Along a bounded path,
denominator replacement costs only \(O(\log H/H^2)\).  Thus the
quotient lift has no uncharged positive logarithmic toll.

## 2. Rare-source branch

Every designated path retains all clocks, stops at the actual endpoint of
the first competitor, and takes one final ordinary jump after terminal
success.  Hence its exact recursion is

\[
 J_i=D_i+a_iJ_{i+1},\qquad a_i=\alpha_i p_{y_i},\qquad
 \alpha_i\ge\alpha_*>0.
\]

The scalar bounds (5.3) are valid because, once the continuation value is
negative, replacing \(\alpha_i\) by the smaller \(\alpha_*\) increases
the upper bound.  Iterating through any fixed path length still tends to
\(-\infty\) as the terminal source probability tends to zero.  The
finite path menu therefore supplies one \(A(\delta)\uparrow\infty\).

The global hazard satisfies \(\Lambda\ge c(H+1)\).  A lower-linkage
mark uses terminal source zero, whose probability is \(O(H^{-1})\).
Every rare episode has bounded jump count and expected physical duration
\(O(H^{-1})\).  Choosing \(\delta\) after \(\epsilon\) makes its negative
\(\epsilon J/H\) contribution dominate births and a fixed positive
physical-time toll.

## 3. All-nonrare branch and repaired hazard transport

For a top mark \(t\), the success endpoint of a path to \(c\) is
\(z_c=x-t+c\).  If every \(p_c(z_c)>\delta\), the unary source
\(C\) gives

\[
 C(x)=\Theta(H),\qquad \Lambda(z_C)=O(H).
\]

For a bounded integer displacement \(b\), the correct comparison is

\[
 \Lambda(w+b)\le C_b\{\Lambda(w)+H(w)+1\}.               \tag{3.1}
\]

The linear remainder is necessary because a bounded shift can activate a
mixed or double source on a face.  Equation (3.1) transports the
\(O(H)\) hazard at \(z_C\) to every \(z_q\).  Together with
\(p_q(z_q)>\delta\) and the global lower hazard, it gives

\[
                         (z_q)_q=\Theta(H)\qquad(q\in Q). \tag{3.2}
\]

Each of the three cores \(\{2A,2B\}\), \(\{2A,A+B\}\), and
\(\{2B,A+B\}\) therefore forces

\[
                         A=\Theta(\sqrt H),\qquad
                         B=\Theta(\sqrt H).                 \tag{3.3}
\]

This covers all four possible \(Q\)-supports.  Strong connectivity of
the lower graph makes at least one of \(A,B\) a direct-death source, for
every orientation.  Thus \(\mathcal LH\le-c\sqrt H\), while
\(\Lambda(x)=\Theta(H)\).  One ordinary all-clock jump consequently
satisfies

\[
 \mathbb E\Delta V\le-{c\over\sqrt H}+{C\over H},\qquad
 \mathbb E\tau\le {C\over H}.                         \tag{3.4}
\]

The negative \(H^{-1/2}\) term dominates both quotient and duration
costs.  A coordinate face either enters the rare branch or is itself forced
by (3.2)--(3.3) into this square-root regime, so no face is omitted.

## 4. Physical-time composition

The state-selected menu is finite.  Every episode includes a physical jump,
every competitor endpoint and target are actual, and the endpoint mark
immediately selects the next rule.  The common potential is nonnegative and
proper.  On a finite \(V\)-sublevel there are finitely many marked starts,
and every episode has bounded jump count and bounded displacement; this
supplies the positive-endpoint integrability needed for localized
conditional summation.

The stopped inequality yields

\[
       \eta\,\mathbb E S_{n\wedge N_K\wedge\sigma_R}\le V(y).
\]

Nonnegativity and Fatou remove the sublevel localization.  If \(K\) is
not hit, the episode endpoints contain infinitely many genuine jump times;
nonexplosion forces their times to diverge, contradicting the bound.
Therefore \(\mathbb E_y\tau_K\le V(y)/\eta\).  A finite mean return
to the finite marked set gives a finite invariant occupation measure;
irreducibility and projection of the finite mark prove positive recurrence
of the physical class.

## 5. Exact-byte and render replay

The target hash, line count, byte count, and absence of hidden control bytes
were recomputed.  The exact Markdown was converted independently with
Pandoc's single-backslash TeX-math reader to MathJax HTML and to LaTeX.
Tectonic produced a seven-page letter-size PDF with zero overfull or
underfull diagnostics.  All seven pages were inspected; the two split
opening displays, equation tags, theorem block, and final scope paragraph
are legible and unbroken, with no orphan page.

**Frozen verdict: STRICT PASS.**  Concatenating the following two lines gives
the target SHA-256:

~~~text
9206aa2b07aa802e4d06a769b3b60d520
b2dbd12752312497aa5b41156780d48
~~~

# Exact purity filter on the nonsmooth Ky--Fan-four locus

## Theorem

Let \(z\) be a unit three-qutrit tensor.  Write the distinct paired squared
singular values of the skew matrix \(D_z\) as

\[
 \lambda_1\ge\lambda_2\ge\cdots\ge\lambda_{13}\ge0.
\]

Suppose the Ky--Fan-four boundary is nonsmooth,

\[
 \lambda_2=\lambda_3,
\]

and is a strict DTH violation,

\[
 \lambda_1+\lambda_2>{1\over4}.
\]

Then

\[
\boxed{P_{\rm loc}(z)>{57\over31}.}
\tag{1}

## Proof

Put \(x=\lambda_1\).  The sharp leading-pair theorem gives
\(x\le1/6\), while \(\lambda_1\ge\lambda_2\) and the violation give
\(x>1/8\).  On the violation boundary, convexity minimizes the squared
spectrum by setting

\[
 \lambda_2=\lambda_3={1\over4}-x
\]

and distributing the remaining pair trace equally over the last ten
entries:

\[
 \lambda_4=\cdots=\lambda_{13}={x\over10}.
\]

The ordering constraint is automatic on \(x\in[1/8,1/6]\).  Hence every
strict violation satisfies

\[
\begin{aligned}
 \operatorname{Tr}(D_z^\dagger D_z)^2
 &>2\left[x^2+2\left({1\over4}-x\right)^2+{x^2\over10}\right]\\
 &\ge {11\over124}.
\end{aligned}
\tag{2}

The quadratic on the first line has its minimum at \(x=5/31\), which lies
in the required interval.  Finally, the exact output-purity identity

\[
 \operatorname{Tr}(D_z^\dagger D_z)^2={1+P_{\rm loc}(z)\over32}
\]

turns (2) into

\[
 P_{\rm loc}(z)>32{11\over124}-1={57\over31}.
\]

This proves (1). \(\square\)

This theorem covers the fourth/fifth-eigenvalue degeneracy excluded from
the smooth Euler analysis.  It is a necessary filter, not an exclusion of
the remaining high-purity locus.

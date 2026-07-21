#!/usr/bin/env node
/**
 * Exact, dependency-free JavaScript check of the four exported certificates.
 *
 * This implementation deliberately shares no arithmetic or polynomial code
 * with the Python verifiers. Rational real and imaginary parts are represented
 * by normalized BigInt fractions.
 */

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));

function abs(value) {
  return value < 0n ? -value : value;
}

function gcd(left, right) {
  let a = abs(left);
  let b = abs(right);
  while (b !== 0n) {
    [a, b] = [b, a % b];
  }
  return a;
}

function rat(numerator, denominator = 1n) {
  if (denominator === 0n) throw new Error("zero denominator");
  if (numerator === 0n) return { n: 0n, d: 1n };
  const sign = denominator < 0n ? -1n : 1n;
  const common = gcd(numerator, denominator);
  return { n: sign * numerator / common, d: abs(denominator) / common };
}

function parseRat(source) {
  const parts = source.split("/");
  return rat(BigInt(parts[0]), parts.length === 2 ? BigInt(parts[1]) : 1n);
}

function ratAdd(left, right) {
  return rat(left.n * right.d + right.n * left.d, left.d * right.d);
}

function ratSub(left, right) {
  return rat(left.n * right.d - right.n * left.d, left.d * right.d);
}

function ratMul(left, right) {
  return rat(left.n * right.n, left.d * right.d);
}

function ratEqual(left, right) {
  return left.n === right.n && left.d === right.d;
}

const ZERO_RAT = rat(0n);
const ONE_RAT = rat(1n);

function complex(real = ZERO_RAT, imag = ZERO_RAT) {
  return { r: real, i: imag };
}

function parseComplex(source) {
  return complex(parseRat(source.real), parseRat(source.imag));
}

function cAdd(left, right) {
  return complex(ratAdd(left.r, right.r), ratAdd(left.i, right.i));
}

function cSub(left, right) {
  return complex(ratSub(left.r, right.r), ratSub(left.i, right.i));
}

function cMul(left, right) {
  return complex(
    ratSub(ratMul(left.r, right.r), ratMul(left.i, right.i)),
    ratAdd(ratMul(left.r, right.i), ratMul(left.i, right.r)),
  );
}

function cScale(integer, value) {
  const scalar = rat(BigInt(integer));
  return complex(ratMul(scalar, value.r), ratMul(scalar, value.i));
}

function cPow(value, exponent) {
  let result = complex(ONE_RAT, ZERO_RAT);
  let base = value;
  let power = exponent;
  while (power > 0) {
    if (power % 2 === 1) result = cMul(result, base);
    base = cMul(base, base);
    power = Math.floor(power / 2);
  }
  return result;
}

function cEqual(left, right) {
  return ratEqual(left.r, right.r) && ratEqual(left.i, right.i);
}

function vectorEqual(left, right) {
  return left.length === right.length && left.every((value, index) => cEqual(value, right[index]));
}

function assert(condition, message) {
  if (!condition) throw new Error(`certificate check failed: ${message}`);
}

function load(relativePath) {
  return JSON.parse(readFileSync(join(ROOT, relativePath), "utf8"));
}

function gradient(terms, point, dimension) {
  const result = Array.from({ length: dimension }, () => complex());
  for (const term of terms) {
    const coefficient = parseComplex(term.coefficient);
    for (const [variable, exponent] of term.powers) {
      let value = cScale(exponent, coefficient);
      for (const [factor, factorExponent] of term.powers) {
        value = cMul(value, cPow(point[factor], factorExponent - Number(factor === variable)));
      }
      result[variable] = cAdd(result[variable], value);
    }
  }
  return result;
}

function hessianAtOrigin(terms, dimension) {
  const result = Array.from(
    { length: dimension },
    () => Array.from({ length: dimension }, () => complex()),
  );
  for (const term of terms) {
    const totalDegree = term.powers.reduce((sum, [, exponent]) => sum + exponent, 0);
    if (totalDegree !== 2) continue;
    const coefficient = parseComplex(term.coefficient);
    if (term.powers.length === 1) {
      const [variable, exponent] = term.powers[0];
      assert(exponent === 2, "malformed quadratic square");
      result[variable][variable] = cAdd(result[variable][variable], cScale(2, coefficient));
    } else {
      assert(term.powers.length === 2, "malformed quadratic cross-term");
      const [first, firstExponent] = term.powers[0];
      const [second, secondExponent] = term.powers[1];
      assert(firstExponent === 1 && secondExponent === 1, "malformed quadratic exponents");
      result[first][second] = cAdd(result[first][second], coefficient);
      result[second][first] = cAdd(result[second][first], coefficient);
    }
  }
  return result;
}

function main() {
  const symmetric = load("output/symmetric_potential_sparse.json");
  const symmetricCollision = load("output/symmetric_collision.json");
  const quartic = load("output/potential_sparse.json");
  const quarticCollision = load("output/collision.json");

  assert(symmetric.field === "Q(i)", "six-variable field");
  assert(symmetric.degree === 8, "six-variable degree");
  assert(symmetric.number_of_terms === 204 && symmetric.terms.length === 204, "six-variable term count");
  assert(symmetric.variables.length === 6, "six-variable dimension");
  assert(JSON.stringify(symmetricCollision.variables) === JSON.stringify(symmetric.variables), "six-variable labels");

  const symmetricPoints = symmetricCollision.points.map((point) => point.map(parseComplex));
  assert(symmetricPoints.length === 3, "three-point fiber size");
  assert(!vectorEqual(symmetricPoints[0], symmetricPoints[1]), "first two points are distinct");
  assert(!vectorEqual(symmetricPoints[0], symmetricPoints[2]), "first and third points are distinct");
  assert(!vectorEqual(symmetricPoints[1], symmetricPoints[2]), "last two points are distinct");
  const symmetricImages = symmetricPoints.map((point) => gradient(symmetric.terms, point, 6));
  assert(vectorEqual(symmetricImages[0], symmetricImages[1]), "first six-variable collision equality");
  assert(vectorEqual(symmetricImages[0], symmetricImages[2]), "second six-variable collision equality");

  const hessian = hessianAtOrigin(symmetric.terms, 6);
  for (let row = 0; row < 6; row += 1) {
    for (let column = 0; column < 6; column += 1) {
      const expected = complex(row === column ? ONE_RAT : ZERO_RAT, ZERO_RAT);
      assert(cEqual(hessian[row][column], expected), "identity linear part");
    }
  }

  assert(quartic.field === "Q(i)", "quartic field");
  assert(quartic.degree === 4, "quartic degree");
  assert(quartic.number_of_terms === 538 && quartic.terms.length === 538, "quartic term count");
  assert(quartic.variables.length === 44, "quartic dimension");
  assert(
    quartic.terms.every((term) => term.powers.reduce((sum, [, exponent]) => sum + exponent, 0) === 4),
    "quartic homogeneity",
  );
  assert(JSON.stringify(quarticCollision.variables) === JSON.stringify(quartic.variables), "quartic labels");

  const quarticPoints = quarticCollision.points.map((point) => point.map(parseComplex));
  assert(quarticPoints.length === 2 && !vectorEqual(quarticPoints[0], quarticPoints[1]), "distinct quartic points");
  const quarticImages = quarticPoints.map((point) => {
    const derivative = gradient(quartic.terms, point, 44);
    return point.map((value, index) => cSub(value, derivative[index]));
  });
  assert(vectorEqual(quarticImages[0], quarticImages[1]), "quartic collision equality");

  console.log("Independent Node.js BigInt certificate checks passed:");
  console.log("  degree-8 potential in 6 variables with 204 terms");
  console.log("  identity linear part and exact Q(i) three-point gradient fiber");
  console.log("  homogeneous quartic in 44 variables with 538 terms");
  console.log("  two distinct exact Q(i)-points collide under Z-gradient(P)");
}

main();

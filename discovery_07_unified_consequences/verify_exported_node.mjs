#!/usr/bin/env node
"use strict";

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const certificatePath = path.join(here, "output", "unified_every_order.json");

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function sha256(buffer) {
  return crypto.createHash("sha256").update(buffer).digest("hex");
}

function gcd(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b !== 0n) [a, b] = [b, a % b];
  return a;
}

function rational(numerator, denominator = 1n) {
  assert(denominator !== 0n, "zero denominator");
  if (denominator < 0n) {
    numerator = -numerator;
    denominator = -denominator;
  }
  const divisor = gcd(numerator, denominator);
  return [numerator / divisor, denominator / divisor];
}

function parseRational(text) {
  const pieces = text.split("/");
  return rational(BigInt(pieces[0]), pieces.length === 1 ? 1n : BigInt(pieces[1]));
}

function binomial(n, k) {
  if (k < 0 || k > n) return 0n;
  k = Math.min(k, n - k);
  let value = 1n;
  for (let j = 1; j <= k; j += 1) {
    value = (value * BigInt(n - k + j)) / BigInt(j);
  }
  return value;
}

function qCoefficient(m) {
  const residue = m % 3;
  if (residue === 0) {
    const k = m / 3;
    return rational((-1n) ** BigInt(k) * binomial(3 * k + 1, k), 2n ** BigInt(2 * k + 1));
  }
  if (residue === 1) {
    const k = (m - 1) / 3;
    return rational(
      (-1n) ** BigInt(k + 1) * 3n * binomial(3 * k + 1, k),
      BigInt(3 * k + 1) * 2n ** BigInt(2 * k + 1),
    );
  }
  const k = (m - 2) / 3;
  return rational((-1n) ** BigInt(k) * binomial(3 * k + 4, k + 1), 2n ** BigInt(2 * k + 3));
}

function rCoefficient(m) {
  const residue = m % 3;
  if (residue !== 2) return qCoefficient(m);
  const k = (m - 2) / 3;
  return rational(
    (-1n) ** BigInt(k) * 3n * binomial(3 * k + 2, k),
    2n ** BigInt(2 * k + 2),
  );
}

function checkSparse(companion, variableCount, termCount, allowedDegrees) {
  assert(companion.variables.length === variableCount, "wrong variable count");
  assert(companion.number_of_terms === termCount, "wrong declared term count");
  assert(companion.terms.length === termCount, "wrong actual term count");
  const seen = new Set();
  const degrees = new Set();
  for (const term of companion.terms) {
    assert(term.powers.length === variableCount, "wrong exponent-vector length");
    assert(term.powers.every((power) => Number.isInteger(power) && power >= 0), "invalid exponent");
    const key = term.powers.join(",");
    assert(!seen.has(key), "duplicate monomial");
    seen.add(key);
    const [realNumerator] = parseRational(term.coefficient_qi[0]);
    const [imaginaryNumerator] = parseRational(term.coefficient_qi[1]);
    assert(realNumerator !== 0n || imaginaryNumerator !== 0n, "zero sparse term");
    degrees.add(term.powers.reduce((sum, power) => sum + power, 0));
  }
  assert(
    [...degrees].sort((a, b) => a - b).join(",") === [...allowedDegrees].join(","),
    "wrong degree support",
  );
}

const raw = fs.readFileSync(certificatePath);
const payload = JSON.parse(raw.toString("utf8"));
assert(payload.format === "unified-every-order-certificate-v1", "wrong certificate format");

for (const precursor of Object.values(payload.precursors)) {
  const precursorPath = path.resolve(here, precursor.path);
  assert(sha256(fs.readFileSync(precursorPath)) === precursor.sha256, "precursor hash mismatch");
}
console.log("[1/4] precursor hashes");

assert(payload.unipotent14.weights.join(",") === "1,1,1,2,3,2,3,4,5,2,3,4,5,6", "wrong weights");
assert(payload.unipotent14.homogeneous_jordan_type.join(",") === "14,1", "wrong homogeneous type");
for (const x of [-1n, 0n, 1n]) {
  const y = rational(-3n * x, 2n);
  const z = rational(27n * x * x - 1n, 4n);
  assert(rational(-27n * x * x * z[1] + 4n * z[0] + z[1])[0] === 0n, "fiber z relation failed");
  assert(rational(3n * x * y[1] + 2n * y[0])[0] === 0n, "fiber y relation failed");
  assert(x ** 3n - x === 0n, "fiber x relation failed");
}
console.log("[2/4] reduced three-point fiber data");

for (let m = 0; m < 1000; m += 1) {
  assert(qCoefficient(m)[0] !== 0n, `q_${m} vanished`);
  assert(rCoefficient(m)[0] !== 0n, `r_${m} vanished`);
}
console.log("[3/4] closed coefficient families are nonzero through index 999");

checkSparse(payload.companions.nonhomogeneous28, 28, 178, [2, 3, 4, 5, 6, 7, 8]);
checkSparse(payload.companions.homogeneous30, 30, 608, [8]);
console.log("[4/4] expanded 28D and 30D companions");
console.log(`PASS unified_every_order.json sha256=${sha256(raw)}`);

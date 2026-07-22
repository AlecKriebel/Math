#!/usr/bin/env node
// Independent exact BigInt-rational checker for the exported SIC(21) witness.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const payload = JSON.parse(
  fs.readFileSync(path.join(here, "output", "sic21_sparse.json"), "utf8"),
);

function gcd(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b !== 0n) [a, b] = [b, a % b];
  return a;
}

class Q {
  constructor(n, d = 1n) {
    if (d === 0n) throw new Error("zero denominator");
    if (d < 0n) [n, d] = [-n, -d];
    const common = gcd(n, d);
    this.n = n / common;
    this.d = d / common;
  }
  static parse(value) {
    const [n, d = "1"] = value.toString().split("/");
    return new Q(BigInt(n), BigInt(d));
  }
  add(other) { return new Q(this.n * other.d + other.n * this.d, this.d * other.d); }
  sub(other) { return new Q(this.n * other.d - other.n * this.d, this.d * other.d); }
  mul(other) { return new Q(this.n * other.n, this.d * other.d); }
  div(other) { return new Q(this.n * other.d, this.d * other.n); }
  neg() { return new Q(-this.n, this.d); }
  pow(exponent) {
    let result = ONE;
    let base = this;
    let power = exponent;
    while (power > 0) {
      if (power & 1) result = result.mul(base);
      base = base.mul(base);
      power >>= 1;
    }
    return result;
  }
  equals(other) { return this.n === other.n && this.d === other.d; }
  get zero() { return this.n === 0n; }
  toString() { return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`; }
}

const ZERO = new Q(0n);
const ONE = new Q(1n);

function evaluate(terms, point) {
  let answer = ZERO;
  for (const term of terms) {
    let value = Q.parse(term.coefficient);
    term.powers.forEach((exponent, index) => {
      value = value.mul(point[index].pow(exponent));
    });
    answer = answer.add(value);
  }
  return answer;
}

function derivativeValue(terms, variableIndex, point) {
  let answer = ZERO;
  for (const term of terms) {
    const exponent = term.powers[variableIndex];
    if (exponent === 0) continue;
    let value = Q.parse(term.coefficient).mul(new Q(BigInt(exponent)));
    term.powers.forEach((power, index) => {
      value = value.mul(point[index].pow(power - (index === variableIndex ? 1 : 0)));
    });
    answer = answer.add(value);
  }
  return answer;
}

function determinant(input) {
  const matrix = input.map((row) => row.slice());
  let result = ONE;
  for (let column = 0; column < matrix.length; column += 1) {
    let pivot = column;
    while (pivot < matrix.length && matrix[pivot][column].zero) pivot += 1;
    if (pivot === matrix.length) return ZERO;
    if (pivot !== column) {
      [matrix[pivot], matrix[column]] = [matrix[column], matrix[pivot]];
      result = result.neg();
    }
    const pivotValue = matrix[column][column];
    result = result.mul(pivotValue);
    for (let j = column; j < matrix.length; j += 1) {
      matrix[column][j] = matrix[column][j].div(pivotValue);
    }
    for (let row = column + 1; row < matrix.length; row += 1) {
      const factor = matrix[row][column];
      if (factor.zero) continue;
      for (let j = column; j < matrix.length; j += 1) {
        matrix[row][j] = matrix[row][j].sub(factor.mul(matrix[column][j]));
      }
    }
  }
  return result;
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

assert(payload.format === "sic21-sparse-certificate-v1", "format");
assert(payload.g.length === 21 && payload.A.length === 72, "dimensions/support");
assert(payload.g.reduce((sum, component) => sum + component.length, 0) === 72, "g support");

const points = payload.collision_points.map((point) => point.map(Q.parse));
const common = payload.common_image.map(Q.parse);
assert(points.map((point) => point[0].toString()).join(",") === "0,1,-1", "first coordinates");
for (const point of points) {
  const mapped = payload.g.map((component, index) => point[index].add(evaluate(component, point)));
  assert(mapped.every((value, index) => value.equals(common[index])), "collision");
}
console.log("[1/2] Node BigInt: exact three-point collision and separating coordinate");

const scalarValues = [-2, -1, 0, 1, 2, 3].map((value) => new Q(BigInt(value)));
for (const point of points) {
  const jacobian = payload.g.map((component) =>
    Array.from({ length: 21 }, (_, column) => derivativeValue(component, column, point)),
  );
  for (const scalar of scalarValues) {
    const matrix = Array.from({ length: 21 }, (_, row) =>
      Array.from({ length: 21 }, (_, column) =>
        (row === column ? ONE : ZERO).add(scalar.mul(jacobian[row][column])),
      ),
    );
    assert(determinant(matrix).equals(ONE), "determinant pencil");
  }
}
console.log("[2/2] Node BigInt: 18 exact determinant-pencil specializations");
console.log("All independent Node checks passed.");


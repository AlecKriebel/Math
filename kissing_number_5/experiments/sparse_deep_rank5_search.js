#!/usr/bin/env node
/*
Numerical search for rank-five realizations of the classified 23/24-edge
deep graphs, restricted only by making each isolated K2 exactly antipodal.

This is discovery code, not a verifier or certificate.  It has no package
dependencies and uses deterministic xorshift seeds plus a Riemannian Adam
descent on a log-sum-exp approximation to the largest graph-cell violation.
*/
"use strict";

const DIM = 5;
const STRICT_MARGIN = 1e-6;

function rngFor(seed) {
  let state = (seed >>> 0) || 0x9e3779b9;
  return function rng() {
    state ^= state << 13;
    state ^= state >>> 17;
    state ^= state << 5;
    return (state >>> 0) / 4294967296;
  };
}

function gaussian(rng) {
  const u = Math.max(rng(), 1e-15);
  const v = rng();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

function dot(a, b) {
  let value = 0;
  for (let d = 0; d < DIM; d++) value += a[d] * b[d];
  return value;
}

function normalize(row) {
  const norm = Math.sqrt(dot(row, row));
  for (let d = 0; d < DIM; d++) row[d] /= norm;
}

function d5Lines() {
  const rows = [];
  const scale = 1 / Math.sqrt(2);
  for (let i = 0; i < DIM; i++) {
    for (let j = i + 1; j < DIM; j++) {
      for (const sign of [1, -1]) {
        const row = Array(DIM).fill(0);
        row[i] = scale;
        row[j] = sign * scale;
        rows.push(row);
      }
    }
  }
  return rows;
}

function graphSpec(kind) {
  if (kind === "e23_c5") {
    const edges = [];
    for (let i = 0; i < 5; i++) edges.push([i, (i + 1) % 5]);
    return {kind, pairs: 18, core: 5, edges};
  }
  if (kind === "e24_c7") {
    const edges = [];
    for (let i = 0; i < 7; i++) edges.push([i, (i + 1) % 7]);
    return {kind, pairs: 17, core: 7, edges};
  }
  if (kind === "e24_c5_tail2") {
    const edges = [];
    for (let i = 0; i < 5; i++) edges.push([i, (i + 1) % 5]);
    edges.push([0, 5], [5, 6]);
    return {kind, pairs: 17, core: 7, edges};
  }
  if (kind === "e24_c5_p4") {
    const edges = [];
    for (let i = 0; i < 5; i++) edges.push([i, (i + 1) % 5]);
    edges.push([5, 6], [6, 7], [7, 8]);
    return {kind, pairs: 16, core: 9, edges};
  }
  throw new Error(`unknown graph kind ${kind}`);
}

function edgeKey(i, j) {
  return i < j ? `${i}:${j}` : `${j}:${i}`;
}

function constraints(rows, spec, withGradient) {
  const edgeSet = new Set(spec.edges.map(([i, j]) => edgeKey(i, j)));
  const records = [];
  function add(i, j, sign, offset, type) {
    records.push({
      value: sign * dot(rows[i], rows[j]) + offset,
      i, j, sign, type,
    });
  }

  // The first `pairs` rows represent exact antipodal pairs.  Absolute inner
  // products between their lines, and between a line and a core point, must
  // be at most 1/2.
  for (let i = 0; i < spec.pairs; i++) {
    for (let j = i + 1; j < spec.pairs; j++) {
      add(i, j, 1, -0.5, "base_upper");
      add(i, j, -1, -0.5, "base_lower");
    }
    for (let a = 0; a < spec.core; a++) {
      const j = spec.pairs + a;
      add(i, j, 1, -0.5, "cross_upper");
      add(i, j, -1, -0.5, "cross_lower");
    }
  }

  for (let a = 0; a < spec.core; a++) {
    for (let b = a + 1; b < spec.core; b++) {
      const i = spec.pairs + a;
      const j = spec.pairs + b;
      add(i, j, 1, -0.5, "core_upper");
      if (edgeSet.has(edgeKey(a, b))) {
        add(i, j, 1, 0.5 + STRICT_MARGIN, "deep_required");
      } else {
        add(i, j, -1, -0.5, "nondeep_required");
      }
    }
  }
  return records;
}

function objectiveGradient(rows, spec, beta) {
  const records = constraints(rows, spec, true);
  let maximum = -Infinity;
  for (const record of records) maximum = Math.max(maximum, record.value);
  const weights = [];
  let total = 0;
  for (const record of records) {
    const weight = Math.exp(beta * (record.value - maximum));
    weights.push(weight);
    total += weight;
  }
  const gradient = rows.map(() => Array(DIM).fill(0));
  for (let k = 0; k < records.length; k++) {
    const record = records[k];
    const weight = weights[k] / total;
    for (let d = 0; d < DIM; d++) {
      gradient[record.i][d] += weight * record.sign * rows[record.j][d];
      gradient[record.j][d] += weight * record.sign * rows[record.i][d];
    }
  }
  for (let i = 0; i < rows.length; i++) {
    const radial = dot(gradient[i], rows[i]);
    for (let d = 0; d < DIM; d++) {
      gradient[i][d] -= radial * rows[i][d];
    }
  }
  return {
    objective: maximum + Math.log(total) / beta,
    trueMaximum: maximum,
    gradient,
    records,
  };
}

function initialRows(spec, seed) {
  const rng = rngFor(seed);
  const source = d5Lines();
  // A deterministic seed-dependent partial shuffle.
  for (let i = source.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [source[i], source[j]] = [source[j], source[i]];
  }
  const rows = source.slice(0, spec.pairs).map(row => row.slice());
  for (let a = 0; a < spec.core; a++) {
    const row = Array.from({length: DIM}, () => gaussian(rng));
    normalize(row);
    rows.push(row);
  }
  // Deliberately break the root-system symmetry.
  const noiseScale = 0.01 + 0.04 * (seed % 5);
  for (const row of rows) {
    for (let d = 0; d < DIM; d++) row[d] += noiseScale * gaussian(rng);
    normalize(row);
  }
  return rows;
}

function optimize(spec, seed, stepsPerStage) {
  const rows = initialRows(spec, seed);
  const firstMoment = rows.map(() => Array(DIM).fill(0));
  const secondMoment = rows.map(() => Array(DIM).fill(0));
  let iteration = 0;
  let best = {value: Infinity, rows: null, active: null};
  const stages = [
    [12, 0.018],
    [35, 0.012],
    [100, 0.007],
    [300, 0.0035],
    [900, 0.0018],
    [2700, 0.0009],
  ];
  for (const [beta, learningRate] of stages) {
    for (let step = 0; step < stepsPerStage; step++) {
      iteration++;
      const state = objectiveGradient(rows, spec, beta);
      if (state.trueMaximum < best.value) {
        best = {
          value: state.trueMaximum,
          rows: rows.map(row => row.slice()),
          active: state.records
            .filter(record => record.value >= state.trueMaximum - 1e-5)
            .map(record => record.type),
        };
      }
      for (let i = 0; i < rows.length; i++) {
        for (let d = 0; d < DIM; d++) {
          const g = state.gradient[i][d];
          firstMoment[i][d] = 0.9 * firstMoment[i][d] + 0.1 * g;
          secondMoment[i][d] = 0.999 * secondMoment[i][d] + 0.001 * g * g;
          const mhat = firstMoment[i][d] / (1 - Math.pow(0.9, iteration));
          const vhat = secondMoment[i][d] / (1 - Math.pow(0.999, iteration));
          rows[i][d] -= learningRate * mhat / (Math.sqrt(vhat) + 1e-8);
        }
        normalize(rows[i]);
      }
    }
  }
  return {
    kind: spec.kind,
    seed,
    representatives: spec.pairs + spec.core,
    fullPoints: 2 * spec.pairs + spec.core,
    maximumViolation: best.value,
    feasible: best.value <= 0,
    strictMargin: STRICT_MARGIN,
    activeTypes: best.active,
    representativeCoordinates: best.rows,
  };
}

function main() {
  const args = process.argv.slice(2);
  const kinds = args.length ? args : [
    "e23_c5", "e24_c7", "e24_c5_tail2", "e24_c5_p4",
  ];
  const seedCount = Number(process.env.SEEDS || 8);
  const steps = Number(process.env.STEPS || 1800);
  const output = {
    status: "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE",
    restriction: "isolated K2 components are imposed as exact antipodal pairs",
    seedCount,
    stepsPerStage: steps,
    runs: [],
  };
  for (const kind of kinds) {
    const spec = graphSpec(kind);
    let best = null;
    for (let seed = 1; seed <= seedCount; seed++) {
      const result = optimize(spec, 1000 * (kinds.indexOf(kind) + 1) + seed, steps);
      if (best === null || result.maximumViolation < best.maximumViolation) {
        best = result;
      }
      process.stderr.write(
        `${kind} seed=${seed} violation=${result.maximumViolation.toFixed(10)}\n`
      );
    }
    output.runs.push(best);
  }
  process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
}

main();

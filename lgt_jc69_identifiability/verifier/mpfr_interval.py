#!/usr/bin/env python3
"""Minimal outward-rounded interval arithmetic backed by MPFR via ctypes.

This module intentionally avoids Python float arithmetic in all certified
operations.  Decimal literals are interpreted as exact finite decimals and
then rounded outward by MPFR.
"""
from __future__ import annotations

import ctypes
import ctypes.util
from dataclasses import dataclass
from typing import Iterable, Sequence

# MPFR's public ABI for a scalar.  This layout is stable for MPFR 4.x on
# platforms where GMP limbs are unsigned long (Linux x86_64 in the verifier
# environment).  The shared library itself owns the significand storage.
class _MPFRStruct(ctypes.Structure):
    _fields_ = [
        ("_mpfr_prec", ctypes.c_long),
        ("_mpfr_sign", ctypes.c_int),
        ("_mpfr_exp", ctypes.c_long),
        ("_mpfr_d", ctypes.POINTER(ctypes.c_ulong)),
    ]

_libname = ctypes.util.find_library("mpfr") or "libmpfr.so.6"
_lib = ctypes.CDLL(_libname)
_PTR = ctypes.POINTER(_MPFRStruct)

# Rounding modes from mpfr.h.
RNDN, RNDZ, RNDU, RNDD, RNDA = 0, 1, 2, 3, 4

# Function signatures used below.
_lib.mpfr_init2.argtypes = [_PTR, ctypes.c_long]
_lib.mpfr_init2.restype = None
_lib.mpfr_clear.argtypes = [_PTR]
_lib.mpfr_clear.restype = None
_lib.mpfr_set.argtypes = [_PTR, _PTR, ctypes.c_int]
_lib.mpfr_set.restype = ctypes.c_int
_lib.mpfr_set_str.argtypes = [_PTR, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
_lib.mpfr_set_str.restype = ctypes.c_int
_lib.mpfr_set_si.argtypes = [_PTR, ctypes.c_long, ctypes.c_int]
_lib.mpfr_set_si.restype = ctypes.c_int
_lib.mpfr_add.argtypes = [_PTR, _PTR, _PTR, ctypes.c_int]
_lib.mpfr_add.restype = ctypes.c_int
_lib.mpfr_sub.argtypes = [_PTR, _PTR, _PTR, ctypes.c_int]
_lib.mpfr_sub.restype = ctypes.c_int
_lib.mpfr_mul.argtypes = [_PTR, _PTR, _PTR, ctypes.c_int]
_lib.mpfr_mul.restype = ctypes.c_int
_lib.mpfr_div.argtypes = [_PTR, _PTR, _PTR, ctypes.c_int]
_lib.mpfr_div.restype = ctypes.c_int
_lib.mpfr_neg.argtypes = [_PTR, _PTR, ctypes.c_int]
_lib.mpfr_neg.restype = ctypes.c_int
_lib.mpfr_exp.argtypes = [_PTR, _PTR, ctypes.c_int]
_lib.mpfr_exp.restype = ctypes.c_int
_lib.mpfr_log.argtypes = [_PTR, _PTR, ctypes.c_int]
_lib.mpfr_log.restype = ctypes.c_int
_lib.mpfr_sqrt.argtypes = [_PTR, _PTR, ctypes.c_int]
_lib.mpfr_sqrt.restype = ctypes.c_int
_lib.mpfr_cmp.argtypes = [_PTR, _PTR]
_lib.mpfr_cmp.restype = ctypes.c_int
_lib.mpfr_get_d.argtypes = [_PTR, ctypes.c_int]
_lib.mpfr_get_d.restype = ctypes.c_double

PREC_BITS = 384


class MP:
    __slots__ = ("v", "_cleared")

    def __init__(self, precision: int = PREC_BITS):
        self.v = _MPFRStruct()
        self._cleared = False
        _lib.mpfr_init2(ctypes.byref(self.v), precision)

    def clear(self) -> None:
        if not self._cleared:
            _lib.mpfr_clear(ctypes.byref(self.v))
            self._cleared = True

    def __del__(self):  # pragma: no cover - cleanup at interpreter exit
        try:
            self.clear()
        except Exception:
            pass

    @classmethod
    def from_str(cls, text: str, rnd: int) -> "MP":
        z = cls()
        rc = _lib.mpfr_set_str(ctypes.byref(z.v), text.encode("ascii"), 10, rnd)
        if rc == 0 or rc in (-1, 1):
            return z
        z.clear()
        raise ValueError(f"MPFR could not parse {text!r}")

    @classmethod
    def from_int(cls, n: int) -> "MP":
        z = cls()
        _lib.mpfr_set_si(ctypes.byref(z.v), int(n), RNDN)
        return z

    def copy(self, rnd: int = RNDN) -> "MP":
        z = MP()
        _lib.mpfr_set(ctypes.byref(z.v), ctypes.byref(self.v), rnd)
        return z

    def to_float_down(self) -> float:
        return float(_lib.mpfr_get_d(ctypes.byref(self.v), RNDD))

    def to_float_up(self) -> float:
        return float(_lib.mpfr_get_d(ctypes.byref(self.v), RNDU))

    def cmp(self, other: "MP") -> int:
        return int(_lib.mpfr_cmp(ctypes.byref(self.v), ctypes.byref(other.v)))


def _binop(a: MP, b: MP, fn, rnd: int) -> MP:
    z = MP()
    fn(ctypes.byref(z.v), ctypes.byref(a.v), ctypes.byref(b.v), rnd)
    return z


def mp_add(a: MP, b: MP, rnd: int) -> MP:
    return _binop(a, b, _lib.mpfr_add, rnd)


def mp_sub(a: MP, b: MP, rnd: int) -> MP:
    return _binop(a, b, _lib.mpfr_sub, rnd)


def mp_mul(a: MP, b: MP, rnd: int) -> MP:
    return _binop(a, b, _lib.mpfr_mul, rnd)


def mp_div(a: MP, b: MP, rnd: int) -> MP:
    return _binop(a, b, _lib.mpfr_div, rnd)


def mp_neg(a: MP, rnd: int) -> MP:
    z = MP()
    _lib.mpfr_neg(ctypes.byref(z.v), ctypes.byref(a.v), rnd)
    return z


def mp_exp(a: MP, rnd: int) -> MP:
    z = MP()
    _lib.mpfr_exp(ctypes.byref(z.v), ctypes.byref(a.v), rnd)
    return z


def mp_log(a: MP, rnd: int) -> MP:
    z = MP()
    _lib.mpfr_log(ctypes.byref(z.v), ctypes.byref(a.v), rnd)
    return z


def mp_sqrt(a: MP, rnd: int) -> MP:
    z = MP()
    _lib.mpfr_sqrt(ctypes.byref(z.v), ctypes.byref(a.v), rnd)
    return z


def _min_mp(values: Sequence[MP]) -> MP:
    best = values[0]
    for v in values[1:]:
        if v.cmp(best) < 0:
            best = v
    out = best.copy(RNDD)
    for v in values:
        v.clear()
    return out


def _max_mp(values: Sequence[MP]) -> MP:
    best = values[0]
    for v in values[1:]:
        if v.cmp(best) > 0:
            best = v
    out = best.copy(RNDU)
    for v in values:
        v.clear()
    return out


@dataclass
class Interval:
    lo: MP
    hi: MP

    def __post_init__(self):
        if self.lo.cmp(self.hi) > 0:
            raise ValueError("invalid interval: lower endpoint exceeds upper endpoint")

    @classmethod
    def decimal(cls, text: str) -> "Interval":
        return cls(MP.from_str(text, RNDD), MP.from_str(text, RNDU))

    @classmethod
    def fraction(cls, num: int, den: int = 1) -> "Interval":
        if den == 0:
            raise ZeroDivisionError
        a = MP.from_int(num)
        b = MP.from_int(den)
        lo = mp_div(a, b, RNDD)
        hi = mp_div(a, b, RNDU)
        a.clear(); b.clear()
        if den < 0:
            lo, hi = hi, lo
        return cls(lo, hi)

    @classmethod
    def from_bounds(cls, lo_text: str, hi_text: str) -> "Interval":
        return cls(MP.from_str(lo_text, RNDD), MP.from_str(hi_text, RNDU))

    @classmethod
    def zero(cls) -> "Interval":
        return cls.fraction(0)

    @classmethod
    def one(cls) -> "Interval":
        return cls.fraction(1)

    def copy(self) -> "Interval":
        return Interval(self.lo.copy(RNDD), self.hi.copy(RNDU))

    def contains_zero(self) -> bool:
        z = MP.from_int(0)
        ans = self.lo.cmp(z) <= 0 and self.hi.cmp(z) >= 0
        z.clear()
        return ans

    def strictly_positive(self) -> bool:
        z = MP.from_int(0)
        ans = self.lo.cmp(z) > 0
        z.clear()
        return ans

    def strictly_negative(self) -> bool:
        z = MP.from_int(0)
        ans = self.hi.cmp(z) < 0
        z.clear()
        return ans

    def strict_subset_of(self, other: "Interval") -> bool:
        return self.lo.cmp(other.lo) > 0 and self.hi.cmp(other.hi) < 0

    def disjoint(self, other: "Interval") -> bool:
        return self.hi.cmp(other.lo) < 0 or other.hi.cmp(self.lo) < 0

    def __neg__(self) -> "Interval":
        return Interval(mp_neg(self.hi, RNDD), mp_neg(self.lo, RNDU))

    def __add__(self, other) -> "Interval":
        other = as_interval(other)
        return Interval(mp_add(self.lo, other.lo, RNDD), mp_add(self.hi, other.hi, RNDU))

    __radd__ = __add__

    def __sub__(self, other) -> "Interval":
        other = as_interval(other)
        return Interval(mp_sub(self.lo, other.hi, RNDD), mp_sub(self.hi, other.lo, RNDU))

    def __rsub__(self, other) -> "Interval":
        return as_interval(other).__sub__(self)

    def __mul__(self, other) -> "Interval":
        other = as_interval(other)
        lows = [
            mp_mul(self.lo, other.lo, RNDD),
            mp_mul(self.lo, other.hi, RNDD),
            mp_mul(self.hi, other.lo, RNDD),
            mp_mul(self.hi, other.hi, RNDD),
        ]
        highs = [
            mp_mul(self.lo, other.lo, RNDU),
            mp_mul(self.lo, other.hi, RNDU),
            mp_mul(self.hi, other.lo, RNDU),
            mp_mul(self.hi, other.hi, RNDU),
        ]
        return Interval(_min_mp(lows), _max_mp(highs))

    __rmul__ = __mul__

    def __truediv__(self, other) -> "Interval":
        other = as_interval(other)
        if other.contains_zero():
            raise ZeroDivisionError("interval denominator contains zero")
        lows = [
            mp_div(self.lo, other.lo, RNDD),
            mp_div(self.lo, other.hi, RNDD),
            mp_div(self.hi, other.lo, RNDD),
            mp_div(self.hi, other.hi, RNDD),
        ]
        highs = [
            mp_div(self.lo, other.lo, RNDU),
            mp_div(self.lo, other.hi, RNDU),
            mp_div(self.hi, other.lo, RNDU),
            mp_div(self.hi, other.hi, RNDU),
        ]
        return Interval(_min_mp(lows), _max_mp(highs))

    def __rtruediv__(self, other) -> "Interval":
        return as_interval(other).__truediv__(self)

    def exp(self) -> "Interval":
        return Interval(mp_exp(self.lo, RNDD), mp_exp(self.hi, RNDU))

    def log(self) -> "Interval":
        if not self.strictly_positive():
            raise ValueError("log requires a strictly positive interval")
        return Interval(mp_log(self.lo, RNDD), mp_log(self.hi, RNDU))

    def sqrt(self) -> "Interval":
        z = MP.from_int(0)
        if self.lo.cmp(z) < 0:
            z.clear()
            raise ValueError("sqrt requires a nonnegative interval")
        z.clear()
        return Interval(mp_sqrt(self.lo, RNDD), mp_sqrt(self.hi, RNDU))

    def pow(self, exponent) -> "Interval":
        exponent = as_interval(exponent)
        return (exponent * self.log()).exp()

    def approx(self) -> tuple[float, float]:
        return self.lo.to_float_down(), self.hi.to_float_up()

    def __repr__(self) -> str:
        a, b = self.approx()
        return f"[{a:.18e}, {b:.18e}]"


def as_interval(value) -> Interval:
    if isinstance(value, Interval):
        return value
    if isinstance(value, int):
        return Interval.fraction(value)
    if isinstance(value, str):
        return Interval.decimal(value)
    raise TypeError(f"cannot convert {type(value).__name__} to Interval")


@dataclass
class Jet:
    val: Interval
    der: list[Interval]

    @classmethod
    def constant(cls, val, n: int = 3) -> "Jet":
        return cls(as_interval(val), [Interval.zero() for _ in range(n)])

    @classmethod
    def variable(cls, val: Interval, index: int, n: int = 3) -> "Jet":
        d = [Interval.zero() for _ in range(n)]
        d[index] = Interval.one()
        return cls(val, d)

    def _coerce(self, other) -> "Jet":
        if isinstance(other, Jet):
            return other
        return Jet.constant(other, len(self.der))

    def __neg__(self):
        return Jet(-self.val, [-d for d in self.der])

    def __add__(self, other):
        other = self._coerce(other)
        return Jet(self.val + other.val, [a + b for a, b in zip(self.der, other.der)])

    __radd__ = __add__

    def __sub__(self, other):
        other = self._coerce(other)
        return Jet(self.val - other.val, [a - b for a, b in zip(self.der, other.der)])

    def __rsub__(self, other):
        return self._coerce(other).__sub__(self)

    def __mul__(self, other):
        other = self._coerce(other)
        return Jet(
            self.val * other.val,
            [a * other.val + self.val * b for a, b in zip(self.der, other.der)],
        )

    __rmul__ = __mul__

    def reciprocal(self):
        one = Interval.one()
        val = one / self.val
        return Jet(val, [-(d / (self.val * self.val)) for d in self.der])

    def __truediv__(self, other):
        other = self._coerce(other)
        return self * other.reciprocal()

    def __rtruediv__(self, other):
        return self._coerce(other).__truediv__(self)

    def exp(self):
        val = self.val.exp()
        return Jet(val, [val * d for d in self.der])

    def log(self):
        return Jet(self.val.log(), [d / self.val for d in self.der])

    def pow(self, exponent):
        exponent = self._coerce(exponent)
        return (exponent * self.log()).exp()


def interval_dot(row: Sequence[Interval], col: Sequence[Interval]) -> Interval:
    acc = Interval.zero()
    for a, b in zip(row, col):
        acc = acc + a * b
    return acc


def interval_matmul(A: Sequence[Sequence[Interval]], B: Sequence[Sequence[Interval]]) -> list[list[Interval]]:
    nr, nk, nc = len(A), len(B), len(B[0])
    if any(len(row) != nk for row in A) or any(len(row) != nc for row in B):
        raise ValueError("matrix shape mismatch")
    return [[interval_dot(A[i], [B[k][j] for k in range(nk)]) for j in range(nc)] for i in range(nr)]


def interval_matvec(A: Sequence[Sequence[Interval]], x: Sequence[Interval]) -> list[Interval]:
    return [interval_dot(row, x) for row in A]


def det3(A: Sequence[Sequence[Interval]]) -> Interval:
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def identity3() -> list[list[Interval]]:
    return [[Interval.one() if i == j else Interval.zero() for j in range(3)] for i in range(3)]

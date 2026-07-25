"""Proof-oriented synthesis for the order-12, parameter-three slice."""

from .encoding import (
    K3Encoding,
    build_k3_encoding,
    same_color_cut,
    validate_decoded_candidate,
)

__all__ = [
    "K3Encoding",
    "build_k3_encoding",
    "same_color_cut",
    "validate_decoded_candidate",
]

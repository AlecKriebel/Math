#!/bin/sh
# Deliberately fake GP used only to test that the strict wrapper fails closed.

case "${AUDIT_CONIC_DOUBLE_COVER_FAKE_MODE:-pass}" in
    pass)
        printf '%s\n' "AUDIT_CONIC_DOUBLE_COVER_PARI_PASS_7E4A91"
        exit 0
        ;;
    diagnostic)
        printf '%s\n' "*** injected GP diagnostic"
        printf '%s\n' "AUDIT_CONIC_DOUBLE_COVER_PARI_PASS_7E4A91"
        exit 0
        ;;
    extra)
        printf '%s\n' "AUDIT_CONIC_DOUBLE_COVER_PARI_PASS_7E4A91"
        printf '%s\n' "injected trailing output"
        exit 0
        ;;
    nonzero)
        printf '%s\n' "AUDIT_CONIC_DOUBLE_COVER_PARI_PASS_7E4A91"
        exit 42
        ;;
    *)
        exit 64
        ;;
esac

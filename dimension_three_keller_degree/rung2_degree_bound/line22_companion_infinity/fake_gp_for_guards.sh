#!/bin/sh

sentinel='PASS: independent PARI line-(2,2) companion-at-infinity certificate'

case "${FAKE_GP_MODE:-wrong}" in
    good)
        printf '%s\n' "$sentinel"
        ;;
    diagnostic)
        printf '%s\n' '*** forged GP diagnostic'
        printf '%s\n' "$sentinel"
        ;;
    extra)
        printf '%s\n' 'unexpected extra output'
        printf '%s\n' "$sentinel"
        ;;
    badstatus)
        printf '%s\n' "$sentinel"
        exit 7
        ;;
    wrong)
        printf '%s\n' 'wrong sentinel'
        ;;
esac

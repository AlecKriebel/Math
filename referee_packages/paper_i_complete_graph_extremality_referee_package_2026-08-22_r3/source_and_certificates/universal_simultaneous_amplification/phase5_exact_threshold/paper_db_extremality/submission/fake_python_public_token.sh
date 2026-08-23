#!/bin/sh

# A deliberately non-Python executable used only by the package's hostile
# negative control.  The internal replay must reject the PYTHON override before
# this public token can be printed.
printf '%s\n' PAPER1_EXECUTION_SAFETY_OK
exit 0

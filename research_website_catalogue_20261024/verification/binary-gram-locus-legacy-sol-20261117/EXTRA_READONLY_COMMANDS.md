# Additional literal fixed-object reads

Both commands completed exit 0; their literal stdout and empty stderr are retained under the names below. They read existing Git objects only and ran before the closing full native guard. No link in the wrapper was followed.

`/usr/bin/git --no-optional-locks -c core.hooksPath=/dev/null -c core.fsmonitor=false -C /Users/alec/Documents/Math diff --no-ext-diff --no-textconv --raw --no-abbrev a4ce3c37dad209339e490d18dcced6c48cf912d2 674c6b9f9b296dd7a18dac4eec87b4ace840ccd5 -- docs`

Outputs: NATIVE_RELEASED_DOCS_DIFF.stdout.txt and NATIVE_RELEASED_DOCS_DIFF.stderr.txt. The thirteen modifications are retained literally. This is a successful raw data comparison, not a science execution.

`/usr/bin/git --no-optional-locks -c core.hooksPath=/dev/null -c core.fsmonitor=false -C /Users/alec/Documents/Math show 674c6b9f9b296dd7a18dac4eec87b4ace840ccd5:docs/papers/s-tc-jc-sharp-boundary/index.html`

Outputs: RELEASED_STC_WRAPPER.html and RELEASED_STC_WRAPPER.stderr.txt. The complete wrapper was personally read as an identity comparison with the native/physical candidate article.

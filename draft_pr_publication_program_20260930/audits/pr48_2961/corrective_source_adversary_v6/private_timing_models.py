"""Independent small chronology/type models; never loads proposed sources."""
import datetime as dt
import json
import os
import sys

UTC = dt.timezone.utc
started = dt.datetime.now(UTC).isoformat()
rows = []

def parse_literal(value):
    if type(value) is not str or value != value.strip():
        raise ValueError('literal UTC string required')
    result = dt.datetime.fromisoformat(value[:-1] + '+00:00' if value.endswith('Z') else value)
    if result.tzinfo is None or result.utcoffset() != dt.timedelta(0):
        raise ValueError('aware zero-offset UTC required')
    return result

def prefix_tail(initial, phases):
    last = parse_literal(initial)
    for start, finish in phases:
        begin, end = parse_literal(start), parse_literal(finish)
        if not last <= begin <= end:
            raise ValueError('unordered actual prefix')
        last = end
    return last

def author_model(last, epoch, push_finished):
    return last <= parse_literal(epoch) and parse_literal(push_finished) <= parse_literal(epoch)

def caller_model(last, epoch):
    return last <= parse_literal(epoch)

def check(label, expected, action):
    try:
        result = action()
        observed = result is not False
        failure = None
    except (ValueError, TypeError) as exc:
        observed, failure = False, type(exc).__name__
    rows.append(dict(label=label, expected_acceptance=expected, observed_acceptance=observed, rejection_type=failure))
    if observed is not expected:
        raise AssertionError(label)

zero = '2026-10-03T13:14:00+00:00'
push = '2026-10-03T13:15:00+00:00'
first = ('2026-10-03T18:20:00Z', '2026-10-03T18:21:00Z')
second = ('2026-10-03T18:22:00+00:00', '2026-10-03T18:23:00+00:00')
for role, phases, epoch in [
    ('finalize', [], '2026-10-03T18:20:00Z'),
    ('mirror', [first], '2026-10-03T18:22:00Z'),
    ('post', [first, second], '2026-10-03T18:24:00Z'),
]:
    last = prefix_tail(zero, phases)
    check(role + ': prefix returns aware UTC datetime', True, lambda: type(last) is dt.datetime and last.utcoffset() == dt.timedelta(0))
    check(role + ': corrected author and caller consume prefix datetime', True, lambda: author_model(last, epoch, push) and caller_model(last, epoch))
    check(role + ': adapter validates prefix without parsing datetime again', True, lambda: prefix_tail(zero, phases) == last)

last = prefix_tail(zero, [first, second])
check('M5 old author reparses datetime and fails', False, lambda: parse_literal(last))
check('equality boundary remains valid', True, lambda: author_model(last, last.isoformat(), push))
check('prefix later than epoch is rejected', False, lambda: author_model(last, '2026-10-03T18:22:59Z', push))
check('push later than epoch is rejected', False, lambda: author_model(last, '2026-10-03T18:24:00Z', '2026-10-03T18:24:01Z'))
check('reversed next-phase chronology is rejected', False, lambda: prefix_tail(zero, [first, ('2026-10-03T18:20:59Z', '2026-10-03T18:23:00Z')]))
check('reversed child interval is rejected', False, lambda: prefix_tail(zero, [('2026-10-03T18:22:00Z', '2026-10-03T18:21:00Z')]))
for label, value in [('datetime', last), ('boolean', True), ('integer', 0), ('naive string', '2026-10-03T18:24:00'), ('nonzero offset', '2026-10-03T18:24:00+01:00'), ('whitespace', ' 2026-10-03T18:24:00Z '), ('malformed string', 'not a timestamp')]:
    check('unchanged strict string parser rejects ' + label, False, lambda value=value: parse_literal(value))
check('direct naive datetime comparison cannot pass', False, lambda: author_model(dt.datetime(2026, 10, 3), '2026-10-03T18:24:00Z', push))

print(json.dumps(dict(schema='pr48-v6-independent-private-typeflow-models/v1', status='PASS_PRIVATE_MODELS_ONLY', actual_pid=os.getpid(), argv=sys.argv, started_utc=started, finished_utc=dt.datetime.now(UTC).isoformat(), controls=rows, count=len(rows), proposed_or_production_import_compile_execute=False, native_Git_remote_ROOT_mutation=False), indent=2, sort_keys=True))

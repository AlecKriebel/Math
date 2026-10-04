"""First-party handwritten time-type models only; no proposed source loading."""
import datetime as dt,json
def literal_utc(value):
 if type(value) is not str or value!=value.strip():raise ValueError('string UTC only')
 parsed=dt.datetime.fromisoformat(value[:-1]+'+00:00' if value.endswith('Z') else value)
 if parsed.tzinfo is None or parsed.utcoffset()!=dt.timedelta(0):raise ValueError('aware zero-offset only')
 return parsed
rows=[]
def record(name,fn,expected):
 try:value=fn();got='ACCEPT' if value else 'REJECT';error=None
 except (ValueError,TypeError) as e:got='REJECT';error=type(e).__name__
 if got!=expected:raise ValueError((name,got,expected))
 rows.append(dict(name=name,outcome=got,expected=expected,error_type=error))
utc=dt.timezone.utc;last=dt.datetime(2026,10,3,17,54,45,tzinfo=utc)
for role in ['finalize','mirror','post']:
 record(role+'_aware_prefix_before_epoch',lambda:last<=literal_utc('2026-10-03T17:54:46+00:00'),'ACCEPT')
 record(role+'_equal_boundary',lambda:last<=literal_utc('2026-10-03T17:54:45Z'),'ACCEPT')
 record(role+'_reversed_boundary',lambda:last<=literal_utc('2026-10-03T17:54:44+00:00'),'REJECT')
record('old_M5_datetime_reparse_reproduced',lambda:literal_utc(last),'REJECT')
record('naive_epoch_refused',lambda:last<=literal_utc('2026-10-03T17:54:46'),'REJECT')
record('nonUTC_epoch_refused',lambda:last<=literal_utc('2026-10-03T18:54:46+01:00'),'REJECT')
record('whitespace_epoch_refused',lambda:last<=literal_utc(' 2026-10-03T17:54:46Z'),'REJECT')
record('bool_epoch_refused',lambda:last<=literal_utc(True),'REJECT')
record('datetime_epoch_refused',lambda:last<=literal_utc(last),'REJECT')
record('naive_prefix_refused',lambda:dt.datetime(2026,10,3,17,54,45)<=literal_utc('2026-10-03T17:54:46Z'),'REJECT')
record('string_prefix_is_not_datetime',lambda:'2026-10-03T17:54:45Z'<=literal_utc('2026-10-03T17:54:46Z'),'REJECT')
print(json.dumps(dict(schema='pr48-V6-private-time-type-model-results/v1',status='PASS_PRIVATE_MODELS_ONLY',assertions=len(rows),rows=rows,proposed_or_production_imported_compiled_executed=False,mathematical_credit=0),sort_keys=True))

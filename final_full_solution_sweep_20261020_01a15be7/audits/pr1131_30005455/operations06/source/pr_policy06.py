"""Bounded explicit known-PR references; every match is a reconciliation lead."""
if not globals().get('_OPS06_VERIFIED',False):raise RuntimeError('Use verified06 bootstrap')
import re,unicodedata

LABEL=re.compile(r'(?<!\w)(?:pr|pull\s+request)\s*(?::\s*)?(?:#\s*)?(?P<number>[0-9]+)(?!\w|\.[0-9])')
URL=re.compile(r'(?<!\w)https?://(?:www\.)?github\.com/aleckriebel/math/pull/(?P<number>[0-9]+)(?!\w|\.[0-9])')
BASE=re.compile(r'30005455|12697708|warm|whisker|reinforced.{0,10}graph|forest.{0,12}(?:bound|threshold)',re.I)
def normalize(text,decode):
    return ''.join(c for c in unicodedata.normalize('NFKD',decode(text)).casefold()
                   if unicodedata.category(c)!='Cf')
def known_pr(text,decode):
    value=normalize(text,decode)
    return any(m.group('number').lstrip('0')=='1131'
               for pattern in [LABEL,URL] for m in pattern.finditer(value))
def semantic(text,decode):
    value=decode(text)
    return bool(BASE.search(text) or BASE.search(value) or known_pr(text,decode))

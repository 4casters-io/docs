"""Gate 1 (structure): compare each translated page against its English source.

Run from the repo root:  python scripts/check-structure.py
Exit code 0 = pass, 1 = failures. Informational findings never fail the gate.

FAILURES (these break the site or the examples):
  FENCE-COUNT     a code fence was added or dropped
  FENCE-BODY      code inside a fence differs from English
  MDX-COMPONENTS  an MDX component was added, dropped or renamed
  OPENAPI         an `openapi:` frontmatter line was altered
  INLINE-CODE     an API identifier in backticks differs from English

INFORMATIONAL (expected; the rules ask for these to be translated):
  FENCE-INFO      the CodeGroup fence label, e.g. ```json Request -> ```json Solicitud
"""
import re, os, sys, collections

if hasattr(sys.stdout, 'reconfigure'):        # Windows consoles default to cp1252
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add new locales here. check-links.py has its own list -- keep them in step.
LOCALES = ['es', 'zh-Hans', 'zh-Hant', 'ru', 'fr', 'pt-BR', 'pt', 'nl', 'it']

# Inline code that is prose, not an API identifier, and so follows the
# translated heading it names. Keep this list short and justified.
#   changelog.mdx: "Changes are grouped under `Added`, `Changed`, ..." refers to
#   the `### Added` headings on the same page, which are themselves translated.
#   Leaving these in English would point at headings that do not exist.
# Keyed on the English source path, not the basename, so a future
# changelog.mdx elsewhere in the tree does not inherit this silently.
INLINE_EXEMPT = {
    'pages/changelog.mdx': {'Added', 'Changed', 'Fixed', 'Deprecated', 'Removed'},
}

FAIL_KINDS = {'FENCE-COUNT', 'FENCE-BODY', 'MDX-COMPONENTS', 'OPENAPI', 'INLINE-CODE', 'NO-EN-SOURCE'}
INFO_KINDS = {'FENCE-INFO'}

FENCE = re.compile(r'^(```+|~~~+)(.*)$')
ANY_FENCE = re.compile(r'^(```+|~~~+).*?^\1', re.S | re.M)


def fences(t):
    out, lines, i = [], t.split('\n'), 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if m:
            mark, info, body = m.group(1), m.group(2), []
            i += 1
            while i < len(lines) and not lines[i].startswith(mark):
                body.append(lines[i])
                i += 1
            out.append((info.strip(), '\n'.join(body)))
            i += 1
        else:
            i += 1
    return out


def strip_fences(t):
    return ANY_FENCE.sub('', t)          # handles ``` and ~~~


def inline(t):
    return collections.Counter(re.findall(r'`([^`\n]+)`', strip_fences(t)))


def comps(t):
    return collections.Counter(re.findall(r'<\s*([A-Z][A-Za-z0-9]*)', strip_fences(t)))


def fm(t):
    m = re.match(r'^---\n(.*?)\n---', t, re.S)
    return m.group(1) if m else ''


def openapi(t):
    return [l.strip() for l in fm(t).split('\n') if l.strip().startswith('openapi:')]


def norm(p):
    return p.replace(os.sep, '/')


issues = collections.defaultdict(list)

for lang in LOCALES:
    base = os.path.join(lang, 'pages')
    if not os.path.isdir(base):
        print('skip %s (no %s)' % (lang, base))
        continue
    for root, _, fs in os.walk(base):
        for f in sorted(fs):
            if not f.endswith('.mdx'):
                continue
            tp = norm(os.path.join(root, f))
            ep = tp[len(lang) + 1:]
            if not os.path.exists(ep):
                issues[lang].append(('NO-EN-SOURCE', tp, ''))
                continue
            T = open(tp, encoding='utf-8').read()
            E = open(ep, encoding='utf-8').read()

            tf, ef = fences(T), fences(E)
            if len(tf) != len(ef):
                issues[lang].append(('FENCE-COUNT', tp, '%d vs en %d' % (len(tf), len(ef))))
            else:
                for i, (a, b) in enumerate(zip(tf, ef)):
                    if a[1] != b[1]:
                        issues[lang].append(('FENCE-BODY', tp, '#%d' % (i + 1)))
                    elif a[0] != b[0]:
                        issues[lang].append(('FENCE-INFO', tp, '#%d %r vs %r' % (i + 1, a[0], b[0])))

            tc, ec = comps(T), comps(E)
            if tc != ec:
                d = {k: (tc.get(k, 0), ec.get(k, 0)) for k in set(tc) | set(ec) if tc.get(k, 0) != ec.get(k, 0)}
                issues[lang].append(('MDX-COMPONENTS', tp, str(d)))

            to, eo = openapi(T), openapi(E)
            if to != eo:
                issues[lang].append(('OPENAPI', tp, '%s vs en %s' % (to, eo)))

            exempt = INLINE_EXEMPT.get(ep, set())
            ti, ei = inline(T), inline(E)
            miss = {k: (ti.get(k, 0), ei[k]) for k in ei
                    if ti.get(k, 0) != ei[k] and k not in exempt}
            if miss:
                items = list(miss.items())[:6]
                issues[lang].append(('INLINE-CODE', tp, str(dict(items)) + (' ...' if len(miss) > 6 else '')))

fails = info = 0
for lang in LOCALES:
    found = issues.get(lang, [])
    by = collections.defaultdict(list)
    for k, p, d in found:
        by[k].append((p, d))
    nf = sum(len(v) for k, v in by.items() if k in FAIL_KINDS)
    ni = sum(len(v) for k, v in by.items() if k in INFO_KINDS)
    fails += nf
    info += ni
    print('\n########## %s — %s (%d failures, %d informational)' % (
        lang, 'PASS' if nf == 0 else 'FAIL', nf, ni))
    for k in sorted(by):
        tag = 'FAIL' if k in FAIL_KINDS else 'info'
        print('\n  [%s] %s (%d files)' % (tag, k, len(by[k])))
        for p, d in by[k][:12]:
            print('    %s%s' % (p, '\n        ' + d if d else ''))
        if len(by[k]) > 12:
            print('    ... +%d more' % (len(by[k]) - 12))

print('\n' + '=' * 60)
print('GATE 1 STRUCTURE: %s — %d failures, %d informational' % (
    'PASS' if fails == 0 else 'FAIL', fails, info))
sys.exit(1 if fails else 0)

"""Gate 1 (links): every internal link and #anchor in the docs resolves.

Run from the repo root:  python scripts/check-links.py
Exit code 0 = pass, 1 = unresolved targets.

Covers absolute links (/es/pages/foo) and relative links (../foo, ./foo, foo),
each with an optional #fragment checked against the target page's headings and
its explicit {#id} anchors.
"""
import re, os, sys, collections

if hasattr(sys.stdout, 'reconfigure'):        # Windows consoles default to cp1252
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add new locales here. check-structure.py has its own list -- keep them in step.
LOCALES = ['es', 'zh-Hans', 'zh-Hant']
ROOTS = ['pages'] + LOCALES

# Link targets that are not pages in this repo.
EXTERNAL_PREFIXES = ('api-reference', 'sources')

# markdown ](target) plus component href="target" -- Card/Columns hrefs are
# real navigation and 404 just as loudly as a markdown link.
LINK = re.compile(r"""\]\(([^)\s]+)\)|href=["']([^"']+)["']""")
ANCHOR = re.compile(r'\{#([A-Za-z0-9_-]+)\}')
# indent-tolerant: headings nested inside JSX children (e.g. <Update>) are
# still headings to the MDX renderer, so they are to this checker too.
HEADING = re.compile(r'^\s{0,3}#{1,6}\s+(.*?)\s*$', re.M)


def norm(p):
    return p.replace(os.sep, '/')


def slug(text):
    text = ANCHOR.sub('', text)
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'[*_]', '', text)
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9一-鿿\s-]', '', text)
    return re.sub(r'\s+', '-', text)


_anchor_cache = {}


dup_anchor = []


def anchors_of(path):
    if path in _anchor_cache:
        return _anchor_cache[path]
    t = open(path, encoding='utf-8').read()
    out = set()
    explicit = collections.Counter()
    for h in HEADING.findall(t):
        m = ANCHOR.search(h)
        if m:
            explicit[m.group(1)] += 1
        out.add(m.group(1) if m else slug(h))
    for a, n in explicit.items():
        if n > 1:
            dup_anchor.append((path, a, n))   # deep links land on the first only
    out |= set(ANCHOR.findall(t))
    _anchor_cache[path] = out
    return out


# key (path without .mdx) -> file path
mdx = {}
for root, _, fs in os.walk('.'):
    if '.git' in root:
        continue
    for f in fs:
        if f.endswith('.mdx'):
            p = norm(os.path.join(root, f))
            p = p[2:] if p.startswith('./') else p
            mdx[p[:-4]] = p

SNIPPET = re.compile(r"""<Snippet\s[^>]*file=["']([^"']+)["']""")

bad_page, bad_anchor, bad_snippet, skipped = [], [], [], 0
total = 0

for key, path in sorted(mdx.items()):
    if key.split('/')[0] not in ROOTS:
        continue
    anchors_of(path)          # populates dup_anchor for every page, linked or not
    for m in LINK.findall(open(path, encoding='utf-8').read()):
        link = m[0] or m[1]
        if link.startswith(('http://', 'https://', 'mailto:')):
            continue
        total += 1
        target, _, frag = link.partition('#')
        if not target:
            # same-page anchor, e.g. ](#order-types) -- resolve against this
            # page's own headings. This is the exact break from translating a
            # heading without carrying the English {#id} over.
            if frag and frag not in anchors_of(path):
                bad_anchor.append((path, link, sorted(anchors_of(path))[:5]))
            continue
        if target.startswith('/'):
            resolved = target.strip('/')
        else:                                  # relative to the linking page's dir
            resolved = norm(os.path.normpath(os.path.join(os.path.dirname(key), target)))
        resolved = resolved[:-4] if resolved.endswith('.mdx') else resolved
        if resolved.startswith(EXTERNAL_PREFIXES):
            skipped += 1
            continue
        if resolved not in mdx:
            bad_page.append((path, link))
            continue
        if frag and frag not in anchors_of(mdx[resolved]):
            bad_anchor.append((path, link, sorted(anchors_of(mdx[resolved]))[:5]))

    # <Snippet file="..."> resolves against snippets/
    for ref in SNIPPET.findall(open(path, encoding='utf-8').read()):
        total += 1
        target = 'snippets/' + ref.lstrip('/')
        if not os.path.exists(target):
            bad_snippet.append((path, ref))

print('internal links checked: %d  (%d external/openapi targets skipped)' % (total, skipped))

print('\n=== UNRESOLVED PAGE TARGETS (%d) ===' % len(bad_page))
for p, l in bad_page[:25]:
    print('  %s\n      -> %s' % (p, l))
if len(bad_page) > 25:
    print('  ... +%d more' % (len(bad_page) - 25))

print('\n=== UNRESOLVED SNIPPET REFS (%d) ===' % len(bad_snippet))
for p, r in bad_snippet[:25]:
    print('  %s\n      -> file="%s"' % (p, r))
if len(bad_snippet) > 25:
    print('  ... +%d more' % (len(bad_snippet) - 25))

print('\n=== UNRESOLVED ANCHORS (%d) ===' % len(bad_anchor))
agg = collections.Counter(l for _, l, _ in bad_anchor)
for l, c in agg.most_common(25):
    ex = next(x for x in bad_anchor if x[1] == l)
    print('  %-58s x%d  (in %s)\n      have: %s' % (l, c, ex[0], ex[2]))
if len(agg) > 25:
    print('  ... +%d more distinct' % (len(agg) - 25))

# --- docs.json navigation: every page path must exist and live in its own locale ---
import json
NAV_SKIP_KEYS = {'banner', 'footer', 'navbar', 'openapi', 'global', 'icon',
                 'language', 'tab', 'group', 'description', 'content'}
bad_nav = []
_doc = json.load(open('docs.json', encoding='utf-8'))
_langs = _doc.get('navigation', {}).get('languages', [])
for _lang in _langs:
    _code = _lang.get('language')
    _stack = [{k: v for k, v in _lang.items() if k not in NAV_SKIP_KEYS}]
    while _stack:
        _o = _stack.pop()
        if isinstance(_o, dict):
            _stack.extend(v for k, v in _o.items() if k not in NAV_SKIP_KEYS)
        elif isinstance(_o, list):
            _stack.extend(_o)
        elif isinstance(_o, str) and '/' in _o and ' ' not in _o \
                and not _o.startswith(('http', '/')):
            total += 1
            if not os.path.exists(_o + '.mdx'):
                bad_nav.append((_code, _o, 'missing file'))
            elif _code != 'en' and not _o.startswith(_code + '/'):
                bad_nav.append((_code, _o, 'points outside its locale'))
            elif _code == 'en' and not _o.startswith('pages/'):
                bad_nav.append((_code, _o, 'points outside its locale'))

# Every locale tree on disk must have a nav block -- catches a deleted block.
_nav_codes = {l.get('language') for l in _langs}
for _code in ['en'] + LOCALES:
    _dir = 'pages' if _code == 'en' else _code
    if os.path.isdir(_dir) and _code not in _nav_codes and (_code != 'en' or 'en' not in _nav_codes):
        bad_nav.append((_code, '(no navigation.languages block)', 'locale tree exists on disk'))

print('\n=== DUPLICATE EXPLICIT ANCHORS (%d) ===' % len(dup_anchor))
for _p, _a, _n in dup_anchor[:25]:
    print('  %s  {#%s} x%d' % (_p, _a, _n))

print('\n=== NAV ENTRIES UNRESOLVED (%d) ===' % len(bad_nav))
for _c, _p, _why in bad_nav[:25]:
    print('  [%s] %s  (%s)' % (_c, _p, _why))

bad = len(bad_page) + len(bad_anchor) + len(bad_snippet) + len(bad_nav) + len(dup_anchor)
print('\n' + '=' * 60)
print('GATE 1 LINKS: %s — %d unresolved' % ('PASS' if bad == 0 else 'FAIL', bad))
sys.exit(1 if bad else 0)

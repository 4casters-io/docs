"""Generate zh-Hant from zh-Hans via OpenCC s2twp, protecting code."""
import os, re, io, json, sys
import opencc

CC = opencc.OpenCC('s2twp')

# s2twp leaves mainland vocabulary in places Taiwan renders differently.
POST = [
    ('實時', '即時'),
    ('賬戶', '帳戶'),
    ('賬號', '帳號'),
    ('賬單', '帳單'),
    ('登錄', '登入'),
    ('注銷', '登出'),
]

FENCE = re.compile(r'(^|\n)(```+|~~~+)[^\n]*\n.*?\n\2(?=\n|$)', re.S)
INLINE = re.compile(r'`[^`\n]+`')


def convert_text(s):
    out = CC.convert(s)
    for a, b in POST:
        out = out.replace(a, b)
    return out


def convert_doc(text):
    """Convert prose only; code fences and inline code stay byte-identical."""
    slots = []

    def stash(m):
        slots.append(m.group(0))
        return '\x00%d\x00' % (len(slots) - 1)

    t = FENCE.sub(stash, text)
    t = INLINE.sub(stash, t)
    t = convert_text(t)
    for i, v in enumerate(slots):
        t = t.replace('\x00%d\x00' % i, v)
    return t


def retarget(text, frm, to):
    text = text.replace('](/%s/' % frm, '](/%s/' % to)
    text = text.replace('file="%s/' % frm, 'file="%s/' % to)
    return text


def main():
    src, dst = 'zh-Hans', 'zh-Hant'
    n = 0
    for base in (os.path.join(src, 'pages'), os.path.join('snippets', src)):
        for root, _, fs in os.walk(base):
            for f in sorted(fs):
                if not f.endswith('.mdx'):
                    continue
                sp = os.path.join(root, f)
                dp = sp.replace(src, dst, 1) if root.startswith('snippets') else sp.replace(src + os.sep, dst + os.sep, 1)
                dp = sp.replace(src, dst, 1)
                os.makedirs(os.path.dirname(dp), exist_ok=True)
                t = io.open(sp, encoding='utf-8', newline='').read()
                t = convert_doc(t)
                t = retarget(t, src, dst)
                io.open(dp, 'w', encoding='utf-8', newline='').write(t)
                n += 1
    print('wrote %d zh-Hant files' % n)


if __name__ == '__main__':
    main()

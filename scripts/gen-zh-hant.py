"""Generate zh-Hant from zh-Hans via OpenCC s2twp, protecting code.

Fence BODIES and inline code are never converted (rule 2: byte-identical
to English). Fence labels, prose, headings and MDX text children are.
Line-based parsing, so CRLF files are handled correctly.
"""
import os, re, io
import opencc

CC = opencc.OpenCC('s2twp')

# s2twp converts script, not register. These are the mainland terms it
# leaves behind (or mis-converts) that Taiwan API docs render differently.
# Longest-first: compounds before their substrings.
POST = [
    ('實時', '即時'),
    ('賬戶', '帳戶'),
    ('賬號', '帳號'),
    ('賬單', '帳單'),
    ('登錄', '登入'),
    ('注銷', '登出'),
    ('響應頭', '回應標頭'),
    ('請求頭', '請求標頭'),
    ('響應體', '回應主體'),
    ('請求體', '請求主體'),
    ('響應', '回應'),
    ('返回', '回傳'),
    ('撥用', '呼叫'),      # s2twp mangles 调用 into 撥用 (to appropriate funds)
    ('調用', '呼叫'),
    ('標識符', '識別碼'),
    # 标识 is noun (identifier) AND verb (marks / identifies). The verb
    # cases must not become the noun 識別碼 -- "`0` 識別碼取消" is gibberish.
    # Enumerated verb contexts first; the generic noun rule last.
    ('標識取消', '表示取消'),            # `0` marks a cancel
    ('標識哪', '標示哪'),                # identifies which side of the book
    ('組合**標識', '組合**識別'),        # identified by the market+side combination
    ('標識', '識別碼'),
    ('載荷', '酬載'),
    ('釋出', '發布'),      # s2twp turns 发布 (publish) into 釋出 (a software release)
    ('平臺', '平台'),
    # Taiwan register (review pass 2026-09-07; Microsoft zh-TW and the app catalog agree):
    ('程式設計方式', '程式化方式'),   # programmatic
    ('程式碼', '代碼'),          # league code / short code, not source code
    ('運動專案', '運動項目'),      # 專案 is a project
    ('十六進位制', '十六進位'),
    ('全域性', '全域'),
    ('反規範化', '反正規化'),      # denormalized
    ('速率限制', '速率限制'),
    ('限流', '速率限制'),
    ('客戶端', '用戶端'),
    ('引數', '參數'),
    ('指令碼', '腳本'),
    ('字首', '前綴'),
    ('映象', '鏡像'),
    ('對映', '對應'),
    ('後臺', '後台'),
    ('郵箱', '電子郵件'),
    ('提現', '提款'),
    ('複用', '重複使用'),
    ('訪問', '存取'),
    ('按產品規則', '依產品規則'),
    ('憑據', '憑證'),
    ('對賬', '對帳'),
    ('服務端', '伺服器端'),
    ('時間戳', '時間戳記'),
    ('回滾', '復原'),          # rolled back (order fills)
    ('撞庫攻擊', '憑證填充攻擊'),
]

INLINE = re.compile(r'`[^`\n]+`')
FENCE_MARK = re.compile(r'^(\s*)(```+|~~~+)(.*)$')


def convert_text(s):
    out = CC.convert(s)
    for a, b in POST:
        out = out.replace(a, b)
    return out


def convert_doc(text):
    """Convert prose; fence bodies and inline code stay byte-identical."""
    nl = '\r\n' if '\r\n' in text else '\n'
    lines = text.split(nl)
    out = []
    in_fence = False
    fence_mark = ''
    for line in lines:
        m = FENCE_MARK.match(line)
        if not in_fence and m:
            in_fence, fence_mark = True, m.group(2)
            out.append(convert_text(line))     # the label is human-facing
        elif in_fence:
            out.append(line)                   # body: byte-identical
            if line.lstrip().startswith(fence_mark):
                in_fence = False
        else:
            slots = []

            def stash(mm):
                slots.append(mm.group(0))
                return '\x00%d\x00' % (len(slots) - 1)

            t = INLINE.sub(stash, line)
            t = convert_text(t)
            for i, v in enumerate(slots):
                t = t.replace('\x00%d\x00' % i, v)
            out.append(t)
    return nl.join(out)


def retarget(text, frm, to):
    text = text.replace('](/%s/' % frm, '](/%s/' % to)           # markdown links
    text = text.replace('href="/%s/' % frm, 'href="/%s/' % to)   # Card/Columns hrefs
    text = text.replace("href='/%s/" % frm, "href='/%s/" % to)
    text = text.replace('file="%s/' % frm, 'file="%s/' % to)     # <Snippet file=...>
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

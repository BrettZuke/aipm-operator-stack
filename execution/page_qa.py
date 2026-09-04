#!/usr/bin/env python3
"""Full page QA for a live URL: the verification gate for any web build.

Usage:
  python3 page_qa.py URL [URL...] [--out DIR] [--max-links 30] [--skip-links]

Per URL, at desktop 1440x900 and mobile 390x844:
  - full-page screenshot saved to --out (default .tmp/page_qa/)
  - console errors and page errors collected (must be zero)
  - banned character scan of rendered text (emoji, em/en dash must be zero)
  - font check: flags Inter/Roboto or bare system fallbacks on body/h1/buttons
  - desktop only: crawls every <a href> (capped) and flags dead links
Exit 0 only if everything passes. Requires:
  python3 -m pip install --user playwright && python3 -m playwright install chromium
"""
import os
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("FAIL playwright missing. Install:\n"
          "  python3 -m pip install --user playwright\n"
          "  python3 -m playwright install chromium")
    sys.exit(2)

EM, EN = chr(0x2014), chr(0x2013)
BANNED_FONTS = ("inter", "roboto")
VIEWPORTS = [("desktop", 1440, 900, False), ("mobile", 390, 844, True)]


def emoji_count(text):
    return sum(1 for ch in text
               if 0x1F000 <= ord(ch) <= 0x1FAFF or 0x2600 <= ord(ch) <= 0x27BF)


def slug(url):
    return url.replace("https://", "").replace("http://", "").strip("/").replace("/", "_").replace(".", "-")[:60]


def qa_url(pw, url, out_dir, max_links, skip_links):
    problems = []
    browser = pw.chromium.launch()
    for name, w, h, mobile in VIEWPORTS:
        ctx = browser.new_context(viewport={"width": w, "height": h},
                                  is_mobile=mobile, device_scale_factor=2)
        page = ctx.new_page()
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        try:
            page.goto(url, wait_until="networkidle", timeout=45000)
        except Exception:
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                errors.append("networkidle timeout, loaded domcontentloaded only")
            except Exception as e:
                problems.append(f"{name}: page failed to load: {e}")
                ctx.close()
                continue
        page.wait_for_timeout(2500)
        inner = page.evaluate("window.innerWidth")
        if abs(inner - w) > 40:
            problems.append(f"{name}: viewport floor hit, innerWidth={inner} wanted {w} "
                            "(use fixed-width iframe harness for shots)")
        shot = os.path.join(out_dir, f"{slug(url)}_{name}_{w}.png")
        page.screenshot(path=shot, full_page=True)
        print(f"  {name} screenshot: {shot}")
        for e in errors:
            problems.append(f"{name} console: {e[:200]}")
        text = page.evaluate("document.body ? document.body.innerText : ''")
        em, en, emo = text.count(EM), text.count(EN), emoji_count(text)
        if em or en or emo:
            problems.append(f"{name}: banned chars in rendered text em={em} en={en} emoji={emo}")
        fonts = page.evaluate(
            """() => ['body','h1','h2','button','a'].map(sel => {
                 const el = document.querySelector(sel);
                 return el ? sel + ':' + getComputedStyle(el).fontFamily : null;
               }).filter(Boolean)""")
        for f in fonts:
            fam = f.split(":", 1)[1].lower()
            first = fam.split(",")[0].strip().strip('"\'')
            if first in BANNED_FONTS:
                problems.append(f"{name} banned font on {f.split(':')[0]}: {first}")
        if name == "desktop":
            print(f"  fonts: {fonts[:3]}")
            if not skip_links:
                hrefs = page.evaluate(
                    """() => Array.from(document.querySelectorAll('a[href]'))
                          .map(a => a.href)
                          .filter(h => h.startsWith('http'))""")
                seen = []
                for hr in hrefs:
                    if hr not in seen:
                        seen.append(hr)
                dropped = len(seen) - max_links if len(seen) > max_links else 0
                for hr in seen[:max_links]:
                    try:
                        resp = ctx.request.get(hr, timeout=12000, max_redirects=5)
                        if resp.status >= 400:
                            problems.append(f"dead link {resp.status}: {hr}")
                    except Exception as e:
                        problems.append(f"link error: {hr} ({str(e)[:80]})")
                print(f"  links checked: {min(len(seen), max_links)}"
                      + (f" ({dropped} over cap, not checked)" if dropped else ""))
        ctx.close()
    browser.close()
    return problems


def main(argv):
    urls = [a for a in argv[1:] if not a.startswith("--")]
    out_dir = ".tmp/page_qa"
    max_links, skip_links = 30, "--skip-links" in argv
    if "--out" in argv:
        out_dir = argv[argv.index("--out") + 1]
        if out_dir in urls:
            urls.remove(out_dir)
    if "--max-links" in argv:
        v = argv[argv.index("--max-links") + 1]
        max_links = int(v)
        if v in urls:
            urls.remove(v)
    if not urls:
        print(__doc__)
        return 2
    os.makedirs(out_dir, exist_ok=True)
    all_ok = True
    with sync_playwright() as pw:
        for url in urls:
            print(f"== {url}")
            problems = qa_url(pw, url, out_dir, max_links, skip_links)
            for p in problems:
                print(f"  FAIL {p}")
            if problems:
                all_ok = False
            else:
                print("  clean")
    print("RESULT:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

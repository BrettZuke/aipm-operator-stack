#!/usr/bin/env python3
"""Verify a deploy actually serves the new content. A 200 is not verification.

Usage:
  python3 deploy_verify.py URL --expect "string" [--expect "..."] [--absent "old string"]

Fetches URL with a browser User-Agent, retries 3x, checks every --expect
string is present and every --absent string is gone. Prints context snippets.
Exit 0 only if all checks pass.
"""
import sys
import time
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def fetch(url, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, r.read().decode("utf-8", errors="replace")
        except Exception as e:
            last = e
            time.sleep(3 * (i + 1))
    raise SystemExit(f"FAIL could not fetch {url} after {retries} tries: {last}")


def main(argv):
    args = argv[1:]
    if not args:
        print(__doc__)
        return 2
    url = args[0]
    expects, absents = [], []
    i = 1
    while i < len(args):
        if args[i] == "--expect":
            expects.append(args[i + 1]); i += 2
        elif args[i] == "--absent":
            absents.append(args[i + 1]); i += 2
        else:
            print(f"unknown arg {args[i]}"); return 2
    status, body = fetch(url)
    print(f"fetched {url} status={status} bytes={len(body)}")
    ok = status < 400
    if not ok:
        print(f"FAIL status {status}")
    for s in expects:
        idx = body.find(s)
        if idx == -1:
            print(f"FAIL expect not found: \"{s}\"")
            ok = False
        else:
            ctx = body[max(0, idx - 30):idx + len(s) + 30].replace("\n", " ")
            print(f"PASS expect found: \"{s}\" ...{ctx}...")
    for s in absents:
        if s in body:
            print(f"FAIL absent string still present: \"{s}\"")
            ok = False
        else:
            print(f"PASS absent confirmed gone: \"{s}\"")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

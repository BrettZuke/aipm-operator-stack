# Setup

This repo is a toolkit for Claude Code, not an application. There is no server to
run and no database to connect. You install the skills once, and from then on
Claude has them in every project on your machine.

Fifteen minutes, most of it waiting on downloads.

---

## 1. Get the code

```bash
git clone <this repo>
cd aipm-operator-stack
```

That is enough to use the skills. The steps below add the extras.

---

## 2. Install the skills

```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
rm -f ~/.claude/skills/INDEX.md
```

The connection runbooks are skills too. Install them the same way if you want them:

```bash
cp -R connections/* ~/.claude/skills/
```

Restart Claude Code. Ask it "what skills do you have" and you should see them.

---

## 3. Give Claude a browser

Open this folder in Claude Code. It will ask to approve the Playwright server listed
in `.mcp.json`. Say yes.

Now Claude can open a real browser, screenshot the pages you build at phone and
desktop width, click through them, and read the console. Read [MCP.md](MCP.md) for
what to do with that.

This is the single most useful thing in the repo if you are shipping websites you
cannot read the code of.

---

## 4. Optional: the four checking tools

Only needed if you want to run the verification scripts the prompt templates call.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Python 3.10 or newer.

| Tool | What it does |
|---|---|
| `execution/copy_lint.py` | Fails on em dashes, en dashes, emoji and slop phrases in your copy |
| `execution/page_qa.py` | Screenshots a page at 1440px and 390px, fails on console errors, dead links, banned fonts |
| `execution/deploy_verify.py` | Proves the new content is actually serving, rather than trusting a 200 response |
| `execution/apify_pool.py` | Rotates Apify tokens so one hitting its monthly quota does not stop a scrape |

---

## 5. Optional: API keys

```bash
cp .env.example .env
```

Fill in only what a skill asks you for. Most skills need nothing.

Start with the free ones. `GROQ_API_KEY` and `GEMINI_API_KEY` both have free tiers
that cover normal use. Add a paid key only when a specific skill needs it and you
have decided the cost is worth it.

**Never commit `.env`.** It is already in `.gitignore`. `.env.example` is the blank
template and is safe to commit. `.env` is yours and never leaves your machine.

---

## 6. Before you run anything against a live account

- Read what a script does before you run it. Every one has a docstring at the top.
- Test on your own accounts before a client's.
- Anything that sends email, sends a text, or spends credits costs real money. Check
  what it will do first.

---

## 7. Structure

| Folder | What it is |
|---|---|
| `skills/` | The Claude Code skills. This is the main thing you are here for |
| `connections/` | Deeper runbooks for specific services, installable as skills |
| `agents/` | Subagent definitions, for delegating work to cheaper models |
| `rules/` | Coding and review standards by language |
| `prompts/` | Task templates. `00_universal_wrapper.md` is the default |
| `execution/` | The four checking tools above |

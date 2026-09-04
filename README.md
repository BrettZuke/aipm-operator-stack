# Operator stack

The Claude Code toolkit for AI Partner Method students: 212 skills, the connection
runbooks, subagent definitions, coding standards, and task templates.

This is a toolkit, not an application. There is no server and no database. You install
the skills once and Claude has them in every project on your machine from then on.

Nothing here holds an account, a key or a customer record. Everything reads its
settings from a `.env` file you create.

---

## Where to start

1. Run through [SETUP.md](SETUP.md). Fifteen minutes.
2. Approve the Playwright browser when Claude Code asks. See [MCP.md](MCP.md) for why
   that one matters more than anything else here.
3. Browse [skills/INDEX.md](skills/INDEX.md) and find the three or four you will
   actually use this week. There are 212. You do not need most of them.

---

## What is in here

| Folder | What it is | Size |
|---|---|---|
| [skills/](skills/) | 212 Claude Code skills: design, copy, SEO, video, content, research, code quality. Start with [skills/INDEX.md](skills/INDEX.md) | 212 |
| [connections/](connections/) | Deeper runbooks: Typeform, GitHub workflow, asset hosting and scrapers, design systems, agent orchestration | 39 |
| [rules/](rules/) | Coding, testing, security and review standards by language | 65 files |
| [agents/](agents/) | Subagent definitions, for pushing volume work to cheaper models | 34 |
| [prompts/](prompts/) | Task templates. `00_universal_wrapper.md` is the default for anything | 8 |
| [execution/](execution/) | Four checking tools: copy lint, page QA, deploy verify, Apify token rotation | 4 |
| [MCP.md](MCP.md) | Giving Claude a real browser, so it can see the pages you ship | 1 |

---

## Why skills are worth the setup

A skill is a set of instructions Claude loads automatically when the task matches. The
difference is not that Claude can suddenly do something new. It is that it does the same
thing the same way every time, instead of freestyling and producing something that looks
plausible and is subtly wrong.

The design skills are the clearest example. Ask a model to build a landing page and you
get the same generic layout everyone else gets. Load `high-end-visual-design` first and
you get a considered typographic identity, because the skill tells it what to do and what
never to do.

---

## Verify, do not assume

The four tools in `execution/` exist because "it should work" is not a standard you can
sell against.

- `copy_lint.py` fails on em dashes, en dashes, emoji and slop phrases.
- `page_qa.py` screenshots a page at 1440px and 390px and fails on console errors, dead
  links and banned fonts.
- `deploy_verify.py` proves the new content is actually serving. A 200 response is not
  verification.
- `apify_pool.py` rotates Apify tokens so one hitting its monthly quota does not kill a
  scrape halfway through.

Run them before you send a client a link, not after they find the problem.

---

## Money rule

Default to free keys: `GROQ_API_KEY` and `GEMINI_API_KEY` both have free tiers that cover
normal use.

Leave `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` out of your `.env` entirely and nothing can
bill you by accident. Add a paid key only for a specific job you have decided to pay for,
and take it back out afterwards if you are worried.

Anything that sends an email, sends a text, or runs a scrape spends real money. Read what
a script does before you run it.

---

## Honest limits

**212 skills is too many to learn.** Do not try. Read the index, pick the handful that
match what you are doing this month, and ignore the rest until you need them. Skills for
Kotlin, Spring Boot, Rust and C++ are in here because the pack is shared across projects,
and you will almost certainly never open them.

**A skill is instructions, not magic.** It makes Claude consistent. It does not make it
right. You still have to check the output, which is what the browser and the four tools
are for.

**Some skills expect tools you may not have installed**, like `ffmpeg` for the video ones.
They will tell you what is missing when you run them.

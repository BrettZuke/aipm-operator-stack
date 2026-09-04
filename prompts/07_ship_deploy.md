# Ship / deploy

---

Operate under the Fable Protocol in CLAUDE.md.

Ship: {{PROJECT DIRECTORY}} to {{TARGET, e.g. Vercel project or domain}}

1. Run git status first. State exactly what will ship, including uncommitted changes. If unrelated WIP is present, stop and list it before proceeding.
2. Pick the right credentials: your personal Vercel token for your own projects; a client's projects require that client's token plus --scope <VERCEL_SCOPE>. Check the project's .env and the memory files before guessing. Never assume your own token can reach a client's scope.
3. Build locally first if the project has a build step, and quote the passing output.
4. Deploy. Then prove the change is serving: `python3 execution/deploy_verify.py <url> --expect "<string only in the new build>"` (add `--absent "<old string>"` when replacing content). A 200 response is not verification. For UI changes also run `python3 execution/page_qa.py <url>` and paste both outputs.
5. Commit the working tree after a successful deploy so git stays clean.

Report: live URL, the proof that the new content serves, commit hash.

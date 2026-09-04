# MCP: giving Claude a browser

MCP is how Claude gets abilities it does not have out of the box. Without it, Claude can
read and write files and run commands. With Playwright, it can also open a real browser.

That matters because you are shipping websites to paying clients. Claude can build a page
it cannot see. Playwright is what lets it look.

## What you get

This repo ships with one server already configured: **Playwright**.

Open this folder in Claude Code and it will ask you to approve it. Say yes. That is the
whole setup, there is nothing to install by hand.

Once approved you can ask for things like:

- "Open the site you just built, screenshot it at phone width and desktop width"
- "Click every link in the footer and tell me which ones 404"
- "Fill in the contact form with test details and confirm the lead actually arrives"
- "Check the console for errors on every page"

That last one catches the failure students miss most: a page that looks fine but throws a
JavaScript error, so the contact form silently never submits. The client finds out when
they wonder why nobody is calling.

## Use it before you hand anything over

Before you send a client a link, ask Claude to open the site, screenshot both widths,
click the CTAs, and submit the form. A screenshot is proof. "It should work" is not.

## Do not add more servers

Every MCP server loads its full tool list into every conversation, whether you use it or
not. Three or four servers and you will notice your usage limit arriving sooner, for
abilities you are not using.

Playwright is the one that earns its place, because you are shipping websites you cannot
read the code of and it is the only way Claude can actually look at them. Everything else
you can do with a script or a command, more cheaply and more predictably.

If you ever genuinely need another one, add it then, for that job, and consider taking it
back out afterwards.

## If Claude does not offer to connect

Check you opened the repo folder itself in Claude Code, not a parent folder. `.mcp.json`
is read from the folder you open. You can also run `/mcp` inside Claude Code to see which
servers are connected.

# Performance Optimization

## Model Selection Strategy (updated 2026-07-03)

**Fable 5** (claude-fable-5, available until ~2026-07-08):
- Highest judgment: design-heavy, client-facing, hard debugging
- Writing execution specs and reviewing other models' output (prompts/ 09 and 10)

**Opus 4.8** (claude-opus-4-8, the default after Fable access ends):
- Main development work and complex coding
- Runs under the Fable Protocol in ~/.claude/CLAUDE.md

**Sonnet 5** (claude-sonnet-5) and **Haiku 4.5** (claude-haiku-4-5):
- Cheaper volume work and lightweight worker agents, only when delegation is explicitly wanted

## Context Window Management

Avoid last 20% of context window for:
- Large-scale refactoring
- Feature implementation spanning multiple files
- Debugging complex interactions

Lower context sensitivity tasks:
- Single-file edits
- Independent utility creation
- Documentation updates
- Simple bug fixes

## Extended Thinking + Plan Mode

Extended thinking is enabled by default, reserving up to 31,999 tokens for internal reasoning.

Control extended thinking via:
- **Toggle**: Option+T (macOS) / Alt+T (Windows/Linux)
- **Config**: Set `alwaysThinkingEnabled` in `~/.claude/settings.json`
- **Budget cap**: `export MAX_THINKING_TOKENS=10000`
- **Verbose mode**: Ctrl+O to see thinking output

For complex tasks requiring deep reasoning:
1. Ensure extended thinking is enabled (on by default)
2. Enable **Plan Mode** for structured approach
3. Use multiple critique rounds for thorough analysis
4. Use split role sub-agents for diverse perspectives

## Build Troubleshooting

If build fails:
1. Use **build-error-resolver** agent
2. Analyze error messages
3. Fix incrementally
4. Verify after each fix

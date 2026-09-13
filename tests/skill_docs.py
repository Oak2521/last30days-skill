"""Read the reachable split instruction corpus for existing semantic contracts.

Tests of frontmatter or the always-loaded bootstrap must read SKILL.md directly.
This helper follows actual links and rejects missing local references; it does not
substitute the historical monolithic instructions or monkeypatch file reads.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / "skills" / "last30days"
ORDER = ["runtime", "setup", "setup-claude-code-modal-flow", "setup-non-modal-prose-flow", "setup-grok-bot-prose-flow", "setup-manual-setup-guide", "planning"]

def read_skill_docs():
    entry = ROOT / "SKILL.md"
    seen = set()
    def visit(path):
        path = path.resolve()
        if path in seen:
            return
        seen.add(path)
        text = path.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            link = link.split("#")[0]
            if not link or "://" in link or link.startswith(("/", "mailto:")) or "<" in link:
                continue
            target = (path.parent / link).resolve()
            if not target.is_relative_to(ROOT.resolve()):
                continue
            if not target.exists():
                raise AssertionError(f"Missing linked instruction: {target}")
            if target.suffix == ".md":
                visit(target)
    visit(entry)
    workflow = ROOT / "references" / "workflows"
    missing = {p.resolve() for p in workflow.glob("*.md")} - seen
    if missing:
        raise AssertionError(f"Unreachable workflow references: {sorted(missing)}")
    ordered = [entry] + [workflow / (name + ".md") for name in ORDER]
    ordered += sorted(p for p in seen if p.parent == workflow.resolve() and p not in [q.resolve() for q in ordered])
    return "\n\n".join(p.read_text(encoding="utf-8") for p in ordered if p.resolve() in seen)

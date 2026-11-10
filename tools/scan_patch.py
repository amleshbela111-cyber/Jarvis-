#!/usr/bin/env python3
"""
Reviews a change to the Jarvis source and writes a report. It never merges, commits or installs anything.

Usage:
    python3 tools/scan_patch.py <base_dir> <proposed_dir> [report.md]

It compares two folders and flags things a human reviewer must look at:
  - new network addresses or changed ones
  - new Android permissions, and changes to accessibility or device-admin setup
  - secret-looking strings (API keys, tokens, private keys)
  - process execution, dynamic code loading, and file deletion
  - new or changed dependencies in Gradle files
  - new or changed binary files (these cannot be reviewed as text)

Exit code 0: no high-risk finding. Exit code 2: at least one high-risk finding (a human must review).
A clean report is not proof of safety. It only means these checks found nothing.
"""
import os
import re
import sys

TEXT_EXT = (".kt", ".java", ".kts", ".gradle", ".xml", ".html", ".js", ".json", ".md", ".pro", ".properties", ".yml", ".yaml", ".txt")

SECRET_PATTERNS = [
    (r"AIza[0-9A-Za-z_\-]{30,}", "Google API key"),
    (r"ghp_[A-Za-z0-9]{20,}", "GitHub token"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "GitHub token"),
    (r"sk-[A-Za-z0-9]{20,}", "API secret key"),
    (r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "private key"),
]

RISKY_CODE = [
    (r"Runtime\.getRuntime\(\)\.exec|ProcessBuilder\(", "runs a system process", "high"),
    (r"DexClassLoader|PathClassLoader|loadClass\(|Class\.forName\(", "loads code at runtime", "high"),
    (r"\.delete\(\)|deleteRecursively\(|File\(.*\)\.delete", "deletes files", "medium"),
    (r"Cipher\.getInstance|SecretKeySpec", "encryption code (check it)", "medium"),
    (r"sendBroadcast|startActivity\(Intent\(Intent\.ACTION_SEND", "sends data to other apps", "medium"),
]

URL = re.compile(r"https?://[A-Za-z0-9.\-_~:/?#\[\]@!$&'()*+,;=%]+")
PERMISSION = re.compile(r'<uses-permission[^>]*android:name="([^"]+)"')
DEP = re.compile(r'implementation\(["\']([^"\']+)["\']\)')


def read_tree(root):
    files = {}
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "build", ".gradle")]
        for name in fn:
            path = os.path.join(dp, name)
            rel = os.path.relpath(path, root)
            if rel.lower().endswith(TEXT_EXT):
                try:
                    with open(path, encoding="utf-8") as f:
                        files[rel] = f.read()
                except UnicodeDecodeError:
                    files[rel] = None
            else:
                files[rel] = None
    return files


def findings_for(text, rel):
    out = []
    for pat, label in SECRET_PATTERNS:
        if re.search(pat, text):
            out.append(("high", f"{rel}: looks like a {label}"))
    for pat, label, level in RISKY_CODE:
        if re.search(pat, text):
            out.append((level, f"{rel}: {label}"))
    return out


def urls_in(text):
    return set(URL.findall(text or ""))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    base, proposed = sys.argv[1], sys.argv[2]
    report_path = sys.argv[3] if len(sys.argv) > 3 else None
    old, new = read_tree(base), read_tree(proposed)
    findings = []
    lines = ["# Jarvis change review", "", "This report only lists things to check. It does not approve or merge anything.", ""]

    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(f for f in set(old) & set(new) if old[f] != new[f])
    lines += ["## Files", f"- Added: {len(added)}", f"- Removed: {len(removed)}", f"- Changed: {len(changed)}", ""]
    for f in added:
        if new[f] is None:
            findings.append(("high", f"{f}: new binary file, cannot be reviewed as text"))
    for f in changed:
        if old[f] is None or new[f] is None:
            findings.append(("high", f"{f}: binary file changed, cannot be reviewed as text"))

    # Checks on every text file that is new or changed.
    for f in added + changed:
        text = new[f]
        if text is None:
            continue
        findings += findings_for(text, f)
        new_urls = urls_in(text) - urls_in(old.get(f))
        for u in sorted(new_urls):
            findings.append(("high", f"{f}: new network address {u}"))

    # Permissions and accessibility / admin changes in the manifest.
    for f in sorted(set(new) & {p for p in new if p.endswith("AndroidManifest.xml")}):
        old_perm = set(PERMISSION.findall(old.get(f) or ""))
        new_perm = set(PERMISSION.findall(new[f] or ""))
        for p in sorted(new_perm - old_perm):
            findings.append(("high", f"{f}: new permission {p}"))
        if "BIND_ACCESSIBILITY_SERVICE" in (new[f] or "") and "BIND_ACCESSIBILITY_SERVICE" not in (old.get(f) or ""):
            findings.append(("high", f"{f}: accessibility service added"))
        if "device_admin" in (new[f] or "") and "device_admin" not in (old.get(f) or ""):
            findings.append(("high", f"{f}: device admin added"))

    # New Gradle dependencies.
    for f in sorted(p for p in new if p.endswith((".gradle.kts", ".gradle"))):
        old_dep = set(DEP.findall(old.get(f) or ""))
        new_dep = set(DEP.findall(new[f] or ""))
        for d in sorted(new_dep - old_dep):
            findings.append(("medium", f"{f}: new dependency {d}"))

    high = [m for lvl, m in findings if lvl == "high"]
    medium = [m for lvl, m in findings if lvl == "medium"]
    lines += ["## High-risk findings (a human must review before merge)"]
    lines += [f"- {m}" for m in high] or ["- none"]
    lines += ["", "## Medium findings (check them)"]
    lines += [f"- {m}" for m in medium] or ["- none"]
    lines += ["", "## Removed files", *([f"- {f}" for f in removed] or ["- none"])]
    text_report = "\n".join(lines) + "\n"
    print(text_report)
    if report_path:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(text_report)
    return 2 if high else 0


if __name__ == "__main__":
    sys.exit(main())

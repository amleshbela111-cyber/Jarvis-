#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

# Push the JARVIS PWA source to GitHub.
# GitHub Actions automatically runs .github/workflows/build.yml after the push.

REPO_NAME="${1:-Jarvis-AI}"
BRANCH="${2:-main}"

say() { printf "\n[JARVIS] %s\n" "$*"; }
die() { printf "\n[ERROR] %s\n" "$*" >&2; exit 1; }

command -v git >/dev/null 2>&1 || die "Git missing. Run: pkg install git"
command -v gh  >/dev/null 2>&1 || die "GitHub CLI missing. Run: pkg install gh"

[[ -f "index.html" && -f "manifest.json" && -f ".github/workflows/build.yml" ]] \
  || die "Run this script from the extracted project folder containing index.html and .github/workflows/build.yml."

gh auth status >/dev/null 2>&1 || die "GitHub login required. Run: gh auth login"

OWNER="$(gh api user --jq .login)"
[[ -n "$OWNER" ]] || die "Could not read your GitHub username."
FULL_REPO="${OWNER}/${REPO_NAME}"
REMOTE_URL="https://github.com/${FULL_REPO}.git"

if ! git config user.name >/dev/null; then
  GH_NAME="$(gh api user --jq '.name // .login')"
  git config user.name "$GH_NAME"
fi
if ! git config user.email >/dev/null; then
  GH_ID="$(gh api user --jq .id)"
  GH_LOGIN="$(gh api user --jq .login)"
  git config user.email "${GH_ID}+${GH_LOGIN}@users.noreply.github.com"
fi

if [[ ! -d ".git" ]]; then
  say "Initializing Git repository..."
  git init
fi

git branch -M "$BRANCH"

if [[ ! -f ".gitignore" ]]; then
cat > .gitignore <<'GITIGNORE'
build/
dist/
*.log
.DS_Store
Thumbs.db
GITIGNORE
fi

git add -A

if ! git diff --cached --quiet; then
  git commit -m "Update JARVIS Energy Core PWA"
else
  say "No new file changes to commit."
fi

if gh repo view "$FULL_REPO" >/dev/null 2>&1; then
  say "GitHub repository already exists: ${FULL_REPO}"
else
  say "Creating private GitHub repository: ${FULL_REPO}"
  gh repo create "$REPO_NAME" --private --description "JARVIS Energy Core PWA"
fi

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE_URL"
else
  git remote add origin "$REMOTE_URL"
fi

say "Pushing to ${FULL_REPO}..."
git push -u origin "$BRANCH"

say "Push complete. GitHub Actions build workflow should start automatically."
say "Check: https://github.com/${FULL_REPO}/actions"

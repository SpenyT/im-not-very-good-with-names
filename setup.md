# Git Hooks Setup Guide

This guide explains how to set up the custom git hooks in this repository. The hooks are tracked in the `.githooks` folder and enforce Conventional Commits format with issue references.

## Overview

The repository uses a custom hooks directory (`.githooks`) instead of the default `.git/hooks` to allow version control of git hooks. This ensures all team members use the same validation rules.

## Prerequisites

- Git 2.9+ (for `core.hooksPath` support)
- Bash shell (available by default on Linux/macOS, Git Bash on Windows)

## Setup Instructions

### Option 1: Direct Configuration (Recommended)

This method configures Git to use the `.githooks` directory directly.

#### All Platforms (Linux, macOS, Windows)

```bash
# Configure Git to use the custom hooks directory
git config core.hooksPath .githooks

# Make hooks executable (Linux/macOS)
chmod +x .githooks/commit-msg

# On Windows (Git Bash), the executable bit is usually set automatically,
# but you can run this command anyway—it won't hurt
```

**Windows users:** If using Git Bash, the chmod command should work. If using PowerShell or CMD, the executable permission is typically handled automatically by Git.

### Option 2: Symlink Method (Alternative)

This method creates a symlink from `.git/hooks` to `.githooks`. Useful if you prefer the traditional hooks location or have tools that expect hooks in `.git/hooks`.

#### Linux / macOS

```bash
# Remove existing hooks directory (backup first if needed)
rm -rf .git/hooks

# Create symlink
ln -s ../.githooks .git/hooks

# Make hooks executable
chmod +x .githooks/commit-msg
```

#### Windows

**Using Git Bash (Recommended):**

```bash
# Remove existing hooks directory (backup first if needed)
rm -rf .git/hooks

# Create symlink (requires Developer Mode or Administrator privileges)
ln -s ../.githooks .git/hooks

# Make hooks executable
chmod +x .githooks/commit-msg
```

**Using PowerShell (Run as Administrator):**

```powershell
# Remove existing hooks directory (backup first if needed)
Remove-Item -Recurse -Force .git\hooks -ErrorAction SilentlyContinue

# Create symlink
New-Item -ItemType SymbolicLink -Path .git\hooks -Target .githooks
```

**Using Command Prompt (Run as Administrator):**

```cmd
REM Remove existing hooks directory
rmdir /S /Q .git\hooks

REM Create symlink
mklink /D .git\hooks .githooks
```

**Note for Windows users:**
- Creating symlinks on Windows requires either:
  - Administrator privileges, OR
  - Developer Mode enabled (Windows 10+), OR
  - Using Option 1 (Direct Configuration) which doesn't require special privileges

To enable Developer Mode on Windows 10/11:
1. Open Settings → Update & Security → For developers
2. Toggle "Developer Mode" to On

## Verification

After setup, verify the hooks are working:

```bash
# Check Git configuration
git config core.hooksPath
# Should output: .githooks (if using Option 1)

# Check if hook is executable (Linux/macOS/Git Bash)
ls -l .githooks/commit-msg
# Should show 'x' permission bits

# Test the hook with an invalid commit message
git commit --allow-empty -m "invalid message"
# Should fail with validation error

# Test with a valid commit message
git commit --allow-empty -m "feat: add new feature #123"
# Should succeed

# Remove the test commit
git reset --soft HEAD~1
```

## Commit Message Format

The `commit-msg` hook enforces the following format:

```
type(scope)?: subject #issue

[optional body]

[optional footer]
```

### Required Elements

- **Type**: One of: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- **Subject**: Short description (≤100 chars), starts with lowercase, imperative mood
- **Issue reference**: At least one issue number like `#123` anywhere in the message

### Optional Elements

- **Scope**: Component/module name in parentheses, e.g., `(parser)`, `(ui)`
- **Breaking change marker**: `!` after type/scope for breaking changes
- **Body**: Detailed explanation (blank line after subject)
- **Footer**: Metadata like `BREAKING CHANGE:`, `Refs:`, etc.

### Examples

**Valid commits:**

```
feat(parser)!: support new syntax (#33)

fix(ui): correct button color #123

docs(readme): add install instructions (#22)

refactor: simplify error handling
Closes #456

BREAKING CHANGE: API signature changed
```

**Invalid commits:**

```
Add new feature #123
❌ Missing type

feat add feature #123
❌ Missing colon

feat: #123
❌ Empty subject

feat: add feature
❌ Missing issue reference

feat():  add feature #123
❌ Empty scope or extra space after colon
```

## Troubleshooting

### Hook not executing

1. Verify `core.hooksPath` is set: `git config core.hooksPath`
2. Check hook file exists: `ls -la .githooks/commit-msg`
3. Ensure hook is executable: `chmod +x .githooks/commit-msg`

### Permission denied (Windows)

- Use Git Bash instead of PowerShell/CMD
- Or use Option 1 (Direct Configuration) which doesn't require symlinks

### Symlink creation failed (Windows)

- Enable Developer Mode or run terminal as Administrator
- Or use Option 1 (Direct Configuration) as an alternative

### Hook validation seems wrong

- Check for CRLF line endings: `file .githooks/commit-msg`
- The hook handles CRLF automatically, but ensure the script itself uses LF endings
- Configure Git to preserve LF: `git config core.autocrlf input`

## Disabling Hooks Temporarily

If you need to bypass the hook for a single commit:

```bash
git commit --no-verify -m "your message"
```

**Note:** Use this sparingly—hooks exist to maintain code quality!

## Updating Hooks

When hooks are updated in the repository:

1. Pull the latest changes: `git pull`
2. No additional setup needed—hooks are automatically updated since they're tracked

## Team Setup

**For new team members:**

1. Clone the repository
2. Run setup commands from this guide
3. Test with a commit

**Add to onboarding checklist:**
-[] Configure git hooks: `git config core.hooksPath .githooks`
-[] Make hooks executable: `chmod +x .githooks/commit-msg` (Linux/macOS/Git Bash)
-[] Test with a dummy commit

## Additional Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [core.hooksPath Documentation](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corehooksPath)
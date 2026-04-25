# GitLord – Automate your GitLab CICD branch workflow

GitLord is a Python CLI tool that streamlines the repetitive Git steps required for
creating feature branches, pushing commits, amending them, and opening merge requests
on GitLab – all from your macOS terminal.

It wraps three phases of a typical Terraform/GitLab workflow into simple, colour‑coded
commands, so you can focus on writing code instead of typing the same `git` incantations
over and over.

---

## Features

- **Phase 1** – Start a new feature branch from `main`/`master` in a safe, clean state.
- **Phase 2** – Stage, commit, push, and automatically open the new merge request URL in your browser.
- **Phase 3** – Amend the last commit (reusing its message) and force‑push with lease.
- **Phase 4** – Switch to the master/main branch and pull the latest changes.
- Automatic detection of the default branch (`main` or `master`).
- Rich coloured output (8‑bit terminal colours) – disabled automatically when output is redirected.
- Comprehensive error logging to `/tmp/gitlord.log` with size‑based rotation and compression.

---

## Requirements

- **Python 3.7** or higher (uses `Optional` type hints for compatibility).
- **Git** – must be installed and accessible in `PATH`.
- macOS (or any Unix‑like system with `/tmp` write access; the script can run elsewhere but was developed for macOS).
- Git authentication (SSH or HTTPS) already set up – the script does not handle login.

---

## Installation

1. Download the `gitlord` script and make it executable:
   ```bash
   chmod +x gitlord
   ```
2. Move it to a directory in your $PATH, e.g. /usr/local/bin:
   ```bash
   sudo mv gitlord /usr/local/bin/
   ```
   (If you don’t have /usr/local/bin, you can also place it in ~/bin and add that to your PATH.)
3. Verify installation:
   ```bash
   gitlord --help
   ```

## Usage

### 1. Start a new feature branch (Phase 1)
```bash
gitlord start <branch-name> [--base main|master]
```
- Ensures your working tree is clean.
- Fetches the latest remote refs.
- Checks out the base branch and fast‑forwards it.
- Creates and switches to <branch-name>.

Examples:
```bash
# auto‑detect base branch (main or master)
gitlord start feature/terraform-module

# explicitly use 'master' as base
gitlord start fix/vpc-bug --base master
```

### 2. Commit, push, and open merge request (Phase 2)
```bash
gitlord push "<commit message>" [--branch <branch>]
```
- Stages all changes (git add .).
- Creates a commit with the given message.
- Pushes to origin/<branch>.
- Extracts the merge request URL from the GitLab push response and opens it in your default browser.

If --branch is omitted, the current branch is used.

- Optionally, use `--user` to specify the git user name for the commit message. If not provided, the git user name is read from your local Git configuration.

Example:
```bash
gitlord push "Add new VPC module with subnet outputs" --user "Alice"
```

Example:
```bash
gitlord push "Add new VPC module with subnet outputs"
```

After running, your browser will automatically open the merge request creation page.

### 3. Amend the last commit and force‑push (Phase 3) (OPTIONNAL)
```bash
gitlord amend [--branch <branch>]
```
- Stages all changes.
- Amends the previous commit without changing its message (--no-edit).
- Force‑pushes with --force-with-lease to avoid overwriting remote work accidentally.

### 4. Switch to master/main branch and pull latest (Phase 4)
```bash
gitlord done
```
- Detects the default branch (master or main).
- Checks out the default branch.
- Pulls the latest changes from origin.

Example:
```bash
gitlord done
```
This is useful after completing feature work to sync your local repository with the latest main/master branch.

Example:
```bash
gitlord amend
```

## Logging

All actions – successful or otherwise – are written to /tmp/gitlord.log with a timestamp and log level (DEBUG, INFO, ERROR).

### Log rotation

When the log file exceeds 20 MiB, GitLord automatically:

- Deletes any existing /tmp/gitlord.log.zip.
- Compresses the current log into /tmp/gitlord.log.zip.
- Starts a fresh /tmp/gitlord.log.
- This keeps the log tidy and prevents it from consuming too much disk space.

If you ever need to inspect a rotated log, simply unzip it:
```bash
unzip -p /tmp/gitlord.log.zip
```

## Error handling

GitLord validates every step:

- Dirty working tree – You will be asked to commit or stash before starting a new branch.
- No changes to commit/amend – The script raises a clear error and stops.
- Git command failures – Errors are captured, displayed in red, and logged.
- Detached HEAD – Detects and aborts.
- Missing remote branch – If the local base branch doesn’t exist, GitLord creates it from origin.
- If anything goes wrong, the script exits with a non‑zero status and prints the error to stderr. The full details are always available in the log file.

Troubleshooting

| Issue | Likely fix |
|-------|-------------|
| `git: command not found` | Install Git or adjust your PATH. |
| `Working tree is dirty` | Commit or stash changes before running `gitlord start`. |
| `Cannot detect default branch` | Explicitly use `--base main` or `--base master`. |
| Merge request URL not opened | Your GitLab remote might not output the MR URL; create it manually via the GitLab UI. |
| Colours not showing | You’re probably redirecting output to a file – colour is only active in a real terminal. |

## Example workflow
```bash
# Inside your Terraform repo folder in VSCode’s integrated terminal
gitlord start feat/azure-vnet

# ... make your changes ...

gitlord push "Implement Azure VNet module"

# ... review the automatically opened merge request ...

# Oops, need to fix something? Make your edits, then:
gitlord amend
```

## License

This project is provided as‑is under the MIT License. Feel free to modify and use it in your own team.

If you LOVE this tool, STAR it or buy me a coffee.
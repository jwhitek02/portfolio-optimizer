# Getting Started: Setup & Week 1

Exact commands to go from "nothing installed" to "Week 1 done and pushed to GitHub." Written for Windows (PowerShell). Run each command, in order, in the same terminal window unless noted otherwise.

## Before you start: check what you already have

Open PowerShell (Start menu → type "PowerShell" → Enter) and run:

```
python --version
```

If you see something like `Python 3.11.4`, you're good — skip to the Git check below. If you get an error or "Python was not found":

1. Go to https://www.python.org/downloads/ and download the installer
2. On the first installer screen, check the box **"Add python.exe to PATH"** before clicking Install — this step is easy to miss and causes most "command not found" problems later
3. Close and reopen PowerShell, then re-run `python --version` to confirm

Now check Git:

```
git --version
```

If missing, install from https://git-scm.com/downloads (defaults are fine on every screen).

Finally, if you don't already have one, create a free account at https://github.com — you'll need it in Step 7.

## Step 1: Open a terminal in the project folder

In File Explorer, navigate to:

```
C:\Users\jwhit\Claude\Projects\Finance Project\portfolio-optimizer
```

Click the address bar, type `powershell`, press Enter. This opens PowerShell already pointed at that folder. Confirm with:

```
dir
```

You should see `fetch_data.py`, `README.md`, `requirements.txt`, `.gitignore`, `WEEK1_WALKTHROUGH.md`.

## Step 2: Create a virtual environment

```
python -m venv .venv
```

This creates a `.venv` folder — a private set of installed libraries just for this project. It's normal to see it appear in File Explorer; `.gitignore` already excludes it from git.

## Step 3: Activate the virtual environment

```
.venv\Scripts\Activate.ps1
```

Success looks like your prompt now starting with `(.venv)`.

> If you get a "running scripts is disabled on this system" error, run this once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then try activating again.

You'll need to repeat this activation step every time you open a new terminal for this project — it doesn't stay on permanently.

## Step 4: Install the project's libraries

```
pip install -r requirements.txt
```

This installs pandas, yfinance, and everything else listed in `requirements.txt` into `.venv`. Takes a minute; a wall of text scrolling by is normal.

## Step 5: Run the Week 1 script

```
python fetch_data.py
```

Expected output: a line listing the 11 tickers being downloaded, then (after a few seconds) a row/column count and a ranked list of cumulative returns.

## Step 6: Check the output

```
dir data
```

You should see `raw_prices.csv`, `daily_returns.csv`, and `cumulative_returns.csv`. Open one in Excel and confirm it has dates down the left and tickers across the top with numbers in between.

If anything errors in Step 5 or 6, copy the exact error message back to me and I'll fix it.

## Step 7: Commit your work with git

```
git init
git add .
git commit -m "Week 1: data pipeline"
```

What each line does: `git init` turns this folder into a git repo. `git add .` stages every file (except what `.gitignore` excludes). `git commit` saves a permanent snapshot with a description.

> First time using git on this machine? It'll ask you to set an identity — run these once: `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"`.

## Step 8: Push to GitHub

1. Go to https://github.com/new
2. Repository name: `portfolio-optimizer`
3. Leave "Initialize this repository with a README" **unchecked** — you already have one
4. Click "Create repository"
5. Copy the URL GitHub shows you (looks like `https://github.com/<your-username>/portfolio-optimizer.git`)
6. Back in your terminal:

```
git remote add origin <paste-the-url-here>
git branch -M main
git push -u origin main
```

7. Refresh the GitHub page in your browser — your files should now show up there. This is the link you'll eventually put on your resume.

## Week 1 done-checklist

- [ ] `python fetch_data.py` runs with no errors
- [ ] `data/` contains the three CSVs with reasonable-looking numbers
- [ ] Code is pushed to GitHub and visible at your repo URL

## Common hiccups

- `'python' is not recognized...` — Python isn't on PATH. Reinstall and check the PATH box, or try `py` instead of `python` in every command above.
- `pip install` fails on `PyPortfolioOpt` — it's not needed until Week 3. If it's blocking you now, delete that line from `requirements.txt`, rerun `pip install -r requirements.txt`, and revisit it later.
- yfinance returns empty data or a JSON error — usually a temporary Yahoo Finance hiccup. Wait a minute and rerun `python fetch_data.py`.
- `git push` asks you to sign in — a browser window should pop up to authenticate with GitHub; follow the prompt.

## Next

Once everything above is checked off, let me know and we'll do the same step-by-step for Week 2 (risk & return analytics).

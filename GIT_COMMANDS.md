# Git Commands Cheat Sheet

Quick reference for all Git commands you'll need for this project.

---

## 🚀 Initial Setup (One Person Does This Once)

```bash
# Navigate to project directory
cd f:\medilink4

# Initialize Git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Complete hospital management system"

# Create GitHub repository on website first, then:
git remote add origin https://github.com/YOUR_USERNAME/medilink-hospital.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 👥 Team Members Setup (Everyone Does This)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/medilink-hospital.git
cd medilink-hospital

# OR if you already have the code, just add remote:
git remote add origin https://github.com/YOUR_USERNAME/medilink-hospital.git
git pull origin main
```

---

## 🌿 Create Your Feature Branch

### Option 1: Use the Setup Script (Easiest!)
```bash
# Just double-click:
setup_member.bat

# Choose your number and it does everything!
```

### Option 2: Manual Commands
```bash
# Mahtab
git checkout -b feature/mahtab-patient-auth

# Al Mamun Oualid
git checkout -b feature/oualid-doctor-features

# Prottoy
git checkout -b feature/prottoy-admin-features

# Mahieer Haai
git checkout -b feature/mahieer-patient-features
```

---

## 📝 Making Changes

```bash
# Check which branch you're on
git branch

# Check what files changed
git status

# Add all changes
git add .

# Or add specific files
git add docs/YourName_features.md
git add tests/test_YourName_features.py

# Commit with a message
git commit -m "Add documentation for F6 and F7"

# Push to GitHub
git push -u origin feature/your-branch-name

# For subsequent pushes (after first push):
git push
```

---

## 🔄 Updating Your Branch

```bash
# Get latest changes from main
git checkout main
git pull origin main

# Go back to your branch
git checkout feature/your-branch-name

# Merge main into your branch (if needed)
git merge main
```

---

## 📊 Checking Status

```bash
# See current branch and changed files
git status

# See commit history
git log --oneline

# See what changed in files
git diff

# See branches
git branch -a
```

---

## 🆘 Common Fixes

### Undo Changes (Before Commit)
```bash
# Undo changes to a specific file
git checkout -- filename.md

# Undo all changes
git reset --hard
```

### Fix Last Commit Message
```bash
git commit --amend -m "New commit message"
```

### Switch Branches
```bash
# Switch to existing branch
git checkout branch-name

# Create and switch to new branch
git checkout -b new-branch-name
```

### See Remote URL
```bash
git remote -v
```

### Change Remote URL
```bash
git remote set-url origin https://github.com/NEW_USERNAME/medilink-hospital.git
```

---

## 📤 Creating Pull Request

```bash
# 1. Make sure everything is committed and pushed
git status  # Should say "nothing to commit"
git push

# 2. Go to GitHub website
# 3. Click "Pull Requests" → "New Pull Request"
# 4. Select your branch
# 5. Add title and description
# 6. Click "Create Pull Request"
```

---

## ✅ Complete Workflow Example

```bash
# 1. Create your branch (or use setup_member.bat)
git checkout -b feature/mahtab-patient-auth

# 2. Make your changes (edit files, add documentation)

# 3. Check what changed
git status

# 4. Add all changes
git add .

# 5. Commit with clear message
git commit -m "Add documentation and tests for F6 and F7 - Patient Authentication"

# 6. Push to GitHub
git push -u origin feature/mahtab-patient-auth

# 7. Create Pull Request on GitHub website

# Done! ✅
```

---

## 🎯 Best Practices

### Good Commit Messages
✅ **Good:**
- "Add documentation for F6 and F7"
- "Add screenshots for patient registration"
- "Fix typo in patient login documentation"

❌ **Bad:**
- "update"
- "changes"
- "asdf"

### Commit Frequently
- After completing documentation for one feature
- After adding screenshots
- After testing and documenting results
- Don't wait until everything is done!

### Before Pushing
```bash
# Always check what you're committing
git status
git diff

# Make sure you're on the right branch
git branch
```

---

## 🆘 Emergency Commands

### I'm on the Wrong Branch!
```bash
# Don't commit! Just switch branches
git checkout correct-branch-name

# If you already committed, move the commit:
git checkout correct-branch-name
git cherry-pick commit-hash
```

### I Need to Start Over
```bash
# Delete your branch and start fresh
git checkout main
git branch -D feature/your-branch-name
git checkout -b feature/your-branch-name
```

### I Committed to Main by Mistake!
```bash
# Create a new branch with your changes
git branch feature/your-branch-name

# Reset main to remote
git checkout main
git reset --hard origin/main

# Go to your feature branch
git checkout feature/your-branch-name
```

---

## 📞 Getting Help

```bash
# Help for any command
git help <command>

# Example:
git help commit
git help push
```

---

## 🎓 Git Glossary

- **Repository (repo):** Your project folder with Git tracking
- **Branch:** A separate version of your code
- **Commit:** Saving your changes with a message
- **Push:** Sending commits to GitHub
- **Pull:** Getting changes from GitHub
- **Clone:** Copying a repository from GitHub
- **Merge:** Combining branches
- **Pull Request (PR):** Asking to merge your branch into main

---

**Remember:** Git is just a way to save and share your work. Don't overthink it! 🚀

*For this project, you mainly need: checkout, add, commit, push*

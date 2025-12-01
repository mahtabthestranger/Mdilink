@echo off
REM Quick Setup Script for Team Members
REM Run this script to set up your development environment quickly

echo ========================================
echo Medilink Hospital Management System
echo Team Member Setup Script
echo ========================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo Git initialized!
) else (
    echo Git repository already initialized.
)

echo.
echo ========================================
echo Choose your team member:
echo ========================================
echo 1. Mahtab (F6, F7 - Patient Auth)
echo 2. Al Mamun Oualid (F3, F4, F5 - Doctor Features)
echo 3. Prottoy (F1, F2 - Admin Features)
echo 4. Mahieer Haai (F8, F9 - Patient Features)
echo ========================================
echo.

set /p choice="Enter your number (1-4): "

if "%choice%"=="1" (
    set BRANCH_NAME=feature/mahtab-patient-auth
    set MEMBER_NAME=Mahtab
    set FEATURES=F6, F7 - Patient Registration and Login
) else if "%choice%"=="2" (
    set BRANCH_NAME=feature/oualid-doctor-features
    set MEMBER_NAME=Al Mamun Oualid
    set FEATURES=F3, F4, F5 - Doctor Login, Appointments, Medical Records
) else if "%choice%"=="3" (
    set BRANCH_NAME=feature/prottoy-admin-features
    set MEMBER_NAME=Prottoy
    set FEATURES=F1, F2 - Admin Login and Doctor Management
) else if "%choice%"=="4" (
    set BRANCH_NAME=feature/mahieer-patient-features
    set MEMBER_NAME=Mahieer Haai
    set FEATURES=F8, F9 - Patient Appointments and Medical History
) else (
    echo Invalid choice! Please run the script again.
    pause
    exit /b
)

echo.
echo ========================================
echo Setting up for: %MEMBER_NAME%
echo Features: %FEATURES%
echo Branch: %BRANCH_NAME%
echo ========================================
echo.

REM Create docs directory if it doesn't exist
if not exist "docs" mkdir docs

REM Create tests directory if it doesn't exist
if not exist "tests" mkdir tests

REM Check if we're already on the branch
git rev-parse --verify %BRANCH_NAME% >nul 2>&1
if %errorlevel% equ 0 (
    echo Branch %BRANCH_NAME% already exists. Switching to it...
    git checkout %BRANCH_NAME%
) else (
    echo Creating new branch: %BRANCH_NAME%
    git checkout -b %BRANCH_NAME%
)

echo.
echo ========================================
echo Setup Complete! ✓
echo ========================================
echo.
echo Next steps:
echo 1. Edit your documentation file in: docs\%MEMBER_NAME%_features.md
echo 2. Add your test cases in: tests\test_%MEMBER_NAME%_features.py
echo 3. Test your features by running: python app.py
echo 4. Commit your changes: git add . && git commit -m "Your message"
echo 5. Push to GitHub: git push -u origin %BRANCH_NAME%
echo.
echo ========================================
echo Happy coding! 🚀
echo ========================================
echo.

pause

@ECHO OFF
REM Medilink Admin Routes - Sphinx Documentation Build Script
REM
REM Usage: make.bat [target]
REM Targets: html, pdf, clean, help, all
REM

pushd %~dp0

REM Configuration
set SPHINXOPTS=
set SPHINXBUILD=sphinx-build
set SOURCEDIR=docs\source
set BUILDDIR=docs\build

REM Check if sphinx-build is available
where %SPHINXBUILD% >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Sphinx is not installed or not in PATH
    echo.
    echo Please install Sphinx using:
    echo   pip install sphinx sphinx-rtd-theme
    echo.
    pause
    exit /b 1
)

REM Display help
if "%1"=="help" goto help

REM Clean build directory
if "%1"=="clean" (
    echo Cleaning build directory...
    rmdir /s /q %BUILDDIR% 2>nul
    echo Clean complete.
    goto :EOF
)

REM Build HTML documentation
if "%1"=="html" goto html
if "%1"=="" goto html

REM Build PDF documentation
if "%1"=="pdf" goto pdf

REM Build all formats
if "%1"=="all" (
    goto html
)

REM Default - display help
:help
echo Medilink Admin Routes - Sphinx Documentation
echo.
echo Usage: make.bat [target]
echo.
echo Targets:
echo   html        Build HTML documentation (default)
echo   pdf         Build PDF documentation
echo   clean       Clean build directory
echo   help        Display this help message
echo.
echo Examples:
echo   make.bat                 - Build HTML documentation
echo   make.bat clean           - Clean build directory
echo   make.bat html            - Build HTML documentation
echo   make.bat pdf             - Build PDF documentation
echo.
goto :EOF

:html
echo Building HTML documentation...
%SPHINXBUILD% -b html %SOURCEDIR% %BUILDDIR%\html
if errorlevel 1 (
    echo.
    echo ERROR: HTML build failed
    pause
    exit /b 1
)
echo.
echo HTML documentation built successfully!
echo View the documentation at: %BUILDDIR%\html\index.html
echo.
start %BUILDDIR%\html\index.html
goto :EOF

:pdf
echo Building PDF documentation...
echo.
echo Note: PDF generation requires LaTeX installation
echo Install MiKTeX from: https://miktex.org/
echo.
%SPHINXBUILD% -b latex %SOURCEDIR% %BUILDDIR%\latex
if errorlevel 1 (
    echo.
    echo ERROR: LaTeX build failed
    pause
    exit /b 1
)
echo.
cd %BUILDDIR%\latex
echo Running LaTeX...
make
cd ..\..
echo.
echo PDF documentation built successfully!
echo PDF location: %BUILDDIR%\latex\medilink_admin_routes.pdf
echo.
goto :EOF

:error
echo An error occurred during documentation build.
pause
exit /b 1

popd

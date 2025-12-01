@echo off
echo Building Sphinx Documentation for Al Mamun Oualid's Features...
echo.

cd sphinx

echo Installing dependencies...
pip install -r ../requirements_docs.txt

echo.
echo Building HTML documentation...
sphinx-build -b html . _build/html

echo.
echo Documentation built successfully!
echo Open: sphinx\_build\html\index.html
echo.

pause

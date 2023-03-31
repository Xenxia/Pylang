@echo off


python setup.py bdist_wheel
cd dist
for %%i in (*-py3-none-any.whl) do set TEST=%%~i

pip install %TEST% --force-reinstall
cd ..
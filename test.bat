    rm aimodels.json
    @REM Init
    py.exe .\main.py init
    py.exe .\main.py list
    @REM Install, Add to aimodels, remove, uninstall
    py.exe .\main.py install BSRGAN
    py.exe .\main.py add BSRGAN
    py.exe .\main.py remove BSRGAN:1.0
    py.exe .\main.py uninstall BSRGAN

    py.exe .\main.py add GFPGAN
    py.exe .\main.py remove GFPGAN:1.4
    py.exe .\main.py uninstall GFPGAN
    @REM py.exe .\main.py install anothe-aimodel
    @REM py.exe .\main.py add GFPGAN
    @REM py.exe .\main.py uninstall GFPGAN
    cat aimodels.json
    @REM py.exe .\main.py info Codeformer
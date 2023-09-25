from cx_Freeze import setup, Executable
import sys

base = "Win32GUI" if sys.platform == "win32" else None

build_exe_options = {
    "packages": ["PyQt5", "sys"],
    "include_files": ["protector.ui", "bg.png", "pdficon.ico"],
    "include_msvcr": True
}

setup(
    name="PdfProtect",
    author="Agnivo\'s Software Corporation",
    description="PdfProtect",
    options= {"build_exe": build_exe_options},
    executables = [
        Executable(
            "protecter.py",
            base=base,
            icon="pdficon.ico",
            target_name="pdfsecure"
        )
    ]
)
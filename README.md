# ImputeApp
Desktop app for treating missing values in datasets

## Builidng for Linux (on Linux)

Prepare a virtual environment and use pip to install imputena and pyinstaller:

```ShellSession
pip install imputena
pip install pyinstaller
```

This is only necessary once. Inside the virtual environment, run the following
command to build the application for macOS at the project root directory:

```ShellSession
pyinstaller --onefile ImputeApp-Linux.spec
```

Explanation:

* onefile indicates that we want a single executable file
* pyinstaller is called on the .spec instead of the .py because the .spec
 includes information about hidden imports
 
The executable file will be located in the dist directory.


## Building for macOS (on macOS)

Prepare a virtual environment and use pip to install imputena and pyinstaller:

```ShellSession
pip install imputena
pip install pyinstaller
```

This is only necessary once. Inside the virtual environment, run the following
command to build the application for macOS at the project root directory:

```ShellSession
pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' --windowed --noconfirm ImputeApp-macOS.spec
```

Explanation:

* onefile indicates that we want a single executable file
* the two add-binary are necessary to avoid problems with tkinter ([See
 stackoverflow](https://stackoverflow.com/a/56503307))
* windowed indicates that we want a .app
* noconfirm indicates that any old build should be overwritten without
 confirmation
* pyinstaller is called on the .spec instead of the .py because the .spec
 includes information about hidden imports
 
 The executable file will be located in the dist directory.
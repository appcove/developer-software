## How the build process works

Each script is indipendent and is responsable for the construction of a `.deb` file. The source code of the program with the same name as the build script should be compiled, inserted inside a folder with the `control` file and then at last dpkg is called to build the package, which *MUST* be placed in the `./temp` directory.
# GTIT (Genealogy Tree In Terminal)

**GTIT** is a **python** command-line tool to read _GEDCOM (.GED)_ files. It can display small genealogical tree directly in a terminal, list individuals in a .GED file, etc.

### Goals
- [x] Parse .GED files
- [x] List individuals in the .GED file
- [x] Build basic tree (from root, to parents)
- [x] Build more complex trees (brotherhoods)
- [ ] Build _even_ more complex trees (rebuilt families for example)


## Usage

As of now, you need to have Python 3 installed to use **GTIT**.
```
    python3 gtit.py <MODE> <OPTIONS> <FILEPATH>
```

You can find use-cases examples in [example.md](./example/example.md)


## Known problems
- The graph use the width of your terminal to draw the tree, so requesting trees with a high depth could result in weirdness in the tree. I'd recommand sticking to depths between -2 and 3.
- Sometimes, the wrong character is used for the line splits and crosses.


## Build
GTIT uses [pyinstaller](https://pypi.org/project/pyinstaller/) to be bundled in a single package.
To package **GTIT**, simply execute the `build.sh` file. It will create multiple directories:
- `dist` will contain a `gtit` directory. You can copy this directory on your system, add the path to the executable `gtit` in the PATH variable, and you've got **GTIT** installed!
- `package` will contain a compressed archive of the `dist/gtit` directory.
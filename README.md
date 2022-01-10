# GTIT (Genealogy Tree In Terminal)

GTIT is a **python** command-line tool to read _GEDCOM (.GED)_ files. It can display small genealogical tree directly in a terminal, list individuals in a .GED file, etc.

### Goals
- [x] Parse .GED files
- [x] List individuals in the .GED file
- [x] Build basic tree (from root, to parents)
- [ ] Build more complex trees (brotherhoods)
- [ ] Build _even_ more complex trees (rebuilt families for example)


## Usage

As of now, you need to have Python 3 installed to use GTIT.
```
    python3 gtit.py <MODE> <OPTIONS> <FILEPATH>
```

You can find use-cases examples in [example.md](./example/example.md)
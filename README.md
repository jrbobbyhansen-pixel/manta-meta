# Manta CLI

Unified interface for all 15 Manta CLI tools with pipe chain support.

## Install

```bash
pip install git+https://github.com/jrbobbyhansen-pixel/manta-meta.git
```

## Usage

```bash
# Run any Manta tool
manta toc README.md
manta qr "Hello, world!"
manta size /path/to/dir
manta dup ~/Downloads

# List all tools
manta list

# Pipe tools together
manta pipe toc dup -- README.md
manta pipe hash envlock -- .env

# Version
manta --version
```

## Tools

| Tool     | Description                          |
|----------|--------------------------------------|
| toc      | Generate table of contents from md   |
| qr       | Generate QR codes from terminal      |
| cheat    | Personal cheatsheet manager          |
| size     | Directory size analyzer              |
| envlock  | Lock .env files with checksum        |
| hash     | File hashing utility                 |
| todo     | CLI todo list manager                |
| json     | JSON processing tool                 |
| port     | Port availability checker            |
| cert     | SSL certificate inspector            |
| dup      | Duplicate file finder                |
| rename   | Batch file renamer                   |
| backup   | File backup utility                  |
| env      | Environment variable manager         |
| url      | URL parser and validator             |

## Pipe Chains

The `manta pipe` command chains tools together, passing each tool's output as the next tool's input:

```bash
manta pipe <tool1> <tool2> [tool3...] -- [final-args]
```

Example: hash a file, then lock the hash:
```bash
manta pipe hash envlock -- myfile.txt
```

## License

MIT

#!/usr/bin/env python3
"""manta — unified CLI for all Manta tools with pipe chain support.

Usage:
  manta <tool> [args...]       Run a Manta tool
  manta list                   List all available tools
  manta pipe <tool1> <tool2>   Pipe output of tool1 into tool2
  manta --version              Show version
  manta --help                 Show this help
"""

import subprocess
import sys
import shutil
from pathlib import Path

__version__ = "1.0.0"

# Tools that are pip-installable (available as system commands)
PIP_TOOLS = {
    "hash": "hash",
    "todo": "todo",
    "json": "json",
    "port": "port",
    "cert": "cert",
    "rename": "rename",
    "backup": "backup",
    "env": "env",
    "url": "url",
}

# Standalone tools (shipped as scripts, installed via pip from master branch)
STANDALONE_TOOLS = {
    "toc": "toc",
    "qr": "qr",
    "cheat": "cheat",
    "size": "size",
    "envlock": "envlock",
    "dup": "dup",
}

ALL_TOOLS = {**PIP_TOOLS, **STANDALONE_TOOLS}

# Tool descriptions for `manta list`
TOOL_DESCRIPTIONS = {
    "toc": "Generate table of contents from markdown",
    "qr": "Generate QR codes from terminal",
    "cheat": "Personal cheatsheet manager",
    "size": "Directory size analyzer",
    "envlock": "Lock .env files with checksum",
    "hash": "File hashing utility",
    "todo": "CLI todo list manager",
    "json": "JSON processing tool",
    "port": "Port availability checker",
    "cert": "SSL certificate inspector",
    "dup": "Duplicate file finder",
    "rename": "Batch file renamer",
    "backup": "File backup utility",
    "env": "Environment variable manager",
    "url": "URL parser and validator",
}


def find_tool(tool_name):
    """Find a tool by name, checking pip-installed commands first, then standalone scripts."""
    if tool_name in PIP_TOOLS:
        cmd = shutil.which(PIP_TOOLS[tool_name])
        if cmd:
            return cmd
    if tool_name in STANDALONE_TOOLS:
        cmd = shutil.which(STANDALONE_TOOLS[tool_name])
        if cmd:
            return cmd
    return None


def run_tool(tool_name, args, stdin_data=None):
    """Run a tool with optional stdin data. Returns (returncode, stdout, stderr)."""
    cmd = find_tool(tool_name)
    if not cmd:
        return (1, "", f"Error: tool '{tool_name}' not found. Try 'manta list'.")

    try:
        proc = subprocess.run(
            [cmd] + args,
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return (proc.returncode, proc.stdout, proc.stderr)
    except FileNotFoundError:
        return (1, "", f"Error: tool '{tool_name}' is not installed. Run: pip install manta-{tool_name}")
    except subprocess.TimeoutExpired:
        return (1, "", f"Error: tool '{tool_name}' timed out after 30 seconds")


def cmd_list():
    """List all available Manta tools with descriptions."""
    print(f"Manta CLI v{__version__} — {len(ALL_TOOLS)} tools")
    print()
    for name in sorted(ALL_TOOLS):
        desc = TOOL_DESCRIPTIONS.get(name, "")
        installed = "✓" if find_tool(name) else " "
        print(f"  [{installed}] {name:12s}  {desc}")
    print()
    print("Usage: manta <tool> [args...]")
    print("       manta pipe <tool1> <tool2> [args...]")


def cmd_pipe(args):
    """Pipe the output of one tool into another."""
    if len(args) < 2:
        print("Usage: manta pipe <tool1> <tool2> [tool3...] [-- <final-args>]", file=sys.stderr)
        return 1

    # Find the split point for final args
    if "--" in args:
        split_idx = args.index("--")
        pipe_chain = args[:split_idx]
        final_args = args[split_idx + 1:]
    else:
        pipe_chain = args
        final_args = []

    if len(pipe_chain) < 2:
        print("Error: pipe chain needs at least 2 tools", file=sys.stderr)
        return 1

    # First tool gets no stdin
    stdin_data = None
    for i, tool_name in enumerate(pipe_chain):
        tool_args = final_args if i == len(pipe_chain) - 1 else []
        rc, stdout, stderr = run_tool(tool_name, tool_args, stdin_data)

        if stderr:
            print(stderr, file=sys.stderr, end="")

        if rc != 0:
            return rc

        # Pass stdout as stdin to next tool
        stdin_data = stdout

    # Print final output
    if stdin_data:
        print(stdin_data, end="")

    return 0


def cli():
    """Main entry point."""
    if not sys.argv[1:]:
        print("Usage: manta <tool> [args...]")
        print("       manta list")
        print("       manta pipe <tool1> <tool2> [args...]")
        print(f"       manta --version")
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "--version" or cmd == "-v":
        print(f"manta v{__version__}")
        sys.exit(0)

    if cmd == "--help" or cmd == "-h":
        print(__doc__.strip())
        sys.exit(0)

    if cmd == "list":
        cmd_list()
        sys.exit(0)

    if cmd == "pipe":
        rc = cmd_pipe(args)
        sys.exit(rc)

    # Run a specific tool
    if cmd in ALL_TOOLS:
        rc, stdout, stderr = run_tool(cmd, args)
        if stdout:
            print(stdout, end="")
        if stderr:
            print(stderr, file=sys.stderr, end="")
        sys.exit(rc)
    else:
        print(f"Error: unknown tool '{cmd}'. Try 'manta list' for available tools.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    cli()

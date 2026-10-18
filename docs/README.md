---
title: LED Head Tracking Psychopy Plugin 
authors:
   joe_starr
---

![PyPI Version](https://img.shields.io/pypi/v/psychopy-ledstrip)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](<https://opensource.org/licenses/MIT>)

![hero](./infra/assets/logo.svg)

[![White Logo image](https://brainmade.org/white-logo.svg)](https://brainmade.org)

## Install

To install in a Psychopy Studio environment run the following:

### Command Prompt

```batch
cd %appdata%\psychopy4
.uv\uv.exe pip install psychopy-ledstrip --python .\.python\2026.1.3
```

### PowerShell  

```batch
cd $env:APPDATA\psychopy4
./.uv/uv.exe pip install psychopy-ledstrip --python ./.python/2026.1.3
```

## Note to Reader

### What Am I?

### About the Documentation

The following document describes the "rules" and expectation for the tool. The
["Code Comments"](./lib/files/) page contains the technical context descriptions found in the source
files. The ["Use Cases"](./use_cases/) page contains a collection of use cases and a use case
diagram for the tool. The ["Decisions"](./madr/) page contains a collection of
[architectural decision records](https://adr.github.io/madr/) [@Kopp2018] giving context on why this
tool is the way it is.

### Issues

If you discover an issue with this repository or have a question, please feel free to open an issue.
I've included templates for the following issues:

- 🖋️ Spelling and Grammar: Found some language that is incorrect?
- 🤷 Clarity: Found a section that just makes no sense?
- ❓ Question: Do you have a general question?
- 🐞 Bug: Found an error in the code?
- 🚀 Enhancement: Have a suggestion for improving the toolchain?

[:fontawesome-solid-paper-plane: Open Issue!](https://github.com/Joecstarr/itt_2_plpath_converter/issues/new/choose){ .md-button }

## 📃 Cite Me

## ⚖️ License

## Planning and Administration

### Tasks

Tasks are tracked as GitHub issues.

### Version Control

The toolchain shall be kept under Git versioning. Development shall take place on branches with
`main` on GitHub as a source of truth. GitHub pull requests shall serve as the arbiter for inclusion
on main with the following quality gates:

- Running and passing the unit test suite.
- Running and passing linting and style enforcers.
- Successful generation of documentation.

#### Release Tagging

The project shall be tagged when a new feature or bug fix is merged into main. The tag shall follow
[semantic versioning](https://semver.org) for labels.

```text
vMAJOR.MINOR.PATCH
```

### Project Structure

Files and directories shall be lower case, where capital is not required by a tool, and contain no
`' '`.

```text
📁 .
├── 📁 .github
│   ├── 📁 ISSUE_TEMPLATE
│   ├── 📁 PULL_REQUEST_TEMPLATE
│   ├── 📁 workflows
│   └── 📝 pull_request_template.md
├── 📁 .vscode
│   └── ⚙️ launch.json
├── 📁 docs
│   ├── 📁 content
│   │   ├── 📁 madr
│   │   └── 📁 units
│   ├── 📁 infra
│   └── 📖 README.md
├── 📁 psychopy_ledstrip 
│   ├── 📁 component 
│   ├── 📁 hardware 
│   ├── 📁 wrapper 
│   └── 🐍 __init__.py
├── 📁 test 
│   ├── 📁 component 
│   ├── 📁 hardware 
│   ├── 📁 wrapper 
│   ├── 🐍 test_<unit>.py 
│   └── 🐍 __init__.py
├── ⚙️ .editorconfig
├── 🙈 .gitignore
├── 🛠️ .pre-commit-config.yaml
├── ⚙️ .rumdl.toml
├── ❄️ flake.lock
├── ❄️ flake.nix
├── 🛠️ Justfile
├── 📜 LICENSE
├── 📄 mkdocs.yml
├── 🐍 pyproject.toml
└── 🔒 uv.lock
```

### Directories of Interest

- docs: This directory contains the high level documentation for the tool.
- psychopy_ledstrip : This directory contains the source code of the tool.
- test: This directory contains the test code of the tool.
- .github: This directory contains the GitHub infrastructure.  
- .vscode: This directory contains the debugger configuration.  

### Define a Unit

### Quality

The tool and its units shall fail-safe, that is the tool and its units can fail, but the failure
must be detectable. A segfault is okay, an off by one error that computes the wrong value is not.

#### Unit Testing

Each internal unit shall have a unit test suite.

#### Integration Testing

The plugin shall have manual integration testing.

### Requirements

There will be no unit testings for the project.

#### Functional Requirements

Requirements are documented by [ADR](./content/madr/index.md). Use cases not covered by generated
code are omitted as they follow the PsychoPy plugin design requirements.

```mermaid
flowchart LR
  aT["👤 Time"]

  CLS(["Command LED State"])
  CLF(["Command LED Off"])
  CLN(["Command LED On"])
  SLS(["Setup LED Strip"])
  RLS(["Reset LED Strip"])
  GFP(["Get Fastrak Position"])

  aT --> CLN 
  aT --> CLF
  aT --> SLS 
  aT --> RLS 
  aT --> GFP 

  CLN -. include .-> CLS
  CLF -. include .-> CLS
```

##### Architectural Decisions

Architectural decisions [MADR](<https://github.com/adr/madr>) [@Kopp2018] serve as the primary
documentation for architectural decisions.

The following is the order of operations for the proposal of a MADR:

1. Create a branch for a proposal with the name:

    ```text
    proposal-{{short title}}
    ```

1. Create a pull request with this template.
1. In the branch create a Markdown file based on the
    [MADR Template](https://github.com/adr/madr/blob/4.0.0/template/adr-template.md). Name the
    Markdown file:

    ```text
    {{issue# padded to five digits}}-{{title}}
    ```

1. When a decision is made change the status to:
    - "accepted" and pull the branch into main branch
    - "rejected" and pull the branch into main branch

#### Nonfunctional Requirements

##### Colors

Diagrams included in documentation for features (use case and unit descriptions) are expected to use
the [COLORS](https://clrs.cc) color palette.

##### Technologies

###### Languages and Frameworks

- git
- mermaid.js
- prek
- tombi
- rumdl
- ruff
- uv
- MADR[@Kopp2018]

###### Documentation of Implementation

Matches the [psychopy-fastrak](https://github.com/Nontrivial-Solutions/psychopy-fastrak) plugin.

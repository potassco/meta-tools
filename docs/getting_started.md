---
hide:
  - navigation
---

# Getting started

## Installation

=== "Pip"

    ```console
    pip install meta-tools-clingo
    ```

=== "Development mode"

    ```console
    git clone https://github.com/potassco/meta_tools.git/
    cd meta_tools
    pip install -e .[all]
    ```

    !!! warning
        Use only for development purposes

## Usage

### Command line interface

Details about the command line usage can be found with:

```console
reify -h
```

This command will show the available options and extensions.

The output of the reification will be printed to standard output. To save it to a file, use output redirection:

```console
reify input.lp > reified_output.lp
```

By default, both the [TagExtension](./reference/extensions/tag.md) and [ShowExtension](./reference/extensions/show.md) are enabled.

---
hide:
  - navigation
  - toc
---

# meta_tools

A compilation of tools for working with ASP meta programming.
It provides an API to extend the reification of ASP programs with custom information. Using this api two extensions are provided:

- **TagExtension**: An extension to use comment directives to tag rules in the reified program. This can also be used to make sure all rules have distinct identifiers.
- **ShowExtension**: An extension to remove show statements from the reified program and handle them separately. This allows a clear mapping from literal numbers to symbols.


!!! info
    *meta_tools* is part of the [Potassco](https://potassco.org) suite.

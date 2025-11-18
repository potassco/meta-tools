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

!!! example
    Consider the example in `examples/test`

    ```clingo
    % @domain :: a(X)

    {a(1)}.
    % @myrule
    b(X):-a(X).
    #show b/1.
    ```

    Using the command line one can reify the program with:

    ```
    > reify examples/test/encoding.lp --clean > reified_output.lp
    ```

    ```clingo
    symbol_literal(a(1),3).
    symbol_literal(b(1),6).
    show_hide.
    show(b(1),3).
    tag(rule(choice(1),normal(1)),rule_fo("{ a(1) }.")).
    tag(rule(disjunction(2),normal(2)),myrule).
    tag(rule(disjunction(2),normal(2)),rule_fo("b(X) :- a(X).")).
    tag(atom(3),domain).
    rule(disjunction(0),normal(0)).
    rule(choice(1),normal(1)).
    rule(disjunction(2),normal(2)).
    literal_tuple(2,3).
    literal_tuple(3,6).
    literal_tuple(5,3).
    literal_tuple(7,1).
    literal_tuple(0).
    literal_tuple(1).
    literal_tuple(2).
    literal_tuple(3).
    literal_tuple(5).
    literal_tuple(7).
    atom_tuple(0,1).
    atom_tuple(1,3).
    atom_tuple(2,6).
    atom_tuple(0).
    atom_tuple(1).
    atom_tuple(2).
    atom_tuple(4).

    ```

## Debugging

To help debugging we provide a `--log` option as well as `--save-out` to inspect the transformed program before reification and the full reified outout before cleaning.

## Visualization

To visualize the reified output we provide a [clingraph](https://clingraph.readthedocs.io/en/latest/) integration
This option can be added with `--view`, which will open a browser with the visualization.


!!! example

    ```console
    > reify examples/test/encoding.lp --clean --view
    ```

    ![Visualization Example](view.png)

## Mimic normal reification

To obtain the normal clingo reification one can use the tag `--classic`

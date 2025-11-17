---
icon: material/eye
---

# ShowExtension

Handles show statements in the reified program separately, allowing a clear mapping from literal numbers to symbols.
The extension will rewrite the show statements by adding a custom predicate `_show/1` and removing the show statements.

## Output Symbols

- `symbol_literal(Symbol, LiteralNumber)`: This atom maps each symbol in the reified program to its corresponding (positive) literal number.
- `show(Symbol, LiteralCondition)`: This atom indicates that the symbol is shown in the original program, if the conditional literal tuple identified by `LiteralCondition` holds.
- `show_hide`: This atom indicate that anything that was not explicitly show should be hidden. Like `#show.`.


!!! example

    ```prolog
    b(1..2).
    #show a(X):b(X).
    ```

    Transformed program is:

    ```prolog
    _show(a(X)):-b(X).
    ```

    Output of reification will include:

    ```prolog
    symbol_literal(b(1),2).
    symbol_literal(b(2),3).
    show(a(1),1).
    show(a(2),2).
    ```

    Notice that there is no mapping for `a(X)` since it is not part of the reified program.


!!! example

    ```prolog
    b(1..2).
    #show b/1.
    ```

    Transformed program is:

    ```prolog
    _show(b(X)):-b(X).
    _show.
    ```

    Output of reification will include:

    ```prolog
    symbol_literal(b(1),3).
    symbol_literal(b(2),4).
    show_hide.
    show(b(1),2).
    show(b(2),3).
    ```

    Notice that `show_hide` indicates that anything not explicitly shown should be hidden. This is present since show signatures automatically hide everything else.






!!! example

    ```prolog
    #show a/1.
    ```

    Reification is extended with the following atoms:
    ```prolog
    _show(a(X)):-a(X).
    _show.
    ```

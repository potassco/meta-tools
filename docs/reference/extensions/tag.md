---
icon: material/tag
---

# TagExtension

Uses comments to add tags to rules and atoms in the reified program.

## Tagging Rules

All tag comments before a rule are added as tags to that rule. Tag comments appear in a comment line starting with `@` followed by the tag.
The tag is a clingo symbol which can use variables that appear (safe) in the rule.

!!! example
    The following program adds the tags `mytag`  and `mytag(1)` to the rule `a:-b.`

    ```prolog
    % @mytag
    % @mytag(1)
    a:-b.
    b.
    ```

    Reification is extended with the following tag atoms:
    ```prolog
    tag(rule(disjunction(1),normal(1)),mytag(1)).
    tag(rule(disjunction(1),normal(1)),mytag).
    ```


!!! example
    The following program adds the tags `mytag`  and `mytag(1)` to the rule `a:-b.`

    ```prolog
    % @label("If {} is parent of {}, then {} is person.",(X,Y,X))
    person(X):-parent(X,Y).
    parent(anna,maria).
    ```

    Reification is extended with the following tag atom:
    ```prolog
    tag(rule(disjunction(1),normal(1)),label("If {} is parent of {}, then {} is person.",(anna,maria,anna))).
    ```

!!! warning
    Notice that the variables `X` and `Y` are replaced by their ground terms. But only if they are variables in the tag atom, not if they appear in a string like "X is parent of Y".


## Tagging Atoms

Tag comments can also be used to tag atoms in the reified program. This is specially helpful; to avoid the need of tagging rules coming form the input.

The atoms for tags are also symbols starting with `@` followed by the tag. But atom tags have the symbol `::` after the tag, followed by the atom to be tagged.

!!! example
    The following program adds the tags `domain` and `label("{} is a person", (P))` to the atoms `person(P)`.

    ```prolog
    % @label("{} is a person", (P)) :: person(P)
    % @domain :: person(P)

    person(anna;maria;juan).
    ```

    Reification is extended with the following tag atoms:
    ```prolog
    tag(atom(2),domain).
    tag(atom(3),domain).
    tag(atom(4),domain).
    tag(atom(2),label("{} is a person",juan)).
    tag(atom(3),label("{} is a person",maria)).
    tag(atom(4),label("{} is a person",anna)).
    ```

!!! note
    The atoms added to the reification use the internal atom ids assigned during grounding.

### Atom Tags with Conditions

Atom tags can also contain conditions. These are specified after symbol `:`

!!! example

    ```prolog
    % @label("{} is an adult", (P)) :: person(P) : age(P,A), A > 10
    % @label("{} is a child", (P)) :: person(P) : age(P,A), A <= 10
    % @domain :: person(P)

    person(anna;maria;juan).
    age(anna,20).
    age(maria,7).
    age(juan,25).
    ```

    Reification is extended with the following tag atoms:
    ```prolog
    tag(atom(8),domain).
    tag(atom(9),domain).
    tag(atom(10),domain).
    tag(atom(9),label("{} is a child",maria)).
    tag(atom(8),label("{} is an adult",juan)).
    tag(atom(10),label("{} is an adult",anna)).
    ```

    Notice how the tag `label("{} is a child", (P))` is only added to `person(maria)` since only for this atom the condition `age(P,A), A <= 10` holds.


## Default Tags

By default, the TagExtension adds tags to all rules with a string using the with the first order representation of the rule.

```prolog
a(X):-b(X).
```

is tagged as

```prolog
% @rule_fo("a(X):-b(X).")
a(X):-b(X).
```

!!! tip
    You can customize the tagging behavior using the `include_fo` and `include_loc` parameters when initializing the TagExtension.

!!! note
    Including these default tags will prevent grounding simplification so that multiple rules remain distinct. Otherwise, in a program like `person(anna). person(maria).`, both facts would be simplified the same literal number since they are true.

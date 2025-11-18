## People example

As an example we will consider the encoding in `examples/people.lp`.

`instance.lp`

```clingo
--8<-- "examples/people/instance.lp"
```

`encoding.lp`

```clingo
--8<-- "examples/people/encoding.lp"
```

Using the command line one can reify the program with:

```
> reify examples/people/encoding.lp examples/people/instance.lp --clean > reified_output.lp
```

`reified_output.lp`

```clingo
symbol_literal(person(susana),4).
symbol_literal(person(brais),5).
symbol_literal(height(susana,160),15).
symbol_literal(height(brais,180),17).
symbol_literal(drive(brais),2).
symbol_literal(drink(susana),9).
symbol_literal(drink(brais),11).
tag(rule(disjunction(0),normal(0)),rule_fo("drive(brais).")).
tag(rule(disjunction(1),normal(1)),rule_fo("person(susana;brais).")).
tag(rule(disjunction(2),normal(1)),rule_fo("person(susana;brais).")).
tag(rule(choice(3),normal(2)),disabled).
tag(rule(choice(3),normal(2)),rule_fo("{ drink(P) } :- person(P).")).
tag(rule(choice(3),normal(2)),label("{} might be drink",(susana,))).
tag(rule(choice(4),normal(3)),disabled).
tag(rule(choice(4),normal(3)),rule_fo("{ drink(P) } :- person(P).")).
tag(rule(choice(4),normal(3)),label("{} might be drink",(brais,))).
tag(rule(disjunction(5),normal(4)),rule_fo("#false :- drink(P); drive(P).")).
tag(rule(disjunction(5),normal(4)),label("{} can't drink and drive",(brais,))).
tag(rule(disjunction(6),normal(5)),rule_fo("height(susana,160).")).
tag(rule(disjunction(7),normal(6)),rule_fo("height(brais,180).")).
tag(atom(4),label("{} is a short person",(susana,))).
tag(atom(4),domain).
tag(atom(5),label("{} is a tall person",(brais,))).
tag(atom(5),domain).
tag(atom(15),label("{} is {} cm tall",(susana,160))).
tag(atom(17),label("{} is {} cm tall",(brais,180))).
tag(atom(2),label("{} is driving",(brais,))).
rule(disjunction(0),normal(0)).
rule(disjunction(1),normal(1)).
rule(disjunction(2),normal(1)).
rule(choice(3),normal(2)).
rule(choice(4),normal(3)).
rule(disjunction(5),normal(4)).
rule(disjunction(6),normal(5)).
rule(disjunction(7),normal(6)).
literal_tuple(2,4).
literal_tuple(3,5).
literal_tuple(4,2).
literal_tuple(4,11).
literal_tuple(14,4).
literal_tuple(15,5).
literal_tuple(16,15).
literal_tuple(17,17).
literal_tuple(18,2).
literal_tuple(19,9).
literal_tuple(20,11).
literal_tuple(0).
literal_tuple(1).
literal_tuple(2).
literal_tuple(3).
literal_tuple(4).
literal_tuple(5).
literal_tuple(6).
literal_tuple(14).
literal_tuple(15).
literal_tuple(16).
literal_tuple(17).
literal_tuple(18).
literal_tuple(19).
literal_tuple(20).
atom_tuple(0,2).
atom_tuple(1,4).
atom_tuple(2,5).
atom_tuple(3,9).
atom_tuple(4,11).
atom_tuple(6,15).
atom_tuple(7,17).
atom_tuple(0).
atom_tuple(1).
atom_tuple(2).
atom_tuple(3).
atom_tuple(4).
atom_tuple(5).
atom_tuple(6).
atom_tuple(7).
```

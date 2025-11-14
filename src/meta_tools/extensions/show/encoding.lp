show(X,B):-
    rule(disjunction(H),normal(B)),
    atom_tuple(H,L),
    symbol_literal(_show(X),L).



hide(rule(disjunction(H),normal(B))):-
    rule(disjunction(H),normal(B)),
    atom_tuple(H,L),
    symbol_literal(_show(X),L).
#show literal_tuple(B):
    rule(disjunction(H),normal(B)),
    atom_tuple(H,L),
    symbol_literal(_show(X),L).

hide(atom(L)):-
    rule(disjunction(H),normal(B)),
    atom_tuple(H,L),
    symbol_literal(_show(X),L).

hide(atom_tuple(H)):-
    rule(disjunction(H),normal(B)),
    atom_tuple(H,L),
    symbol_literal(_show(X),L).


#show show(X,B):show(X,B).

symbol_literal(F,L):- output(F,B), literal_tuple(B,L).
#show symbol_literal(F,L):symbol_literal(F,L).

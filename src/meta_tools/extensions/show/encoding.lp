% New predicates
show(X,B):-
    rule(disjunction(H),normal(B)),
    atom_tuple(H,L),
    symbol_literal(_show(X),L).

#show show(X,B):show(X,B).
#show show_hide:output(_show,B).

% Symbol table
symbol_literal(F,L):- output(F,B), literal_tuple(B,L).
aux_show_atom(_show(X)):- symbol_literal(_show(X),L).
aux_show_atom(_show):- symbol_literal(_show,L).
#show symbol_literal(F,L):symbol_literal(F,L), not aux_show_atom(F).


% Hiden predicates
% Hide rule but not the literal tuple
hide(rule(disjunction(H),normal(B))):-
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

hide(literal_tuple(B)):-
    literal_tuple(B,L),
    symbol_literal(_show(X),L).

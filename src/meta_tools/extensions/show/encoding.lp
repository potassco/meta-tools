% New predicates
explicit_show(X,B):-
    rule(disjunction(H),normal(B)),
    atom_tuple(H,L),
    symbol_literal(_show(X),L).

show_symbol(_show(X)):- output(_show(X), _).
show_symbol(_show):- output(_show, _).

#show show(X,B):explicit_show(X,B).
#show show(X,B):output(X,B), not output(_show, _).
% #show show_hide:output(_show,B).

% Symbol table
symbol_literal(F,L):- output(F,B), literal_tuple(B,L).
aux_show_atom(S):- symbol_literal(S,L), show_symbol(S).
#show symbol_literal(F,L):symbol_literal(F,L), not aux_show_atom(F).


% Hiden predicates
% Hide rule but not the literal tuple
hide(rule(disjunction(H),normal(B))):-
    rule(disjunction(H),normal(B)),
    atom_tuple(H,L),
    symbol_literal(S,L),
    show_symbol(S).

hide(atom(L)):-
    rule(disjunction(H),normal(B)),
    atom_tuple(H,L),
    symbol_literal(S,L),
    show_symbol(S).

hide(atom_tuple(H)):-
    rule(disjunction(H),normal(B)),
    atom_tuple(H,L),
    symbol_literal(S,L),
    show_symbol(S).

hide(literal_tuple(B)):-
    literal_tuple(B,L),
    symbol_literal(S,L),
    show_symbol(S).

hide(output(S,B)):-
    output(S,B),
    show_symbol(S).

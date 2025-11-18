% Transforms a reified program in to a program graph
%
% !!! warning Assumes one body for each rule, which is achieved by tagging each rule, this is done automatically before the reification

% --------------------------------------------------------
tag_theory_atom(L, tag_rule(T)):-theory_atom(L,ID_O,_),
            theory_symbol(ID_O,tag_rule(T)).

tag_theory_atom(L,tag_atom(T,A)):-theory_atom(L,ID_O,_),
                        theory_symbol(ID_O,tag_atom(T,A)).

% Hide rules and atom that are auxiliary for tagging
hide((rule(H,normal(B));literal_tuple(B))):-
    rule(H,normal(B)),
    literal_tuple(B,-L), tag_theory_atom(L,tag_atom(_,_)).

hide(atom(L)):-tag_theory_atom(L,_).

hide(theory_symbol(ID_O,tag_atom(T,A))):-
    theory_symbol(ID_O,tag_atom(T,A)).

hide(theory_symbol(ID_O,tag_rule(T))):-
    theory_symbol(ID_O,tag_rule(T)).

% Output tagging information

tag(rule(H,normal(B)),F):-
    rule(H,normal(B)),
    not hide(rule(H,normal(B))),
    literal_tuple(B,L), tag_theory_atom(L,tag_rule(F)).

tag(rule(H,sum(B,G)),F):-
    rule(H,sum(B,G)),
    not hide(rule(H,sum(B,G))),
    literal_tuple(B,L), tag_theory_atom(L,tag_rule(F)).

tag(atom(E),T):-
    tag_theory_atom(L,tag_atom(T,A)),
    symbol_literal(A, E).

#show tag(ID,T):tag(ID,T).



% -------------

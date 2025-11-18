% Explicit show statements
% Do not use #show pred/arity.
% In python we add #show . if cleaning is enabled.

#show theory_symbol(ID,S):theory_symbol(ID,S), not hide(theory_symbol(ID,S)).
#show atom_tuple(T):atom_tuple(T), not hide(atom_tuple(T)).
#show atom_tuple(T,A):atom_tuple(T,A), not hide(atom(A)).
#show literal_tuple(B): literal_tuple(B), not hide(literal_tuple(B)).
#show literal_tuple(B,L): literal_tuple(B,L), not hide(atom(L)), not hide(atom(-L)), not hide(literal_tuple(B)).
#show rule(H,B):rule(H,B), not hide(rule(H,B)).
#show external(A,V):external(A,V), not hide(external(A,V)).


% TODO: Only show the theory things that are not hidden,
% this needs to be propagated from theory atoms to the rest of the theory parts
% for now they are all jus hidden

% active_theory_atom(A):-
%     theory_atom(ID, ID_STR, ID_ET),
%     not hide(atom(ID)).

% active_theory_atom(A):-
%     theory_atom(ID, ID_STR, ID_ET, ID_GUARD, ID_SYMBOL),
%     not hide(atom(ID)).

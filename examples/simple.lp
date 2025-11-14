% ----------
%# Instance
% Should not be expected to tagged manually, use atom tags

person(susana;brais).
height(susana,160).
height(brais,180).
drive(brais).


% ----------
%# Atom tags
% @label("{} is driving",(P,)) :: drive(P)

% @domain :: person(P)
% @label("{} is a tall person",(P,)) :: person(P) : height(P,H), H>170
% @label("{} is a short person",(P,)) :: person(P) : height(P,H), H<=170
% @label("{} is {} cm tall",(P,H)) :: height(P,H)

% ----------
%# Encoding
% @myruletag
% Tag will be added to the next rule found

% @label("{} might be drink",(P,))
% @disabled
{drink(P)}:-person(P).

% @label("{} can't drink and drive",(P,))
:-drink(P), drive(P).

#external a.

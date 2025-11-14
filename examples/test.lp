
% @domain :: a(X)
{a(1..2)}.
b(X):-a(X), not on.
#show a/1.
#show c(X):b(X),a(X).
{on}.
:- not on.

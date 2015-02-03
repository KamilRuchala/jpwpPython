Aplikacja składa sie z trzech części:

*klient-nadawca(client.py)
*klient-odbiorca(clienthttp2.py)
*serwer(serwer.py)

Domyślnie serwer nasłuchuje na porcie 8888, a klient odbiorczy na porcie 9999. Klient nadawczy wysyła żądanie w postaci JSON na serwer.
Klienci nie wymagają szczególnego omówienia. 

Serwer odbiera obiekt JSON, następnie pobiera z niego adres i port klienta-odbiorcy, a także treść zapytania. Treść zapytania zostaje przekazana do funkcji odpowiedz(z pliku main.py). Tam zostaje to zapytanie odpowiednio rozbite na części i odpowiednio zostaje np. pobrana nazwa kraju za pomocą regexpa. Przetwarzanie zapytań podzielono na dwie części. I - przetwarzanie tekstu dla zapytań rozpoczynających się od country. II - przetwarzanie obrazów dla zapytań checkflag. Część I dodatkowo moze mieć 3 opcje: pobranie linku flagi, pobranie tekstu o danym państwie oraz pobranie listy zdań z zadanym słowem. Wszystkie funkcje dla danych zapytań znajdują się w pliku wszystko.py. W folderze dokumentacja zostanie dołączona mini-dokumentacja kodu(dziala dokumentacja klas, metod póki co nie, ale nie mam czasu żeby to poprawić, metody są skomentowane więc w kodzie powinno wszystko powinno być widoczne :) ). 

Wszelkie pytania proszę kierować na kruchala@student.agh.edu.pl.


# Aplikacja do przechowywania notatek
## Informacje ogólne
Celem projektu jest stworzenie bezpiecznej aplikacji internetowej, która pozawala na przechowywanie notatek. Notatki mogą przechowywać tylko zalogowani użytkownicy, mogą oni również je udostępniać i szyfrować. 

Podczas pracy nad aplikacją najwięcej uwagi będzie poświęcone bezpieczeństwu aplikacji.

## Stos technologiczny
Aplikacja zostanie napisana w języku **Python** przy pomocy frameworku **Flask**.

Baza danych będzie bazą **SQLite**.

Aplikacja zostanie skonteneryzowana przy pomocy **Docker**.

Do szyfrowania notatek zostanie wykorzystana biblioteka **PyCryptodrome** natomiast do szyfrowania haseł **Passlib**.


## Zastosowae rozwiązania
### 1.	Rejestracja

Przy rejestracji wymagane jest podanie adresu e-mail, nazwy użytkownika oraz hasła. Hasło powinno spełniać określone wymagania, aby było wystarczająco silne.

Hasło powinno:
- Składać się z co najmniej 10 znaków
-	Zawierać zarówno małe jak i wielkie litery
-	Zawierać co najmniej jedną cyfrę
-	Zawierać co najmniej jeden znak specjalny

Sprawdzane będzie również czy hasło znajduje się na liście najczęściej używanych haseł.

W przypadku utraty hasła możliwa będzie zmiana hasła poprzez link wysłany na adres email.

### 2.	Logowanie

Przy logowaniu zostanie zastosowane opóźnienie oraz limit prób zalogowania. 

Jeśli wystąpi podejrzanie duża liczba nieudanych prób zalogowania się, zostanie to odnotowane a użytkownik, na którego konto próbowano się zalogować zostanie poinformowany poprzez email.

### 3.	Dodawanie notatek

Aby dodać notatkę użytkownik musi posiadać konto oraz być zalogowany. 

Notatki mogą zostać ostylowane:
- Pogrubienie, pochylenie, podkreślenie tekstu
- Dodanie nagłówka
- Dodanie obrazka z zewnętrznego serwisu
- Dodanie odnośnika

### 4.	Szyfrowanie notatek

Notatka może zostać zaszyfrowana przy użyciu hasła. By odczytać zaszyfrowaną notatkę należy podać hasło którego się użyło do zaszyfrowania notatki.

Notatka która została zaszyfrowana nie może zostać udostępniona.

### 5.	Udostępnianie notatek 

Użytkownik może udostępnić notatkę wybranemu innemu użytkownikowi lub publicznie.

Notatka która została udostępniona innemu użytkownikowi pojawia się na jego stronie głównej w sekcji udostępnionych dla niego notatek.

Notatka która jest udostępniona publicznie może zostać odczytana przez każdą osobę (również osobę nie posiadającą konta w aplikacji) posiadającą link do notatki.
Udostępniana notatka nie może być zaszyfrowana.


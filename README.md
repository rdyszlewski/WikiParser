## **WiktionaryParser**
Aplikacja umożliwiająca parsowanie Wiktionary. Jako plik źródłowy przyjumje pliki xml wiktionary, które można pobrać z: https://dumps.wikimedia.org/backup-index.html.
Plik wyjściowy jest w formacie json. 
## Dane
Dane wyciągnięte z wiktionary:
- definicja
- część mowy
- rodzaj
- przykłady użycia
- rejestry
- relacje (synonimy, antonimy, hiperonimy, hiponimy, holonimy, meronimy)
- tłumaczenia
- linki do Wikipedii

Aplikacja potrafi parsować Wiktionary w wersji angielskiej i polskiej (każda wersja językowa ma inny format danych). Dodatkowo z danej wersji językowej można pobierać dane z innego języka (np. z angielskiej Wikitonary można pobrać wpisy dla języka polskiego)

## Konfiguracja

- **wiktionary_path** – ścieżka do pliku dump z odpowiedniej wersji językowej Wiktionary
- **output_path** – ścieżka do której zostaną zapisane sparsowane dane
- **settings_folder** – folder w którym znajdują się pliki z ustawieniami parsowania dla określonej wersji językowej Wiktionary
- **symbols_file** – nazwa pliku z oznaczeniami wykorzystywanymi w określonej wersji językowej Wiktionary. Plik musi znajdować się w folderze podanym przez _settings_folder_
- **patterns_file** – nazwa pliku z wyrażeniami regularnymi wykorzystywanymi przy parsowaniu Wiktionary. Plik musi znajdować się w folderze podanym przez _settings_folder_
- **parser** – wersja językowa Wiktionary. Dostepne wartości: **pl**, **en**
- **language** – określa, z jakiego języka mają zostać pobrane dane. Możliwe jest ustawienia innego języka niż w parser, jeżeli dana wersja językowa Wiktionary zawiera dane w podanym języku. Dostępne wartości: **pl**, **en**, **sp**

## Uruchamienie

`python3 parser.py ścieżka_do_konfiguracji`


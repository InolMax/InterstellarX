# InterstellarX

Я написал программу для расчета параметров Звездолета.

Определяет оптимальные параметры в заданных вами диапазонах.
Выводит график времени полета в зависимости от массы топлива.
Есть возможность рассчитать так же и двухступенчатый вариант.

.exe файл для Windows
На телефонах запускать можно используя исходный код в Pydroid 3 IDE после импорта в разделе pip Pydroid 3 необходимых библиотек.

Не проверено другими людьми, может иметь ошибки в работе или в выводимых параметрах. Я не опытный программист, так что код состоит из одного скрипта (python - 743 строки), плохо читаемый и не расширяемый, любое, даже мелкое улучшение будет трудно реализуемо.

Может не точно работать при больших скоростях, поскольку поправка на релятивистский эффект учитывается только как коэффициент на скорость при полете без топлива.

Большая часть кода написана нейросетью:
https://chat.deepseek.com/
Исходный код: 
https://github.com/InolMax/InterstellarX/blob/main/Main.py
В основе всего несколько формул из сайта 
https://projectrho.com/public_html/rocket/torchships.php



I wrote a program to calculate the parameters of the Starship.

Determines the optimal parameters in the ranges you specify.
Displays a graph of the flight time depending on the mass of fuel.
It is possible to calculate a two-stage option as well.

.exe file for Windows
On phones, you can run it using the source code in the Pydroid 3 IDE after importing the necessary libraries in the pip section of Pydroid 3.

Not tested by other people, may have errors in operation or in the output parameters. I am not an experienced programmer, so the code consists of one script (python - 743 lines), poorly readable and not expandable, any, even minor, improvement will be difficult to implement.

May not work accurately at high speeds, since the correction for the relativistic effect is taken into account only as a coefficient for the speed when flying without fuel.

Most of the code is written by a neural network:
https://chat.deepseek.com/
Source code:
https://github.com/InolMax/InterstellarX/blob/main/Main.py
Based on just a few formulas from the site
https://projectrho.com/public_html/rocket/torchships.php

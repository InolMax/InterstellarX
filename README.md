# InterstellarX
Программа для расчета параметров звездолета

Программа определяет оптимальные параметры в заданных вами диапазонах.
Выводит график времени полета в зависимости от массы топлива.
Есть возможность рассчитать так же и двухступенчатый вариант.

Program for calculating starship parameters

The program determines the optimal parameters in the ranges you specify.
Displays a graph of the flight time depending on the mass of fuel.
It is also possible to calculate a two-stage option.

![image](https://github.com/user-attachments/assets/9fc8d92b-3555-4c4f-ba9e-402f312b359f)
![image](https://github.com/user-attachments/assets/7f5110a6-a433-4de0-9520-3e93e57bff31)
![image](https://github.com/user-attachments/assets/79f40624-80a4-49ed-b682-6e190de1cd0a)
![image](https://github.com/user-attachments/assets/1fdef8b4-0921-427f-a340-d612f2179a16)


.exe файл для Windows
На телефонах запускать можно используя исходный код в Pydroid 3 IDE после импорта в разделе pip Pydroid 3 необходимых библиотек.
Сделать билд на телефонах слишком сложно из-за использования библиотеки PySyde6
Не проверено другими людьми, может иметь ошибки в работе или в выводимых параметрах. Я не опытный программист, так что код состоит из одного скрипта (python - 743 строки), плохо читаемый и не расширяемый, любое, даже мелкое улучшение будет трудно реализуемо.
Может не точно работать при больших скоростях, поскольку поправка на релятивистский эффект учитывается только как коэффициент на скорость при полете без топлива.

Возможные проблемы:

Расчет не производится:
Часто на самом деле он производится, просто задано так много вариантов для расчета, что вы не видите прогресс в progress-bar, нужно увеличить шаг или уменьшить диапазон.

Масса одной из ступеней получилась очень маленькой:
Параметры вашего звездолета могут быть такими, что звездолет не хочет расставаться с дополнительной тягой и по этому уменьшает массу одной из ступеней как может. Вы можете в этом убедиться протестировав одноступенчатый вариант, он тогда покажет меньшее время полета.

Баги, ошибки, зависания:
Сколько дней тестил столько и находил проблемы, вполне вероятно что есть те что проблемы, что я не нашел или не обработал

Большая часть кода написана нейросетью:
chat.deepseek.com/
Исходный код:
github.com/InolMax/In...
В основе всего несколько формул из сайта
projectrho.com/public_htm...





.exe file for Windows
On phones, you can run it using the source code in the Pydroid 3 IDE after importing the necessary libraries in the pip section of Pydroid 3.
It is too difficult to build on phones due to the use of the PySyde6 library
Not tested by other people, may have errors in operation or in the output parameters. I am not an experienced programmer, so the code consists of one script (python - 743 lines), poorly readable and not expandable, any, even minor, improvement will be difficult to implement.
May not work accurately at high speeds, since the correction for the relativistic effect is taken into account only as a coefficient for the speed when flying without fuel.

Possible problems:

Calculation is not performed:
Often, in fact, it is performed, it is just that so many options are specified for the calculation that you do not see the progress in the progress-bar, you need to increase the step or decrease the range.

The mass of one of the stages turned out to be very small:
The parameters of your starship may be such that the starship does not want to part with the additional thrust and therefore reduces the mass of one of the stages as much as it can. You can verify this by testing the single-stage version, it will then show a shorter flight time.

Bugs, errors, freezes:
How many days I tested, so many problems I found, it is quite possible that there are problems that I did not find or did not process

Most of the code is written by a neural network:
chat.deepseek.com/
Source code:
github.com/InolMax/In...
It is based on just a few formulas from the site
projectrho.com/public_htm...

# Tetris-project-TyulkinT
PyGame project

Проект - игра Тетрис


«Тетрис» представляет собой головоломку, построенную на использовании геометрических фигур «тетрамино» — разновидности полимино, состоящих из четырёх квадратов.


/Правила: 
Случайные фигурки тетрамино падают сверху в прямоугольный стакан шириной 10 и высотой 20 клеток. В полёте игрок может поворачивать фигурку на 90° и двигать её по    горизонтали. Также можно «сбрасывать» фигурку, то есть ускорять её падение, когда уже решено, куда фигурка должна упасть. Фигурка летит до тех пор, пока не наткнётся на другую фигурку либо на дно стакана. Если при этом заполнился горизонтальный ряд из 10 клеток, он пропадает и всё, что выше него, опускается на одну клетку. Дополнительно показывается фигурка, которая будет следовать после текущей — это подсказка, которая позволяет игроку планировать действия. Игра заканчивается, когда новая фигурка не может поместиться в стакан. Игрок получает очки за каждый заполненный ряд, поэтому его задача — заполнять ряды, не заполняя сам стакан (по вертикали) как можно дольше, чтобы таким образом получить как можно больше очков.


/Начисление очков:
Очки начисляются за убранные линии. При начислении очков за линии количество очков обычно зависит от того, сколько линий убрано за один раз. Начисление очков будет таким: 1 линия — 100 очков, 2 линии — 300 очков, 3 линии — 700 очков, 4 линии (то есть сделать Тетрис) — 1000 очков. То есть чем больше линий убирается за один раз, тем больше отношение количества очков к количеству линий. Тетрисом называется действие, после которого исчезает сразу 4 линии. Это можно сделать только одним способом — сбросить «палку» (фигурку, в которой все клетки расположены на одной линии) в «шахту» ширины 1 и глубины как минимум 4.


/Звук: Основной: Tetris Theme.mp3 ('Коробейники')
       Проигрыш: game over.mp3

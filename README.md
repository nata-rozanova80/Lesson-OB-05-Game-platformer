# Lesson-OB-05-Game-platformer

### Объяснение некоторых переменных и функций:
1. **Гравитация и падение**:
   - Добавлена переменная `vel_y`, которая управляет вертикальной скоростью персонажа.
   - При нажатии на кнопку "вверх" задаётся отрицательное значение для `vel_y`, чтобы осуществить прыжок.
   - При каждом обновлении `vel_y` увеличивается на значение гравитации, что заставляет персонажа падать.
   - Метод `fall()` реализует падение игрока до следующей платформы или до нижней границы экрана.

2. **Проверка нахождения на платформе**:
   - Метод `on_ground()` проверяет, находится ли персонаж на платформе, с использованием `pygame.sprite.spritecollide()`.

3. Флаг on_ground_flag:
   - Добавлен флаг on_ground_flag, который указывает, находится ли герой на земле. Он сбрасывается при прыжке и устанавливается обратно, когда герой достигает земли или платформы.

4. Прыжок:
   - При нажатии кнопки "вверх" (K_UP) герой может прыгать только если он находится на земле (on_ground_flag).

5. Гравитация и падение:
   - Если координаты y героя достигают 500, мы сбрасываем вертикальную скорость и устанавливаем флаг on_ground_flag в True.
   - Если герой не на земле, проверяем, находится ли он на платформе, чтобы правильно обрабатывать падение.

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import platform

# Настройка цветов
Window.clearcolor = (0.08, 0.08, 0.12, 1) 

class CalorieApp(App):
    def build(self):
        self.title = "AI Calorie Scanner"
        # Подключаем иконку (файл icon.png должен лежать в этой же папке)
        self.icon = 'icon.png' 
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Заголовок
        title = Label(text="Сканер Калорий", font_size='32sp', bold=True, color=(0.2, 0.8, 1, 1), size_hint=(1, 0.15))
        layout.add_widget(title)
        
        # Статус
        self.status_label = Label(text="Наведи камеру на еду и нажми кнопку", font_size='18sp', color=(0.8, 0.8, 0.8, 1), size_hint=(1, 0.15))
        layout.add_widget(self.status_label)
        
        # Превью фото
        self.image = Image(source='', size_hint=(1, 0.4))
        layout.add_widget(self.image)
        
        # Кнопка
        btn = Button(text="СДЕЛАТЬ ФОТО", size_hint=(1, 0.15), font_size='24sp', 
                     background_color=(0, 0.7, 1, 1), background_normal='')
        btn.bind(on_press=self.take_photo)
        layout.add_widget(btn)
        
        return layout

    def take_photo(self, instance):
        # Если приложение запущено на телефоне Android
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE])
            
            from plyer import camera
            try:
                # Сохраняем фото во внутреннюю память телефона
                camera.take_picture(filename="/sdcard/food.jpg", on_complete=self.process_image)
            except Exception as e:
                self.status_label.text = f"Ошибка камеры: {e}"
        else:
            # Заглушка для запуска на компьютере (чтобы проверить интерфейс)
            self.status_label.text = "Тестовый режим (только для ПК)"
            self.image.source = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Red_Apple.jpg/200px-Red_Apple.jpg"
            self.process_image("/sdcard/food.jpg")

    def process_image(self, filename):
        # Обновляем картинку на экране
        self.image.source = filename
        self.image.reload()
        self.status_label.text = "⏳ ИИ анализирует фото..."
        
        # В этой версии мы имитируем задержку работы ИИ (1.5 секунды)
        # В следующей версии мы подключим сюда реальный API (например, LogMeal)
        import time
        time.sleep(1.5) 
        
        # Выдаем результат
        self.status_label.text = "🍏 Определено: Яблоко\n🔥 Калорийность: 52 ккал (на 100г)"

if __name__ == '__main__':
    CalorieApp().run()

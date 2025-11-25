#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import socket
import threading
import time
import os

class NewYearServer(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=".", **kwargs)
    
    def end_headers(self):
        # Добавляем CORS заголовки для JavaScript
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Кастомизируем логирование
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def get_local_ip():
    """Получаем локальный IP адрес"""
    try:
        # Создаем временный сокет для определения IP
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def open_browser(url):
    """Открываем браузer через 2 секунды"""
    # Автоматическое открытие браузера отключено по просьбе пользователя
    pass

def main():
    # Проверяем наличие HTML файла
    if not os.path.exists("new-year-countdown.html"):
        print("❌ Ошибка: Файл new-year-countdown.html не найден!")
        print("Пожалуйста, убедитесь, что файл находится в той же директории, что и этот скрипт.")
        return
    
    # Определяем порт и хост
    PORT = 8000
    HOST = "0.0.0.0"  # Слушаем все интерфейсы
    
    # Получаем локальный IP
    local_ip = get_local_ip()
    
    # Создаем и настраиваем сервер
    try:
        with HTTPServer((HOST, PORT), NewYearServer) as httpd:
            print("=" * 60)
            print("🎉 Новогодний сервер запущен!")
            print("=" * 60)
            print(f"📁 Сервер запущен из директории: {os.getcwd()}")
            print(f"📄 Служебный файл: new-year-countdown.html")
            print("=" * 60)
            print("🌐 Доступ к странице:")
            print(f"   Локально:     http://localhost:{PORT}")
            print(f"   По IP:        http://{local_ip}:{PORT}")
            print("=" * 60)
            print("🔥 Для остановки сервера нажмите Ctrl+C")
            print("=" * 60)
            
            # Автоматическое открытие браузера отключено
            
            # Запускаем сервер
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Сервер остановлен")
        print("Спасибо за использование новогоднего сервера! 🎄")
        
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Ошибка: Порт {PORT} уже занят!")
            print("Попробуйте остановить другие серверы или используйте другой порт.")
            print("Вы можете изменить порт в настройках сервера.")
        else:
            print(f"❌ Ошибка запуска сервера: {e}")
            
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    print("🚀 Запуск новогоднего веб-сервера...")
    main()

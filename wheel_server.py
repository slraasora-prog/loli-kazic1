"""
Сервер для Telegram Mini App "Колесо Фортуны"
Запуск: python server.py
"""

from flask import Flask, send_from_directory, jsonify
import sys
import os

# Добавляем путь к боту чтобы импортировать MarkovSystem
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, static_folder='.')

# ── API: фразы из базы Маркова ─────────────────────────────────────────────
@app.route('/api/phrases')
def get_phrases():
    """Возвращает 10 случайных сгенерированных фраз из базы бота."""
    try:
        # Импортируем мозг бота
        from markov_bot import brain
        phrases = []
        for _ in range(10):
            phrase = brain.generate('wheel', None)
            if phrase and len(phrase) > 3:
                phrases.append(phrase)
        return jsonify({'phrases': list(set(phrases))})
    except Exception as e:
        # Если бот недоступен — возвращаем дефолтные фразы
        return jsonify({'phrases': [
            'Удача улыбнулась тебе!',
            'Судьба сделала выбор',
            'Колесо не лжёт',
            'Вот это поворот событий!',
            'Фортуна благосклонна',
            'Звёзды выстроились в ряд',
            'Это знак свыше',
            'Везунчик нашёлся',
        ]})

# ── Статика ────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"[WHEEL] Сервер запущен на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

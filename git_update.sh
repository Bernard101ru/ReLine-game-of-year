#!/bin/bash

# Скрипт обновления git-репозитория

echo "📦 Добавляем изменения..."
git add .

echo "📝 Создаём коммит..."
git commit -m "${1:-Обновление проекта $(date +%Y-%m-%d)}"

echo "⬆️ Отправляем на GitHub..."
git push origin main

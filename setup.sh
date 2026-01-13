#!/bin/bash

# Copy .env if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

# Build and start services
echo "Starting services..."
docker compose up -d --build

echo "Setup complete. Backend at http://localhost:8000, Frontend at http://localhost:3000"

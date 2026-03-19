FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv pip install --system --no-cache -r pyproject.toml

COPY . .

EXPOSE 8000

CMD sh -c "python manage.py migrate && python manage.py setup_data && python manage.py runserver 0.0.0.0:8000"


FROM astral/uv:python3.13-trixie-slim

WORKDIR /backend
COPY .python-version .
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync

COPY src/ ./src
ENTRYPOINT ["uv", "run", "python", "src/main.py"]

FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser \
    && chown -R appuser /app
USER appuser
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD pgrep -f worker.py || exit 1
CMD ["python", "worker.py"]

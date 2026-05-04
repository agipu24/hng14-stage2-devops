FROM node:18-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev

FROM node:18-slim
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser \
    && chown -R appuser /app
USER appuser
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000', (r) => process.exit(r.statusCode === 200 ? 0 : 1))" || exit 1
CMD ["node", "app.js"]

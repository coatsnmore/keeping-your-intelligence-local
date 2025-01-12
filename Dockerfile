FROM alpine
RUN apk update
RUN apk add bash curl wget bc jq git base64
WORKDIR /app
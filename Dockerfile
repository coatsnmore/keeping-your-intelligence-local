FROM alpine
RUN apk update
RUN apk add bash curl wget bc jq git
WORKDIR /app
FROM alpine
RUN apk update
RUN apk add bash curl wget bc jq git
RUN apk --update add postgresql-client

# ADD . .
WORKDIR /app
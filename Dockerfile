FROM node:20-alpine

# Install additional utilities
RUN apk update && apk add --no-cache \
    bash \
    curl \
    wget \
    bc \
    jq

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# COPY .env.docker ./.env

# Install dependencies
RUN npm install

# Copy application files
# COPY . .

# Default command
# CMD ["npm", "start"]
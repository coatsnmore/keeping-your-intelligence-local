FROM node:20-alpine

# Install additional utilities
RUN apk update && apk add --no-cache \
    bash \
    curl \
    wget \
    bc \
    jq \
    python3 \
    py3-pip \
    py3-pylint

# Create python symlink
RUN ln -sf /usr/bin/python3 /usr/bin/python


# Install pylint and create python symlink
# RUN pip3 install pylint && \
#     ln -sf /usr/bin/python3 /usr/bin/python

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
# Use Python as the base image
FROM python:3.13.0-bullseye

# Install dependencies for Node.js, npm, Puppeteer, and Python
RUN apt-get update && apt-get install -y \
    curl \
    fonts-liberation \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm-dev \
    libglib2.0-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@9.4.0 \
    && pip install --no-cache-dir flask requests \
    && pip install pytz \
    && pip install python-dotenv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY package.json . 
COPY capture.js . 
COPY app.py .

# Install Node.js dependencies and Puppeteer
RUN npm install \
    && npm install puppeteer \
    && npx puppeteer browsers install chrome

# Set permissions for the /app directory
RUN chmod -R 777 /app

# Expose port
EXPOSE 6000

# Command to run the application
CMD ["python", "app.py"]

FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/bot

# Set a label with the image name
LABEL name="phantom-bot"

# Install system dependencies for PostgreSQL, Python development tools, and locales
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-pip \
    postgresql \
    locales && \
    rm -rf /var/lib/apt/lists/*

# Update locales
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# Copy the requirements file to the container
COPY requirements.txt .

# upgrade pip if possible and install the Python dependencies specified in requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Make scripts executable
RUN chmod +x initiateDatabase.sh initiateBot.sh

# Run the initialization scripts
CMD ["bash", "-c", "./initiateDatabase.sh && ./initiateBot.sh"]

#!/bin/bash

# Function to handle command result and exit code
try() {
    local result="$1"
    local exit_code=$2
    if [ $exit_code -ne 0 ]; then
        echo "Command Failed: $result"
    else
        echo "Command Succeeded: $result"
    fi
}

# Start PostgreSQL server
service postgresql start

# Wait for a maximum of 10 seconds until you give up
for i in {10..1}; do
    if pg_isready -q; then
        echo "PostgreSQL is ready!"
        break
    elif [ $i -eq 1 ]; then
        echo "PostgreSQL failed to start within the expected time."
    else
        sleep 1
    fi
done

# Build the PostgreSQL URL
POSTGRES_URL="postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"

# Check if the user already exists
USER_EXISTS=$(su postgres -c "psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='$POSTGRES_USER'\"")
EXIT_CODE=$?
try "USER EXISTS $POSTGRES_USER" "$EXIT_CODE"  # Check the result of the user existence query

# Create or alter user based on whether they exist
if [ $EXIT_CODE -ne 0 ]; then
    # User doesn't exist, create the user
    su postgres -c "psql -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD' SUPERUSER;\""
    try "CREATE USER $POSTGRES_USER" $?  # Check the result of the user creation
else
    # User exists, alter the user
    su postgres -c "psql -c \"ALTER USER $POSTGRES_USER PASSWORD '$POSTGRES_PASSWORD';\""
    try "ALTER USER $POSTGRES_USER" $?  # Check the result of the user alteration
fi

echo "Database initialization complete."

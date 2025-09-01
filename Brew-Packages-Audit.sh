#!/bin/bash

# Brew Packages Audit Script
# Lists all Homebrew formulas and casks with their versions

# Get the main user by filtering out system users from /Users directory
local_user=$(sudo ls -l /Users | grep -v '^total' | awk '{print $3}' | grep -v -e 'root' | grep -v -i 'admin' | head -1)

if [ -z "$local_user" ]; then
    echo "Error: Could not determine local user directory"
fi

# Check if Homebrew is installed for the local user
if [ ! -f "/Users/$local_user/.homebrew/bin/brew" ] && [ ! -f "/opt/homebrew/bin/brew" ]; then
    echo "Homebrew is not installed or not in PATH"
fi

# Switch to the local user and run Homebrew commands
sudo -u "$local_user" /opt/homebrew/bin/brew list --versions | while read -r package version rest; do
    echo "$package,$version"
done
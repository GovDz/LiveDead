# SSH Checker

This Python script checks the connectivity of SSH servers listed in a file and categorizes them as live or dead. It supports both password and key-based authentication.

## Requirements

- Python 3.x
- sshpass (for password authentication)
- (Optional) `ssh-copy-id` for setting up key-based authentication

## Usage

1. **Install Dependencies:**

   If not already installed, you can install the required dependencies using the following commands:

   ```bash
   sudo apt-get install python3
   sudo apt-get install sshpass

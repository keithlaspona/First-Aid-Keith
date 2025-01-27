#!/bin/bash

# Update package lists
apt-get update

# Install Python package dependencies
pip install streamlit langchain
pip install transformers
pip install datasets

# You might need to add additional setup commands here
# For example, if you need to install other system packages or tools

# Setup complete message
echo "Setup complete!"
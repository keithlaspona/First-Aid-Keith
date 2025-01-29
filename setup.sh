#!/bin/bash

# Update package lists
apt-get update

# Install Python package dependencies
pip install streamlit langchain

streamlit run app.py

# Setup complete message
echo "Setup complete!"

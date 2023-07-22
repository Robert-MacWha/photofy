#!/usr/bin/env bash

# Function to kill existing processes of npx hardhat node
kill_existing_hardhat_node() {
  echo "Checking for existing npx hardhat node processes..."

  # Kill the process listening on port 8545
  HARDHAT_NODE_PID=$(netstat -ano | grep 'LISTEN' | grep ':8545' | awk '{print $5}')
  
  if [ -n "$HARDHAT_NODE_PID" ]; then
    echo "Killing existing npx hardhat node processes..."
    taskkill //PID $HARDHAT_NODE_PID //F
    sleep 5 # Give some time for the processes to terminate gracefully
  else
    echo "No existing npx hardhat node processes found."
  fi
}

# Function to start npx hardhat node in the background
start_hardhat_node() {
  echo "Starting npx hardhat node..."
  npx hardhat node --port 8545 &
}

# Function to run backend/deploy.py script from within the backend directory
run_deploy_script() {
  echo "Running backend/deploy.py script..."
  cd backend
  C:/Users/trebo/Documents/GitHub/PhotoFy/.conda/python deploy.py
}

# Main script execution
kill_existing_hardhat_node # Kill any existing processes of npx hardhat node

start_hardhat_node # Start npx hardhat node in the background

# Wait for a few seconds to ensure that the hardhat node is up and running
sleep 5

run_deploy_script # Run the backend/deploy.py script

# This loop keeps the script running until the user types 'exit'
while true
do
  echo "Type 'exit' to terminate the script."
  read INPUT_STRING
  if [[ "$INPUT_STRING" == "exit" ]]; then
    echo "Exiting."
    break
  fi
done
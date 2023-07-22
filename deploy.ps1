# Function to kill existing processes of npx hardhat node
function Kill-ExistingHardhatNode {
  Write-Host "Checking for existing npx hardhat node processes..."
  $HARDHAT_NODE_PIDS = Get-Process | Where-Object { $_.CommandLine -like "*npx hardhat node*" } | Select-Object -ExpandProperty Id

  if ($HARDHAT_NODE_PIDS) {
    Write-Host "Killing existing npx hardhat node processes..."
    Stop-Process -Id $HARDHAT_NODE_PIDS -Force
    Start-Sleep -Seconds 5
  } else {
    Write-Host "No existing npx hardhat node processes found."
  }
}

# Function to start npx hardhat node in the background
function Start-HardhatNode {
  Write-Host "Starting npx hardhat node..."
  Start-Process -NoNewWindow -FilePath "npx" -ArgumentList "hardhat node --port 8545"
}

# Function to run backend/deploy.py script from within the backend directory
function Run-DeployScript {
  Write-Host "Running backend/deploy.py script..."
  Set-Location -Path .\backend
  python3 .\deploy.py
}

# Main script execution
Kill-ExistingHardhatNode

Start-HardhatNode

# Wait for a few seconds to ensure that the hardhat node is up and running
Start-Sleep -Seconds 10

Run-DeployScript

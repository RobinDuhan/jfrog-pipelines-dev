#!bin/bash

export NVM_VERSION=v0.39.1
export NODE_VERSION=16.10.0
curl -sS https://raw.githubusercontent.com/creationix/nvm/"$NVM_VERSION"/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
bash "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}  
bash "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
bash "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
export PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
node --version && npm --version

sudo apt-get update && sudo apt install -y nfs-common
sudo apt-get update && sudo apt install -y cifs-utils
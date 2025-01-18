.PHONY: start-ganache compile migrate

# Start Ganache CLI
start-ganache:
	@echo "Starting Ganache CLI..."
	ganache-cli -h 127.0.0.1 -p 8545

# Compile the smart contracts
compile:
	@echo "Compiling contracts..."
	truffle compile

# Migrate the contracts and copy the build folder and deployment_config.json to backend
migrate:
	@echo "Migrating contracts..."
	truffle migrate --network development
	@echo "Copying build folder and deployment_config.json to backend..."
	cp -r build/contracts ./backend/build
	cp deployment_config.json ./backend/deployment_config.json

# blockcrt
This is a blockchain-based certificate validation system that allows institutions to issue and verify certificates using smart contracts deployed on Ethereum. It integrates with IPFS for certificate storage and uses FastAPI for backend development.

## Requirements

Before running the project, make sure you have the following installed on your machine:

### General Requirements

- **Node.js** (v16 or higher) - Required for running Truffle and Ganache
- **Python 3.10 or higher** - Backend application
- **Docker** (Optional, but recommended for isolated environment)

### Installations

#### 1. Install Truffle and Ganache CLI

You need to install **Truffle** and **Ganache CLI** manually. Follow these steps:

- **Install Truffle**:

```bash
npm install -g truffle
```

- **Install Ganache CLI**

```bash
npm install -g ganache-cli
```

#### 2. Install Python Dependencies:

Install the required Python dependencies for the backend:

```bash
pip install -r backend/requirements.txt
```

## Project Structure

```bash
.
├── backend/
│   ├── app/                     # FastAPI backend code
│   ├── requirements.txt         # Python dependencies for backend
│   └── supabase/config.toml     # Supabase config
├── build/                       # Build folder for compiled contracts
├── contracts/                   # Smart contract source code
├── deployment_config.json       # Contract address after deployment
├── docker/                      # Docker setup for different environments
├── migrations/                  # Truffle migration scripts
├── README.md                    # This file
└── truffle-config.js            # Truffle configuration file
```

## Setup Instructions

### 1. Clone the Repository
Clone the repository to your local machine:

```bash
git clone git@github.com:same-ou/blockcrt.git && \
cd blockcrt
```
### 2. Install Dependencies
```
pip install -r backend/requirements.txt
```

### 3. Configure Ganache CLI
Ganache is used to run a local Ethereum blockchain. You can run Ganache CLI in the background by using the Makefile.

- Start Ganache CLI with the following command:

```bash
make start-ganache
```
This will start Ganache on `127.0.0.1:8545`.

### 4. Compile the Smart Contracts

Compile the smart contracts using Truffle. This will generate the necessary `build` files in the build folder.

```bash
make compile
```

### 5. Migrate the Contracts

After compiling the contracts, migrate them to the Ganache network. This step will deploy the smart contracts and create the `deployment_config.json` file with the contract address.

```bash
make migrate
```

This will:

- Deploy the contracts.
- Copy the build files and deployment_config.json to the backend folder.

### 6. Set Up Supabase
Supabase is used for both authentication and database management. You can choose to use a local instance or the cloud version.

#### Local Supabase Setup
Follow the instructions on [Supabase Local Development Setup](https://supabase.com/docs/guides/local-development) to install Supabase locally on your machine. After installation, run the following command to start Supabase:
```bash
supabase start
```
#### Supabase Cloud Version Setup
If you prefer using the cloud version of Supabase, you can create a Supabase project through the [Supabase dashboard](https://supabase.com/dashboard/projects). Once your project is set up, you'll receive the necessary credentials (URL and API keys) to configure the connection.

#### Configure Supabase in the Backend

In your backend folder, create a `.env` file with the following environment variables:
```bash
SUPABASE_URL=<Your Supabase URL>
SUPABASE_KEY=<Your Supabase API Key>
...
```
- For local setup, you can use the URL and keys provided by the local Supabase instance once it's started.
- For cloud setup, you can find your Supabase URL and API key in the Supabase dashboard.

#### Create the Institution Database
After setting up Supabase, you'll need to create the table for storing institution data. You can do this through the Supabase dashboard or using SQL scripts.

### 7. Pinata Setup

- **Create a Pinata Account**  
   To upload your generated certificates to IPFS, you will need a Pinata account. Follow these steps to set up:
   - Visit [Pinata's website](https://pinata.cloud/) and create an account if you don't already have one.
   - After signing in, navigate to the "API Keys" section under your profile.
   - Generate a new API key. You'll receive a `Pinata API Key` and a `Pinata Secret Key`.

- **Configure Pinata in the Backend**  
   In your backend `.env` file, add the following environment variables:
   ```env
   PINATA_API_KEY=<Your Pinata API Key>
   PINATA_SECRET_KEY=<Your Pinata Secret Key>
   ```

### 8. Run the Backend
The backend application is built using FastAPI. You can start the FastAPI server with Uvicorn.

Navigate to the backend directory:
```bash
cd backend
```

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The backend server will be accessible at `http://127.0.0.1:8000`.

### 9. Using the System
Once the backend is running, you can issue certificates and verify them through the API.

**Issue a Certificate**
To issue a certificate, make a POST request to the /issue-certificate endpoint with the required data (CNE, candidate name, major name).

**Verify a Certificate**
To verify a certificate, upload the certificate PDF to the /verify-certificate endpoint, and the system will extract the necessary details and verify it using the smart contract.





# MyEDR

MyEDR is a basic Endpoint Detection and Response project, Currently focused on device registration and management.

The project consists of:

- **Agent**: Collects system information from a device and registers it with the server.
- **Server**: FastAPI backend that receives and stores device information.
- **Frontend**: React frontend for admin login and viewing registered devices.
- **Database**: Supabase PostgreSQL.

## Current Features

- Device registration
- Persistent agent-generated device UUID
- System information collection
  - Hostname
  - OS name, version, and build
  - Serial number
  - CPU
  - RAM
  - GPU
  - Network interfaces
- PostgreSQL storage using Supabase
- Basic React admin dashboard

---

## Project Structure

```text
myedr/
├── agent/
├── server/
├── dashboard/
└── README.md
````

## Run Server

From the project root:

create a venv in the root folder

for server
```powershell
pip install -r server/requirements.txt
```
and for agent
```powershell
pip install -r agent/requirements.txt
```

Create `server/.env`:

```env
DATABASE_URL=your_supabase_postgres_url

JWT_SECRET=your_long_random_secret
```

Start:

```powershell
cd server
uvicorn app.main:app --reload
```

Server:

```text
http://localhost:8000
```

Docs:

```text
http://localhost:8000/docs
```

## Add Demo Admin Account

Generate password hash:

```powershell
python
```

```python
from server.app.security.auth import hash_password

print(hash_password("admin"))
```

Insert the generated hash into Supabase:

```sql
INSERT INTO users (
    username,
    password_hash,
    is_admin
)
VALUES (
    'admin',
    'PASTE_PASSWORD_HASH_HERE',
    TRUE
);
```

Demo credentials:

```text
Username: admin
Password: admin
```

## Test Agent

Make sure the server is running.

From the project root:

```powershell
python -m agent.main
```

The agent collects device information and registers it with the server.

## Run Frontend

```powershell
cd dashboard
npm install
npm run dev
```

Open the URL

```text
http://localhost:5173
```

## Development

Terminal 1:

```powershell
cd server
uvicorn app.main:app --reload
```

Terminal 2:

```powershell
cd dashboard
npm run dev
```

Terminal 3:

```powershell
python -m agent.main
```

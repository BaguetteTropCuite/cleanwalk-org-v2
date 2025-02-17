# Cleanwalk V2 DEV FORK => Original : https://github.com/cleanwalk-org-asso/cleanwalk-org-v2

Cleanwalk.org is a website to find clean walks all over France.

## Table of Contents

- **[Frontend](front/README.md)**
- **[API](api/README.md)**

## Requirements

- Docker and docker compose [install link ->](https://docs.docker.com/engine/install/)
- MySQL DataBase
- node.js [install link ->](https://nodejs.org/fr)
- *(optional)* python3 [install link ->](https://www.python.org/downloads/)

## environement
Create a `.env` file in the `api` and `front` directories and follow the `.env.example` schema.

## How to launch

### Developement

To launch the app on dev environnement, use the docker compose tool at the root directory of the project.

**API ->**

```bash
docker compose up -d
```
or <br />
- go in **api** Directory -> `cd api`
- install
```bash
pip install -r requirements.txt
```
- launch
```bash
docker compose up -d
```

To down **API**

```bash
docker compose down
```

<div style="color:#f1c232">⚠️ Tips : with docker Adminer is launched on port :8080 </div>

**Frontend ->**
- go in **api** Directory -> `cd api`
- install
```bash
npm install
```
- run on port 5173
```bash
npm run dev
```

### Production

#### lauch
```bash
docker-compose -f "docker-compose.prod.yml" up -d --build
```

###"" config nginx proxy manager

**first login**: connect to @server_ip:81
- username: admin@example.com
- password: changeme    **! change admin info**

**proxy hosts**
Go to Hosts > Proxy Hosts and click on Add Proxy Host.

**frontend**
- Domain Names: yourdomain.example, www.yourdomain.example
- Scheme: http
- Forward Hostname / IP: frontend
- Forward Port: 80

**API**
- Domain Names: api.yourdomain.example
- Scheme: http
- Forward Hostname / IP: api
- Forward Port: 5000

**uploads**
- Domain Names : uploads.yourdomain.example
- Scheme : http
- Forward Hostname / IP : nginx-proxy-manager
- Forward Port : 81

in advanced add:
```
location / {
    alias /var/www/uploads/;
    autoindex on;
}
```

**SSL Config**
- check Force SSL
- select Request a new SSL certificate
- add email and save






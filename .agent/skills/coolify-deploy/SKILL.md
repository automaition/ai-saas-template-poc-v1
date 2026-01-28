---
name: coolify-deploy
description: |
  Configurazione produzione-ready per deploy su Coolify. Ottimizzazione Dockerfile,
  health checks, gestione env vars, e best practice per il self-hosting.
  Trigger: "deploy", "coolify", "produzione", "docker produzione", "hosting", 
  "env production", "health check", "deploy server"
keywords: [deploy, coolify, production, docker, hosting, health-check, env]
---

## Goal
Preparare l'applicazione per deploy istantaneo su Coolify: container ottimizzati, configurazione automatica delle variabili d'ambiente, health checks affidabili, e gestione corretta del reverse proxy già gestito da Coolify.

## Instructions

1. **Frontend Dockerfile (Coolify-ready)**:
   - Multi-stage build: stage 1 (Node builder), stage 2 (serve statici)
   - Stage 2: usare `nginx:alpine` LEGGERO solo per servire i file statici della build (Vite), NON per reverse proxy
   - Oppure usare `node:20-alpine` con `serve` (`npx serve -s dist -l 80`) per semplicità
   - Copiare solo la cartella `dist/` dalla build stage
   - Configurare `EXPOSE 80` (Coolify mapperà la porta automaticamente)
   - Variabile d'ambiente `VITE_API_URL` deve puntare al dominio backend (es. `https://api.tuodominio.com` o per stesso dominio con path `/api`)

2. **Backend Dockerfile**:
   - Python 3.11-slim, installare solo dipendenze necessarie
   - Health check endpoint `/api/v1/health` già implementato (deve rispondere 200)
   - CMD con `uvicorn` (se singolo worker) o `gunicorn` con `uvicorn.workers.UvicornWorker` (se multi-worker)
   - EXPOSE 8000 (Coolify si occupa del mapping porta esterna)
   - Variabili d'ambiente da configurare su Coolify dashboard (non hardcodate)

3. **Docker Compose per Coolify**:
   - Non serve sezione `ports` esposta pubblicamente (Coolify gestisce il routing)
   - Usare `expose` invece di `ports` per comunicazione interna tra servizi se necessario
   - Volume per persistenza SQLite: montare su path assoluto stabile (`/app/data`)
   - Network: lasciare default bridge o usare network interna se multi-servizi
   - Restart policy: `unless-stopped`

4. **Configurazione Coolify Dashboard**:
   - Tipo deploy: `Docker Compose` (se usi docker-compose.yml) o separare in due Resources (Frontend Static + Backend)
   - Environment Variables: inserire tutte le variabili da `.env.example` nella sezione Environment di Coolify
   - Domains: configurare dominio frontend (es. `app.tuodominio.com`) e backend (es. `api.tuodominio.com`)
   - Health Check Path: `/api/v1/health` per il backend (Coolify monitora il container)
   - Build无限: disabilitare se fai build locale e push immagini, oppure abilitare per build su server

5. **Variabili d'Ambiente Critiche**:
   - `ENVIRONMENT=production`
   - `CORS_ORIGINS`: dominio frontend effettivo (es. `https://app.tuodominio.com`)
   - `DATABASE_URL`: path assoluto nel container (es. `sqlite:///app/data/app.db`)
   - `OPENROUTER_API_KEY` e `SITE_URL`: dominio effettivo del progetto
   - NO `localhost` o `127.0.0.1` nelle URL di produzione

6. **Health Checks**:
   - Backend: endpoint `/api/v1/health` che controlla anche connessione DB (se usata) e ritorna `{"status": "ok"}`
   - Frontend: se usato Nginx, health check implicito sulla porta 80, altrimenti endpoint `/health` semplice
   - Coolify userà questi per capire se il容器 è healthy

7. **Persistenza Dati**:
   - SQLite: volume montato su `/app/data` (path fuori dal codice sorgente)
   - Backup: Coolify non backuppa automaticamente i volumi, documentare comando backup manuale o script
   - Logs: configurare logging su stdout/stderr (Coolify li raccoglie automaticamente)

8. **Ottimizzazioni**:
   - `.dockerignore` robusto per ridurre build context (node_modules, .git, __pycache__)
   - Layer caching: copiare requirements.txt/package.json prima del codice sorgente
   - Multi-arch: se server ARM (Raspberry), usare immagini `linux/arm64` compatibili

## Constraints

- NO reverse proxy custom: Coolify gestisce Nginx/Traefik automaticamente, non configurare `nginx.conf` complessi
- NO port binding manuali su 80/443: Coolify gestisce SSL e routing, usare porte interne (8000, 3000, ecc)
- NO hardcoded secrets: tutte le API key e password devono essere env vars su Coolify
- Database: SQLite accettabile per PoC in produzione se volume persistente, ma documentare limiti (concorrenza)
- Health check: deve essere veloce (&lt; 1s), non eseguire query pesanti nel check
- Frontend: buildare con `VITE_API_URL` puntante al backend reale, mai a localhost

## Examples

### Esempio utilizzo per Antigravity
Utente: "Prepara il progetto per deploy su Coolify"

Azioni:
1. Verificare che `.env.example` contenga tutte le variabili necessarie
2. Aggiornare Dockerfile backend con health check e CMD production-ready
3. Dockerfile frontend: build Vite + serve su porta 80 (senza reverse proxy complex)
4. docker-compose.yml con `expose` invece di `ports` aperte e volume per SQLite
5. Documentare nella skill: "Su Coolify, crea Resource Docker Compose, carica env vars dalla dashboard, imposta dominio, deploy"
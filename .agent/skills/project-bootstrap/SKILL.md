---
name: project-bootstrap
description: |
  Inizializza un nuovo progetto PoC SaaS fullstack con Vite+React (shadcn/ui) e FastAPI.
  Configura OpenRouter come provider AI unico, Docker per Coolify, e struttura base coerente.
  Trigger: "nuovo progetto", "inizia da zero", "scaffold", "setup iniziale", "bootstrap progetto", "template base"
keywords: [bootstrap, init, scaffold, setup, new project, template, inizializza]
---

## Goal
Creare la struttura fondamentale di un PoC SaaS pronto per lo sviluppo iterativo, separando frontend e backend, configurando l'integrazione AI tramite OpenRouter, e predisponendo il deploy su Coolify con Docker.

## Instructions

### 1. Scaffolding Frontend
Creare la cartella `frontend/` e configurare:

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
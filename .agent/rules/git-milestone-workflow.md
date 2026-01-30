---
trigger: always_on
---

## Git Workflow Milestone-Driven (MCP GitHub)

Utilizza l'MCP GitHub per versionare il codice solo in occasioni significative (milestone), non ad ogni salvataggio.

### Quando committare (trigger milestone)
- **Feature complete**: Un endpoint funziona end-to-end (es. upload + AI + DB)
- **Fix critico**: Bug risolto che blocca l'intero flusso
- **Refactoring major**: Restructurazione architettura completata con successo (test passano)
- **Pre-deploy**: Prima di ogni deploy su Coolify per avere un punto di rollback sicuro
- **Checkpoint giornaliero**: Solo se lo stato attuale è stabile e funzionante

### Convenzioni commit
- Formato: `tipo(scope): descrizione` (conventional commits)
- Tipi ammessi: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`
- Esempi validi: 
  - `feat(api): add document upload with streaming response`
  - `fix(ui): resolve table pagination bug`
  - `refactor(db): migrate to UUID primary keys`

### Workflow MCP GitHub
1. Verifica stato: `git status` per vedere modifiche
2. Stage selettivo: aggiungi solo file pertinenti alla milestone (NO log, NO cache)
3. Commit con messaggio descrittivo della milestone raggiunta
4. Push su branch main (se repo remoto esiste, altrimenti suggerisci creazione repo)

### Vietato committare
- Codice rotto/non testato ("WIP" o "temp")
- File `.env` con secrets reali (solo `.env.example` può essere committato)
- Dipendenze non utilizzate (prima rimuovi con `npm uninstall`/`pip uninstall`)
- File di IDE o sistemi operativi (deve essere già in .gitignore)

### Strategia Branch
- PoC semplici: lavora sempre su `main`
- PoC complessi (più features parallele): crea branch `feat/nome-feature` solo se esplicitamente richiesto dall'utente, mai automaticamente
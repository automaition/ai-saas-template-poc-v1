---
name: ai-integration-advanced
description: |
  Pattern avanzati per integrazione LLM via OpenRouter: streaming SSE, structured output JSON,
  chunking documenti, retry logic, gestione rate limit e timeout. Ottimizzato per UX reattiva e affidabilità.
  Trigger: "stream AI", "streaming response", "json garantito", "chunking", "rate limit", 
  "documento lungo", "structured output", "sse", "retry AI"
keywords: [ai, llm, openrouter, streaming, sse, json, chunking, retry, rate-limit]
---

## Goal
Implementare pattern LLM robusti oltre la chiamata base: streaming per UX responsive, output JSON strutturato garantito, gestione documenti lunghi (chunking), e recupero errori transienti (retry, rate limiting).

## Instructions

1. **Streaming SSE (Server-Sent Events)**:
   - Endpoint dedicato `/stream` che ritorna `StreamingResponse` con `media_type="text/event-stream"`
   - Client OpenRouter con `stream=True` in payload
   - Generatore async che yielda `f"data: {json}\n\n"` formato SSE
   - Headers obbligatori: `Cache-Control: no-cache`, `X-Accel-Buffering: no` (disabilita buffering nginx)
   - Frontend: `EventSource` nativo o libreria `@microsoft/fetch-event-source` per header custom
   - Gestione disconnessione: heartbeat o riconnessione automatico lato client

2. **Structured Output (JSON Garantito)**:
   - Usare `response_format: {type: "json_object"}` nelle chiamate OpenRouter (se modello supporta)
   - Sempre includere nello user o system prompt: "Restituisci SOLO JSON valido, niente markdown"
   - Validazione risposta con Pydantic prima di restituirla al frontend
   - Fallback: se JSON parse fallisce, ritentare con prompt "correggi il JSON" o restituire errore strutturato
   - Per schemi complessi: usare `response_format` con JSON schema se il modello lo supporta (GPT-4, Claude 3.5)

3. **Chunking Documenti Lunghi**:
   - Tokenizzazione preventiva (tiktoken o stima caratteri: ~4 char = 1 token)
   - Limite safe: 4000 token per GPT-4-mini, 8000 per Claude 3.5 Sonnet (lasciare margine per output)
   - Strategie: split by character (chunk_size ~3000), overlap tra chunks (context conservation), oppure split by semantic units (paragrafi/titoli)
   - Pattern "Map-Reduce": processare chunks separatamente (map) e poi sintetizzare risultati (reduce) con chiamata finale
   - Metadati per chunk: index, total_chunks, source_filename per ricostruzione

4. **Retry Logic e Rate Limiting**:
   - Exponential backoff: 3 tentativi (2s, 4s, 8s) con jitter
   - Gestione specifica HTTP 429 (rate limit): leggere header Retry-After se presente, altrimenti backoff esponenziale
   - Gestione 502/503 (gateway error): retry immediato
   - Timeout per chiamata: 60s default, 120s per documenti lunghi
   - Circuit breaker semplice: se 5 errori consecutivi, pausa di 30s (opzionale per PoC)

5. **Prompt Management**:
   - System message coerente e specifico del dominio (es: "Sei un estrattore dati fatture")
   - Few-shot examples nel prompt per formati complessi (1-2 esempi input/output)
   - Separazione chiara: system (istruzioni) vs user (contenuto variabile)
   - Temperature: 0.1-0.3 per estrazione dati (deterministico), 0.7 per generazione testo creativa
   - Max_tokens: impostare sempre per prevenire risposte troppo lunghe o costi imprevisti

6. **Gestione Errori Specifici**:
   - Context length exceeded (413/400 con messaggio specifico): fallback a modello con contesto maggiore (Claude 100k, GPT-4-turbo) oppure chunking automatico
   - Timeout: restituire 202 Accepted con job_id per polling (async processing), o continuare stream con placeholder
   - Content filter: gestire risposte vuote o censurate da moderazione OpenRouter

## Constraints

- Streaming: sempre usare IAsyncGenerator, mai lista in memoria per stream
- JSON: mai affidarsi al parsing senza try/except, mai esporre JSON malformato al frontend
- Chunking: mai mandare documenti &gt;50k caratteri in una singola chiamata (rischio truncate o errore)
- Retry: massimo 3 tentativi per singola richiesta (evita loop infiniti o costi esponitivi)
- Token: stimare sempre input tokens prima della chiamata, loggare usage se possibile
- NO: blocking IO durante streaming, salvare risultati parziali su DB invece di bufferare tutto in RAM

## Examples

### Esempio utilizzo per Antigravity
Utente: "Crea endpoint per analizzare fatture lunghe in stream"

Azioni:
1. Endpoint `/api/v1/invoices/stream-analyze` con SSE
2. Chunking PDF: dividere in blocchi di 3000 token, processare sequenzialmente o in parallelo (asyncio.gather)
3. Per ogni chunk: chiamata OpenRouter con system message "Estrai dati fattura parziali in JSON"
4. Merge risultati chunks e stream finale al client via SSE
5. Gestione 429: se rate limited, attendere 10s e retry con messaggio "processing..." sullo stream
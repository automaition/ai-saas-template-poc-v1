---
name: frontend-generics
description: |
  Genera componenti UI React con shadcn/ui, 21st.dev/magic e MCP shadcn.
  Pattern: form type-safe, tabelle dati, upload file. Usa MCP per componenti ufficiali e temi.
  Trigger: "nuovo componente", "crea form", "tabella dati", "pagina frontend", "ui upload", "shadcn"
keywords: [react, component, shadcn, 21st, form, table, ui, zod, tailwind, mcp]
---

## Goal
Creare componenti React coerenti usando MCP shadcn per componenti ufficiali e MCP 21st-dev per UI/UX avanzati, con validazione Zod (speculare a Pydantic backend) e TanStack Table per dati.

## Instructions

1. **Setup Componenti Base (via MCP)**:
   - Usare **MCP shadcn** per aggiungere componenti: `npx shadcn add button card input form label table progress sonner`
   - Usare **MCP 21st-dev** per temi, animazioni o componenti enhanced quando richiesto esplicitamente
   - Struttura: `components/ui/` (shadcn base), `features/` (componenti specifici progetto)

2. **Pattern Form**:
   - Schema Zod che rispecchia esattamente il modello Pydantic del backend
   - React Hook Form con `zodResolver`
   - Componenti shadcn: `&lt;Form&gt;, &lt;FormField&gt;, &lt;FormItem&gt;, &lt;FormLabel&gt;, &lt;FormControl&gt;, &lt;FormMessage&gt;`
   - Gestione errori server 422: mappare `error.response.data.detail` sui field specifici via `form.setError()`

3. **Pattern Tabella Dati**:
   - Usare `@tanstack/react-table` v8
   - Wrapper attorno a componenti shadcn `&lt;Table&gt;`, `&lt;TableHeader&gt;`, `&lt;TableBody&gt;`
   - Funzionalità minime: sorting, filtro globale su testo, pagination client-side (per PoC)
   - Props: `columns: ColumnDef&lt;T&gt;[]`, `data: T[]`, `onRowClick?: (row: T) =&gt; void`

4. **Pattern Upload File**:
   - `react-dropzone` per drag & drop (installare separatamente)
   - Preview file (icona PDF, thumbnail img)
   - Progress bar durante upload axios (onUploadProgress)
   - Validazione: max size (default 10MB), mime type check

5. **API Client**:
   - File `lib/api.ts` con istanza axios configurata (`baseURL` da env VITE_API_URL)
   - Interceptor globale errori 500 con toast errore (sonner)

6. **Uso MCP**:
   - **MCP shadcn**: sempre per aggiungere nuovi componenti ufficiali (es. "aggiungi shadcn calendar")
   - **MCP 21st-dev**: per generare componenti complessi, landing page sections, animazioni, o quando l'utente chiede "bello", "moderno", "animato"

## Constraints

- Componenti UI: usare **MCP shadcn** come default (vietato Material-UI, Ant Design)
- Styling avanzato/animazioni: usare **MCP 21st-dev** quando richiesto UX ricca
- Solo Tailwind CSS (no CSS-in-JS)
- Form obbligatori React Hook Form + Zod (mai form non controllati)
- Tabelle: TanStack Table obbligatorio per dati tabulari
- Upload: react-dropzone obbligatorio per file input
- HTTP client: solo axios con interceptors
- Icons: Lucide React (inclusa in shadcn)
- Toast: sonner

## Examples

### Esempio utilizzo MCP per Antigravity
Utente: "Aggiungi un calendario bello al form"

Azioni:
1. Usare MCP shadcn: `add calendar` (base functionality)
2. Usare MCP 21st-dev per stile enhanced se richiesto (es. animazioni, tema specifico)
3. Integrare nel form esistente con React Hook Form

### Esempio utilizzo standard
Utente: "Crea form per creare documento"

Azioni:
1. Schema Zod: `title: z.string().min(3), file: z.instanceof(File)`
2. Componente `DocumentForm` con shadcn `&lt;Form&gt;` e `&lt;FileUpload&gt;` custom
3. Integrazione API: POST multipart/form-data a `/api/v1/documents`
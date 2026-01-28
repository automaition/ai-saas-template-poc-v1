---
name: frontend-generics
description: |
  Genera componenti UI React con shadcn/ui, Tailwind, React Hook Form + Zod.
  Pattern essenziali: form type-safe, tabelle dati, upload file.
  Trigger: "nuovo componente", "crea form", "tabella dati", "pagina frontend", "ui upload"
keywords: [react, component, shadcn, form, table, ui, zod, tailwind]
---

## Goal
Creare componenti React coerenti con lo stack PoC: shadcn/ui per UI, Zod per validazione (speculare a Pydantic backend), TanStack Table per dati, react-dropzone per upload.

## Instructions

1. **Setup Componenti Base**:
   - Installare shadcn components necessari: `button`, `card`, `input`, `form`, `label`, `table`, `progress`, `sonner` (toast)
   - Struttura: `components/ui/` (shadcn base), `features/` (componenti specifici progetto)
   - Path alias `@/` configurato su `./src`

2. **Pattern Form**:
   - Schema Zod che rispecchia esattamente il modello Pydantic del backend
   - React Hook Form con `zodResolver`
   - Componenti: `&lt;Form&gt;`, `&lt;FormField&gt;`, `&lt;FormItem&gt;`, `&lt;FormLabel&gt;`, `&lt;FormControl&gt;`, `&lt;FormMessage&gt;`
   - Gestione errori server 422: mappare `error.response.data.detail` sui field specifici via `form.setError()`
   - Submit con `axios.post()`, gestire loading state su `&lt;Button disabled={form.formState.isSubmitting}&gt;`

3. **Pattern Tabella Dati**:
   - Usare `@tanstack/react-table` v8
   - Wrapper attorno a componenti shadcn `&lt;Table&gt;`, `&lt;TableHeader&gt;`, `&lt;TableBody&gt;`, ecc.
   - Funzionalità minime: sorting, filtro globale su testo, pagination client-side (per PoC)
   - Props: `columns: ColumnDef&lt;T&gt;[]`, `data: T[]`, `onRowClick?: (row: T) =&gt; void`

4. **Pattern Upload File**:
   - `react-dropzone` per drag & drop
   - Preview file (icona PDF, thumbnail img)
   - Progress bar durante upload axios (onUploadProgress)
   - Validazione: max size (default 10MB), mime type check
   - Cleanup automatico in finally

5. **API Client**:
   - File `lib/api.ts` con istanza axios configurata (`baseURL` da env VITE_API_URL)
   - Interceptor globale errori 500 con toast errore (sonner)

6. **Stato**:
   - Zustand solo per stato globale essenziale (user, theme)
   - Vietato Redux/MobX/Recoil per PoC
   - Form state gestito solo da React Hook Form (non Zustand)

## Constraints

- SOLO shadcn/ui + Radix (vietato Material-UI, Ant Design, Chakra)
- Solo Tailwind CSS (no CSS-in-JS)
- Form obbligatori React Hook Form + Zod (mai form non controllati)
- Tabelle: TanStack Table obbligatorio per dati tabulari (no HTML table vanilla)
- Upload: react-dropzone obbligatorio per file input
- HTTP client: solo axios con interceptors (no fetch nativo)
- Icons: Lucide React (inclusa in shadcn)
- Toast: sonner
- Export: named exports (default export solo per pages)

## Examples

### Esempio utilizzo per Antigravity
Utente: "Crea form per creare documento con campo titolo e upload PDF"

Azioni:
1. Creare schema Zod: `title: z.string().min(3), file: z.instanceof(File)`
2. Componente `DocumentForm` con shadcn `&lt;Form&gt;` e `&lt;FileUpload&gt;` custom
3. Integrazione API: POST multipart/form-data a `/api/v1/documents`
4. On success: redirect o toast success + reset form
# mCODE Radiomics Ontology Taxonomy Browser

## Project structure

```
# To do...
```

## Quick start

_1. **Install dependencies**
   ```bash
   cd mCODE-browser
   uv sync
   ```_

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and set:
   #   SUPABASE_URL=https://xxxx.supabase.co
   #   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   #   SECRET_KEY=''
   #   WTF_CSRF_SECRET_KEY=''
   ```

3. **Add the missing static assets**
   - Copy your original `ontology-data.js` into `static/js/`

4. **Run**
     ```bash
      # Go to the source folderT
      cd src
      ```
   - Flask development server
      ```bash
      # To run a Flask development server accessible externally - replace the port as needed -
      uv run flask run --host=0.0.0.0 -p 8085
      ```
      Open http://localhost:5000
   - gunicorn server
      ```bash
      # To run a gunicorn server accessible externally - replace the port as needed -
      uv run gunicorn -w 3 "wsgi:app" -b 0.0.0.0:8085
      ```

## Next steps you may want later

- Move `ontology-data.js` (or the processed registry) into a database / JSON file served by `/api/ontology/data`
- Add authentication around the feedback endpoints
- Replace the Visualization placeholder with a real WebVOWL / D3 / vis.js canvas
- Serve the frontend from a CDN or build step if the app grows further

## API reference

### `GET /api/feedback`
Returns the full feedback object in the exact shape the frontend already uses:

```json
{
  "some-node-id": {
    "classId": "some-node-id",
    "className": "Class Label",
    "notes": [
      { "timestamp": "...", "tag": "Correction Required", "text": "..." }
    ]
  }
}
```

### `POST /api/feedback`
Body:
```json
{
  "node_id": "class-id",
  "class_name": "Class Label",
  "comment": "My note",
  "tag": "General Comment"
}
```

### `GET /api/health`
Simple liveness check.
Returns the status 200 / "ok" if the api is running:
```json
{
  "status": "ok",
  "timestamp": "2026-08-20T22:33:42.009839"
}
```

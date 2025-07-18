# AI Letter Generation Agent

This project is an AI-powered automation tool for generating professional company letters and exporting them to Google Docs. It features a FastAPI backend, a modern chat-based frontend, and deep integration with Google Drive and OpenAI (or compatible LLMs) via LangChain.

---

## 📁 File Structure

```
report_agent copy/
├── backend/
│   ├── app.py                        # FastAPI backend entrypoint and API endpoints
│   ├── letter_agent.py               # Core automation logic for letter generation (LangChain agent)
│   ├── google_docs.py                # Google Docs API integration for document creation
│   ├── client_secret.json            # [PLACEHOLDER] Google OAuth client credentials (do not commit real secrets)
│   ├── report-agent-...json          # [PLACEHOLDER] Google service account credentials (do not commit real secrets)
│          
├── frontend/
│   └── main.html                     # Modern chat UI for interacting with the agent
└──              
```

---

## 🚀 Setup & Installation

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials**
   - Place your Google OAuth and service account credentials in `backend/client_secret.json` and `backend/report-agent-...json` (see the provided placeholder files for structure).
   - Set your OpenAI or compatible API key as an environment variable (`OPENAI_API_KEY`).
   - Update any other placeholders in `letter_agent.py` and `google_docs.py` (e.g., Google Drive folder IDs, template IDs).

4. **Run the backend**
   ```bash
   uvicorn backend.app:app --reload
   ```

5. **Open the frontend**
   - Open `frontend/main.html` in your browser.
   - Ensure the backend is running at `http://localhost:8000` (or update the API URL in the HTML if needed).

---

## 🧠 Workflow: How Letter Automation Works

### 1. **User Interaction**
- The user interacts with a chat interface (`frontend/main.html`), sending prompts describing the letter they want to generate.

### 2. **API Request**
- The frontend sends the user's message to the `/chat` endpoint of the FastAPI backend (`backend/app.py`).

### 3. **LetterGenerationAgent (Core Logic)**
- The backend manages conversation state and delegates the request to a `LetterGenerationAgent` (see `backend/letter_agent.py`).
- The agent uses LangChain's ReAct framework, combining:
  - **Company context**: Loads relevant documents from Google Drive (via `GoogleDriveLoader`).
  - **LLM reasoning**: Uses OpenAI (or compatible) LLM to generate letter content, recipient details, and role.
  - **Custom tools**:
    - `get_current_datetime`: Fetches the current date/time.
    - `get_company_context`: Extracts company/recipient info from loaded docs.
    - `generate_formal_letter`: Assembles a formal letter using a template and LLM-generated content.
    - `create_google_doc_from_letter`: Converts the letter into a Google Doc and returns the shareable URL.
- The agent follows a workflow:
  1. Extract recipient info from company docs.
  2. Generate main content and role using the LLM.
  3. Assemble the letter in a formal template.
  4. Optionally, create a Google Doc and return the link.

### 4. **Response**
- The backend returns the generated letter (and optionally a Google Doc link) to the frontend, which displays it in the chat.

---

## 📝 API Endpoints

- `GET /` — Health check
- `POST /chat` — Main chat endpoint (send user prompt, get letter response)
- `POST /new-conversation` — Start a new chat session
- `DELETE /conversation/{conversation_id}` — Delete a session
- `GET /conversations` — List all active sessions

---

## ⚙️ Dependencies

See `requirements.txt` for all dependencies. Key packages:
- `fastapi`, `uvicorn` — API server
- `langchain`, `langchain-openai`, `langchain-google-community` — LLM and tool orchestration
- `openai` — LLM API
- `google-auth`, `google-api-python-client`, `google-auth-oauthlib` — Google Docs/Drive integration
- `python-dotenv` — Environment variable management

---

## 🔒 Security & Secrets
- **Never commit real API keys or credentials.** Use the provided placeholder files and environment variables.
- The `__pycache__` folders contain only compiled Python files and can be ignored.

---


**Built by Shilok Kumar**


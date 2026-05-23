# AI Research Agent 

An advanced AI-powered research assistant designed to automate the academic research workflow. This agent can search for recent papers on ArXiv, extract knowledge from PDFs, synthesize new research directions, and generate professional, publication-ready LaTeX PDFs.

## 🌟 Key Features

- **Automated ArXiv Search**: Find the latest research papers in fields like Physics, AI, CS, and Economics using a custom ArXiv tool.
- **Deep PDF Extraction**: Intelligently reads and parses PDF content from ArXiv links to understand complex methodologies.
- **Synthesized Research**: Uses Google's `gemini-2.5-flash` to identify promising future research directions based on current state-of-the-art papers.
- **LaTeX PDF Generation**: Automatically writes and renders new research papers into high-quality PDFs using the Tectonic typesetting engine.
- **Interactive Agent Loop**: Built with LangGraph for a robust, multi-step conversational research experience.
- **Streamlit Web Interface**: A clean, interactive graphical UI for managing the conversational research flow.
## 🏗️ Architecture

The agent is built using a **ReAct (Reasoning + Acting)** framework powered by:
- **LLM**: Google Gemini 2.5 Flash
- **Framework**: LangChain & LangGraph
- **Typesetting**: Tectonic (LaTeX)
- **Data Source**: ArXiv API

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- **Tectonic**: Required for rendering LaTeX to PDF.
  - [Install Tectonic](https://tectonic-typesetting.org/en-US/install.html)
- **Google AI API Key**: Get your key from [Google AI Studio](https://aistudio.google.com/).

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rajiv-rane/research-agent.git
   cd research-agent
   ```

2. **Install dependencies**:
   This project uses `uv` for fast dependency management.
   ```bash
   uv sync
   ```
   *Alternatively, use pip:*
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

## 📖 Usage

### Option 1: Streamlit Web UI (Recommended)
Run the interactive web interface for a user-friendly conversational experience:

```bash
streamlit run frontend.py
```

### Option 2: Terminal/CLI Mode
Run the main agent script to start a research session directly in the terminal:

```bash
python ai_researcher2.py
```
*(Note: `ai_researcher2.py` contains the latest agent setup with optimized prompt structures and safety threshold configurations.)*

### Example Workflow:
1. **Topic Selection**: Discuss a research area (e.g., "Quantum Neural Networks").
2. **Paper Discovery**: The agent searches ArXiv and presents recent papers.
3. **Deep Dive**: Choose a paper for the agent to read and analyze.
4. **Idea Generation**: The agent suggests new research directions.
5. **Paper Writing**: The agent writes a full paper with LaTeX equations.
6. **PDF Delivery**: A PDF is generated in the `output/` folder.

## 📂 Project Structure

- `frontend.py`: Streamlit-based graphical user interface.
- `ai_researcher2.py` / `ai_researcher.py`: The main entry point and agent logic for the CLI and backend.
- `arxiv_tool.py`: custom tool for searching the ArXiv API.
- `read_pdf.py`: Tool for extracting text from online PDF files.
- `write_pdf.py`: Tool for rendering LaTeX content into PDFs using Tectonic.
- `pyproject.toml`: Project configuration and dependencies.

## 🛠️ Tech Stack

- **LangGraph**: Orchestrating the agentic workflow.
- **LangChain**: Tooling and LLM abstractions.
- **Gemini 2.5 Flash**: The brain of the assistant.
- **PyPDF2**: PDF text extraction.
- **Requests**: API communication.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built with ❤️ for the research community.*

# Dual-Mind

Compare Claude Sonnet 4.5 and GPT-4 Turbo responses side-by-side. Never ship AI hallucinations again.

![[Dual-Mind Demo](https://dual-mind.streamlit.app/)](<img width="1919" height="1008" alt="image" src="https://github.com/user-attachments/assets/2409352f-a6b5-4c8d-84de-3d92fec88bf0" />
)

## Why This Exists

Got different answers from Claude and GPT-4 for the same question. Both sounded confident. Both were plausible. Only one was correct.

Dual-Mind runs both models in parallel so you can:
- Spot contradictions before they become bugs
- See which model is better for specific tasks
- Track exactly what you're spending on API calls

## Features

- **Parallel execution**: Both models respond simultaneously
- **Cost tracking**: Real-time token usage and dollar amounts
- **Conversation history**: SQLite storage with search
- **Demo mode**: Test without API keys
- **Local-first**: Your API keys never leave your machine

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
streamlit run dual_mind_mvp.py
```

Open http://localhost:8501 in your browser.

### Demo Mode

Enable "Demo Mode" in the sidebar to test the interface with simulated responses. No API keys required.

### Real APIs

Uncheck "Demo Mode" and add your API keys:
- **Anthropic API Key**: Get from https://console.anthropic.com
- **OpenAI API Key**: Get from https://platform.openai.com/api-keys

## Cost

Approximately $0.03 per dual query:
- Claude Sonnet 4.5: ~$0.01 per response
- GPT-4 Turbo: ~$0.02 per response

All costs tracked in real-time in the sidebar.

## What I've Learned Using This

**Claude excels at:**
- Debugging code
- Spotting edge cases
- Implementation details

**GPT-4 excels at:**
- System architecture
- Explaining concepts
- Creative solutions

**When both agree on specifics → high confidence it's correct**  
**When they contradict → investigate further**

## Examples

Try these queries to see model differences:
```
"Debug this React component with a memory leak"
"Review my microservices architecture design"
"Best way to handle authentication in Flask?"
```

## Roadmap

- [ ] Hallucination detection (highlights contradictions automatically)
- [ ] Confidence scoring (quantifies certainty per response)
- [ ] Debate mode (models respond to each other's answers)
- [ ] Model selection (add Gemini, Claude Haiku, GPT-3.5)
- [ ] Export conversations to markdown
- [ ] Prompt variant testing

## Technical Details

**Stack**: Python, Streamlit, SQLite  
**APIs**: Anthropic Messages API, OpenAI Chat Completions API  
**Storage**: Local SQLite database (`dual_mind.db`)  
**State**: Streamlit session state (no external dependencies)

## Privacy

- API keys stored in session state only (cleared on browser close)
- All data stored locally in SQLite
- No external logging or analytics
- Your conversations never leave your machine

## Contributing

PRs welcome. Focus areas:
1. Hallucination detection algorithms
2. Additional model integrations
3. Export/import functionality
4. UI improvements

## License

MIT

## Author

Built by [your-name] because I got burned by AI hallucinations one too many times.

## Support

If this saved you from shipping a bug, star the repo ⭐
```

**Save as**: `requirements.txt` and `README.md` in your project root.

**Before pushing**, add `.gitignore`:
```
# .gitignore
dual_mind.db
__pycache__/
*.pyc
.streamlit/
venv/
env/
.env
*.db-journal

.DS_Store

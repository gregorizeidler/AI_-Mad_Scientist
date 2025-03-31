# 🧪 AI Mad Scientist

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/Streamlit-Latest-FF4B4B.svg" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/OpenAI-API-412991.svg" alt="OpenAI API"/>
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"/>
</div>

<p align="center">
  <i>Generate creative, absurd, and thought-provoking scientific theories with specialized AI agents</i>
</p>

---

## 📋 Overview

AI Mad Scientist is a sophisticated Streamlit application that harnesses the power of AI to generate, evaluate, and refine creative scientific theories. It leverages a diverse ecosystem of specialized AI agents, each with unique perspectives and creativity levels, to transform your ideas into engaging scientific narratives.

<div align="center">
  <h3>📺 Watch the Demo Video</h3>
  <a href="https://drive.google.com/file/d/1Oe3WwBT8yh3SKNsb7chqcYgnP3ygK8Zm/view?usp=sharing" target="_blank">
    <img src="https://via.placeholder.com/800x400?text=AI+Mad+Scientist+Demo+Video" alt="AI Mad Scientist Demo" width="80%"/>
  </a>
  <p><i>Click the image above to watch the demonstration video (US version)</i></p>
</div>

## ✨ Key Features

- 🧠 **Multi-Agent Architecture** - A diverse ecosystem of specialized AI agents with unique characteristics
- 🌡️ **Temperature Control** - Adjust creativity levels from analytical to wildly imaginative
- 🔬 **Scientific Plausibility Assessment** - Visual plausibility meter for theories
- 🎭 **Scientific Debate Mode** - Watch AI agents debate the merits of theories
- 🤖 **Custom Agent Creation** - Design your own specialized agents with unique perspectives
- 📥 **Export to PDF** - Save and share your generated theories with customized formatting
- 📚 **Theory History** - Track and revisit previously generated theories
- 🎨 **Modern UI** - Intuitive, responsive interface with dark mode support

## 🤖 Agent Ecosystem

Our application employs a sophisticated system of specialized agents, each with a specific function and creativity level controlled by temperature parameters:

### High Creativity Agents (Temperature 0.8-1.5)
- **💣 ExplosiveGPT** - Generates bold, absurd hypotheses to spark innovation
- **🧨 EvolutiveGPT** - Creates advanced versions with cutting-edge technological elements

### Medium Creativity Agents (Temperature 0.5-0.7)
- **📖 NarratorGPT** - Transforms theories into engaging science fiction narratives
- **🧠 ConnectorGPT** - Establishes interdisciplinary connections between fields
- **🎤 PitchGPT** - Creates persuasive presentations for investors
- **🔬 TesterGPT** - Evaluates scientific plausibility with a visual meter
- **🛡️ DefenderGPT** - Presents the strongest possible case for theories
- **⚔️ ChallengerGPT** - Identifies flaws and counterarguments in theories

### Low Creativity Agents (Temperature 0.3-0.4)
- **👓 CriticGPT** - Provides rigorous peer-review style critique
- **💼 ViabilityGPT** - Analyzes practical implementation feasibility
- **🧵 SummarizerGPT** - Synthesizes theories into concise scientific abstracts
- **🔍 ResearcherGPT** - Transforms creative ideas into serious research questions

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-mad-scientist.git
   cd ai-mad-scientist
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your OpenAI API key**
   - Create a `.env` file in the project root
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

### Running the App

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## 📊 Usage Modes

### Quick Mode
Generate ideas rapidly with minimal processing:
- 💣 ExplosiveGPT: Initial hypothesis
- 🧵 SummarizerGPT: Concise summary

### Standard Mode
Balanced creativity and analysis:
- 💣 ExplosiveGPT: Hypothesis generation
- 🔬 TesterGPT: Scientific evaluation
- 🧠 ConnectorGPT: Interdisciplinary connections
- 🧵 SummarizerGPT: Final synthesis

### Complete Mode
Comprehensive theory development:
- All agents contribute their unique perspectives
- Full scientific evaluation and refinement
- Multiple formats (abstract, narrative, pitch)

### Debate Mode
Dialectical exploration of theories:
- 🛡️ DefenderGPT vs ⚔️ ChallengerGPT
- Multiple rounds of structured debate
- Strengthening through critical examination

## 🎛️ Advanced Features

### Temperature Control
Fine-tune the creativity level of your agents:
- Higher temperatures (0.8-1.5): More creative, innovative, and surprising outputs
- Medium temperatures (0.5-0.7): Balanced creativity and coherence
- Lower temperatures (0.3-0.4): Focused, analytical, and methodical responses

### Custom Agent Creation
Design your own specialized agents:
- Choose a distinctive emoji and name
- Define area of expertise and temperature
- Craft custom instructions for unique perspectives
- Seamless integration with existing agents

### Plausibility Meter
Visual assessment of scientific validity:
- 0-20: Completely implausible (Red)
- 21-40: Highly questionable (Orange)
- 41-60: Speculative but possible (Yellow)
- 61-80: Plausible (Light green)
- 81-100: Highly plausible (Dark green)

### 🌎 International Versions
The AI Mad Scientist application is available in multiple regional versions:
- 🇺🇸 **US Version** - [View Demo](https://drive.google.com/file/d/1Oe3WwBT8yh3SKNsb7chqcYgnP3ygK8Zm/view?usp=sharing)
- 🇧🇷 **Brazil Version** - Coming soon
- 🇪🇺 **Europe Version** - Coming soon
- 🇯🇵 **Japan Version** - Coming soon

Each regional version includes localized examples, culturally-relevant themes, and region-specific scientific references.

## 📁 Project Structure

```
ai-mad-scientist/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Project dependencies
├── .env                        # Environment variables (API keys)
├── AGENTS_TEMPERATURE.md       # Temperature guide documentation
├── agents_visualization.html   # Interactive agent visualization
└── saved_theories/             # Directory for saved theories
```

## 📚 Additional Documentation

- **[AGENTS_TEMPERATURE.md](./AGENTS_TEMPERATURE.md)** - Detailed guide on temperature settings and their effects on creativity.
- **[agents_visualization.html](./agents_visualization.html)** - Interactive visualization of agents and their characteristics.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [OpenAI](https://openai.com/) for their powerful API
- [Streamlit](https://streamlit.io/) for the amazing web app framework
- All contributors and users who provide feedback

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/yourusername">Your Name</a>
</p> 

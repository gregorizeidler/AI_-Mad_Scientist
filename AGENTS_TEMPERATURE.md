# 🌡️ Temperature and Agents Guide for AI Mad Scientist

This document provides detailed information on how temperature affects the creativity of agents in our system and how you can adjust these parameters to achieve the desired results.

## Understanding Temperature in LLMs

Temperature is a crucial hyperparameter in language models that controls the randomness (or diversity) of generated responses:

```
Low temperature (close to 0) → More deterministic and predictable responses
High temperature (close to 2) → More diverse, creative, and unpredictable responses
```

## Temperature Diagram of Agents

Below is a visual representation of agents organized by temperature:

```
TEMPERATURE  │  AGENTS                     │  CHARACTERISTICS
─────────────┼─────────────────────────────┼──────────────────────────────────
             │                             │
    2.0      │                             │  Extremely creative
             │                             │  Highly unpredictable
    1.5      │                             │  Frequently innovative
             │                             │  May generate absurd concepts
    1.0 ─────┼─ 💣 ExplosiveGPT (adjustable)┼─ Highly creative
             │                             │  Non-obvious connections
    0.9 ─────┼─ 🧨 EvolutiveGPT ───────────┼─ Innovative, futuristic
             │                             │  Concept elaborator
    0.8      │                             │
             │                             │
    0.7 ─────┼─ 📖 NarratorGPT ────────────┼─ Creative with structure
             │                             │  Imaginative narrative
    0.6 ─────┼─ 🧠 ConnectorGPT ────────────┼─ Interdisciplinary connections
             │  🎤 PitchGPT                │  Balance between creativity and logic
    0.5 ─────┼─ 🔬 TesterGPT ─────────────┼─ Analytical but open to innovation
             │                             │  Scientific validation 
    0.4 ─────┼─ 👓 CriticGPT ─────────────┼─ Detailed critical analysis
             │  💼 ViabilityGPT            │  Pragmatic, fact-checking
    0.3 ─────┼─ 🧵 SummarizerGPT ───────────┼─ Highly focused
             │                             │  Synthetic and precise
    0.2      │                             │  
             │                             │
    0.1      │                             │  Extremely deterministic
             │                             │  Repetitive
    0.0      │                             │  No variability
```

## Agent Workflow

The system is designed to function as a creativity pipeline, where ideas flow from more creative agents to more analytical ones:

```
   GENERATION           EXPLORATION            ANALYSIS              SYNTHESIS
┌─────────────┐       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│ HIGH TEMP   │       │ MEDIUM TEMP │       │ LOW TEMP    │       │ LOW TEMP    │
│             │       │             │       │             │       │             │
│ ExplosiveGPT│─────▶│ TesterGPT   │─────▶│ CriticGPT   │─────▶│SummarizerGPT│
│ EvolutiveGPT│       │ ConnectorGPT│       │ ViabilityGPT│       │             │
│             │       │ NarratorGPT │       │             │       │             │
│             │       │ PitchGPT    │       │             │       │             │
└─────────────┘       └─────────────┘       └─────────────┘       └─────────────┘
      ▲                                           │                      │
      │                                           │                      │
      └───────────────────────────────────────────┘                      │
                          Feedback                                       │
      ┌─────────────────────────────────────────────────────────────────┘
      │                       Refinement
      ▼
┌─────────────┐
│  FINAL      │
│  RESULT     │
└─────────────┘
```

## Adjusting Temperatures for Different Objectives

Depending on your objectives, you may want to adjust temperatures in different ways:

### For Extremely Creative and Disruptive Theories

- Increase ExplosiveGPT temperature to 1.5-2.0
- Increase EvolutiveGPT temperature to 1.2-1.5
- Maintain medium temperatures for analytical agents (0.4-0.6)

### For More Scientifically Plausible Theories

- Moderate ExplosiveGPT temperature to 0.8-1.0
- Increase analytical agents' temperature to 0.6-0.7
- Keep SummarizerGPT temperature low (0.3-0.4)

### For Educational Exploration

- Keep ExplosiveGPT temperature around 0.9-1.1
- Increase ConnectorGPT temperature to 0.7-0.8
- Increase TesterGPT temperature to 0.6-0.7

## Interesting Temperature Experiments

Try these configurations for interesting results:

### "Inverted World"
Completely invert the temperatures: use low values for creative agents and high for analytical agents. This can produce analytically constructed theories that are evaluated in a creative and unconventional way.

### "Creativity Cascade"
Configure the agents with a smooth temperature gradation, from highest to lowest:
- ExplosiveGPT: 1.5
- EvolutiveGPT: 1.3
- NarratorGPT: 1.1
- ConnectorGPT: 0.9
- PitchGPT: 0.7
- TesterGPT: 0.5
- CriticGPT: 0.3

### "Controlled Explosion"
Keep ExplosiveGPT very high (1.8) and all other agents very low (0.3-0.4). This creates an extremely creative idea that is then evaluated with great rigor.

## Important Observations

1. **Extreme temperatures** can generate incoherent or nonsensical content
2. **The ideal balance** varies depending on the theme being explored
3. **Some themes** work better with high temperatures, others with low temperatures
4. **Experiment** with different configurations to find your preferred style

## Recommendations by Knowledge Area

| Area | Temperature Recommendation |
|------|----------------------------|
| Theoretical Physics | High (generates speculative theories) |
| Biology | Medium-High (allows innovation while maintaining plausibility) |
| History | Medium (balances creativity with facts) |
| Engineering | Medium-Low (favors viable ideas) |
| Mathematics | Low-Medium (prioritizes logical consistency) |

## Measuring Success

A successful theory in AI Mad Scientist generally exhibits:

1. **Originality** - An idea you wouldn't have easily thought of
2. **Coherence** - An internal logic that makes sense, even if unlikely
3. **Inspirational potential** - The ability to make you think in new ways
4. **Sensible chaining** - Each agent can work with the result of the previous one

Have fun experimenting with different temperature configurations and find the perfect balance between creative madness and analytical rigor! 

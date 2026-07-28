<h1 align="center">{{ app_name }}</h1>

<p align="center">
  <strong>{{ app_description }}</strong>
</p>
<p align="center">
  Created with 💪 by {{ creator_name }}
</p>

<br/>

## 🚀 Welcome to Your New Journey

Your **{{ app_name }}** project is ready. It gives you a working foundation for a data analysis tool, a web service, or an AI-powered application.

<br/>

### 🎯 What's Next?

Some directions you might take from here:

{% if feature_ai == "Y" %}
- **Agentic AI**: Built in and governed, ask via ```{{ app_label }} ai ask```, every tool call passes validate, policy, audit and more.
{% else %}
- **AI Integration**: Add intelligence by integrating LLMs or classic ML pipelines
{% endif %}
- **Data Exploration**: Uncover insights by analyzing data with pandas, matplotlib, or seaborn
- **Web Interfaces**: Create beautiful dashboard and web tools with the built-in NiceGUI extension and tailwindcss based admin theme
- **Automation**: Schedule tasks and create workflows with the scheduler extension or total local and remote automation
- **API Development**: Build robust APIs for your services

Remember, every great application started exactly where you are now!

<br/>

## 🛠️ Getting Started

### Installation

First, set up your virtual environment:

```bash
# Create and activate virtual environment
make venv
source .venv/bin/activate

# Install development dependencies
make dev
```

### Running Your Application

Once installed, you can launch your application:

```bash
# See available commands
{{ app_label }} --help

# Run a specific command
{{ app_label }} <command>
```

{% if feature_grpc == "Y" %}
### Compiling Protocol Buffers

If you're using gRPC services, you have to run:

```bash
# Generate Python code from proto files
make proto
```
{% endif %}

<br/>

## 📊 Exploring Tokeo Features

{% if feature_dramatiq == "Y" %}
### Process Background Tasks with Dramatiq (needs a running RabbitMQ)

```bash
# Launch Dramatiq workers to process background tasks
{{ app_label }} dramatiq serve

# Trigger a task (e.g., count-words)
{{ app_label }} emit count-words --url https://github.com
```

{% endif %}
{% if feature_grpc == "Y" %}
### Expose Services via gRPC

```bash
# Start the gRPC server for external task access
{{ app_label }} grpc serve

# Execute a task using the gRPC client
{{ app_label }} grpc-client count-words --url https://github.com
```

{% endif %}
{% if feature_apscheduler == "Y" %}
### Schedule Recurring Tasks

```bash
# Run the scheduler with interactive shell
{{ app_label }} scheduler launch

# Within the scheduler shell, list and manage tasks
Scheduler> list
Scheduler> tasks pause 1 2 3  # Pause task with ID 1, 2, 3
Scheduler> tasks resume 1  # Resume task with ID 1
Scheduler> tasks fire 1  # Resume task with ID 1
```

{% endif %}
{% if feature_automate == "Y" %}
### Automate Operations

```bash
# Run automation tasks locally or remotely
{{ app_label }} automate run uname --verbose --as-json
```

{% endif %}
{% if feature_nicegui == "Y" %}
### Create Web Interfaces

```bash
# Start the web interface
{{ app_label }} nicegui serve

# Access the interface at http://localhost:4123
```

{% endif %}
{% if feature_diskcache == "Y" %}
### Use Diskcache

```bash
# List content
{{ app_label }} cache list

# Set value
{{ app_label }} cache set counter --value 1 --value-type int

# Get value
{{ app_label }} cache get counter
```

{% endif %}
{% if feature_ai == "Y" %}
### Ask an AI Agent

Your application speaks to AI providers through one governed runtime. The model plans, the pipeline governs, the tools compute. Profiles and agents are plain YAML in ```config/```: ```audited``` records everything and forbids nothing, ```guarded``` adds validation and policy. The tools are your own plain functions in ```{{ app_label }}/core/ai/tools/```, activated in groups per profile.

```bash
# The mock provider answers without any external service
{{ app_label }} ai ask "ping"

# Inspect agents, profiles, and registered tools
{{ app_label }} ai list
```
{% if feature_ai_akili == "Y" %}

Your project also ships **akili**, a train-first micro LLM (~600K parameters, ~2.5 MB) that plans calendar tool calls. No weights are included. You create them, and that is the point:

```bash
# Train on your machine (CPU is fine)
python -m {{ app_label }}.core.akili.train

# Then ask in English or German (guarded, traced, deterministic)
{{ app_label }} ai ask "the weekday of today plus 2 days" --profile akili --agent guarded
{{ app_label }} ai ask "welches datum ist übermorgen" --profile akili
```

The model's whole language lives in ```{{ app_label }}/core/akili/AKILI-LEX.yaml```: teach it new words and sentence patterns by editing the file and retraining. ```AKILI-LLM.md``` next to it explains training, the anatomy of the weights, and grammar-constrained decoding with detailed diagrams.
{% endif %}

{% endif %}

<br/>

## 📊 Development Tools

This project includes several helpful commands to streamline your development:

```bash
# Format your code
make fmt

# Run linting checks
make lint

# Run tests
make test

# Run tests with coverage report
make test cov=1

# Build documentation
make doc

# Check for outdated dependencies
make outdated
```

<br/>

## 🚀 Deployment Options

### Package Your Application

```bash
# Create source distribution
make sdist

# Create wheel package
make wheel

# Build Docker image
make docker
```

<br/>

## Control Logging

Set log levels via config, environment variables, or CLI flags:

```bash
# App debug logs
{{ app_label | upper }}_LOG_COLORLOG_LEVEL=debug {{ app_label }} command

# App + framework debug logs
{{ app_label }} --debug command

# Framework debug logs only
CEMENT_LOG=1 {{ app_label }} command
```

<br/>

## 📚 Project Structure

Your project is organized into a clean, modular structure:

- ```config/``` - Configuration files for prod, stage, dev and test environments
- ```{{ app_label }}/core/logic``` - Space for your core application logic
- ```{{ app_label }}/core/tasks/``` - Implementations of actors, agents, automations, operations, performers etc.
{% if feature_ai == "Y" %}
- ```{{ app_label }}/core/ai/``` - AI providers and plain-function tools behind the guarded contracts
{% endif %}
{% if feature_ai == "Y" and feature_ai_akili == "Y" %}
- ```{{ app_label }}/core/akili/``` - The train-first micro LLM lab: model, lexicon (```AKILI-LEX.yaml```), teaching docs
{% endif %}
{% if feature_grpc == "Y" %}
- ```{{ app_label }}/core/grpc/``` - gRPC service definitions and implementations
{% endif %}
- ```{{ app_label }}/core/utils/``` - A place to put your overall tools and helper functions
- ```{{ app_label }}/controllers/``` - Command-line interface controllers
{% if feature_ai == "Y" %}
- ```{{ app_label }}/pact/ai/``` - AI util-functions necessary for sandboxes
{% endif %}
{% if feature_nicegui == "Y" %}
- ```{{ app_label }}/site/``` - Web interface pages and apis
{% endif %}
- ```{{ app_label }}/templates/``` - Templates for rendering content
- ```tests/``` - Test suite to ensure reliability

<br/>

## 🌟 Making It Your Own

As you build and shape this project, consider:

- What problem are you trying to solve?
- Who will use your application and how?
- How can you make it not just functional, but pleasant to use?
{% if feature_ai == "Y" %}
- Which routine work could a governed agent take over and which tools would you trust it with?
{% endif %}

<br/>

## 🔄 Continuous Improvement

Keep your project healthy with these practices:

- Document your code and add examples
- Write tests for new features
- Refactor when needed for clarity
- Stay up-to-date with your packages using ```make outdated```

<br/>

## Tokeo packages

- **Tokeo** is the event-driven CLI framework: the command surface, messaging, scheduling, automation, gRPC, web, vault, and the project generator.
- **Ramani** ships all the project templates, including the AI template and the akili lab that gets generated into your application.
{% if feature_ai == "Y" %}
- **Fundi** (```tokeo-fundi```) is the source-available AI runtime.
{% if feature_ai_akili == "Y" %}
- **Akili** is generated by ```tokeo generate``` from Ramani's template and placed into your application for demonstration purposes under ```{{ app_label }}/core/akili/```.
{% endif %}
{% endif %}

<br/>

## ⚖️ Licensing

These generated project sources are yours. Use them freely and license them however you like. This scaffold imposes no attribution requirement and no license of its own on your code.

That covers the code you take from here. It does not extend to the third-party packages a project installs, those keep their own licenses.

Tokeo's author believes in empowering the community while building a sustainable ecosystem. That's why Tokeo and its extensions use a dual-approach to licensing:

**The Tokeo Core Framework (Apache 2.0)**

Tokeo's author transitioned the core Tokeo framework from its original MIT license to the **Apache 2.0 license**. This switch wasn't primarily about Tokeo itself. It was made to provide *you*, the implementer and the project, with absolute legal certainty. In addition, the Apache 2.0 license includes explicit patent grants and protection, giving your projects a legally safe and rock-solid foundation to build upon.

{% if feature_ai == "Y" %}
**The Tokeo Fundi Agent AI Extension (Source-Available License)**

The optional ```tokeo-fundi``` is the agentic framework that powers the tokeo ai features: agents, tools, governors, sandboxing, audit and more. It is a dependency, not part of these sources, and it is **not** open source but fair source and source available released by the custom **Tokeo-Fundi Source-Available License 1.0**. Please don't let this scare you off! Tokeo's author is deeply committed to keeping software free for the community. If you are a hobbyist, a startup, or a small team, ```tokeo-fundi``` is **free of charge** for you to use in any personal, internal or commercial project.

However, to keep the tokeo project healthy, actively developed, and sustainable, this license introduces a fair-use threshold. Businesses with highly successful commercial operations (across the whole group: more than EUR 2,000,000 in fiscal year global gross revenue excluding VAT, or more than 50 FTEs) are required to purchase a commercial Enterprise License. The license also restricts using its source code as training data for machine-learning systems. Read the complete and authoritative terms in ```LICENSE.md``` of the [tokeo-fundi](https://github.com/tokeo/fundi/) distribution.

From Tokeo's author — I believe this is a fair balance: those who achieve significant economic success using this software should contribute back to the developers making it possible.

{% if feature_ai_akili == "Y" %}
**The Tokeo Akili Demonstration LLM (Apache 2.0)**

There is an exception among the sources in ```{{ app_label }}.core.akili``` module. It is meant as a demonstration and is not intended for delivery. It ships so you can experiment and learn, and it can be removed without side effects.

If you really have reasons to keep ```akili``` in your own project, its files must remain under the Apache License, Version 2.0. Make sure to comply with that license. Keep the file headers and the ```LICENSE.txt``` copy in the ```{{ app_label }}/core/akili``` directory.

To put it another way: the purpose of ```akili``` is lab work. Use it to understand LLMs, to learn how to build one yourself, and how to equip it with tools. It is there to give you the idea and the know-how to reach your own goals efficiently. For that reason ```akili``` normally does not belong in your delivered project and this README.
{% endif %}
{% endif %}

<br/>

## 🤝 Need Help?

If you encounter challenges or have questions:

- Check the Tokeo documentation
- Explore similar open-source projects for inspiration
- Connect with the community of developers

<br/>
<br/>

Built with ❤️ and <a href="https://github.com/tokeo/tokeo">tokeo</a> - Empowering Python Applications

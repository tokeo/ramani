<br/>

<h1 align="center">ramani</h1>

<p align="center">
  <strong>Project blueprints for Tokeo. The templates behind <code>tokeo generate project</code>.</strong>
</p>

<br/>

## 🗺️ What is Ramani?

*Ramani* is Kiswahili for map or blueprint. It ships the `generate` templates that the [Tokeo](https://github.com/tokeo/tokeo) CLI uses to scaffold a complete application. It is packaged as its own distribution, separate from the framework.

Ramani carries no runtime logic and no framework dependency of its own. It is a pure template payload.

<br/>

## 🛠️ Getting Started

### Adding the templates to Tokeo

```bash
# Install directly from Pypi.org, alongside Tokeo
pip install tokeo-ramani
```

After the install, the `generate` templates are available to the `tokeo` CLI. No extension to load. No path to register.

### Creating a New Project

Set up a Tokeo project in minutes:

```bash
# Generate a new project (interactive prompts)
tokeo generate project your_app
```

<br/>

## 🌿 Features to enable

The `project` blueprint is driven by interactive prompts. The same template produces anything from a minimal CLI up to a full event-driven backend:

- **Dramatiq** background task processing (paired with RabbitMQ)
- **gRPC** service for external task and workflow access
- **APScheduler** cron service for timed job execution
- **Automate** (Fabric-based) local and remote task automation
- **smtpd** mail-receiving service that turns SMTP messages into events
- **NiceGUI** web interface for pages and APIs
- **DiskCache** disk-based caching
- **AI branch** needs [tokeo-fundi](https://github.com/tokeo/fundi)

Answer a feature with *no* and the generated project does not contain it. Neither its code nor its dependencies.

### akili, the train-first micro LLM demo

When you generate a project with the AI feature, you may also add `akili`. It is a small, teachable language model that plans calendar tool calls:

- **A few hundred thousand parameters, ~1.5 MB.** Byte-level tokenizer, NumPy-only inference in tens of milliseconds, no GPU and no service.
- **Train first, no shipped weights.** `python -m your_app.core.akili.train` creates the model on your machine. CPU is fine.
- **The language is data.** Every word and sentence pattern lives in `AKILI-LEX.yaml`. Teaching the model new language means editing a file and retraining.
- **Grammar-constrained planning.** A byte-level automaton makes malformed plans impossible.
- **Taught, not just documented.** `AKILI-LLM.md` explains training, the anatomy of the weights, and constrained decoding.

The `akili` module is in general a self-contained demonstration only. It should not be required by the generated application and should be removed without side effects.

<br/>

## 📊 Exploring the Generated Project

Once generated, the generated project exposes each selected feature through its own commands:

```bash
# Process background tasks with Dramatiq (needs a running RabbitMQ)
your_app dramatiq serve
your_app emit count-words --url https://github.com

# Expose services via gRPC
your_app grpc serve
your_app grpc-client count-words --url https://github.com

# Schedule recurring tasks
your_app scheduler launch

# Automate operations locally or remotely
your_app automate run uname --verbose --as-json

# Receive emails with the SMTPD service
your_app smtpd serve

# Create web interfaces
your_app nicegui serve

# Ask an AI agent (requires the AI branch / tokeo-fundi)
your_app ai ask "add 14 days to 2026-06-08" --profile akili --agent guarded
```

<br/>

## 📚 Generated Project Structure

Every `project` blueprint expands into a clean, modular layout:

- `config/` - Configuration files for prod, stage, dev and test environments
- `your_app/core/logic` - Space for your core application logic
- `your_app/core/tasks/` - Implementations of actors, agents, automations, operations, performers etc.
- `your_app/core/ai/` - AI providers and plain-function tools behind the guarded contracts (when the AI branch is selected)
- `your_app/core/akili/` - The train-first micro LLM lab: model, lexicon (`AKILI-LEX.yaml`), teaching docs (when the AI branch is selected)
- `your_app/core/grpc/` - gRPC service definitions and implementations
- `your_app/core/utils/` - A place to put your overall tools and helper functions
- `your_app/controllers/` - Command-line interface controllers
- `your_app/site/` - Web interface pages and apis
- `your_app/templates/` - Templates for rendering content
- `tests/` - Test suite to ensure reliability

<br/>

## 🔮 Next Steps

The generated project is designed to grow with you. As you build, consider:

- Customizing the application structure for your specific needs
- Creating new controllers for additional commands
- Adding task processors for background workloads
- Designing web interfaces to visualize data
- Adding the optional [tokeo-fundi](https://github.com/tokeo/fundi) package to wire your own AI behind the guarded agent contracts
- Implementing automated deployment pipelines

<br/>
<br/>

**Checkout the example project at [Tokeo Spiral](https://github.com/tokeo/spiral)** and explore the main [Tokeo framework](https://github.com/tokeo/tokeo) for the full picture.

<br/>
<br/>

ramani is built with ❤️ by Tom Freudenberg - Empowering Python Applications

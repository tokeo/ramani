<br/>

<h1 align="center">ramani</h1>

<p align="center">
  <strong>Project blueprints for Tokeo. The templates behind <code>tokeo generate project</code>.</strong>
</p>

<br/>

## 🗺️ What is Ramani?

*Ramani* is Kiswahili for map or blueprint. It ships the ```generate``` templates that the [Tokeo](https://github.com/tokeo/tokeo) CLI uses to scaffold a complete application. It is packaged as its own distribution, separate from the framework.

Ramani carries no framework logic of its own. It is essentially a template payload, with just enough Python to expose the blueprints to Tokeo.

<br/>

## 🛠️ Getting Started

### Adding the templates to Tokeo

```bash
# Install directly from Pypi.org, alongside Tokeo
pip install tokeo-ramani
```

After the install, the ```generate``` templates are available to the ```tokeo``` CLI. No extension to load. No path to register.

### Creating a New Project

Set up a Tokeo project in minutes:

```bash
# Generate a new project (interactive prompts)
tokeo generate project your_app
```

<br/>

## 🌿 Features to enable

The ```project``` blueprint is driven by interactive prompts. The same template produces anything from a minimal CLI up to a full event-driven backend:

- **Dramatiq** background task processing for efficient, decoupled workloads (paired with RabbitMQ)
- **gRPC** service that exposes your tasks and workflows to external callers
- **APScheduler** cron service for timed job execution
- **Automate** Fabric-based local and remote task automation, configured in YAML with CLI overrides
- **smtpd** mail-receiving service that turns SMTP messages into events, with optional auto-generated TLS certificates
- **NiceGUI** web interface to visualize data and interact with your application
- **DiskCache** disk-based caching for frequently accessed data, reducing load times
- **PocketBase** zero-config SQLite backend providing REST API and authentication
- **Vault** keeps credentials encrypted inside your YAML (```!vault:<profile>``` tags) and decrypts them transparently at the leaf, so consumer code never changes and plaintext never lands in the config
- **AI branch** a provider-agnostic AI runtime with typed contracts, profiles and agents as plain configuration, where every tool call passes a guard pipeline (validate, policy, audit) and leaves a full trace. Needs [tokeo-fundi](https://github.com/tokeo/fundi), with optional WASM and Docker sandboxes for tool execution

Answer a feature with *no* and the generated project does not contain it. Neither its code nor its dependencies.

### akili, the train-first micro LLM demo

When you generate a project with the AI feature, you may also add ```akili```. It is a small, teachable language model that plans calendar tool calls:

- **A few hundred thousand parameters, ~2.5 MB.** Byte-level tokenizer, NumPy-only inference in tens of milliseconds, no GPU and no service.
- **Train first, no shipped weights.** ```python -m your_app.core.akili.train``` creates the model on your machine. CPU is fine.
- **The language is data.** Every word and sentence pattern lives in ```AKILI-LEX.yaml```. Teaching the model new language means editing a file and retraining.
- **Grammar-constrained planning.** A byte-level automaton makes malformed plans impossible.
- **Taught, not just documented.** ```AKILI-LLM.md``` explains training, the anatomy of the weights, and constrained decoding.

The ```akili``` module is a self-contained demonstration only. It is not required by the generated application and can be removed without side effects.

<br/>

## 📊 Exploring the Generated Project

Once created, your project exposes each selected feature through its own commands:

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

Every ```project``` blueprint expands into a clean, modular layout:

- ```config/``` - Configuration files for prod, stage, dev and test environments
- ```your_app/core/logic``` - Space for your core application logic
- ```your_app/core/tasks/``` - Implementations of actors, agents, automations, operations, performers etc.
- ```your_app/core/ai/``` - AI providers and plain-function tools behind the guarded contracts (when the AI branch is selected)
- ```your_app/core/akili/``` - The train-first micro LLM lab: model, lexicon (```AKILI-LEX.yaml```), teaching docs (when the AI branch is selected)
- ```your_app/core/grpc/``` - gRPC service definitions and implementations
- ```your_app/core/utils/``` - A place to put your overall tools and helper functions
- ```your_app/controllers/``` - Command-line interface controllers
- ```your_app/pact/ai/``` - AI util-functions necessary for sandboxes (when the AI branch is selected)
- ```your_app/site/``` - Web interface pages and apis
- ```your_app/templates/``` - Templates for rendering content
- ```tests/``` - Test suite to ensure reliability

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

## Tokeo packages

- **Tokeo** is the event-driven CLI framework: the command surface, messaging, scheduling, automation, gRPC, web, vault, and the project generator.
- **Ramani** ships all the project templates, including the AI branch and the akili lab that gets generated into your application.
- **Fundi** (```tokeo-fundi```) is the source-available AI runtime when selected during your setup.
- **Akili** is generated by ```tokeo generate``` from Ramani's template and placed into your application for demonstration purposes under ```your_app/core/akili/``` when selected during your setup.

<br/>

## ⚖️ Licensing

Ramani is published under the Apache License, Version 2.0. The project sources it generates are yours. Use them freely and license them however you like. This scaffold imposes no attribution requirement and no license of its own on your code.

That covers the code you take from here or a generated project. It does not extend to the third-party packages a project installs, those keep their own licenses.

Tokeo's author believes in empowering the community while building a sustainable ecosystem. That's why Tokeo and its extensions use a dual-approach to licensing:

**The Tokeo Core Framework (Apache 2.0)**

Tokeo's author transitioned the core Tokeo framework from its original MIT license to the **Apache 2.0 license**. This switch wasn't primarily about Tokeo itself. It was made to provide *you*, the implementer and the project, with absolute legal certainty. In addition, the Apache 2.0 license includes explicit patent grants and protection, giving your projects a legally safe and rock-solid foundation to build upon.

**The Tokeo Fundi Agent AI Extension (Source-Available License)**

Enabling the AI branch adds ```tokeo-fundi```, the agentic framework that powers the tokeo ai features: agents, tools, governors, sandboxing, audit and more. It is a dependency, not part of these templates, and it is **not** open source but fair source and source available released by the custom **Tokeo-Fundi Source-Available License 1.0**. Please don't let this scare you off! Tokeo's author is deeply committed to keeping software free for the community. If you are a hobbyist, a startup, or a small team, ```tokeo-fundi``` is **free of charge** for you to use in any personal, internal or commercial project.

However, to keep the tokeo project healthy, actively developed, and sustainable, this license introduces a fair-use threshold. Businesses with highly successful commercial operations (across the whole group: more than EUR 2,000,000 in fiscal year global gross revenue excluding VAT, or more than 50 FTEs) are required to purchase a commercial Enterprise License. The license also restricts using its source code as training data for machine-learning systems. Read the complete and authoritative terms in ```LICENSE.md``` of the [tokeo-fundi](https://github.com/tokeo/fundi/) distribution.

From Tokeo's author — I believe this is a fair balance: those who achieve significant economic success using this software should contribute back to the developers making it possible.

**The Tokeo Akili Demonstration LLM (Apache 2.0)**

There is an exception among the generated sources in the ```your_app.core.akili``` module. It is meant as a demonstration and is not intended for delivery. It ships so you can experiment and learn, and it can be removed without side effects.

If you really have reasons to keep ```akili``` in your own project, its files must remain under the Apache License, Version 2.0. Make sure to comply with that license. Keep the file headers and the ```LICENSE.txt``` copy in the ```your_app/core/akili``` directory.

To put it another way: the purpose of ```akili``` is lab work. Use it to understand LLMs, to learn how to build one yourself, and how to equip it with tools. It is there to give you the idea and the know-how to reach your own goals efficiently.

<br/>
<br/>

**Checkout the example project at [Tokeo Spiral](https://github.com/tokeo/spiral)** and explore the main [Tokeo framework](https://github.com/tokeo/tokeo) for the full picture.

<br/>
<br/>

ramani is built with ❤️ by Tom Freudenberg - Empowering Python Applications

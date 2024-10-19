# <a href="https://github.com/dmarcoux/customer-chat">dmarcoux/customer-chat</a>

Imagine a situation where you need to implement a chat software for our
customer service to interact with our customers.

How would the quick win solution look like and how would the state-of-the-art
solution look like?

Implement a simple solution for a chat that enables customers to send
messages to customer service.

Talking points / topics to be considered:

- Which objects / classes would you create?
- How do they interact?
- How does the frontend interact with your classes?
- Which enhancements come to your mind when talking about chat software solutions?

## Python Development Environment with Nix Flakes

Reproducible development environment for Python projects which relies on
[Nix](https://github.com/NixOS/nix) [Flakes](https://nixos.wiki/wiki/Flakes),
a purely functional and cross-platform package manager.

**Start development environment:**

```bash
nix develop
```

**Create a virtual environment:**

```bash
python -m venv venv
```

**Activate the virtual environment:**

```bash
source venv/bin/activate
```

**Deactivate the virtual environment:**

```bash
deactivate
```

**Freeze dependencies:**

```bash
pip freeze > requirements.txt
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

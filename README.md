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

## Quick Win Solution

### Architecture

- Monolith application built with Django
- SQLite as a database
- Models / Entity Relationship Diagram
    <details>
      <summary>Click to see the entity relationship diagram</summary>

    #### Entity Relationship Diagram

    ```mermaid
        erDiagram
            UserCustomer["User (Customer)"]
            UserCustomerAgent["User (Customer Agent)"]

            UserCustomer ||--o{ SupportCase : opens
            UserCustomer ||--o{ Message : sends
            UserCustomerAgent ||--o{ Message : sends
            SupportCase ||--o{ Message : has
    ```
    </details>

- Features
    - Messages aren't in real-time, the browser window must be refreshed to see
    messages from other users.
    - Customers can open multiple support cases
    - Customers can send messages in the support cases they created
    - Customer agents can send messages in all support cases, but they cannot
    open support cases.
    - For simplicity purposes, users cannot register themselves. They must be
    created by the superuser in the Django admin.

### Limitations

- Scalability
    - Every feature is part of the same application. What if one part of the application would benefit from having more resources?
    - SQLite scales well vertically, but it is hard to scale horizontally since a SQLite database is just a file on disk.
- Extensibility
    - Monolith application is simple to develop, but it's quite rigid.
    - User as the single model for customers and customer agents is fine at a small scale, but if this application grows, it would be better to
      split this model into 2 models (Customer, Customer Agent). It would be easier to understand what is specific to customers and customer agents.
      Right now, we tell customer and customer agents apart from each other via the `is_staff` field in the `User` model.
    - It's possible for customers to open multiple support cases, but the support cases don't have any status (like "on going", "completed", etc...)
- Security / Data Privacy
    - Customer agents have access to all support cases. It would be better to assign one customer agent per support case
      to limit data access. In general, it's a questionable and risky practice to give everyone access
      to everything.
    - With GitHub, we are notified whenever one of the project's dependency has
      a security vulnerability. When this happens, we need to update this
      dependency as soon as possible, but it could be somewhat difficult if the
      new version brings a lot of changes. The longer we wait before updating our
      dependencies, the harder it potentially gets. This is why we should use a
      tool like Dependabot to automate dependency updates.
- Single point of failure
    - Since the application is hard to scale horizontally, thus most surely running on a single server, it has
      a single point of failure. If the server goes down (hardware failure, power outage, etc...), the application
      isn't usable anymore. The solution would be to address the scalability limitations. We are then able to
      remove this single point of failure by scaling horizontally with multiple application instances behind a
      load balancer, a database cluster with multiple read/write nodes
- Interactivity
    - Chat is not in real-time. Relying on an implementation based on WebSockets would fix this.
- Automation
    - It's possible that different customers ask the same questions. Whenever
      this happens, a customer agent must take their time to still reply what has
      already been said to a previous customer. It could be perhaps automated with
      AI.

## State-Of-The-Art Solution

It all depends on what we want to achieve and our needs. If we start from the
"Quick Win" solution, then addressing its limitations would definitely take us
to a pretty good state.

## Development Environment

The development environment is based on [devcontainer](https://containers.dev/)
which relies on [Docker](https://www.docker.com/) and
[Docker-Compose](https://docs.docker.com/compose/). devcontainer is [supported
in various IDEs/editors](https://containers.dev/supporting), in addition to
having a [CLI](https://github.com/devcontainers/cli).

The following versions were tested:
- Docker: 26.1.5
- Docker-Compose: 2.27.0
- devcontainer CLI: 0.71.0
- VS Code editor (1.93.1) with Dev Containers extension (v0.388.0)

Refer to the [Makefile](./Makefile) to see various commands, like starting the
development environment or formatting the code.

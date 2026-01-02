# Production-Grade Logging Patterns for AI Agents

**Category:** #python #ai-native #observability
**Tags:** #solutions-engineering #debugging #best-practices

### The Problem
When building AI agents or prepping for a POV, you live in two states: **Deep Debugging** and **Customer Demoing**.

* **Debugging State:** You need to see *everything*—the exact token counts, stop reasons, raw content blocks, and deeply nested metadata returned by the LLM API.
* **Demo State:** You want a clean console showing only the final output.

Using `print(response)` ruins demos with massive text blobs. Using a basic logger like `logger.info(response)` is often useless, resulting in unhelpful output like: `<anthropic.types.message.Message object at 0x10a42b...>` instead of the actual data. Furthermore, trying to serialize these complex SDK response objects directly often crashes your app because they contain non-standard types (like `datetime` or Pydantic models).

### The Solution
Combine Python's standard `logging` with a robust `json.dumps` pattern specifically designed to handle complex AI SDK objects without crashing.

This approach gives you searchable, structured logs during development that stay completely silent during demos.

```python
import logging
import json

# === SETUP (At application startup) ===
# 1. Configure global logging. 
# During dev, use level=logging.DEBUG. For demos, switch to logging.INFO.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 2. Name your logger based on the component (e.g., "ClaudeAgent", "VectorDB")
logger = logging.getLogger("AI-Workflow-Engine")


# === THE PATTERN (In your agent loop) ===
# Assume 'response' is a complex, nested object from an AI SDK (OpenAI/Anthropic)

logger.info(f"Received response from model: {response.model}")

# Use "Lazy Interpolation" for heavy debug logs
logger.debug(
    "Full serialized response state:\n%s", 
    json.dumps(response.__dict__, indent=2, default=str)
)

```

### Why this works for SEs:

1. **The `default=str` Lifesaver:** AI SDK responses often contain types JSON can't handle natively. Adding `default=str` tells Python: "If you don't know how to serialize an object, convert it to its string representation instead of crashing."
2. **Lazy Interpolation for Performance:** Notice we use `logger.debug("msg: %s", expensive_call())` instead of an f-string. This is crucial. If your log level is set to `INFO`, Python *skips* the expensive `json.dumps()` operation entirely, saving precious milliseconds in tight agent loops.
3. **Demo Hygiene:** When it's time to present, change one line of config (`level=logging.INFO`), and your console is instantly clean for the client.

---

> [!TIP]
> **Pro Tip: The Observability Hook**
> Because you are now logging structured JSON strings, if you pipe these logs into a tool like **Datadog** or **Elastic**, the logs become instantly searchable. You can filter by specific field existence like `content.stop_reason: "max_tokens"` across thousands of agent runs.

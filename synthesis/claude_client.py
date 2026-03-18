import logging
import anthropic

logger = logging.getLogger(__name__)

_FALLBACK = (
    "# Morning Research Brief\n\n"
    "> **Error**: Claude API call failed. Check logs for details. "
    "Raw research data was collected — re-run to retry synthesis.\n"
)


def generate_brief(prompt: str, config: dict) -> str:
    model_cfg = config.get("model", {})
    model = model_cfg.get("name", "claude-sonnet-4-6")
    max_tokens = model_cfg.get("max_tokens", 4096)
    temperature = model_cfg.get("temperature", 0.3)

    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
    except anthropic.APIError as e:
        logger.error("Anthropic API error: %s", e)
        return _FALLBACK
    except Exception as e:
        logger.error("Unexpected error calling Claude: %s", e)
        return _FALLBACK

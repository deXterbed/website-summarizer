"""
Prompt building module for constructing messages for AI models.
"""


class PromptBuilder:
    """Builds prompts for AI models."""

    SYSTEM_PROMPT = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

    @staticmethod
    def build_messages(website):
        """Build messages for AI model interaction."""
        user_prompt = f"You are looking at a website titled {website.title}"
        user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
        user_prompt += website.text

        return [
            {"role": "system", "content": PromptBuilder.SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

    @staticmethod
    def build_custom_messages(system_prompt, user_prompt):
        """Build custom messages with specified prompts."""
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    @staticmethod
    def get_default_system_prompt():
        """Get the default system prompt."""
        return PromptBuilder.SYSTEM_PROMPT
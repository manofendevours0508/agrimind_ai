class IntentClassifier:
    """Identifies the type of task requested by a farmer."""

    def classify(self, message: str) -> str:
        """Classify a farmer's message into a supported intent."""

        if not isinstance(message, str) or not message.strip():
            raise ValueError("Message must be a non-empty string.")

        text = message.lower()

        if any(word in text for word in ["dataset", "csv", "analyse data", "analyze data"]):
            return "data_analysis"

        if any(word in text for word in ["research", "studies", "scientific papers"]):
            return "research"

        return "general_question"

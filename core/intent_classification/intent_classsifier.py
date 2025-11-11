from sentence_transformers import SentenceTransformer, util
import torch


class IntentClassifier:
    def __init__(self, intent_examples: dict[str, list[str]], model_name: str = "all-MiniLM-L6-v2", threshold: float = 0.45):
        self.model = SentenceTransformer(model_name)
        self.intent_examples = intent_examples
        self.threshold = threshold
        self.index = []  # list of (intent_label, example_embedding)

        self._build_index()

    def _build_index(self):
        for label, examples in self.intent_examples.items():
            embeddings = self.model.encode(examples, convert_to_tensor=True)
            for emb in embeddings:
                self.index.append((label, emb))

    def predict(self, user_input: str):
        input_emb = self.model.encode(user_input, convert_to_tensor=True)
        best_score = -1
        best_label = None

        for label, emb in self.index:
            score = util.cos_sim(input_emb, emb).item()
            if score > best_score:
                best_score = score
                best_label = label

        if best_score >= self.threshold:
            return best_label, best_score
        return None, best_score  # Rejection path


intent_examples = {
    "vibration_analysis": [
        "Check machine vibrations",
        "Run vibration analysis",
        "Is it vibrating too much?",
    ],
    "temperature_monitoring": [
        "What's the machine temperature?",
        "Check heat levels",
        "Is it overheating?",
    ],
    "remaining_useful_life": [
        "Estimate machine lifespan",
        "How long will it last?",
        "Give me the RUL forecast",
    ],
}

classifier = IntentClassifier(intent_examples)

test_inputs = [
    "What's the current heat level on forklift 2?",
    "Give me logs from last week",
    "Why is the engine noisy?",
    "What's the price of Bitcoin?"  # OOS
]

for inp in test_inputs:
    intent, score = classifier.predict(inp)
    print(f"Input: {inp}")
    print(f" → Intent: {intent} (Score: {score:.3f})\n")


def intent_analyser(user_intent, machine_id, sensor, window):
    classifier = IntentClassifier(intent_examples)  # pass the examples
    predicted_label, score = classifier.predict(user_intent)  # unpack tuple
    intent_specs = {
        "intent": predicted_label,
        "score": score,
        "machine_id": machine_id,
        "params": {
            "sensor": sensor,
            "window": window
        }
    }
    return intent_specs


# Example usage
example_usage = intent_analyser(test_inputs[0], 12, "Sensor_4", 12)
print(example_usage)

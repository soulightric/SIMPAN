from backend.knowledge.rules import RULES

class RuleEngine:
    def evaluate(self, finance):
        hasil = []
        for rule in RULES:
            if rule["condition"](finance):
                hasil.append({
                    "rule_id": rule["id"],
                    "rule": rule["name"],
                    "message": rule["message"]
                })
        return hasil
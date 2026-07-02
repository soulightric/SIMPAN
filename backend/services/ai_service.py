from backend.services.finance_service import calculate_finance
from backend.services.rule_engine import RuleEngine
from backend.services.planning_service import PlanningService
from backend.services.recommendation_service import RecommendationService

class AIService:
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.planning = PlanningService()
        self.recommendation = RecommendationService()
    def analyze(self, data):
        finance = calculate_finance(data)
        rules = self.rule_engine.evaluate(finance)
        plan = self.planning.create_plan(finance)
        rekomendasi = self.recommendation.generate(
            finance,
            rules,
            plan
        )
        return {
            "finance": finance,
            "rules": rules,
            "planning": plan,
            "recommendation": rekomendasi
        }
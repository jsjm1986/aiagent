"""演化引擎 - 学习和策略更新"""
from datetime import datetime
import json
import os

class StrategyUpdate:
    def __init__(self, parameter: str, old_value: float, new_value: float, reason: str):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.timestamp = datetime.now()
        self.parameter = parameter
        self.old_value = old_value
        self.new_value = new_value
        self.reason = reason

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'parameter': self.parameter,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'reason': self.reason
        }

class EvolutionEngine:
    def __init__(self, value_engine, data_dir: str = "./data"):
        self.value_engine = value_engine
        self.data_dir = data_dir
        self.history_file = os.path.join(data_dir, "evolution_history.json")
        self.strategy_history = self._load_history()
        self.value_outcomes = []

    def _load_history(self) -> list:
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _save_history(self):
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.strategy_history, f, ensure_ascii=False, indent=2)

    def evolve_after_action(self, action: dict, result: dict):
        """每次行动后的演化"""
        # 1. 记录价值结果
        self._record_value_outcome(action, result)

        # 2. 更新策略
        self._update_strategy(action, result)

    def _record_value_outcome(self, action: dict, result: dict):
        """记录价值结果"""
        outcome = {
            'action_type': action.get('type'),
            'predicted_value': action.get('score', 0),
            'actual_value': result.get('actual_value', 0),
            'timestamp': datetime.now().isoformat()
        }
        self.value_outcomes.append(outcome)

    def _update_strategy(self, action: dict, result: dict):
        """更新策略参数"""
        actual_value = result.get('actual_value', 0)
        predicted_value = action.get('score', 0)

        # 如果实际价值远高于预测，提升该维度权重
        if actual_value > predicted_value + 0.2:
            self._adjust_dimension_weight(action, +0.05, "实际价值高于预测")
        # 如果实际价值远低于预测，降低权重
        elif actual_value < predicted_value - 0.2:
            self._adjust_dimension_weight(action, -0.05, "实际价值低于预测")

    def _adjust_dimension_weight(self, action: dict, delta: float, reason: str):
        """调整维度权重"""
        # 简化版：调整主要维度
        dimension = 'value'
        current = self.value_engine.DIMENSIONS.get(dimension, 0.25)
        new_value = max(0.1, min(0.4, current + delta))

        if abs(new_value - current) > 0.01:
            update = StrategyUpdate(
                parameter=f'dimension.{dimension}',
                old_value=current,
                new_value=new_value,
                reason=reason
            )
            self.strategy_history.append(update.to_dict())
            self._save_history()

    def get_timeline(self, days: int = 7) -> list:
        """获取演化时间线"""
        return self.strategy_history[-50:]  # 最近50条

    def get_insights(self) -> list:
        """获取学习洞察"""
        insights = []

        if len(self.value_outcomes) > 10:
            # 计算预测准确度
            errors = [abs(o['predicted_value'] - o['actual_value'])
                     for o in self.value_outcomes[-10:]]
            avg_error = sum(errors) / len(errors)

            if avg_error > 0.3:
                insights.append({
                    'type': 'prediction_accuracy',
                    'message': f'价值预测误差较大 ({avg_error:.2f})，需要改进',
                    'priority': 'high'
                })

        return insights

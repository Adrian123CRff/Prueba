# weather_manager.py
import random
import time

MULTIPLIERS = {
    "clear": 1.00,
    "clouds": 0.98,
    "rain_light": 0.90,
    "rain": 0.85,
    "storm": 0.75,
    "fog": 0.88,
    "wind": 0.92,
    "heat": 0.90,
    "cold": 0.92,
}

class WeatherManager:
    def __init__(self, bursts=None, transition_matrix=None):
        """
        bursts: optional list of bursts fetched from API (each with duration_sec, condition, intensity)
        transition_matrix: dict mapping current -> list of (next_cond, prob)
        """
        self.bursts = bursts or []
        self.transition_matrix = transition_matrix or {}
        self.current = None
        self.intensity = 0.0
        self.timer = 0.0

        # interpolation
        self.transitioning = False
        self.old_multiplier = 1.0
        self.target_multiplier = 1.0
        self.transition_elapsed = 0.0
        self.transition_duration = 0.0

        if self.bursts:
            b = self.bursts[0]
            self.current = b["condition"]
            self.intensity = b.get("intensity", 0.0)
            self.timer = b.get("duration_sec", 60)

    def _sample_next_condition(self, current):
        if current in self.transition_matrix:
            choices, probs = zip(*self.transition_matrix[current])
            return random.choices(choices, probs)[0]
        # fallback aleatorio
        return random.choice(list(MULTIPLIERS.keys()))

    def start_transition_to(self, next_cond):
        self.transitioning = True
        self.old_multiplier = MULTIPLIERS.get(self.current, 1.0)
        self.target_multiplier = MULTIPLIERS.get(next_cond, 1.0)
        self.transition_elapsed = 0.0
        self.transition_duration = random.uniform(3.0, 5.0)
        self.next_condition = next_cond

    def update(self, dt):
        """dt: segundos reales (o tiempo de juego). Devuelve el multiplicador Mclima actual."""
        if self.transitioning:
            self.transition_elapsed += dt
            t = min(1.0, self.transition_elapsed / self.transition_duration)
            # interpolación lineal
            cur = self.old_multiplier + (self.target_multiplier - self.old_multiplier) * t
            if t >= 1.0:
                self.transitioning = False
                self.current = self.next_condition
                # reset timer tomando un valor razonable
                self.timer = random.uniform(45, 60)
            return cur
        # no en transición
        self.timer -= dt
        if self.timer <= 0:
            # elegir siguiente usando Markov
            next_cond = self._sample_next_condition(self.current)
            # intensidad aleatoria si lo deseas:
            self.intensity = random.random()
            self.start_transition_to(next_cond)
        return MULTIPLIERS.get(self.current, 1.0)

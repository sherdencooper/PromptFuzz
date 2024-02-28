import re


class Predictor:
    def __init__(self, path):
        self.path = path

    def predict(self, sequences):
        raise NotImplementedError("Predictor must implement predict method.")

class MatchPredictor(Predictor):
    def __init__(self, match_target):
        self.match_target = match_target

    def predict(self, sequences):
        results = []
        for sequence in sequences:
            # check if the sequence contains the match target
            results.append(int(self.match_target in sequence))
        return results

class AccessGrantedPredictor(Predictor):
    def __init__(self):
        pass
    def predict(self, sequences):
        ACCESS_GRANTED_REGEX = re.compile(r"^\W*access granted\W*$", re.IGNORECASE)
        # check each sequence
        results = []
        for sequence in sequences:
            # check if the sequence matches the access granted regex
            results.append(int(bool(ACCESS_GRANTED_REGEX.match(sequence))))
        return results
        
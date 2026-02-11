from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

from .nlp_config import NLP_CONFIGURATION


def load_nltk_data():
    import re
    import nltk
    from importlib.metadata import version

    nltk_version = version("nltk")
    nltk_breaking_version = "3.8.2" # The version where the dataset changed

    def parse_major_minor_patch(version: str):
        """Extract the major, minor, and patch version numbers from a version string."""
        match = re.match(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)(?:\.(0|[1-9]\d*))?(?:[-+][0-9A-Za-z-.]+)?$", version)
        if match:
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3)) if match.group(3) else 0  # Default to 0 if patch is not provided
            return major, minor, patch
        else:
            raise ValueError(f"Invalid semantic version: '{version}'")

    def install_pre_382_dataset():
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")
        
    def install_post_382_dataset():
        try:
            nltk.data.find("tokenizers/punkt_tab")
        except LookupError:
            nltk.download("punkt_tab")

    try:
        target_major, target_minor, target_patch = parse_major_minor_patch(nltk_breaking_version)
        major, minor, patch = parse_major_minor_patch(nltk_version)

        if (major, minor, patch) >= (target_major, target_minor, target_patch):
            install_post_382_dataset()
        elif (major, minor, patch) < (target_major, target_minor, target_patch):
            install_pre_382_dataset()
    except Exception:
        print((
            "Error auto-installing nltk dataset, please install manually.\n"
            "This can be done with:\n",
            "Version < 3.8.2:\n import nltk\n nltk.download('punkt')",
            "Version >= 3.8.2:\n import nltk\n nltk.download('punkt_tab')"
        ))


load_nltk_data()

provider = NlpEngineProvider(nlp_configuration=NLP_CONFIGURATION)
nlp_engine = provider.create_engine()

# Download models
AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["fr"])
AnonymizerEngine()

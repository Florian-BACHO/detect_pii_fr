import pytest
from validator.main import DetectPII
from guardrails import Guard

# Setup Guard with DetectPII validator
guard = Guard().use(
    DetectPII,
    ["EMAIL_ADDRESS", "PHONE_NUMBER"],
    "exception",
    use_local=True,
)


# Test passing response (no PII)
def test_pii_pass():
    response = guard.validate("Mon nom est Paul et j'adore la randonnée!")
    assert response.validation_passed is True


# Test failing response (contains PII)
def test_pii_fail():
    with pytest.raises(Exception) as e:
        guard.validate(
            "Mon addresse email est demo@lol.com, et mon numéro de téléphone est 1234567890"
        )

    print(e)
    assert "Validation failed for field with errors:" in str(e.value)


# Setup Guard with DetectPII validator
guard_name = Guard().use(
    DetectPII,
    ["PERSON"],
    "exception",
    use_local=True,
)


# Test failing response (contains no name)
def test_pii_no_name():
    response = guard_name.validate("Je suis un humain et j'adore la randonnée!")
    assert response.validation_passed is True


# Test passing response (contains a name)
def test_pii_fail_name():
    with pytest.raises(Exception) as e:
        guard_name.validate("Mon nom est Paul Richard et j'adore la randonnée!")

    print(e)
    assert "Validation failed for field with errors:" in str(e.value)

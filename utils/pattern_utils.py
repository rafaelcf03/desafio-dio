# function to remove special characters from ssn (cpf)
def clean_ssn(ssn: str) -> str:
    return ssn.replace("-", "").replace(".", "").strip()


def is_valid_ssn(ssn: str) -> bool:
    parsed_ssn = clean_ssn(ssn)
    return len(parsed_ssn) == 11 and parsed_ssn.isdigit()

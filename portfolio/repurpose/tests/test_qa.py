from repurpose import qa

SOURCE = (
    "Average wait fell to 51 minutes, a reduction of 46%. "
    "Missed appointments fell from 8% to 3%. Revenue reached $1.2M."
)


def test_grounded_numbers_pass():
    draft = "Wait times dropped 46% to 51 minutes."
    assert qa.check_claims_grounded(draft, SOURCE) == []


def test_fabricated_number_fails():
    draft = "Wait times dropped 73% across every site."
    findings = qa.check_claims_grounded(draft, SOURCE)
    assert [f.check for f in findings] == ["claims_grounded"]
    assert "73%" in findings[0].message


def test_number_formatting_is_normalised():
    assert qa.check_claims_grounded("We hit $1,200,000 in revenue.", "Revenue: 1200000") == []


def test_currency_claim_is_matched_against_source():
    assert qa.check_claims_grounded("Revenue reached $1.2M.", SOURCE) == []


def test_each_fabricated_number_reported_once():
    draft = "Up 73%. Still up 73%. And 73% again."
    assert len(qa.check_claims_grounded(draft, SOURCE)) == 1


def test_banned_phrase_detected_case_insensitively():
    findings = qa.check_banned_phrases("It's Important To Note this.", ["it's important to note"])
    assert len(findings) == 1
    assert findings[0].severity == "fail"


def test_length_bounds():
    assert qa.check_length("abc", 10, None)[0].check == "length"
    assert qa.check_length("abc" * 100, None, 10)[0].check == "length"
    assert qa.check_length("abcdefghij", 5, 20) == []


def test_required_elements():
    assert qa.check_required("see northwind.example/report", ["northwind.example/report"]) == []
    assert len(qa.check_required("no link here", ["northwind.example/report"])) == 1


def test_readability_warns_not_fails():
    dense = (
        "The implementation of comprehensive organisational restructuring "
        "necessitates considerable administrative reconfiguration throughout "
        "the entirety of the distribution infrastructure."
    )
    findings = qa.check_readability(dense, max_grade=8)
    assert findings and findings[0].severity == "warn"


def test_readability_skipped_when_unset():
    assert qa.check_readability("anything at all", None) == []


def test_cross_channel_duplication_flags_shared_runs():
    shared = "we moved from fixed hourly appointment blocks to twenty minute windows"
    findings = qa.check_cross_channel_duplication(
        {"linkedin": shared, "newsletter": shared, "meta": "unrelated text entirely"}
    )
    assert findings and findings[0].check == "duplication"


def test_cross_channel_duplication_allows_distinct_drafts():
    assert (
        qa.check_cross_channel_duplication(
            {"a": "wait times fell sharply at every site", "b": "carriers rescheduled themselves"}
        )
        == []
    )


def test_review_aggregates_and_gates():
    rules = {"banned_phrases": ["delve"], "min_chars": 5, "required": ["link"]}
    card = qa.review("post", "Let's delve into 99% growth", SOURCE, rules)
    assert not card.passed
    assert {f.check for f in card.failures} == {"banned_phrases", "claims_grounded", "required"}

import types
from unittest.mock import patch
import pytest

import src.news_classification.news_scraper as news_scraper

def test_shorten_url_success():
    with patch("src.news_classification.news_scraper.pyshorteners.Shortener") as MockShortener:
        mock_instance = MockShortener.return_value

        mock_instance.tinyurl.short.return_value = "https://tinyurl.com/"

        result = news_scraper.shorten_url("https://longlonglongurl.com/")
        assert result == "https://tinyurl.com/"
        mock_instance.tinyurl.short.assert_called_once_with("https://longlonglongurl.com/")

def test_shorten_url_exception():
    with patch("src.news_classification.news_scraper.pyshorteners.Shortener") as MockShortener:
        mock_instance = MockShortener.return_value
        mock_instance.tinyurl.short.side_effect = Exception("service down")

        url = "http://long-url.example/page"
        result = news_scraper.shorten_url(url)
        assert result == url

def test_parse_date_ok():
    s = "Fri, 19 Sep 2025 12:34:56 GMT"
    assert news_scraper.parse_date(s) == "19/09/2025"

def test_parse_date_bad_format():
    with pytest.raises(ValueError):
        news_scraper.parse_date("2025-09-19")  

def test_clean_title():
    title = "Important discovery - The Science Times"
    assert news_scraper.clean_title(title) == "Important discovery"

def make_entry(title, link, published, source_title, source_href):
    return types.SimpleNamespace(
        title=title,
        link=link,
        published=published,
        source={"title": source_title, "href": source_href}
    )

@patch("src.news_classification.news_scraper.pyshorteners.Shortener")
@patch("src.news_classification.news_scraper.feedparser.parse")
def test_fetch_news_parses_entries_and_shortens_links(mock_parse, MockShortener):
    entries = [
        make_entry("T1 - Source A", "http://example.com/a", "Fri, 19 Sep 2025 01:02:03 GMT", "A", "https://a.example"),
        make_entry("T2 - Source B", "http://example.com/b", "Fri, 19 Sep 2025 02:03:04 GMT", "B", "https://b.example"),
    ]
    fake_feed = types.SimpleNamespace(entries=entries)
    mock_parse.return_value = fake_feed

    mock_short_instance = MockShortener.return_value
    mock_short_instance.tinyurl.short.side_effect = lambda x: "short:" + x

    df = news_scraper.fetch_news("lawsuit", max_articles=1)

    assert len(df) == 1
    row = df.iloc[0].to_dict()
    assert row["Headline"] == "T1"
    assert row["URL"] == "short:http://example.com/a"
    assert row["Published"] == "19/09/2025"
    assert row["Source"] == "A"
    assert row["Source URL"] == "https://a.example"

    expected_url_fragment = "q=lawsuit"
    called_url = mock_parse.call_args[0][0]
    assert expected_url_fragment in called_url

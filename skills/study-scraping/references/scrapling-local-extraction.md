# Scrapling Local Extraction

Use Scrapling for allowed public pages when targeted local extraction, JavaScript rendering, stable selectors, or a repeatable spider is needed. Do not use it to bypass authentication, paywalls, robots/terms restrictions, rate limits, or anti-bot challenges.

## Runtime Check

```bash
command -v scrapling
python3 -c 'import scrapling; print(scrapling.__version__)'
```

Install or upgrade dependencies only when the user has approved environment changes.

## Allowed CLI Flow

```bash
scrapling extract get "https://example.com/article" /tmp/page.md --ai-targeted
scrapling extract get "https://example.com" /tmp/items.md --ai-targeted --css-selector "article"
scrapling extract fetch "https://example.com/public-app" /tmp/page.md --ai-targeted --network-idle
scrapling extract fetch "https://example.com/public-app" /tmp/page.md --ai-targeted --wait-selector ".content"
```

Escalate from static `get` to JavaScript `fetch` only when the same public page requires rendering. If either route receives 401/403/429, login state, challenge pages, or terms restrictions, stop and record the blocker.

Output extension controls format:

- `.md`: readable article/research extraction.
- `.txt`: clean text.
- `.html`: structure-preserving parse input.
- `.json`: structured output when supported.

Use `/tmp` for one-off extraction and remove temporary files after inspection unless preservation was requested.

## Python And Spiders

Use `Fetcher` for allowed static pages and `DynamicFetcher` for public JavaScript pages. Use sessions only for public state that does not require user authentication.

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get("https://quotes.toscrape.com/")
quotes = page.css(".quote .text::text").getall()
```

Use a spider only for bounded pagination or repeatable exports:

```python
from scrapling.spiders import Spider, Response

class StudySpider(Spider):
    name = "study_spider"
    start_urls = ["https://example.com/public-index"]

    async def parse(self, response: Response):
        for article in response.css("article"):
            yield {
                "title": article.css("h2::text").get(),
                "url": article.css("a::attr(href)").get(),
            }
```

Set explicit item/page limits and checkpoint output. Keep raw snapshots separate from normalized `research.v1` cards.

## Routing

1. Static extraction for known public pages.
2. JavaScript rendering for the same allowed page when required.
3. Bounded spider for repeatable public pagination.
4. Firecrawl when discovery is broader than extraction.
5. Stop and report the coverage gap when access boundaries appear.

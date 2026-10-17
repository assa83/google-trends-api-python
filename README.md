# Google Trends API in Python – working example

Get Google Trends interest over time, interest by region, related and rising queries and Trending Now searches as clean JSON from Python, JavaScript or n8n – a reliable pytrends alternative.

Powered by the [google-trends-scraper](https://apify.com/lagenuina_agency/google-trends-scraper) actor on Apify. No browser, no cookies, no account on Google.

## Example output (real result, shortened)

```json
{
  "type": "keyword",
  "searchTerm": "chatgpt",
  "geo": "IT",
  "timeRange": "today 12-m",
  "data_granularity": "week",
  "timeline": [
    {
      "date": "2026-10-11T00:00:00.000Z",
      "value": 88,
      "isPartial": true
    }
  ],
  "relatedQueries_top": [
    {
      "query": "chatgpt gratis",
      "value": 100,
      "formattedValue": "100"
    }
  ],
  "relatedQueries_rising": [
    {
      "query": "chatgpt atlas",
      "value": 4250,
      "formattedValue": "+4,250%"
    }
  ],
  "isPartial": false,
  "trendsUrl": "https://trends.google.com/trends/explore?q=chatgpt&date=today+12-m&hl=en-US&geo=IT"
}
```

## Quickstart (3 steps)

1. Create a free Apify account and copy your API token from [Settings → Integrations](https://console.apify.com/settings/integrations).
2. Put it in an environment variable (never in code): `export APIFY_TOKEN=your_token`
3. Run the example:

```bash
pip install -r python/requirements.txt
python python/example.py "chatgpt" "gemini" --geo US
```

JavaScript: `cd js && npm install && node example.mjs`

## Examples

**Python** (`pip install "apify-client<2"`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("lagenuina_agency/google-trends-scraper").call(run_input={
  "searchTerms": [
    "chatgpt",
    "gemini"
  ],
  "geo": "US",
  "timeRange": "today 12-m"
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

**JavaScript / Node.js** (`npm install apify-client`)

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('lagenuina_agency/google-trends-scraper').call({"searchTerms": ["chatgpt", "gemini"], "geo": "US", "timeRange": "today 12-m"});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

**cURL / any language** – one HTTP call, results in the response:

```bash
curl -X POST "https://api.apify.com/v2/acts/lagenuina_agency~google-trends-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mode": "trending", "trendingSearchesCountry": "US", "trendingSearchesTimeframe": "24"}'
```

All input fields are documented on the [actor page](https://apify.com/lagenuina_agency/google-trends-scraper) (Input tab).

## Use case: Weekly Google Trends export to CSV / Google Sheets

`python/example.py` pulls the last 90 days of interest for your keywords and writes one row per keyword and week (`trends_<date>.csv`) plus the rising queries (`rising_<date>.csv`). Import the CSV in Google Sheets, or let the n8n workflow append the rows to a sheet every Monday.

## n8n workflow

[`n8n/workflow.json`](n8n/workflow.json): every Monday 08:00 → run the actor → flatten `timeline` (one row per keyword and week) → append to Google Sheets.

1. In n8n: **Workflows → Import from File** and pick `n8n/workflow.json`.
2. Create a **Header Auth** credential named `Apify API token` with name `Authorization` and value `Bearer <your token>`, and select it in the *Run Apify actor* node.
3. Edit the JSON body (your keywords/targets), set your Google Sheet ID and activate.

The `run-sync-get-dataset-items` endpoint waits up to 300 s; for bigger runs use `/runs` plus a webhook.

## Use with AI agents (MCP)

Give Claude, ChatGPT, Cursor or any MCP client this actor as a tool:

```
https://mcp.apify.com/?actors=lagenuina_agency/google-trends-scraper
```

Example config (Claude Desktop, Cursor, VS Code):

```json
{
  "mcpServers": {
    "google-trends-scraper": {
      "url": "https://mcp.apify.com/?actors=lagenuina_agency/google-trends-scraper"
    }
  }
}
```

Sign in with Apify OAuth when asked, or send `Authorization: Bearer <APIFY_TOKEN>`.

## Pricing

From $2.40 per 1,000 results on the Apify Free plan down to $0.24 on Gold and above (one keyword with all its data = one result), platform usage included, no start fee, pay only for results – see [lagenuina_agency/google-trends-scraper](https://apify.com/lagenuina_agency/google-trends-scraper).

## Disclaimer

Independent, not affiliated with Google (not endorsed by Google LLC). It reads only publicly available data. Use it in line with the applicable terms and laws.

## License

[MIT](LICENSE) © Quelli di Carne Genuina

// Google Trends: interest over time + rising queries for a few keywords.
// Usage: node example.mjs chatgpt gemini
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set APIFY_TOKEN first: https://console.apify.com/settings/integrations');
    process.exit(1);
}

const terms = process.argv.slice(2).length ? process.argv.slice(2) : ['chatgpt', 'gemini'];
const client = new ApifyClient({ token });
const run = await client.actor('lagenuina_agency/google-trends-scraper').call({
    searchTerms: terms,
    geo: 'US',
    timeRange: 'today 3-m',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const it of items) {
    const last = it.timeline?.at(-1);
    console.log(`${it.searchTerm}: latest ${last?.value} (${last?.date?.slice(0, 10)})`);
    for (const q of it.relatedQueries_rising ?? []) console.log(`  rising: ${q.query} ${q.formattedValue}`);
}

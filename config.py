config_keys = {
  'api_key': '229d6a98940b520f310d75e2e7ca402d',
}

config_urls = {
  'sports_url': 'https://api.the-odds-api.com/v3/sports/?apiKey=' + config_keys['api_key'],
  'ncaa_fb_spreads_url': 'https://api.the-odds-api.com/v3/odds/?apiKey=' + config_keys['api_key'] + '&sport=americanfootball_ncaaf&region=us&mkt=spreads',
  'ncaa_fb_totals_url': 'https://api.the-odds-api.com/v3/odds/?apiKey=' + config_keys['api_key'] + '&sport=americanfootball_ncaaf&region=us&mkt=totals',
  'ncaa_fb_h2h_url': 'https://api.the-odds-api.com/v3/odds/?apiKey=' + config_keys['api_key'] + '&sport=americanfootball_ncaaf&region=us&mkt=h2h'
}
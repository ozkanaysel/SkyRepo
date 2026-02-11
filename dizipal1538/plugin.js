Here is the `plugin.js` code for the given site:

globalThis.getManifest = () => ({
  id: 'dizipal1538',
  name: 'DiziPal',
  version: '1.0',
  baseUrl: 'https://dizipal1538.com/'
});

getHome = (cb) => {
  const homeElements = document.querySelectorAll('.main-content');
  cb({
    Latest: homeElements[0],
    Trending: homeElements[1]
  });
};

search = (query, cb) => {
  // Simulate search on the site
  const searchInput = document.querySelector('#search-input');
  searchInput.value = query;
  const searchButton = document.querySelector('#search-button');
  searchButton.click();
  setTimeout(() => {
    const searchResults = document.querySelectorAll('.search-result');
    cb(searchResults);
  }, 500);
};

load = (url, cb) => {
  // Load film details using REGEX
  const regex = /<h2>([^<]+)<\/h2><img src="([^"]+)">.*?(\w+<\/p>)/g;
  const html = fetch(url).then((response) => response.text());
  html.then((html) => {
    const matches = html.match(regex);
    if (matches) {
      cb({
        title: matches[1],
        poster: matches[2],
        summary: matches[3]
      });
    }
  });
};

loadStreams = (url, cb) => {
  // Load video streams
  const regex = /<a href="([^"]+)">.*?(\w+)<\/a>/g;
  const html = fetch(url).then((response) => response.text());
  html.then((html) => {
    const matches = html.match(regex);
    if (matches) {
      cb({
        streams: matches.map((match) => match[1])
      });
    }
  });
};

export { getManifest, getHome, search, load, loadStreams };

Note that this code assumes the site has a similar structure to what you provided in the HTML. The `getHome` function extracts the Latest and Trending sections from the page, the `search` function simulates a search query on the site, the `load` function uses REGEX to extract film details, and the `loadStreams` function extracts video streams from the page.
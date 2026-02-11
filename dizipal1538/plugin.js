const MAIN_URL = "https://dizipal1538.com/"; // Replace with your main URL

function getManifest() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve({
        manifest: {
          version: "1.0",
          name: "SkyStream Plugin",
          description: "A plugin for SkyStream to enhance streaming experience.",
          iconUrl: "https://dizipal1538.com/assets/skystream.png",
          authors: ["Your Name"],
          license: "MIT",
        },
      });
    }, 2000);
  });
}

function getHome() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve({
        home: {
          title: "SkyStream Home",
          description: "Welcome to the SkyStream home page.",
          logoUrl: "https://dizipal1538.com/assets/skystream.png",
          links: [
            { label: "About", url: "/about" },
            { label: "Help", url: "/help" },
            { label: "Support", url: "/support" },
          ],
        },
      });
    }, 2000);
  });
}

function load(url, cb) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve({
        stream: {
          id: "stream1",
          name: "Stream 1",
          description: "Description of Stream 1.",
          url: `${MAIN_URL}/stream/stream1`,
          thumbnailUrl: "https://dizipal1538.com/assets/skystream.png",
          type: "video",
        },
      });
    }, 2000);
  });
}

function loadStreams(url, cb) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve({
        streams: [
          {
            id: "stream1",
            name: "Stream 1",
            description: "Description of Stream 1.",
            url: `${MAIN_URL}/stream/stream1`,
            thumbnailUrl: "https://dizipal1538.com/assets/skystream.png",
            type: "video",
          },
        ],
      });
    }, 2000);
  });
}

globalThis.getManifest = getManifest;
globalThis.getHome = getHome;
globalThis.load = load;
globalThis.loadStreams = loadStreams;
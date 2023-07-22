// Create a new observer
let observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      // Check if new nodes are added
      if (mutation.addedNodes) {
        mutation.addedNodes.forEach((node) => {
          // Only handle element nodes
          if (node.nodeType === 1) {
            // Check if the node is an image
            if (node.tagName === 'IMG') {
              // Handle the image
              handleImage(node);
            }
          }
        });
      }
    });
  });
  
  // Start observing the document with the configured parameters
  observer.observe(document, { childList: true, subtree: true });
  
  function handleImage(img) {
    console.log("Loading Data:");
    // Fetch the image over HTTP
    fetch(img.src)
      .then(response => {
        // Check if the image was fetched successfully
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.arrayBuffer();
      })
      .then(buffer => {
        // Create a SHA-256 hash of the image
        return window.crypto.subtle.digest('SHA-256', buffer);
      })
      .then(hashBuffer => {
        // Convert the hash to a string
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        console.log("Loading Data:" + hashHex);
      })
      .catch(e => {
        console.log('There has been a problem with your fetch operation: ' + e.message);
      });
  }
  
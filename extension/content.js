window.onload = function() {
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
        // Create a new Image object
        let image = new Image();
        // Set the src of the image
        image.src = img.src;
        // Wait for the image to load
        image.onload = function() {
          // Create a new canvas
          let canvas = document.createElement('canvas');
          // Set the width and height of the canvas
          canvas.width = image.width;
          canvas.height = image.height;
          // Get the 2D context of the canvas
          let context = canvas.getContext('2d');
          // Draw the image onto the canvas
          context.drawImage(image, 0, 0);
          // Get the image data from the canvas
          let imageData = context.getImageData(0, 0, canvas.width, canvas.height);
          // Get the pixel data from the image data
          let pixelData = imageData.data;
          // Create a SHA-256 hash of the pixel data
          window.crypto.subtle.digest('SHA-256', pixelData)
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
      }
    }      
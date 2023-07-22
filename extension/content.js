
window.onload = function () {
  let images = document.getElementsByTagName('img');
  for (let img of images) {
    handleImage(img);
  }
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
    // Create a new Image object
    let image = new Image();
    // Set the src of the image
    image.src = img.src;
    fetch(image.src)
      .then(response => response.blob())
      .then(blob => createImageBitmap(blob))
      .then(imageBitmap => {
        // Create a canvas
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        // Set the canvas size to the image size
        canvas.width = imageBitmap.width;
        canvas.height = imageBitmap.height;

        // Draw the image onto the canvas
        ctx.drawImage(imageBitmap, 0, 0);

        // Get the pixel data from the canvas
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const uint8Array = new Uint8Array(imageData.data.buffer)

        // Call the function and get the SHA-256 hash
        sha256(uint8Array).then(hash => {
          result = getImage(hash);
        });

      })
      .catch(error => console.log(error));
  }
}

async function sha256(buffer) {
  const digestBuffer = await window.crypto.subtle.digest('SHA-256', buffer);
  const hashArray = Array.from(new Uint8Array(digestBuffer));
  const hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
  return hashHex;
}

function getImage(representation) {
  console.log(representation)
  const data = "0x6ced1ae9" + representation;
  const contractAddress = "0x850ec3780cedfdb116e38b009d0bf7a1ef1b8b38"

  fetch('http://localhost:8545', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'eth_call',
      params: [{
        to: contractAddress,
        data: data
      }, 'latest']
    }),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(result => {
      console.log(result.result);
    })
    .catch(e => console.log('There was an error: ' + e));
}
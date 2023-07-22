// let provider = new ethers.providers.JsonRpcProvider('http://127.0.01:8545/');


// let abi = ["..."]; 
// let contractAddress = '...'; 

// Create a contract instance
// let contract = new ethers.Contract(contractAddress, abi, provider);

window.onload = function () {
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
          console.log(uint8Array, hash); // The SHA-256 hash of the image data

          // Call the contract's getImage function
          contract.getImage(hash).then((image) => {
            console.log(image);
          });
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

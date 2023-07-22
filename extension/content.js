window.onload = function () {
  let images = document.getElementsByTagName('img');
  for (let img of images) {
    handleImage(img.src);
  }

  // Handle divs with background images
  let divs = document.getElementsByTagName('div');
  for (let div of divs) {
    const style = window.getComputedStyle(div);
    const backgroundImage = style.getPropertyValue('background-image');
    if (backgroundImage && backgroundImage !== 'none') {
      const href = div.parentElement.getAttribute("href");

      if (href != null) {
        handleImage("https://photos.google.com" + href.slice(1));
      }
    }
  }

  // Create a new observer
  let observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      // Check if new nodes are added
      if (mutation.addedNodes) {
        mutation.addedNodes.forEach((node) => {
          // Only handle element nodes
          if (node.nodeType === 1) {
            // Check if the node is an image or a div with a background image
            if (node.tagName === 'IMG') {
              handleImage(node.src);
            } else if (node.tagName === 'DIV') {
              const style = window.getComputedStyle(node);
              const backgroundImage = style.getPropertyValue('background-image');
              if (backgroundImage && backgroundImage !== 'none') {
                const url = backgroundImage.slice(4, -1).replace(/['"]/g, '');
                handleImage(url);
              }
            }
          }
        });
      }
    });
  });

  // Start observing the document with the configured parameters
  observer.observe(document, { childList: true, subtree: true });
}

function handleImage(imageUrl) {
  console.log(imageUrl);
  fetch(imageUrl)
    .then(response => response.blob())
    .then(blob => createImageBitmap(blob))
    .then(imageBitmap => {
      // Create a canvas
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');

      // Set the canvas size to the image size
      canvas.width = imageBitmap.width;
      canvas.height = imageBitmap.height;
      console.log(imageUrl);
      console.log(canvas.width, canvas.height, "div");

      // Draw the image onto the canvas
      ctx.drawImage(imageBitmap, 0, 0);

      // Get the pixel data from the canvas
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const uint8Array = new Uint8Array(imageData.data.buffer)

      // Call the function and get the SHA-256 hash
      sha256(uint8Array).then(hash => {
        return getImage(hash);
      });

    })
    .then(result => {
      if (canvas.width > 64 && canvas.height > 64) {
        const lastBytes = parseInt(result.result.slice(-20), 16); // Last 10 bytes are the last 20 characters
        let color;
        if (lastBytes < Number.MAX_SAFE_INTEGER / 3) {
          color = 'red';
        } else if (lastBytes < (Number.MAX_SAFE_INTEGER / 3) * 2) {
          color = 'green';
        } else {
          color = 'blue';
        }
        ctx.fillStyle = color;
        ctx.fillRect(0, 0, 50, 50); // Draw a 50x50 rectangle in the top left corner
      }
      const body = document.querySelector('body');
      body.appendChild(canvas); // Append the canvas to the body
    })
    .catch(error => console.log(error));
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
      return result.result;
    })
    .catch(e => console.log('There was an error: ' + e));
}
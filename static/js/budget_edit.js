////////////////////////////// to update Partial when creating a new mesurement ling////////////
// Get the input fields
const nrInput = document.getElementById('nr');
const widthInput = document.getElementById('width');
const lengthInput = document.getElementById('length');
const heightInput = document.getElementById('height');
const partialInput = document.getElementById('partial');

// Define a function to update the partial value
function updatePartial() {
    const nr = nrInput.value;
    const width = widthInput.value;
    const length = lengthInput.value;
    const height = heightInput.value;
  
    const partial = parseInt(nr) * parseFloat(width) * parseFloat(length) * parseFloat(height);
  
    if (isNaN(partial)) {
      partialInput.value = " ";
    } else {
      partialInput.value = partial.toLocaleString('en-US', { minimumFractionDigits: 3 });
    }
  }
  
  // Add event listeners to the input fields
  nrInput.addEventListener('input', updatePartial);
  widthInput.addEventListener('input', updatePartial);
  lengthInput.addEventListener('input', updatePartial);
  heightInput.addEventListener('input', updatePartial);
  
  // Initial update
  updatePartial();

//////////////////////// Update dynamically the measurements lines ////////////////////////////////

function updateMeasurement(id, name, value) {
  const url = '/measurement_update/';
  const data = { id, name, value };
  console.log("This is the data sent: ", data);

  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
  };

  fetch(url, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    updatePartial_DJ(id, data.partial);
    updateGrandTotal(data.grand_total);
    updateWorkQuantity(data.grand_total);
  })
  .catch(error => {
    console.error('Error:', error);
    throw error; // re-throw the error
  });
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  function updatePartial_DJ(id, data_partial){
    const partialValue = data_partial;
    const partialTd = document.getElementById(`partial-${id}`);
    partialTd.innerText = partialValue;
  }

  function updateGrandTotal(grandTotal) {
    const grandTotalElement = document.getElementById('grand-total');
    grandTotalElement.textContent = grandTotal;
  }
  
  function updateWorkQuantity(grandTotal) {
    const workQuantityInput = document.querySelector(`input[id^="work-quantity-"]`);
    workQuantityInput.value = grandTotal;
  }





// function updateWorkQuantity(id) {
//   const inputElement = document.getElementById(`work-quantity-${id}`);
//   if (inputElement) {
//     const grandTotal = calculateTotalPartial();
//     inputElement.value = grandTotal.toFixed(3);
//   } else {
//     console.error(`Input element with id 'work-quantity-${id}' not found`);
//   }
//   try {
//     updateWorkQuantityInDB(id, grandTotal);
//   } catch (error) {
//     console.error('Error updating work quantity:', error);
//   }
// }

// function updateWorkQuantityInDB(workId, grandTotal) {
//   // Update the grand total in the DB
// }
const taskSelect = document.getElementById('task');
taskSelect.addEventListener('change', async () => {
  const taskId = taskSelect.value;
  const response = await fetch(`/get-task-details/${taskId}`);
  const taskDetails = await response.json();
  document.getElementById('task_name').textContent = taskDetails.name;
  document.getElementById('task_unit').textContent = taskDetails.unit;
  document.getElementById('task_price').textContent = taskDetails.price;

  const quantityInput = document.getElementById('quantity');
  quantityInput.addEventListener('input', () => {
    const inputValue = quantityInput.value;
    const quantity = parseFloat(inputValue);
    if (isNaN(quantity)) {
      console.error('Invalid quantity');
    } else {
      const amount = taskDetails.price * quantity;
      document.getElementById('amount').textContent = amount.toFixed(2);
    }
  });
});

function updateQuantity(workId, fieldName, currentValue, priceValue){
  const amountValue = priceValue * currentValue;
  // const inputElement = target.parentNode.querySelector(`#work-amount-${workId}`);
  const inputElement = document.getElementById(`work-amount-${workId}`);
  inputElement.value = amountValue;

  const url = `/updatework/`;
  const data = {
    'work_id': workId,
    'field_name': fieldName,
    'value': currentValue,
  };
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
    console.log(data.message);
    })
  .catch(error => {
    console.error('Error:', error);
    });

    console.log("data:", data);
};

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


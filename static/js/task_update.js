function updateTaskName(id, name, value) {
    
    const url = '/task_name_update/';

    const data = {
        'id': id,
        'name': name,
        'value': value,
    };
    
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
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
  }

function updateComponentQuantity(id, name, value) { 
  const url = '/task_component_quantity_update/';

  const data = {
      'id': id,
      'name': name,
      'value': value,
  };
  
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
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
}   

// Component update ////////////////////////////////
function updatePrice(priceId, fieldName, value){
  const url = `/updateprice/`;
  const data = {
    'price_id': priceId,
    'field_name': fieldName,
    'value': value,
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
}
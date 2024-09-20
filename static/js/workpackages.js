function updateWorkpackageField(id, name, value) {
    
    const url = '/workpackage_update/';

    const data = {
        'id': id,
        'name': name,
        //'value': value,
        'value': event.target.tagName === 'SELECT' ? event.target.options[event.target.selectedIndex].text : event.target.value,
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
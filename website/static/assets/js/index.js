function deleteClient(clientId) {
    fetch('/clients/delete',{
        method: 'POST',
        body: JSON.stringify({clientId: clientId})
    }).then((_res) => {
        window.location.href = "{{ url_for('views.client') }}";
    });
}

function updateClient(clientId) {
    fetch('/clients/update',{
        method: 'POST',
        body: JSON.stringify({clientId: clientId})
    }).then((_res) => {
        window.location.href = '/';
    });
}
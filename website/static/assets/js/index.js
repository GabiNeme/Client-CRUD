function deleteClient(clientId) {
    fetch('/client-delete',{
        method: 'POST',
        body: JSON.stringify({clientId: clientId})
    }).then((_res) => {
        window.location.href = '/';
    });
}

function updateClient(clientId) {
    fetch('/client-update',{
        method: 'POST',
        body: JSON.stringify({clientId: clientId})
    }).then((_res) => {
        window.location.href = '/';
    });
}
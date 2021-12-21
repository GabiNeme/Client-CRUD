function deleteClient(clientId) {
    fetch('/clients/delete',{
        method: 'POST',
        body: JSON.stringify({clientId: clientId})
    }).then((_res) => {
        window.location.href = "/clients";
    });
}

function deleteBankAccount(clientId, bankId) {
    fetch('/clients/details/deletebankaccount',{
        method: 'POST',
        body: JSON.stringify({bankId: bankId})
    }).then((_res) => {
        window.location.href = "/clients/details/".concat(clientId);
    });
}

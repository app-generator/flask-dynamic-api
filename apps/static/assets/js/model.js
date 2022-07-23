
document.querySelector('.list-group').addEventListener('click' , (e) => {
    if (e.target.nodeName === 'A') {
        if (e.target.className.includes('edit')) {
            editAction()
        } else if (e.target.className.includes('delete'))
            deleteAction(e.target.id)

    }
})

const deleteAction = (id) => {
    fetch(`/api/${id}`,{
        method: 'DELETE'
    })
        .then(response => response.json())
        .then(res => {console.log(res)})
        .catch(err => {console.log(err)})
}

const editAction =  () => {
    // get data from template
    document.getElementById('name').value = document.getElementById('model-name')
    document.getElementById('year').value = document.getElementById('model-detail')
}
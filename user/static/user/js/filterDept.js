document.addEventListener('DOMContentLoaded', function () {
    const companySelect = document.getElementById('id_company');
    const departmentSelect = document.getElementById('id_department');
    console.log(companySelect);

    companySelect.addEventListener('change', function () {
        const companyId = this.value;

        fetch(`/user/filter/dept/?company=${companyId}`)
            .then(response => response.json())
            .then(data => {
                departmentSelect.innerHTML = '';
                data.forEach(department => {
                    const option = document.createElement('option');
                    option.value = department.id;
                    option.textContent = department.name;
                    departmentSelect.appendChild(option);
                });
            });
    });
});

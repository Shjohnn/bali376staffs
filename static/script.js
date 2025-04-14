document.addEventListener('DOMContentLoaded', function () {
    // Sidebar menyusida qay sahifa tanlanganini avtomatik belgilash
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.sidebar ul li a');

    menuLinks.forEach(link => {
        if(link.getAttribute('href') === currentPath || link.getAttribute('href') === currentPath.split('/').pop()){
            link.parentElement.classList.add('active');
        }
    });

    // Barcha edit tugmalar uchun umumiy hodisa
    let editBtns = document.querySelectorAll(".edit-btn");

    editBtns.forEach(function(btn) {
        btn.addEventListener("click", function() {
            let row = this.closest("tr");
            let data = row.children[0].innerText; // Birinchi ustun qiymati olinadi
            alert("Tahrirlash uchun tanlangan qiymat: " + data);
            // Bu joyga backend bilan aloqador qo'shimcha kod yozishingiz mumkin.
        });
    });
});
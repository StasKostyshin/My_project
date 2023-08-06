function toggleDropdown() {
    var dropdownContent = document.querySelector(".dropdown-content");
    dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
    }

    function showContent(contentId) {
        var content = document.getElementById(contentId);
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            dropdowns[i].style.display = "none";
            }
            content.style.display = "block";
    }

function toggleDropdownMenu() {
    var dropdownContentMenu = document.querySelector('.dropdown-content-menu');
    dropdownContentMenu.style.display = dropdownContentMenu.style.display === 'block' ? 'none' : 'block';
    }

    function showContentMenu(contentId) {
        var content = document.getElementById(contentId);
        var dropdowns = document.getElementsByClassName("dropdown-content-menu");
        for (var i = 0; i < dropdowns.length; i++) {
            dropdowns[i].style.display = "none";
        }
            content.style.display = "block";
    }





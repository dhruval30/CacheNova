

const exampleNavbarContent = [
    {title: "Introduction", link: "some-link" },
    {title: "What you should already know", link: "some-link" },
    {title: "JavaScript and Java", link: "some-link" },
    {title: "Hello World", link: "some-link" },
    {title: "Variables", link: "some-link" },
];

function populateNavbar(content) {
    const navbarList = document.querySelector('#navbar .navlist');
    navbarList.innerHTML = ''; // Clear existing content

    content.forEach(item => {
        const listItem = document.createElement('li');
        const link = document.createElement('a');
        link.classList.add('nav-link');
        link.href = `#${item.link}`;
        link.textContent = item.title;
        listItem.appendChild(link);
        navbarList.appendChild(listItem);
    });
}

populateNavbar(exampleNavbarContent);

document.getElementById('toggleNav').addEventListener('click', function() {
    document.getElementById('navbar').classList.toggle('active');
});



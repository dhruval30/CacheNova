
    // Add an event listener to trigger the search when Enter key is pressed
    document.querySelector('.searchtext').addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        handleSearch();
      }
    });

    // Function to handle the search
    async function handleSearch() {
      console.log("Search triggered.");
      
      // Show loading screen
      const loadingScreen = document.querySelector('.loading-screen');
      loadingScreen.style.display = 'flex';
      
      try {
        // Make a fetch request to your Python backend
        const response = await fetch('/your-python-endpoint');
        
        // Check if the response is successful
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        
        // Parse the JSON response
        const data = await response.json();
        
        // Clear existing popup cards
        const popupContainer = document.querySelector('.popup-container');
        popupContainer.innerHTML = '';
        
        // Populate cards with the subjects and links
        data.forEach((item, index) => {
          console.log("Displaying card for subject:", item.subject);
          displayPopupCard(item.subject, item.link, index, popupContainer);
        });
      } catch (error) {
        console.error('Error:', error.message);
      } finally {
        // Hide loading screen after 3 seconds
        setTimeout(() => {
          loadingScreen.style.display = 'none';
        }, 3000);
      }
    }

    function displayPopupCard(subject, link, index, container) {
      const card = document.createElement('div');
      card.classList.add('popup-card');
      card.innerHTML = `<a href="${link}" target="_blank">${subject}</a>`;
      
      // Append the card to the container
      container.appendChild(card);

      // Determine the position of the card based on its index
      const topPosition = 50 + index * 60; // Adjust as needed
      
      // Set the position of the card
      card.style.top = `${topPosition}px`;

      setTimeout(() => {
        card.classList.add('show');
      }, 100);
    }
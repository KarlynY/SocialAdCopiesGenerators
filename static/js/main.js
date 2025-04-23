document.getElementById('adForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Show loading state
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').innerHTML = '';
    
    const formData = {
        companyName: document.getElementById('companyName').value,
        landingUrl: document.getElementById('landingUrl').value,
        productType: document.getElementById('productType').value,
        aiModel: document.getElementById('aiModel').value
    };

    try {
        const response = await fetch('/generate-ads', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }

        // Display the generated ad copies
        displayAdCopies(data);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while generating ad copies. Please try again.');
    } finally {
        // Hide loading state
        document.getElementById('loading').classList.add('hidden');
    }
});

function displayAdCopies(data) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = ''; // Clear previous results
    
    // Create platform tabs
    const tabsContainer = document.createElement('div');
    tabsContainer.className = 'platform-tabs';
    
    // Create a section for each platform
    for (const [platform, content] of Object.entries(data)) {
        // Create tab button
        const tabButton = document.createElement('button');
        tabButton.className = 'tab-btn';
        tabButton.setAttribute('data-platform', platform);
        tabButton.textContent = platform.charAt(0).toUpperCase() + platform.slice(1);
        tabsContainer.appendChild(tabButton);
        
        const platformSection = document.createElement('div');
        platformSection.className = 'platform-section';
        platformSection.id = platform;
        
        try {
            const ads = JSON.parse(content);
            
            // Create a card for each ad
            for (const [adKey, ad] of Object.entries(ads)) {
                const adCard = document.createElement('div');
                adCard.className = 'ad-copy';
                
                adCard.innerHTML = `
                    <h3>${ad.headline}</h3>
                    <div class="copy-content">
                        <p>${ad.description}</p>
                        <p class="cta"><strong>Call to Action:</strong> ${ad.cta}</p>
                    </div>
                    <button class="copy-button" onclick="copyToClipboard(this)">Copy</button>
                `;
                
                platformSection.appendChild(adCard);
            }
        } catch (error) {
            // If there was an error parsing the JSON, display the error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = content;
            platformSection.appendChild(errorDiv);
        }
        
        resultsContainer.appendChild(platformSection);
    }
    
    // Add tabs container before the results
    resultsContainer.insertBefore(tabsContainer, resultsContainer.firstChild);
    
    // Add click handlers for tabs
    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and sections
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.platform-section').forEach(section => section.classList.remove('active'));
            
            // Add active class to clicked button and corresponding section
            button.classList.add('active');
            const platform = button.getAttribute('data-platform');
            document.getElementById(platform).classList.add('active');
        });
    });
    
    // Activate first tab by default
    const firstTab = document.querySelector('.tab-btn');
    if (firstTab) {
        firstTab.click();
    }
}

function copyToClipboard(button) {
    const adCard = button.closest('.ad-copy');
    const headline = adCard.querySelector('h3').textContent;
    const description = adCard.querySelector('.copy-content p').textContent;
    const cta = adCard.querySelector('.cta').textContent;
    
    const textToCopy = `${headline}\n\n${description}\n\n${cta}`;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        button.textContent = 'Copied!';
        button.classList.add('copied');
        setTimeout(() => {
            button.textContent = 'Copy';
            button.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy text to clipboard');
    });
} 
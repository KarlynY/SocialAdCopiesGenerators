document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('adForm');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const platformTabs = document.querySelectorAll('.tab-btn');
    const platformSections = document.querySelectorAll('.platform-section');

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            companyName: document.getElementById('companyName').value,
            landingUrl: document.getElementById('landingUrl').value,
            productType: document.getElementById('productType').value,
            aiModel: document.getElementById('aiModel').value
        };

        // Show loading state
        loading.classList.remove('hidden');
        results.classList.add('hidden');

        try {
            const response = await fetch('/generate-ads', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                displayResults(data);
            } else {
                showError(data.error || 'Something went wrong');
            }
        } catch (error) {
            showError(error.message);
        } finally {
            loading.classList.add('hidden');
        }
    });

    // Handle platform tab switching
    platformTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const platform = tab.dataset.platform;
            
            // Update active tab
            platformTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Update active section
            platformSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === platform) {
                    section.classList.add('active');
                }
            });
        });
    });

    // Copy text to clipboard
    async function copyToClipboard(text, button) {
        try {
            await navigator.clipboard.writeText(text);
            button.textContent = 'Copied!';
            button.classList.add('copied');
            setTimeout(() => {
                button.textContent = 'Copy';
                button.classList.remove('copied');
            }, 2000);
        } catch (err) {
            showError('Failed to copy text');
        }
    }

    // Show error message
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        form.insertAdjacentElement('beforebegin', errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }

    // Display results function
    function displayResults(data) {
        results.classList.remove('hidden');

        // Clear previous results
        document.querySelectorAll('.ad-copies').forEach(container => {
            container.innerHTML = '';
        });

        // Display results for each platform
        Object.entries(data).forEach(([platform, content]) => {
            const container = document.querySelector(`#${platform} .ad-copies`);
            const adCopies = JSON.parse(content);

            Object.entries(adCopies).forEach(([adKey, adContent]) => {
                const adCopy = document.createElement('div');
                adCopy.className = 'ad-copy';
                
                // Create copy button
                const copyButton = document.createElement('button');
                copyButton.className = 'copy-button';
                copyButton.textContent = 'Copy';
                
                // Create the full ad text
                const fullAdText = `${adContent.headline}\n\n${adContent.description}\n\n${adContent.cta}`;
                
                // Add click handler for copy button
                copyButton.addEventListener('click', () => copyToClipboard(fullAdText, copyButton));
                
                adCopy.innerHTML = `
                    <h3>${adKey.toUpperCase()}</h3>
                    <div class="copy-content">
                        <p><strong>Headline:</strong> ${adContent.headline}</p>
                        <p><strong>Description:</strong> ${adContent.description}</p>
                        <p class="cta"><strong>Call to Action:</strong> ${adContent.cta}</p>
                    </div>
                `;
                
                // Add copy button to the header
                const header = adCopy.querySelector('h3');
                header.appendChild(copyButton);
                
                container.appendChild(adCopy);
            });
        });
    }
}); 
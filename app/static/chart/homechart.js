document.addEventListener('DOMContentLoaded', async function () {
    // Constants and initial values
    const perthLat = -31.9505;
    const perthLng = 115.8605;
    let selectedCity = 'Perth';  // Default city

    // Mapping weacher code to  weather svg icon
    function getWeatherIconName(code, isDay) {
        const base = isDay ? '-day' : '-night';
        const map = {
            0: `clear${base}`,
            1: `cloudy-1${base}`,
            2: `cloudy-2${base}`,
            3: `cloudy`,
            45: `fog${base}`,
            48: `fog`,
            51: `rainy-1${base}`,
            53: `rainy-2${base}`,
            55: `rainy-3${base}`,
            56: `frost${base}`,
            57: `frost`,
            61: `rainy-1${base}`,
            63: `rainy-2${base}`,
            65: `rainy-3${base}`,
            66: `frost${base}`,
            67: `frost`,
            71: `snowy-1${base}`,
            73: `snowy-2${base}`,
            75: `snowy-3${base}`,
            80: `rainy-1${base}`,
            81: `rainy-2${base}`,
            82: `rainy-3${base}`,
            95: `thunderstorms`,
            96: `hail`,
            99: `severe-thunderstorm`
        };
        return map[code] || 'wind'; // Default icon for unknown codes
    }

    // Map Initialization
    const map = L.map('map', {
        worldCopyJump: true,
        maxBounds: [[-38, 112], [-20, 129]],
        maxBoundsViscosity: 1.0,
        bounceAtZoomLimits: true,
        inertia: true
    }).setView([perthLat, perthLng], 7);
    
    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        minZoom: 5,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> ',
        bounds: [[-35, 112], [-20, 129]]
    }).addTo(map);

    const markersLayer = L.layerGroup().addTo(map);
    const resourcesBaseUrl = "/static/chart/resources"; // Base URL for resources

    // // Data Loading (legacy code, faster to use local data))
    // const cities = await fetch(`${resourcesBaseUrl}/city_lat_lon.json`).then(r => r.json());
    // const weatherData = await fetch(`${resourcesBaseUrl}/wa_weather_data.json`).then(r => r.json());
    
    // Data Loading (api from db)
    const weatherData = await fetch('/api/weather_data').then(r => r.json());
    const cities = await fetch('/api/city_lat_lon').then(r => r.json());

    // Date Setup
    const dates = weatherData.map(w => w.date);
    const minDate = dates.reduce((a, b) => a < b ? a : b);
    const maxDate = dates.reduce((a, b) => a > b ? a : b);
    const today = new Date().toISOString().split('T')[0];
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayStr = yesterday.toISOString().split('T')[0];

    // UI Elements Initialization
    const dateSlider = document.getElementById('date-slider');
    const dateRange = document.getElementById('date-range');
    const selectedDateSpan = document.getElementById('selected-date');
    const sidebar = $('#sidebar');
    const toggleBtn = $('#toggle-sidebar');
    const showSidebarBtn = $('#show-sidebar');

    // Date Controls Setup
    const minTimestamp = new Date(minDate).getTime();
    const maxTimestamp = new Date(maxDate).getTime();
    const yesterdayTimestamp = new Date(yesterdayStr).getTime();

    dateRange.min = minTimestamp;
    dateRange.max = maxTimestamp;
    dateRange.value = yesterdayTimestamp;
    dateSlider.min = minDate;
    dateSlider.max = maxDate;
    dateSlider.value = yesterdayStr;
    selectedDateSpan.textContent = new Date(yesterdayStr).toLocaleDateString();

    // Marker Functions
    function addWeatherIcon(lat, lng, iconName, weatherData) {
        const icon = L.icon({
            iconUrl: `${resourcesBaseUrl}/animated_weather/${iconName}.svg`,
            iconSize: [75, 75],
            iconAnchor: [50, 50]
        });

        const marker = L.marker([lat, lng], { icon: icon });
        const popupContent = `
            <div class="weather-popup">
            <h4>${weatherData.city}</h4>
            <p>Date: ${weatherData.date}</p>
            <p>Temperature: ${weatherData.temperature_low}°C  ~  ${weatherData.temperature_high}°C</p>
            <p>Weather: <img class="weather-icon" src="${resourcesBaseUrl}/animated_weather/${iconName}.svg" />  ${weatherData.weather_description}</p>
            <p>Wind: ${weatherData.wind_speed} km/h </p> 
            </div>
        `;

        const popup = L.popup({
            className: 'weather-popup-container',
            offset: [0, -10],
            closeButton: false
        }).setContent(popupContent);

        marker.bindPopup(popup);
        marker.on('mouseover', function (e) { this.openPopup(); });
        marker.on('mouseout', function (e) {
            setTimeout(() => { this.closePopup(); }, 2000);
        });
        marker.on('click', function(e) {
            selectedCity = weatherData.city;
            updateForecastSeries(dateSlider.value);
            document.querySelector('.content-box h2').textContent = `Weather Forecast - ${selectedCity}`;
        });

        return marker;
    }

    // Update Functions
    function updateForecastSeries(selectedDate) {
        const dates = [];
        const currentDate = new Date(selectedDate);
        
        currentDate.setDate(currentDate.getDate() - 1);
        dates.push(currentDate.toISOString().split('T')[0]);
        
        currentDate.setDate(currentDate.getDate() + 1);
        for (let i = 0; i < 4; i++) {
            dates.push(currentDate.toISOString().split('T')[0]);
            currentDate.setDate(currentDate.getDate() + 1);
        }

        const forecastDays = document.querySelectorAll('.forecast-day');
        dates.forEach((date, index) => {
            const weather = weatherData.find(w => w.date === date && w.city === selectedCity);
            if (weather) {
                const iconName = getWeatherIconName(weather.weather, weather.is_day);
                const forecastDay = forecastDays[index];
                forecastDay.querySelector('.forecast-icon').src = `${resourcesBaseUrl}/animated_weather/${iconName}.svg`;
                forecastDay.querySelector('.forecast-temp').textContent = 
                    `${weather.temp_min}°C ~ ${weather.temp_max}°C`;
            }
        });

        document.querySelector('.content-box h2').textContent = `Weather Forecast - ${selectedCity}`;
    }

    function updateMarkers(selectedDate) {
        markersLayer.clearLayers();
        cities.forEach(cityObj => {
            const { city, lat, lon } = cityObj;
            const weather = weatherData.find(w => w.city === city && w.date === selectedDate);
            if (weather) {
                const iconName = getWeatherIconName(weather.weather, weather.is_day);
                const weatherInfo = {
                    city: city,
                    date: selectedDate,
                    temperature_low: weather.temp_min || 'N/A',
                    temperature_high: weather.temp_max || 'N/A',
                    weather_description: iconName.split('-')[0] || 'N/A',
                    wind_speed: weather.wind_speed || 'N/A',
                    wind_direction: weather.wind_direction || ''
                };
                
                const marker = addWeatherIcon(lat, lon, iconName, weatherInfo);
                marker.addTo(markersLayer);
            }
        });
        updateForecastSeries(selectedDate);
    }

    function updateDate(date) {
        const dateStr = new Date(date).toISOString().split('T')[0];
        dateSlider.value = dateStr;
        dateRange.value = new Date(date).getTime();
        selectedDateSpan.textContent = new Date(date).toLocaleDateString();
        updateMarkers(dateStr);
    }

    // Event Listeners
    dateSlider.addEventListener('change', (e) => updateDate(e.target.value));
    dateRange.addEventListener('input', (e) => updateDate(Number(e.target.value)));
    
    // Sidebar Event Handlers
    toggleBtn.on('click', () => sidebar.addClass('collapsed'));
    showSidebarBtn.on('click', () => sidebar.removeClass('collapsed'));
    
    $(document).on('click', function (e) {
        if (!$(e.target).closest('#sidebar').length &&
            !$(e.target).closest('#show-sidebar').length &&
            sidebar.is(':visible') &&
            !sidebar.hasClass('collapsed')) {
            sidebar.addClass('collapsed');
        }
    });

    function checkScreenSize() {
        if (window.innerWidth <= 768) {
            sidebar.addClass('collapsed');
        }
    }

    // Travel Tips Button Handler
    document.getElementById('get-tips-btn').addEventListener('click', async function() {
        const cityName = selectedCity;
        const tipsList = document.getElementById('travel-tips-list');
        const spotsList = document.getElementById('main-spots-list');
        const tipsSection = document.getElementById('travel-tips-section');
        const spotsSection = document.getElementById('main-spots-section');
        tipsSection.style.display = 'none';
        spotsSection.style.display = 'none';
        tipsList.innerHTML = '<li>Loading...</li>';
        spotsList.innerHTML = '';

        try {
            const resp = await fetch(`/api/travel_tips?city_name=${encodeURIComponent(cityName)}`);
            const data = await resp.json();
            tipsList.innerHTML = '';
            spotsList.innerHTML = '';
            if (data.length > 0) {
                spotsSection.style.display = '';
                tipsSection.style.display = '';
                // Main Spots
                if (data[0].main_spots.length > 0) {
                    data[0].main_spots.forEach(spot => {
                        const li = document.createElement('li');
                        li.textContent = spot;
                        spotsList.appendChild(li);
                    });
                } else {
                    spotsList.innerHTML = '<li>No main spots available for this city.</li>';
                }
                // Travel Tips
                if (data[0].tips.length > 0) {
                    data[0].tips.forEach(tip => {
                        const li = document.createElement('li');
                        li.textContent = tip;
                        tipsList.appendChild(li);
                    });
                } else {
                    tipsList.innerHTML = '<li>No tips available for this city.</li>';
                }
            } else {
                spotsSection.style.display = '';
                tipsSection.style.display = '';
                spotsList.innerHTML = '<li>No main spots available for this city.</li>';
                tipsList.innerHTML = '<li>No tips available for this city.</li>';
            }
        } catch (err) {
            spotsSection.style.display = '';
            tipsSection.style.display = '';
            tipsList.innerHTML = '<li>Error loading tips.</li>';
        }
    });

    // Share Button Handler
    document.getElementById('share-to-btn').addEventListener('click', function() {
        // Get selected city and date
        const city = encodeURIComponent(selectedCity);
        const date = encodeURIComponent(document.getElementById('date-slider').value);
    
        // Find the weather data for the selected city and date
        const weather = weatherData.find(w => w.city === selectedCity && w.date === date);
        let params = `city=${city}&date=${date}`;
        if (weather) {
            const iconName = getWeatherIconName(weather.weather, weather.is_day);
            params +=
            `&temperature_low=${encodeURIComponent(weather.temp_min || 'N/A')}` +
            `&temperature_high=${encodeURIComponent(weather.temp_max || 'N/A')}` +
            `&weather_description=${encodeURIComponent(iconName.split('-')[0] || 'N/A')}` +
            `&wind_speed=${encodeURIComponent(weather.wind_speed || 'N/A')}` +
            `&wind_direction=${encodeURIComponent(weather.wind_direction || '')}` +
            `&icon_name=${encodeURIComponent(iconName)}`;
        }
        // Redirect to /share with all parameters
        window.location.href = `/share?${params}`;
    });

    // Initial Setup
    sidebar.addClass('collapsed');
    checkScreenSize();
    $(window).resize(checkScreenSize);
    updateMarkers(yesterdayStr);
});